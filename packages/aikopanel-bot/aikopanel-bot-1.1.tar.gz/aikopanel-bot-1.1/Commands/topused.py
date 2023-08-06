import aikopanel_bot
import datetime
import calendar
import pytz
from handler import MysqlUtils
from telegram import Update
from telegram.ext import ContextTypes

desc = 'Top Member Sử dụng Băng thông cao nhất'
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
    timestemp = int(calendar.timegm(inconvert.timetuple()) + 25200)  # Add 7 hours in seconds
    return timestemp

def onSendUser():
    # Get the data from the database
    result = onQuery(
        "SELECT user_id, u, d FROM v2_stat_user WHERE record_at = %s" % getTimestemp())
    if result is None or len(result) == 0:
        return 'Không có dữ liệu'

    # Process the data
    result_dict = {}
    for i in result:
        result_dict[str(i[0])] = result_dict.get(str(i[0]), 0) + i[1] + i[2]

    # Sort the data
    result_list = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)

    # Prepare the text
    index = min(Settings.index, len(result_list))
    text = f'Trước khi sử dụng {index} Tên người dùng:\n\n'
    for i in range(index):
        user = onQuery("SELECT * FROM v2_user WHERE id = %s" % result_list[i][0])
        total = round(result_list[i][1] / 1024 / 1024 / 1024, 2)
        # Display the first 5 characters of the user's email
        email_start = user[0][3][:5]
        text += f'{email_start}...@aikocute.tech - {total} GB\n'
    return text


async def exec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    user_id = msg.from_user.id
    chat_id = msg.chat_id
    chat_type = msg.chat.type
    if chat_type == 'private' or chat_id == config['group_id']:
					if Settings.send_server:
						text = onSendUser()
					if text is not None:
						await msg.reply_text(text, parse_mode='Markdown')