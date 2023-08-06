from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Union

from coiote.utils import AutoNamedEnum


class HandlerType(str, AutoNamedEnum):
    Kafka = "kafka"
    Webhook = "webhook"


class DeviceLifecycleEventType(str, AutoNamedEnum):
    Created = "deviceCreated"
    FirstRegistration = "deviceFirstRegistration"
    UpdatedViaWrite = "deviceUpdatedViaWrite"
    UpdatedViaFota = "deviceUpdatedViaFota"
    Deleted = "deviceDeleted"


@dataclass
class DataEventHandlerFilter:
    lwm2mUrls: List[str]
    type: str = "dataModel"


@dataclass
class LifecycleEventHandlerFilter:
    eventTypes: List[DeviceLifecycleEventType]
    type: str = "lifecycle"


EventHandlerFilter = Union[DataEventHandlerFilter, LifecycleEventHandlerFilter]


@dataclass
class EventHandlerUpdateData:
    name: Optional[str] = None
    enabled: Optional[bool] = None
    description: Optional[str] = None
    filter: Optional[EventHandlerFilter] = None
    connectionConfig: Optional[dict] = None


@dataclass
class BasicAuth:
    user: str
    password: str
    type: str = "basic"


@dataclass
class Token:
    token: str
    type: str = "token"


WebhookAuth = Union[BasicAuth, Token]


class WebhookFormat(str, AutoNamedEnum):
    Generic = "generic"
    InfluxDb = "influxDb"


class WebhookMethod(str, AutoNamedEnum):
    Post = "post"
    Put = "put"
    Patch = "patch"


@dataclass
class WebhookConnectionConfig:
    uri: str
    auth: Optional[WebhookAuth] = None
    additionalHeaders: Dict[str, str] = field(default_factory=dict)
    format: Optional[WebhookFormat] = None
    method: Optional[WebhookMethod] = WebhookMethod.Post


@dataclass
class KafkaFromPropertiesConnectionConfig:
    topic: str
    headers: Dict[str, str] = field(default_factory=dict)
    type: str = "domainProperty"


@dataclass
class CustomKafkaConnectionConfig:
    value: str
    topic: str
    headers: Dict[str, str] = field(default_factory=dict)
    type: str = "custom"


KafkaConnectionConfig = Union[KafkaFromPropertiesConnectionConfig,
                              CustomKafkaConnectionConfig]


@dataclass
class EventHandlerConfiguration:
    type: HandlerType
    name: str
    enabled: bool
    filter: EventHandlerFilter
    connectionConfig: Union[WebhookConnectionConfig, KafkaConnectionConfig]
    domain: Optional[str] = None
    description: Optional[str] = None


@dataclass
class EventHandler(EventHandlerConfiguration):
    id: Optional[str] = None


@dataclass
class HandlerTestResult:
    successful: bool
    message: Optional[str] = None
