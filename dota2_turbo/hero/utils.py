from django.db.models import Case, When, IntegerField


SORT_TIER_ORDER = Case(
    When(tier="S", then=1),
    When(tier="A", then=2),
    When(tier="B", then=3),
    When(tier="C", then=4),
    When(tier="D", then=5),
    output_field=IntegerField(),
)

POSITIONS = [
    "All",
    "Core Safe",
    "Core Mid",
    "Core Off",
    "Support Off",
    "Support Safe"
]

PERIODS = {
    "month": "Last 30 days",
    "3months": "Last 90 days",
    "6months": "Last 180 days"
}

SORT_MAP = {
    "winrate": "winrate",
    "pickrate": "pickrate",
    "tier": "tier",
    "name": "hero__name",
}

SORT_HEADERS = [
    ("name", "Hero"),
    ("winrate", "Win rate"),
    ("pickrate", "Pick rate"),
    ("tier", "Tier"),
]

FACET_SORT_HEADERS = [
    ("name", "Facet / Hero"),
    ("winrate", "Win rate"),
    ("pickrate", "Pick rate"),
    ("tier", "Tier"),
]


def calculate_tier(winrate):
    if winrate >= 53.5:
        tier = "S"
    elif winrate >= 51.5:
        tier = "A"
    elif winrate >= 49.5:
        tier = "B"
    elif winrate >= 47.5:
        tier = "C"
    else:
        tier = "D"
    return tier


def common_filters(
    queryset,
    *,
    period=None,
    position=None,
    sort="winrate",
    direction="desc",
    sort_map=None,
):

    if period is not None:
        queryset = queryset.filter(period=period)

    if position and position != "All":
        queryset = queryset.filter(hero__positions__contains=[position])

    if sort not in sort_map:
        sort = "winrate"

    sort_field = sort_map[sort]

    if sort_field == "tier":
        queryset = queryset.annotate(tier_order=SORT_TIER_ORDER)
        order = "-tier_order" if direction == "desc" else "tier_order"
        queryset = queryset.order_by(order)
    else:
        order = f"-{sort_field}" if direction == "desc" else sort_field
        queryset = queryset.order_by(order)

    return queryset
