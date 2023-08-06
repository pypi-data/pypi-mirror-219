import typing, abc
from TransformsAI.Animo.Objects.Character import CharacterObject
from TransformsAI.Animo.Constants import TypeIds
from System import Predicate_1
from TransformsAI.Animo import GridObject

class HeuristicBehaviourExtensions(abc.ABC):
    MaxSightDistance : float
    RandomRotationFrequency : float
    @staticmethod
    def ChopAllTrees(character: CharacterObject, targetAnimoOnMissingTarget: bool) -> CharacterObject.Actions: ...
    @staticmethod
    def CrystalDestroyer(character: CharacterObject, targetAnimoOnMissingTarget: bool) -> CharacterObject.Actions: ...
    @staticmethod
    def DecideAction(autoBehaviour: HeuristicBehaviours, character: CharacterObject) -> CharacterObject.Actions: ...
    @staticmethod
    def MoveRandomly(character: CharacterObject) -> CharacterObject.Actions: ...
    @staticmethod
    def SmackAllBalls(character: CharacterObject, targetAnimoOnMissingTarget: bool) -> CharacterObject.Actions: ...
    @staticmethod
    def UseOnTargetWithTool(character: CharacterObject, grabTarget: TypeIds, targetDiscriminant: Predicate_1[GridObject], targetAnimoOnMissingTarget: bool) -> CharacterObject.Actions: ...
    @staticmethod
    def WaterWiltedFlowers(character: CharacterObject, targetAnimoOnMissingTarget: bool) -> CharacterObject.Actions: ...


class HeuristicBehaviours(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    StandStill : HeuristicBehaviours # 0
    MoveRandomly : HeuristicBehaviours # 1
    ChopTreesWithAxe : HeuristicBehaviours # 2
    WaterAllFlowers : HeuristicBehaviours # 3
    CrystalDestroyer : HeuristicBehaviours # 4
    SmackBallsWithBat : HeuristicBehaviours # 5

