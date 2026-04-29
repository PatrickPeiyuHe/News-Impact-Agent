"""Wiki build agent architecture used by the daily impact pipeline.

The daily pipeline uses the reduced builder as the production default for
event-driven wiki rebuilds. The full builder is documented and represented here
as the heavier research-loop architecture used when the goal is a deeper first
principles company wiki.
"""

from .contracts import (
    DocumentRecord,
    SourceRoleAssignment,
    WikiBuildMode,
    WikiBuildPlan,
    WikiBuildStage,
)
from .full import FullWikiBuildAgent
from .orchestrator import build_wiki_build_plan, describe_wiki_build_modes
from .reduced import ReducedWikiBuildAgent

__all__ = [
    "DocumentRecord",
    "FullWikiBuildAgent",
    "ReducedWikiBuildAgent",
    "SourceRoleAssignment",
    "WikiBuildMode",
    "WikiBuildPlan",
    "WikiBuildStage",
    "build_wiki_build_plan",
    "describe_wiki_build_modes",
]
