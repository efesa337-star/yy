"""Точка входа: middleware, фоновые задачи, поллинг."""

from __future__ import annotations

import asyncio
import html
import logging
import time
import traceback
from typing import Any, Awaitable, Callable, Optional

from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, ErrorEvent, Message, TelegramObject, Update

import config
import h_mod
import keyboards
import h_owner
import h_user
import logs
import moderation
import timeutil
from db import db
from texts import t

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
log = logging.getLogger("echobot")

_GREETED: dict[int, float] = {}


class ContextMiddleware(BaseMiddleware):
    """Подтягивает пользователя из БД и проверяет, включена ли команда."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        tg_user = data.get("event_from_user")
        if tg_user is None or tg_user.is_bot:
            return None

        user = await db.ensure_user(tg_user.id)
        if tg_user.id == config.OWNER_ID and user["role"] != "owner":
            await db.update(tg_user.id, role="owner")
            user["role"] = "owner"

        message: Optional[Message] = event.message if isinstance(event, Update) else None
        callback = event.callback_query if isinstance(event, Update) else None

        if not user["registered"]:
            if db.get_bool("reg_blocked") and user["id"] != config.OWNER_ID:
                if callback is not None:
                    await callback.answer(t(user["lang"], "reg_closed"), show_alert=True)
                    return None
                if message is not None:
                    now = time.time()
                    if now - _GREETED.get(tg_user.id, 0) > 300:
                        _GREETED[tg_user.id] = now
                        await message.answer(t(user["lang"], "reg_closed"))
                return None

            if callback is not None and callback.data == "reg:ok":
                data["user"] = user
                return await handler(event, data)
            if message is None:
                return None
            if callback is not None:
                return None
            text = (message.text or "").strip()
            if not text.startswith("/start"):
                now = time.time()
                if now - _GREETED.get(tg_user.id, 0) > 300:
                    _GREETED[tg_user.id] = now
                    await message.answer(
                        t(user["lang"], "greet",
                          name=html.escape(message.from_user.full_name)),
                        reply_markup=keyboards.confirm_start_kb(),
                    )
                return None

        if message is not None and message.text and message.text.startswith("/"):
            name = message.text[1:].split()[0].split("@")[0].lower()
            if (
                name in config.TOGGLEABLE_COMMANDS
                and not db.command_enabled(name)
                and not moderation.is_owner(user)
            ):
                await message.answer(t(user["lang"], "cmd_disabled"))
                return None

        data["user"] = user
        return await handler(event, data)


async def on_error(event: ErrorEvent) -> None:
    """Ни одна ошибка не должна теряться молча."""
    tb = "".join(
        traceback.format_exception(
            type(event.exception), event.exception, event.exception.__traceback__
        )
    )
    log.error("необработанная ошибка:\n%s", tb)
    await logs.event("ERROR", f"<pre>{html.escape(tb[-3000:])}</pre>")

    update = event.update
    message = getattr(update, "message", None) or getattr(update, "edited_message", None)
    if message is not None:
        try:
            await message.answer(
                "Сообщение не отправлено: внутренняя ошибка. Лог ушёл овнеру."
            )
        except Exception:  # noqa: BLE001
            pass


async def watcher(bot: Bot) -> None:
    """Истёкшие муты, голосования, пустышки, авто-AFK — раз в минуту."""
    while True:
        try:
            for person in await db.expired_mutes():
                await db.update(person["id"], mute_until=0, mute_reason=None)
                await moderation.system_notify(
                    bot, person["id"], t(person["lang"], "mute_expired")
                )

            for record in await db.due_deletions():
                await moderation.delete_message(bot, record["ref"])
                await db.mark_message(record["ref"], delete_at=0)

            for vote in await db.pending_votes():
                await moderation.resolve_vote(bot, vote)

            stale = await db.stale_messages(
                int(time.time()) - db.get_int("stub_hours") * 3600
            )
            for record in stale:
                await db.mark_message(record["ref"], stub=1)
            if stale:
                log.info("помечено пустышками: %s", len(stale))

            days = db.get_int("autoafk_days")
            if days:
                for person in await db.silent_users(int(time.time()) - days * 86400):
                    await db.update(person["id"], afk=1, afk_auto=1)
                    await moderation.system_notify(
                        bot, person["id"],
                        t(
                            person["lang"], "afk_auto",
                            period=timeutil.human_delta(days * 86400),
                            last=timeutil.fmt_dt(person["last_msg_at"]),
                        ),
                    )
        except Exception as exc:  # noqa: BLE001
            log.exception("watcher: %s", exc)
        await asyncio.sleep(60)


async def set_commands(bot: Bot) -> None:
    """Меню бота — порядок и подписи один в один как в боте-образце."""
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="start bot"),
            BotCommand(command="help", description="help commands"),
            BotCommand(command="lang", description="Изменить язык бота"),
            BotCommand(command="rules", description="Правила бота"),
            BotCommand(command="privacy", description="Privacy"),
            BotCommand(command="tag", description="Твой тег под сообщениями"),
            BotCommand(command="leave", description="Покинуть бота"),
            BotCommand(command="profile", description="Инфо о тебе"),
            BotCommand(command="protect", description="Запретить сохранять твое сообщение"),
            BotCommand(command="autodel", description="Включить автоудаление след. сообщ."),
            BotCommand(command="afk", description="Не получать сообщ. Архив"),
            BotCommand(command="unafk", description="Получать сообщения"),
            BotCommand(command="pm", description="Личное сообщ. человеку"),
            BotCommand(command="config", description="Как поживает бот"),
            BotCommand(command="report", description="Жалоба на сообщение"),
            BotCommand(command="reaction", description="Не ставить для вас реакции"),
            BotCommand(command="ignore", description="Отключить сообщения от человека"),
            BotCommand(command="unignore", description="Включить сообщения от человека"),
            BotCommand(command="ignorelist", description="Сколько пользователей в игнор листе"),
            BotCommand(command="filter", description="Скрыть сообщения включающие слово"),
            BotCommand(command="unfilter", description="Убрать фильтр"),
            BotCommand(command="filterlist", description="Лист фильтра"),
            BotCommand(command="emoji", description="Премиум эмодзи в вашем теге"),
        ]
    )


async def main() -> None:
    if not config.BOT_TOKEN:
        raise SystemExit("BOT_TOKEN не задан — заполни .env")
    if not config.OWNER_ID:
        raise SystemExit("OWNER_ID не задан — без овнера панель работать не будет")

    await db.connect()
    if not db.get("started_at"):
        await db.set("started_at", int(time.time()))

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    logs.setup(bot)

    dp = Dispatcher()
    dp.update.outer_middleware(ContextMiddleware())
    dp.include_router(h_owner.router)
    dp.include_router(h_mod.router)
    dp.include_router(h_user.router)
    (getattr(dp, "errors", None) or dp.error).register(on_error)

    await set_commands(bot)
    asyncio.create_task(watcher(bot))
    await logs.event("BOOT", f"Бот запущен, версия {config.VERSION}")
    log.info("Бот запущен")

    try:
        await dp.start_polling(
            bot,
            allowed_updates=[
                "message",
                "edited_message",
                "callback_query",
                "message_reaction",
            ],
        )
    finally:
        await logs.event("STOP", "Бот остановлен")
        await db.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.info("Остановлено")