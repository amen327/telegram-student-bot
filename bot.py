
import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# تحميل ملف الإكسل وإزالة الفراغات من أسماء الأعمدة
df = pd.read_excel("sabahi.xlsx")
df.columns = df.columns.str.strip()  # إزالة الفراغات من أسماء الأعمدة
df["كود الطالب"] = df["كود الطالب"].astype(str)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! أرسل كود الطالب الخاص بك للحصول على معلوماتك.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    result = df[df["كود الطالب"] == user_input]

    if not result.empty:
        row = result.iloc[0]
        name = row.get("اسم الطالب", "غير معروف")
        student_id = row.get("id", "غير معروف")
        password = row.get("الرقم السري", "غير معروف")

        response = (
            f"👤 *اسم الطالب:* {name}\n"
            f"🆔 *ID:* {student_id}\n"
            f"🔐 *الرمز السري:* {password}"
        )
    else:
        response = "❌ الكود غير صحيح، يرجى التحقق والمحاولة مرة أخرى."

    await update.message.reply_text(response, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token("7562170232:AAHQQbOlH5riNDm57vnItVFlqgRrSC0LPgI").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
