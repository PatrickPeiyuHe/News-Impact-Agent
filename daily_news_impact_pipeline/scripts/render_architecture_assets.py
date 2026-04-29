from __future__ import annotations

from pathlib import Path
from textwrap import wrap

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "open_source_assets"

INK = "#111827"
MUTED = "#475569"
GRID = "#E5E7EB"
ARROW = "#334155"

COLORS = {
    "source": ("#F8FAFC", "#CBD5E1", "#64748B"),
    "control": ("#FFF7ED", "#FED7AA", "#C2410C"),
    "policy": ("#EFF6FF", "#93C5FD", "#1D4ED8"),
    "disclosure": ("#ECFDF5", "#86EFAC", "#047857"),
    "wiki": ("#EEF2FF", "#A5B4FC", "#4338CA"),
    "output": ("#FDF2F8", "#F9A8D4", "#BE185D"),
}


def new_canvas(title: str, subtitle: str) -> tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=(24, 13.5), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 13.5)
    ax.axis("off")
    ax.text(0.75, 12.8, title, fontsize=27, fontweight="bold", color=INK, va="top")
    ax.text(0.78, 12.18, subtitle, fontsize=14.5, color=MUTED, va="top")
    return fig, ax


def lane(ax: plt.Axes, y: float, h: float, title: str, color: str) -> None:
    _, _, accent = COLORS[color]
    ax.add_patch(
        FancyBboxPatch(
            (0.65, y),
            22.7,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.16",
            linewidth=1.0,
            edgecolor=GRID,
            facecolor="#FFFFFF",
        )
    )
    ax.plot([0.65, 23.35], [y + h, y + h], color=accent, linewidth=3.0, solid_capstyle="round")
    ax.text(0.95, y + h - 0.22, title, fontsize=14, fontweight="bold", color=accent, va="top")


def box(
    ax: plt.Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    body: str,
    kind: str,
    *,
    title_size: int = 12,
    body_size: int = 10,
) -> None:
    fill, edge, accent = COLORS[kind]
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.08,rounding_size=0.16",
            linewidth=1.45,
            edgecolor=edge,
            facecolor=fill,
        )
    )
    ax.plot([x + 0.18, x + w - 0.18], [y + h - 0.18, y + h - 0.18], color=accent, linewidth=2.4, alpha=0.9)
    ax.text(x + 0.24, y + h - 0.38, title, fontsize=title_size, fontweight="bold", color=INK, va="top")
    if h <= 0.9:
        max_lines = 1
        body_y = y + h - 0.70
        line_spacing = 1.0
    elif h <= 1.05:
        max_lines = 2
        body_y = y + h - 0.80
        line_spacing = 1.02
    else:
        max_lines = 3
        body_y = y + h - 0.86
        line_spacing = 1.08
    body_lines = wrap(body, width=max(18, int(w * 11)))[:max_lines]
    ax.text(
        x + 0.24,
        body_y,
        "\n".join(body_lines),
        fontsize=body_size,
        color=MUTED,
        va="top",
        linespacing=line_spacing,
    )


def arrow(ax: plt.Axes, x1: float, y1: float, x2: float, y2: float) -> None:
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle="-|>",
            mutation_scale=13,
            linewidth=1.6,
            color=ARROW,
            shrinkA=4,
            shrinkB=4,
        )
    )


def arrow_chain(ax: plt.Axes, boxes: list[tuple[float, float, float, float]]) -> None:
    for left, right in zip(boxes, boxes[1:]):
        x1, y1, w1, h1 = left
        x2, y2, _, h2 = right
        arrow(ax, x1 + w1, y1 + h1 / 2, x2, y2 + h2 / 2)


def callout(ax: plt.Axes, x: float, y: float, text: str, color: str = "control") -> None:
    fill, edge, accent = COLORS[color]
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            5.25,
            0.7,
            boxstyle="round,pad=0.05,rounding_size=0.14",
            linewidth=1.1,
            edgecolor=edge,
            facecolor=fill,
        )
    )
    ax.text(x + 0.18, y + 0.47, text, fontsize=10, fontweight="bold", color=accent, va="center")


