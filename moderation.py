"""Модерация: права и лимиты, префиксы, муты, варны, удаление, голосования."""

from __future__ import annotations

import asyncio
import time
from typing import Any, Optional

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import LinkPreviewOptions, MessageEntity, ReplyParameters

import config
import delivery
import keyboards
import logs
import timeutil
from db import db
from texts import t

NO_PREVIEW = LinkPreviewOptions(is_disabled=True)


# --------------------------------------------------------------------------- #
#                              роли и префиксы                                 #
# --------------------------------------------------------------------------- #

def is_owner(user: dict[str, Any]) -> bool:
    return user["id"] == config.OWNER_ID


def is_staff(user: dict[str, Any]) -> bool:
    return is_owner(user) or user["role"] == "admin"


def prefix_of(user: dict[str, Any]) -> Optional[str]:
    """Кастомный префикс, иначе дефолт из настроек."""
    if user.get("prefix"):
        return user["prefix"]
    if is_owner(user):
        return db.get("owner_prefix")
    if user["role"] == "admin":
        return db.get("admin_prefix")
    return None


async def check_right(user: dict[str, Any], right: str) -> tuple[bool, str]:
    if is_owner(user):
        return True, ""
    if user["role"] != "admin":
        return False, t(user["lang"], "no_rights")
    rights = await db.rights_of(user["id"])
    if right not in rights:
        return False, t(user["lang"], "no_rights")
    limit = rights[right]
    if limit <= 0:
        return True, ""
    used = await db.usage_today(user["id"], right)
    if used >= limit:
        return False, t(user["lang"], "limit_reached", used=used, limit=limit)
    return True, ""


async def spend(user: dict[str, Any], right: str) -> None:
    if not is_owner(user):
        await db.bump_usage(user["id"], right)


async def rights_summary(user: dict[str, Any]) -> str:
    if is_owner(user):
        return "все, без лимитов"
    rights = await db.rights_of(user["id"])
    if not rights:
        return t(user["lang"], "rights_none")
    parts = []
    for right, limit in rights.items():
        used = await db.usage_today(user["id"], right)
        parts.append(f"{right} {used}/{limit or '∞'}")
    return ", ".join(parts)


# --------------------------------------------------------------------------- #
#                             системные сообщения                              #
# --------------------------------------------------------------------------- #

async def system_notify(bot: Bot, user_id: int, text: str) -> bool:
    try:
        await bot.send_message(user_id, text, link_preview_options=NO_PREVIEW)
        return True
    except (TelegramForbiddenError, TelegramBadRequest):
        await db.update(user_id, active=0)
        return False


async def notify_staff(bot: Bot, text: str, markup=None) -> list[tuple[int, int]]:
    sent: list[tuple[int, int]] = []
    for member in await db.staff():
        try:
            message = await bot.send_message(
                member["id"], text, link_preview_options=NO_PREVIEW, reply_markup=markup
            )
            sent.append((member["id"], message.message_id))
        except (TelegramForbiddenError, TelegramBadRequest):
            continue
    return sent


# --------------------------------------------------------------------------- #
#                                     мут                                      #
# --------------------------------------------------------------------------- #

def mute_left(user: dict[str, Any]) -> int:
    return max(0, int(user["mute_until"]) - int(time.time()))


def muted(user: dict[str, Any]) -> bool:
    return mute_left(user) > 0


def mute_message(user: dict[str, Any]) -> str:
    reason = (user["mute_reason"] or "").strip()
    if reason and reason != "—":
        return t(
            user["lang"], "mute_blocked_reason",
            name=user["custom_name"] or "",
            reason=reason,
            left=timeutil.human_delta(mute_left(user), 2),
            until=timeutil.fmt_dt(user["mute_until"]),
        ).strip()
    return t(
        user["lang"], "mute_blocked",
        name=user["custom_name"] or "",
        left=timeutil.human_delta(mute_left(user), 2),
        until=timeutil.fmt_dt(user["mute_until"]),
    ).strip()


async def apply_mute(
    bot: Bot,
    target: dict[str, Any],
    seconds: int,
    reason: str,
    by: Optional[dict[str, Any]] = None,
) -> None:
    await db.update(
        target["id"], mute_until=int(time.time()) + seconds, mute_reason=reason
    )
    clean = (reason or "").strip()
    await system_notify(
        bot, target["id"],
        t(
            target["lang"],
            "mute_notice_reason" if clean and clean != "—" else "mute_notice",
            duration=timeutil.human_delta(seconds, 3), reason=clean,
        ) if clean and clean != "—" else t(
            target["lang"], "mute_notice", duration=timeutil.human_delta(seconds, 3)
        ),
    )
    await logs.event(
        "MUTE",
        f"{logs.who(target)} на {timeutil.human_delta(seconds, 3)}\n"
        f"Причина: {logs.esc(reason)}\nКем: {logs.who(by)}",
    )


async def apply_unmute(bot: Bot, target: dict[str, Any]) -> None:
    await db.update(target["id"], mute_until=0, mute_reason=None)
    await system_notify(bot, target["id"], t(target["lang"], "unmute_notice"))
    await logs.event("UNMUTE", logs.who(target))


# --------------------------------------------------------------------------- #
#                                    варны                                     #
# --------------------------------------------------------------------------- #

