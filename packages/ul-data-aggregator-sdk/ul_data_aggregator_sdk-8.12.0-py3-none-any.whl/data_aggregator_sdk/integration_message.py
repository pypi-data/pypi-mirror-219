from datetime import datetime
from enum import Enum, IntEnum, unique
from typing import Optional, List, Tuple, Dict, Any

from pydantic import BaseModel, UUID4, root_validator, Field  # pylint: disable=no-name-in-module
from ul_api_utils.errors import ValidateApiError
from ul_api_utils.utils.api_method import ApiMethod
from unipipeline.message.uni_message import UniMessage

from data_aggregator_sdk.constants.enums import IntegrationV0MessageEvent, IntegrationV0MessageMetaBSChannelProtocol, \
    ProtocolEnum, IntegrationV0MessageErrorType
from data_aggregator_sdk.types.device import NetworkSysTypeEnum


class ProfileGranulation(Enum):
    """
    Enumeration of time granulations for profile packets
    """
    MINUTE_01 = "MINUTE_01"
    MINUTE_02 = "MINUTE_02"
    MINUTE_03 = "MINUTE_03"
    MINUTE_04 = "MINUTE_04"
    MINUTE_05 = "MINUTE_05"
    MINUTE_06 = "MINUTE_06"
    MINUTE_10 = "MINUTE_10"
    MINUTE_12 = "MINUTE_12"
    MINUTE_15 = "MINUTE_15"
    MINUTE_20 = "MINUTE_20"
    MINUTE_30 = "MINUTE_30"
    MINUTE_60 = "MINUTE_60"

    SECOND_01 = "SECOND_01"
    SECOND_02 = "SECOND_02"
    SECOND_03 = "SECOND_03"
    SECOND_04 = "SECOND_04"
    SECOND_05 = "SECOND_05"
    SECOND_06 = "SECOND_06"
    SECOND_10 = "SECOND_10"
    SECOND_12 = "SECOND_12"
    SECOND_15 = "SECOND_15"
    SECOND_20 = "SECOND_20"
    SECOND_30 = "SECOND_30"


