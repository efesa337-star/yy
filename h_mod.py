"""Команды модерации: мут, варн, удаление, голосование."""

from __future__ import annotations

import html
from typing import Any, Optional

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import CallbackQuery, Message, ReplyParameters

import keyboards
import logs
import moderation
import timeutil
from db import db
from texts import t

router = Router()


async def answer(message: Message, text: str, **kwargs):
    """Ответ бота всегда цитирует твоё сообщение, а не улетает в пустоту."""
    kwargs.setdefault(
        "reply_parameters",
        ReplyParameters(message_id=message.message_id, allow_sending_without_reply=True),
    )
    return await message.answer(text, **kwargs)


async def resolve_target(
    message: Message, args: list[str]
) -> tuple[Optional[dict[str, Any]], list[str], Optional[int], bool]:
    """
    Главный способ — ответить на сообщение и написать команду.
    ID остаётся запасным вариантом, когда отвечать не на что.
    Возвращает (юзер, остаток args, ref сообщения, реплай_не_распознан).
    """
    if message.reply_to_message:
        record = await db.find_message(
            message.chat.id, message.reply_to_message.message_id
        )
        if record:
            return await db.get_user(record["author_id"]), args, record["ref"], False
        peer = await db.get_pm(message.chat.id, message.reply_to_message.message_id)
        if peer:
            return await db.get_user(peer), args, None, False
        return None, args, None, True

    if args:
        target = await db.resolve(args[0])
        if target:
            return target, args[1:], None, False
    return None, args, None, False


def protected(actor: dict[str, Any], target: dict[str, Any]) -> bool:
    """Овнера тронуть нельзя; админа может тронуть только овнер."""
    if moderation.is_owner(target):
        return True
    return target["role"] == "admin" and not moderation.is_owner(actor)


@router.message(Command("mute"))
async def cmd_mute(message: Message, user: dict[str, Any], command: CommandObject, bot: Bot):
    allowed, error = await moderation.check_right(user, "mute")
    if not allowed:
        await answer(message, error)
        return

    target, rest, ref, bad_reply = await resolve_target(message, (command.args or "").split())
    if bad_reply:
        await answer(message, t(user["lang"], "reply_unknown"))
        return
    if not target or not rest:
        await answer(message, t(user["lang"], "mute_usage"))
        return
    if protected(user, target):
        await answer(message, t(user["lang"], "no_rights"))
        return

    seconds = timeutil.parse_duration(rest[0])
    if not seconds:
        await answer(message, t(user["lang"], "mute_bad_time"))
        return
    reason = " ".join(rest[1:]).strip() or "—"

    if ref:
        await moderation.delete_message(bot, ref)

    await moderation.apply_mute(bot, target, seconds, reason, user)
    await moderation.spend(user, "mute")
    await answer(message, 
        t(
            user["lang"], "mute_done",
            target=str(target["id"]),
            duration=timeutil.human_delta(seconds, 3),
            reason=html.escape(reason),
        )
    )


@router.message(Command("unmute"))
async def cmd_unmute(message: Message, user: dict[str, Any], command: CommandObject, bot: Bot):
    allowed, error = await moderation.check_right(user, "unmute")
    if not allowed:
        await answer(message, error)
        return
    target, _, _, bad_reply = await resolve_target(message, (command.args or "").split())
    if bad_reply:
        await answer(message, t(user["lang"], "reply_unknown"))
        return
    if not target:
        await answer(message, t(user["lang"], "target_not_found"))
        return
    if not moderation.muted(target):
        await answer(message, t(user["lang"], "not_muted"))
        return
    await moderation.apply_unmute(bot, target)
    await moderation.spend(user, "unmute")
    await answer(message, t(user["lang"], "unmute_done", target=str(target["id"])))


@router.message(Command("warn"))
async def cmd_warn(message: Message, user: dict[str, Any], command: CommandObject, bot: Bot):
    allowed, error = await moderation.check_right(user, "warn")
    if not allowed:
        await answer(message, error)
        return
    target, rest, ref, bad_reply = await resolve_target(message, (command.args or "").split())
    if bad_reply:
        await answer(message, t(user["lang"], "reply_unknown"))
        return
    if not target:
        await answer(message, t(user["lang"], "need_reply"))
        return
    if protected(user, target):
        await answer(message, t(user["lang"], "no_rights"))
        return

    reason = " ".join(rest).strip() or "—"
    if ref:
        await moderation.delete_message(bot, ref)
    warns, mute_seconds = await moderation.apply_warn(bot, target, reason, user)
    await moderation.spend(user, "warn")

    limit = db.get_int("warn_limit") or 3
    text = t(
        user["lang"], "warn_done",
        target=str(target["id"]), n=min(warns, limit), limit=limit,
    )
    if mute_seconds:
        text += f" Мут: {timeutil.human_delta(mute_seconds, 3)}."
    await answer(message, text)


