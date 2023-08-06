import typing, clr, abc
from TransformsAI.Animo.Data import CheckpointData
from System.Collections.Generic import List_1, KeyValuePair_2, IEnumerable_1, Dictionary_2, IReadOnlyList_1, HashSet_1, IEnumerator_1, IList_1
from TransformsAI.Animo.Rewards import RewardFunction
from System import Action_2, Exception, MulticastDelegate, IAsyncResult, AsyncCallback, Action_1, Predicate_1, Array_1, IDisposable, Random, Func_3
from TransformsAI.Animo.Numerics import Vec2Int, Vec3Int
from TransformsAI.Animo import VoxelGrid, GridTransform
from System.Reflection import MethodInfo
from TransformsAI.Animo.Constants import TypeIds
from System.Numerics import Vector3

class AgentCheckpointAccumulator:
    def __init__(self) -> None: ...
    def AddReward(self, index: int, stepCount: int) -> None: ...
    def OnCheckpointCreated(self, checkpointTimestamp: int, agentId: int, sessionId: str, rewards: List_1[RewardFunction]) -> CheckpointData: ...
    def OnEpisodeEnded(self, stepCount: int) -> None: ...


class AnimoLogger(abc.ABC):
    StandardLogger : Action_2[typing.Any, AnimoLogger.LogType]
    @staticmethod
    def Log(message: typing.Any) -> None: ...
    @staticmethod
    def LogError(message: typing.Any) -> None: ...
    @staticmethod
    def LogException(exception: Exception) -> None: ...
    @staticmethod
    def LogWarning(message: typing.Any) -> None: ...
    @staticmethod
    def RegisterLogger(printLog: Action_2[typing.Any, AnimoLogger.LogType]) -> None: ...

    class LogType(typing.SupportsInt):
        @typing.overload
        def __init__(self, value : int) -> None: ...
        @typing.overload
        def __init__(self, value : int, force_if_true: bool) -> None: ...
        def __int__(self) -> int: ...
        
        # Values:
        Info : AnimoLogger.LogType # 0
        Warning : AnimoLogger.LogType # 1
        Error : AnimoLogger.LogType # 2
        Exception : AnimoLogger.LogType # 3



class AStar(abc.ABC):
    @staticmethod
    def GetNextStepTo(grid: VoxelGrid, start: Vec2Int, end: Vec2Int, check: AStar.TraversalCheck = ...) -> Vec2Int: ...
    @staticmethod
    def GetPathTo(grid: VoxelGrid, start: Vec2Int, end: Vec2Int, outPath: List_1[Vec2Int], check: AStar.TraversalCheck = ...) -> bool: ...

    class TraversalCheck(MulticastDelegate):
        def __init__(self, object: typing.Any, method: int) -> None: ...
        @property
        def Method(self) -> MethodInfo: ...
        @property
        def Target(self) -> typing.Any: ...
        def BeginInvoke(self, grid: VoxelGrid, from_: Vec2Int, to: Vec2Int, callback: AsyncCallback, object: typing.Any) -> IAsyncResult: ...
        def EndInvoke(self, result: IAsyncResult) -> bool: ...
        def Invoke(self, grid: VoxelGrid, from_: Vec2Int, to: Vec2Int) -> bool: ...



