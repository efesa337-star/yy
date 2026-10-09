"""Тексты бота. RU — основной, EN — частичный (недостающее берётся из RU)."""

RU: dict[str, str] = {
    # ------------------------------------------------------------- регистрация
    "greet": (
        "Привет, {name}!\n"
        "Это бот-проект для анонимной отправки любых ваших сообщений пользователям, "
        "которые находятся в этом боте, его можно назвать чатом, но только анонимным\n"
        "Здесь есть правила, и вы всегда можете их прочитать. Для того чтобы "
        "зарегистрироваться в этом эхо-боте, вы должны подтвердить, что прочитали "
        "и согласны со всеми правилами, которые публично существуют в /rules"
    ),
    "reg_closed": "Регистрация в боте закрыта.",
    "reg_block_on": "Регистрация закрыта. Новые пользователи войти не смогут.",
    "reg_block_off": "Регистрация открыта. Новые пользователи снова могут войти.",
    "registered": (
        "Салам, {name}!\n\n"
        "Смотри /help дабы понять что к чему\n"
        "Если возникнут вопросы или проблемы, пишите @{owner}"
    ),
    "start_help": (
        "Помощь по боту.\n"
        "> /help - Подробная помощь по боту!\n\n"
        "> /rules - правила\n"
        "> /tag - включить упоминание ника и юзера\n"
        "> /profile - стата о тебе\n"
        "> /protect - запрет пересылки\n"
        "> /autodel - автоудаление\n"
        "> /report - жалоба на сообщение\n"
        "> /users - юзеров в боте"
    ),
    "help": (
        "Помощь в командах.\n"
        "/rules -  Правила бота\n"
        "/users - Сколько пользователей в боте\n"
        "/lang - Сменить язык бота\n"
        "/tag - (Вкл/Выкл) тег под твоими сообщениями\n"
        "/profile - Информация о тебе в боте\n"
        "/protect - (Вкл/Выкл) - (копировать/пересылать/сохранять) твои сообщения\n"
        "/report &lt;ответ&gt; [причина] - Пожаловаться на сообщение\n"
        "/leave &lt;ид&gt; - Покинуть бота\n"
        "/autodel - Автоудаление ваших сообщений\n"
        "/config - Посмотреть конфигурацию бота\n"
        "/pm &lt;reply&gt; &lt;text&gt; - Отправить личное сообщение\n"
        "/afk - Перенести себя в архив\n"
        "/unafk - Восстановить себя с архива\n"
        "/reaction - (Вкл/Выкл) приход реакций вам\n"
        "/ignore &lt;reply&gt; - Отключить сообщения от человека\n"
        "/unignore &lt;reply|#index|all&gt; - Включить показ сообщений от человека\n"
        "/ignoreList - Сколько пользователей в игнор листе\n"
        "/name [text] - Кастомный текст для тега\n"
        "/emoji [emoji-id|emoji] - Установить Premium эмодзи в теге\n"
        "/filter &lt;reply_to_media|word|/regex/&gt; - Добавить слово/медиа/регулярное в ваш фильтр\n"
        "/unfilter &lt;reply_to_media|word|/regex/|all&gt; - Убрать слово/медиа/регулярное из вашего фильтра\n"
        "/filterList - Список ваших фильтров"
    ),
    "help_admin": (
        "\n\nАдмин команды.\n"
        "/mute &lt;reply&gt; &lt;время&gt; [причина] - Отключить от чата\n"
        "/unmute &lt;reply&gt; - Вернуть в чат\n"
        "/warn &lt;reply&gt; [причина] - Выдать предупреждение\n"
        "/unwarn &lt;reply&gt; - Снять предупреждение\n"
        "/del &lt;reply&gt; | /del &lt;id&gt; &lt;сколько&gt; - Удалить сообщения\n"
        "/votemute &lt;reply&gt; &lt;время&gt; [причина] - Голосование на мут\n"
        "/media &lt;reply&gt; - Запретить/вернуть отправку медиа\n"
        "/pin &lt;reply&gt; - Закрепить сообщение у всех\n"
        "/unpin &lt;reply&gt; - Открепить\n"
        "/media &lt;reply&gt; - Запретить/вернуть отправку медиа\n"
        "/pin &lt;reply&gt; - Закрепить сообщение у всех\n"
        "/unpin &lt;reply&gt; - Открепить\n"
        "/rights - Твои права и остаток лимитов"
    ),
    "help_owner": (
        "\n\nОвнер команды.\n"
        "/sett - Панель управления ботом\n"
        "/set &lt;ключ&gt; &lt;значение&gt; - Ручная правка любой настройки\n"
        "/promote &lt;reply&gt; - Выдать админку\n"
        "/demote &lt;reply&gt; - Снять админку\n"
        "/prefix &lt;reply&gt; &lt;текст&gt; - Префикс админа\n"
        "/mytag &lt;текст&gt; [link|nolink] - Свой кастомный тег\n"
        "/who &lt;reply&gt; - Кто это пишет (id, юзернейм, ник)\n"
        "/settag &lt;текст&gt; | &lt;ссылка&gt; - Свой кастомный тег\n"
        "/system &lt;текст&gt; - Системная рассылка\n"
        "/blockreg - Закрыть или открыть регистрацию новым\n"
        "/restart - Перезапустить бота"
    ),
    "rules_default": "БОТ НОУРУЛС, НО ВСЁ РАССМАТРИВАЕТСЯ ИНДИВИДУАЛЬНО, НАСКОЛЬКО ВЫ БИОМУСОР 🤣",
    "support": "If you have questions or known problems, contact @{owner}",
    "specials_guide": (
        "Спецсимволы работают единоразово для сообщения\n"
        "  1. !n — Типично !\\d+, ставит авто-удаления для текущего сообщения, "
        "измеряется в минутах. Максимум 40 минут\n"
        "  2. * — Включает или выключает /protect в противоположное значения текущего.\n"
        "  3. ^ — Выключает /tag\n"
        "  4. ~ — Переключает текущий спойлер медиа в противоположенное значение профиля\n"
        "  5. &amp; — Модернизирует текст (спуфинг)\n\n"
        "Как использовать? Пишите в начало текста сообщения.\n"
        "К примеру, пишите сообщение с текстом:\n"
        "  \"!32День хороший!\" - вырежет из текста \"!32\",\n"
        "  отправит \"День хороший!\",\n"
        "  сообщение удалится для всех через 32 минуты.\n\n"
        "Можно комбинировать.\n"
        "Это можно отключить в /profile."
    ),
    "privacy": (
        "Условия использования.\n"
        "Введение\n"
        "Это бот \"эхо-бот\", который повторяет сообщения пользователей.\n\n"
        "Правила использования\n"
        "После команды /start пользователь обязан ознакомиться с правилами бота и согласиться с ними.\n\n"
        "Регистрация\n"
        "После команды /start выполняется captcha для проверки, что пользователь не бот. Бот сохраняет \"id\" и \"language_code\" пользователя.\n\n"
        "Анонимность и отправка сообщений\n"
        "Пользователь может видеть и отправлять сообщения по умолчанию анонимно. Другие пользователи не видят информацию о пользователе, пока он сам не раскроет full_name или username.\n\n"
        "Команда /tag меняет анонимность пользователя. Есть кнопка для переключения видимости ссылки на пользователя. При отключении анонимности, в сообщения добавляется информация о пользователе в inline_keyboard.\n\n"
        "Сохранение данных\n"
        "После первого сообщения бот сохранит username пользователя в зашифрованном виде. Это нужно для уведомлений хештегом #Mention.\n\n"
        "Также пользователь вправе удалить свои данные из базы с помощью команды /leave или заблокировав бота, тогда бот сам удалит пользователя из базы данных.\n\n"
        "Распространение сообщений\n"
        "После отправки сообщения бот дублирует его всем пользователям и сохраняет user_id и message_id в базу данных. Пользователь может удалить запись, удалив сообщение. Связки сообщений живут {hours} часов.\n\n"
        "Нарушение правил\n"
        "За нарушение правил или по усмотрению администратора пользователь может быть отключен от отправки сообщений на любой срок. Администратор также имеет право удалить пользователя из базы данных бота.\n\n"
        "Конфиденциальность\n"
        "База данных доступна только владельцу бота.\n\n"
        "Контактная информация\n"
        "Для вопросов: @{owner}"
    ),

    # ------------------------------------------------------------------ шифр
    "username_encrypted": "Ваш username был зашифрован и записан в базу как: {blob}",
    "username_changed": (
        "Твой username изменился и перезаписан в базе как: {blob}"
    ),

    # --------------------------------------------------------------- профиль
    "profile": (
        "Салам {name}\n"
        "Твой ID: {id}\n"
        "Время у бота: {clock}\n"
        "Время регистрации в боте: {joined} — {joined_ago}\n"
        "Юзернейм: {username}\n"
        "Время последнего твоего сообщ.: {last} — {last_ago}\n"
        "Сообщений отправлено тобою: {msgs}\n"
        "{role_line}\n"
        "У тебя {warns}/{warn_limit} предупреждений. Серия {streak}"
    ),
    "role_user": "Вы не админ :(",
    "role_owner": "Вы овнер бота. Префикс: {prefix}",
    "role_admin": "Вы админ. Префикс: {prefix}\nПрава: {rights}",
    "rights_none": "нет прав",
    "rights_mine": "Твой админ тег: {prefix}\nТвои права:\n{items}",
    "rights_owner": "Ты овнер. Твой тег: {prefix}\nПрава: все, без лимитов.",

    # ---------------------------------------------------------------- кнопки
    "btn_media_meta": "Медиа метадата: {v}",
    "btn_autoedit": "Авторедактирование: {v}",
    "btn_protect": "Защита сообщений: {v}",
    "btn_tag": "Ник(тег) в сообщениях: {v}",
    "btn_tag_link": "Ссылка на вас в кнопке: {v}",
    "btn_autodel": "Автоудаление сообщений: {v}",
    "btn_keep_username": "Хранить твой юзер (зашифр.): {v}",
    "btn_del_warning": "Предупреждение об удаление: {v}",
    "btn_reaction": "Ставить вам реакции: {v}",
    "btn_specials": "Использование спецсимволов: {v}",
    "btn_autoreply": "Авто ответ: {v}",
    "btn_spoiler_in": "Спойлерить медиа людей: {v}",
    "btn_spoiler_out": "Спойлерить мои медиа: {v}",
    "btn_modernize": "Модернизировать ваш текст: {v}",
    "btn_ignore": "🗑 Игнор: {n}",
    "btn_ignore_pm": "🗑 Игнор ЛС: {n}",
    "btn_filters": "🗑 Фильтры: {n}",
    "btn_pm": "Личные сообщения: {v}",
    "btn_custom": "Кастомный текст: {v}",
    "btn_badge": "Админ тег: {v}",
    "btn_mark": "Пометить ваши сообщения: {v}",
    "btn_link": "Ссылка на вас: {v}",
    "btn_close": "Закрыть",
    "btn_delete_mine": "Удалить моё сообщение",

    # ------------------------------------------------------------------- тег
    "tag_head": (
        "Де-анонимизация ваших сообщений.\n"
        "По умолчанию ваши сообщения анонимны, но вы можете помечать свои "
        "сообщения своим именем"
    ),
    "name_head": (
        "Команда /name устанавливает или сбрасывает кастомный никнейм для тега.\n"
        "В теге вместо вашего имени \"🌧️\" будет отображаться другой текст.\n"
        "Ограничение: от 1 до 24 символа\n\n"
        "Для сброса введите эту команду без аргументов."
    ),
    "name_set": "Кастомный текст установлен: {name}",
    "name_off": "Кастомный текст сброшен, в теге снова ник аккаунта.",
    "name_bad": "Длина от 1 до 24 символов.",

    "emoji_head": (
        "Установить Premium эмодзи в вашем кастомном нике/теге.\n"
        "Примеры:\n"
        "/emoji 5383922934177701460 (emoji-id)\n"
        "/emoji 5383922934177701460 (tg-emoji)\n\n"
        "Для сброса введите команду без аргументов."
    ),
    "emoji_set": "Кастомный эмодзи установлен.",
    "emoji_off": "Эмодзи сброшен.",
    "emoji_bad": "Некорректный эмодзи или ID эмодзи.",

    # -------------------------------------------------------------- автоудал.
    "autodel_head": (
        "Выберите время которое по истечению будет автоматически удалять ваши "
        "сообщения для всех."
    ),
    "autodel_set": "Автоудаление: {value}",
    "autodel_off": "Автоудаление отключено.",

    # ------------------------------------------------------------------ язык
    "lang_head": "Выбери на каком должен быть язык бота\nChoose the bot language",
    "lang_set": "Язык бота: {name}",

    # -------------------------------------------------------------- настройки
    "protect_on": "Теперь пользователям будет запрещено (копировать/пересылать/сохранять) твои сообщения.",
    "protect_off": "Теперь пользователям разрешено (копировать/пересылать/сохранять) твои сообщения.",
    "reaction_toggled": "Реакции теперь {v} для вас.",

    # ----------------------------------------------------------------- users
    "users": (
        "{active} активных пользователей.\n"
        "{afk} пользователей в AFK.\n\n"
        "{today} сегодня отправлено сообщений\n"
        "{mine} сегодня отправлено тобою"
    ),
    "ping": "Понг. {ms} мс",

    # ---------------------------------------------------------------- config
    "config": (
        "Время работы: {uptime}\n"
        "Задержка в отправке сообщений: {send_delay}\n"
        "Задержка между сообщениями: {slowmode} sec\n"
        "Лимит параллельной отправки: {parallel}\n"
        "Отправка эхо:\n"
        "  Text: {text}\n"
        "  Doc: {doc}\n"
        "  Voice: {voice}\n"
        "  Sticker: {sticker}\n"
        "  Video: {video}\n"
        "  Photo: {photo}\n"
        "  Poll: {poll}"
    ),

    # ------------------------------------------------------------------- afk
    "afk_on": "Ok! you transfer to afk",
    "afk_off": "Ok! you untransfer to afk",
    "afk_restored": "Твой аккаунт был восстановлен с архива (AFK)\nОтправь сообщение ещё раз.",
    "afk_auto": (
        "Ты был принудительно перемещён системой в Afk, по причине:\n"
        "Отправляй хоть одно сообщение в течении {period}, ты отправлял последнее "
        "сообщение в {last}."
    ),
    "tag_disabled_safety": "\n\nТвой тег был отключен для безопасности.",

    # ----------------------------------------------------------------- leave
    "leave_confirm": "Ты уверен(а) что хочешь покинуть бота?\nЕсли да, то напиши /leave {id}.",
    "leave_done": "Ты покинул бота. Вернуться — /start",

    # -------------------------------------------------------------- отправка
    "sending": "Отправляю…",
    "sent_ok": "Твоё сообщение успешно отправлено за {elapsed} {count} пользователям.",
    "sent_partial": "Твоё сообщение успешно отправлено за {elapsed} {ok}/{total} пользователям.",
    "sent_failed_head": "Не все получили сообщение: {n} по причине {reason}",
    "sent_flood": (
        "(В отправке сообщения у {n} пользователей возник flood wait "
        "с ожиданием: {waits} секунд)"
    ),
    "nobody": "Кроме тебя в боте никого нет.",
    "slowmode": "Задержка между сообщениями. Подожди {left} сек.",
    "type_disabled": "Отправка этого типа сообщений отключена овнером.",
    "duplicate": "То же самое сообщение можно повторить через {left}.",

    # -------------------------------------------------------- удал./редакт.
    "deleted_ok": "Ваше сообщение было удалено {count} пользователям.",
    "delete_confirm": "Удалить это сообщение у всех?",
    "edit_confirm": "Изменить это сообщение у всех получателей?",
    "edited_ok": "Сообщение изменено {count} пользователям.",
    "edited_mark": "(edited message)",
    "msg_stub": "Сообщение слишком старое — на него больше нельзя ответить или пожаловаться.",
    "not_your_msg": "Это не твоё сообщение.",

    # ------------------------------------------------------------------- ЛС
    "pm_head": "Отправить анонимное сообщение любому человеку.",
    "pm_usage": "Ответь этой командой на сообщение и напиши текст.",
    "pm_sent": "Личное сообщение отправлено.",
    "pm_fail": "Не доставлено: пользователь заблокировал бота или вышел.",
    "pm_blocked": "Этот пользователь закрыл для тебя личные сообщения.",
    "pm_closed": "У пользователя выключены личные сообщения.",
    "pm_in_head": "Вам пришло новое Анонимное сообщение:",
    "pm_in_foot": "Для ответа просто ответьте на это сообщение.\n(Ваш юзернейм скрыт)",
    "pm_block_done": "Пользователь заблокирован, писать тебе в ЛС он больше не сможет.",
    "pm_unblock_done": "Пользователь разблокирован в ЛС.",
    "pm_block_cleared": "Игнор ЛС очищен.",
    "btn_pm_block": "Заблокировать пользователя",
    "pm_block_empty": "Игнор ЛС пуст.",
    "pm_block_list": "В игноре ЛС {n}:\n{items}",

    # ---------------------------------------------------------------- игноры
    "ignore_head": (
        "Эта команда добавляет человека (по ответу на сообщение), в игнор лист.\n"
        "Вы не увидите следующих сообщений от этого пользователя. Но убрать его из "
        "списка вы всегда можете.\n"
        "Для удаления из списка вы можете использовать команду /unignore "
        "&lt;reply|#index|all&gt;\n\n"
        "Пример: /ignore &lt;reply&gt;"
    ),
    "unignore_head": (
        "Эта команда удаляет человека из игнор листа.\n"
        "Вам вновь будут приходить сообщения того человека.\n\n"
        "Пример: /unignore &lt;reply|#index|all&gt;"
    ),
    "ignore_added": "Пользователь добавлен в игнор лист. Всего в списке: {n}",
    "mode_tag": "с тегом",
    "mode_anon": "анонимом",
    "ignore_exists": "Этот пользователь уже в игнор листе.",
    "ignore_self": "Себя в игнор добавить нельзя.",
    "ignore_removed": "Пользователь убран из игнор листа. Осталось: {n}",
    "ignore_cleared": "Игнор лист очищен, удалено: {n}",
    "ignore_empty": "Игнор-лист пуст.",
    "ignore_list": "В игнор листе {n}:\n{items}",

    # --------------------------------------------------------------- фильтры
    "filter_head": (
        "Фильтр позволяет вам скрыть сообщения, содержащие определённые слова или медиа.\n"
        "Вы можете добавлять слова в ваш фильтр, и сообщения с этими словами не будут "
        "отображаться вам.\n\n"
        "Чтобы скрыть слово, просто в аргументах укажите слово\n"
        "Чтобы скрыть медиа, ответьте данной командой на сообщение с медиа.\n\n"
        "Вы также можете использовать regex, для этого начните и закончите слово с /\n"
        "Вы можете использовать группы и классы символов.\n\n"
        "Примеры:\n"
        "/filter test\n"
        "/filter /test\\d+/"
    ),
    "unfilter_head": (
        "Нет аргументов. Добавьте слово, чтобы удалить его из фильтра.\n"
        "Или вы можете добавить all, чтобы удалить все из фильтра."
    ),
    "filter_added": "Добавлено в фильтр ({kind}): {value}\nВсего фильтров: {n}",
    "filter_exists": "Такой фильтр уже есть.",
    "filter_bad_regex": "Некорректное регулярное выражение.",
    "filter_removed": "Удалено из фильтра: {value}. Осталось: {n}",
    "filter_not_found": "Такого фильтра нет.",
    "filter_cleared": "Фильтры очищены, удалено: {n}",
    "filter_empty": "Список фильтров пуст.",
    "filter_list": "Ваши фильтры ({n}):\n{items}",
    "filter_need_media": "Ответьте командой на сообщение с медиа или укажите слово.",

    # -------------------------------------------------------------- репорты
    "report_usage": "Ответь этой командой на сообщение и укажи причину.",
    "report_sent": "Жалоба отправлена админам.",
    "report_cd": "Следующая жалоба будет доступна через {left}.",
    "report_muted": "Ты в муте, репорт недоступен.",
    "report_self": "На себя жаловаться не нужно.",
    "report_admin": (
        "#REPORT\n"
        "На: {target} (ID {target_id})\n"
        "От: {author} (ID {author_id})\n"
        "Причина: {reason}"
    ),

    # -------------------------------------------------------------- модерация
    "no_rights": "Нет прав.",
    "limit_reached": "Лимит по команде исчерпан: {used}/{limit} за сутки.",
    "need_reply": "Нужно ответить на сообщение.",
    "reply_unknown": "Не нашёл, чьё это сообщение. Ответь именно на сообщение человека.",
    "target_not_found": "Пользователь не найден.",
    "mute_usage": "Ответь командой на сообщение: /mute &lt;время&gt; [причина]\nЛибо: /mute &lt;id&gt; &lt;время&gt; [причина]",
    "mute_bad_time": "Не понял время. Примеры: 30s, 15m, 3h, 7d, 1w, 1mo, 1y.",
    "mute_notice": "#MUTE\nВы были отключены от чата на {duration}.",
    "mute_notice_reason": "#MUTE\nВы были отключены от чата на {duration}.\n\nПо причине: {reason}",
    "mute_blocked": "{name} ты отключен(а) от чата\nВернись через {left}. {until}",
    "mute_blocked_reason": (
        "{name} ты отключен(а) от чата\n"
        "По причине: {reason}\n"
        "Вернись через {left}. {until}"
    ),
    "mute_done": "{target} замучен на {duration}. Причина: {reason}",
    "unmute_notice": "#UNMUTE\nВы снова можете писать в чат.",
    "unmute_done": "{target} размучен.",
    "not_muted": "Пользователь не в муте.",
    "mute_expired": "#UNMUTE\nМут истёк, вы снова можете писать.",
    "warn_notice": "#WARN\nВы получили предупреждение {n}/{limit}.\n\nПо причине: {reason}",
    "warn_done": "{target}: варн {n}/{limit}.",
    "unwarn_done": "{target}: варнов {n}/{limit}.",
    "warn_automute": "\n\nЗа {limit} предупреждения выдан мут на {duration}.",
    "pin_done": "Закреплено у {count} пользователей.",
    "unpin_done": "Открепление у {count} пользователей.",
    "settag_usage": (
        "Кастомный тег: /settag &lt;текст&gt; | &lt;ссылка&gt;\n"
        "Только текст: /settag Хрюхряка\n"
        "С ссылкой: /settag Хрюхряка | https://t.me/digitkiss\n"
        "Сброс: /settag"
    ),
    "settag_set": "Тег: {text}\nСсылка: {url}",
    "settag_off": "Кастомный тег сброшен.",
    "media_blocked": "Тебе запрещено отправлять медиа, только текст.",
    "media_unblocked": "Запрет на медиа снят.",
    "media_done": "{target}: медиа {state}.",
    "media_on": "запрещены",
    "media_off": "разрешены",
    "del_usage": "Ответь командой на сообщение: /del\nЛибо: /del &lt;id&gt; &lt;сколько последних&gt;",
    "del_done": "Удалено сообщений: {msgs}, копий: {copies}.",
    "pin_done": "Закреплено у {count}.",
    "unpin_done": "Откреплено у {count}.",
    "log_delete": "#DELETE\n{who}\nКопий снято: {count}",
    "del_notice": "#SYSTEM MESSAGE\nВаше сообщение было удалено модератором.",
    "deleted_broadcast": "Это сообщение было удалено для {count} пользователей.",
    "tag_system": "#SYSTEM",
    "tag_deleted": "DELETED",

    # ---------------------------------------------------------- голосование
    "vote_usage": "Ответь командой на сообщение: /votemute &lt;время&gt; [причина]",
    "vote_started": "Голосование запущено, идёт {minutes} мин.",
    "vote_head": (
        "#VOTEMUTE\n"
        "Предложен мут: {target}\n"
        "Срок: {duration}\n"
        "Причина: {reason}\n"
        "Инициатор: {author}\n\n"
        "Голосование идёт {minutes} мин."
    ),
    "vote_voted": "Голос учтён.",
    "vote_result_pass": "#VOTEMUTE\nГолосование завершено: {yes} за / {no} против. Мут выдан.",
    "vote_result_fail": "#VOTEMUTE\nГолосование завершено: {yes} за / {no} против. Мут не выдан.",
    "vote_no_staff": "Некому голосовать: нет админов.",
    "vote_over": "Голосование завершено.",

    # ------------------------------------------------------------------ прочее
    "system_prefix": "#SYSTEM MESSAGE",
    "cmd_disabled": "Команда отключена.",
    "unknown_cmd": "Нет такой команды. /help",
    "reply_mark": "#REPLY",
    "mention_mark": "#Mention",
    "who_usage": "Ответь командой на сообщение: /who\nЛибо: /who &lt;id&gt;",
    "who_result": (
        "ID: {id}\n"
        "Юзернейм: {username}\n"
        "Ник: {name}\n"
        "Роль: {role}\n"
        "Регистрация: {joined}\n"
        "Сообщений: {msgs}"
    ),

    # ------------------------------------------------------------ овнер-панель
    "sett_head": "Панель овнера. Версия {version}.",
    "sett_echo": "Типы сообщений",
    "sett_speed": "Скорость и лимиты",
    "sett_cmds": "Команды",
    "sett_admins": "Админы",
    "sett_misc": "Прочее",
    "sett_buttons": "Кнопки и префиксы",
    "sett_owner_only": "Панель доступна только овнеру.",
    "set_usage": "/set &lt;ключ&gt; &lt;значение&gt;",
    "set_done": "{key} = {value}",
    "admin_added": "{target} назначен админом. Админ тег: {badge}",
    "admin_removed": "{target} больше не админ.",
    "admin_usage": "Ответь командой на сообщение: /promote\nЛибо: /promote &lt;id&gt;",
    "mytag_usage": (
        "/mytag &lt;текст&gt; — поставить кастомный тег\n"
        "/mytag &lt;текст&gt; link — с ссылкой на твой профиль\n"
        "/mytag &lt;текст&gt; nolink — без ссылки\n"
        "/mytag off — сбросить"
    ),
    "mytag_set": "Кастомный тег: {text}\nСсылка на профиль: {link}",
    "mytag_off": "Кастомный тег сброшен, в теге снова ник аккаунта.",
    "prefix_usage": "Ответь командой на сообщение: /prefix &lt;текст&gt;",
    "prefix_set": "Префикс для {target}: {value}",
    "system_usage": "/system &lt;текст&gt; — разослать системное сообщение всем.",
    "system_done": "Системное сообщение отправлено: {count}",
    "restarting": "Перезапускаюсь…",
    "ask_value": (
        "Отправь новое значение для <code>{key}</code> следующим сообщением.\n"
        "Чтобы сбросить — отправь <code>-</code>. Любая команда отменяет ввод."
    ),
    "ask_prefix": (
        "Отправь новый префикс для {target} следующим сообщением.\n"
        "Чтобы вернуть дефолтный — отправь <code>-</code>."
    ),
    "value_saved": "Сохранено: <code>{key}</code> = {value}",
    "value_reset": "Сброшено: <code>{key}</code>",
}

