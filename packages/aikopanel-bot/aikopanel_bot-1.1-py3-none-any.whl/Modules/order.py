import aikopanel_bot
import pytz
import enhanced
import os
from datetime import datetime
from handler import MysqlUtils
from telegram.ext import ContextTypes


class Conf:
    desc = 'Đẩy đơn hàng mới.'
    method = 'lặp lại'
    interval = 60


timezone = pytz.timezone('Asia/Ho_Chi_Minh')
config = aikopanel_bot.config['bot']
order_total = 0
order_status = []
thisEnhanced = False

if aikopanel_bot.isEnhanced:
    if aikopanel_bot.enhancedModules.count('order'):
        try:
            enhanced.initEnhanced()
            enhanced.dbEnhanced(os.path.basename(__file__).replace('.py', ''))
            thisEnhanced = True
        except Exception as err:
            print(repr(err))


mapping = {
    'Loại': ['Không', 'Mua mới', 'Gia hạn', 'Nâng cấp', 'Đặt lại'],
    'Kỳ hạn': {
        'month_price': 'Trả theo tháng',
        'quarter_price': 'Trả theo quý',
        'half_year_price': 'Trả theo nửa năm',
        'year_price': 'Trả theo năm',
        'two_year_price': 'Trả theo hai năm',
        'three_year_price': 'Trả theo ba năm',
        'onetime_price': 'Một lần',
        'reset_price': 'Gói đặt lại',
    }
}

def addEscapeChar(string):
    reserved_chars = '''\\`*_{}[]()#+.!|'''
    replace = ['\\' + l for l in reserved_chars]
    trans = str.maketrans(dict(zip(reserved_chars, replace)))
    return string.translate(trans)

def onQuery(sql):
    try:
        db = MysqlUtils()
        result = db.sql_query(sql)
    finally:
        db.close()
        return result


def onSqlExec(sql):
    try:
        db = MysqlUtils()
        result = db.execute_sql(sql)
        if result is not None:
            raise Exception(result)
    finally:
        db.close()


def onUpdate(tableName, params, conditions):
    try:
        db = MysqlUtils()
        db.update_one(tableName, params, conditions)
    except Exception as err:
        print(err)
    finally:
        db.close()


def getUnsentOrdersFull():
    try:
        onSqlExec('INSERT INTO enhncd_v2_order_notice (`id`,`tg_send_mask`) SELECT `id`,0 FROM v2_order WHERE NOT EXISTS(SELECT `id` from enhncd_v2_order_notice where `id`=v2_order.`id`)')
        sql = 'SELECT v2btb.`user_id`, v2btb.`plan_id`, v2btb.`payment_id`, v2btb.`type`, v2btb.`period`, v2btb.`total_amount`, v2btb.`status`, v2btb.`paid_at`, enhncdtb.`id`, enhncdtb.`tg_send_mask` FROM enhncd_v2_order_notice enhncdtb INNER JOIN v2_order v2btb ON enhncdtb.`id`=v2btb.`id` WHERE enhncdtb.`tg_send_mask`=0'
        unsentOrdersFull = onQuery(sql)
        return unsentOrdersFull
    except Exception as err:
        print(repr(err))


def cleanupUnsentOrders(rows):
    rows = list(rows)
    try:
        for row in rows[:]:
            if row[6] == 0 or row[6] == 1:
                rows.remove(row)
            elif row[6] == 2:
                onUpdate('enhncd_v2_order_notice', params={
                         'tg_send_mask': -1}, conditions={'id': row[8]})
                rows.remove(row)
            elif (row[6] == 3 or row[6] == 4) and row[5] == 0:
                onUpdate('enhncd_v2_order_notice', params={
                         'tg_send_mask': -1}, conditions={'id': row[8]})
                rows.remove(row)
        return rows
    except Exception as err:
        print(repr(err))


def markSent(row):
    try:
        onUpdate('enhncd_v2_order_notice', params={
                 'tg_send_mask': 1}, conditions={'id': row[8]})
    except Exception as err:
        print(repr(err))


def getNewOrder():
    global order_total
    global order_status
    result = onQuery("SELECT id,status FROM v2_order")
    if order_total != 0 and len(result) > order_total:
        for i in range(order_total-1, len(result)):
            status = result[i][1]
            if status == 0 or status == 1:
                order_status.append(result[i][0])
    order_total = len(result)


def onOrderData(current_order):
    getUser = onQuery('SELECT email FROM v2_user WHERE `id` = %s' %
                      current_order[0])
    User = getUser[0][0]
    getPlan = onQuery('SELECT name FROM v2_plan WHERE `id` = %s' %
                      current_order[1])
    Plan = getPlan[0][0]
    Payment = 'Không có'
    if current_order[2] is not None:
        getPaygate = onQuery(
            'SELECT name FROM v2_payment WHERE `id` = %s' % current_order[2])
        Payment = getPaygate[0][0]

    Type = mapping['Type'][current_order[3]]
    Period = mapping['Period'][current_order[4]]
    Amount = round(current_order[5] / 100, 2)
    Paid_Time = datetime.fromtimestamp(
        (current_order[7]), timezone).strftime("%Y-%m-%d %H:%M:%S")

    text = '📠*Đơn hàng mới*\n\n'
    text = f'{text}👤*Người dùng*：`{User}`\n'
    text = f'{text}🛍*Gói*：{addEscapeChar(Plan)}\n'
    text = f'{text}💵*Thanh toán*：{addEscapeChar(Payment)}\n'
    text = f'{text}📥*Loại*：{Type}\n'
    text = f'{text}📅*Thời gian*：{Period}\n'
    text = f'{text}🏷*Giá*：{Amount}\n'
    text = f'{text}🕰*Thời gian thanh toán*：{Paid_Time}\n'

    return text


async def exec(context: ContextTypes.DEFAULT_TYPE):
    if thisEnhanced:
        # enhanced order push
        unsentOrdersFull = getUnsentOrdersFull()
        unsentOrdersFull = cleanupUnsentOrders(unsentOrdersFull)
        if len(unsentOrdersFull) > 0:
            for current_order in unsentOrdersFull:
                text = onOrderData(current_order)
                for admin_id in config['admin_id']:
                    try:
                        await context.bot.send_message(
                            chat_id=admin_id,
                            text=text,
                            parse_mode='Markdown'
                        )
                        markSent(current_order)
                    except Exception as err:
                        print("Failed To Send message: ", err)
    else:
        # original order push
        getNewOrder()
        global order_status
        if len(order_status) > 0:
            for i in order_status:
                current_order = onQuery(
                    "SELECT user_id,plan_id,payment_id,type,period,total_amount,status,paid_at FROM v2_order WHERE id = %s" % i)
                if current_order[0][6] == 2:
                    order_status.remove(i)
                elif current_order[0][6] == 3 or current_order[0][6] == 4:
                    if current_order[0][5] > 0 and current_order[0][2] is not None:
                        text = onOrderData(current_order[0])
                        for admin_id in config['admin_id']:
                            await context.bot.send_message(
                                chat_id=admin_id,
                                text=text,
                                parse_mode='Markdown'
                            )
                    order_status.remove(i)
