import typing
from TransformsAI.Animo.Learning.Sensors import Sensor, SensorConfig, AttentionSensorShape, SensorSpec
from TransformsAI.Animo.Objects.Character import CharacterObject
from System import Array_1, Span_1
from System.Collections.Generic import IComparer_1
from TransformsAI.Animo import GridObject
from TransformsAI.Animo.Numerics import Vec3Int

class AttentionSensor(Sensor):
    def __init__(self, sensorConfig: SensorConfig) -> None: ...
    Id : str
    MaxNumEntitiesProperty : str
    SensorConfig : SensorConfig
    @property
    def AttentionSensorShape(self) -> AttentionSensorShape: ...
    @property
    def SensorSpec(self) -> SensorSpec: ...
    def GetAttentionObservations(self, character: CharacterObject, numObjNumValsObservations: Array_1[float]) -> None: ...


class DistanceToCharacterComparer(IComparer_1[GridObject]):
    def __init__(self, characterPosition: Vec3Int) -> None: ...
    def Compare(self, a: GridObject, b: GridObject) -> int: ...


class ObjectEntitySensor(Sensor):
    SensorConfig : SensorConfig
    @property
    def Length(self) -> int: ...
    @property
    def SensorSpec(self) -> SensorSpec: ...
    # Skipped GetObservations due to it being static, abstract and generic.

    GetObservations : GetObservations_MethodGroup
    class GetObservations_MethodGroup:
        @typing.overload
        def __call__(self, character: CharacterObject, sensedObject: GridObject, values: Span_1[float]) -> None:...
        @typing.overload
        def __call__(self, character: CharacterObject, sensedObject: GridObject, observations: Array_1[float], offset: int = ...) -> None:...



class ObjectTypeAndLocationSensor(ObjectEntitySensor):
    def __init__(self, sensorConfig: SensorConfig) -> None: ...
    Id : str
    IsHeldObservationLength : int
    LocationObservationLength : int
    SensorConfig : SensorConfig
    SensorObservationEncodingProperty : str
    @property
    def Length(self) -> int: ...
    @property
    def SensorSpec(self) -> SensorSpec: ...
    def GetObservations(self, character: CharacterObject, sensedObject: GridObject, values: Span_1[float]) -> None: ...

