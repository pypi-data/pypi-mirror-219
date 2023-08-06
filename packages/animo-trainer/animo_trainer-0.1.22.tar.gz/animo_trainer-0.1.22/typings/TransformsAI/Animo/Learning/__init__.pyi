import typing
from System.Collections.Generic import HashSet_1
from TransformsAI.Animo.Constants import TypeIds
from TransformsAI.Animo import VoxelGrid

class EndCondition:
    def __init__(self) -> None: ...
    NeedsCharacters : bool
    RequiredObjects : HashSet_1[TypeIds]
    StepLimit : typing.Optional[int]
    def IsMet(self, grid: VoxelGrid, stepCount: int) -> bool: ...
    def Validate(self, grid: VoxelGrid) -> None: ...

