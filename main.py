from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import logging
from keep_alive import keep_alive
import os, time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CRYPTO_CHANNEL_ID = -1002687727934  # کانال کریپتو رایگان
FOREX_CHANNEL_ID = -1002519930114  # کانال VIP فارکس ✅ جدید

waiting_for_uid = {}

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
    user_id = query.from_user.id

    try:
        if data == 'contact':
            keyboard = [
                [InlineKeyboardButton("📷 اینستاگرام", url='https://www.instagram.com/trading_duos?igsh=MWZic3Y1Z3ZsZmhzZA%3D%3D&utm_source=qr')],
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
                "⚠️ شما باید در سیگنال‌ها، مدیریت سرمایه و ریسک منیجمنت را رعایت کنید.\nاگر کال یا لیکویید شدید، ما هیچ مسئولیتی قبول نمی‌کنیم.",
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
                [InlineKeyboardButton("💎 عضویت VIP کریپتو (به‌زودی)", callback_data='crypto_vip')],
                [InlineKeyboardButton("🔙 بازگشت", callback_data='signals')]
            ]
            await query.edit_message_text("📊 انتخاب نوع عضویت در سیگنال کریپتو:", reply_markup=InlineKeyboardMarkup(keyboard))

        elif data == 'crypto_vip':
            await query.edit_message_text("💎 عضویت VIP کریپتو به زودی افتتاح خواهد شد!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data='crypto')]]))

        elif data == 'toobit':
            waiting_for_uid[user_id] = 'crypto'
            keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data='crypto_free')]]
            await query.edit_message_text(
                "📌 لطفاً ابتدا از طریق لینک زیر در صرافی Toobit با کد رفرال ما ثبت‌نام کنید:\n\n🔗 https://www.toobit.com/\nکد رفرال: giWAS2\n\nسپس UID خود را برای ما بفرستید:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        elif data == 'lbank_crypto':
            waiting_for_uid[user_id] = 'crypto'
            keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data='crypto_free')]]
            await query.edit_message_text(
                "📌 ثبت‌نام در صرافی LBank به‌زودی با کد رفرال اختصاصی ما فعال خواهد شد.\n\nفعلاً UID خود را بعد از ثبت‌نام ارسال نمایید:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        elif data == 'crypto_free':
            keyboard = [
                [InlineKeyboardButton("ثبت‌نام در Toobit", callback_data='toobit')],
                [InlineKeyboardButton("ثبت‌نام در LBank", callback_data='lbank_crypto')],
                [InlineKeyboardButton("🔙 بازگشت", callback_data='crypto')]
            ]
            await query.edit_message_text(
                "🎁 برای عضویت رایگان کریپتو:\nلطفاً یکی از صرافی‌های زیر را انتخاب کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        elif data == 'forex_vip':
            try:
                invite_link = await context.bot.create_chat_invite_link(
                    chat_id=FOREX_CHANNEL_ID,
                    member_limit=1,
                    expire_date=int(time.time()) + 60
                )
                await query.edit_message_text(
                    f"💎 عضویت VIP فارکس رایگان فعال شد! روی لینک زیر بزنید تا وارد شوید (اعتبار: ۶۰ ثانیه):\n{invite_link.invite_link}",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data='signals')]])
                )
            except Exception as e:
                logger.error(f"خطا در ساخت لینک دعوت فارکس: {e}")
                await query.edit_message_text("❌ خطا در ساخت لینک عضویت. لطفاً دوباره تلاش کن.")

        elif data == 'start':
            await start(update, context)

    except Exception as e:
        logger.error(f"خطا در button_handler: {e}")
        await query.edit_message_text("❌ مشکلی پیش اومده. دوباره تلاش کن.")

async def uid_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    uid_type = waiting_for_uid.get(user_id)

    if uid_type:
        del waiting_for_uid[user_id]
        try:
            invite_link = await context.bot.create_chat_invite_link(
                chat_id=CRYPTO_CHANNEL_ID,
                member_limit=1,
                expire_date=int(time.time()) + 60
            )
            await update.message.reply_text(
                f"✅ UID دریافت شد! برای عضویت روی لینک زیر بزنید (تا ۶۰ ثانیه معتبره):\n{invite_link.invite_link}"
            )
        except Exception as e:
            logger.error(f"خطا در ساخت لینک دعوت کریپتو: {e}")
            await update.message.reply_text("❌ خطا در ساخت لینک عضویت. لطفاً دوباره تلاش کنید.")

if __name__ == '__main__':
    keep_alive()
    print("✅ ربات روشن شد.")
    try:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(button_handler))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), uid_handler))
        app.run_polling()
    except Exception as e:
        logger.error(f"❌ خطا در اجرای اصلی ربات: {e}")
