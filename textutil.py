"""Работа с текстом: entities, спецсимволы, упоминания, хеш для антидубля."""

from __future__ import annotations

import hashlib
import re
import unicodedata
from typing import Optional, Sequence

from aiogram.types import Message, MessageEntity

MENTION_RE = re.compile(r"@([A-Za-z0-9_]{4,32})")

_BOLD_UPPER = 0x1D5D4 - ord("A")
_BOLD_LOWER = 0x1D5EE - ord("a")
_BOLD_DIGIT = 0x1D7EC - ord("0")


# --------------------------------------------------------------------------- #
#                                  entities                                    #
# --------------------------------------------------------------------------- #

def u16len(text: str) -> int:
    """Длина в UTF-16 code units — Telegram считает offset'ы именно так."""
    return len(text.encode("utf-16-le")) // 2


def shift_entities(
    entities: Optional[Sequence[MessageEntity]], shift: int
) -> list[MessageEntity]:
    out: list[MessageEntity] = []
    for entity in entities or []:
        out.append(
            MessageEntity(
                type=entity.type,
                offset=entity.offset + shift,
                length=entity.length,
                url=entity.url,
                user=entity.user,
                language=entity.language,
                custom_emoji_id=entity.custom_emoji_id,
            )
        )
    return out


def compose(
    text: str,
    entities: Optional[Sequence[MessageEntity]],
    prefix: str = "",
    suffix: str = "",
    suffix_entities: Optional[Sequence[MessageEntity]] = None,
) -> tuple[str, list[MessageEntity]]:
    """Склеивает префикс + текст + суффикс, сохраняя всё форматирование."""
    result = prefix + (text or "")
    out = shift_entities(entities, u16len(prefix))
    if suffix:
        out += shift_entities(suffix_entities, u16len(result))
        result += suffix
    return result, out


def source_text(src: Message) -> tuple[str, list[MessageEntity]]:
    if src.text is not None:
        return src.text, list(src.entities or [])
    if src.caption is not None:
        return src.caption, list(src.caption_entities or [])
    return "", []


# --------------------------------------------------------------------------- #
#                           преобразования текста                              #
# --------------------------------------------------------------------------- #

def strip_specials(text: str) -> str:
    """Приводит вычурный юникод к обычным буквам: 𝒶𝓮𝓉𝒽 -> aeth."""
    if not text:
        return text
    normalized = unicodedata.normalize("NFKC", text)
    cleaned = "".join(
        ch for ch in normalized if not unicodedata.combining(ch)
    )
    return cleaned


def modernize(text: str) -> str:
    """Переводит текст в жирный юникод-шрифт."""
    out = []
    for ch in text or "":
        code = ord(ch)
        if "A" <= ch <= "Z":
            out.append(chr(code + _BOLD_UPPER))
        elif "a" <= ch <= "z":
            out.append(chr(code + _BOLD_LOWER))
        elif "0" <= ch <= "9":
            out.append(chr(code + _BOLD_DIGIT))
        else:
            out.append(ch)
    return "".join(out)


KEEP_AS_IS = {"url", "text_link", "mention", "text_mention", "code", "pre", "bot_command"}


def has_links(entities: Optional[Sequence[MessageEntity]]) -> bool:
    """Есть ли в тексте ссылки, @юзернеймы или код — такое не трогаем вообще."""
    return any(e.type in KEEP_AS_IS for e in (entities or []))


def apply_style(text: str, specials: bool, modern: bool) -> str:
    """specials=False -> чистим спецсимволы; modern=True -> красивый шрифт."""
    if not text:
        return text
    if not specials:
        text = strip_specials(text)
    if modern:
        text = modernize(text)
    return text


# --------------------------------------------------------------------------- #
#                                 упоминания                                   #
# --------------------------------------------------------------------------- #

def mentions_in(text: str, entities: Sequence[MessageEntity]) -> set[str]:
    """Все @юзернеймы сообщения — и текстом, и entity-ссылками."""
    found = {m.lower() for m in MENTION_RE.findall(text or "")}
    for entity in entities or []:
        if entity.type == "mention":
            chunk = text[entity.offset: entity.offset + entity.length]
            found.add(chunk.lstrip("@").lower())
    return {name for name in found if name}


# --------------------------------------------------------------------------- #
#                             хеш для антидубля                                #
# --------------------------------------------------------------------------- #

def content_hash(sources: list[Message]) -> str:
    parts: list[str] = []
    for src in sources:
        text, _ = source_text(src)
        parts.append(text or "")
        for obj in (
            src.photo[-1] if src.photo else None,
            src.video, src.animation, src.audio, src.voice,
            src.document, src.sticker, src.video_note,
        ):
            if obj is not None:
                parts.append(getattr(obj, "file_unique_id", ""))
        if src.poll:
            parts.append(src.poll.question)
    return hashlib.sha256("|".join(parts).encode()).hexdigest()


def media_ids(src: Message) -> list[str]:
    """file_unique_id всех вложений — для медиа-фильтров."""
    out: list[str] = []
    for obj in (
        src.photo[-1] if src.photo else None,
        src.video, src.animation, src.audio, src.voice,
        src.document, src.sticker, src.video_note,
    ):
        if obj is not None:
            uid = getattr(obj, "file_unique_id", None)
            if uid:
                out.append(uid)
    return out


# --------------------------------------------------------------------------- #
#                              спецсимволы                                     #
# --------------------------------------------------------------------------- #

SPECIALS_RE = re.compile(r"^(?:!\d+|[*^~&])+")


def parse_specials(text: str) -> tuple[str, dict, int]:
    flags: dict = {}
    if not text:
        return text, flags, 0

    match = SPECIALS_RE.match(text)
    if not match:
        return text, flags, 0

    chunk = match.group(0)
    for token in re.findall(r"!\d+|[*^~&]", chunk):
        if token.startswith("!"):
            flags["autodel"] = min(int(token[1:]), 40)
        elif token == "*":
            flags["protect"] = True
        elif token == "^":
            flags["notag"] = True
        elif token == "~":
            flags["spoiler"] = True
        elif token == "&":
            flags["modern"] = True

    return text[len(chunk):], flags, u16len(chunk)


def cut_prefix(
    text: str, entities: Optional[Sequence[MessageEntity]], cut: int
) -> tuple[str, list[MessageEntity]]:
    out: list[MessageEntity] = []
    for entity in entities or []:
        offset, length = entity.offset - cut, entity.length
        if offset < 0:
            length += offset
            offset = 0
        if length <= 0:
            continue
        out.append(
            MessageEntity(
                type=entity.type, offset=offset, length=length, url=entity.url,
                user=entity.user, language=entity.language,
                custom_emoji_id=entity.custom_emoji_id,
            )
        )
    return text, out


# системные теги, которые нельзя подделывать в своём тексте
SYSTEM_TAGS = (
    "#REPLY", "#Mention", "#MUTE", "#UNMUTE", "#WARN", "#REPORT",
    "#SYSTEM", "#VOTEMUTE", "#DELETE", "DELETED",
)
_MANGLE = "\u0489"


def mangle_system_tags(text: str) -> str:
    """Чужой '#MUTE' в тексте перестаёт выглядеть как настоящий системный тег."""
    if not text:
        return text
    for tag in SYSTEM_TAGS:
        if tag in text:
            text = text.replace(tag, tag[0] + _MANGLE + tag[1:])
    return text