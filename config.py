"""Конфигурация. Секреты — из .env, поведение — в БД (правится через /sett и /set)."""

import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "").strip()

# Овнер только один и только по ID. Командой овнерку выдать невозможно.
OWNER_ID: int = int(os.getenv("OWNER_ID", "0") or 0)
OWNER_USERNAME: str = os.getenv("OWNER_USERNAME", "digitkiss").lstrip("@")

# Приватный канал логов (бот должен быть там админом).
LOG_CHANNEL: int = int(os.getenv("LOG_CHANNEL", "0") or 0)

DB_PATH: str = os.getenv("DB_PATH", "echo.db")

# Ключ шифрования юзернеймов. Сменишь — старые записи не расшифруются.
SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-please")

TIMEZONE: str = os.getenv("TIMEZONE", "Europe/Moscow")
TZ_LABEL: str = os.getenv("TZ_LABEL", "MSK")

VERSION = "3.0"

DEFAULT_SETTINGS: dict[str, str] = {
    # какие типы сообщений вообще рассылаются
    "echo_text": "1",
    "echo_doc": "1",
    "echo_voice": "1",
    "echo_sticker": "1",
    "echo_video": "1",
    "echo_photo": "1",
    "echo_poll": "1",
    # скорость
    "send_delay": "0",           # задержка перед каждой копией, сек
    "slowmode": "8",             # КД между сообщениями пользователя, сек
    "slowmode_staff": "1",       # действует ли КД на админов
    "slowmode_owner": "0",       # действует ли КД на овнера
    "parallel_limit": "80",      # лимит параллельных отправок
    # второй тег: у админа цифра со ссылкой, у овнера просто OWNER.
    # Показывается только вместе с первым тегом; у обычных юзеров его нет.
    "staff_badge": "1",                              # глобальный выключатель второго тега
    "admin_badge_url": "https://t.me/alltoechobot",  # куда ведёт цифра админа
    "owner_prefix": "OWNER",
    "admin_prefix": "1",
    # поведение
    "stub_hours": "30",          # когда сообщение становится пустышкой
    "autoafk_days": "3",         # авто-AFK при молчании
    "report_cooldown": "300",    # КД репорта, сек
    "vote_minutes": "5",         # длительность голосования на мут
    "warn_limit": "3",           # варнов до мута
    "warn_base_mute": "10800",   # первый мут за варны, сек
    "warn_multiplier": "3",      # множитель мута на каждом цикле
    "media_group_wait": "1.3",   # сколько ждём сборки альбома, сек
    "reg_blocked": "0",          # закрыть вход новым пользователям
    "specials_enabled": "1",     # спецсимволы !n * ^ ~ &
    "mangle_system_tags": "1",   # ломать #MUTE и прочие системные теги в чужом тексте
    "ignore_enabled": "1",       # выключить игнор глобально, не стирая списки
    "filters_enabled": "1",      # то же для фильтров
    "no_duplicates": "1",        # запрет дублировать своё прошлое сообщение
    "duplicate_window": "600",  # через сколько секунд дубль снова разрешён
    "name_max": "17",            # длина кастомного тега
    "greet_registered": "1",
}

# Команды, которые овнер может отключать. /start отключить нельзя.
TOGGLEABLE_COMMANDS = [
    "help", "rules", "users", "lang", "tag", "name", "emoji", "profile", "protect",
    "autodel", "reaction", "pm", "report", "afk", "unafk",
    "config", "leave", "support", "ping", "privacy",
    "ignore", "unignore", "ignorelist", "filter", "unfilter", "filterlist",
]

# Права админов. У овнера всё и без лимитов.
RIGHTS = ["mute", "unmute", "warn", "unwarn", "del", "votemute", "who", "pin"]

DEFAULT_LIMITS = {
    "mute": 10,
    "unmute": 20,
    "warn": 20,
    "unwarn": 20,
    "del": 50,
    "votemute": 5,
    "pin": 20,
    "media": 20,
    "who": 0,   # 0 в rights = право есть, но без лимита; отсутствие ключа = нет права
}