def render_news_impact_agent() -> Path:
    fig, ax = new_canvas(
        "News Impact Agent Architecture",
        "Daily source update, policy RAG matching, company-disclosure impact analysis, and wiki maintenance in one run.",
    )

    lane(ax, 9.55, 1.75, "1. Shared intake and knowledge base", "source")
    intake = [
        (1.05, 9.85, 3.55, 0.95),
        (5.0, 9.85, 3.55, 0.95),
        (8.95, 9.85, 3.55, 0.95),
        (12.9, 9.85, 3.55, 0.95),
        (16.85, 9.85, 3.55, 0.95),
        (20.8, 9.85, 2.05, 0.95),
    ]
    box(ax, *intake[0], "Date Window", "target dates, target companies, CUDA preference", "source")
    box(ax, *intake[1], "Crawl + Parse", "policy, filings, financial reports, broker research", "control")
    box(ax, *intake[2], "Ingest", "normalized source rows and document metadata", "source")
    box(ax, *intake[3], "Index", "document chunks and final company wiki chunks", "wiki")
    box(ax, *intake[4], "Preflight", "DB counts, manifests, missing inputs, resume state", "control")
    box(ax, *intake[5], "Ready", "run gates open", "output")
    arrow_chain(ax, intake)

    lane(ax, 6.8, 2.0, "2. Policy news branch: unknown ticker, two-round hybrid RAG", "policy")
    policy = [
        (1.05, 7.13, 2.75, 1.12),
        (4.15, 7.13, 2.75, 1.12),
        (7.25, 7.13, 2.75, 1.12),
        (10.35, 7.13, 2.9, 1.12),
        (13.6, 7.13, 2.9, 1.12),
        (16.85, 7.13, 2.75, 1.12),
        (19.95, 7.13, 2.9, 1.12),
    ]
    box(ax, *policy[0], "Policy Text", "original or compressed 1500-2000 Chinese chars", "policy")
    box(ax, *policy[1], "Analysis Gate", "skip incomplete, tiny, or low-signal policy items", "policy")
    box(ax, *policy[2], "Round 1 Plan", "direct terms, semantic terms, downweight terms", "policy")
    box(ax, *policy[3], "Hybrid Search 1", "broad search across final wiki chunks", "policy")
    box(ax, *policy[4], "Hybrid Search 2", "company-filtered search from round 1 evidence", "policy")
    box(ax, *policy[5], "Initial Match", "stricter soft gate; empty match skips GPT impact", "policy")
    box(ax, *policy[6], "Final Impact", "news + each matched company wiki", "policy")
    arrow_chain(ax, policy)
    callout(ax, 11.6, 6.08, "Token control: no final impact call when initial match is empty", "policy")

    lane(ax, 3.9, 2.05, "3. Company disclosure branch: ticker known, impact first, wiki action second", "disclosure")
    disclosure = [
        (1.05, 4.27, 3.25, 1.15),
        (4.72, 4.27, 3.05, 1.15),
        (8.2, 4.27, 3.1, 1.15),
        (11.75, 4.27, 3.3, 1.15),
        (15.5, 4.27, 3.15, 1.15),
        (19.1, 4.27, 3.75, 1.15),
    ]
    box(ax, *disclosure[0], "Mapped Disclosure", "filing, quarterly report, annual report, announcement", "disclosure")
    box(ax, *disclosure[1], "Length Gate", "compress only when the source is too long", "disclosure")
    box(ax, *disclosure[2], "Direct Impact", "current wiki + source text, before any wiki write", "disclosure")
    box(ax, *disclosure[3], "Wiki Decision", "no update, small patch, or force rebuild", "disclosure")
    box(ax, *disclosure[4], "Apply Action", "archive old wiki before patch or rebuild", "wiki")
    box(ax, *disclosure[5], "Refresh Wiki Index", "single final rebuild for downstream RAG", "wiki")
    arrow_chain(ax, disclosure)
    callout(ax, 11.95, 3.16, "Most disclosures save impact only; annual/prospectus-class events can rebuild", "disclosure")

    lane(ax, 1.05, 1.75, "4. Daily outputs", "output")
    outputs = [
        (1.05, 1.35, 4.25, 0.95),
        (5.85, 1.35, 4.25, 0.95),
        (10.65, 1.35, 4.25, 0.95),
        (15.45, 1.35, 4.25, 0.95),
        (20.25, 1.35, 2.6, 0.95),
    ]
    box(ax, *outputs[0], "Daily Company Actions", "one row per date, ticker, source, action, status", "output")
    box(ax, *outputs[1], "Impact Reports", "Markdown and CSV analysis outputs", "output")
    box(ax, *outputs[2], "Coverage Table", "all 41 wiki companies, including no-action rows", "output")
    box(ax, *outputs[3], "Wiki Snapshot", "latest wiki files plus archived prior versions", "output")
    box(ax, *outputs[4], "Run Log", "resume-safe stages", "control")
    arrow_chain(ax, outputs)

    ax.text(
        0.78,
        0.42,
        "Design rule: source processing is batched; expensive LLM calls are gated; wiki writes happen only after impact analysis is saved.",
        fontsize=11,
        color=MUTED,
    )

    out = ASSET_DIR / "news_impact_agent_architecture.png"
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out


