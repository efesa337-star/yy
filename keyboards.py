"""Инлайн-клавиатуры."""

from __future__ import annotations

from typing import Any, Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config
from db import db
from texts import LANGS, t

ON, OFF = "Вкл", "Выкл"
YES, NO = "Да", "Нет"

# порядок кнопок профиля — строго как в боте-образце
PROFILE_FIELDS: list[tuple[str, str]] = [
    ("media_meta", "btn_media_meta"),
    ("autoedit", "btn_autoedit"),
    ("protect", "btn_protect"),
    ("tag", "btn_tag"),
    ("tag_link", "btn_tag_link"),
]

PROFILE_FIELDS_TAIL: list[tuple[str, str]] = [
    ("keep_username", "btn_keep_username"),
    ("del_warning", "btn_del_warning"),
    ("reaction", "btn_reaction"),
    ("specials", "btn_specials"),
    ("autoreply", "btn_autoreply"),
    ("spoiler_in", "btn_spoiler_in"),
    ("spoiler_out", "btn_spoiler_out"),
    ("modernize", "btn_modernize"),
]

ALL_TOGGLES = {f for f, _ in PROFILE_FIELDS + PROFILE_FIELDS_TAIL} | {"badge"}

AUTODEL_PRESETS = [
    ("7 секунд", 7),
    ("15 секунд", 15),
    ("30 секунд", 30),
    ("1 минута", 60),
    ("2 минуты", 120),
    ("5 минут", 300),
    ("10 минут", 600),
    ("15 минут", 900),
    ("30 минут", 1800),
]


def flag(value: Any) -> str:
    return ON if value else OFF


def yesno(value: Any) -> str:
    return YES if value else NO


# --------------------------------------------------------------------------- #
#                                   профиль                                    #
# --------------------------------------------------------------------------- #

def profile_kb(
    user: dict[str, Any], ignores: int = 0, pm_blocks: int = 0
) -> InlineKeyboardMarkup:
    """Порядок и состав кнопок — один в один как в боте-образце (15 строк)."""
    lang = user["lang"]
    kb = InlineKeyboardBuilder()
    for field, key in PROFILE_FIELDS:
        kb.row(
            InlineKeyboardButton(text=t(lang, key, v=flag(user[field])), callback_data=f"t:{field}")
        )
    kb.row(
        InlineKeyboardButton(text=t(lang, "btn_ignore", n=ignores), callback_data="open:ignore"),
        InlineKeyboardButton(text=t(lang, "btn_ignore_pm", n=pm_blocks), callback_data="open:pmblock"),
    )
    autodel = f"{user['autodel']} sec" if user["autodel"] else "Null"
    kb.row(
        InlineKeyboardButton(text=t(lang, "btn_autodel", v=autodel), callback_data="open:autodel")
    )
    for field, key in PROFILE_FIELDS_TAIL:
        kb.row(
            InlineKeyboardButton(text=t(lang, key, v=flag(user[field])), callback_data=f"t:{field}")
        )
    return kb.as_markup()


def tag_kb(user: dict[str, Any], is_staff: bool = False) -> InlineKeyboardMarkup:
    """Пометка ником аккаунта, ссылка на профиль, цвет кнопки и кастомный текст."""
    lang = user["lang"]
    kb = InlineKeyboardBuilder()
    
    kb.row(
        InlineKeyboardButton(
            text=t(lang, "btn_mark", v=yesno(user["tag"])), 
            callback_data="t:tag"
        )
    )
    kb.row(
        InlineKeyboardButton(
            text=t(lang, "btn_link", v=yesno(user["tag_link"])), 
            callback_data="t:tag_link"
        )
    )
    
    current_color = user.get("tag_color") or "default"
    color_labels = {
        "default": "Стандартный (прозрачный)",
        "primary": "primary (blue)",
        "success": "success (green)",
        "danger": "danger (red)"
    }
    color_text = color_labels.get(current_color, "default")
    btn_style = current_color if current_color in ("primary", "success", "danger") else None
    
    kb.row(
        InlineKeyboardButton(
            text=f"Цвет кнопки: {color_text}", 
            callback_data="open:tag_colors",
            style=btn_style
        )
    )
    kb.row(
        InlineKeyboardButton(
            text=t(lang, "btn_custom", v=user["custom_name"] or NO), 
            callback_data="open:name"
        )
    )
    
    if is_staff:
        kb.row(
            InlineKeyboardButton(
                text=t(lang, "btn_badge", v=yesno(user["badge"])), 
                callback_data="t:badge"
            )
        )
    return kb.as_markup()


