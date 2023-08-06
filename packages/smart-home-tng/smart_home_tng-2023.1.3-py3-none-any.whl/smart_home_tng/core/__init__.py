"""
Core components of Smart Home - The Next Generation.

Smart Home - TNG is a Home Automation framework for observing the state
of entities and react to changes. It is based on Home Assistant from
home-assistant.io and the Home Assistant Community.

Copyright (c) 2022-2023, Andreas Nixdorf

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program.  If not, see
http://www.gnu.org/licenses/.
"""

# pylint: disable=unused-variable

from . import helpers
from .abort_flow import AbortFlow
from .abstract_oauth2_implementation import AbstractOAuth2Implementation
from .abstract_outh2_flow_handler import AbstractOAuth2FlowHandler
from .action_condition_platform import ActionConditionPlatform
from .action_platform import ActionPlatform
from .action_trace import ActionTrace
from .adapter import Adapter
from .add_entities_callback import AddEntitiesCallback
from .alarm_control_panel import AlarmControlPanel
from .alexa import Alexa
from .api_config import ApiConfig
from .application_credentials_platform import ApplicationCredentialsPlatform
from .area import Area
from .area_registry import AreaRegistry
from .async_zero_conf import AsyncZeroConf
from .audio_bit_rate import AudioBitRate
from .audio_channel import AudioChannel
from .audio_codec import AudioCodec
from .audio_format import AudioFormat
from .audio_sample_rate import AudioSampleRate
from .auth_component import AuthComponent
from .authorization_server import AuthorizationServer
from .automation_component import AutomationComponent
from .backup_platform import BackupPlatform
from .base_notification_service import BaseNotificationService
from .base_service_info import BaseServiceInfo
from .base_tracker_entity import BaseTrackerEntity
from .binary_sensor import BinarySensor
from .blueprint_base import BlueprintBase
from .blueprint_component import BlueprintComponent
from .blueprint_inputs_base import BlueprintInputsBase
from .browse_media import BrowseMedia, BrowseMediaSource
from .button import Button
from .caching_static_resource import CachingStaticResource
from .callback import callback, is_callback
from .callback_type import CallbackType
from .camera import Camera
from .change_listener import ChangeListener
from .change_set_listener import ChangeSetListener
from .check_config_error import CheckConfigError
from .circular_dependency import CircularDependency
from .client_credential import ClientCredential
from .climate import Climate
from .cloud_component import CloudComponent
from .cloud_connection_state import CloudConnectionState
from .cloud_not_available import CloudNotAvailable
from .cloud_not_connected import CloudNotConnected
from .collection_change_set import CollectionChangeSet
from .collection_error import CollectionError
from .components import Components
from .condition_checker_type import ConditionCheckerType
from .condition_error import ConditionError
from .condition_error_container import ConditionErrorContainer
from .condition_error_index import ConditionErrorIndex
from .condition_error_message import ConditionErrorMessage
from .condition_platform import ConditionPlatform
from .config import Config
from .config_entries import ConfigEntries
from .config_entries_flow_manager import ConfigEntriesFlowManager
from .config_entry import ConfigEntry
from .config_entry_auth_failed import ConfigEntryAuthFailed
from .config_entry_change import ConfigEntryChange
from .config_entry_disabler import ConfigEntryDisabler
from .config_entry_not_ready import ConfigEntryNotReady
from .config_entry_source import ConfigEntrySource
from .config_entry_state import ConfigEntryState
from .config_error import ConfigError
from .config_errors import ConfigErrors
from .config_flow import ConfigFlow
from .config_flow_platform import ConfigFlowPlatform
from .config_source import ConfigSource
from .config_type import ConfigType
from .config_validation import ConfigValidation
from .const import Const
from .context import Context
from .conversation import Conversation
from .coordinator_entity import CoordinatorEntity
from .core_state import CoreState
from .cover import Cover
from .data_update_coordinator import DataUpdateCoordinator
from .debouncer import Debouncer
from .deleted_device import DeletedDevice
from .dependency_error import DependencyError
from .device import Device
from .device_automation import DeviceAutomation
from .device_info import DeviceInfo
from .device_not_found import DeviceNotFound
from .device_registry import DeviceRegistry
from .device_registry_entry_disabler import DeviceRegistryEntryDisabler
from .device_registry_entry_type import DeviceRegistryEntryType
from .device_tracker import DeviceTracker
from .device_tracker_component import DeviceTrackerComponent
from .dhcp_matcher import DHCPMatcher
from .dhcp_matcher_optional import DHCPMatcherOptional
from .dhcp_matcher_required import DHCPMatcherRequired
from .dhcp_service_info import DhcpServiceInfo
from .diagnostics import Diagnostics
from .diagnostics_platform import DiagnosticsPlatform
from .discovery_dict import DiscoveryDict
from .discovery_info_type import DiscoveryInfoType
from .domain_blueprints_base import DomainBlueprintsBase
from .energy_component import EnergyComponent
from .energy_platform import EnergyPlatform
from .entity import Entity
from .entity_category import EntityCategory
from .entity_component import EntityComponent
from .entity_description import EntityDescription
from .entity_filter import EntityFilter
from .entity_platform import EntityPlatform
from .entity_platform_state import EntityPlatformState
from .entity_registry import EntityRegistry
from .entity_registry_entry import EntityRegistryEntry
from .entity_registry_entry_disabler import EntityRegistryEntryDisabler
from .entity_registry_entry_hider import EntityRegistryEntryHider
from .entity_registry_items import EntityRegistryItems
from .entity_selector import EntitySelector
from .entity_selector_config import EntitySelectorConfig
from .event import Event
from .event_bus import EventBus
from .event_origin import EventOrigin
from .event_tracker import EventTracker
from .extended_json_encoder import ExtendedJsonEncoder
from .extra_stored_data import ExtraStoredData
from .fan import Fan
from .flow_dispatcher import FlowDispatcher
from .flow_error import FlowError
from .flow_handler import FlowHandler
from .flow_manager import FlowManager
from .flow_manager_index_view import FlowManagerIndexView
from .flow_manager_resource_view import FlowManagerResourceView
from .flow_result import FlowResult
from .flow_result_type import FlowResultType
from .forecast import Forecast
from .frontend_component import FrontendComponent
from .google_assistant import GoogleAssistant
from .gps_type import GpsType
from .group_component import GroupComponent
from .group_entity import GroupEntity
from .group_integration_registry import GroupIntegrationRegistry
from .group_platform import GroupPlatform
from .helpers.selectors import register_selectors
from .http_client import HttpClient
from .humidifier import Humidifier
from .id_less_collection import IDLessCollection
from .id_manager import IDManager
from .image import Image
from .input import Input
from .input_number import InputNumber
from .integration import Integration
from .integration_error import IntegrationError
from .integration_not_found import IntegrationNotFound
from .integration_platform import IntegrationPlatform
from .intent import Intent
from .intent_manager import IntentManager
from .interruptible_thread_pool_executor import InterruptibleThreadPoolExecutor
from .invalid_device_automation_config import InvalidDeviceAutomationConfig
from .invalid_entity_format_error import InvalidEntityFormatError
from .invalid_state_error import InvalidStateError
from .ip_ban import IpBan
from .ipv4_configured_address import IPv4ConfiguredAddress
from .ipv6_configured_address import IPv6ConfiguredAddress
from .item_not_found import ItemNotFound
from .json_encoder import JsonEncoder
from .json_type import JsonType
from .keyed_rate_limit import KeyedRateLimit
from .lazy_partial_state import LazyPartialState
from .light import Light
from .loader_error import LoaderError
from .local_oauth2_implementation import LocalOAuth2Implementation
from .location_info import LocationInfo
from .lock import Lock
from .logbook_callback import LogbookCallback
from .logbook_component import LogbookComponent
from .logbook_platform import LogbookPlatform
from .manifest import Manifest
from .max_length_exceeded import MaxLengthExceeded
from .media_player import MediaPlayer
from .media_player_component import MediaPlayerComponent
from .media_source import MediaSource
from .media_source_component import MediaSourceComponent
from .media_source_error import MediaSourceError
from .media_source_item import MediaSourceItem
from .media_source_platform import MediaSourcePlatform
from .missing_integration_frame import MissingIntegrationFrame
from .mock_request import MockRequest
from .mock_stream_reader import MockStreamReader
from .module_wrapper import ModuleWrapper
from .mqtt import MQTT
from .mqtt_service_info import MqttServiceInfo, ReceivePayloadType
from .network_component import NetworkComponent
from .no_entity_specified_error import NoEntitySpecifiedError
from .no_url_available_error import NoURLAvailableError
from .notify import Notify
from .notify_component import NotifyComponent
from .notify_platform import NotifyPlatform
from .oauth2_provider import OAuth2Provider
from .oauth2_session import OAuth2Session
from .observable_collection import ObservableCollection
from .onboarding_component import OnboardingComponent
from .operation_not_allowed import OperationNotAllowed
from .options_flow import OptionsFlow
from .options_flow_manager import OptionsFlowManager
from .ouath2_authorize_callback_view import OAuth2AuthorizeCallbackView
from .persistent_notification_component import PersistentNotificationComponent
from .person_component import PersonComponent
from .platform import Platform
from .platform_implementation import PlatformImplementation
from .platform_not_ready import PlatformNotReady
from .play_media import PlayMedia
from .protocol import Protocol
from .query_type import QueryType
from .queue_logging_handler import QueueLoggingHandler
from .read_only_dict import ReadOnlyDict
from .recorder_component import RecorderComponent
from .recorder_filters_base import RecorderFiltersBase
from .recorder_history_base import RecorderHistoryBase
from .recorder_platform import RecorderPlatform
from .recorder_statistics_base import RecorderStatisticsBase
from .registry import Registry
from .reload_service_helper import ReloadServiceHelper
from .reproduce_state_platform import ReproduceStatePlatform
from .request_data_validator import RequestDataValidator
from .required_parameter_missing import RequiredParameterMissing
from .requirements_not_found import RequirementsNotFound
from .restore_entity import RestoreEntity
from .restore_sensor import RestoreSensor
from .restore_state_data import RestoreStateData
from .restored_extra_data import RestoredExtraData
from .restored_trace import RestoredTrace
from .rtsp_to_web_rtc_provider_type import RtspToWebRtcProviderType
from .runtime_config import RuntimeConfig
from .scanner_entity import ScannerEntity
from .scene import Scene
from .scene_platform import ScenePlatform
from .schema_flow import SchemaFlow
from .script_component import ScriptComponent
from .script_condition import ScriptCondition
from .script_variables import ScriptVariables
from .scripts import Scripts
from .secrets import Secrets
from .select import Select
from .select_option_dict import SelectOptionDict
from .select_selector import SelectSelector
from .select_selector_config import SelectSelectorConfig
from .select_selector_mode import SelectSelectorMode
from .selected_entities import SelectedEntities
from .selector import Selector
from .sensor import Sensor
from .sensor_component import SensorComponent
from .serialization_error import SerializationError
from .service import Service
from .service_call import ServiceCall
from .service_data_type import ServiceDataType
from .service_description import ServiceDescription
from .service_not_found import ServiceNotFound
from .service_params import ServiceParams
from .service_registry import ServiceRegistry
from .service_target_selector import ServiceTargetSelector
from .setup_manager import SetupManager
from .significant_change import SignificantChange
from .significant_change_platform import SignificantChangePlatform
from .singleton import Singleton
from .siren import Siren
from .smart_home_controller import SmartHomeController
from .smart_home_controller_component import SmartHomeControllerComponent
from .smart_home_controller_error import SmartHomeControllerError
from .smart_home_controller_http import SmartHomeControllerHTTP
from .smart_home_controller_job import SmartHomeControllerJob
from .smart_home_controller_job_type import SmartHomeControllerJobType
from .smart_home_controller_site import SmartHomeControllerSite
from .smart_home_controller_view import SmartHomeControllerView
from .solar_forecast_type import SolarForecastType
from .speech_metadata import SpeechMetadata
from .speech_result import SpeechResult
from .speech_result_state import SpeechResultState
from .speech_to_text_platform import SpeechToTextPlatform
from .speech_to_text_provider import SpeechToTextProvider
from .sql_session import SqlSession
from .ssdp import SSDP
from .state import State
from .state_machine import StateMachine
from .state_type import StateType
from .statistic_business_model import Statistic
from .stop_reason import StopReason
from .storage_collection import StorageCollection
from .storage_collection_web_socket import StorageCollectionWebSocket
from .store import Store
from .stored_state import StoredState
from .stream_base import StreamBase
from .stream_component import StreamComponent, StreamEndedError, StreamWorkerError
from .stream_type import StreamType
from .sun import Sun
from .sun_listener import SunListener
from .switch import Switch
from .system_health_component import SystemHealthComponent
from .system_health_platform import SystemHealthPlatform
from .system_health_registration import SystemHealthRegistration
from .tag_component import TagComponent
from .template import Template
from .template_environment import TemplateEnvironment
from .template_environment_type import TemplateEnvironmentType
from .template_error import TemplateError
from .template_vars_type import TemplateVarsType
from .thread_with_exception import ThreadWithException
from .throttle import Throttle
from .timeout_manager import TimeoutManager
from .timer import Timer
from .toggle import Toggle
from .trace import Trace
from .trace_base import TraceBase
from .trace_component import TraceComponent
from .trace_element import TraceElement
from .track_states import TrackStates
from .track_template import TrackTemplate
from .track_template_result import TrackTemplateResult
from .track_template_result_listener import TrackTemplateResultListener
from .tracker_entity import TrackerEntity
from .tracker_source_type import TrackerSourceType
from .trigger import Trigger
from .trigger_action_type import TriggerActionType
from .trigger_data import TriggerData
from .trigger_info import TriggerInfo
from .trigger_platform import TriggerPlatform
from .tts import TTS
from .tuple_wrapper import TupleWrapper
from .turbo_jpeg_singleton import TurboJPEGSingleton
from .unauthorized import Unauthorized
from .undefined_substitution import UndefinedSubstitution
from .unit_conversion import (
    BaseUnitConverter,
    DataRateConverter,
    DistanceConverter,
    ElectricCurrentConverter,
    ElectricPotentialConverter,
    EnergyConverter,
    InformationConverter,
    MassConverter,
    PowerConverter,
    PressureConverter,
    SpeedConverter,
    TemperatureConverter,
    UnitlessRatioConverter,
    VolumeConverter,
)
from .unit_system import UnitSystem
from .unknown_entry import UnknownEntry
from .unknown_flow import UnknownFlow
from .unknown_handler import UnknownHandler
from .unknown_step import UnknownStep
from .unknown_user import UnknownUser
from .unresolvable import Unresolvable
from .update import Update
from .update_failed import UpdateFailed
from .url_manager import UrlManager
from .usb_component import UsbComponent
from .usb_service_info import UsbServiceInfo
from .vacuum import Vacuum
from .weather_entity import WeatherEntity
from .weather_entity_description import WeatherEntityDescription
from .web_socket import WebSocket
from .webhook_component import WebhookComponent
from .write_error import WriteError
from .yaml_collection import YamlCollection
from .yaml_loader import YamlLoader
from .zero_conf import ZeroConf
from .zeroconf_component import ZeroconfComponent
from .zeroconf_service_info import ZeroconfServiceInfo
from .zone import Zone
from .zone_component import ZoneComponent

register_selectors()
