import typing, abc
from TransformsAI.Animo import GridObject

class Effects(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Splash : Effects # 1
    Slash : Effects # 2
    Burn : Effects # 3
    Push : Effects # 4
    Feed : Effects # 5
    HitByProjectile : Effects # 6
    Bounced : Effects # 7
    Ricocheted : Effects # 8
    Smack : Effects # 9


class GroundMaterials(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : GroundMaterials # 0
    ShallowWater : GroundMaterials # 1
    DeepWater : GroundMaterials # 2


class TypeIds(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : TypeIds # 0
    Character : TypeIds # 1
    Axe : TypeIds # 2
    BlockMaker : TypeIds # 3
    FakeAgent : TypeIds # 4
    Flute : TypeIds # 5
    TreeSprout : TypeIds # 6
    Tree : TypeIds # 7
    TreeWithFruits : TypeIds # 8
    Crystal : TypeIds # 9
    WaterGun : TypeIds # 10
    TreeFruit : TypeIds # 11
    Flamethrower : TypeIds # 12
    Bat : TypeIds # 13
    Ball : TypeIds # 14
    Flower : TypeIds # 15
    FlowerSeed : TypeIds # 16
    FlowerSprout : TypeIds # 17
    Fire : TypeIds # 18
    Salamander : TypeIds # 19
    Obstacle : TypeIds # 20
    BounceResolution : TypeIds # 21
    Dog : TypeIds # 22
    NPCObstacle : TypeIds # 23
    LargeSnowball : TypeIds # 24
    SnowPal : TypeIds # 25
    SmallSnowball : TypeIds # 26
    SnowballHeap : TypeIds # 27
    Shovel : TypeIds # 28
    DestructibleProp : TypeIds # 29
    WiltedFlower : TypeIds # 30
    Torch : TypeIds # 31
    RedPaint : TypeIds # 32
    BluePaint : TypeIds # 33
    RedPaintBrush : TypeIds # 34
    BluePaintBrush : TypeIds # 35
    IndestructibleProp : TypeIds # 36
    QuestMarker : TypeIds # 37
    Hatch : TypeIds # 38


class UsePriorities(abc.ABC):
    Character : float
    Inanimate : float
    Medium : float
    NPC : float
    Resolution : float
    @staticmethod
    def Comparer(x: GridObject, y: GridObject) -> int: ...

