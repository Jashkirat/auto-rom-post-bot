import os
from telegram import Update, Bot, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
AUTHORIZED_USER_ID = 123456789  # Replace this with your actual Telegram user ID

(ROM_NAME, VERSION, ANDROID_VER, RELEASE_DATE, CHANGELOG_SRC, CHANGELOG_DEV, DOWNLOAD, SUPPORT, DONATE, SCREENSHOTS, BANNER, CONFIRM) = range(12)

user_data = {}

async def start_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("You are not authorized to use this bot.")
        return ConversationHandler.END
    await update.message.reply_text("Let's create a build post!\nWhat is the ROM name?")
    return ROM_NAME

async def rom_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['rom_name'] = update.message.text
    await update.message.reply_text("ROM version?")
    return VERSION

async def version(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['version'] = update.message.text
    await update.message.reply_text("Android version?")
    return ANDROID_VER

async def android_version(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['android'] = update.message.text
    await update.message.reply_text("Release date? (e.g., 17/05/25)")
    return RELEASE_DATE

async def release_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['date'] = update.message.text
    await update.message.reply_text("Changelog source link?")
    return CHANGELOG_SRC

async def changelog_source(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['changelog_src'] = update.message.text
    await update.message.reply_text("Changelog device link?")
    return CHANGELOG_DEV

async def changelog_device(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['changelog_dev'] = update.message.text
    await update.message.reply_text("Download link?")
    return DOWNLOAD

async def download_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['download'] = update.message.text
    await update.message.reply_text("Support group link?")
    return SUPPORT

async def support_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['support'] = update.message.text
    await update.message.reply_text("Donate link?")
    return DONATE

async def donate_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['donate'] = update.message.text
    await update.message.reply_text("Screenshots link?")
    return SCREENSHOTS

async def screenshots_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['screenshots'] = update.message.text
    await update.message.reply_text("Please upload the banner image.")
    return BANNER

async def receive_banner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    await file.download_to_drive("banner.jpg")
    user_data['banner'] = "banner.jpg"
    await update.message.reply_text("Banner received! Type 'yes' to confirm and post.")
    return CONFIRM

async def confirm_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.lower() != 'yes':
        await update.message.reply_text("Cancelled.")
        return ConversationHandler.END

    rom = user_data['rom_name'].replace(" ", "")
    msg = (
        f"#{rom} #spes #spesn #oss #A15 #QPR2 #Official\n"
        f"{user_data['rom_name']} | {user_data['version']} | {user_data['android']} | OFFICIAL\n"
        f"Released: {user_data['date']}’\n\n"
        f"▪️Changelog - [Source]({user_data['changelog_src']}) | [Device]({user_data['changelog_dev']})\n"
        f"▪️[Download]({user_data['download']})\n"
        f"▪️[Support Group]({user_data['support']})\n"
        f"▪️[Donate]({user_data['donate']})\n"
        f"▪️[Screenshots]({user_data['screenshots']})\n\n"
        f"*Notes:*\n"
        f"• Leica camera included\n"
        f"• Use official OrangeFox recovery\n"
        f"• Report bugs properly with logs and respectful behavior in the support group\n\n"
        f"*Credits:*\n"
        f"• All spes devs for device trees and sources\n\n"
        f"By @JassiV07\nFollow @JassiVBuilds\nJoin @JassiVBuildsSupport"
    )

    bot = Bot(token=BOT_TOKEN)
    with open("banner.jpg", 'rb') as img:
        await bot.send_photo(chat_id=CHAT_ID, photo=InputFile(img), caption=msg, parse_mode='Markdown')
    await update.message.reply_text("Post sent!")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("post", start_post)],
        states={
            ROM_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, rom_name)],
            VERSION: [MessageHandler(filters.TEXT & ~filters.COMMAND, version)],
            ANDROID_VER: [MessageHandler(filters.TEXT & ~filters.COMMAND, android_version)],
            RELEASE_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, release_date)],
            CHANGELOG_SRC: [MessageHandler(filters.TEXT & ~filters.COMMAND, changelog_source)],
            CHANGELOG_DEV: [MessageHandler(filters.TEXT & ~filters.COMMAND, changelog_device)],
            DOWNLOAD: [MessageHandler(filters.TEXT & ~filters.COMMAND, download_link)],
            SUPPORT: [MessageHandler(filters.TEXT & ~filters.COMMAND, support_link)],
            DONATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, donate_link)],
            SCREENSHOTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, screenshots_link)],
            BANNER: [MessageHandler(filters.PHOTO, receive_banner)],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_post)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    print("Bot is running...")
    app.run_polling()
