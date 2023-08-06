from TransformsAI.Animo import IIntentConflictResolver
from System.Collections.Generic import HashSet_1
from TransformsAI.Animo.Intents import Intent

class ExecuteAllResolver(IIntentConflictResolver):
    def __init__(self) -> None: ...
    def ExecuteOrCancelConflicts(self, originalIntents: HashSet_1[Intent]) -> None: ...

