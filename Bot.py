import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен бота (замените на ваш)
BOT_TOKEN = "8491171457:AAG2ZaQ5vJJzmKw4-oc482fsIgQk0-0N21I"

# Ссылки (замените на ваши)
INSTRUCTION_CHANNEL_URL = "https://t.me/your_instruction_channel"
VIP_SERVER_URL = "https://roblox.com.py/games/126884695634066/Grow-a-Garden?privateServerLinkCode=45493874925927451576244822459786	"
BOT_PROFILE_URL = "https://roblox.com.py/users/1201171802/profile"	
TUTORIAL_URL = "https://youtube.com/your-tutorial"
DEFAULT_PHOTO_URL = "https://example.com/default-photo.jpg"

# Список питомцев (название и URL фото)
PETS = [
    {"name": "🐉 Огненный дракон", "photo": "https://example.com/dragon.jpg"},
    {"name": "🦄 Волшебный единорог", "photo": "https://example.com/unicorn.jpg"},
    {"name": "🐺 Ледяной волк", "photo": "https://example.com/wolf.jpg"},
    {"name": "🦅 Громовая птица", "photo": "https://example.com/bird.jpg"},
    {"name": "🐢 Золотая черепаха", "photo": "https://example.com/turtle.jpg"},
]

# Эмодзи для оформления
EMOJI = {
    "welcome": "👋",
    "pet": "🎁",
    "referral": "📊",
    "back": "⬅️",
    "next": "➡️",
    "get": "✅",
    "vip": "⭐",
    "friend": "👥",
    "server": "🎮",
    "profile": "👤",
    "tutorial": "📚"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    keyboard = [
        [
            InlineKeyboardButton(f"{EMOJI['tutorial']} Инструкция", url=INSTRUCTION_CHANNEL_URL),
        ],
        [
            InlineKeyboardButton(f"{EMOJI['pet']} Получить пета", callback_data="get_pet"),
            InlineKeyboardButton(f"{EMOJI['referral']} Моя реф. ссылка", callback_data="referral"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""{EMOJI['welcome']} *Добро пожаловать в Roblox бесплатные питомцы*

🎉 *Получи любого питомца за подписку на канал*

👇 *Выбери действие ниже:*"""
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "get_pet":
        await show_pet(query, context, 0)
    elif data == "referral":
        await show_referral(query)
    elif data.startswith("pet_"):
        pet_index = int(data.split("_")[1])
        await show_pet(query, context, pet_index)
    elif data.startswith("take_"):
        pet_index = int(data.split("_")[1])
        await show_get_methods(query, context, pet_index)
    elif data.startswith("vip_"):
        pet_index = int(data.split("_")[1])
        await show_vip_method(query, pet_index)
    elif data.startswith("friend_"):
        pet_index = int(data.split("_")[1])
        await show_friend_method(query, pet_index)
    elif data == "back_to_start":
        await back_to_start(query)

async def show_pet(query, context, pet_index: int) -> None:
    """Показать питомца с кнопками навигации"""
    pet = PETS[pet_index % len(PETS)]
    
    keyboard = [
        [
            InlineKeyboardButton(f"{EMOJI['get']} Забрать этого", callback_data=f"take_{pet_index}"),
            InlineKeyboardButton(f"{EMOJI['next']} Следующий", callback_data=f"pet_{(pet_index + 1) % len(PETS)}"),
        ],
        [
            InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="back_to_start"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    pet_text = f"""🎁 *{pet['name']}*

✨ Этот удивительный питомец ждет своего хозяина!"""
    
    try:
        await query.edit_message_media(
            media=InputMediaPhoto(media=pet['photo'], caption=pet_text, parse_mode='Markdown'),
            reply_markup=reply_markup
        )
    except:
        await query.edit_message_text(
            text=pet_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def show_referral(query) -> None:
    """Показать реферальную ссылку"""
    keyboard = [
        [InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="back_to_start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    referral_text = f"""📊 *Моя реферальная ссылка*

🔗 `https://t.me/your_bot?start=ref{query.from_user.id}`

📢 Приглашай друзей и получай бонусы!"""
    
    await query.edit_message_text(
        text=referral_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_get_methods(query, context, pet_index: int) -> None:
    """Показать методы получения питомца"""
    keyboard = [
        [
            InlineKeyboardButton(f"{EMOJI['vip']} Получить пета на VIP-сервере бота", 
                               callback_data=f"vip_{pet_index}"),
        ],
        [
            InlineKeyboardButton(f"{EMOJI['friend']} Добавить бота в друзья", 
                               callback_data=f"friend_{pet_index}"),
        ],
        [
            InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data=f"pet_{pet_index}"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    methods_text = f"""🎯 *Выберите метод получения:*

⭐ *VIP-сервер* - Быстро и удобно
👥 *Добавить в друзья* - Альтернативный способ"""
    
    await query.edit_message_text(
        text=methods_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_vip_method(query, pet_index: int) -> None:
    """Показать метод получения через VIP-сервер"""
    keyboard = [
        [
            InlineKeyboardButton(f"{EMOJI['server']} Зайти на сервер", url=VIP_SERVER_URL),
            InlineKeyboardButton(f"{EMOJI['tutorial']} Туториал", url=TUTORIAL_URL),
        ],
        [
            InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data=f"take_{pet_index}"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    vip_text = f"""⭐ *Получить пета на VIP-сервере бота*

Чтобы получить своего питомца зайдите на вип сервер к боту. 
Бот ждет вас *в специальной зоне выдачи*.

📸 *Фото локации:*"""
    
    try:
        await query.edit_message_media(
            media=InputMediaPhoto(media=DEFAULT_PHOTO_URL, caption=vip_text, parse_mode='Markdown'),
            reply_markup=reply_markup
        )
    except:
        await query.edit_message_text(
            text=vip_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def show_friend_method(query, pet_index: int) -> None:
    """Показать метод получения через добавление в друзья"""
    keyboard = [
        [
            InlineKeyboardButton(f"{EMOJI['profile']} Перейти к профилю бота", url=BOT_PROFILE_URL),
            InlineKeyboardButton(f"{EMOJI['tutorial']} Туториал", url=TUTORIAL_URL),
        ],
        [
            InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data=f"take_{pet_index}"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    friend_text = f"""👥 *Добавить бота в друзья*

Чтобы получить своего питомца добавьте бота в друзья и зайдите к нему на сервер. 
Бот ждет вас *в специальной зоне выдачи*.

📸 *Фото локации:*"""
    
    try:
        await query.edit_message_media(
            media=InputMediaPhoto(media=DEFAULT_PHOTO_URL, caption=friend_text, parse_mode='Markdown'),
            reply_markup=reply_markup
        )
    except:
        await query.edit_message_text(
            text=friend_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def back_to_start(query) -> None:
    """Вернуться к начальному меню"""
    keyboard = [
        [
            InlineKeyboardButton(f"{EMOJI['tutorial']} Инструкция", url=INSTRUCTION_CHANNEL_URL),
        ],
        [
            InlineKeyboardButton(f"{EMOJI['pet']} Получить пета", callback_data="get_pet"),
            InlineKeyboardButton(f"{EMOJI['referral']} Моя реф. ссылка", callback_data="referral"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""{EMOJI['welcome']} *Добро пожаловать в Roblox бесплатные питомцы*

🎉 *Получи любого питомца за подписку на канал*

👇 *Выбери действие ниже:*"""
    
    await query.edit_message_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def main() -> None:
    """Запуск бота"""
    # Создаем Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Запускаем бота
    print("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()