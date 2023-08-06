import typing, abc
from System.Collections.Generic import Dictionary_2, List_1
from TransformsAI.Animo import IIntentConflictResolver, ObjectInfo
from TransformsAI.Animo.Tools import ReadOnlyList_1
from TransformsAI.Animo.Constants import TypeIds
from System.Reflection import Assembly
from System import Attribute
from TransformsAI.Animo.Rewards.Categories import RewardCategory

class AnimoConfig:
    def __init__(self) -> None: ...
    ConflictResolvers : Dictionary_2[float, IIntentConflictResolver]
    Instance : AnimoConfig
    MaxStepHeight : int


class ObjectRegistry(abc.ABC):
    @staticmethod
    def GetRegisteredObjectInfos() -> ReadOnlyList_1[ObjectInfo]: ...
    @staticmethod
    def ToType(typeId: typing.Optional[TypeIds]) -> typing.Type[typing.Any]: ...
    @staticmethod
    def ToTypeId(type: typing.Type[typing.Any]) -> TypeIds: ...
    # Skipped AddObjectsToRegistry due to it being static, abstract and generic.

    AddObjectsToRegistry : AddObjectsToRegistry_MethodGroup
    class AddObjectsToRegistry_MethodGroup:
        @typing.overload
        def __call__(self, objectsToAdd: List_1[ObjectInfo]) -> None:...
        @typing.overload
        def __call__(self, assembly: Assembly) -> None:...

    # Skipped GetInfo due to it being static, abstract and generic.

    GetInfo : GetInfo_MethodGroup
    class GetInfo_MethodGroup:
        @typing.overload
        def __call__(self, typeId: TypeIds) -> ObjectInfo:...
        @typing.overload
        def __call__(self, typeId: typing.Optional[TypeIds]) -> ObjectInfo:...
        @typing.overload
        def __call__(self, type: typing.Type[typing.Any]) -> ObjectInfo:...



class RegisterAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class RegisterRewardsAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class RewardRegistry:
    def __init__(self) -> None: ...
    @property
    def Categories(self) -> ReadOnlyList_1[RewardCategory]: ...
    @classmethod
    @property
    def Instance(cls) -> RewardRegistry: ...
    # Skipped AddRewardsToRegistry due to it being static, abstract and generic.

    AddRewardsToRegistry : AddRewardsToRegistry_MethodGroup
    class AddRewardsToRegistry_MethodGroup:
        @typing.overload
        def __call__(self, rewardsToAdd: List_1[RewardCategory]) -> None:...
        @typing.overload
        def __call__(self, assembly: Assembly) -> None:...

    # Skipped Get due to it being static, abstract and generic.

    Get : Get_MethodGroup
    class Get_MethodGroup:
        def __getitem__(self, t:typing.Type[Get_1_T1]) -> Get_1[Get_1_T1]: ...

        Get_1_T1 = typing.TypeVar('Get_1_T1')
        class Get_1(typing.Generic[Get_1_T1]):
            Get_1_T = RewardRegistry.Get_MethodGroup.Get_1_T1
            def __call__(self) -> Get_1_T:...

        def __call__(self, categoryId: str) -> RewardCategory:...