def render_wiki_build_agent() -> Path:
    fig, ax = new_canvas(
        "Company Wiki Build Agent Architecture",
        "Reduced builder is the daily default; full builder is the heavier research route for onboarding and deep review.",
    )

    lane(ax, 10.0, 1.35, "Shared source foundation", "source")
    foundation = [
        (1.05, 10.25, 3.6, 0.82),
        (5.05, 10.25, 3.6, 0.82),
        (9.05, 10.25, 3.6, 0.82),
        (13.05, 10.25, 3.6, 0.82),
        (17.05, 10.25, 5.8, 0.82),
    ]
    box(ax, *foundation[0], "Company Corpus", "annual reports, quarterlies, announcements, broker reports", "source", body_size=9)
    box(ax, *foundation[1], "Chunk Store", "heading, keyword, semantic, table-aware chunks", "source", body_size=9)
    box(ax, *foundation[2], "Identity Surface", "aliases, entities, products, projects, trigger terms", "source", body_size=9)
    box(ax, *foundation[3], "Fresh Documents", "newly ingested files can change source selection", "control", body_size=9)
    box(ax, *foundation[4], "Wiki Quality Target", "retrievable, evidence-bound, mechanism-oriented Markdown", "wiki", body_size=9)
    arrow_chain(ax, foundation)

    lane(ax, 6.95, 2.05, "Reduced builder: default route for daily rebuilds", "wiki")
    reduced = [
        (1.05, 7.33, 3.1, 1.15),
        (4.55, 7.33, 3.1, 1.15),
        (8.05, 7.33, 3.25, 1.15),
        (11.7, 7.33, 3.45, 1.15),
        (15.55, 7.33, 3.25, 1.15),
        (19.2, 7.33, 3.65, 1.15),
    ]
    box(ax, *reduced[0], "Source Selection", "latest annual, latest periodic, origin doc, material events, research context", "wiki")
    box(ax, *reduced[1], "Primer Snippets", "small source excerpts for planning without large context", "wiki")
    box(ax, *reduced[2], "Retrieval Plan", "LLM returns direct terms, semantic terms, and file choices", "wiki")
    box(ax, *reduced[3], "Hybrid Package", "retrieval surface plus business, products, customers, finance, risks", "wiki")
    box(ax, *reduced[4], "Reduced Writer", "2000-4000 Chinese chars, compact Markdown", "wiki")
    box(ax, *reduced[5], "Publish", "archive old wiki, update manifest, rebuild wiki RAG index", "output")
    arrow_chain(ax, reduced)
    callout(ax, 12.15, 6.18, "Used by force_rebuild after impact analysis, especially annual reports and prospectuses", "wiki")

    lane(ax, 3.0, 3.05, "Full builder: deep research route", "policy")
    full_top = [
        (1.05, 4.65, 3.1, 0.95),
        (4.55, 4.65, 3.1, 0.95),
        (8.05, 4.65, 3.1, 0.95),
        (11.55, 4.65, 4.55, 0.95),
        (16.5, 4.65, 3.0, 0.95),
        (19.9, 4.65, 2.95, 0.95),
    ]
    box(ax, *full_top[0], "Corpus Preflight", "validate index and source coverage", "policy", body_size=9)
    box(ax, *full_top[1], "Anchor Brief", "company scope, initial hypotheses, gaps", "policy", body_size=9)
    box(ax, *full_top[2], "Research Router", "track ownership and work plan", "policy", body_size=9)
    box(ax, *full_top[3], "Planner Research Loops", "company map, business engine, economics, recent risks", "policy", body_size=9)
    box(ax, *full_top[4], "Evidence Bank", "source-located fact boundaries", "control", body_size=9)
    box(ax, *full_top[5], "Draft + Critic", "synthesis, gap check, fixes", "control", body_size=9)
    arrow_chain(ax, full_top)

    full_bottom = [
        (8.05, 3.28, 3.1, 0.95),
        (11.55, 3.28, 3.1, 0.95),
        (15.05, 3.28, 3.1, 0.95),
        (18.55, 3.28, 4.3, 0.95),
    ]
    box(ax, *full_bottom[0], "Valuation Lens", "methods, assumptions, fragility", "control", body_size=9)
    box(ax, *full_bottom[1], "Final Writer", "long-form full wiki synthesis", "wiki", body_size=9)
    box(ax, *full_bottom[2], "Full Wiki", "deep onboarding artifact", "wiki", body_size=9)
    box(ax, *full_bottom[3], "Same Publishing Contract", "archive, manifest, final wiki RAG index", "output", body_size=9)
    arrow_chain(ax, full_bottom)
    arrow(ax, full_top[-1][0] + full_top[-1][2] / 2, full_top[-1][1], full_bottom[0][0] + full_bottom[0][2] / 2, full_bottom[0][1] + full_bottom[0][3])

    lane(ax, 1.0, 1.05, "How daily impact uses the wiki", "output")
    daily = [
        (1.05, 1.22, 4.2, 0.62),
        (5.75, 1.22, 4.2, 0.62),
        (10.45, 1.22, 4.2, 0.62),
        (15.15, 1.22, 3.8, 0.62),
        (19.45, 1.22, 3.4, 0.62),
    ]
    box(ax, *daily[0], "News impact", "policy RAG or disclosure direct analysis", "output", title_size=10, body_size=8)
    box(ax, *daily[1], "Wiki decision", "no update, small patch, force rebuild", "output", title_size=10, body_size=8)
    box(ax, *daily[2], "Apply wiki action", "archive before patch or rebuild", "wiki", title_size=10, body_size=8)
    box(ax, *daily[3], "Re-index", "one final refresh per run", "wiki", title_size=10, body_size=8)
    box(ax, *daily[4], "Next day ready", "fresh retrieval surface", "output", title_size=10, body_size=8)
    arrow_chain(ax, daily)

    ax.text(
        0.78,
        0.38,
        "Source-selection rule is shared: latest annual report is primary; latest real periodic report, origin document, material announcement, and research context are added when available.",
        fontsize=11,
        color=MUTED,
    )

    out = ASSET_DIR / "wiki_build_agent_architecture.png"
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out


def render_policy_news_branch_detail() -> Path:
    fig, ax = new_canvas(
        "Policy News Impact Branch",
        "Policy news starts without a known ticker. The branch uses gated LLM planning plus two-round hybrid RAG over final company wikis.",
    )

    lane(ax, 9.25, 1.7, "1. Prepare policy text", "policy")
    prep = [
        (1.05, 9.58, 3.35, 0.95),
        (4.85, 9.58, 3.35, 0.95),
        (8.65, 9.58, 3.35, 0.95),
        (12.45, 9.58, 3.35, 0.95),
        (16.25, 9.58, 3.35, 0.95),
    ]
    box(ax, *prep[0], "Source Loader", "title, date, source URL, parsed full text", "source")
    box(ax, *prep[1], "Analysis Gate", "skip tiny, incomplete, repetitive, or non-impactable items", "policy")
    box(ax, *prep[2], "Length Gate", "only long sources enter compressor", "control")
    box(ax, *prep[3], "Compressor", "keep mechanism, scope, timeline, named sectors", "policy")
    box(ax, *prep[4], "Working Text", "original or compressed policy text", "source")
    arrow_chain(ax, prep)

    lane(ax, 6.0, 2.2, "2. Two-round hybrid search", "wiki")
    search = [
        (1.05, 6.55, 3.15, 1.15),
        (4.65, 6.55, 3.15, 1.15),
        (8.25, 6.55, 3.15, 1.15),
        (11.85, 6.55, 3.15, 1.15),
        (15.45, 6.55, 3.15, 1.15),
        (19.05, 6.55, 3.45, 1.15),
    ]
    box(ax, *search[0], "Round 1 Planner", "direct terms, semantic terms, downweight terms", "policy")
    box(ax, *search[1], "Search Round 1", "broad hybrid search over all 41 final wikis", "wiki")
    box(ax, *search[2], "Round 1 Evidence", "chunks include ticker, company, heading path, matched query", "wiki")
    box(ax, *search[3], "Round 2 Planner", "company-filtered search plan from round 1 candidates", "policy")
    box(ax, *search[4], "Search Round 2", "only companies surfaced in round 1 are searchable", "wiki")
    box(ax, *search[5], "Combined Evidence", "round 1 + round 2 compact render", "wiki")
    arrow_chain(ax, search)
    callout(ax, 8.9, 5.08, "Hybrid search combines exact/direct terms and semantic retrieval; generic terms are downweighted", "wiki")

    lane(ax, 2.65, 2.35, "3. Match and final impact", "output")
    decision = [
        (1.05, 3.08, 4.2, 1.15),
        (5.75, 3.08, 4.2, 1.15),
        (10.45, 3.08, 4.2, 1.15),
        (15.15, 3.08, 3.6, 1.15),
        (19.25, 3.08, 3.6, 1.15),
    ]
    box(ax, *decision[0], "Initial Match Node", "DeepSeek thinking, higher max token budget, stricter soft gate", "policy")
    box(ax, *decision[1], "No-Match Exit", "if match list is empty, save reason and stop", "control")
    box(ax, *decision[2], "Matched Companies", "0-8 target range, hard cap 15, company + reason JSON", "output")
    box(ax, *decision[3], "Impact Node", "GPT-5.2 high reasoning, wiki + news, optional cautious web search", "output")
    box(ax, *decision[4], "Policy Impact Row", "mechanism, direction, horizon, certainty, stock-level note", "output")
    arrow(ax, decision[0][0] + decision[0][2], decision[0][1] + decision[0][3] / 2, decision[1][0], decision[1][1] + decision[1][3] / 2)
    arrow(ax, decision[0][0] + decision[0][2], decision[0][1] + decision[0][3] / 2, decision[2][0], decision[2][1] + decision[2][3] / 2)
    arrow_chain(ax, decision[2:])
    callout(ax, 5.8, 1.75, "Cost rule: final impact calls happen only for matched companies with useful evidence", "output")

    out = ASSET_DIR / "policy_news_branch_detail.png"
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out


