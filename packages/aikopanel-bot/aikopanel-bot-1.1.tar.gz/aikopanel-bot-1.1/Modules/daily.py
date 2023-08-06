import aikopanel_bot
import pytz
import os
import datetime
import calendar
import yaml
from handler import MysqlUtils
from telegram.ext import ContextTypes


timezone = pytz.timezone('Asia/Ho_Chi_Minh')


class Conf:
    desc = 'Định kỳ đẩy lượng sử dụng'
    method = 'daily'
    runtime = '00:00:00+07:00:00'


class Settings:
    # Thống kê máy chủ
    send_server = True
    # Thống kê người dùng
    send_user = True
    # Thống kê bao nhiêu
    index = 5
    # Thống kê đơn hàng (chỉ đẩy admin)
    send_order = True


config = aikopanel_bot.config['bot']


def onQuery(sql):
    try:
        db = MysqlUtils()
        result = db.sql_query(sql)
    finally:
        db.close()
        return result


def getTimestemp():
    yesterday = (datetime.datetime.now(timezone) - datetime.timedelta(days=1)).strftime("%d-%m-%Y")
    inconvert = datetime.datetime.strptime(yesterday, "%d-%m-%Y")
    timestemp = int(calendar.timegm(inconvert.timetuple()) + 25200)  # Add 7 hours in seconds
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
        text += f'`***@***.com` - #`{user[0][0]}` - `{total}` GB\n'
    return text


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


def onTodayData():
    text = '📊*Thống kê ngày hôm qua：*\n\n'
    if Settings.send_server is True:
        text = f'{text}{onSendServer()}\n'
    if Settings.send_user is True:
        text = f'{text}{onSendUser()}\n'
    if Settings.send_server is False and Settings.send_user is False:
        return False, ''
    else:
        return True, text


def onTodayOrderData():
    content = onSendOrder()
    if Settings.send_order is False or len(content) == 0:
        return False, ''
    elif Settings.send_order is True:
        text = f'📊*Thống kê ngày hôm qua：*\n\n{content}\n'
        return True, text


async def exec(context: ContextTypes.DEFAULT_TYPE):
    result, text = onTodayData()
    if result is True:
        await context.bot.send_message(
            chat_id=config['group_id'],
            text=text,
            parse_mode='Markdown'
        )
    result, text = onTodayOrderData()
    if result is True:
        for admin_id in config['admin_id']:
            await context.bot.send_message(
                chat_id=admin_id,
                text=text,
                parse_mode='Markdown'
            )