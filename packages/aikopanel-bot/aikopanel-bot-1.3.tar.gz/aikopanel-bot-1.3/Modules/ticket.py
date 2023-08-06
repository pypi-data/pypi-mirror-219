import aikopanel_bot
from handler import MysqlUtils
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class Conf:
    desc = 'Thông báo về các tickets mới'
    method = 'lặp lại'
    interval = 60


config = aikopanel_bot.config['bot']
ticket_total = 0
ticket_status = []

mapping = {
    'Level': ['Thấp', 'Trung bình', 'Cao']
}


def onQuery(sql):
    try:
        db = MysqlUtils()
        result = db.sql_query(sql)
    finally:
        db.close()
        return result


def getNewTicket():
    global ticket_total
    global ticket_status
    result = onQuery("SELECT id,user_id FROM v2_ticket_message")
    if ticket_total != 0 and len(result) > ticket_total:
        for i in range(ticket_total, len(result)):
            ticket = result[i]
            getUser = onQuery('SELECT is_admin,is_staff FROM v2_user WHERE `id` = %s' %
                              ticket[1])[0]
            if getUser[0] == 0 and getUser[1] == 0:
                ticket_status.append(ticket[0])
    ticket_total = len(result)


def onTicketData(current_ticket):
    User = onQuery('SELECT email FROM v2_user WHERE `id` = %s' %
                   current_ticket[1])[0][0]
    getTitle = onQuery('SELECT subject,level FROM v2_ticket WHERE `id` = %s' %
                       current_ticket[2])[0]
    Subject = getTitle[0]
    Level = mapping['Level'][getTitle[1]]

    text = '📠*MỘT VÉ MỚI*\n\n'
    text = f'{text}👤*Người dùng*：`{User}`\n'
    text = f'{text}📩*Chủ đề*：{Subject}\n'
    text = f'{text}🔔*Mức độ*：{Level}\n'
    text = f'{text}🧾*Nội dung*：{current_ticket[3]}\n'
    keyboard = [[InlineKeyboardButton(
        text='Phản hồi vé',
        url=f"{config['website']}/{config['admin_path']}#/ticket/{current_ticket[2]}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return text, reply_markup


async def exec(context: ContextTypes.DEFAULT_TYPE):
    getNewTicket()
    global ticket_status
    if len(ticket_status) > 0:
        for i in ticket_status:
            current_ticket = onQuery(
                "SELECT id,user_id,ticket_id,message FROM v2_ticket_message WHERE id = %s" % i)
            text, reply_markup = onTicketData(current_ticket[0])
            for admin_id in config['admin_id']:
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=text,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            ticket_status.remove(i)
