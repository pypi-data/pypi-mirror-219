import aikopanel_bot
import datetime
import calendar
import pytz
from handler import MysqlUtils
from telegram import Update
from telegram.ext import ContextTypes

desc = 'Trả lời dung lượng máy chủ sử dụng'
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
    timestemp = int(calendar.timegm(inconvert.timetuple()) - 25200)  # Add 7 hours in seconds
    return timestemp


def onSendServer():
    result = onQuery(
        "SELECT server_id, server_type, u, d FROM v2_stat_server WHERE record_at = %s" % getTimestemp())
    if result is None or len(result) == 0:
        return 'Không có dữ liệu'

    # Process the data
    result_list = sorted(result, key=lambda x: x[3], reverse=True)

    # Prepare the text
    index = min(Settings.index, len(result_list))
    text = f'Trước khi sử dụng {index} Nút: \n\n'
    for i in range(index):
        tbl_name = f'v2_server_{result_list[i][1]}'
        node_name = onQuery(
            f"SELECT name FROM {tbl_name} WHERE id = {result_list[i][0]}")[0][0]
        download = round((result_list[i][2] + result_list[i][3]) / 1024 / 1024 / 1024, 2)
        text += f'{node_name} - `{download}` GB\n'
    return text


async def exec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    user_id = msg.from_user.id
    chat_id = msg.chat_id
    chat_type = msg.chat.type
    if chat_type == 'private' or chat_id == config['group_id']:
					if Settings.send_server:
						text = onSendServer()
					if text is not None:
						await msg.reply_text(text, parse_mode='Markdown')