def render_company_disclosure_branch_detail() -> Path:
    fig, ax = new_canvas(
        "Company Disclosure Impact Branch",
        "Company disclosures already map to a ticker, so the branch skips RAG matching and analyzes impact directly against the current wiki.",
    )

    lane(ax, 9.25, 1.75, "1. Direct impact analysis", "disclosure")
    impact = [
        (1.05, 9.56, 3.5, 0.98),
        (5.0, 9.56, 3.5, 0.98),
        (8.95, 9.56, 3.5, 0.98),
        (12.9, 9.56, 4.05, 0.98),
        (17.4, 9.56, 4.1, 0.98),
    ]
    box(ax, *impact[0], "Disclosure Source", "annual, quarterly, semiannual, forecast, announcement", "source")
    box(ax, *impact[1], "Text Normalizer", "load source, remove boilerplate, preserve tables/events", "control")
    box(ax, *impact[2], "Compressor", "only long disclosures are compressed", "disclosure")
    box(ax, *impact[3], "Current Company Wiki", "latest wiki before any update", "wiki")
    box(ax, *impact[4], "Disclosure Impact Node", "impact first: business model, stock impact, wiki action decision", "disclosure")
    arrow_chain(ax, impact)

    lane(ax, 6.25, 2.0, "2. Wiki action routing", "wiki")
    actions = [
        (1.05, 6.63, 3.5, 1.05),
        (5.0, 6.63, 3.5, 1.05),
        (8.95, 6.63, 3.5, 1.05),
        (12.9, 6.63, 4.05, 1.05),
        (17.4, 6.63, 4.1, 1.05),
    ]
    box(ax, *actions[0], "No Update", "most announcements only save impact", "output")
    box(ax, *actions[1], "Small Patch", "only change affected facts; keep stable wiki structure", "wiki")
    box(ax, *actions[2], "Force Rebuild", "annual report, prospectus, or truly major event", "wiki")
    box(ax, *actions[3], "Archive First", "old wiki version is stored before overwrite", "control")
    box(ax, *actions[4], "Apply + Manifest", "updated wiki becomes the new final wiki", "wiki")
    arrow_chain(ax, actions[1:])
    callout(ax, 7.8, 5.18, "All impact outputs are saved before small patch or rebuild starts", "disclosure")

    lane(ax, 2.75, 2.35, "3. Daily outputs and next-run readiness", "output")
    outputs = [
        (1.05, 3.18, 4.05, 1.1),
        (5.55, 3.18, 4.05, 1.1),
        (10.05, 3.18, 4.05, 1.1),
        (14.55, 3.18, 4.05, 1.1),
        (19.05, 3.18, 3.8, 1.1),
    ]
    box(ax, *outputs[0], "Impact Report", "concise Markdown with horizon, direction, certainty", "output")
    box(ax, *outputs[1], "Company Action Row", "date, ticker, source, action, wiki decision, status", "output")
    box(ax, *outputs[2], "Reduced Rebuild Queue", "batched after all disclosure impacts finish", "wiki")
    box(ax, *outputs[3], "Final Index Refresh", "single wiki RAG index rebuild per run", "wiki")
    box(ax, *outputs[4], "Daily Snapshot", "latest wiki collection and archived old versions", "output")
    arrow_chain(ax, outputs)

    ax.text(
        0.78,
        0.75,
        "Default stance: preserve the wiki unless the disclosure adds durable company knowledge. Rebuild is intentionally rare.",
        fontsize=11,
        color=MUTED,
    )

    out = ASSET_DIR / "company_disclosure_branch_detail.png"
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out


