"""Время: русские склонения, интервалы, парсинг длительностей."""

from __future__ import annotations

import re
import time
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

import config

TZ = ZoneInfo(config.TIMEZONE)

MONTHS_GEN = [
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря",
]

UNITS = [
    (31536000, ("год", "года", "лет")),
    (2592000, ("месяц", "месяца", "месяцев")),
    (604800, ("неделя", "недели", "недель")),
    (86400, ("день", "дня", "дней")),
    (3600, ("час", "часа", "часов")),
    (60, ("минута", "минуты", "минут")),
    (1, ("секунда", "секунды", "секунд")),
]

ALIASES = {
    "s": 1, "sec": 1, "с": 1, "сек": 1,
    "m": 60, "min": 60, "мин": 60, "м": 60,
    "h": 3600, "hour": 3600, "ч": 3600, "час": 3600,
    "d": 86400, "day": 86400, "д": 86400, "день": 86400,
    "w": 604800, "week": 604800, "н": 604800, "нед": 604800,
    "mo": 2592000, "mon": 2592000, "month": 2592000, "мес": 2592000,
    "y": 31536000, "year": 31536000, "г": 31536000, "год": 31536000, "л": 31536000,
}


def plural(n: int, forms: tuple[str, str, str]) -> str:
    n = abs(n) % 100
    if 11 <= n <= 14:
        return forms[2]
    n %= 10
    if n == 1:
        return forms[0]
    if 2 <= n <= 4:
        return forms[1]
    return forms[2]


def human_delta(seconds: float, max_units: int = 2) -> str:
    seconds = int(max(0, seconds))
    if seconds < 1:
        return "0 секунд"
    parts: list[str] = []
    left = seconds
    skip_weeks = seconds >= 2592000 or max_units < 3
    for size, forms in [u for u in UNITS if not (u[0] == 604800 and skip_weeks)]:
        if left < size:
            continue
        value, left = divmod(left, size)
        parts.append(f"{value} {plural(value, forms)}")
        if len(parts) >= max_units:
            break
    return ", ".join(parts)


def human_ms(elapsed: float) -> str:
    total_ms = int(round(elapsed * 1000))
    sec, ms = divmod(total_ms, 1000)
    if sec:
        return f"{sec} {plural(sec, ('секунду', 'секунды', 'секунд'))} и {ms} миллисекунд"
    return f"{ms} миллисекунд"


def parse_duration(raw: str) -> Optional[int]:
    if not raw:
        return None
    total, found = 0, False
    for num, unit in re.findall(r"(\d+)\s*([a-zA-Zа-яА-Я]*)", raw.strip().lower()):
        unit = unit.strip()
        if unit and unit not in ALIASES:
            for key in sorted(ALIASES, key=len, reverse=True):
                if unit.startswith(key):
                    unit = key
                    break
            else:
                return None
        total += int(num) * ALIASES.get(unit, 1)
        found = True
    return total if found and total > 0 else None


def fmt_dt(ts: float) -> str:
    return f"{datetime.fromtimestamp(ts, TZ):%d.%m.%Y, %H:%M:%S} {config.TZ_LABEL}"


def fmt_dt_short(ts: float) -> str:
    return f"{datetime.fromtimestamp(ts, TZ):%d.%m.%y %H:%M:%S}"


def fmt_dt_long(ts: float) -> str:
    dt = datetime.fromtimestamp(ts, TZ)
    return f"{dt.day} {MONTHS_GEN[dt.month - 1]} {dt.year} г., {dt:%H:%M}"


def fmt_clock(ts: Optional[float] = None) -> str:
    return f"{datetime.fromtimestamp(ts if ts else time.time(), TZ):%H:%M:%S}"


def ago(ts: float, max_units: int = 1) -> str:
    """Округлённо, как в боте-образце: 27 дней -> 'месяц назад', 17 -> '17 дней назад'."""
    seconds = int(max(0, time.time() - ts))
    minutes, hours, days = seconds / 60, seconds / 3600, seconds / 86400

    if seconds < 45:
        return "несколько секунд назад"
    if seconds < 90:
        return "минуту назад"
    if minutes < 45:
        n = round(minutes)
        return f"{n} {plural(n, UNITS[5][1])} назад"
    if minutes < 90:
        return "час назад"
    if hours < 22:
        n = round(hours)
        return f"{n} {plural(n, UNITS[4][1])} назад"
    if hours < 36:
        return "день назад"
    if days < 26:
        n = round(days)
        return f"{n} {plural(n, UNITS[3][1])} назад"
    if days < 46:
        return "месяц назад"
    if days < 320:
        n = round(days / 30)
        return f"{n} {plural(n, UNITS[1][1])} назад"
    if days < 548:
        return "год назад"
    n = round(days / 365)
    return f"{n} {plural(n, UNITS[0][1])} назад"


def uptime_line(started_at: float) -> str:
    return f"{human_delta(time.time() - started_at, 4)} назад; в {fmt_dt_long(started_at)}"