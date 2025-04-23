from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import logging
from keep_alive import keep_alive
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📞 ارتباط با ما", callback_data='contact')],
        [InlineKeyboardButton("📢 کانال‌های سیگنال ما", callback_data='signals_warning')]
    ]
    if update.message:
        await update.message.reply_text(
            "سلام! به ربات سیگنال خوش اومدی 🌟 لطفاً یکی از گزینه‌های زیر رو انتخاب کن:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            "سلام! به ربات سیگنال خوش اومدی 🌟 لطفاً یکی از گزینه‌های زیر رو انتخاب کن:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    try:
        if data == 'contact':
            keyboard = [
                [InlineKeyboardButton("📷 اینستاگرام", url='https://www.instagram.com/moamir_tradegroup')],
                [InlineKeyboardButton("🎮 دیسکورد", url='https://discord.gg/ZZBhyBhf')],
                [InlineKeyboardButton("🔙 بازگشت", callback_data='start')]
            ]
            await query.edit_message_text("📩 راه‌های ارتباط با ما:", reply_markup=InlineKeyboardMarkup(keyboard))

        elif data == 'signals_warning':
            keyboard = [
                [InlineKeyboardButton("✅ موافقم", callback_data='signals')],
                [InlineKeyboardButton("❌ مخالفم", callback_data='start')]
            ]
            await query.edit_message_text(
                """⚠️ شما باید در سیگنال‌ها، مدیریت سرمایه و ریسک منیجمنت را رعایت کنید.
اگر کال یا لیکویید شدید، ما هیچ مسئولیتی قبول نمی‌کنیم.""",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        elif data == 'signals':
            keyboard = [
                [InlineKeyboardButton("💱 سیگنال فارکس (VIP)", callback_data='forex_vip')],
                [InlineKeyboardButton("🪙 سیگنال کریپتو", callback_data='crypto')],
                [InlineKeyboardButton("🔙 بازگشت", callback_data='start')]
            ]
            await query.edit_message_text("📢 کانال‌های سیگنال ما:", reply_markup=InlineKeyboardMarkup(keyboard))

        elif data == 'crypto':
            keyboard = [
                [InlineKeyboardButton("🎁 عضویت رایگان کریپتو", callback_data='crypto_free')],
                [InlineKeyboardButton("💎 عضویت VIP کریپتو", callback_data='crypto_vip')],
                [InlineKeyboardButton("🔙 بازگشت", callback_data='signals')]
            ]
            await query.edit_message_text("📊 انتخاب نوع عضویت در سیگنال کریپتو:", reply_markup=InlineKeyboardMarkup(keyboard))

        elif data == 'crypto_vip':
            keyboard = [
                [InlineKeyboardButton("ثبت‌نام در Toobit", callback_data='toobit')],
                [InlineKeyboardButton("ثبت‌نام در LBank", callback_data='lbank')],
                [InlineKeyboardButton("🔙 بازگشت", callback_data='crypto')]
            ]
            await query.edit_message_text("صرافی مورد نظر رو انتخاب کن:", reply_markup=InlineKeyboardMarkup(keyboard))

        elif data == 'toobit':
            keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data='crypto_vip')]]
            await query.edit_message_text(
                """📌 ابتدا با این لینک در Toobit ثبت‌نام کن:
https://www.toobit.com/
کد رفرال: giWAS2

✅ لطفاً UID اکانتی که با رفرال ما ثبت‌نام کردید رو همینجا بفرستید.""",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            await query.message.reply_text("✅ UID دریافت شد! تیم ما بررسی می‌کند و شما را به کانال VIP اضافه خواهد کرد.")

        elif data == 'lbank':
            keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data='crypto_vip')]]
            await query.edit_message_text(
                """📌 ابتدا با این لینک در LBank ثبت‌نام کن:
https://www.lbank.com/
کد رفرال: به‌زودی اضافه میشه...

✅ لطفاً UID اکانتی که با رفرال ما ثبت‌نام کردید رو همینجا بفرستید.""",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            await query.message.reply_text("✅ UID دریافت شد! تیم ما بررسی می‌کند و شما را به کانال VIP اضافه خواهد کرد.")

        elif data == 'crypto_free':
            keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data='crypto')]]
            await query.edit_message_text(
                """🎁 برای عضویت رایگان:
لطفاً ابتدا در یکی از صرافی‌های زیر با کد رفرال ما ثبت‌نام کن:

🔗 Toobit: https://www.toobit.com/  (کد رفرال: giWAS2)
🔗 LBank: https://www.lbank.com/

سپس UID خودتو همینجا بفرست تا بررسی کنیم. اگه تایید شدی، با افتخار به کانال رایگان اضافه‌ت می‌کنیم!""",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        elif data == 'forex_vip':
            keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data='signals')]]
            await query.edit_message_text(
                """برای عضویت VIP فارکس لطفاً ابتدا پرداخت را از طریق لینک زرین‌پال انجام دهید.
پس از پرداخت، ما با شما جهت عضویت در کانال VIP تماس می‌گیریم.""",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        elif data == 'start':
            await start(update, context)

    except Exception as e:
        logger.error(f"خطا در button_handler: {e}")
        await query.edit_message_text("یه مشکلی پیش اومده. لطفاً دوباره امتحان کن.")

if __name__ == '__main__':
    keep_alive()
    print("✅ ربات روشن شد.")
    try:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(button_handler))
        app.run_polling()
    except Exception as e:
        logger.error(f"❌ خطا در اجرای اصلی ربات: {e}")
