from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class WikiBuildMode(str, Enum):
    REDUCED = "reduced"
    FULL = "full"


@dataclass(frozen=True)
class DocumentRecord:
    """A normalized source document available to a wiki builder.

    This deliberately mirrors the database-facing document shape without
    depending on a concrete SQLite schema. Open-source readers can understand
    the builder contract from this one object.
    """

    doc_id: str
    ticker: str
    company: str
    title: str
    doc_family: str
    publish_date: str
    text_length: int = 0
    llm_ready_md_path: str = ""
    broker: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SourceRoleAssignment:
    """A selected document and the role it plays in the wiki source package."""

    role: str
    document: DocumentRecord
    reason: str
    event_families: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["document"] = self.document.to_dict()
        return payload


@dataclass(frozen=True)
class WikiBuildStage:
    """A readable stage contract for one node in a wiki builder."""

    stage_id: str
    name: str
    kind: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    model: str = ""
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class WikiBuildPlan:
    """The planned execution shape for one company wiki build."""

    ticker: str
    company: str
    mode: WikiBuildMode
    stages: tuple[WikiBuildStage, ...]
    source_roles: tuple[SourceRoleAssignment, ...] = ()
    output_contract: tuple[str, ...] = ()
    quality_contract: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "ticker": self.ticker,
            "company": self.company,
            "mode": self.mode.value,
            "stages": [stage.to_dict() for stage in self.stages],
            "source_roles": [item.to_dict() for item in self.source_roles],
            "output_contract": list(self.output_contract),
            "quality_contract": list(self.quality_contract),
        }