@router.message(Command("unwarn"))
async def cmd_unwarn(message: Message, user: dict[str, Any], command: CommandObject):
    allowed, error = await moderation.check_right(user, "unwarn")
    if not allowed:
        await answer(message, error)
        return
    target, _, _, bad_reply = await resolve_target(message, (command.args or "").split())
    if bad_reply:
        await answer(message, t(user["lang"], "reply_unknown"))
        return
    if not target:
        await answer(message, t(user["lang"], "target_not_found"))
        return
    warns = max(0, target["warns"] - 1)
    await db.update(target["id"], warns=warns)
    await moderation.spend(user, "unwarn")
    await answer(message, 
        t(
            user["lang"], "unwarn_done",
            target=str(target["id"]), n=warns, limit=db.get_int("warn_limit") or 3,
        )
    )


@router.message(Command("del"))
async def cmd_del(message: Message, user: dict[str, Any], command: CommandObject, bot: Bot):
    allowed, error = await moderation.check_right(user, "del")
    if not allowed:
        await answer(message, error)
        return

    args = (command.args or "").split()
    if message.reply_to_message:
        record = await db.find_message(
            message.chat.id, message.reply_to_message.message_id
        )
        if not record:
            await answer(message, t(user["lang"], "reply_unknown"))
            return
        target = await db.get_user(record["author_id"])

        count = int(args[0]) if args and args[0].isdigit() else 1
        if count > 1:
            msgs, copies = await moderation.delete_from(
                bot, record["author_id"], record["ref"], min(count, 50)
            )
            await moderation.spend(user, "del")
            await answer(message, t(user["lang"], "del_done", msgs=msgs, copies=copies))
            await logs.event("DELETE", t("ru", "log_delete", who=logs.who(target), count=copies))
            return

        copies = await moderation.delete_message(bot, record["ref"])
        await moderation.spend(user, "del")
        await moderation.system_notify(bot, record["author_id"], t("ru", "del_notice"))
        await answer(message, t(user["lang"], "del_done", msgs=1, copies=copies))
        await logs.event(
            "DELETE", t("ru", "log_delete", who=logs.who(target), count=copies)
        )
        return

    if len(args) < 2 or not args[1].isdigit():
        await answer(message, t(user["lang"], "del_usage"))
        return
    target = await db.resolve(args[0])
    if not target:
        await answer(message, t(user["lang"], "target_not_found"))
        return

    msgs, copies = await moderation.delete_last(bot, target["id"], min(int(args[1]), 50))
    await moderation.spend(user, "del")
    await answer(message, t(user["lang"], "del_done", msgs=msgs, copies=copies))
    await logs.event("DEL", f"{msgs} сообщений {logs.who(target)} — {logs.who(user)}")


@router.message(Command("votemute"))
async def cmd_votemute(
    message: Message, user: dict[str, Any], command: CommandObject, bot: Bot
):
    allowed, error = await moderation.check_right(user, "votemute")
    if not allowed:
        await answer(message, error)
        return
    target, rest, _, bad_reply = await resolve_target(message, (command.args or "").split())
    if bad_reply:
        await answer(message, t(user["lang"], "reply_unknown"))
        return
    if not target or not rest:
        await answer(message, t(user["lang"], "vote_usage"))
        return
    if protected(user, target):
        await answer(message, t(user["lang"], "no_rights"))
        return
    seconds = timeutil.parse_duration(rest[0])
    if not seconds:
        await answer(message, t(user["lang"], "mute_bad_time"))
        return

    vote_id = await moderation.start_vote(
        bot, user, target, seconds, " ".join(rest[1:]).strip() or "—"
    )
    if vote_id is None:
        await answer(message, t(user["lang"], "vote_no_staff"))
        return
    await moderation.spend(user, "votemute")
    await answer(message, 
        t(user["lang"], "vote_started", minutes=db.get_int("vote_minutes") or 5)
    )