class ProfileKind(Enum):
    """
    Enumeration of profile types:
        energy A-, A+, R-, R+
        full power S
        active power P
        reactive power Q
        voltage U
        current I
        frequency F
        point factor K
    """
    # active generated energy A-
    ENERGY_A_N = 'ENERGY_A_N'
    ENERGY_A_N_A = 'ENERGY_A_N_A'
    ENERGY_A_N_B = 'ENERGY_A_N_B'
    ENERGY_A_N_C = 'ENERGY_A_N_C'
    # active consumed energy A+
    ENERGY_A_P = 'ENERGY_A_P'
    ENERGY_A_P_A = 'ENERGY_A_P_A'
    ENERGY_A_P_B = 'ENERGY_A_P_B'
    ENERGY_A_P_C = 'ENERGY_A_P_C'
    # reactive generated energy R-
    ENERGY_R_N = 'ENERGY_R_N'
    ENERGY_R_N_A = 'ENERGY_R_N_A'
    ENERGY_R_N_B = 'ENERGY_R_N_B'
    ENERGY_R_N_C = 'ENERGY_R_N_C'
    # reactive consumed energy R+
    ENERGY_R_P = 'ENERGY_R_P'
    ENERGY_R_P_A = 'ENERGY_R_P_A'
    ENERGY_R_P_B = 'ENERGY_R_P_B'
    ENERGY_R_P_C = 'ENERGY_R_P_C'
    # full power S
    FULL_POWER_ABC = 'FULL_POWER_ABC'
    FULL_POWER_A = 'FULL_POWER_A'
    FULL_POWER_B = 'FULL_POWER_B'
    FULL_POWER_C = 'FULL_POWER_C'
    FULL_POWER_MIN_ABC = 'FULL_POWER_MIN_ABC'
    FULL_POWER_MIN_A = 'FULL_POWER_MIN_A'
    FULL_POWER_MIN_B = 'FULL_POWER_MIN_B'
    FULL_POWER_MIN_C = 'FULL_POWER_MIN_C'
    FULL_POWER_MAX_ABC = 'FULL_POWER_MAX_ABC'
    FULL_POWER_MAX_A = 'FULL_POWER_MAX_A'
    FULL_POWER_MAX_B = 'FULL_POWER_MAX_B'
    FULL_POWER_MAX_C = 'FULL_POWER_MAX_C'
    # active power P
    ACTIVE_POWER_ABC = 'ACTIVE_POWER_ABC'
    ACTIVE_POWER_A = 'ACTIVE_POWER_A'
    ACTIVE_POWER_B = 'ACTIVE_POWER_B'
    ACTIVE_POWER_C = 'ACTIVE_POWER_C'
    ACTIVE_POWER_MIN_ABC = 'ACTIVE_POWER_MIN_ABC'
    ACTIVE_POWER_MIN_A = 'ACTIVE_POWER_MIN_A'
    ACTIVE_POWER_MIN_B = 'ACTIVE_POWER_MIN_B'
    ACTIVE_POWER_MIN_C = 'ACTIVE_POWER_MIN_C'
    ACTIVE_POWER_MAX_ABC = 'ACTIVE_POWER_MAX_ABC'
    ACTIVE_POWER_MAX_A = 'ACTIVE_POWER_MAX_A'
    ACTIVE_POWER_MAX_B = 'ACTIVE_POWER_MAX_B'
    ACTIVE_POWER_MAX_C = 'ACTIVE_POWER_MAX_C'
    # reactive power Q
    REACTIVE_POWER_ABC = 'REACTIVE_POWER_ABC'
    REACTIVE_POWER_A = 'REACTIVE_POWER_A'
    REACTIVE_POWER_B = 'REACTIVE_POWER_B'
    REACTIVE_POWER_C = 'REACTIVE_POWER_C'
    REACTIVE_POWER_MIN_ABC = 'REACTIVE_POWER_MIN_ABC'
    REACTIVE_POWER_MIN_A = 'REACTIVE_POWER_MIN_A'
    REACTIVE_POWER_MIN_B = 'REACTIVE_POWER_MIN_B'
    REACTIVE_POWER_MIN_C = 'REACTIVE_POWER_MIN_C'
    REACTIVE_POWER_MAX_ABC = 'REACTIVE_POWER_MAX_ABC'
    REACTIVE_POWER_MAX_A = 'REACTIVE_POWER_MAX_A'
    REACTIVE_POWER_MAX_B = 'REACTIVE_POWER_MAX_B'
    REACTIVE_POWER_MAX_C = 'REACTIVE_POWER_MAX_C'
    # voltage U
    VOLTAGE_ABC = 'VOLTAGE_ABC'
    VOLTAGE_A = 'VOLTAGE_A'
    VOLTAGE_B = 'VOLTAGE_B'
    VOLTAGE_C = 'VOLTAGE_C'
    VOLTAGE_MIN_ABC = 'VOLTAGE_MIN_ABC'
    VOLTAGE_MIN_A = 'VOLTAGE_MIN_A'
    VOLTAGE_MIN_B = 'VOLTAGE_MIN_B'
    VOLTAGE_MIN_C = 'VOLTAGE_MIN_C'
    VOLTAGE_MAX_ABC = 'VOLTAGE_MAX_ABC'
    VOLTAGE_MAX_A = 'VOLTAGE_MAX_A'
    VOLTAGE_MAX_B = 'VOLTAGE_MAX_B'
    VOLTAGE_MAX_C = 'VOLTAGE_MAX_C'
    # current I
    CURRENT_ABC = 'CURRENT_ABC'
    CURRENT_A = 'CURRENT_A'
    CURRENT_B = 'CURRENT_B'
    CURRENT_C = 'CURRENT_C'
    CURRENT_MIN_ABC = 'CURRENT_MIN_ABC'
    CURRENT_MIN_A = 'CURRENT_MIN_A'
    CURRENT_MIN_B = 'CURRENT_MIN_B'
    CURRENT_MIN_C = 'CURRENT_MIN_C'
    CURRENT_MAX_ABC = 'CURRENT_MAX_ABC'
    CURRENT_MAX_A = 'CURRENT_MAX_A'
    CURRENT_MAX_B = 'CURRENT_MAX_B'
    CURRENT_MAX_C = 'CURRENT_MAX_C'
    # frequency F
    FREQUENCY_ABC = 'FREQUENCY_ABC'
    FREQUENCY_A = 'FREQUENCY_A'
    FREQUENCY_B = 'FREQUENCY_B'
    FREQUENCY_C = 'FREQUENCY_C'
    FREQUENCY_MIN_ABC = 'FREQUENCY_MIN_ABC'
    FREQUENCY_MIN_A = 'FREQUENCY_MIN_A'
    FREQUENCY_MIN_B = 'FREQUENCY_MIN_B'
    FREQUENCY_MIN_C = 'FREQUENCY_MIN_C'
    FREQUENCY_MAX_ABC = 'FREQUENCY_MAX_ABC'
    FREQUENCY_MAX_A = 'FREQUENCY_MAX_A'
    FREQUENCY_MAX_B = 'FREQUENCY_MAX_B'
    FREQUENCY_MAX_C = 'FREQUENCY_MAX_C'
    # power factor K
    POWER_FACTOR_ABC = 'POWER_FACTOR_ABC'
    POWER_FACTOR_A = 'POWER_FACTOR_A'
    POWER_FACTOR_B = 'POWER_FACTOR_B'
    POWER_FACTOR_C = 'POWER_FACTOR_C'
    POWER_FACTOR_MIN_ABC = 'POWER_FACTOR_MIN_ABC'
    POWER_FACTOR_MIN_A = 'POWER_FACTOR_MIN_A'
    POWER_FACTOR_MIN_B = 'POWER_FACTOR_MIN_B'
    POWER_FACTOR_MIN_C = 'POWER_FACTOR_MIN_C'
    POWER_FACTOR_MAX_ABC = 'POWER_FACTOR_MAX_ABC'
    POWER_FACTOR_MAX_A = 'POWER_FACTOR_MAX_A'
    POWER_FACTOR_MAX_B = 'POWER_FACTOR_MAX_B'
    POWER_FACTOR_MAX_C = 'POWER_FACTOR_MAX_C'

    def __repr__(self) -> str:
        return f'{type(self).__name__}.{self.name}'