class EnumerableExtensions(abc.ABC):
    # Skipped Deconstruct due to it being static, abstract and generic.

    Deconstruct : Deconstruct_MethodGroup
    class Deconstruct_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[Deconstruct_2_T1], typing.Type[Deconstruct_2_T2]]) -> Deconstruct_2[Deconstruct_2_T1, Deconstruct_2_T2]: ...

        Deconstruct_2_T1 = typing.TypeVar('Deconstruct_2_T1')
        Deconstruct_2_T2 = typing.TypeVar('Deconstruct_2_T2')
        class Deconstruct_2(typing.Generic[Deconstruct_2_T1, Deconstruct_2_T2]):
            Deconstruct_2_TKey = EnumerableExtensions.Deconstruct_MethodGroup.Deconstruct_2_T1
            Deconstruct_2_TValue = EnumerableExtensions.Deconstruct_MethodGroup.Deconstruct_2_T2
            def __call__(self, kvp: KeyValuePair_2[Deconstruct_2_TKey, Deconstruct_2_TValue], key: clr.Reference[Deconstruct_2_TKey], value: clr.Reference[Deconstruct_2_TValue]) -> None:...


    # Skipped ForEach due to it being static, abstract and generic.

    ForEach : ForEach_MethodGroup
    class ForEach_MethodGroup:
        def __getitem__(self, t:typing.Type[ForEach_1_T1]) -> ForEach_1[ForEach_1_T1]: ...

        ForEach_1_T1 = typing.TypeVar('ForEach_1_T1')
        class ForEach_1(typing.Generic[ForEach_1_T1]):
            ForEach_1_T = EnumerableExtensions.ForEach_MethodGroup.ForEach_1_T1
            def __call__(self, ts: IEnumerable_1[ForEach_1_T], action: Action_1[ForEach_1_T]) -> None:...


    # Skipped GetPooledCopy due to it being static, abstract and generic.

    GetPooledCopy : GetPooledCopy_MethodGroup
    class GetPooledCopy_MethodGroup:
        @typing.overload
        def __getitem__(self, t:typing.Tuple[typing.Type[GetPooledCopy_2_T1], typing.Type[GetPooledCopy_2_T2]]) -> GetPooledCopy_2[GetPooledCopy_2_T1, GetPooledCopy_2_T2]: ...

        GetPooledCopy_2_T1 = typing.TypeVar('GetPooledCopy_2_T1')
        GetPooledCopy_2_T2 = typing.TypeVar('GetPooledCopy_2_T2')
        class GetPooledCopy_2(typing.Generic[GetPooledCopy_2_T1, GetPooledCopy_2_T2]):
            GetPooledCopy_2_TK = EnumerableExtensions.GetPooledCopy_MethodGroup.GetPooledCopy_2_T1
            GetPooledCopy_2_TV = EnumerableExtensions.GetPooledCopy_MethodGroup.GetPooledCopy_2_T2
            @typing.overload
            def __call__(self, list: Dictionary_2[GetPooledCopy_2_TK, GetPooledCopy_2_TV], filter: Predicate_1[KeyValuePair_2[GetPooledCopy_2_TK, GetPooledCopy_2_TV]] = ...) -> PooledList_1[KeyValuePair_2[GetPooledCopy_2_TK, GetPooledCopy_2_TV]]:...
            @typing.overload
            def __call__(self, list: Dictionary_2.ValueCollection_2[GetPooledCopy_2_TK, GetPooledCopy_2_TV], filter: Predicate_1[GetPooledCopy_2_TV] = ...) -> PooledList_1[GetPooledCopy_2_TV]:...
            @typing.overload
            def __call__(self, list: Dictionary_2.KeyCollection_2[GetPooledCopy_2_TK, GetPooledCopy_2_TV], filter: Predicate_1[GetPooledCopy_2_TK] = ...) -> PooledList_1[GetPooledCopy_2_TK]:...

        @typing.overload
        def __getitem__(self, t:typing.Type[GetPooledCopy_1_T1]) -> GetPooledCopy_1[GetPooledCopy_1_T1]: ...

        GetPooledCopy_1_T1 = typing.TypeVar('GetPooledCopy_1_T1')
        class GetPooledCopy_1(typing.Generic[GetPooledCopy_1_T1]):
            GetPooledCopy_1_T = EnumerableExtensions.GetPooledCopy_MethodGroup.GetPooledCopy_1_T1
            def __call__(self, list: IReadOnlyList_1[GetPooledCopy_1_T], filter: Predicate_1[GetPooledCopy_1_T] = ...) -> PooledList_1[GetPooledCopy_1_T]:...


    # Skipped SingleOrDefault due to it being static, abstract and generic.

    SingleOrDefault : SingleOrDefault_MethodGroup
    class SingleOrDefault_MethodGroup:
        def __getitem__(self, t:typing.Type[SingleOrDefault_1_T1]) -> SingleOrDefault_1[SingleOrDefault_1_T1]: ...

        SingleOrDefault_1_T1 = typing.TypeVar('SingleOrDefault_1_T1')
        class SingleOrDefault_1(typing.Generic[SingleOrDefault_1_T1]):
            SingleOrDefault_1_T = EnumerableExtensions.SingleOrDefault_MethodGroup.SingleOrDefault_1_T1
            def __call__(self, set: HashSet_1[SingleOrDefault_1_T]) -> SingleOrDefault_1_T:...




