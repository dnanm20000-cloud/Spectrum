import os
import asyncio
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# التُّوكِنُ الْخَاصُّ بِكَ
TOKEN = "8630383826:AAFdjn_RWyrFsBenPH2sO0Z_N6m1_I3w0E4"

# جُمْلَةُ التَّحَقُّقِ
REQUIRED_PHRASE = "اللهم صل على سيدنا محمد وعلى اله وصحبه"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """رِسَالَةُ التَّرْحِيبِ"""
    await update.message.reply_text(
        "أَهْلًا بِكَ فِي بُوتِ سْبِيكْتْرُوم 👋\n\n"
        "أَقُومُ بِتَحْمِيلِ الْفِيدِيُو لَكَ، أَرْسِلِ الرَّابِطَ أَوَّلًا 🚀"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    if not url.startswith(("http://", "https://")):
        await update.message.reply_text("الرَّجَاءُ إِرْسَالُ رَابِطِ فِيدِيُو صَحِيحٍ ⚠️")
        return

    status_msg = await update.message.reply_text("جَارٍِي تَحْمِيلُ الْفِيدِيُو، انْتَظِرْ قَلِيلًا... ⏳")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        # التَّحْمِيلُ بِاسْتِخْدَامِ yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # إِرْسَالُ الْفِيدِيُو
        if os.path.exists('video.mp4'):
            with open('video.mp4', 'rb') as video:
                await update.message.reply_video(video=video, caption=REQUIRED_PHRASE)
            os.remove('video.mp4')
        
        await status_msg.delete()

    except Exception as e:
        await update.message.reply_text(f"حَدَثَ خَطَأٌ: {str(e)}")

if __name__ == "__main__":
    print("--- الْبُوتُ يَعْمَلُ الآنَ عَلَى Termux ---")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.VIDEO | filters.PHOTO | filters.Document.ALL, lambda u, c: None))
    application.run_polling()
