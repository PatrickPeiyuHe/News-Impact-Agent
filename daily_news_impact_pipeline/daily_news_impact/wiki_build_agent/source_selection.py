from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, timedelta
import re
from typing import Iterable

from .contracts import DocumentRecord, SourceRoleAssignment


ANNUAL_FAMILIES = {"annual_report"}
PERIODIC_FAMILIES = {
    "quarterly_report_q1",
    "quarterly_report_q3",
    "semiannual_report",
    "annual_report",
}
RESEARCH_FAMILIES = {"stock_report", "research_report", "broker_report"}
ANNOUNCEMENT_FAMILIES = {"announcement"}

ANNUAL_TITLE_TERMS = ("年度报告", "年报")
Q1_TITLE_TERMS = ("第一季度报告", "一季报", "2026年第一季度")
Q3_TITLE_TERMS = ("第三季度报告", "三季报")
SEMI_TITLE_TERMS = ("半年度报告", "半年报")
ORIGIN_TITLE_TERMS = ("招股说明书", "招股意向书", "募集说明书")

PERIODIC_EXCLUDE_TERMS = (
    "摘要",
    "提示性公告",
    "更正",
    "修订",
    "取消",
    "问询函",
    "回复",
    "审计报告",
)

MATERIAL_SIGNAL_TERMS = {
    "operating_data": ("经营数据", "主要经营数据", "销售数据", "订单", "中标", "定点", "合同"),
    "earnings": ("业绩预告", "业绩快报", "盈利预测", "亏损", "扭亏", "净利润"),
    "asset_project_transaction": ("收购", "出售", "重大资产", "资产重组", "项目", "产能", "投产", "募投"),
    "financing_or_obligation": ("可转债", "定增", "向特定对象发行", "融资租赁", "担保", "授信"),
    "control_or_group": ("控制权", "实际控制人", "控股股东", "权益变动", "同业竞争"),
    "customer_order": ("客户", "供应商", "订单", "合同", "中标", "定点", "框架协议"),
    "risk_event": ("诉讼", "仲裁", "处罚", "风险提示", "减值", "停产", "被调查"),
}

ROUTINE_ANNOUNCEMENT_TERMS = (
    "董事会",
    "监事会",
    "股东大会",
    "会议资料",
    "会议决议",
    "独立董事",
    "法律意见",
    "保荐",
    "核查意见",
    "持续督导",
    "现金管理",
    "利润分配",
    "权益分派",
    "分红",
    "投资者关系",
    "制度",
    "章程",
)


def parse_date(value: str) -> date:
    raw = str(value or "").strip()[:10]
    if not raw:
        return date.min
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"):
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            pass
    return date.min


def compact_title(value: str) -> str:
    return re.sub(r"\s+", "", str(value or ""))


def contains_any(text: str, terms: Iterable[str]) -> bool:
    return any(term in text for term in terms)


def is_actual_annual_report(doc: DocumentRecord) -> bool:
    title = compact_title(doc.title)
    if doc.doc_family in ANNUAL_FAMILIES:
        return not contains_any(title, PERIODIC_EXCLUDE_TERMS)
    return contains_any(title, ANNUAL_TITLE_TERMS) and not contains_any(title, PERIODIC_EXCLUDE_TERMS)


def is_actual_periodic_like(doc: DocumentRecord) -> bool:
    title = compact_title(doc.title)
    if contains_any(title, PERIODIC_EXCLUDE_TERMS):
        return False
    if doc.doc_family in PERIODIC_FAMILIES:
        return True
    return contains_any(title, Q1_TITLE_TERMS + Q3_TITLE_TERMS + SEMI_TITLE_TERMS + ANNUAL_TITLE_TERMS)


def periodic_kind(doc: DocumentRecord) -> str:
    title = compact_title(doc.title)
    if contains_any(title, Q1_TITLE_TERMS):
        return "q1"
    if contains_any(title, SEMI_TITLE_TERMS):
        return "semiannual"
    if contains_any(title, Q3_TITLE_TERMS):
        return "q3"
    if contains_any(title, ANNUAL_TITLE_TERMS):
        return "annual"
    return str(doc.doc_family or "periodic")


def is_origin_document(doc: DocumentRecord) -> bool:
    return contains_any(compact_title(doc.title), ORIGIN_TITLE_TERMS)


