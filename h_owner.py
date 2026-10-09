"""Овнер: панель /sett, админы и префиксы, /who, /restart, системные рассылки."""

from __future__ import annotations

import asyncio
import html
import os
import secrets
import sys
from typing import Any, Optional

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import BaseFilter, Command, CommandObject
from aiogram.types import CallbackQuery, Message, ReplyParameters

import config
import crypto
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


PENDING_INPUT: dict[int, tuple[str, str]] = {}


class AwaitingInput(BaseFilter):
    """Ловит ответ овнера на запрос значения из панели."""

    async def __call__(self, message: Message) -> bool:
        if message.from_user.id not in PENDING_INPUT:
            return False
        if not message.text or message.text.startswith("/"):
            PENDING_INPUT.pop(message.from_user.id, None)
            return False
        return True


def owner_only(user: dict[str, Any]) -> bool:
    return moderation.is_owner(user)


async def free_badge() -> str:
    """Случайная цифра 1-9 под админ тег, по возможности незанятая."""
    used = {m["prefix"] for m in await db.staff() if m["prefix"]}
    free = [d for d in "123456789" if d not in used]
    return secrets.choice(free or list("123456789"))


async def target_from(message: Message, args: str) -> Optional[dict[str, Any]]:
    """Сначала реплай на сообщение, ID — запасной вариант."""
    if message.reply_to_message:
        record = await db.find_message(
            message.chat.id, message.reply_to_message.message_id
        )
        if record:
            return await db.get_user(record["author_id"])
        peer = await db.get_pm(message.chat.id, message.reply_to_message.message_id)
        if peer:
            return await db.get_user(peer)
        return None
    if args.strip():
        return await db.resolve(args.strip())
    return None


# --------------------------------------------------------------------------- #
#                                   /sett                                      #
# --------------------------------------------------------------------------- #

@router.message(Command("sett"))
async def cmd_sett(message: Message, user: dict[str, Any]):
    if not owner_only(user):
        await answer(message, t(user["lang"], "no_rights"))
        return
    await answer(message, 
        t(user["lang"], "sett_head", version=config.VERSION),
        reply_markup=keyboards.sett_root_kb(),
    )


