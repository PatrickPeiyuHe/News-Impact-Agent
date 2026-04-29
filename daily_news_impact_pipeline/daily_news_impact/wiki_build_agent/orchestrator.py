from __future__ import annotations

from .contracts import DocumentRecord, WikiBuildMode, WikiBuildPlan
from .full import FullWikiBuildAgent
from .reduced import ReducedWikiBuildAgent


def describe_wiki_build_modes() -> dict[str, dict[str, str]]:
    return {
        WikiBuildMode.REDUCED.value: {
            "default": "yes",
            "purpose": "Fast, source-package based rebuild for daily impact-triggered wiki updates.",
            "typical_trigger": "annual report, prospectus, or a very material disclosure after impact analysis.",
            "output": "compact reduced wiki suitable for downstream RAG and news impact reasoning.",
        },
        WikiBuildMode.FULL.value: {
            "default": "no",
            "purpose": "Heavy research-loop build for initial or high-stakes company understanding.",
            "typical_trigger": "manual deep build, new company onboarding, or major model quality review.",
            "output": "long-form full wiki with research trace, valuation lens, and final writer synthesis.",
        },
    }


def build_wiki_build_plan(
    *,
    mode: str | WikiBuildMode,
    ticker: str,
    company: str,
    documents: list[DocumentRecord] | None = None,
) -> WikiBuildPlan:
    selected_mode = mode if isinstance(mode, WikiBuildMode) else WikiBuildMode(str(mode))
    if selected_mode == WikiBuildMode.REDUCED:
        return ReducedWikiBuildAgent().plan(ticker=ticker, company=company, documents=documents or [])
    if selected_mode == WikiBuildMode.FULL:
        return FullWikiBuildAgent().plan(ticker=ticker, company=company)
    raise ValueError(f"unsupported_wiki_build_mode:{mode}")