class EnumUtils_GenericClasses(abc.ABCMeta):
    Generic_EnumUtils_GenericClasses_EnumUtils_1_T = typing.TypeVar('Generic_EnumUtils_GenericClasses_EnumUtils_1_T')
    def __getitem__(self, types : typing.Type[Generic_EnumUtils_GenericClasses_EnumUtils_1_T]) -> typing.Type[EnumUtils_1[Generic_EnumUtils_GenericClasses_EnumUtils_1_T]]: ...

EnumUtils : EnumUtils_GenericClasses

EnumUtils_1_T = typing.TypeVar('EnumUtils_1_T')
class EnumUtils_1(typing.Generic[EnumUtils_1_T], abc.ABC):
    Values : Array_1[EnumUtils_1_T]


class GridUtils(abc.ABC):
    @staticmethod
    def GetAdjacentPositionsForObject(grid: VoxelGrid, origin: Vec3Int, maxNumberOfPositions: int, typeId: TypeIds, outValidPositionsPool: List_1[Vec2Int]) -> None: ...
    @staticmethod
    def IterateByDistance(maxDistance: float) -> GridUtils.EuclideanGridEnumerable: ...
    @staticmethod
    def ToSurface(cell: Vec2Int, grid: VoxelGrid) -> Vec3Int: ...
    @staticmethod
    def ToSurfaceTransform(cell: Vec2Int, grid: VoxelGrid) -> GridTransform: ...
    # Skipped VectorSize due to it being static, abstract and generic.

    VectorSize : VectorSize_MethodGroup
    class VectorSize_MethodGroup:
        def __getitem__(self, t:typing.Type[VectorSize_1_T1]) -> VectorSize_1[VectorSize_1_T1]: ...

        VectorSize_1_T1 = typing.TypeVar('VectorSize_1_T1')
        class VectorSize_1(typing.Generic[VectorSize_1_T1]):
            VectorSize_1_T = GridUtils.VectorSize_MethodGroup.VectorSize_1_T1
            def __call__(self, array: Array_1[VectorSize_1_T]) -> Vec2Int:...
            # Method VectorSize(array : T[,,]) was skipped since it collides with above method



    class EuclideanGridEnumerable(IEnumerable_1[Vec2Int]):
        def __init__(self, maxDistance: float) -> None: ...
        def GetEnumerator(self) -> GridUtils.EuclideanGridEnumerator: ...


    class EuclideanGridEnumerator(IEnumerator_1[Vec2Int]):
        def __init__(self, maxDistance: float) -> None: ...
        @property
        def Current(self) -> Vec2Int: ...
        def Dispose(self) -> None: ...
        @staticmethod
        def GenerateCache() -> None: ...
        def MoveNext(self) -> bool: ...
        def Reset(self) -> None: ...



class MathHelpers(abc.ABC):
    @staticmethod
    def IsValidYDelta(a: Vec3Int, b: Vec3Int, maxDelta: int = ...) -> bool: ...
    @staticmethod
    def NarySize(value: int, radix: int) -> int: ...
    @staticmethod
    def NormalizedSafe(v: Vector3) -> Vector3: ...
    @staticmethod
    def Round(value: float) -> int: ...
    @staticmethod
    def RoundToInt(v: Vector3) -> Vec3Int: ...
    @staticmethod
    def ToUnitDirection(v1: Vector3) -> Vec3Int: ...
    # Skipped Clamp due to it being static, abstract and generic.

    Clamp : Clamp_MethodGroup
    class Clamp_MethodGroup:
        def __call__(self, value: float, min: float, max: float) -> float:...
        # Method Clamp(value : Int32, min : Int32, max : Int32) was skipped since it collides with above method



