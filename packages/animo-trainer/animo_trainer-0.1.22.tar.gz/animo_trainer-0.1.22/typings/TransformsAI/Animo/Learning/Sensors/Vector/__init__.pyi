import typing
from TransformsAI.Animo.Learning.Sensors import SensorConfig, SensorSpec, Sensor
from TransformsAI.Animo.Objects.Character import CharacterObject
from System import Span_1, Array_1

class CompassSensor(VectorSensor):
    def __init__(self, sensorConfig: SensorConfig) -> None: ...
    CompassTypeIdProperty : str
    CompassVariantIdProperty : str
    Id : str
    MaxCompassDistance : float
    SensorConfig : SensorConfig
    @property
    def Length(self) -> int: ...
    @property
    def SensorSpec(self) -> SensorSpec: ...
    def GetObservations(self, character: CharacterObject, values: Span_1[float]) -> None: ...


class SurroundingsSensor(VectorSensor):
    def __init__(self, sensorConfig: SensorConfig) -> None: ...
    Id : str
    SensorConfig : SensorConfig
    @property
    def Length(self) -> int: ...
    @property
    def SensorSpec(self) -> SensorSpec: ...
    def GetObservations(self, character: CharacterObject, values: Span_1[float]) -> None: ...


class VectorSensor(Sensor):
    SensorConfig : SensorConfig
    @property
    def Length(self) -> int: ...
    @property
    def SensorSpec(self) -> SensorSpec: ...
    # Skipped GetObservations due to it being static, abstract and generic.

    GetObservations : GetObservations_MethodGroup
    class GetObservations_MethodGroup:
        @typing.overload
        def __call__(self, character: CharacterObject, values: Span_1[float]) -> None:...
        @typing.overload
        def __call__(self, character: CharacterObject, observations: Array_1[float], offset: int = ...) -> None:...


