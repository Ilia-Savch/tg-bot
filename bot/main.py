from application.core.models.post import TgPost
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from bot.db import SessionLocal

import os

TOKEN = os.getenv("BOT_TOKEN")

async def get_all_posts():
    async with SessionLocal() as session:
        result = await session.execute(TgPost.__table__.select())
        return result.fetchall()

async def get_post_by_id(post_id):
    async with SessionLocal() as session:
        result = await session.execute(TgPost.__table__.select().where(TgPost.id == post_id))
        return result.first()

async def posts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    posts = await get_all_posts()
    if not posts:
        await update.message.reply_text("Постов пока нет.")
        return

    keyboard = [
        [InlineKeyboardButton(post.title, callback_data=f"post_{post.id}")]
        for post in posts
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите пост:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("post_"):
        post_id = int(query.data.split("_")[1])
        post = await get_post_by_id(post_id)
        if post:
            await query.edit_message_text(
                text=f"**{post.title}**\n\n{post.text}\n\n {post.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
                parse_mode="Markdown"
            )
        else:
            await query.edit_message_text("Пост не найден.")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Используйте команду /posts чтобы получить список постов.")


def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("posts", posts_command))
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling()

if __name__ == "__main__":
    main()
