import aikopanel_bot
import time
import re
from handler import MysqlUtils
from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import CallbackContext

desc = 'Check thông tin người dùng'
config = aikopanel_bot.config['bot']
configid = aikopanel_bot.config['aikopanel']['idapple']

def onQuery(sql, *params):
    try:
        db = MysqlUtils()
        if params:
            result = db.sql_query(sql, params)
        else:
            result = db.sql_query(sql)
    finally:
        db.close()
        return result


def getContent(user, chat_type):
    text = '📋*Thông tin cá nhân*\n'
    User_id = user[0]
    Register_time = time.strftime(
        "%d-%m-%Y %H:%M:%S", time.localtime(user[1]))
    Plan_id = ''
    if user[2]:
        plan = onQuery('SELECT name FROM v2_plan WHERE id = %s' % user[2])
        if plan:
            Plan_id = plan[0][0]
    Expire_time = 'Vĩnh Viễn'
    if user[3] is not None:
        Expire_time = time.strftime(
            "%d-%m-%Y %H:%M:%S", time.localtime(user[3]))
    Data_Upload = round(user[4] / 1024 / 1024 / 1024, 2)
    Data_Download = round(user[5] / 1024 / 1024 / 1024, 2)
    Data_Total = round(user[6] / 1024 / 1024 / 1024, 2)
    Data_Last = round(
        (user[6]-user[5]-user[4]) / 1024 / 1024 / 1024, 2)
    Data_Time = time.strftime(
        "%d-%m-%Y %H:%M:%S", time.localtime(user[7]))
    Email = user[8]
    
    CountgetIDapple = onQuery('Select count_idapple From v2_user Where id = %s' % User_id)[0][0]
    sni = onQuery('Select user_sni From v2_user Where id = %s' % User_id)[0][0]

    text = f'{text}\n🎲*ID：* {User_id}'
    if chat_type == 'private':
        text = f'{text}\n📧*Email：* {Email}'
    text = f'{text}\n⌚️*Thời gian đăng kí：* {Register_time}'
    if Plan_id != '':
        text = f'{text}\n📚*Gói：* {Plan_id}'
        text = f'{text}\n📌*Hạn sử dụng：* {Expire_time}'
        if Plan_id in configid['plan_limit']['plan_unlimit']:
            text = f'{text}\n🍎*Số Lần lấy IDApple：* ∞'
        else:
            text = f'{text}\n🍎*Số Lần lấy IDApple：* {CountgetIDapple} Lần/Tháng'
        text = f'{text}\n'
        if chat_type == 'private':
            text = f'{text}\n📌*SNI hiện tại：* {sni}'
            text = f'{text}\n📤*Upload：* {Data_Upload} GB'
            text = f'{text}\n📥*Dowload：* {Data_Download} GB'
            text = f'{text}\n📃*Còn lại：* {Data_Last} GB'
            text = f'{text}\n📜*Tổng：* {Data_Total} GB'
            text = f'{text}\n📊*Thời gian dùng cuối cùng：* {Data_Time}'
    else:
        text = f'{text}\n📚*Gói：* Không mua gói'
    return text


async def autoDelete(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.delete_message(job.chat_id, job.data)
    
async def check_info(update: Update, context: CallbackContext, info: str):
    user = None

    if '@' in info:
        user = onQuery(
            f"SELECT id,created_at,plan_id,expired_at,u,d,transfer_enable,t,email FROM v2_user WHERE `email` = '{info}'")
    elif '-' in info:
        user = onQuery(
            f"SELECT id,created_at,plan_id,expired_at,u,d,transfer_enable,t,email FROM v2_user WHERE `uuid` = '{info}'")
    else:
        try:
            user_id = int(info)
            user = onQuery(
                'SELECT id,created_at,plan_id,expired_at,u,d,transfer_enable,t,email FROM v2_user WHERE `id` = %s' % user_id)
        except ValueError:
            pass

    if user and len(user) > 0:
        text = getContent(user[0], update.effective_chat.type)
        callback = await update.message.reply_markdown(text)
    else:
        callback = await update.message.reply_markdown('❌*Lỗi*\nKhông tìm thấy người dùng với thông tin này!')

    return callback

async def exec(update: Update, context: CallbackContext):
    msg = update.effective_message
    user_id = msg.from_user.id
    chat_id = msg.chat_id
    chat_type = msg.chat.type

    # Handle check command
    if msg.text.startswith('/check'):
        if user_id not in config['admin_id']:
            callback = await msg.reply_markdown('❌*Lỗi*\nBạn không có quyền sử dụng lệnh này!')
            return

        # Check for reply message
        if msg.reply_to_message:
            reply_user_id = msg.reply_to_message.from_user.id
            user = onQuery(
                f"SELECT id,created_at,plan_id,expired_at,u,d,transfer_enable,t,email FROM v2_user WHERE `telegram_id` = '{reply_user_id}'")
            if user and len(user) > 0:
                info = str(user[0][0])
            else:
                callback = await msg.reply_markdown('❌*Lỗi*\nKhông tìm thấy người dùng với thông tin này!')
                return
        elif len(msg.text.split(' ')) < 2:
            callback = await msg.reply_markdown('❌*Lỗi*\nVui lòng cung cấp địa chỉ email, ID, UUID, hoặc token của người dùng!')
            return
        else:
            info = msg.text.split(' ')[1]

            # Check for Email
            if '@' in info:
                user = onQuery(
                    f"SELECT id,created_at,plan_id,expired_at,u,d,transfer_enable,t,email FROM v2_user WHERE `email` = '{info}'")
                if user and len(user) > 0:
                    info = str(user[0][0])
                else:
                    callback = await msg.reply_markdown('❌*Lỗi*\nKhông tìm thấy Email người dùng!')
                    return

            # Check for UUID
            elif '-' in info:
                user = onQuery(
                    f"SELECT id,created_at,plan_id,expired_at,u,d,transfer_enable,t,email FROM v2_user WHERE `uuid` = '{info}'")
                if user and len(user) > 0:
                    info = str(user[0][0])
                else:
                    callback = await msg.reply_markdown('❌*Lỗi*\nKhông tìm thấy UUID người dùng!')
                    return

            # Check for Token in URL
            elif 'token=' in info:
                token = re.search(r'token=([a-zA-Z0-9]+)', info)
                if token:
                    token = token.group(1)
                    user = onQuery(
                        f"SELECT id,created_at,plan_id,expired_at,u,d,transfer_enable,t,email FROM v2_user WHERE `token` = '{token}'")
                    if user and len(user) > 0:
                        info = str(user[0][0])
                    else:
                        callback = await msg.reply_markdown('❌*Lỗi*\nKhông tìm thấy Thông tin qua đường dẫn bạn cung cấp người dùng!')
                        return

            # Check for Token
            elif any(c.isalpha() for c in info) and any(c.isdigit() for c in info):
                user = onQuery(
                    f"SELECT id,created_at,plan_id,expired_at,u,d,transfer_enable,t,email FROM v2_user WHERE `token` = '{info}'")
                if user and len(user) > 0:
                    info = str(user[0][0])
                else:
                    callback = await msg.reply_markdown('❌*Lỗi*\nKhông tìm thấy Token người dùng!')
                    return

        callback = await check_info(update, context, info)

    # Schedule deletion of messages
    if chat_type != 'private':
        context.job_queue.run_once(
            autoDelete, 300, data=msg.id, chat_id=chat_id, name=str(msg.id))
        context.job_queue.run_once(
            autoDelete, 300, data=callback.message_id, chat_id=chat_id, name=str(callback.message_id))
