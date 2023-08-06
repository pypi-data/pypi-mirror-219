from __future__ import annotations

import json
import logging
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable

from confluent_kafka.schema_registry import Schema, SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer, AvroSerializer
from confluent_kafka.serialization import SerializationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError

from .utils import CitizenKError, annotate_function

if TYPE_CHECKING:
    from .citizenk import CitizenK

logger = logging.getLogger(__name__)


class JSONSchema(BaseModel):
    class Config:
        # This allows adding new optional properites to the schema
        schema_extra = {"additionalProperties": False}


class TopicDir(Enum):
    INPUT = 1
    OUTPUT = 2
    BIDIR = 3


class SchemaType(Enum):
    JSON = 1
    AVRO = 2
    PROTOBUF = 3


class Topic:
    def __init__(
        self,
        app: CitizenK,
        name: str,
        value_type: BaseModel,
        topic_dir: TopicDir = TopicDir.INPUT,
        schema_type: SchemaType = SchemaType.JSON,
        subject_name: str | None = None,
        partitioner: Callable[[str | bytes], int] = None,
    ):
        self.app = app
        self.name = name
        self.value_type = value_type
        self.topic_dir = topic_dir
        self.schema_type = schema_type
        self.subject_name = (
            f"{name}-value".lower() if subject_name is None else subject_name
        )
        self.schema_id = None
        self.partitioner = partitioner
        self.partition_count = None
        self.replica_count = None
        if self.app.auto_generate_apis:
            self._generate_apis()

        # Register topic schema
        self.serializer = None
        self.deserializer = None
        self.manage_schema()

    def info(self, lags: dict[str, int] = {}, assignments: dict[str, list[int]] = {}):
        topic_info = {
            "name": self.name,
            "dir": self.topic_dir.name,
            "value": self.value_type.__name__,
            "subject": self.subject_name,
            "schema_type": self.schema_type.name,
            "partitions": self.partition_count,
            "replicas": self.replica_count,
        }
        if self.name in lags:
            topic_info["lag"] = lags[self.name]
        if self.name in assignments:
            topic_info["assignments"] = assignments[self.name]
        return topic_info

    def _generate_apis(self):
        if self.topic_dir in [TopicDir.OUTPUT, TopicDir.BIDIR]:

            def f(value: int, key: str = "", count: int = 1, partition: int = -1):
                for n in range(count):
                    if key == "":
                        self.send(value, str(n), partition)
                    else:
                        self.send(value, key, partition)
                return value

            annotate_function(
                f,
                name=f"send_to_topic_{self.name}",
                doc=f"This endpoint sends value to topic {self.name}",
                argument_types={"value": self.value_type},
            )
            self.app.add_api_route(
                path=f"{self.app.api_router_prefix}/topic/{self.name}",
                response_class=JSONResponse,
                methods=["POST"],
                endpoint=f,
            )

    def send(
        self,
        value: dict[Any, Any] | BaseModel,
        key: str | bytes = None,
        partition: int = -1,
    ):
        if self.app.is_sink():
            raise CitizenKError("Trying to produce in a sink app")
        if self.topic_dir == TopicDir.INPUT:
            raise CitizenKError("Trying to produce to an input topic")
        value = self.serialize(value)
        if value is None:
            return False
        if not isinstance(key, (str, bytes)):
            raise CitizenKError("Key should be a either a str or bytes", key)
        if self.partitioner is not None and partition == -1:
            partition = self.partitioner(key)
        # TODO: Add schema to headers
        self.app.producer.produce(
            topic=self.name, value=value, key=key, partition=partition
        )
        return True

    def manage_schema(self):
        """Handle schema registry registration and validation"""
        # https://yokota.blog/2021/03/29/understanding-json-schema-compatibility/
        if self.app.schema_registry_url is not None:
            # Schema registration
            schema_registry_conf = {"url": self.app.schema_registry_url}
            schema_registry_client = SchemaRegistryClient(schema_registry_conf)
            schema = Schema(
                schema_str=self.value_type.schema_json(),
                schema_type=self.schema_type.name,
            )
            if self.topic_dir != TopicDir.OUTPUT:
                if self.schema_type == SchemaType.AVRO:
                    self.serializer = AvroSerializer(schema_registry_client, schema)
                schema_id = schema_registry_client.register_schema(
                    subject_name=self.subject_name, schema=schema
                )
                logger.info("Schema id registered for %s is %s", self.name, schema_id)
                self.schema_id = schema_id
            # Schema validation
            if self.topic_dir != TopicDir.INPUT:
                if self.schema_type == SchemaType.AVRO:
                    self.deserializer = AvroDeserializer(schema_registry_client, schema)

                if not schema_registry_client.test_compatibility(
                    subject_name=self.subject_name, schema=schema
                ):
                    logger.error(
                        "Schema for %s is not compatible with the latest schema registry",
                        self.name,
                    )
                else:
                    logger.info(
                        "Schema for %s is compatible with the latest schema registry",
                        self.name,
                    )
        elif self.schema_type == SchemaType.AVRO:
            raise CitizenKError("AVRO Schema requires a schema registry")

    def serialize(self, value: dict[Any, Any] | BaseModel) -> bytes:
        if isinstance(value, dict):
            try:
                value = self.value_type(**value)
            except ValidationError as exp:
                logger.error("Error while validating send value %s", exp.json())
                return None
        if not isinstance(value, BaseModel):
            raise CitizenKError("Value should be a pydantic model", value)
        if self.schema_type == SchemaType.JSON:
            return value.json()
        elif self.schema_type == SchemaType.AVRO:
            try:
                return self.serializer(value)
            except SerializationError:
                logger.error("Failed to serialise value %s", value)
                return None
        else:
            raise CitizenKError("No available serializer")

    def deserialize(self, value: bytes) -> BaseModel:
        # convert bytes to dict
        if self.schema_type == SchemaType.JSON:
            try:
                value = json.loads(value)
            except json.decoder.JSONDecodeError as exp:
                logger.error("For now, CitizenK only supports JSON values %s", exp)
                return None
        elif self.schema_type == SchemaType.AVRO:
            try:
                value = self.deserializer(value)
            except SerializationError as exp:
                logger.error("Failed to deserialise value %s", exp.json())
                return None
        else:
            raise CitizenKError("No available serializer")

        # convert dict to pydantic model
        try:
            value = self.value_type(**value)
        except ValidationError as exp:
            logger.error("Error while validating received value %s", exp.json())
            return None
        return value

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name
