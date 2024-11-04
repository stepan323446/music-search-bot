from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from music_services.base import Track
from music_services.deezer import Deezer

BOT_TOKEN = '7402965953:AAHlVTpVNtUa1Whvq1sz81cEw-3JBAx77uI'

SERVICES_ENABLED = (
    Deezer(),
)

async def reply_answer_from_bot(origin_track: Track,
                                service_tracks: list[Track], 
                                update: Update, 
                                context: ContextTypes.DEFAULT_TYPE):
    
    
    await update.message.reply_text(
        f"""
<b>Track: {origin_track.name}</b>
<i>Authors: {", ".join(origin_track.authors)}</i>

<b>Other services:</b>

""", 
        ParseMode.HTML)

def get_search_query(track: Track):
    return f'{track.name} {track.authors[0]}'