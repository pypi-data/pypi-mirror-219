import typing
from TransformsAI.Animo.Learning.Sensors import SensorConfig, SensorSpec, Sensor, GridSensorShape
from TransformsAI.Animo.Objects.Character import CharacterObject
from TransformsAI.Animo.Numerics import Vec2Int
from System import Span_1, Array_1
from TransformsAI.Animo.Learning.Sensors.Vector import VectorSensor
from System.Collections.Generic import Dictionary_2
from TransformsAI.Animo.Constants import TypeIds

class ActorAtCellSensor(CellSensor):
    def __init__(self, sensorConfig: SensorConfig) -> None: ...
    ActorLength : int
    Id : str
    SensorConfig : SensorConfig
    UnknownActorCode : int
    VariantLength : int
    @property
    def Length(self) -> int: ...
    @property
    def SensorSpec(self) -> SensorSpec: ...
    def GetObservations(self, character: CharacterObject, absoluteCell: Vec2Int, values: Span_1[float]) -> None: ...


class CellSensor(Sensor):
    SensorConfig : SensorConfig
    @property
    def Length(self) -> int: ...
    @property
    def SensorSpec(self) -> SensorSpec: ...
    # Skipped GetObservations due to it being static, abstract and generic.

    GetObservations : GetObservations_MethodGroup
    class GetObservations_MethodGroup:
        @typing.overload
        def __call__(self, character: CharacterObject, absoluteCell: Vec2Int, values: Span_1[float]) -> None:...
        @typing.overload
        def __call__(self, character: CharacterObject, absoluteCell: Vec2Int, observations: Array_1[float], offset: int = ...) -> None:...



class FlattenedGridSensor(VectorSensor):
    def __init__(self, sensorConfig: SensorConfig) -> None: ...
    Id : str
    SensorConfig : SensorConfig
    @property
    def Length(self) -> int: ...
    @property
    def SensorSpec(self) -> SensorSpec: ...
    def GetObservations(self, character: CharacterObject, values: Span_1[float]) -> None: ...


class GridSensor(Sensor):
    def __init__(self, sensorConfig: SensorConfig) -> None: ...
    Id : str
    SensorConfig : SensorConfig
    XLengthProperty : str
    ZLengthProperty : str
    @property
    def GridShape(self) -> GridSensorShape: ...
    @property
    def SensorSpec(self) -> SensorSpec: ...
    def GetGridObservations(self, character: CharacterObject, xzdObservations: Array_1[float]) -> None: ...


class HeldObjectAtCellSensor(CellSensor):
    def __init__(self, sensorConfig: SensorConfig) -> None: ...
    Id : str
    SensorConfig : SensorConfig
    SensorObservationEncodingProperty : str
    @property
    def Length(self) -> int: ...
    @property
    def SensorSpec(self) -> SensorSpec: ...
    def GetObservations(self, character: CharacterObject, absoluteCell: Vec2Int, values: Span_1[float]) -> None: ...


class MediumAtCellOneHotSensor(CellSensor):
    def __init__(self, sensorConfig: SensorConfig) -> None: ...
    Id : str
    SensorConfig : SensorConfig
    UnknownMediumIndex : int
    @property
    def Length(self) -> int: ...
    @classmethod
    @property
    def MediumTypeIds(cls) -> Dictionary_2[TypeIds, int]: ...
    @property
    def SensorSpec(self) -> SensorSpec: ...
    def GetObservations(self, character: CharacterObject, absoluteCell: Vec2Int, values: Span_1[float]) -> None: ...


class ObjectOnFloorAtCellSensor(CellSensor):
    def __init__(self, sensorConfig: SensorConfig) -> None: ...
    Id : str
    SensorConfig : SensorConfig
    SensorObservationEncodingProperty : str
    @property
    def Length(self) -> int: ...
    @property
    def SensorSpec(self) -> SensorSpec: ...
    def GetObservations(self, character: CharacterObject, absoluteCell: Vec2Int, values: Span_1[float]) -> None: ...


class TerrainAtCellSensor(CellSensor):
    def __init__(self, sensorConfig: SensorConfig) -> None: ...
    Id : str
    SensorConfig : SensorConfig
    @property
    def Length(self) -> int: ...
    @property
    def SensorSpec(self) -> SensorSpec: ...
    def GetObservations(self, character: CharacterObject, absoluteCell: Vec2Int, values: Span_1[float]) -> None: ...

