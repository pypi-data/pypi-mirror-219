import aikopanel_bot
import requests
from handler import MysqlUtils
from telegram import Update
from telegram.ext import ContextTypes

desc = 'Giải trừ tài khoản Telegram của tài khoản này'
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
            await msg.reply_markdown('❌*Lỗi*\nBạn chưa kết nối tài khoản!')
        else:
            if len(context.args) == 2:
                email = context.args[0]
                password = context.args[1]
                if onLogin(email, password) is True:
                    check = onQuery(
                        'SELECT telegram_id FROM v2_user WHERE `email` = "%s"' % email)
                    if user_id == check[0][0]:
                        db = MysqlUtils()
                        db.execute_sql(
                            sql='UPDATE v2_user SET telegram_id = NULL WHERE email = "%s"' % email)
                        db.conn.commit()
                        db.close()
                        await msg.reply_markdown('✔️*Thành công*\nBạn đã giải trừ tài khoản Telegram!')
                    else:
                        await msg.reply_markdown('❌*Lỗi*\nTài khoản này không khớp với Telegram đã kết nối!')
                else:
                    await msg.reply_markdown('❌*Lỗi*\nEmail hoặc mật khẩu không đúng!')
            else:
                await msg.reply_markdown('❌*Lỗi*\nĐịnh dạng đúng là: /unbind email mật khẩu')
    else:
        if chat_id == config['group_id']:
            callback = await msg.reply_markdown('❌*Lỗi*\nVì sự an toàn của tài khoản của bạn, hãy nhắn tin cho tôi riêng tư!')
            context.job_queue.run_once(
                autoDelete, 300, data=msg.id, chat_id=chat_id, name=str(msg.id))
            context.job_queue.run_once(
                autoDelete, 300, data=callback.message_id, chat_id=chat_id, name=str(callback.message_id))