EN: dict[str, str] = {
    # ------------------------------------------------------------- registration
    "greet": (
        "Hi, {name}!\n"
        "This is an anonymous echo-bot project for sending any of your messages "
        "to other users in the bot — basically an anonymous chat.\n"
        "There are rules, and you can always read them. To register "
        "in this echo-bot, you must confirm that you have read "
        "and agree to all the rules publicly listed in /rules"
    ),
    "reg_closed": "Registration is currently closed.",
    "reg_block_on": "Registration is closed. New users cannot join.",
    "reg_block_off": "Registration is open. New users can join again.",
    "registered": (
        "Welcome, {name}!\n\n"
        "Check /help to understand how the bot works.\n"
        "If you have any questions or issues, message @{owner}"
    ),
    "start_help": (
        "Bot Help.\n"
        "> /help - Detailed command help!\n\n"
        "> /rules - Rules\n"
        "> /tag - Toggle tag/username in messages\n"
        "> /profile - Your stats\n"
        "> /protect - Prevent forwarding/copying\n"
        "> /autodel - Auto-delete your messages\n"
        "> /report - Report a message\n"
        "> /users - Active users count"
    ),
    "help": (
        "Command Help.\n"
        "/rules - Bot rules\n"
        "/users - Total users count\n"
        "/lang - Change bot language\n"
        "/tag - (On/Off) display tag under your messages\n"
        "/profile - Information about you in the bot\n"
        "/protect - (On/Off) - restrict copying/forwarding of your messages\n"
        "/report &lt;reply&gt; [reason] - Report a message\n"
        "/leave &lt;id&gt; - Leave the bot\n"
        "/autodel - Auto-delete your messages\n"
        "/config - View bot configuration\n"
        "/pm &lt;reply&gt; &lt;text&gt; - Send private message\n"
        "/afk - Move yourself to archive\n"
        "/unafk - Restore yourself from archive\n"
        "/reaction - (On/Off) toggle receiving reactions\n"
        "/ignore &lt;reply&gt; - Ignore messages from a user\n"
        "/unignore &lt;reply|#index|all&gt; - Unignore messages from a user\n"
        "/ignorelist - List of ignored users\n"
        "/name [text] - Set custom text for tag\n"
        "/emoji [emoji-id|emoji] - Set premium emoji in your tag\n"
        "/filter &lt;reply_to_media|word|/regex/&gt; - Add word/media/regex to filter\n"
        "/unfilter &lt;reply_to_media|word|/regex/|all&gt; - Remove word/media/regex from filter\n"
        "/filterlist - List of your filters"
    ),
    "help_admin": (
        "\n\nAdmin Commands.\n"
        "/mute &lt;reply&gt; &lt;time&gt; [reason] - Disconnect user from chat\n"
        "/unmute &lt;reply&gt; - Restore user access\n"
        "/warn &lt;reply&gt; [reason] - Warn user\n"
        "/unwarn &lt;reply&gt; - Remove warning\n"
        "/del &lt;reply&gt; | /del &lt;id&gt; &lt;count&gt; - Delete messages\n"
        "/votemute &lt;reply&gt; &lt;time&gt; [reason] - Start a vote to mute\n"
        "/media &lt;reply&gt; - Toggle media sending permission\n"
        "/pin &lt;reply&gt; - Pin message for everyone\n"
        "/unpin &lt;reply&gt; - Unpin message\n"
        "/rights - Your permissions and limits"
    ),
    "help_owner": (
        "\n\nOwner Commands.\n"
        "/sett - Bot control panel\n"
        "/set &lt;key&gt; &lt;value&gt; - Edit configuration\n"
        "/promote &lt;reply&gt; - Promote to admin\n"
        "/demote &lt;reply&gt; - Demote from admin\n"
        "/prefix &lt;reply&gt; &lt;text&gt; - Set admin prefix\n"
        "/mytag &lt;text&gt; [link|nolink] - Custom owner tag\n"
        "/who &lt;reply&gt; - Identify user (id, username, name)\n"
        "/settag &lt;text&gt; | &lt;url&gt; - Custom url tag\n"
        "/system &lt;text&gt; - Broadcast system message\n"
        "/blockreg - Toggle registration block\n"
        "/restart - Restart the bot"
    ),
    "rules_default": "BOT HAS NO RULES, BUT EVERYTHING IS EVALUATED INDIVIDUALLY 🤣",
    "support": "If you have questions or known problems, contact @{owner}",
    "specials_guide": (
        "Special characters work once per message\n"
        "  1. !n — Usually !\\d+, sets auto-deletion for current message in minutes. Max 40 mins\n"
        "  2. * — Toggles /protect setting for current message.\n"
        "  3. ^ — Disables /tag\n"
        "  4. ~ — Toggles media spoiler\n"
        "  5. &amp; — Modernizes text (spoofing)\n\n"
        "How to use? Put them at the very beginning of your message.\n"
        "For example:\n"
        "  \"!32Good day!\" - will strip \"!32\",\n"
        "  send \"Good day!\",\n"
        "  and delete the message for everyone in 32 minutes.\n\n"
        "You can combine them. Can be turned off in /profile."
    ),
    "privacy": (
        "Terms of Use.\n"
        "Introduction\n"
        "This is an \"echo-bot\" that repeats user messages.\n\n"
        "Terms of Use\n"
        "After the /start command, the user is obliged to read and agree to the bot's rules.\n\n"
        "Registration\n"
        "After the /start command, a captcha is executed to verify that the user is not a bot. The bot saves the \"id\" and \"language_code\" of the user.\n\n"
        "Anonymity and Sending Messages\n"
        "The user can see and send messages anonymously by default. Other users do not see information about the user until they reveal their full_name or username themselves.\n\n"
        "The /tag command changes the user's anonymity. There is a button to toggle the visibility of the link to the user. When anonymity is turned off, user information is added to the messages in the inline_keyboard.\n\n"
        "Data Storage\n"
        "After the first message, the bot will save the user's username in encrypted form. This is needed for #Mention hashtag notifications.\n\n"
        "Also, the user has the right to delete their data from the database using the /leave command or by blocking the bot, then the bot itself will delete the user from the database.\n\n"
        "Distribution of Messages\n"
        "After sending a message, the bot duplicates it to all users and saves the user_id and message_id in the database. The user can delete the record by deleting the message. Message links last for {hours} hours.\n\n"
        "Violation of Rules\n"
        "For violating the rules or at the discretion of the administrator, the user may be disabled from sending messages for any period. The administrator also has the right to delete the user from the bot's database.\n\n"
        "Confidentiality\n"
        "The database is only accessible to the bot owner.\n\n"
        "Contact Information\n"
        "For questions: @{owner}"
    ),
    "username_encrypted": "Your username has been encrypted and saved: {blob}",
    "username_changed": "Your username has changed and was updated: {blob}",
    "profile": (
        "Hello {name}\n"
        "Your ID: {id}\n"
        "Bot clock: {clock}\n"
        "Registered: {joined} — {joined_ago}\n"
        "Username: {username}\n"
        "Last message: {last} — {last_ago}\n"
        "Total messages sent: {msgs}\n"
        "{role_line}\n"
        "Warnings: {warns}/{warn_limit}. Streak: {streak}"
    ),
    "role_user": "You are not an admin :(",
    "role_owner": "You are the bot owner. Prefix: {prefix}",
    "role_admin": "You are an admin. Prefix: {prefix}\nRights: {rights}",
    "rights_none": "no rights",
    "rights_mine": "Your admin tag: {prefix}\nYour rights:\n{items}",
    "rights_owner": "You are the owner. Tag: {prefix}\nRights: unlimited.",
    "btn_media_meta": "Media Metadata: {v}",
    "btn_autoedit": "Auto-edit: {v}",
    "btn_protect": "Message protection: {v}",
    "btn_tag": "Tag in messages: {v}",
    "btn_tag_link": "Profile link in button: {v}",
    "btn_autodel": "Auto-delete messages: {v}",
    "btn_keep_username": "Keep username (enc): {v}",
    "btn_del_warning": "Deletion warning: {v}",
    "btn_reaction": "Allow reactions: {v}",
    "btn_specials": "Use special symbols: {v}",
    "btn_autoreply": "Auto-reply: {v}",
    "btn_spoiler_in": "Spoiler other's media: {v}",
    "btn_spoiler_out": "Spoiler my media: {v}",
    "btn_modernize": "Modernize my text: {v}",
    "btn_ignore": "🗑 Ignore: {n}",
    "btn_ignore_pm": "🗑 Ignore PM: {n}",
    "btn_filters": "🗑 Filters: {n}",
    "btn_pm": "Private Messages: {v}",
    "btn_custom": "Custom text: {v}",
    "btn_badge": "Admin tag: {v}",
    "btn_mark": "Tag your messages: {v}",
    "btn_link": "Link to you: {v}",
    "btn_close": "Close",
    "btn_delete_mine": "Delete my message",
    "tag_head": "De-anonymize your messages. By default, they are anonymous, but you can sign them with your name.",
    "name_head": (
        "The /name command sets or resets a custom nickname for your tag.\n"
        "Instead of your account name, \"🌧️\" will show up in your tag.\n"
        "Limit: 1 to 24 characters\n\n"
        "To reset, send this command without arguments."
    ),
    "name_set": "Custom tag set: {name}",
    "name_off": "Custom tag reset, showing account name again.",
    "name_bad": "Length must be between 1 and 24 characters.",
    
    "emoji_head": (
        "Set Premium emoji in your custom tag.\n"
        "Examples:\n"
        "/emoji 5383922934177701460 (emoji-id)\n"
        "/emoji 5383922934177701460 (tg-emoji)\n\n"
        "To reset, send this command without arguments."
    ),
    "emoji_set": "Custom emoji set.",
    "emoji_off": "Emoji reset.",
    "emoji_bad": "Invalid emoji or emoji ID.",

    "autodel_head": "Choose the time after which your messages will be automatically deleted for everyone.",
    "autodel_set": "Auto-delete: {value}",
    "autodel_off": "Auto-delete disabled.",
    "lang_head": "Choose the bot language",
    "lang_set": "Bot language: {name}",
    "protect_on": "Users are now restricted from copying/forwarding your messages.",
    "protect_off": "Users are now allowed to copy/forward your messages.",
    "reaction_toggled": "Reactions are now {v} for you.",
    "users": (
        "{active} active users.\n"
        "{afk} AFK users.\n\n"
        "{today} messages sent today\n"
        "{mine} sent by you today"
    ),
    "ping": "Pong. {ms} ms",
    "config": (
        "Uptime: {uptime}\n"
        "Send delay: {send_delay}\n"
        "Slowmode: {slowmode} sec\n"
        "Parallel limit: {parallel}\n"
        "Echo delivery:\n"
        "  Text: {text}\n"
        "  Doc: {doc}\n"
        "  Voice: {voice}\n"
        "  Sticker: {sticker}\n"
        "  Video: {video}\n"
        "  Photo: {photo}\n"
        "  Poll: {poll}"
    ),
    "afk_on": "Ok! you transfer to afk",
    "afk_off": "Ok! you untransfer to afk",
    "afk_restored": "Your account has been restored from archive (AFK).\nSend your message again.",
    "afk_auto": (
        "You were moved to AFK by the system due to inactivity.\n"
        "You must send at least one message every {period}, your last message was on {last}."
    ),
    "tag_disabled_safety": "\n\nYour tag has been disabled for safety.",
    "leave_confirm": "Are you sure you want to leave the bot?\nIf yes, type /leave {id}.",
    "leave_done": "You left the bot. To return, type /start",
    "sending": "Sending…",
    "sent_ok": "Your message was successfully sent in {elapsed} to {count} users.",
    "sent_partial": "Your message was successfully sent in {elapsed} to {ok}/{total} users.",
    "sent_failed_head": "Not everyone received the message: {n} due to {reason}",
    "sent_flood": "(Flood wait occurred for {n} users with a wait time of: {waits} seconds)",
    "nobody": "There is no one else in the bot but you.",
    "slowmode": "Slowmode active. Please wait {left} seconds.",
    "type_disabled": "Sending this message type is disabled by the owner.",
    "duplicate": "You can repeat the same message in {left}.",
    "deleted_ok": "Your message was deleted for {count} users.",
    "delete_confirm": "Delete this message for everyone?",
    "edit_confirm": "Edit this message for all recipients?",
    "edited_ok": "Message edited for {count} users.",
    "edited_mark": "(edited message)",
    "msg_stub": "This message is too old — you can no longer reply to it or report it.",
    "not_your_msg": "This is not your message.",
    "pm_head": "Send an anonymous message to any user.",
    "pm_usage": "Reply with this command to a message and type your text.",
    "pm_sent": "Private message sent.",
    "pm_fail": "Delivery failed: the user blocked the bot or left.",
    "pm_blocked": "This user has blocked private messages from you.",
    "pm_closed": "The user has disabled private messages.",
    "pm_in_head": "You have received a new Anonymous message:",
    "pm_in_foot": "To reply, simply reply to this message.\n(Your username is hidden)",
    "pm_block_done": "User blocked, they can no longer write to your PM.",
    "pm_unblock_done": "User unblocked in PM.",
    "pm_block_cleared": "PM blocklist cleared.",
    "btn_pm_block": "Block User",
    "pm_block_empty": "PM blocklist is empty.",
    "pm_block_list": "Ignored in PM ({n}):\n{items}",
    "ignore_head": (
        "This command adds a person (by reply) to your ignore list.\n"
        "You will no longer see messages from them. You can always remove them.\n"
        "To unignore, use /unignore &lt;reply|#index|all&gt;\n\n"
        "Example: /ignore &lt;reply&gt;"
    ),
    "unignore_head": (
        "This command removes a person from your ignore list.\n"
        "You will see their messages again.\n\n"
        "Example: /unignore &lt;reply|#index|all&gt;"
    ),
    "ignore_added": "User added to ignore list. Total: {n}",
    "mode_tag": "with tag",
    "mode_anon": "anonymous",
    "ignore_exists": "This user is already in your ignore list.",
    "ignore_self": "You cannot ignore yourself.",
    "ignore_removed": "User removed from ignore list. Left: {n}",
    "ignore_cleared": "Ignore list cleared, removed: {n}",
    "ignore_empty": "Ignore list is empty.",
    "ignore_list": "Ignore list ({n}):\n{items}",
    "filter_head": (
        "Filters allow you to hide messages containing specific words or media.\n"
        "Add words to your filter, and matching messages won't be shown to you.\n\n"
        "To filter a word, specify it in arguments.\n"
        "To filter media, reply to a media message with this command.\n\n"
        "You can also use regex by enclosing the word in slashes (/)\n\n"
        "Examples:\n"
        "/filter test\n"
        "/filter /test\\d+/"
    ),
    "unfilter_head": "No arguments. Specify a word to remove it from filters, or use 'all' to clear everything.",
    "filter_added": "Added to filter ({kind}): {value}\nTotal filters: {n}",
    "filter_exists": "This filter already exists.",
    "filter_bad_regex": "Invalid regular expression.",
    "filter_removed": "Removed from filter: {value}. Left: {n}",
    "filter_not_found": "Filter not found.",
    "filter_cleared": "Filters cleared, removed: {n}",
    "filter_empty": "Filter list is empty.",
    "filter_list": "Your filters ({n}):\n{items}",
    "filter_need_media": "Reply to a message with media or specify a word.",
    "report_usage": "Reply with this command and specify the reason.",
    "report_sent": "Report sent to admins.",
    "report_cd": "Next report available in {left}.",
    "report_muted": "You are muted, reports are unavailable.",
    "report_self": "No need to report yourself.",
    "report_admin": (
        "#REPORT\n"
        "Target: {target} (ID {target_id})\n"
        "Reporter: {author} (ID {author_id})\n"
        "Reason: {reason}"
    ),
    "no_rights": "No rights.",
    "limit_reached": "Command limit reached: {used}/{limit} per day.",
    "need_reply": "You need to reply to a message.",
    "reply_unknown": "Could not find whose message this is. Reply directly to a user's message.",
    "target_not_found": "User not found.",
    "mute_usage": "Reply with: /mute &lt;time&gt; [reason]\nOr: /mute &lt;id&gt; &lt;time&gt; [reason]",
    "mute_bad_time": "Could not parse time. Examples: 30s, 15m, 3h, 7d, 1w, 1mo, 1y.",
    "mute_notice": "#MUTE\nYou have been muted for {duration}.",
    "mute_notice_reason": "#MUTE\nYou have been muted for {duration}.\n\nReason: {reason}",
    "mute_blocked": "{name} you are muted\nReturn in {left}. {until}",
    "mute_blocked_reason": (
        "{name} you are muted\n"
        "Reason: {reason}\n"
        "Return in {left}. {until}"
    ),
    "mute_done": "{target} muted for {duration}. Reason: {reason}",
    "unmute_notice": "#UNMUTE\nYou can write to the chat again.",
    "unmute_done": "{target} unmuted.",
    "not_muted": "User is not muted.",
    "mute_expired": "#UNMUTE\nMute expired, you can write again.",
    "warn_notice": "#WARN\nYou received a warning {n}/{limit}.\n\nReason: {reason}",
    "warn_done": "{target}: warning {n}/{limit}.",
    "unwarn_done": "{target}: warnings {n}/{limit}.",
    "warn_automute": "\n\nMuted for {duration} due to reaching {limit} warnings.",
    "pin_done": "Pinned for {count} users.",
    "unpin_done": "Unpinned for {count} users.",
    "settag_usage": (
        "Custom tag: /settag &lt;text&gt; | &lt;link&gt;\n"
        "Text only: /settag nickname\n"
        "With link: /settag nickname | https://t.me/digitkiss\n"
        "Reset: /settag"
    ),
    "settag_set": "Tag: {text}\nLink: {url}",
    "settag_off": "Custom tag reset.",
    "media_blocked": "You are restricted from sending media, text only.",
    "media_unblocked": "Media restriction removed.",
    "media_done": "{target}: media {state}.",
    "media_on": "disabled",
    "media_off": "enabled",
    "del_usage": "Reply with /del, or type: /del &lt;id&gt; &lt;count&gt;",
    "del_done": "Deleted messages: {msgs}, copies: {copies}.",
    "log_delete": "#DELETE\n{who}\nCopies removed: {count}",
    "del_notice": "#SYSTEM MESSAGE\nYour message was deleted by a moderator.",
    "deleted_broadcast": "This message was deleted for {count} users.",
    "tag_system": "#SYSTEM",
    "tag_deleted": "DELETED",
    "vote_usage": "Reply with: /votemute &lt;time&gt; [reason]",
    "vote_started": "Voting started, active for {minutes} min.",
    "vote_head": (
        "#VOTEMUTE\n"
        "Proposed mute: {target}\n"
        "Duration: {duration}\n"
        "Reason: {reason}\n"
        "Initiator: {author}\n\n"
        "Active for {minutes} min."
    ),
    "vote_voted": "Vote cast.",
    "vote_result_pass": "#VOTEMUTE\nVoting ended: {yes} for / {no} against. Mute applied.",
    "vote_result_fail": "#VOTEMUTE\nVoting ended: {yes} for / {no} against. Mute rejected.",
    "vote_no_staff": "No one to vote: no admins online.",
    "vote_over": "Voting ended.",
    "system_prefix": "#SYSTEM MESSAGE",
    "cmd_disabled": "Command disabled.",
    "unknown_cmd": "Unknown command. /help",
    "reply_mark": "#REPLY",
    "mention_mark": "#Mention",
    "who_usage": "Reply with /who, or type: /who &lt;id&gt;",
    "who_result": (
        "ID: {id}\n"
        "Username: {username}\n"
        "Name: {name}\n"
        "Role: {role}\n"
        "Registered: {joined}\n"
        "Messages: {msgs}"
    ),
    "sett_head": "Owner Panel. Version {version}.",
    "sett_echo": "Message Types",
    "sett_speed": "Speed and Limits",
    "sett_cmds": "Commands",
    "sett_admins": "Admins",
    "sett_misc": "Misc Settings",
    "sett_buttons": "Buttons and Prefixes",
    "sett_owner_only": "Panel accessible only to owner.",
    "set_usage": "/set &lt;key&gt; &lt;value&gt;",
    "set_done": "{key} = {value}",
    "admin_added": "{target} promoted to admin. Tag: {badge}",
    "admin_removed": "{target} demoted.",
    "admin_usage": "Reply with /promote, or type: /promote &lt;id&gt;",
    "mytag_usage": (
        "/mytag &lt;text&gt; — set custom tag\n"
        "/mytag &lt;text&gt; link — with profile link\n"
        "/mytag &lt;text&gt; nolink — without profile link\n"
        "/mytag off — reset"
    ),
    "mytag_set": "Custom tag: {text}\nProfile link: {link}",
    "mytag_off": "Custom tag reset, showing account name again.",
    "prefix_usage": "Reply with /prefix &lt;text&gt;",
    "prefix_set": "Prefix for {target}: {value}",
    "system_usage": "/system &lt;text&gt; — broadcast system message to all.",
    "system_done": "System message sent to {count} users.",
    "restarting": "Restarting…",
    "ask_value": (
        "Send a new value for <code>{key}</code> in the next message.\n"
        "To reset, send <code>-</code>. Any command cancels input."
    ),
    "ask_prefix": (
        "Send a new prefix for {target} in the next message.\n"
        "To restore default, send <code>-</code>."
    ),
    "value_saved": "Saved: <code>{key}</code> = {value}",
    "value_reset": "Reset: <code>{key}</code>",
}

LANGS = {"ru": "Русский", "en": "English"}


def t(lang: str, key: str, /, **kwargs) -> str:
    """
    lang и key — позиционные (после них стоит `/`), поэтому шаблон спокойно
    может принимать подстановку с именем key=, lang= и любым другим.
    """
    pack = EN if lang == "en" else RU
    value = pack.get(key) or RU.get(key, key)
    return value.format(**kwargs) if kwargs else value