import qrcode
import qrcode.constants
from io import BytesIO
import aikopanel_bot
from handler import MysqlUtils
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

desc = 'Lấy liên kết đăng ký của tôi'
config = aikopanel_bot.config['bot']


def generate_qr_code(url):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")
    byte_stream = BytesIO()
    image.save(byte_stream, format='PNG')
    byte_stream.seek(0)

    return byte_stream


def getContent(token):
    header = '📚*Liên kết đăng ký*\n\n🔮Địa chỉ đăng ký chung là (bấm vào để sao chép)：\n'
    tolink = '`%s/api/v1/client/subscribe?token=%s`' % (
        config['sublink'], token)
    qrlink = '%s/api/v1/client/subscribe?token=%s' % (
        config['sublink'], token)
    qrlink += '&flag=aiko'
    qr_code = generate_qr_code(qrlink)
    buttom = '\n\n⚠️*Nếu liên kết đăng ký bị rò rỉ, vui lòng truy cập trang web chính thức để đặt lại!*'
    keyboard = []
    text = f'{header}{tolink}{buttom}'
    reply_markup = InlineKeyboardMarkup(keyboard)

    return text, qr_code, reply_markup


async def autoDelete(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.delete_message(job.chat_id, job.data)


async def exec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    user_id = msg.from_user.id
    chat_id = msg.chat_id
    chat_type = msg.chat.type
    if chat_type == 'private':
        db = MysqlUtils()
        user = db.sql_query(
            'SELECT token FROM v2_user WHERE `telegram_id` = %s' % user_id)
        db.close()
        if len(user) > 0:
            text, qr_code, reply_markup = getContent(user[0][0])
            await msg.reply_photo(qr_code, caption=text, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await msg.reply_markdown('❌*Lỗi*\n, bạn chưa buộc tài khoản của mình!')
    else:
        if chat_id == config['group_id']:
            callback = await msg.reply_markdown('❌*Lỗi*\nĐể bảo mật tài khoản của bạn, xin vui lòng nói về tôi một cách riêng tư!')
            context.job_queue.run_once(
                autoDelete, 300, data=msg.id, chat_id=chat_id, name=str(msg.id))
            context.job_queue.run_once(
                autoDelete, 300, data=callback.message_id, chat_id=chat_id, name=str(callback.message_id))