class PooledDict_GenericClasses(abc.ABCMeta):
    Generic_PooledDict_GenericClasses_PooledDict_2_TKey = typing.TypeVar('Generic_PooledDict_GenericClasses_PooledDict_2_TKey')
    Generic_PooledDict_GenericClasses_PooledDict_2_TValue = typing.TypeVar('Generic_PooledDict_GenericClasses_PooledDict_2_TValue')
    def __getitem__(self, types : typing.Tuple[typing.Type[Generic_PooledDict_GenericClasses_PooledDict_2_TKey], typing.Type[Generic_PooledDict_GenericClasses_PooledDict_2_TValue]]) -> typing.Type[PooledDict_2[Generic_PooledDict_GenericClasses_PooledDict_2_TKey, Generic_PooledDict_GenericClasses_PooledDict_2_TValue]]: ...

PooledDict : PooledDict_GenericClasses

PooledDict_2_TKey = typing.TypeVar('PooledDict_2_TKey')
PooledDict_2_TValue = typing.TypeVar('PooledDict_2_TValue')
class PooledDict_2(typing.Generic[PooledDict_2_TKey, PooledDict_2_TValue], IDisposable):
    @property
    def Dict(self) -> Dictionary_2[PooledDict_2_TKey, PooledDict_2_TValue]: ...
    @Dict.setter
    def Dict(self, value: Dictionary_2[PooledDict_2_TKey, PooledDict_2_TValue]) -> Dictionary_2[PooledDict_2_TKey, PooledDict_2_TValue]: ...
    def Dispose(self) -> None: ...
    # Skipped Acquire due to it being static, abstract and generic.

    Acquire : Acquire_MethodGroup[PooledDict_2_TKey, PooledDict_2_TValue]
    Acquire_MethodGroup_PooledDict_2_TKey = typing.TypeVar('Acquire_MethodGroup_PooledDict_2_TKey')
    Acquire_MethodGroup_PooledDict_2_TValue = typing.TypeVar('Acquire_MethodGroup_PooledDict_2_TValue')
    class Acquire_MethodGroup(typing.Generic[Acquire_MethodGroup_PooledDict_2_TKey, Acquire_MethodGroup_PooledDict_2_TValue]):
        Acquire_MethodGroup_PooledDict_2_TKey = PooledDict_2.Acquire_MethodGroup_PooledDict_2_TKey
        Acquire_MethodGroup_PooledDict_2_TValue = PooledDict_2.Acquire_MethodGroup_PooledDict_2_TValue
        @typing.overload
        def __call__(self) -> PooledDict_2[Acquire_MethodGroup_PooledDict_2_TKey, Acquire_MethodGroup_PooledDict_2_TValue]:...
        @typing.overload
        def __call__(self, dictionary: clr.Reference[Dictionary_2[Acquire_MethodGroup_PooledDict_2_TKey, Acquire_MethodGroup_PooledDict_2_TValue]]) -> PooledDict_2[Acquire_MethodGroup_PooledDict_2_TKey, Acquire_MethodGroup_PooledDict_2_TValue]:...



class PooledList_GenericClasses(abc.ABCMeta):
    Generic_PooledList_GenericClasses_PooledList_1_T = typing.TypeVar('Generic_PooledList_GenericClasses_PooledList_1_T')
    def __getitem__(self, types : typing.Type[Generic_PooledList_GenericClasses_PooledList_1_T]) -> typing.Type[PooledList_1[Generic_PooledList_GenericClasses_PooledList_1_T]]: ...

PooledList : PooledList_GenericClasses

PooledList_1_T = typing.TypeVar('PooledList_1_T')
class PooledList_1(typing.Generic[PooledList_1_T], IDisposable):
    @property
    def List(self) -> List_1[PooledList_1_T]: ...
    @List.setter
    def List(self, value: List_1[PooledList_1_T]) -> List_1[PooledList_1_T]: ...
    def Dispose(self) -> None: ...
    # Skipped Acquire due to it being static, abstract and generic.

    Acquire : Acquire_MethodGroup[PooledList_1_T]
    Acquire_MethodGroup_PooledList_1_T = typing.TypeVar('Acquire_MethodGroup_PooledList_1_T')
    class Acquire_MethodGroup(typing.Generic[Acquire_MethodGroup_PooledList_1_T]):
        Acquire_MethodGroup_PooledList_1_T = PooledList_1.Acquire_MethodGroup_PooledList_1_T
        @typing.overload
        def __call__(self) -> PooledList_1[Acquire_MethodGroup_PooledList_1_T]:...
        @typing.overload
        def __call__(self, list: clr.Reference[List_1[Acquire_MethodGroup_PooledList_1_T]]) -> PooledList_1[Acquire_MethodGroup_PooledList_1_T]:...