def render_reduced_wiki_builder_detail() -> Path:
    fig, ax = new_canvas(
        "Reduced Wiki Builder Detail",
        "The default rebuild route creates a compact, evidence-bound company wiki after a material source update.",
    )

    lane(ax, 9.05, 1.95, "1. Source selection rules", "wiki")
    roles = [
        (1.05, 9.45, 3.7, 1.05),
        (5.15, 9.45, 3.7, 1.05),
        (9.25, 9.45, 3.7, 1.05),
        (13.35, 9.45, 3.7, 1.05),
        (17.45, 9.45, 4.25, 1.05),
    ]
    box(ax, *roles[0], "Primary Annual", "latest real annual report", "wiki")
    box(ax, *roles[1], "Latest Periodic", "latest real Q1, Q3, semiannual, or annual report", "wiki")
    box(ax, *roles[2], "Origin Document", "prospectus or fundraising document when available", "wiki")
    box(ax, *roles[3], "Material Events", "recent announcements with durable company changes", "wiki")
    box(ax, *roles[4], "Research Context", "broker reports as secondary vocabulary and framing", "source")
    arrow_chain(ax, roles)

    lane(ax, 5.75, 2.1, "2. Retrieval planning and source package", "policy")
    retrieval = [
        (1.05, 6.18, 3.3, 1.1),
        (4.85, 6.18, 3.3, 1.1),
        (8.65, 6.18, 3.3, 1.1),
        (12.45, 6.18, 3.3, 1.1),
        (16.25, 6.18, 5.45, 1.1),
    ]
    box(ax, *retrieval[0], "Tiny Primer", "small snippets prevent oversized planning context", "control")
    box(ax, *retrieval[1], "Brainstormer", "JSON retrieval plan, no prose", "policy")
    box(ax, *retrieval[2], "Hybrid Retrieval", "heading, keyword, semantic, table-aware search", "wiki")
    box(ax, *retrieval[3], "Evidence Package", "sectioned source package with source boundaries", "wiki")
    box(ax, *retrieval[4], "Durable Sections", "business, products, customers, finance, obligations, competition, freshness", "wiki")
    arrow_chain(ax, retrieval)

    lane(ax, 2.3, 2.25, "3. Reduced writer and publication contract", "output")
    publish = [
        (1.05, 2.78, 4.0, 1.15),
        (5.55, 2.78, 4.0, 1.15),
        (10.05, 2.78, 4.0, 1.15),
        (14.55, 2.78, 4.0, 1.15),
        (19.05, 2.78, 3.8, 1.15),
    ]
    box(ax, *publish[0], "Writer Prompt", "preserve uncertainty, stage wording, and evidence limits", "policy")
    box(ax, *publish[1], "Reduced Wiki", "2000-4000 Chinese chars, Markdown, retrieval-friendly", "wiki")
    box(ax, *publish[2], "Archive Old Wiki", "version previous final wiki before overwrite", "control")
    box(ax, *publish[3], "Update Manifest", "source roles and build metadata", "output")
    box(ax, *publish[4], "Rebuild Wiki Index", "ready for next policy RAG run", "wiki")
    arrow_chain(ax, publish)

    out = ASSET_DIR / "reduced_wiki_builder_detail.png"
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out


def render_full_wiki_builder_detail() -> Path:
    fig, ax = new_canvas(
        "Full Wiki Builder Detail",
        "The full route is a heavier research-loop build for onboarding, manual deep review, and complex companies.",
    )

    lane(ax, 9.25, 1.65, "1. Orient and assign research tracks", "policy")
    orient = [
        (1.05, 9.58, 3.55, 0.95),
        (5.0, 9.58, 3.55, 0.95),
        (8.95, 9.58, 3.55, 0.95),
        (12.9, 9.58, 4.05, 0.95),
        (17.4, 9.58, 4.1, 0.95),
    ]
    box(ax, *orient[0], "Corpus Preflight", "validate source coverage and local hybrid index", "source")
    box(ax, *orient[1], "Anchor Brief", "company scope, obvious gaps, starting hypotheses", "policy")
    box(ax, *orient[2], "Research Router", "assign track ownership and work sequence", "policy")
    box(ax, *orient[3], "Track Set", "company map, business engine, economics, recent risks", "policy")
    box(ax, *orient[4], "Local Tools First", "hybrid search and table chunks before web search", "wiki")
    arrow_chain(ax, orient)

    lane(ax, 6.0, 2.2, "2. Research loop and evidence control", "control")
    research = [
        (1.05, 6.55, 3.35, 1.15),
        (4.85, 6.55, 3.35, 1.15),
        (8.65, 6.55, 3.35, 1.15),
        (12.45, 6.55, 3.35, 1.15),
        (16.25, 6.55, 5.3, 1.15),
    ]
    box(ax, *research[0], "Planner Loops", "each track searches, reasons, and records source-located facts", "policy")
    box(ax, *research[1], "Evidence Bank", "committed facts with source locator and boundaries", "control")
    box(ax, *research[2], "Mutable Notes", "working synthesis separate from committed evidence", "control")
    box(ax, *research[3], "Round Draft", "business mechanism and operating model synthesis", "control")
    box(ax, *research[4], "Critic + Fixes", "unsupported inference, stale facts, missing mechanism, weak downstream usefulness", "control")
    arrow_chain(ax, research)

    lane(ax, 2.65, 2.35, "3. Valuation lens and full wiki publication", "output")
    final = [
        (1.05, 3.08, 3.75, 1.15),
        (5.25, 3.08, 3.75, 1.15),
        (9.45, 3.08, 3.75, 1.15),
        (13.65, 3.08, 3.75, 1.15),
        (17.85, 3.08, 4.4, 1.15),
    ]
    box(ax, *final[0], "Valuation Lens", "methods, assumptions, fragility, no target-price framing", "control")
    box(ax, *final[1], "Final Writer", "audit draft, critic notes, valuation memo, evidence bank", "wiki")
    box(ax, *final[2], "Full Wiki", "long-form Markdown company knowledge object", "wiki")
    box(ax, *final[3], "Archive + Manifest", "same publication contract as reduced", "output")
    box(ax, *final[4], "Wiki RAG Index", "full wiki can be indexed for future news impact analysis", "wiki")
    arrow_chain(ax, final)

    out = ASSET_DIR / "full_wiki_builder_detail.png"
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out