def tag_colors_kb(current_color: str) -> InlineKeyboardMarkup:
    """Меню выбора цвета кнопки для тега (без кнопки Назад)."""
    kb = InlineKeyboardBuilder()
    
    colors = [
        ("danger", "danger (red)", "danger"),
        ("success", "success (green)", "success"),
        ("primary", "primary (blue)", "primary"),
        ("default", "default (transparent)", None)
    ]
    
    for code, label, style in colors:
        text = f">> {label}" if current_color == code else label
        kb.row(
            InlineKeyboardButton(text=text, callback_data=f"set_color:{code}", style=style)
        )
        
    return kb.as_markup()


# --------------------------------------------------------------------------- #
#                          кнопки под эхо-сообщением                           #
# --------------------------------------------------------------------------- #

def echo_kb(
    author: dict[str, Any],
    display_name: str,
    username: Optional[str],
    is_owner: bool = False,
    is_admin: bool = False,
    prefix: Optional[str] = None,
    with_delete: Optional[str] = None,
) -> Optional[InlineKeyboardMarkup]:
    rows: list[list[InlineKeyboardButton]] = []

    if author["tag"]:
        label = author["custom_name"] or display_name
        if not label:
            return None
        
        color = author.get("tag_color") or "default"
        btn_style = color if color in ("primary", "success", "danger") else None
        custom_id = author.get("custom_emoji_id")
        
        link = author.get("tag_url") or (
            f"https://t.me/{username}" if author["tag_link"] and username else None
        )
        if link:
            rows.append([InlineKeyboardButton(text=label, url=link, style=btn_style, icon_custom_emoji_id=custom_id)])
        else:
            rows.append([InlineKeyboardButton(text=label, callback_data="noop", style=btn_style, icon_custom_emoji_id=custom_id)])

        if (is_owner or is_admin) and author["badge"] and db.get_bool("staff_badge"):
            if is_owner:
                rows.append(
                    [InlineKeyboardButton(text=db.get("owner_prefix"), callback_data="noop")]
                )
            else:
                rows.append(
                    [
                        InlineKeyboardButton(
                            text=prefix or db.get("admin_prefix"),
                            url=db.get("admin_badge_url"),
                        )
                    ]
                )

    if with_delete:
        rows.append(
            [
                InlineKeyboardButton(
                    text="Удалить моё сообщение", callback_data=f"d:{with_delete}"
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=rows) if rows else None


# --------------------------------------------------------------------------- #
#                        управление своим сообщением                           #
# --------------------------------------------------------------------------- #

def deleted_kb() -> InlineKeyboardMarkup:
    """Две кнопки под удалённым сообщением: #SYSTEM со ссылкой и DELETED без."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="#SYSTEM",
                    url=db.get("admin_badge_url") or "https://t.me/alltoechobot",
                )
            ],
            [InlineKeyboardButton(text="DELETED", callback_data="noop")],
        ]
    )


def sent_kb(token: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Удалить моё сообщение", callback_data=f"d:{token}")]
        ]
    )


def delete_confirm_kb(token: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да, удалить", callback_data=f"dy:{token}"),
                InlineKeyboardButton(text="Отмена", callback_data=f"dn:{token}"),
            ]
        ]
    )


def edit_confirm_kb(token: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подтвердить", callback_data=f"ey:{token}")]
        ]
    )


# --------------------------------------------------------------------------- #
#                                  прочее                                      #
# --------------------------------------------------------------------------- #

def autodel_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for label, seconds in AUTODEL_PRESETS:
        kb.row(InlineKeyboardButton(text=label, callback_data=f"ad:{seconds}"))
    kb.row(InlineKeyboardButton(text=">> Отключить", callback_data="ad:0"))
    return kb.as_markup()


def lang_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for code, name in LANGS.items():
        kb.row(InlineKeyboardButton(text=name, callback_data=f"lang:{code}"))
    return kb.as_markup()


def close_kb(label: str = "Закрыть") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=label, callback_data="close")]]
    )


def confirm_start_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подтвердить мою регистрацию", callback_data="reg:ok")]
        ]
    )


def pm_kb(peer_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t("ru", "btn_pm_block"), callback_data=f"pmb:{peer_id}")]
        ]
    )


def pm_clear_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Очистить игнор ЛС", callback_data="pmclear")]
        ]
    )


def vote_kb(vote_id: int, yes: int = 0, no: int = 0) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"За ({yes})", callback_data=f"vote:{vote_id}:1"),
                InlineKeyboardButton(text=f"Против ({no})", callback_data=f"vote:{vote_id}:0"),
            ]
        ]
    )


# --------------------------------------------------------------------------- #
#                                /sett панель                                  #
# --------------------------------------------------------------------------- #

PRESETS = {
    "send_delay": [0, 1, 2, 5],
    "slowmode": [0, 3, 5, 8, 15, 30],
    "parallel_limit": [10, 30, 50, 80, 120],
    "stub_hours": [6, 12, 24, 30, 72],
    "autoafk_days": [1, 3, 7, 14, 30],
    "report_cooldown": [60, 180, 300, 600],
    "vote_minutes": [1, 3, 5, 10],
    "warn_limit": [2, 3, 5],
    "warn_base_mute": [3600, 10800, 21600, 86400],
    "warn_multiplier": [2, 3, 4],
}

ECHO_TYPES = [
    ("echo_text", "Text"),
    ("echo_doc", "Doc"),
    ("echo_voice", "Voice"),
    ("echo_sticker", "Sticker"),
    ("echo_video", "Video"),
    ("echo_photo", "Photo"),
    ("echo_poll", "Poll"),
]


def sett_root_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Типы сообщений", callback_data="s:echo"))
    kb.row(InlineKeyboardButton(text="Скорость и лимиты", callback_data="s:speed"))
    kb.row(InlineKeyboardButton(text="Кнопки и префиксы", callback_data="s:buttons"))
    kb.row(InlineKeyboardButton(text="Команды", callback_data="s:cmds"))
    kb.row(InlineKeyboardButton(text="Админы", callback_data="s:admins"))
    kb.row(InlineKeyboardButton(text="Прочее", callback_data="s:misc"))
    kb.row(InlineKeyboardButton(text="Закрыть", callback_data="close"))
    return kb.as_markup()


def sett_echo_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for key, label in ECHO_TYPES:
        kb.row(
            InlineKeyboardButton(
                text=f"{label}: {flag(db.get_bool(key))}", callback_data=f"s:techo:{key}"
            )
        )
    kb.row(InlineKeyboardButton(text="« Назад", callback_data="s:root"))
    return kb.as_markup()


def _value_rows(kb: InlineKeyboardBuilder, labels: dict[str, str]) -> None:
    for key, label in labels.items():
        kb.row(InlineKeyboardButton(text=f"{label}: {db.get(key)}", callback_data="noop"))
        kb.row(
            *[
                InlineKeyboardButton(text=str(v), callback_data=f"s:set:{key}:{v}")
                for v in PRESETS[key]
            ]
        )


def sett_speed_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    _value_rows(
        kb,
        {
            "send_delay": "Задержка отправки",
            "slowmode": "КД между сообщениями, сек",
            "parallel_limit": "Параллельно",
        },
    )
    kb.row(
        InlineKeyboardButton(
            text=f"КД действует на админов: {flag(db.get_bool('slowmode_staff'))}",
            callback_data="s:tset:slowmode_staff",
        )
    )
    kb.row(
        InlineKeyboardButton(
            text=f"КД действует на овнера: {flag(db.get_bool('slowmode_owner'))}",
            callback_data="s:tset:slowmode_owner",
        )
    )
    kb.row(InlineKeyboardButton(text="« Назад", callback_data="s:root"))
    return kb.as_markup()


def sett_misc_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    _value_rows(
        kb,
        {
            "stub_hours": "Пустышки, ч",
            "autoafk_days": "Авто-AFK, дней",
            "report_cooldown": "КД репорта, сек",
            "vote_minutes": "Голосование, мин",
            "warn_limit": "Варнов до мута",
            "warn_base_mute": "Базовый мут, сек",
            "warn_multiplier": "Множитель мута",
        },
    )
    kb.row(
        InlineKeyboardButton(
            text=f"Запрет дублей: {flag(db.get_bool('no_duplicates'))}",
            callback_data="s:tset:no_duplicates",
        )
    )
    kb.row(
        InlineKeyboardButton(
            text="Текст правил: " + ("свой" if db.get("rules_text") else "по умолчанию"),
            callback_data="s:ask:rules_text",
        )
    )
    kb.row(
        InlineKeyboardButton(
            text=f"Регистрация закрыта: {flag(db.get_bool('reg_blocked'))}",
            callback_data="s:tset:reg_blocked",
        )
    )
    kb.row(
        InlineKeyboardButton(
            text=f"Игнор включён: {flag(db.get_bool('ignore_enabled'))}",
            callback_data="s:tset:ignore_enabled",
        )
    )
    kb.row(
        InlineKeyboardButton(
            text=f"Фильтры включены: {flag(db.get_bool('filters_enabled'))}",
            callback_data="s:tset:filters_enabled",
        )
    )
    kb.row(
        InlineKeyboardButton(
            text=f"Ломать чужие #ТЕГИ: {flag(db.get_bool('mangle_system_tags'))}",
            callback_data="s:tset:mangle_system_tags",
        )
    )
    kb.row(
        InlineKeyboardButton(
            text=f"Спецсимволы в сообщениях: {flag(db.get_bool('specials_enabled'))}",
            callback_data="s:tset:specials_enabled",
        )
    )
    kb.row(InlineKeyboardButton(text="« Назад", callback_data="s:root"))
    return kb.as_markup()


def sett_buttons_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text=f"Второй тег админам и овнеру: {flag(db.get_bool('staff_badge'))}",
            callback_data="s:tset:staff_badge",
        )
    )
    kb.row(
        InlineKeyboardButton(
            text=f"Ссылка на админ теге: {db.get('admin_badge_url')}",
            callback_data="s:ask:admin_badge_url",
        )
    )
    kb.row(
        InlineKeyboardButton(
            text=f"Тег овнера: {db.get('owner_prefix')}",
            callback_data="s:ask:owner_prefix",
        )
    )
    kb.row(InlineKeyboardButton(text="« Назад", callback_data="s:root"))
    return kb.as_markup()


def sett_cmds_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    row: list[InlineKeyboardButton] = []
    for name in config.TOGGLEABLE_COMMANDS:
        mark = "✅" if db.command_enabled(name) else "✖️"
        row.append(InlineKeyboardButton(text=f"{mark} /{name}", callback_data=f"s:tcmd:{name}"))
        if len(row) == 2:
            kb.row(*row)
            row = []
    if row:
        kb.row(*row)
    kb.row(InlineKeyboardButton(text="« Назад", callback_data="s:root"))
    return kb.as_markup()


def sett_admins_kb(staff: list[dict[str, Any]]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for member in staff:
        mark = "👑" if member["role"] == "owner" else "🛡"
        kb.row(
            InlineKeyboardButton(
                text=f"{mark} {member['id']}",
                callback_data=f"s:adm:{member['id']}",
            )
        )
    kb.row(InlineKeyboardButton(text="« Назад", callback_data="s:root"))
    return kb.as_markup()


def sett_admin_kb(
    user_id: int, rights: dict[str, int], is_owner: bool = False,
    prefix: Optional[str] = None,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text=f"Префикс: {prefix or '—'}", callback_data=f"s:askp:{user_id}"
        )
    )
    if is_owner:
        kb.row(
            InlineKeyboardButton(
                text="У овнера все права без лимитов", callback_data="noop"
            )
        )
    else:
        for right in config.RIGHTS:
            if right in rights:
                label = f"✅ {right} — лимит {rights[right] or '∞'}"
            else:
                label = f"✖️ {right}"
            kb.row(InlineKeyboardButton(text=label, callback_data=f"s:rt:{user_id}:{right}"))
        kb.row(
            InlineKeyboardButton(text="Снять админку", callback_data=f"s:unadm:{user_id}")
        )
    kb.row(InlineKeyboardButton(text="« Назад", callback_data="s:admins"))
    return kb.as_markup()