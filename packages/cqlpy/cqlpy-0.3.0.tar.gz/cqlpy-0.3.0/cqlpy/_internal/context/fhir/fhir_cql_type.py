from dataclasses import dataclass, field


@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=True)
class FhirCqlType:
    name: str
    is_backbone_element: bool = False


@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=True)
class FhirChoice(FhirCqlType):
    choices: list[FhirCqlType] = field(default_factory=list)
    name: str = "Choice"


@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=True)
class FhirList(FhirCqlType):
    item_type: FhirCqlType = field(default=FhirCqlType("String"))
    name: str = "List"


@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=True)
class FhirInterval(FhirCqlType):
    item_type: FhirCqlType = field(default=FhirCqlType("String"))
    name: str = "Interval"
