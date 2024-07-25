import dataclasses

@dataclasses.dataclass
class EmergingThreat:
    ioc: dict = dataclasses.field(default_factory=dict)
    ttps: dict = dataclasses.field(default_factory=dict)
    threat_actors: list = dataclasses.field(default_factory=list)
    cve_ids: list = dataclasses.field(default_factory=list)
