
import asyncio
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("8747500121:AAEMkJOEvKR1mJSOCX3iThfyGfkVjjp2gcA")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bhai ka bot online hai! ❤️")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Bot start\n"
        "/help - Commands\n"
        "/ping - Bot status\n"
        "/userinfo - Apni info\n"
        "/rules - Group rules\n"
        "/spam - Test messages\n"
        "/stop - Test band"
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong! 🏓 Bot online hai.")

async def userinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Name: {user.full_name}\nUser ID: {user.id}"
    )

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Group Rules:\n1. Sabki respect karo.\n"
        "2. Spam mat karo.\n3. Rules follow karo."
    )

async def spam_loop(chat_id, app, chat_data):
    try:
        for i in range(1, 11):
            await app.bot.send_message(
                chat_id=chat_id,
                text=f"Test message {i}/10 🤖"
            )
            await asyncio.sleep(3)
    except asyncio.CancelledError:
        pass
    finally:
        chat_data.pop("spam_task", None)

async def spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        await update.message.reply_text(
            "Ye command sirf personal chat mein chalegi."
        )
        return

    task = context.chat_data.get("spam_task")
    if task and not task.done():
        await update.message.reply_text("Test pehle se chal raha hai!")
        return

    context.chat_data["spam_task"] = (
        context.application.create_task(
            spam_loop(
                update.effective_chat.id,
                context.application,
                context.chat_data
            )
        )
    )
    await update.message.reply_text("Test shuru! /stop se rok sakte ho.")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task = context.chat_data.get("spam_task")
    if task and not task.done():
        task.cancel()
        await update.message.reply_text("Test rok diya, bhai! 🛑")
    else:
        await update.message.reply_text("Koi test nahi chal raha.")

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable set nahi hai.")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("userinfo", userinfo))
    app.add_handler(CommandHandler("rules", rules))
    app.add_handler(CommandHandler("spam", spam))
    app.add_handler(CommandHandler("stop", stop))

    print("Bot start ho raha hai...")
    app.run_polling()

if __name__ == "__main__":
    main()