class PooledSet_GenericClasses(abc.ABCMeta):
    Generic_PooledSet_GenericClasses_PooledSet_1_T = typing.TypeVar('Generic_PooledSet_GenericClasses_PooledSet_1_T')
    def __getitem__(self, types : typing.Type[Generic_PooledSet_GenericClasses_PooledSet_1_T]) -> typing.Type[PooledSet_1[Generic_PooledSet_GenericClasses_PooledSet_1_T]]: ...

PooledSet : PooledSet_GenericClasses

PooledSet_1_T = typing.TypeVar('PooledSet_1_T')
class PooledSet_1(typing.Generic[PooledSet_1_T], IDisposable):
    @property
    def Set(self) -> HashSet_1[PooledSet_1_T]: ...
    @Set.setter
    def Set(self, value: HashSet_1[PooledSet_1_T]) -> HashSet_1[PooledSet_1_T]: ...
    def Dispose(self) -> None: ...
    # Skipped Acquire due to it being static, abstract and generic.

    Acquire : Acquire_MethodGroup[PooledSet_1_T]
    Acquire_MethodGroup_PooledSet_1_T = typing.TypeVar('Acquire_MethodGroup_PooledSet_1_T')
    class Acquire_MethodGroup(typing.Generic[Acquire_MethodGroup_PooledSet_1_T]):
        Acquire_MethodGroup_PooledSet_1_T = PooledSet_1.Acquire_MethodGroup_PooledSet_1_T
        @typing.overload
        def __call__(self) -> PooledSet_1[Acquire_MethodGroup_PooledSet_1_T]:...
        @typing.overload
        def __call__(self, set: clr.Reference[HashSet_1[Acquire_MethodGroup_PooledSet_1_T]]) -> PooledSet_1[Acquire_MethodGroup_PooledSet_1_T]:...



class RandomUtils(abc.ABC):
    @classmethod
    @property
    def Instance(cls) -> Random: ...
    @staticmethod
    def RandomDirection() -> Vec2Int: ...
    # Skipped Pick due to it being static, abstract and generic.

    Pick : Pick_MethodGroup
    class Pick_MethodGroup:
        def __getitem__(self, t:typing.Type[Pick_1_T1]) -> Pick_1[Pick_1_T1]: ...

        Pick_1_T1 = typing.TypeVar('Pick_1_T1')
        class Pick_1(typing.Generic[Pick_1_T1]):
            Pick_1_T = RandomUtils.Pick_MethodGroup.Pick_1_T1
            @typing.overload
            def __call__(self, array: Array_1[Pick_1_T]) -> typing.Optional[Pick_1_T]:...
            @typing.overload
            def __call__(self, list: IList_1[Pick_1_T]) -> typing.Optional[Pick_1_T]:...


    # Skipped Shuffle due to it being static, abstract and generic.

    Shuffle : Shuffle_MethodGroup
    class Shuffle_MethodGroup:
        def __getitem__(self, t:typing.Type[Shuffle_1_T1]) -> Shuffle_1[Shuffle_1_T1]: ...

        Shuffle_1_T1 = typing.TypeVar('Shuffle_1_T1')
        class Shuffle_1(typing.Generic[Shuffle_1_T1]):
            Shuffle_1_T = RandomUtils.Shuffle_MethodGroup.Shuffle_1_T1
            def __call__(self, list: IList_1[Shuffle_1_T]) -> None:...