@router.callback_query(F.data.startswith("s:"))
async def cb_sett(call: CallbackQuery, user: dict[str, Any]):
    if not owner_only(user):
        await call.answer(t(user["lang"], "sett_owner_only"), show_alert=True)
        return

    parts = call.data.split(":")
    section = parts[1]
    lang = user["lang"]

    async def render(text: str, markup) -> None:
        try:
            await call.message.edit_text(text, reply_markup=markup)
        except TelegramBadRequest:
            try:
                await call.message.edit_reply_markup(reply_markup=markup)
            except TelegramBadRequest:
                pass

    if section == "root":
        await render(t(lang, "sett_head", version=config.VERSION), keyboards.sett_root_kb())
    elif section == "echo":
        await render(t(lang, "sett_echo"), keyboards.sett_echo_kb())
    elif section == "speed":
        await render(t(lang, "sett_speed"), keyboards.sett_speed_kb())
    elif section == "misc":
        await render(t(lang, "sett_misc"), keyboards.sett_misc_kb())
    elif section == "buttons":
        await render(t(lang, "sett_buttons"), keyboards.sett_buttons_kb())
    elif section == "cmds":
        await render(t(lang, "sett_cmds"), keyboards.sett_cmds_kb())
    elif section == "admins":
        await render(t(lang, "sett_admins"), keyboards.sett_admins_kb(await db.staff()))

    elif section == "techo":
        key = parts[2]
        await db.set(key, 0 if db.get_bool(key) else 1)
        await render(t(lang, "sett_echo"), keyboards.sett_echo_kb())

    elif section == "tset":
        key = parts[2]
        new = 0 if db.get_bool(key) else 1
        await db.set(key, new)
        if key == "ignore_enabled" and not new:
            wiped = await db.ignore_wipe_all()
            await logs.event("SETT", f"игнор выключен, стёрто записей: {wiped}")
        await logs.event("SETT", f"{key} = {db.get(key)}")
        if key == "staff_badge":
            await render(t(lang, "sett_buttons"), keyboards.sett_buttons_kb())
        elif key.startswith("slowmode"):
            await render(t(lang, "sett_speed"), keyboards.sett_speed_kb())
        else:
            await render(t(lang, "sett_misc"), keyboards.sett_misc_kb())

    elif section == "tcmd":
        name = parts[2]
        state = await db.toggle_command(name)
        await logs.event("SETT", f"/{name} -> {'вкл' if state else 'выкл'}")
        await render(t(lang, "sett_cmds"), keyboards.sett_cmds_kb())

    elif section == "set":
        key, value = parts[2], parts[3]
        await db.set(key, value)
        await logs.event("SETT", f"{key} = {value}")
        speed = key in {"send_delay", "slowmode", "parallel_limit"}
        await render(
            t(lang, "sett_speed" if speed else "sett_misc"),
            keyboards.sett_speed_kb() if speed else keyboards.sett_misc_kb(),
        )

    elif section == "ask":
        PENDING_INPUT[user["id"]] = ("setting", parts[2])
        await call.message.answer(t(lang, "ask_value", key=parts[2]))
        await call.answer()
        return

    elif section == "askp":
        target_id = int(parts[2])
        target = await db.get_user(target_id)
        PENDING_INPUT[user["id"]] = ("prefix", str(target_id))
        await call.message.answer(
            t(lang, "ask_prefix", target=str(target["id"]) if target else target_id)
        )
        await call.answer()
        return

    elif section == "adm":
        target_id = int(parts[2])
        target = await db.get_user(target_id)
        await render(
            f"Пользователь <code>{target_id}</code>\n"
            f"Префикс: {moderation.prefix_of(target) if target else '—'}",
            keyboards.sett_admin_kb(
                target_id,
                await db.rights_of(target_id),
                is_owner=bool(target and moderation.is_owner(target)),
                prefix=moderation.prefix_of(target) if target else None,
            ),
        )

    elif section == "rt":
        target_id, right = int(parts[2]), parts[3]
        rights = await db.rights_of(target_id)
        if right not in rights:
            await db.set_right(target_id, right, config.DEFAULT_LIMITS.get(right, 10))
        elif rights[right] > 0:
            await db.set_right(target_id, right, 0)
        else:
            await db.drop_right(target_id, right)
        target = await db.get_user(target_id)
        await render(
            f"Права <code>{target_id}</code>",
            keyboards.sett_admin_kb(
                target_id,
                await db.rights_of(target_id),
                prefix=moderation.prefix_of(target) if target else None,
            ),
        )

    elif section == "unadm":
        target_id = int(parts[2])
        await db.update(target_id, role="user", prefix=None)
        await db.drop_all_rights(target_id)
        await logs.event("ADMIN", f"снята админка с <code>{target_id}</code>")
        await render(t(lang, "sett_admins"), keyboards.sett_admins_kb(await db.staff()))

    await call.answer()


@router.message(AwaitingInput())
async def on_panel_input(message: Message, user: dict[str, Any]):
    kind, key = PENDING_INPUT.pop(user["id"], ("", ""))
    if not owner_only(user) or not kind:
        return
    value = message.text.strip()
    reset = value in {"-", "—", "reset", "сброс"}

    if kind == "setting":
        await db.set(key, "" if reset else value)
        await logs.event("SETT", f"{key} = {html.escape('' if reset else value)}")
        await answer(message, 
            t(user["lang"], "value_reset", key=key) if reset
            else t(user["lang"], "value_saved", key=key, value=html.escape(value))
        )
        return

    target = await db.get_user(int(key))
    if not target:
        await answer(message, t(user["lang"], "target_not_found"))
        return
    await db.update(target["id"], prefix=None if reset else value)
    fresh = await db.get_user(target["id"])
    await logs.event("ADMIN", f"префикс {logs.who(target)} = {moderation.prefix_of(fresh)}")
    await answer(message, 
        t(
            user["lang"], "prefix_set",
            target=str(target["id"]), value=html.escape(moderation.prefix_of(fresh) or "—"),
        )
    )


# --------------------------------------------------------------------------- #
#                             ручная правка настроек                           #
# --------------------------------------------------------------------------- #