async def apply_warn(
    bot: Bot, target: dict[str, Any], reason: str, by: Optional[dict[str, Any]] = None
) -> tuple[int, int]:
    limit = db.get_int("warn_limit") or 3
    warns = target["warns"] + 1
    text = t(target["lang"], "warn_notice", n=min(warns, limit), limit=limit, reason=reason)
    mute_seconds = 0

    if warns >= limit:
        base = db.get_int("warn_base_mute") or 10800
        multiplier = db.get_int("warn_multiplier") or 3
        mute_seconds = int(base * (multiplier ** target["warn_cycles"]))
        await db.update(
            target["id"],
            warns=0,
            warn_cycles=target["warn_cycles"] + 1,
            streak=target["streak"] + 1,
        )
        text += t(
            target["lang"], "warn_automute",
            limit=limit, duration=timeutil.human_delta(mute_seconds, 3),
        )
        await system_notify(bot, target["id"], text)
        fresh = await db.get_user(target["id"])
        await apply_mute(bot, fresh, mute_seconds, reason, by)
    else:
        await db.update(target["id"], warns=warns)
        await system_notify(bot, target["id"], text)

    await logs.event(
        "WARN",
        f"{logs.who(target)} — {warns}/{limit}\nПричина: {logs.esc(reason)}\n"
        f"Кем: {logs.who(by)}",
    )
    return warns, mute_seconds


# --------------------------------------------------------------------------- #
#                                  удаление                                    #
# --------------------------------------------------------------------------- #

async def bulk(method, pairs: list[tuple[int, int]], **kwargs) -> int:
    """Гонит одну и ту же операцию по всем копиям параллельно."""
    done = 0

    async def run(chat_id: int, msg_id: int) -> None:
        nonlocal done
        try:
            await method(chat_id, msg_id, **kwargs)
            done += 1
        except Exception:  # noqa: BLE001
            pass

    await asyncio.gather(*(run(c, m) for c, m in pairs))
    return done


async def delete_message(bot: Bot, ref: int, notify: bool = True) -> int:
    """
    Сносит копии у всех получателей. Эхо-копию автора оставляем на месте и
    вешаем на неё две кнопки: #SYSTEM и DELETED. Оригинал автора не трогаем.
    """
    record = await db.message_by_ref(ref)
    own = (
        (record["author_id"], await db.copy_in_chat(ref, record["author_id"]))
        if record else None
    )
    if own and own[1] is None:
        own = None

    removed = await delivery.propagate_delete(bot, ref, skip=own if notify else None)

    if own and notify:
        try:
            await bot.edit_message_reply_markup(
                chat_id=own[0], message_id=own[1],
                reply_markup=keyboards.deleted_kb(),
            )
        except (TelegramBadRequest, TelegramForbiddenError):
            try:
                await bot.delete_message(own[0], own[1])
            except (TelegramBadRequest, TelegramForbiddenError):
                pass
    return removed


async def delete_last(bot: Bot, target_id: int, count: int) -> tuple[int, int]:
    messages = await db.last_messages(target_id, count)
    copies = 0
    for record in messages:
        copies += await delete_message(bot, record["ref"])
    return len(messages), copies


async def delete_from(
    bot: Bot, target_id: int, from_ref: int, count: int
) -> tuple[int, int]:
    messages = await db.messages_from(target_id, from_ref, count)
    copies = 0
    for record in messages:
        copies += await delete_message(bot, record["ref"])
    return len(messages), copies


# --------------------------------------------------------------------------- #
#                                голосование                                   #
# --------------------------------------------------------------------------- #

async def start_vote(
    bot: Bot, author: dict[str, Any], target: dict[str, Any], seconds: int, reason: str
) -> Optional[int]:
    minutes = db.get_int("vote_minutes") or 5
    vote_id = await db.add_vote(
        target["id"], author["id"], reason, seconds, int(time.time()) + minutes * 60
    )
    text = t(
        author["lang"], "vote_head",
        target=str(target["id"]),
        duration=timeutil.human_delta(seconds, 3),
        reason=reason,
        author=str(author["id"]),
        minutes=minutes,
    )
    sent = await notify_staff(bot, text, keyboards.vote_kb(vote_id))
    if not sent:
        await db.resolve_vote(vote_id)
        return None
    for chat_id, msg_id in sent:
        await db.add_vote_msg(vote_id, chat_id, msg_id)
    await logs.event(
        "VOTE",
        f"Голосование #{vote_id}: мут {logs.who(target)} "
        f"на {timeutil.human_delta(seconds, 3)}, инициатор {logs.who(author)}",
    )
    return vote_id


async def resolve_vote(bot: Bot, vote: dict[str, Any]) -> None:
    yes, no = await db.ballots(vote["id"])
    await db.resolve_vote(vote["id"])
    target = await db.get_user(vote["target_id"])
    passed = yes > no and yes > 0
    text = t("ru", "vote_result_pass" if passed else "vote_result_fail", yes=yes, no=no)

    for chat_id, msg_id in await db.vote_msgs(vote["id"]):
        try:
            await bot.edit_message_reply_markup(chat_id, msg_id, reply_markup=None)
            await bot.send_message(chat_id, text, link_preview_options=NO_PREVIEW)
        except (TelegramBadRequest, TelegramForbiddenError):
            continue

    if passed and target:
        await apply_mute(bot, target, vote["duration"], vote["reason"] or "Votemute")