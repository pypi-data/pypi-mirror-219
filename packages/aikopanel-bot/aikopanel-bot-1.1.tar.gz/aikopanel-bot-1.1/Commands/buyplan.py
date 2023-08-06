import aikopanel_bot
from handler import MysqlUtils
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

desc = 'Mở cửa hàng mua sắm'
config = aikopanel_bot.config['bot']


def onQuery():
    try:
        db = MysqlUtils()
        result = db.sql_query('SELECT id,name FROM v2_plan WHERE `show` = 1')
    finally:
        db.close()
        return result


def getContent():
    text = '📦*Gói mua*\n\n🌐Nhấn vào nút bên dưới để đi đến địa chỉ mua hàng'
    plan = onQuery()
    keyboard = []
    url = '%s/#/plan/' % config['website']
    for i in plan:
        keyboard.append([InlineKeyboardButton(
            text=f'Mua {i[1]}', url=f"{url}{i[0]}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return text, reply_markup


async def autoDelete(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.delete_message(job.chat_id, job.data)


async def exec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    chat_id = msg.chat_id
    chat_type = msg.chat.type

    if chat_type == 'private' or chat_id == config['group_id']:
        text, reply_markup = getContent()
        callback = await msg.reply_markdown(text, reply_markup=reply_markup)
        if chat_type != 'private':
            context.job_queue.run_once(
                autoDelete, 300, data=msg.id, chat_id=chat_id, name=str(msg.id))
            context.job_queue.run_once(
                autoDelete, 300, data=callback.message_id, chat_id=chat_id, name=str(callback.message_id))