@router.message(Command("set"))
async def cmd_set(message: Message, user: dict[str, Any], command: CommandObject):
    if not owner_only(user):
        await answer(message, t(user["lang"], "no_rights"))
        return
    args = (command.args or "").split(maxsplit=1)
    if len(args) < 2:
        listing = "\n".join(f"{k} = {v}" for k, v in sorted(db.all_settings().items()))
        await answer(message, 
            t(user["lang"], "set_usage") + f"\n\n<code>{html.escape(listing)}</code>"
        )
        return
    key, value = args[0], args[1].strip()
    await db.set(key, value)
    await logs.event("SETT", f"{key} = {html.escape(value)}")
    await answer(message, t(user["lang"], "set_done", key=key, value=html.escape(value)))


# --------------------------------------------------------------------------- #
#                                   админы                                     #
# --------------------------------------------------------------------------- #

@router.message(Command("promote"))
async def cmd_promote(message: Message, user: dict[str, Any], command: CommandObject):
    if not owner_only(user):
        await answer(message, t(user["lang"], "no_rights"))
        return
    target = await target_from(message, command.args or "")
    if not target:
        await answer(message, t(user["lang"], "admin_usage"))
        return

    badge = await free_badge()
    await db.update(target["id"], role="admin", prefix=badge, badge=1)
    for right, limit in config.DEFAULT_LIMITS.items():
        if limit:
            await db.set_right(target["id"], right, limit)
    await logs.event("ADMIN", f"назначен админ {logs.who(target)}, админ тег {badge}")
    await answer(message, 
        t(user["lang"], "admin_added", target=str(target["id"]), badge=badge)
    )


@router.message(Command("demote"))
async def cmd_demote(message: Message, user: dict[str, Any], command: CommandObject):
    if not owner_only(user):
        await answer(message, t(user["lang"], "no_rights"))
        return
    target = await target_from(message, command.args or "")
    if not target:
        await answer(message, t(user["lang"], "target_not_found"))
        return
    await db.update(target["id"], role="user", prefix=None)
    await db.drop_all_rights(target["id"])
    await logs.event("ADMIN", f"снята админка {logs.who(target)}")
    await answer(message, t(user["lang"], "admin_removed", target=str(target["id"])))


@router.message(Command("prefix"))
async def cmd_prefix(message: Message, user: dict[str, Any], command: CommandObject):
    """Кастомный префикс себе или админу. Пусто — сброс на дефолтный."""
    if not owner_only(user):
        await answer(message, t(user["lang"], "no_rights"))
        return
    args = (command.args or "").split(maxsplit=1)

    if message.reply_to_message:
        target = await target_from(message, "")
        value = (command.args or "").strip()
    elif len(args) >= 1 and (await db.resolve(args[0])):
        target = await db.resolve(args[0])
        value = args[1].strip() if len(args) > 1 else ""
    else:
        target, value = user, (command.args or "").strip()

    if not target:
        await answer(message, t(user["lang"], "prefix_usage"))
        return
    await db.update(target["id"], prefix=value or None)
    await answer(message, 
        t(
            user["lang"], "prefix_set",
            target=str(target["id"]),
            value=html.escape(value) or moderation.prefix_of(await db.get_user(target["id"])),
        )
    )


@router.message(Command("mytag"))
async def cmd_mytag(message: Message, user: dict[str, Any], command: CommandObject):
    """
    /mytag <текст>          — поставить кастомный тег
    /mytag <текст> link     — с ссылкой на твой профиль
    /mytag <текст> nolink   — без ссылки
    /mytag off              — сбросить
    """
    if not owner_only(user):
        await answer(message, t(user["lang"], "no_rights"))
        return

    raw = (command.args or "").strip()
    if not raw:
        await answer(message, t(user["lang"], "mytag_usage"))
        return

    if raw.lower() in {"off", "-", "сброс"}:
        await db.update(user["id"], custom_name=None)
        await answer(message, t(user["lang"], "mytag_off"))
        return

    link: Optional[int] = None
    parts = raw.split()
    if parts[-1].lower() in {"link", "ссылка", "+link"}:
        link, parts = 1, parts[:-1]
    elif parts[-1].lower() in {"nolink", "безссылки", "-link"}:
        link, parts = 0, parts[:-1]

    text = " ".join(parts).strip()
    limit = db.get_int("name_max") or 17
    if not text or len(text) > limit:
        await answer(message, t(user["lang"], "name_bad", max=limit))
        return

    fields: dict[str, Any] = {"custom_name": text, "tag": 1}
    if link is not None:
        fields["tag_link"] = link
    await db.update(user["id"], **fields)

    fresh = await db.get_user(user["id"])
    await answer(message, 
        t(
            user["lang"], "mytag_set",
            text=html.escape(text),
            link="да" if fresh["tag_link"] else "нет",
        )
    )


