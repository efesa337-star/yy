"""Логи работы бота в приватный канал овнера. Больше их никто не видит."""

from __future__ import annotations

import html
import logging
import time
from typing import Any, Optional

from aiogram import Bot
from aiogram.types import LinkPreviewOptions

import config
import timeutil

log = logging.getLogger("logs")
_bot: Optional[Bot] = None
NO_PREVIEW = LinkPreviewOptions(is_disabled=True)


def setup(bot: Bot) -> None:
    global _bot
    _bot = bot


def who(user: Optional[dict[str, Any]]) -> str:
    if not user:
        return "—"
    return f"<code>{user['id']}</code>"


def esc(value: Any) -> str:
    return html.escape(str(value))


async def event(tag: str, text: str) -> None:
    """tag: BOOT / START / MUTE / WARN / DEL / REPORT / ADMIN / SETT / WHO / ERROR."""
    log.info("[%s] %s", tag, text.replace("\n", " | "))
    if not (_bot and config.LOG_CHANNEL):
        return
    try:
        await _bot.send_message(
            config.LOG_CHANNEL,
            f"#{tag} {timeutil.fmt_dt_short(time.time())}\n{text}",
            parse_mode="HTML",
            link_preview_options=NO_PREVIEW,
            disable_notification=True,
        )
    except Exception as exc:  # noqa: BLE001
        log.warning("не смог записать лог: %s", exc)