def render_wiki_build_agent() -> Path:
    fig, ax = new_canvas(
        "Company Wiki Build Agent: Mode Map",
        "Two wiki builders share the same document corpus and publishing contract, but optimize for different latency and depth.",
    )

    lane(ax, 9.35, 1.75, "Shared corpus and index foundation", "source")
    foundation = [
        (1.05, 9.68, 3.35, 0.98),
        (4.85, 9.68, 3.35, 0.98),
        (8.65, 9.68, 3.35, 0.98),
        (12.45, 9.68, 4.05, 0.98),
        (16.95, 9.68, 4.75, 0.98),
    ]
    box(ax, *foundation[0], "Document Corpus", "annual reports, prospectuses, filings, broker research", "source")
    box(ax, *foundation[1], "LLM-Ready Text", "parsed Markdown with metadata and body sidecars", "source")
    box(ax, *foundation[2], "Chunk Index", "text, table rows, table bridges, embeddings", "wiki")
    box(ax, *foundation[3], "Company Identity", "aliases, products, entities, trigger terms", "source")
    box(ax, *foundation[4], "Preflight", "corpus status, missing index, resume state, run events", "control")
    arrow_chain(ax, foundation)

    lane(ax, 6.35, 2.05, "Reduced builder: daily default after material source updates", "wiki")
    reduced = [
        (1.05, 6.75, 3.3, 1.08),
        (4.8, 6.75, 3.3, 1.08),
        (8.55, 6.75, 3.3, 1.08),
        (12.3, 6.75, 3.5, 1.08),
        (16.25, 6.75, 5.45, 1.08),
    ]
    box(ax, *reduced[0], "Source Rules", "latest annual, latest periodic, origin doc, recent material events", "wiki")
    box(ax, *reduced[1], "Brainstormer", "Qwen JSON plan: terms, selected docs, downweight terms", "policy")
    box(ax, *reduced[2], "Retrieval Executor", "heading, direct/body, semantic passes with fallbacks", "wiki")
    box(ax, *reduced[3], "Source Package", "writer-visible evidence; trace saved separately", "wiki")
    box(ax, *reduced[4], "Reduced Writer", "Kimi writes compact 2000-4000 Chinese-char wiki from source package only", "wiki")
    arrow_chain(ax, reduced)
    callout(ax, 9.4, 5.35, "Brainstormer JSON controls retrieval; it is not evidence for the writer", "wiki")

    lane(ax, 2.85, 2.45, "Full builder: deep company onboarding and review", "policy")
    full = [
        (1.05, 3.35, 3.05, 1.1),
        (4.5, 3.35, 3.05, 1.1),
        (7.95, 3.35, 3.05, 1.1),
        (11.4, 3.35, 3.05, 1.1),
        (14.85, 3.35, 3.05, 1.1),
        (18.3, 3.35, 4.0, 1.1),
    ]
    box(ax, *full[0], "Anchor", "deterministic bundle to anchor memo and first brief", "source")
    box(ax, *full[1], "Research Loop V1", "router -> 1-4 planner subagents -> evidence bank", "policy")
    box(ax, *full[2], "Draft + Valuation V1", "draft_1, method selection, assumptions, calculators", "control")
    box(ax, *full[3], "Critic", "draft, valuation, evidence, gaps, stale facts", "control")
    box(ax, *full[4], "Research + Valuation V2", "critic-driven second research and refreshed valuation", "policy")
    box(ax, *full[5], "Final Wiki Writer", "GPT-5.5 high reasoning synthesizes one durable company_wiki.md", "output")
    arrow_chain(ax, full)

    lane(ax, 0.82, 1.45, "Shared publication contract", "output")
    publish = [
        (1.05, 1.05, 4.2, 0.72),
        (5.75, 1.05, 4.2, 0.72),
        (10.45, 1.05, 4.2, 0.72),
        (15.15, 1.05, 3.8, 0.72),
        (19.45, 1.05, 3.4, 0.72),
    ]
    box(ax, *publish[0], "Final Markdown Wiki", "retrieval + reasoning object", "output", title_size=10, body_size=8)
    box(ax, *publish[1], "Archive Old Version", "previous final wiki is retained", "control", title_size=10, body_size=8)
    box(ax, *publish[2], "Manifest", "source roles and build metadata", "output", title_size=10, body_size=8)
    box(ax, *publish[3], "Index Refresh", "hybrid wiki RAG chunks", "wiki", title_size=10, body_size=8)
    box(ax, *publish[4], "Downstream Impact", "policy and disclosure agents", "output", title_size=10, body_size=8)
    arrow_chain(ax, publish)

    out = ASSET_DIR / "wiki_build_agent_architecture.png"
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out


