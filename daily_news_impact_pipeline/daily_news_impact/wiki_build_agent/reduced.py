from __future__ import annotations

from .contracts import DocumentRecord, WikiBuildMode, WikiBuildPlan, WikiBuildStage
from .source_selection import select_reduced_wiki_sources


REDUCED_OUTPUT_CONTRACT = (
    "Markdown company wiki, usually 2000-4000 Chinese characters.",
    "Facts stay inside selected source-package evidence boundaries.",
    "Broker research is labeled as secondary context when used.",
    "Named products, entities, projects, geographies, customers, suppliers, stages, and trigger terms stay visible for RAG.",
)

REDUCED_QUALITY_CONTRACT = (
    "Prefer recent disclosed primary sources when facts conflict.",
    "Preserve stage words such as sample, validation, small-batch, planned, proposed, pending approval, and undisclosed.",
    "Avoid promotional language and unsupported competitive claims.",
    "The wiki must be directly useful to policy/disclosure news impact analysis.",
)

REDUCED_SECTION_CONTRACT = (
    "Retrieval Surface",
    "Business And Value Chain",
    "Products Assets Projects",
    "Customers Suppliers Counterparties",
    "Financial Segments Quality",
    "Capital Transactions And Obligations",
    "Industry Competition Triggers",
    "Freshness Recent Events",
)


class ReducedWikiBuildAgent:
    """Default wiki build architecture for daily impact-triggered rebuilds."""

    mode = WikiBuildMode.REDUCED

    def plan(self, *, ticker: str, company: str, documents: list[DocumentRecord]) -> WikiBuildPlan:
        source_roles = select_reduced_wiki_sources(documents)
        stages = (
            WikiBuildStage(
                stage_id="01_source_selection",
                name="Source Selection",
                kind="deterministic",
                inputs=("normalized document catalog",),
                outputs=("source role assignments", "source cutoff", "document availability summary"),
                notes=(
                    "Select latest annual report, latest periodic-like report, origin document, material announcements, and recent broker context.",
                    "Announcement and periodic filters remove routine governance, abstracts, corrections, prompt notices, and legal-only files.",
                ),
            ),
            WikiBuildStage(
                stage_id="02_retrieval_brainstormer",
                name="Retrieval Brainstormer",
                kind="llm_json",
                model="qwen3.5-plus thinking",
                inputs=("company identity", "fixed retrieval sessions", "source availability", "tiny primer snippets"),
                outputs=("company-specific terms", "semantic queries", "selected announcement/report doc_ids"),
                notes=(
                    "The model does not write wiki prose.",
                    "It only improves retrieval terms and selects a small number of high-value optional files.",
                ),
            ),
            WikiBuildStage(
                stage_id="03_source_package_builder",
                name="Hybrid Source Package Builder",
                kind="deterministic_retrieval",
                inputs=("source role assignments", "brainstormer retrieval plan", "llm-ready documents", "local research index"),
                outputs=("sectioned source package",),
                notes=(
                    "Each section uses direct heading/keyword retrieval plus semantic retrieval.",
                    "Tables and small-title sections are kept intact where possible.",
                    "Package sections follow the reduced section contract.",
                ),
            ),
            WikiBuildStage(
                stage_id="04_wiki_writer",
                name="Reduced Wiki Writer",
                kind="llm_markdown",
                model="kimi-k2.6 batch",
                inputs=("system prompt", "company identity", "source package"),
                outputs=("reduced company wiki markdown",),
                notes=(
                    "Writer targets durable investor-readable company knowledge.",
                    "The output is compact enough for daily rebuilds and rich enough for downstream RAG.",
                ),
            ),
            WikiBuildStage(
                stage_id="05_apply_archive_index",
                name="Apply, Archive, And Index",
                kind="deterministic",
                inputs=("writer output", "current wiki manifest", "current wiki collection"),
                outputs=("new wiki file", "archived old wiki", "updated manifest", "rebuilt wiki RAG index"),
                notes=(
                    "Daily company-disclosure impact always runs impact analysis before this stage.",
                    "Index refresh is batched at the end of the daily pipeline when possible.",
                ),
            ),
        )
        return WikiBuildPlan(
            ticker=ticker,
            company=company,
            mode=self.mode,
            stages=stages,
            source_roles=source_roles,
            output_contract=REDUCED_OUTPUT_CONTRACT,
            quality_contract=REDUCED_QUALITY_CONTRACT,
        )

    def section_contract(self) -> tuple[str, ...]:
        return REDUCED_SECTION_CONTRACT
