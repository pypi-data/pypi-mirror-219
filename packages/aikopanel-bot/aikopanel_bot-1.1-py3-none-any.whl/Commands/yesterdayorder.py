import aikopanel_bot
import datetime
import calendar
import pytz
from handler import MysqlUtils
from telegram import Update
from telegram.ext import ContextTypes

desc = 'Thống kê đơn Ngày hôm qua'
config = aikopanel_bot.config['bot']

timezone = pytz.timezone('Asia/Ho_Chi_Minh')

def onQuery(sql):
    try:
        db = MysqlUtils()
        result = db.sql_query(sql)
    finally:
        db.close()
        return result

class Settings:
    send_server = True
    send_user = True
    index = 10
    send_order = True

def getTimestemp():
    yesterday = (datetime.datetime.now(timezone) - datetime.timedelta(days=1)).strftime("%d-%m-%Y")
    inconvert = datetime.datetime.strptime(yesterday, "%d-%m-%Y")
    timestemp = int(calendar.timegm(inconvert.timetuple())-25200)  # Subtract 7 hours in seconds
    return timestemp


def onSendOrder():
    result = onQuery(
        "SELECT order_count,order_total,commission_count,commission_total FROM v2_stat WHERE record_at = %s" % getTimestemp())
    if result is not None and len(result) > 0:
        order_count = result[0][0]
        order_total = round(result[0][1] / 100, 2)
        commission_count = result[0][2]
        commission_total = round(result[0][3] / 100, 2)
        text = ''
        text = f'{text}📑*Tổng số đơn hàng*：{order_count} đơn\n'
        text = f'{text}💰*Tổng số tiền đơn hàng*：{order_total} VNĐ\n'
        text = f'{text}💸*Số lần hoàn tiền*：{commission_count} đơn\n'
        text = f'{text}💵*Tổng số tiền hoàn tiền*：{commission_total} VNĐ\n'
        return text
    else:
        return 'Không có dữ liệu'


async def exec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    user_id = msg.from_user.id
    chat_id = msg.chat_id
    chat_type = msg.chat.type
    if user_id in config['admin_id'] and (chat_type == 'private' or chat_id == config['group_id']):
					if Settings.send_server:
						text = onSendOrder()
					if text is not None:
						await msg.reply_text(text, parse_mode='Markdown')