def render_reduced_wiki_builder_detail() -> Path:
    fig, ax = new_canvas(
        "Reduced Wiki Builder: Two-Node Retrieval Package Pipeline",
        "Reduced wiki generation separates planning from evidence. The writer sees only the deterministic source package.",
    )

    lane(ax, 9.55, 1.55, "1. Build brainstormer input", "source")
    inputs = [
        (1.05, 9.85, 3.3, 0.88),
        (4.75, 9.85, 3.3, 0.88),
        (8.45, 9.85, 3.3, 0.88),
        (12.15, 9.85, 3.3, 0.88),
        (15.85, 9.85, 5.55, 0.88),
    ]
    box(ax, *inputs[0], "Company Info", "ticker, name, industry, valuation context", "source", body_size=9)
    box(ax, *inputs[1], "Tiny Primer", "small semantic snippets from fixed sources", "source", body_size=9)
    box(ax, *inputs[2], "Fixed Search Contract", "cached sessions and required JSON shape", "control", body_size=9)
    box(ax, *inputs[3], "File Availability", "fixed sources, announcement candidates, research candidates", "source", body_size=9)
    box(ax, *inputs[4], "Brainstormer Input", "system prompt + cached fixed context + dynamic user prompt", "policy", body_size=9)
    arrow_chain(ax, inputs)

    lane(ax, 6.65, 2.05, "2. Brainstormer node: retrieval control only", "policy")
    plan = [
        (1.05, 7.08, 3.2, 1.1),
        (4.7, 7.08, 3.2, 1.1),
        (8.35, 7.08, 3.2, 1.1),
        (12.0, 7.08, 3.2, 1.1),
        (15.65, 7.08, 5.75, 1.1),
    ]
    box(ax, *plan[0], "Qwen Brainstormer", "thinking + explicit cache, JSON content required", "policy")
    box(ax, *plan[1], "Company Terms", "products, technologies, customers, assets, risks, stages", "policy")
    box(ax, *plan[2], "Selected Docs", "up to 6 announcements and 2 research reports", "policy")
    box(ax, *plan[3], "Session Overrides", "extra keywords and semantic queries per session", "policy")
    box(ax, *plan[4], "Negative Terms", "meeting, dividend, governance, legal, sponsor and other noise", "control")
    arrow_chain(ax, plan)
    callout(ax, 7.2, 5.78, "Plan doc_ids are validated against corpus; invalid selections are logged and ignored", "policy")

    lane(ax, 3.55, 2.35, "3. Deterministic source package executor", "wiki")
    executor = [
        (1.05, 4.02, 3.05, 1.15),
        (4.5, 4.02, 3.05, 1.15),
        (7.95, 4.02, 3.05, 1.15),
        (11.4, 4.02, 3.05, 1.15),
        (14.85, 4.02, 3.05, 1.15),
        (18.3, 4.02, 4.0, 1.15),
    ]
    box(ax, *executor[0], "Source Selection", "fixed sources first; plan selections with fallback rules", "wiki")
    box(ax, *executor[1], "8 Sessions", "surface, business, products, counterparties, finance, capital, industry, freshness", "wiki")
    box(ax, *executor[2], "Search Passes", "heading, body/direct, semantic", "wiki")
    box(ax, *executor[3], "Rerank + Diversity", "dedupe, downweight noise, doc/heading/table caps", "wiki")
    box(ax, *executor[4], "Expansion", "same chunk, same heading, table, neighbor window", "wiki")
    box(ax, *executor[5], "Fallback", "relaxed heading, broader chunk kinds, base semantic, thin section if still missing", "control")
    arrow_chain(ax, executor)

    lane(ax, 1.0, 1.75, "4. Writer and audit artifacts", "output")
    writer = [
        (1.05, 1.35, 3.9, 0.95),
        (5.45, 1.35, 3.9, 0.95),
        (9.85, 1.35, 3.9, 0.95),
        (14.25, 1.35, 3.9, 0.95),
        (18.65, 1.35, 3.65, 0.95),
    ]
    box(ax, *writer[0], "Source Package", "only Sources, Session, Selected text enter writer prompt", "wiki")
    box(ax, *writer[1], "Retrieval Trace", "full terms, chunk IDs, scores, passes saved beside prompt", "control")
    box(ax, *writer[2], "Kimi Wiki Writer", "writes from source package only", "policy")
    box(ax, *writer[3], "Reduced Wiki", "2000-4000 Chinese chars; Markdown; source-bound", "output")
    box(ax, *writer[4], "Usage + Run Meta", "cost, cache, attempts, parse status", "output")
    arrow_chain(ax, writer)

    out = ASSET_DIR / "reduced_wiki_builder_detail.png"
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out


def render_full_wiki_builder_detail() -> Path:
    fig, ax = new_canvas(
        "Full Wiki Builder: v3 Artifact DAG",
        "The full agent builds one final company_wiki.md from anchor research, two company research loops, valuation loops, critic feedback, and final synthesis.",
    )

    lane(ax, 9.7, 1.45, "1. Anchor and first business agenda", "source")
    anchor = [
        (1.05, 9.98, 3.45, 0.82),
        (4.95, 9.98, 3.45, 0.82),
        (8.85, 9.98, 3.45, 0.82),
        (12.75, 9.98, 3.45, 0.82),
        (16.65, 9.98, 4.7, 0.82),
    ]
    box(ax, *anchor[0], "Anchor Source Bundle", "latest annual, periodic-like, prospectus-like", "source", body_size=8)
    box(ax, *anchor[1], "Anchor", "long-form anchor_memo", "policy", body_size=8)
    box(ax, *anchor[2], "Company Brief V1", "short repeated-read briefing", "policy", body_size=8)
    box(ax, *anchor[3], "Research Goals V1", "first company-research agenda", "policy", body_size=8)
    box(ax, *anchor[4], "Corpus Manifest", "raw families, post-annual windows, stock reports", "source", body_size=8)
    arrow_chain(ax, anchor)

    lane(ax, 7.05, 1.7, "2. Round-one company research and draft", "policy")
    research1 = [
        (1.05, 7.38, 3.1, 0.95),
        (4.55, 7.38, 3.1, 0.95),
        (8.05, 7.38, 3.1, 0.95),
        (11.55, 7.38, 3.1, 0.95),
        (15.05, 7.38, 3.1, 0.95),
        (18.55, 7.38, 3.8, 0.95),
    ]
    box(ax, *research1[0], "Router V1", "1-4 operational subagents", "policy", body_size=8)
    box(ax, *research1[1], "Planner Loop V1", "tools, working memory, done state", "policy", body_size=8)
    box(ax, *research1[2], "Evidence Bank V1", "committed source-located facts", "control", body_size=8)
    box(ax, *research1[3], "Loop Note V1", "track-keyed mutable synthesis", "control", body_size=8)
    box(ax, *research1[4], "Draft Writer V1", "anchor + evidence + note", "wiki", body_size=8)
    box(ax, *research1[5], "Draft 1", "first full company draft", "wiki", body_size=8)
    arrow_chain(ax, research1)

    lane(ax, 4.4, 1.7, "3. Valuation v1 and critic", "control")
    valuation1 = [
        (1.05, 4.73, 3.25, 0.95),
        (4.75, 4.73, 3.25, 0.95),
        (8.45, 4.73, 3.25, 0.95),
        (12.15, 4.73, 3.25, 0.95),
        (15.85, 4.73, 3.25, 0.95),
        (19.55, 4.73, 3.0, 0.95),
    ]
    box(ax, *valuation1[0], "Method Selector", "choose 3 methods from 9-method library", "control", body_size=8)
    box(ax, *valuation1[1], "Valuation Loop V1", "router + planner loop + evidence bank", "control", body_size=8)
    box(ax, *valuation1[2], "Assumption Reasoners", "parallel method-specific memos", "control", body_size=8)
    box(ax, *valuation1[3], "JSON + Calculators", "deterministic bear/base/bull outputs", "control", body_size=8)
    box(ax, *valuation1[4], "Valuation Memo V1", "anchors, checks, sensitivity, fragility", "control", body_size=8)
    box(ax, *valuation1[5], "First Critic", "draft + valuation + evidence + external freshness checks", "output", body_size=8)
    arrow_chain(ax, valuation1)

    lane(ax, 1.45, 2.0, "4. Critic-driven round two and final synthesis", "output")
    final = [
        (1.05, 1.9, 3.15, 1.08),
        (4.65, 1.9, 3.15, 1.08),
        (8.25, 1.9, 3.15, 1.08),
        (11.85, 1.9, 3.15, 1.08),
        (15.45, 1.9, 3.15, 1.08),
        (19.05, 1.9, 3.45, 1.08),
    ]
    box(ax, *final[0], "Brief V2", "anchor + draft_1 + critic_1", "policy")
    box(ax, *final[1], "Router + Loop V2", "critic gaps drive second company research", "policy")
    box(ax, *final[2], "Valuation Refresh V2", "fresh base packet, v2 assumptions, calculators", "control")
    box(ax, *final[3], "Final Input Packet", "anchor, draft, critic, evidence banks, valuation memos, notes", "source")
    box(ax, *final[4], "Final Wiki Writer", "GPT-5.5 high reasoning with web search", "output")
    box(ax, *final[5], "company_wiki.md", "one durable integrated company wiki", "output")
    arrow_chain(ax, final)

    out = ASSET_DIR / "full_wiki_builder_detail.png"
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out