class ResourceType(Enum):
    """
    Enumeration of resource types for consumption and generation info of integration message data
    """
    COMMON = 'COMMON'
    ENERGY_ACTIVE = 'ENERGY_ACTIVE'
    ENERGY_REACTIVE = 'ENERGY_REACTIVE'


class CounterType(Enum):
    """
    Enumeration of counter types for consumption and generation info of integration message data
    """
    COMMON = 'COMMON'
    ENERGY_PHASE_A = 'ENERGY_PHASE_A'
    ENERGY_PHASE_B = 'ENERGY_PHASE_B'
    ENERGY_PHASE_C = 'ENERGY_PHASE_C'


class IntegrationV0MessageClock(BaseModel):
    clock_id: int = Field(
        -1,
        title="Clock ID",
        description="Device timestamp clock ID",
    )
    value: datetime = Field(
        title="Clock value",
        description="Device timestamp clock value",
    )


class IntegrationV0MessageUptime(BaseModel):
    channel_id: int = Field(
        1,
        title="Channel ID",
        description="Device channel Id",
    )
    uptime_s: float = Field(
        title="Uptime seconds",
        description="Uptime seconds value",
    )


class IntegrationV0MessageRelay(BaseModel):
    relay_id: int = Field(
        -1,
        title="Relay ID",
        description="Device relay ID",
    )
    value: bool = Field(
        title="Relay state",
        description="Device relay state",
    )


MINUTES_IN_DAY_CONST = 24 * 60
SECONDS_IN_DAY_CONST = MINUTES_IN_DAY_CONST * 60