@router.message(Command("media"))
async def cmd_media(message: Message, user: dict[str, Any], command: CommandObject):
    """/media <reply> — запретить или вернуть человеку отправку медиа."""
    allowed, error = await moderation.check_right(user, "media")
    if not allowed:
        await answer(message, error)
        return
    target, _, _, bad_reply = await resolve_target(message, (command.args or "").split())
    if bad_reply:
        await answer(message, t(user["lang"], "reply_unknown"))
        return
    if not target:
        await answer(message, t(user["lang"], "need_reply"))
        return
    if protected(user, target):
        await answer(message, t(user["lang"], "no_rights"))
        return

    value = 0 if target["media_block"] else 1
    await db.update(target["id"], media_block=value)
    await moderation.spend(user, "media")
    await moderation.system_notify(
        bot=message.bot, user_id=target["id"],
        text=t(target["lang"], "media_blocked" if value else "media_unblocked"),
    )
    await answer(message, t(user["lang"], "media_done", target=target["id"],
                            state=t(user["lang"], "media_on" if value else "media_off")))
    await logs.event("MEDIA", f"{logs.who(target)} -> {'запрет' if value else 'снят'}")


@router.message(Command("pin"))
async def cmd_pin(message: Message, user: dict[str, Any], bot: Bot):
    """Закрепляет сообщение у всех получателей."""
    allowed, error = await moderation.check_right(user, "pin")
    if not allowed:
        await answer(message, error)
        return
    if not message.reply_to_message:
        await answer(message, t(user["lang"], "need_reply"))
        return
    record = await db.find_message(message.chat.id, message.reply_to_message.message_id)
    if not record:
        await answer(message, t(user["lang"], "reply_unknown"))
        return

    done = await moderation.bulk(
        bot.pin_chat_message, await db.copies(record["ref"]), disable_notification=True
    )
    await moderation.spend(user, "pin")
    await answer(message, t(user["lang"], "pin_done", count=done))
    await logs.event("PIN", f"закрепил {logs.who(user)}, копий {done}")


@router.message(Command("unpin"))
async def cmd_unpin(message: Message, user: dict[str, Any], bot: Bot):
    """Снимает закрепление у всех."""
    allowed, error = await moderation.check_right(user, "pin")
    if not allowed:
        await answer(message, error)
        return
    if not message.reply_to_message:
        await answer(message, t(user["lang"], "need_reply"))
        return
    record = await db.find_message(message.chat.id, message.reply_to_message.message_id)
    if not record:
        await answer(message, t(user["lang"], "reply_unknown"))
        return

    done = await moderation.bulk(bot.unpin_chat_message, await db.copies(record["ref"]))
    await moderation.spend(user, "pin")
    await answer(message, t(user["lang"], "unpin_done", count=done))


@router.message(Command("rights", "myrights"))
async def cmd_rights(message: Message, user: dict[str, Any]):
    """Показывает только твои собственные права и остаток лимитов."""
    if not moderation.is_staff(user):
        await answer(message, t(user["lang"], "no_rights"))
        return

    if moderation.is_owner(user):
        await answer(message, 
            t(user["lang"], "rights_owner", prefix=moderation.prefix_of(user))
        )
        return

    rights = await db.rights_of(user["id"])
    if not rights:
        await answer(message, t(user["lang"], "rights_none"))
        return
    lines = []
    for right, limit in rights.items():
        used = await db.usage_today(user["id"], right)
        lines.append(f"/{right} — {used}/{limit or '∞'} за сутки")
    await answer(message, 
        t(
            user["lang"], "rights_mine",
            prefix=moderation.prefix_of(user), items="\n".join(lines),
        )
    )


@router.callback_query(F.data.startswith("vote:"))
async def cb_vote(call: CallbackQuery, user: dict[str, Any]):
    _, raw_id, raw_value = call.data.split(":")
    vote = await db.get_vote(int(raw_id))
    if not vote or vote["resolved"]:
        await call.answer(t(user["lang"], "vote_over"), show_alert=True)
        return
    if not moderation.is_staff(user):
        await call.answer(t(user["lang"], "no_rights"), show_alert=True)
        return

    await db.cast_ballot(vote["id"], user["id"], int(raw_value))
    yes, no = await db.ballots(vote["id"])
    try:
        await call.message.edit_reply_markup(
            reply_markup=keyboards.vote_kb(vote["id"], yes, no)
        )
    except Exception:  # noqa: BLE001
        pass
    await call.answer(t(user["lang"], "vote_voted"))