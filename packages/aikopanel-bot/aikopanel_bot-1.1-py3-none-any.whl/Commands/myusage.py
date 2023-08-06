import aikopanel_bot
import time
import pytz
import datetime
from handler import MysqlUtils
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

desc = 'Lấy thông tin sử dụng của tôi'
config = aikopanel_bot.config['bot']


def onQuery(sql):
    try:
        db = MysqlUtils()
        result = db.sql_query(sql)
    finally:
        db.close()
        return result


def getContent(uid):
    tz = pytz.timezone('Asia/Ho_Chi_Minh')
    current_date = datetime.datetime.now(tz).strftime("%d-%m-%Y")
    stat = onQuery(
        'SELECT record_at,u,d FROM v2_stat_user WHERE `user_id` = %s' % uid)
    today_usage = 0
    for i in stat:
        today_date = i[0]
        ltime = time.gmtime(today_date + 28800)
        today_date = time.strftime("%d-%m-%Y", ltime)
        if today_date == current_date:
            today_usage = today_usage + i[1] + i[2]
    today_usage = round(today_usage / 1024 / 1024 / 1024, 2)

    text = f'📚*Lưu lượng hôm nay*\n\n📈Tổng lưu lượng sử dụng hôm nay là: *{today_usage} GB*\n'
    text = f'{text}\n📜*Nhấn vào nút bên dưới để xem chi tiết lưu lượng*'
    keyboard = [[InlineKeyboardButton(
        text='Chi tiết lưu lượng', url="%s/#/traffic" % config['website'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    return text, reply_markup


async def autoDelete(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.delete_message(job.chat_id, job.data)


async def exec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    user_id = msg.from_user.id
    chat_id = msg.chat_id
    chat_type = msg.chat.type
    user = onQuery(
        'SELECT id,u,d FROM v2_user WHERE `telegram_id` = %s' % user_id)
    if chat_type == 'private' or chat_id == config['group_id']:
        if len(user) > 0:
            if user[0][1] != 0 and user[0][2] != 0:
                text, reply_markup = getContent(user[0][0])
                callback = await msg.reply_markdown(text, reply_markup=reply_markup)
            else:
                callback = await msg.reply_markdown('❌*Lỗi*\nBạn chưa sử dụng lưu lượng nào!')
        else:
            callback = await msg.reply_markdown('❌*Lỗi*\nBạn chưa liên kết tài khoản!')
        if chat_type != 'private':
            context.job_queue.run_once(
                autoDelete, 300, data=msg.id, chat_id=chat_id, name=str(msg.id))
            context.job_queue.run_once(
                autoDelete, 300, data=callback.message_id, chat_id=chat_id, name=str(callback.message_id))
