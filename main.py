import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, CallbackQueryHandler, filters
)
import aiohttp

# ✅ Your API keys
TELEGRAM_BOT_TOKEN = "7560709423:AAFLv-6ttNBBexyJ-_cL0HAiK0q3auKJyBw"
TOGETHER_API_KEY = "4b2232fefa1f67cadb417a8f338322a5e969e6d71bdb067b910f3600a07c2692"

# ✅ Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Main button menu
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("🤖 AI Chat", callback_data="ai")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")],
        [InlineKeyboardButton("👋 Welcome Message", callback_data="welcome")],
        [InlineKeyboardButton("😢 Goodbye Message", callback_data="goodbye")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ✅ /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Master Bot!\nSelect an option below:",
        reply_markup=get_main_menu()
    )

# ✅ /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 Available Commands:\n"
        "/start - Start the bot\n"
        "/help - Get help\n"
        "/ai - Chat with AI\n"
        "/welcome - Welcome message\n"
        "/goodbye - Goodbye message\n"
        "/menu - Show buttons"
    )

# ✅ AI Chat trigger command
async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💬 Send me your question now!")

# ✅ AI Message handler
async def handle_ai_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    if not user_input:
        return

    msg = await update.message.reply_text("🤖 Thinking...")

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.together.xyz/v1/chat/completions",
            json={
                "model": "meta-llama/Llama-3-8b-chat-hf",
                "messages": [{"role": "user", "content": user_input}],
                "temperature": 0.7
            },
            headers={"Authorization": f"Bearer {TOGETHER_API_KEY}"}
        ) as resp:
            data = await resp.json()
            response = data.get("choices", [{}])[0].get("message", {}).get("content", "❌ AI error occurred.")
            await msg.edit_text(f"🤖 {response}")

# ✅ /welcome command
async def welcome_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Glad you're here.")

# ✅ /goodbye command
async def goodbye_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Goodbye! See you next time.")

# ✅ /menu command
async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 Here’s the main menu:", reply_markup=get_main_menu())

# ✅ Button callback handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "ai":
        await query.message.reply_text("💬 Send me your question now!")
    elif data == "help":
        await query.message.reply_text(
            "🛠 Available Commands:\n"
            "/start - Start the bot\n"
            "/help - Get help\n"
            "/ai - Chat with AI\n"
            "/welcome - Welcome message\n"
            "/goodbye - Goodbye message\n"
            "/menu - Show buttons"
        )
    elif data == "welcome":
        await query.message.reply_text("👋 Welcome! Glad you're here.")
    elif data == "goodbye":
        await query.message.reply_text("👋 Goodbye! See you next time.")

# ✅ Main bot function
def main():
    # Switch to Application class for newer versions of python-telegram-bot
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ai", ai_command))
    app.add_handler(CommandHandler("welcome", welcome_command))
    app.add_handler(CommandHandler("goodbye", goodbye_command))
    app.add_handler(CommandHandler("menu", show_menu))

    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_ai_message))

    logger.info("✅ Master Bot is running with all features...")
    app.run_polling()

if __name__ == "__main__":
    main()
