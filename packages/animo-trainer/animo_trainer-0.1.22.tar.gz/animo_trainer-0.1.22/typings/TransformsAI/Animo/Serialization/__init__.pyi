import typing, abc

class AnimoSerializer(abc.ABC):
    @staticmethod
    def ToJson(obj: typing.Any) -> str: ...
    # Skipped FromJson due to it being static, abstract and generic.

    FromJson : FromJson_MethodGroup
    class FromJson_MethodGroup:
        def __getitem__(self, t:typing.Type[FromJson_1_T1]) -> FromJson_1[FromJson_1_T1]: ...

        FromJson_1_T1 = typing.TypeVar('FromJson_1_T1')
        class FromJson_1(typing.Generic[FromJson_1_T1]):
            FromJson_1_T = AnimoSerializer.FromJson_MethodGroup.FromJson_1_T1
            def __call__(self, json: str) -> FromJson_1_T:...



