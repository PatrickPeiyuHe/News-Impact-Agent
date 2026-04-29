from __future__ import annotations

from .contracts import WikiBuildMode, WikiBuildPlan, WikiBuildStage


FULL_RESEARCH_TRACKS = (
    {
        "track_id": "company_map",
        "mission": "Lock down identity surface, entities, aliases, facilities, ownership/control hooks, and scope boundaries.",
    },
    {
        "track_id": "business_engine",
        "mission": "Explain how the company actually makes money through products, technology routes, capacity, customers, and delivery path.",
    },
    {
        "track_id": "economics_quality",
        "mission": "Extract revenue mix, margin/cash-flow anchors, concentration, capital intensity, impairment, and quality-of-earnings facts.",
    },
    {
        "track_id": "recent_delta_and_risks",
        "mission": "Capture recent changes, open issues, timing dependencies, and external triggers.",
    },
)

FULL_OUTPUT_CONTRACT = (
    "Long-form final company wiki with business mechanism, evidence bank, recent deltas, risk boundaries, and valuation relevance.",
    "Built from committed evidence records instead of one compact source package.",
    "Includes valuation-relevant reasoning only when supported by filings, reliable local data, or clearly labeled secondary sources.",
)

FULL_QUALITY_CONTRACT = (
    "Planner research must produce traceable evidence records before final synthesis.",
    "Web search is limited and reserved for freshness-sensitive gaps.",
    "Broker research may guide questions, terminology, and sanity checks, while primary filings control factual wording.",
    "Valuation logic ignores current stock price, price momentum, analyst targets, and market-derived upside/downside framing.",
)


class FullWikiBuildAgent:
    """Research-loop wiki architecture for high-detail first builds."""

    mode = WikiBuildMode.FULL

    def plan(self, *, ticker: str, company: str) -> WikiBuildPlan:
        stages = (
            WikiBuildStage(
                stage_id="01_corpus_preflight",
                name="Corpus Preflight",
                kind="deterministic",
                inputs=("document database", "local research index", "valuation data availability"),
                outputs=("ready corpus", "index status", "company manifest"),
                notes=("Build or validate searchable local chunks before any expensive LLM work.",),
            ),
            WikiBuildStage(
                stage_id="02_anchor_and_company_brief",
                name="Anchor And Company Brief",
                kind="llm_structured",
                model="deepseek-v4-pro / deepseek-reasoner",
                inputs=("company identity", "initial corpus search", "valuation fact pack"),
                outputs=("company brief", "research anchor memo", "initial hypotheses"),
                notes=("This gives later planner nodes stable company scope and terminology.",),
            ),
            WikiBuildStage(
                stage_id="03_research_router",
                name="Research Router",
                kind="llm_json",
                model="kimi-k2.5",
                inputs=("company brief", "fixed research track templates", "known gaps"),
                outputs=("track ownership plan",),
                notes=("The default four tracks are company_map, business_engine, economics_quality, recent_delta_and_risks.",),
            ),
            WikiBuildStage(
                stage_id="04_planner_research_loops",
                name="Planner Research Loops",
                kind="agentic_retrieval",
                model="kimi-k2.5 planner with local tools",
                inputs=("track plan", "local hybrid search tools", "limited web search budget"),
                outputs=("committed evidence bank", "mutable research note", "retrieval trace"),
                notes=(
                    "Each track searches local corpus first.",
                    "Evidence records keep source type, locator, quote_or_fact, commit mode, and handle id.",
                ),
            ),
            WikiBuildStage(
                stage_id="05_round_draft_and_critic",
                name="Round Draft And Critic",
                kind="llm_markdown_review",
                model="deepseek-v4-pro + grok/deepseek critic",
                inputs=("committed evidence", "mutable research note", "company brief"),
                outputs=("business draft", "critic fixes", "second-round research priorities"),
                notes=("The critic focuses on factual gaps, unsupported inference, mechanism clarity, and downstream usefulness.",),
            ),
            WikiBuildStage(
                stage_id="06_valuation_stage",
                name="Valuation Stage",
                kind="llm_structured_plus_calculator",
                model="deepseek-reasoner + JSONizer + calculator",
                inputs=("valuation fact pack", "business draft", "evidence bank"),
                outputs=("method selection", "assumption memo", "assumptions JSON", "calculator outputs", "valuation memo"),
                notes=(
                    "Valuation is an analytical lens for business quality and sensitivity.",
                    "It avoids current market price and target-price anchoring.",
                ),
            ),
            WikiBuildStage(
                stage_id="07_final_writer",
                name="Full Wiki Final Writer",
                kind="llm_markdown",
                model="gpt-5.5",
                inputs=("business draft", "critic fixes", "valuation memo", "evidence bank", "final research note"),
                outputs=("full company wiki markdown",),
                notes=("The final writer audits prior outputs against evidence and ships one durable wiki.",),
            ),
            WikiBuildStage(
                stage_id="08_publish_and_index",
                name="Publish And Index",
                kind="deterministic",
                inputs=("full wiki markdown", "manifest", "wiki collection"),
                outputs=("published full wiki", "archive entry", "rebuilt wiki RAG index"),
                notes=("Full wiki outputs can be promoted into the same final collection used by news impact.",),
            ),
        )
        return WikiBuildPlan(
            ticker=ticker,
            company=company,
            mode=self.mode,
            stages=stages,
            source_roles=(),
            output_contract=FULL_OUTPUT_CONTRACT,
            quality_contract=FULL_QUALITY_CONTRACT,
        )

    def research_tracks(self) -> tuple[dict[str, str], ...]:
        return FULL_RESEARCH_TRACKS
