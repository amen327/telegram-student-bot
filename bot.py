
import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# تحميل ملف الإكسل مرة واحدة
df = pd.read_excel("sabahi.xlsx")
df["كود الطالب"] = df["كود الطالب"].astype(str)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! أرسل كود الطالب الخاص بك للحصول على معلوماتك.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    result = df[df["كود الطالب"] == user_input]

    if not result.empty:
        row = result.iloc[0]
        name = row["اسم الطالب"]
        student_id = row["id"]
        password = row["الرقم السري"]

        response = (
            f"👤 *اسم الطالب:* {name}\n"
            f"🆔 *ID:* {student_id}\n"
            f"🔐 *الرمز السري:* {password}"
        )
    else:
        response = "❌ الكود غير صحيح، يرجى التحقق والمحاولة مرة أخرى."

    await update.message.reply_text(response, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token("7923983055:AAEc9j_hGp1Qq_3ehoaVSPXP2LKNBlk9oMw").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