class ReadOnlyArray_GenericClasses(abc.ABCMeta):
    Generic_ReadOnlyArray_GenericClasses_ReadOnlyArray_1_T = typing.TypeVar('Generic_ReadOnlyArray_GenericClasses_ReadOnlyArray_1_T')
    def __getitem__(self, types : typing.Type[Generic_ReadOnlyArray_GenericClasses_ReadOnlyArray_1_T]) -> typing.Type[ReadOnlyArray_1[Generic_ReadOnlyArray_GenericClasses_ReadOnlyArray_1_T]]: ...

ReadOnlyArray : ReadOnlyArray_GenericClasses

ReadOnlyArray_1_T = typing.TypeVar('ReadOnlyArray_1_T')
class ReadOnlyArray_1(typing.Generic[ReadOnlyArray_1_T], IReadOnlyList_1[ReadOnlyArray_1_T]):
    def __init__(self, array: Array_1[ReadOnlyArray_1_T]) -> None: ...
    @property
    def Count(self) -> int: ...
    @property
    def Item(self) -> ReadOnlyArray_1_T: ...
    def GetEnumerator(self) -> ReadOnlyArray_1.Enumerator_1[ReadOnlyArray_1_T]: ...
    # Operator not supported op_Implicit(list: T[])

    Enumerator_GenericClasses_ReadOnlyArray_1_T = typing.TypeVar('Enumerator_GenericClasses_ReadOnlyArray_1_T')
    class Enumerator_GenericClasses(typing.Generic[Enumerator_GenericClasses_ReadOnlyArray_1_T], abc.ABCMeta):
        Enumerator_GenericClasses_ReadOnlyArray_1_T = ReadOnlyArray_1.Enumerator_GenericClasses_ReadOnlyArray_1_T
        def __call__(self) -> ReadOnlyArray_1.Enumerator_1[Enumerator_GenericClasses_ReadOnlyArray_1_T]: ...

    Enumerator : Enumerator_GenericClasses[ReadOnlyArray_1_T]

    Enumerator_1_T = typing.TypeVar('Enumerator_1_T')
    class Enumerator_1(typing.Generic[Enumerator_1_T], IEnumerator_1[Enumerator_1_T]):
        Enumerator_1_T = ReadOnlyArray_1.Enumerator_1_T
        def __init__(self, array: Array_1[Enumerator_1_T]) -> None: ...
        @property
        def Current(self) -> Enumerator_1_T: ...
        def Dispose(self) -> None: ...
        def MoveNext(self) -> bool: ...
        def Reset(self) -> None: ...



class ReadOnlyList_GenericClasses(abc.ABCMeta):
    Generic_ReadOnlyList_GenericClasses_ReadOnlyList_1_T = typing.TypeVar('Generic_ReadOnlyList_GenericClasses_ReadOnlyList_1_T')
    def __getitem__(self, types : typing.Type[Generic_ReadOnlyList_GenericClasses_ReadOnlyList_1_T]) -> typing.Type[ReadOnlyList_1[Generic_ReadOnlyList_GenericClasses_ReadOnlyList_1_T]]: ...

ReadOnlyList : ReadOnlyList_GenericClasses