# --------------------------------------------------------------------------- #
#                             кто это пишет                                    #
# --------------------------------------------------------------------------- #

@router.message(Command("settag"))
async def cmd_settag(message: Message, user: dict[str, Any], command: CommandObject):
    """/settag <текст> | <ссылка> — свой кастомный тег с любой ссылкой."""
    if not owner_only(user):
        await answer(message, t(user["lang"], "no_rights"))
        return

    raw = (command.args or "").strip()
    if not raw:
        await db.update(user["id"], custom_name=None, tag_url=None)
        await answer(message, 
            t(user["lang"], "settag_off") + "\n\n" + t(user["lang"], "settag_usage")
        )
        return

    text, _, url = raw.partition("|")
    text, url = text.strip(), url.strip()
    limit = db.get_int("name_max") or 17
    if not text or len(text) > limit:
        await answer(message, t(user["lang"], "name_bad", max=limit))
        return
    if url and not url.startswith(("http://", "https://", "tg://")):
        url = "https://" + url

    await db.update(user["id"], custom_name=text, tag_url=url or None, tag=1)
    await answer(message, 
        t(
            user["lang"], "settag_set",
            text=html.escape(text), url=html.escape(url) if url else "нет",
        )
    )


@router.message(Command("who", "whois"))
async def cmd_who(message: Message, user: dict[str, Any], command: CommandObject):
    allowed, error = await moderation.check_right(user, "who")
    if not allowed:
        await answer(message, error)
        return
    target = await target_from(message, command.args or "")
    if not target:
        await answer(message, t(user["lang"], "who_usage"))
        return

    username = crypto.decrypt(target["username_enc"])
    name = crypto.decrypt(target["name_enc"]) or "—"
    if username and not username.startswith("id"):
        username = f"@{username}"
    await answer(message, 
        t(
            user["lang"], "who_result",
            id=target["id"],
            username=username or "нет",
            name=html.escape(name),
            role=target["role"],
            joined=timeutil.fmt_dt_long(target["joined_at"]),
            msgs=target["msgs"],
        )
    )
    await moderation.spend(user, "who")
    await logs.event("WHO", f"{logs.who(user)} смотрел {logs.who(target)}")


# --------------------------------------------------------------------------- #
#                       системная рассылка и перезапуск                        #
# --------------------------------------------------------------------------- #

@router.message(Command("system"))
async def cmd_system(message: Message, user: dict[str, Any], command: CommandObject, bot: Bot):
    if not owner_only(user):
        await answer(message, t(user["lang"], "no_rights"))
        return
    text = (command.args or "").strip()
    if not text:
        await answer(message, t(user["lang"], "system_usage"))
        return

    payload = f"{t('ru', 'system_prefix')}\n{text}"
    count = 0
    for person in await db.recipients(exclude=0):
        if await moderation.system_notify(bot, person["id"], payload):
            count += 1
    await answer(message, t(user["lang"], "system_done", count=count))
    await logs.event("SYSTEM", html.escape(text))


@router.message(Command("blockreg"))
async def cmd_blockreg(message: Message, user: dict[str, Any]):
    """Закрывает и открывает вход новым пользователям. Без таймера, до отмены."""
    if not owner_only(user):
        await answer(message, t(user["lang"], "no_rights"))
        return
    new = 0 if db.get_bool("reg_blocked") else 1
    await db.set("reg_blocked", new)
    await answer(message, t(user["lang"], "reg_block_on" if new else "reg_block_off"))
    await logs.event(
        "SETT", f"регистрация {'закрыта' if new else 'открыта'} — {logs.who(user)}"
    )


@router.message(Command("restart"))
async def cmd_restart(message: Message, user: dict[str, Any], bot: Bot):
    if not owner_only(user):
        await answer(message, t(user["lang"], "no_rights"))
        return
    await answer(message, t(user["lang"], "restarting"))
    await logs.event("RESTART", f"Перезапуск по команде {logs.who(user)}")
    await db.close()
    await bot.session.close()
    await asyncio.sleep(0.3)
    os.execv(sys.executable, [sys.executable, *sys.argv])