def classify_event_families(doc: DocumentRecord) -> tuple[str, ...]:
    title = compact_title(doc.title)
    if contains_any(title, ROUTINE_ANNOUNCEMENT_TERMS) and not contains_any(
        title,
        MATERIAL_SIGNAL_TERMS["earnings"]
        + MATERIAL_SIGNAL_TERMS["asset_project_transaction"]
        + MATERIAL_SIGNAL_TERMS["customer_order"],
    ):
        return ()
    families = [family for family, terms in MATERIAL_SIGNAL_TERMS.items() if contains_any(title, terms)]
    return tuple(sorted(set(families)))


def latest_document(docs: Iterable[DocumentRecord]) -> DocumentRecord | None:
    candidates = list(docs)
    if not candidates:
        return None
    return max(candidates, key=lambda item: (parse_date(item.publish_date), item.text_length, item.doc_id))


def source_cutoff(documents: Iterable[DocumentRecord]) -> date:
    dates = [parse_date(item.publish_date) for item in documents if parse_date(item.publish_date) != date.min]
    if not dates:
        return date.today() - timedelta(days=365)
    return max(dates) - timedelta(days=365)


def choose_recent_material_announcements(
    documents: Iterable[DocumentRecord],
    *,
    cutoff: date,
    max_count: int = 6,
) -> list[SourceRoleAssignment]:
    grouped: dict[str, list[tuple[DocumentRecord, tuple[str, ...]]]] = defaultdict(list)
    for doc in documents:
        if doc.doc_family not in ANNOUNCEMENT_FAMILIES:
            continue
        if parse_date(doc.publish_date) < cutoff:
            continue
        families = classify_event_families(doc)
        if not families:
            continue
        cluster_key = families[0] + ":" + compact_title(doc.title)[:24]
        grouped[cluster_key].append((doc, families))

    selected: list[tuple[DocumentRecord, tuple[str, ...]]] = []
    for items in grouped.values():
        selected.append(max(items, key=lambda pair: (parse_date(pair[0].publish_date), pair[0].text_length, pair[0].doc_id)))

    family_weight = {
        "earnings": 7,
        "customer_order": 6,
        "asset_project_transaction": 5,
        "operating_data": 4,
        "financing_or_obligation": 3,
        "control_or_group": 3,
        "risk_event": 3,
    }
    selected.sort(
        key=lambda pair: (
            max(family_weight.get(item, 0) for item in pair[1]),
            parse_date(pair[0].publish_date),
            pair[0].text_length,
        ),
        reverse=True,
    )
    return [
        SourceRoleAssignment(
            role="recent_material_announcement",
            document=doc,
            reason="recent material announcement selected by title/event-family signal",
            event_families=families,
        )
        for doc, families in selected[:max_count]
    ]


def choose_secondary_research(
    documents: Iterable[DocumentRecord],
    *,
    cutoff: date,
    max_count: int = 2,
) -> list[SourceRoleAssignment]:
    candidates = [
        item
        for item in documents
        if item.doc_family in RESEARCH_FAMILIES and parse_date(item.publish_date) >= cutoff and item.text_length > 500
    ]
    candidates.sort(key=lambda item: (parse_date(item.publish_date), item.text_length, item.doc_id), reverse=True)
    return [
        SourceRoleAssignment(
            role="secondary_research_context",
            document=doc,
            reason="recent broker research used only for terminology, framing, and trigger variables",
        )
        for doc in candidates[:max_count]
    ]


def select_reduced_wiki_sources(documents: Iterable[DocumentRecord]) -> tuple[SourceRoleAssignment, ...]:
    """Select the source package used by the reduced wiki builder."""

    docs = list(documents)
    cutoff = source_cutoff(docs)
    assignments: list[SourceRoleAssignment] = []

    annual = latest_document(item for item in docs if is_actual_annual_report(item))
    if annual:
        assignments.append(
            SourceRoleAssignment(
                role="primary_annual_report",
                document=annual,
                reason="latest actual annual report is the main primary source",
            )
        )

    periodic = latest_document(item for item in docs if is_actual_periodic_like(item) and item.doc_id != (annual.doc_id if annual else ""))
    if periodic:
        assignments.append(
            SourceRoleAssignment(
                role="latest_periodic_like",
                document=periodic,
                reason=f"latest periodic-like report after filtering abstracts/corrections; kind={periodic_kind(periodic)}",
            )
        )

    origin = latest_document(item for item in docs if is_origin_document(item))
    if origin:
        assignments.append(
            SourceRoleAssignment(
                role="origin_document",
                document=origin,
                reason="prospectus or fundraising document used for durable origin/business detail",
            )
        )

    assignments.extend(choose_recent_material_announcements(docs, cutoff=cutoff))
    assignments.extend(choose_secondary_research(docs, cutoff=cutoff))
    return tuple(assignments)