ReadOnlyList_1_T = typing.TypeVar('ReadOnlyList_1_T')
class ReadOnlyList_1(typing.Generic[ReadOnlyList_1_T], IReadOnlyList_1[ReadOnlyList_1_T]):
    def __init__(self, list: List_1[ReadOnlyList_1_T]) -> None: ...
    Empty : ReadOnlyList_1[ReadOnlyList_1_T]
    @property
    def Count(self) -> int: ...
    @property
    def Item(self) -> ReadOnlyList_1_T: ...
    def GetEnumerator(self) -> List_1.Enumerator_1[ReadOnlyList_1_T]: ...
    # Operator not supported op_Implicit(list: List`1)
    # Skipped GetPooledCopy due to it being static, abstract and generic.

    GetPooledCopy : GetPooledCopy_MethodGroup[ReadOnlyList_1_T]
    GetPooledCopy_MethodGroup_ReadOnlyList_1_T = typing.TypeVar('GetPooledCopy_MethodGroup_ReadOnlyList_1_T')
    class GetPooledCopy_MethodGroup(typing.Generic[GetPooledCopy_MethodGroup_ReadOnlyList_1_T]):
        GetPooledCopy_MethodGroup_ReadOnlyList_1_T = ReadOnlyList_1.GetPooledCopy_MethodGroup_ReadOnlyList_1_T
        def __getitem__(self, t:typing.Type[GetPooledCopy_1_T1]) -> GetPooledCopy_1[GetPooledCopy_MethodGroup_ReadOnlyList_1_T, GetPooledCopy_1_T1]: ...

        GetPooledCopy_1_ReadOnlyList_1_T = typing.TypeVar('GetPooledCopy_1_ReadOnlyList_1_T')
        GetPooledCopy_1_T1 = typing.TypeVar('GetPooledCopy_1_T1')
        class GetPooledCopy_1(typing.Generic[GetPooledCopy_1_ReadOnlyList_1_T, GetPooledCopy_1_T1]):
            GetPooledCopy_1_ReadOnlyList_1_T = ReadOnlyList_1.GetPooledCopy_MethodGroup.GetPooledCopy_1_ReadOnlyList_1_T
            GetPooledCopy_1_V = ReadOnlyList_1.GetPooledCopy_MethodGroup.GetPooledCopy_1_T1
            def __call__(self, filter: Predicate_1[GetPooledCopy_1_V] = ...) -> PooledList_1[GetPooledCopy_1_V]:...

        def __call__(self, filter: Predicate_1[GetPooledCopy_MethodGroup_ReadOnlyList_1_T] = ...) -> PooledList_1[GetPooledCopy_MethodGroup_ReadOnlyList_1_T]:...



class ReadOnlySet_GenericClasses(abc.ABCMeta):
    Generic_ReadOnlySet_GenericClasses_ReadOnlySet_1_T = typing.TypeVar('Generic_ReadOnlySet_GenericClasses_ReadOnlySet_1_T')
    def __getitem__(self, types : typing.Type[Generic_ReadOnlySet_GenericClasses_ReadOnlySet_1_T]) -> typing.Type[ReadOnlySet_1[Generic_ReadOnlySet_GenericClasses_ReadOnlySet_1_T]]: ...

ReadOnlySet : ReadOnlySet_GenericClasses

ReadOnlySet_1_T = typing.TypeVar('ReadOnlySet_1_T')
class ReadOnlySet_1(typing.Generic[ReadOnlySet_1_T], IEnumerable_1[ReadOnlySet_1_T]):
    def __init__(self, set: HashSet_1[ReadOnlySet_1_T]) -> None: ...
    @property
    def Count(self) -> int: ...
    def Contains(self, item: ReadOnlySet_1_T) -> bool: ...
    def CopyTo(self, array: Array_1[ReadOnlySet_1_T], arrayIndex: int) -> None: ...
    def GetEnumerator(self) -> HashSet_1.Enumerator_1[ReadOnlySet_1_T]: ...
    # Operator not supported op_Implicit(set: HashSet`1)
    def Remove(self, item: ReadOnlySet_1_T) -> bool: ...


class ReflectionUtils:
    def __init__(self) -> None: ...


class VoxelGridSearch:
    def __init__(self) -> None: ...
    @property
    def VisitedCount(self) -> int: ...
    def Clear(self) -> None: ...
    def DidVisit(self, goal: Vec2Int) -> bool: ...
    def GetPathTo(self, goal: Vec2Int, path: List_1[Vec2Int]) -> None: ...
    @staticmethod
    def IsWalkable(from_: Vec3Int, to: Vec3Int) -> bool: ...
    def Search(self, graph: VoxelGrid, start: Vec2Int, enqueueCheck: Func_3[Vec3Int, Vec3Int, bool], completionCheck: Func_3[typing.Any, Vec3Int, bool] = ..., completionCheckData: typing.Any = ...) -> None: ...


class Wiggle:
    def __init__(self, chance: float, amount: int) -> None: ...
    Amount : int
    Chance : float
    def WiggleBlocks(self, grid: VoxelGrid) -> None: ...
    def WiggleCharacters(self, grid: VoxelGrid) -> None: ...
    def WiggleObjects(self, grid: VoxelGrid) -> None: ...


class WiggleTypes(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Character : WiggleTypes # 0
    Block : WiggleTypes # 1
    Object : WiggleTypes # 2

