import aikopanel_bot
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


desc = 'Mở liên kết trang web'
config = aikopanel_bot.config['bot']


def getContent():
    text = '🗺*Đi đến trang web*\n\n🌐Nhấn vào nút bên dưới để đi đến địa chỉ trang web'
    text += '\nBạn có thể quét mã QR bên trên để truy cập trang web'
    keyboard = [[InlineKeyboardButton(
        text='Mở trang web', url="%s" % config['website'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return text, reply_markup


async def autoDelete(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.delete_message(job.chat_id, job.data)


async def exec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    chat_id = msg.chat_id
    chat_type = update.effective_chat.type
    if chat_type == 'private' or chat_id == config['group_id']:
        text, reply_markup = getContent()
        # Send the QR code image with caption
        with open(os.path.join(".", "image", "qrweb.jpg"), 'rb') as photo:
            await context.bot.send_photo(chat_id, photo, caption=text, reply_markup=reply_markup)
        if chat_type != 'private':
            context.job_queue.run_once(
                autoDelete, 300, data=msg.id, chat_id=chat_id, name=str(msg.id))