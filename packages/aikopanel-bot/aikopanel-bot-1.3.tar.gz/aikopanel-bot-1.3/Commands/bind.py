import aikopanel_bot
import requests
from handler import MysqlUtils
from telegram import Update
from telegram.ext import ContextTypes

desc = 'Liên kết thông tin tài khoản với tài khoản Telegram này'
config = aikopanel_bot.config['bot']


def onLogin(email, password):
    login = {
        "email": email,
        "password": password
    }
    url = '%s/api/v1/passport/aiko/login' % config['website']
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    x = requests.post(url, login, headers=headers, timeout=5)
    if x.status_code == 200:
        return True
    else:
        return False


def onQuery(sql):
    try:
        db = MysqlUtils()
        result = db.sql_query(sql)
    finally:
        db.close()
        return result


async def autoDelete(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.delete_message(job.chat_id, job.data)


async def exec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    user_id = msg.from_user.id
    chat_id = msg.chat_id
    chat_type = msg.chat.type
    if chat_type == 'private':
        user = onQuery(
            'SELECT * FROM v2_user WHERE `telegram_id` = %s' % user_id)
        if len(user) == 0:
            if len(context.args) == 2:
                email = context.args[0]
                password = context.args[1]
                if onLogin(email, password) is True:
                    check = onQuery(
                        'SELECT telegram_id FROM v2_user WHERE `email` = "%s"' % email)[0]
                    if check[0] is None:
                        db = MysqlUtils()
                        db.update_one('v2_user', params={
                            'telegram_id': user_id}, conditions={'email': email})
                        db.conn.commit()
                        db.close()
                        await msg.reply_markdown('✔️*Thành công*\nBạn đã liên kết Telegram thành công!')
                    else:
                        await msg.reply_markdown('❌*Lỗi*\nTài khoản này đã được liên kết với một tài khoản Telegram khác!')
                else:
                    await msg.reply_markdown('❌*Lỗi*\nEmail hoặc mật khẩu không đúng!')
            else:
                await msg.reply_markdown('❌*Lỗi*\nĐịnh dạng đúng là: /bind email mật khẩu')
        else:
            await msg.reply_markdown('❌*Lỗi*\nBạn đã liên kết tài khoản rồi!')
    else:
        if chat_id == config['group_id']:
            callback = await msg.reply_markdown('❌*Lỗi*\nVì lý do bảo mật, vui lòng nhắn tin riêng cho tôi!')
            context.job_queue.run_once(
                autoDelete, 300, data=msg.id, chat_id=chat_id, name=str(msg.id))
            context.job_queue.run_once(
                autoDelete, 300, data=callback.message_id, chat_id=chat_id, name=str(callback.message_id))