GRANULATION_TO_SECONDS_DELTA_MAP = {
    ProfileGranulation.MINUTE_01: 60,
    ProfileGranulation.MINUTE_02: 120,
    ProfileGranulation.MINUTE_03: 180,
    ProfileGranulation.MINUTE_04: 240,
    ProfileGranulation.MINUTE_05: 300,
    ProfileGranulation.MINUTE_06: 360,
    ProfileGranulation.MINUTE_10: 600,
    ProfileGranulation.MINUTE_12: 720,
    ProfileGranulation.MINUTE_15: 900,
    ProfileGranulation.MINUTE_20: 1200,
    ProfileGranulation.MINUTE_30: 1800,
    ProfileGranulation.MINUTE_60: 3600,

    ProfileGranulation.SECOND_01: 1,
    ProfileGranulation.SECOND_02: 2,
    ProfileGranulation.SECOND_03: 3,
    ProfileGranulation.SECOND_04: 4,
    ProfileGranulation.SECOND_05: 5,
    ProfileGranulation.SECOND_06: 6,
    ProfileGranulation.SECOND_10: 10,
    ProfileGranulation.SECOND_12: 12,
    ProfileGranulation.SECOND_15: 15,
    ProfileGranulation.SECOND_20: 20,
    ProfileGranulation.SECOND_30: 30,
}

assert len(GRANULATION_TO_SECONDS_DELTA_MAP.keys()) == len(ProfileGranulation)

GRANULATION_LENGTH_MAP = {
    ProfileGranulation.MINUTE_01: MINUTES_IN_DAY_CONST,
    ProfileGranulation.MINUTE_02: MINUTES_IN_DAY_CONST / 2,
    ProfileGranulation.MINUTE_03: MINUTES_IN_DAY_CONST / 3,
    ProfileGranulation.MINUTE_04: MINUTES_IN_DAY_CONST / 4,
    ProfileGranulation.MINUTE_05: MINUTES_IN_DAY_CONST / 5,
    ProfileGranulation.MINUTE_06: MINUTES_IN_DAY_CONST / 6,
    ProfileGranulation.MINUTE_10: MINUTES_IN_DAY_CONST / 10,
    ProfileGranulation.MINUTE_12: MINUTES_IN_DAY_CONST / 12,
    ProfileGranulation.MINUTE_15: MINUTES_IN_DAY_CONST / 15,
    ProfileGranulation.MINUTE_20: MINUTES_IN_DAY_CONST / 20,
    ProfileGranulation.MINUTE_30: MINUTES_IN_DAY_CONST / 30,
    ProfileGranulation.MINUTE_60: MINUTES_IN_DAY_CONST / 60,

    ProfileGranulation.SECOND_01: SECONDS_IN_DAY_CONST,
    ProfileGranulation.SECOND_02: SECONDS_IN_DAY_CONST / 2,
    ProfileGranulation.SECOND_03: SECONDS_IN_DAY_CONST / 3,
    ProfileGranulation.SECOND_04: SECONDS_IN_DAY_CONST / 4,
    ProfileGranulation.SECOND_05: SECONDS_IN_DAY_CONST / 5,
    ProfileGranulation.SECOND_06: SECONDS_IN_DAY_CONST / 6,
    ProfileGranulation.SECOND_10: SECONDS_IN_DAY_CONST / 10,
    ProfileGranulation.SECOND_12: SECONDS_IN_DAY_CONST / 12,
    ProfileGranulation.SECOND_15: SECONDS_IN_DAY_CONST / 15,
    ProfileGranulation.SECOND_20: SECONDS_IN_DAY_CONST / 20,
    ProfileGranulation.SECOND_30: SECONDS_IN_DAY_CONST / 30,
}

assert len(GRANULATION_LENGTH_MAP.keys()) == len(ProfileGranulation)


