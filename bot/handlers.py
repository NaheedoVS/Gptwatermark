from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from .config import settings
from .storage import storage
from .watermark import save_user_image, apply_image_watermark, apply_text_watermark
from .utils import LOG, remove_file, validate_crf
import os
import asyncio


async def register_handlers(app: Client):


@app.on_message(filters.command('start'))
async def start(_, message: Message):
await message.reply_text('Hi! Send me a video to watermark, or /help for commands.')


@app.on_message(filters.command('setwatermark') & filters.private)
async def set_wm(_, message: Message):
if not message.reply_to_message or not message.reply_to_message.photo and not message.reply_to_message.document:
await message.reply_text('Reply to an image (PNG/JPG) with /setwatermark')
return
# downloa