def render_full_wiki_research_loop_detail() -> Path:
    fig, ax = new_canvas(
        "Full Wiki Research Loop Subagent Runtime",
        "Routers frame the loop. Planner subagents run tool turns, commit evidence, update loop notes, and stop when enough facts are gathered.",
    )

    lane(ax, 9.25, 1.75, "1. Router creates operational subagents", "policy")
    router = [
        (1.05, 9.58, 3.35, 0.98),
        (4.85, 9.58, 3.35, 0.98),
        (8.65, 9.58, 3.35, 0.98),
        (12.45, 9.58, 3.35, 0.98),
        (16.25, 9.58, 5.15, 0.98),
    ]
    box(ax, *router[0], "Router Input", "company brief or draft context, goals, critic, manifest", "source")
    box(ax, *router[1], "Research Router", "creates 1-4 subagents", "policy")
    box(ax, *router[2], "Assignments", "track ownership and specific gaps", "policy")
    box(ax, *router[3], "Status Board", "active tracks, budget state, done flags", "control")
    box(ax, *router[4], "Loop State", "shared evidence bank, loop mutable note, per-agent working memory", "control")
    arrow_chain(ax, router)

    lane(ax, 5.75, 2.45, "2. Planner turn loop", "wiki")
    turn = [
        (1.05, 6.18, 3.05, 1.1),
        (4.5, 6.18, 3.05, 1.1),
        (7.95, 6.18, 3.05, 1.1),
        (11.4, 6.18, 3.05, 1.1),
        (14.85, 6.18, 3.05, 1.1),
        (18.3, 6.18, 4.0, 1.1),
    ]
    box(ax, *turn[0], "Subagent View", "assignment, brief, loop note, evidence, manifest, working memory", "source")
    box(ax, *turn[1], "Wiki Planner Turn", "one Kimi API request with tools", "policy")
    box(ax, *turn[2], "Tool Calls", "search, expand, web, commit, note, done", "wiki")
    box(ax, *turn[3], "Runtime Executes", "tool results are persisted", "control")
    box(ax, *turn[4], "Merge", "new evidence, updated note, new working memory", "control")
    box(ax, *turn[5], "Next Turn", "still-active subagents see updated shared state", "wiki")
    arrow_chain(ax, turn)
    callout(ax, 8.85, 4.72, "Company and valuation loops use separate evidence banks; final writer sees completed loop artifacts", "wiki")

    lane(ax, 2.15, 2.25, "3. Tools and stop semantics", "output")
    tools = [
        (1.05, 2.65, 3.4, 1.05),
        (4.9, 2.65, 3.4, 1.05),
        (8.75, 2.65, 3.4, 1.05),
        (12.6, 2.65, 3.4, 1.05),
        (16.45, 2.65, 4.95, 1.05),
    ]
    box(ax, *tools[0], "Corpus Tools", "search_corpus and expand_corpus_context", "wiki")
    box(ax, *tools[1], "Freshness Tool", "limited web_search for corpus-external gaps", "output")
    box(ax, *tools[2], "Commit Evidence", "source-located facts become evidence IDs", "control")
    box(ax, *tools[3], "Update Note", "track-keyed mutable synthesis", "control")
    box(ax, *tools[4], "Stop", "done_gathering per agent, or all done, or max_turns=6", "output")
    arrow_chain(ax, tools)

    out = ASSET_DIR / "full_wiki_research_loop_detail.png"
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out


def main() -> int:
    print(render_news_impact_agent())
    print(render_wiki_build_agent())
    print(render_policy_news_branch_detail())
    print(render_company_disclosure_branch_detail())
    print(render_reduced_wiki_builder_detail())
    print(render_full_wiki_builder_detail())
    print(render_full_wiki_research_loop_detail())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
