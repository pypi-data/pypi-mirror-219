import aikopanel_bot
import time
from handler import MysqlUtils
from telegram import Update
from telegram.ext import ContextTypes

desc = 'Lấy thông tin sử dụng của tôi'
config = aikopanel_bot.config['bot']
configid = aikopanel_bot.config['aikopanel']['idapple']


def onQuery(sql):
    try:
        db = MysqlUtils()
        result = db.sql_query(sql)
    finally:
        db.close()
        return result


def getContent(user,chat_type):
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
    Data_Upload = round(user[4] / 1024 / 1024 / 1024, 2)
    Data_Download = round(user[5] / 1024 / 1024 / 1024, 2)
    Data_Total = round(user[6] / 1024 / 1024 / 1024, 2)
    Data_Last = round(
        (user[6]-user[5]-user[4]) / 1024 / 1024 / 1024, 2)
    Data_Time = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(user[7]))
    Email = user[8]
    sni = onQuery('Select user_sni From v2_user Where id = %s' % User_id)[0][0]
    CountgetIDapple = onQuery('Select count_idapple From v2_user Where id = %s' % User_id)[0][0]
    balance = onQuery('Select balance,commission_balance From v2_user Where id = %s' % User_id)

    text = f'{text}\n🎲*UID：* {User_id}'
    if chat_type == 'private':
        text = f'{text}\n📧*Email đăng ký：* {Email}'
    text = f'{text}\n⌚️*Thời gian đăng ký：* {Register_time}'
    text = f'{text}\n📚*Tên gói：* {Plan_id}'
    text = f'{text}\n📌*Thời gian hết hạn：* {Expire_time}'
    if Plan_id in configid['plan_limit']['plan_unlimit']:
        text = f'{text}\n🍎*Số Lần lấy IDApple：* ∞'
    else:
        text = f'{text}\n🍎*Số Lần lấy IDApple：* {CountgetIDapple} Lần/Tháng'
    text = f'{text}\n'
    if chat_type == 'private':
        text = f'{text}\n💳*Số Dư khả dụng: * {balance[0][0]} VNĐ'
        text = f'{text}\n💰*Số Dư hoa hồng: * {balance[0][1]} VNĐ'
        text = f'{text}\n'
        text = f'{text}\n📌*SNI hiện tại：* {sni}'
        text = f'{text}\n📤*Lưu lượng tải lên：* {Data_Upload} GB'
        text = f'{text}\n📥*Lưu lượng tải xuống：* {Data_Download} GB'
        text = f'{text}\n📃*Lưu lượng còn lại：* {Data_Last} GB'
        text = f'{text}\n📜*Tổng lưu lượng：* {Data_Total} GB'
    text = f'{text}\n📊*Lần sử dụng cuối cùng：* {Data_Time}'
    return text


async def autoDelete(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.delete_message(job.chat_id, job.data)


async def exec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    user_id = msg.from_user.id
    chat_id = msg.chat_id
    chat_type = msg.chat.type

    user = onQuery(
        'SELECT id,created_at,plan_id,expired_at,u,d,transfer_enable,t,email FROM v2_user WHERE `telegram_id` = %s' % user_id)
    if chat_type == 'private' or chat_id == config['group_id']:
        if len(user) > 0:
            if user[0][2] is not None:
                text = getContent(user[0],chat_type)
                callback = await msg.reply_markdown(text)
            else:
                callback = await msg.reply_markdown('❌*Lỗi*\nTài khoản của bạn chưa mua gói đăng ký!')
        else:
            callback = await msg.reply_markdown('❌*Lỗi*\nBạn chưa liên kết tài khoản!')
    if chat_type != 'private':
        context.job_queue.run_once(
            autoDelete, 300, data=msg.id, chat_id=chat_id, name=str(msg.id))
        context.job_queue.run_once(
            autoDelete, 300, data=callback.message_id, chat_id=chat_id, name=str(callback.message_id))