class IntegrationV0MessageProfile(BaseModel):
    type: ProfileKind = Field(
        title="Profile type",
        description="Profile type is like side view of collecting data for device (ex. 'VOLTAGE_ABC', 'ENERGY_A_N')",
    )
    granulation: ProfileGranulation = Field(
        title="Profile granulation",
        description="Granulation is detailing of collecting data, resolution of graph by device (ex. 1 hour (MINUTE_60), 1 second (SECONDS_01))",
    )
    values: Tuple[Optional[float], ...] = Field(
        title="Profile values",
        description="Sequence of collected values for profile packet",
    )

    @root_validator
    def validate_profile(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        granulation = values['granulation']
        len_values = len(values['values'])

        if GRANULATION_LENGTH_MAP[granulation] == len_values:
            return values
        raise ValidateApiError(msg=f"Incorrect profile type and granulation: Granulation is {granulation}, Length values={len_values}")


class IntegrationV0MessageConsumption(BaseModel):
    tariff: int = Field(
        -1,
        title="Consumption tariff",
        description="Consumption tariff number",
    )
    counter_type: CounterType = Field(
        title="Counter type",
        description="Consumption counter type",
    )
    resource_type: ResourceType = Field(
        title="Resource type",
        description="Consumption resource type",
    )
    channel: int = Field(
        title="Channel",
        description="Consumption channel number for collecting info",
    )
    value: float = Field(
        title="Channel value",
        description="Consumption channel value",
    )
    overloading_value: Optional[float] = Field(
        None,
        title="Overloading channel value",
        description="Consumption channel overloading value. "
                    "If overloading_value = None - value is fully precise - must replace current. if not None - overload potentially could be",
    )


class IntegrationV0MessageGeneration(BaseModel):
    tariff: int = Field(
        -1,
        title="Generation tariff",
        description="Generation tariff number",
    )
    counter_type: CounterType = Field(
        title="Counter type",
        description="Generation counter type",
    )
    resource_type: ResourceType = Field(
        title="Resource type",
        description="Generation resource type",
    )

    value: float = Field(
        title="Generation value",
        description="Generation channel value",
    )
    overloading_value: Optional[float] = Field(
        None,
        title="Overloading value",
        description="Generation overloading value. "
                    "If overloading_value = None - value is fully precise - must replace current. if not None - overload potentially could be",
    )


@unique
class BatteryId(IntEnum):
    """
    Battery Ids enumeration for identification of battery module meter
    """
    COMMON = -1
    # RESERVED = 0
    CAPACITOR = 1
    RADIO_MODULE = 2


class IntegrationV0MessageCurrentBatteryLevel(BaseModel):
    battery_id: int = Field(
        BatteryId.COMMON,
        title="Battery ID",
        description="Device battery ID",
    )
    voltage: float = Field(
        title="Battery voltage",
        description="Device battery voltage value",
    )


class IntegrationV0MessageCurrentTemperature(BaseModel):
    value: float = Field(
        title="Temperature value",
        description="Float value of environment current temperature",
    )


class IntegrationV0MessageMetaNbFiBS0(BaseModel):
    station_id: int = Field(
        title="Station ID",
        description="Station unique identifier",
    )
    modem_id: int = Field(
        title="Modem ID",
        description="Modem unique identifier",
    )
    encrypted: bool = Field(
        title="Channel encryption",
        description="Index availability of channel encryption",
    )
    freq_channel: int = Field(
        title="Channel frequency",
        description="Working channel frequency",
    )
    freq_expect: int = Field(
        title="Expected frequency",
        description="Expected channel frequency",
    )
    message_id: int = Field(
        title="Message ID",
        description="Message unique identifier",
    )
    nbfi_f_ask: int = Field(
        title="NBFI frequency ASK",
        description="NBFI frequency ASK",
    )
    nbfi_iterator: int = Field(
        title="NBFI iterator",
        description="NBFI iterator",
    )
    nbfi_multi: int = Field(
        title="NBFI multi",
        description="NBFI multi",
    )
    nbfi_system: int = Field(
        title="NBFI system",
        description="NBFI system",
    )
    signal_rssi: int = Field(
        title="RSSI signal level",
        description="RSSI signal level of antenna",
    )
    signal_snr: int = Field(
        title="SNR signal level",
        description="SNR signal level",
    )
    time_detected: int = Field(
        title="Time detection",
        description="Time when signal was detected",
    )
    time_published: int = Field(
        title="Time publishing value",
        description="Time when signal was published",
    )
    ul_phy: int = Field(
        title="UL phy",
        description="UL phy",
    )
    baudrate: int = Field(
        -1,  # -1 for old protocols
        title="Baud rate",
        description="Baud rate of channel",
    )
    sdr: int = Field(
        -1,  # -1 for old protocols
        title="SDR number",
        description="SDR numeric number",
    )
    message_type: IntegrationV0MessageMetaBSChannelProtocol = Field(
        IntegrationV0MessageMetaBSChannelProtocol.nbfi,
        title="Message type",
        description="Message protocol type",
    )


class IntegrationV0MessageMetaBSHttp(BaseModel):
    freq: int = Field(
        title="Frequency",
        description="Frequency",
    )
    freq_channel: int = Field(
        title="Frequency channel",
        description="Channel frequency number",
    )
    sdr: int = Field(
        title="SDR number",
        description="SDR number",
    )
    baud_rate: int = Field(
        title="Baud rate",
        description="Baud rate of channel",
    )
    rssi: int = Field(
        title="RSSI value",
        description="RSSI signal level of antenna",
    )
    snr: int = Field(
        title="SNR value",
        description="SNR signal level",
    )

    mac: int = Field(
        title="MAC",
        description="MAC number",
    )
    station_id: UUID4 = Field(
        title="Station ID",
        description="Station unique identifier",
    )
    station_serial_number: int = Field(
        title="Station serial number",
        description="Station serial number",
    )

    dt_detected: datetime = Field(
        title="Detection datetime",
        description="Datetime of detection",
    )
    dt_published: datetime = Field(
        title="Publishing datetime",
        description="Datetime of publishing",
    )
    channel_protocol: IntegrationV0MessageMetaBSChannelProtocol = Field(
        title="Channel protocol",
        description="Channel protocol",
    )


class IntegrationV0MessageMetaNBIoT(BaseModel):
    modem_id: Optional[int] = Field(
        None,
        title="Modem ID",
        description="Modem identifier",
    )
    ip_address: str = Field(
        title="IP address",
        description="IP address of modem device",
    )
    port: int = Field(
        title="Port",
        description="Pointer to network connection",
    )


class IntegrationV0MessageData(BaseModel):
    is_valid: bool = Field(
        True,  # TODO: remove default
        title="Valid message",
        description="Validation integration message data field",
    )
    dt: Optional[datetime] = Field(  # TODO: remove optional
        None,  # TODO: remove default
        title="Datetime message",
        description="Datetime integration message field which shows when message was received",
    )
    battery: List[IntegrationV0MessageCurrentBatteryLevel] = Field(
        default_factory=list,
        title="Battery info",
        description="Structure which contains battery ID and voltage level for current device",
    )
    consumption: List[IntegrationV0MessageConsumption] = Field(
        default_factory=list,
        title="Consumption info",
        description="Structure which contains consumption info for current device",
    )
    generation: List[IntegrationV0MessageGeneration] = Field(
        default_factory=list,
        title="Generation info",
        description="Structure which contains generation info for current device",
    )
    profiles: List[IntegrationV0MessageProfile] = Field(
        default_factory=list,
        title="Profiles info",
        description="Structure which contains profiles info for current device",
    )
    events: List[IntegrationV0MessageEvent] = Field(
        default_factory=list,
        title="Events list",
        description="Events list which contains triggered events info for current device",
    )
    temperature: List[IntegrationV0MessageCurrentTemperature] = Field(
        default_factory=list,
        title="Temperature info",
        description="Structure which contains temperature info for current device",
    )
    relay: List[IntegrationV0MessageRelay] = Field(
        default_factory=list,
        title="Relay info",
        description="Structure which contains relay info for current device",
    )
    clock: List[IntegrationV0MessageClock] = Field(
        default_factory=list,
        title="Clock info",
        description="Structure which contains clock info for current device",
    )
    uptime: List[IntegrationV0MessageUptime] = Field(
        default_factory=list,
        title="Uptime info",
        description="Structure which contains uptime info for current device",
    )


class IntegrationMessageMetaIotAccountGateway(BaseModel):
    network_id: UUID4 = Field(
        title="Network ID",
        description="Network identifier",
    )
    gateway_id: UUID4 = Field(
        title="Gateway ID",
        description="Gateway identifier",
    )
    device_id: Optional[UUID4] = Field(
        None,
        title="Device ID",
        description="Device identifier",
    )
    protocol_id: Optional[UUID4] = Field(
        None,
        title="Protocol ID",
        description="Protocol identifier",
    )


class IntegrationMessageMetaRecycle(BaseModel):
    date: datetime = Field(
        title="Datetime recycle",
        description="Datetime field which contains packet recycle date",
    )


class IntegrationMessageMetaExternalApiDataInput(BaseModel):
    name: str = Field(
        ...,
        title='Api Integration name',
        description='Api Integration name',
    )
    uri: str = Field(
        ...,
        title='External api uri',
        description='External api uri',
    )
    path: str = Field(
        ...,
        title='External api path',
        description='External api path',
    )
    api_method: ApiMethod = Field(
        ...,
        title='Api Method',
        description='Api Method',
    )
    query_params: Optional[Dict[str, str]] = Field(
        None,
        title='Query Parameters',
        description='Query Parameters',
    )
    status_code: int = Field(
        ...,
        title='Request status code',
        description='Request status code',
    )
    body: Optional[str] = Field(
        None,
        title='Request Body',
        description='Request Body',
    )
    headers: Optional[Dict[str, str]] = Field(
        None,
        title='Request Headers',
        description='request headers',

    )
    current_dt: datetime = Field(
        ...,
        title="request response date and time",
        description="The current date and time of the sender at the time of sending",
    )


class IntegrationMessageMetaUniversalDataInput(BaseModel):
    user_id: UUID4 = Field(
        ...,
        title="Sender user identifier",     # ApiUser.id
        description="Uniq UUID of user",
    )    # DA token id
    name: str = Field(
        ...,
        title="Sender user name",       # ApiUser.name
        description="Name of user",
    )
    type: str = Field(
        ...,
        title="Sender type",        # ApiUser.type
        description="Name of sender type",
    )
    current_dt: datetime = Field(
        ...,
        title="Current sender date and time",
        description="The current date and time of the sender at the time of sending",
    )
    uptime_s: int = Field(
        ...,
        title="Count uninterrupted uptime seconds",
        description="Counter seconds of sender correct working time",
    )
    geo_longitude: float = Field(
        ...,
        title="Geographical longitude of sender",
        description="Geographical latitude coordinate at the time of sending",
    )
    geo_latitude: float = Field(
        ...,
        title="Geographical latitude of sender",
        description="Geographical latitude coordinate at the time of sending",
    )
    version: str = Field(
        ...,
        title="Sender version",
        description="Sender software / hardware version",
    )
    note: str = Field(
        ...,
        title="Note about sender",
        description="Any usefull information about sender",
    )
    ipv4: str = Field(
        ...,
        title='IPv4 sender address',
        description="A unique numerical identifier for every sender that send through the internet",
    )


class IntegrationV0MessageMeta(BaseModel):
    nbfi_bs0: Optional[IntegrationV0MessageMetaNbFiBS0] = Field(
        None,
        title="NBFi BS0 meta message structure",
        description="NBFi BS0 meta message structure",
    )
    nbiot: Optional[IntegrationV0MessageMetaNBIoT] = Field(
        None,
        title="NBIoT meta message",
        description="NBIoT meta message structure",
    )
    bs_http: Optional[IntegrationV0MessageMetaBSHttp] = Field(
        None,
        title="BS HTTP meta message",
        description="BS HTTP meta message structure",
    )
    universal_data_input: Optional[IntegrationMessageMetaUniversalDataInput] = Field(
        None,
        title="Universal data input meta",
        description="Universal data input meta structure",
    )
    external_api_data_input: Optional[IntegrationMessageMetaExternalApiDataInput] = Field(
        None,
        title="External api data input meta",
        description="External api data input meta structure",
    )
    iot_account_gateway: Optional[IntegrationMessageMetaIotAccountGateway] = Field(
        None,
        title="IoT account gateway",
        description="IoT account gateway structure",
    )
    recycle: Optional[IntegrationMessageMetaRecycle] = Field(
        None,
        title="Recycle info",
        description="Structure which contains integration message recycle date",
    )

    @root_validator()
    def check_meta_exists(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if not any((
            values.get('nbfi_bs0'),
            values.get('nbiot'),
            values.get('bs_http'),
            values.get('external_api_data_input'),
            values.get('universal_data_input'),
            values.get('iot_account_gateway'),
            values.get('recycle'),
        )):
            raise ValueError('one of meta sctructure must be set')
        return values


class IntegrationV0MessageError(BaseModel):
    error_message: str = Field(
        '',
        title="Error message",
        description="String with error description",
    )
    error_type: IntegrationV0MessageErrorType = Field(
        IntegrationV0MessageErrorType.none,
        title="Error type",
        description="This field contains error group name",
    )


class IntegrationV0MessageGateway(UniMessage):
    data: IntegrationV0MessageData = Field(
        title="Main data structure",
        description="Main data structure of message consists of some data structures with device load info such as battery, consumption, temperature, events and etc",
    )
    meta: IntegrationV0MessageMeta = Field(
        title="Meta data structure",
        description="Meta data structure of message consists of some data structures with some additional info for instance of device",
    )
    packet_type_name: str = Field(
        '',
        title="Packet type name",
        description="Each message contains packet type information",
    )
    id: Optional[UUID4] = Field(
        None,
        title="Message ID",
        description="Message ID which is UniMessage.id",
    )
    device_mac: int = Field(
        title="Device MAC",
        description="Each message contains device MAC info",
    )
    raw_message: str = Field(
        title="Raw message string",
        description="Just byte string of message",
    )
    raw_payload: str = Field(
        title="Raw payload string",
        description="Just string of unparsed payload without channel protocol wrapper",
    )
    decrypted_payload: str = Field(
        title="Decrypted payload string",
        description="Just string of unparsed but decrypted payload without channel protocol wrapper."
                    "If no encryption protocol, then this field equals 'raw_payload'",
    )
    device_raw_mac: int = Field(
        title="Device raw MAC",
        description="Each message contains device MAC info raw integer field",
    )

    protocol_id: Optional[UUID4] = Field(
        None,
        title="Protocol ID",
        description="Protocol ID for the payload",
    )
    protocol_name: Optional[str] = Field(
        None,
        title="Protocol name string",
        description="Common packet protocol name info of payload",
    )
    protocol_type: Optional[ProtocolEnum] = Field(
        None,
        title="Protocol type string",
        description="Common packet protocol type info of payload",
    )
    network_id: Optional[UUID4] = Field(
        None,
        title="Network ID",
        description="Network ID info",
    )
    network_sys_type: Optional[NetworkSysTypeEnum] = Field(
        None,
        title="Network system type info",
        description="Network system type info",
    )

    date_created: datetime = Field(
        title="Message date creation",
        description="The date when message was created",
    )
    gateway_id: UUID4 = Field(
        title="Gateway ID",
        description="Gateway ID field info",
    )
    device_id: Optional[UUID4] = Field(
        None,
        title="Device ID",
        description="Device ID field info",
    )
    verified_device: bool = Field(
        title="Device verification info",
        description="This field shows that device was found in DB and contains some data",
    )

    dt_calculated: Optional[bool] = Field(
        False,
        title="Datetime calculation info",
        description="Datetime calculation info",
    )
    error: Optional[IntegrationV0MessageError] = Field(
        None,
        title="Error info",
        description="Error structure contains error type and error message string",
    )
