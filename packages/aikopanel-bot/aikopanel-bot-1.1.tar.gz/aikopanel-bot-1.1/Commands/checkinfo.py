import aikopanel_bot
import time
from handler import MysqlUtils
from telegram import Update
from telegram.ext import ContextTypes

desc = 'Trả lời một người để lấy thông tin sử dụng'
config = aikopanel_bot.config['bot']
configid = aikopanel_bot.config['aikopanel']['idapple']


def onQuery(sql):
    try:
        db = MysqlUtils()
        result = db.sql_query(sql)
    finally:
        db.close()
        return result


def getContent(user):
    text = '📋*Thông tin cá nhân*\n'
    User_id = user[0]
    Register_time = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(user[1]))
    Plan_id = onQuery('SELECT name FROM v2_plan WHERE id = %s' %
                      user[2])[0][0]
    Expire_time = 'Không giới hạn'
    if user[3] is not None:
        Expire_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(user[3]))
    Data_Time = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(user[7]))
    CountgetIDapple = onQuery('Select count_idapple From v2_user Where id = %s' % User_id)[0][0]

    text = f'{text}\n🎲*ID：* {User_id}'
    text = f'{text}\n⌚️*Thời gian đăng ký：* {Register_time}'
    if Plan_id != '':
        text = f'{text}\n📚*Tên gói：* {Plan_id}'
        text = f'{text}\n📌*Thời gian hết hạn：* {Expire_time}'
        if Plan_id in configid['plan_limit']['plan_unlimit']:
            text = f'{text}\n🍎*Số Lần lấy IDApple：* ∞'
        else:
            text = f'{text}\n🍎*Số Lần lấy IDApple：* {CountgetIDapple} Lần/Tháng'
        text = f'{text}\n'
        text = f'{text}\n📊*Lần sử dụng cuối cùng：* {Data_Time}'
    else:
        text = f'{text}\n📚*Gói Của Bạn：* Chưa Mua Gói'
    return text


async def autoDelete(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.delete_message(job.chat_id, job.data)


async def exec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    chat_id = msg.chat_id
    chat_type = msg.chat.type

    if chat_type == 'private' or chat_id == config['group_id']:
        if msg.reply_to_message:
            reply_id = msg.reply_to_message.from_user.id
            user = onQuery(
                'SELECT id,created_at,plan_id,expired_at,u,d,transfer_enable,t FROM v2_user WHERE `telegram_id` = %s' % reply_id)
            if len(user) > 0:
                if user[0][2] is not None:
                    text = getContent(user[0])
                    callback = await msg.reply_markdown(text)
                else:
                    callback = await msg.reply_markdown('❌*Lỗi*\nTài khoản này chưa mua gói đăng ký!')
            else:
                callback = await msg.reply_markdown('❌*Lỗi*\nNgười dùng này chưa liên kết tài khoản Telegram')
        else:
            callback = await msg.reply_markdown('❌*Lỗi*\nBạn cần trả lời một tin nhắn để lấy thông tin!')
        if chat_type != 'private':
            context.job_queue.run_once(
                autoDelete, 300, data=msg.id, chat_id=chat_id, name=str(msg.id))
            context.job_queue.run_once(
                autoDelete, 300, data=callback.message_id, chat_id=chat_id, name=str(callback.message_id))

    else:
        await msg.reply_markdown('❌*Lỗi*\nBạn không thể sử dụng lệnh này!')
