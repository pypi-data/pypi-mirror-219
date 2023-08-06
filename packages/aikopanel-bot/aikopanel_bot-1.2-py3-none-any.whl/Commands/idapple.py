import json
import requests
import aikopanel_bot
from handler import MysqlUtils
from telegram import Update , InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Load configuration
config = aikopanel_bot.config['bot']
configid = aikopanel_bot.config['aikopanel']['idapple']

# Define constants
desc = 'Lấy thông tin IDAPPLE'
API_URL = configid['api_url']
URL_FIX_BUG = configid['url_fix_bug']
ALLOWED_PLANS = configid['allow_plan']
REQUEST_LIMIT_MIN = configid['request_limit']['plan_min']
REQUEST_LIMIT_MAX = configid['request_limit']['plan_max']
PLAN_MIN = configid['plan_limit']['plan_min']
PLAN_MAX = configid['plan_limit']['plan_max']
UNLIMITED_PLAN = configid['plan_limit']['plan_unlimit']
QUANTUMULTX_LINK = configid['quantumultx_link']

# Define a function to execute a SQL query
def onQuery(sql):
    try:
        db = MysqlUtils()
        result = db.sql_query(sql)
    finally:
        db.close()
        return result

# Define a function to fetch Apple IDs from the API
def fetch_idapple():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data["accounts"]
    return None

# Define a function to format the Apple ID message
def format_idapple_message(accounts):
    text = '🍏 **IDAPPLE được cung cấp:**\n\n'
    for idx, account in enumerate(accounts):
        status_text = f'ID {account["id"]} Đã được kiểm tra' if account['status'] else f'ID {account["id"]} không được kiểm tra'
        icon_status = '🟢' if account['status'] else '🔴' 
        text += f'{icon_status} **Status:** {status_text}\n\n'
        text += f'📧 **Apple ID:** `{account["username"]}`\n\n'
        text += f'🔑 **Password:** `{account["password"]}`\n\n'
        text += f'📝 **Ghi chú:** Nếu IDAPPLE bị lỗi bạn hãy sử dụng lệnh `/idapple report` để gửi thông báo tới admin\n\n'
    return text

# Define a function to automatically delete a message
async def autoDelete(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.delete_message(job.chat_id, job.data)

# Define a function to check if a user has exceeded their Apple ID request limit
def check_idapple_requests(user_id, request_limit):
    sql = "SELECT count_idapple FROM v2_user WHERE `telegram_id` = %s" % user_id
    result = onQuery(sql)
    return result[0][0] < request_limit

# Define a function to increment the Apple ID request count for a user
def increment_idapple_count(user_id: int):
    db = MysqlUtils()
    # +1 lần request
    count = onQuery('SELECT count_idapple FROM v2_user WHERE `telegram_id` = %s' % user_id)[0][0] + 1
    db.update_one('v2_user', params={'count_idapple': count}, conditions={'telegram_id': user_id})
    db.conn.commit()
    db.close()

# Define a function to get a user's plan ID
def get_plan_id(user):
    plan_id = onQuery(f'SELECT name FROM v2_plan WHERE id = {user[0][2]}')[0][0] 
    return plan_id

# Define a function to reset a user's Apple ID request count
async def reset_idapple(msg, reset_id_str):
    try:
        reset_id = int(reset_id_str)
    except ValueError:
        await msg.reply_text('Định dạng không hợp lệ. Vui lòng nhập số ID muốn reset.')
        return

    db = MysqlUtils()
    db.update_one('v2_user', params={'count_idapple': 0}, conditions={'id': reset_id})
    db.conn.commit()
    db.close()
    await msg.reply_text(f'✔️*Thành Công*\nĐã reset số lần lấy IDAPPLE cho người dùng có ID là {reset_id}.')

# Define a function to set a user's Apple ID request count
async def set_count_idapple(msg, reset_id_str, number):
    try:
        reset_id = int(reset_id_str)
    except ValueError:
        await msg.reply_text('Định dạng không hợp lệ. Vui lòng nhập số ID muốn reset.')
        return

    try:
        db = MysqlUtils()
        db.update_one('v2_user', params={'count_idapple': number}, conditions={'id': reset_id})
        db.conn.commit()
    except Exception as e:
        print(f"Error updating database: {e}")
        await msg.reply_text(f'❌*Thất bại*\nKhông thể cập nhật cơ sở dữ liệu.')
    else:
        await msg.reply_text(f'✔️*Thành Công*\nĐã reset số lần lấy IDAPPLE cho người dùng có ID là {reset_id} = {number}.')
    finally:
        db.close()

# Define a function to unlock Apple IDs
def unlock_idapple():
    import requests
    import time
    
    requests.get(URL_FIX_BUG)
    time.sleep(60)
    
    return True

# Define a function to send an Apple ID message
async def send_idapple_message(plan_id, accounts, count_idapple):
    text = format_idapple_message(accounts)
    text += f"\n🔰 Gói đăng ký: {plan_id}\n"
    if plan_id in PLAN_MAX:
        text += f"🔰 Số lần lấy IDAPPLE còn lại: {REQUEST_LIMIT_MAX - (count_idapple + 1)}\n" # Now request + 1
    elif plan_id in PLAN_MIN:
        text += f"🔰 Số lần lấy IDAPPLE còn lại: {REQUEST_LIMIT_MIN - (count_idapple + 1)}\n" # Now request + 1
    else:
        text += f"🔰 Số lần lấy IDAPPLE còn lại: ∞\n"
    return text

# Define the main function to process requests
async def exec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await process_request(update, context)

# Define a function to process requests
async def process_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    user_id = msg.from_user.id
    chat_id = msg.chat_id
    chat_type = msg.chat.type
    is_admin = user_id in config['admin_id']

    # Handle admin commands
    if is_admin and (chat_id == config["group_id"] or chat_type == "private"):
        args = context.args
        args_lower = [arg.lower() for arg in args]

        if len(args) == 2 and "reset" in args_lower:
            await reset_idapple(msg, args[1])
            return
        
        if len(args) == 1 and "fix" in args_lower:
            await msg.reply_markdown("🔓*Đang Kiểm tra lỗi ...*")
            unlock_idapple()
            await msg.reply_markdown("✔️*Thành Công*, đã fix lỗi IDAPPLE.")
            return
        
        if len(args) == 3 and "set" in args_lower:
            await set_count_idapple(msg, args[1], args[2])
            return

    # Handle private chat
    if chat_type == "private":
        if "report" in context.args:
            # Report to all admins when a user reports an issue
            user_info = onQuery(f'SELECT id, email FROM v2_user WHERE `telegram_id` = {user_id}')
            if user_info:
                user_id_report, email_report = user_info[0]
                report = f'📢*Thông báo*\nNgười dùng có ID là `{user_id_report}` đã thông báo lỗi.\nEmail của họ: `{email_report}`.'
                for admin_id in config["bot"]["admin_id"]:
                    await context.bot.send_message(admin_id, report)
            return

        await update.message.chat.send_action(action="typing")
        user = onQuery(f'SELECT id,created_at,plan_id,expired_at,u,d,transfer_enable,t,count_idapple FROM v2_user WHERE `telegram_id` = {user_id}')

        if user[0][2] is None:
            sent_msg = await msg.reply_markdown('❌*Lỗi*\nBạn chưa mua gói dịch vụ hoặc chưa được cấp ID.')
            return
        
        plan_id = get_plan_id(user)
        request_limit = REQUEST_LIMIT_MIN if plan_id == PLAN_MIN else REQUEST_LIMIT_MAX
        if check_idapple_requests(user_id, request_limit):
            accounts = fetch_idapple()
            if accounts:
                message_text = await send_idapple_message(plan_id, accounts, user[0][8])
                if plan_id in UNLIMITED_PLAN or plan_id in PLAN_MAX:
                    message_text += '\n🔗*Lưu ý:* Bạn lên tải Quantumult-X từ ID xong thì hãy xoá App hiện tại trong gói và Dowload App từ link cung cấp bên dưới để không bị lỗi Build đỏ nhé.'
                    keyboard = [[InlineKeyboardButton(link["text"], url=link["url"])] for link in QUANTUMULTX_LINK]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await msg.reply_markdown(message_text, reply_markup=reply_markup)
                else:
                    await msg.reply_markdown(message_text)
                if not is_admin and plan_id not in UNLIMITED_PLAN:
                    increment_idapple_count(user_id)
            else:
                sent_msg = await msg.reply_markdown('❌*Lỗi*\nKhông thể lấy thông tin IDAPPLE từ API')
        else:
            sent_msg = await msg.reply_markdown('❌*Lỗi*\nBạn đã vượt quá giới hạn số lần lấy IDAPPLE cho gói đăng ký của bạn.')
    else:
        sent_msg = await msg.reply_markdown('❌*Lỗi*\nBạn không có quyền share ID cho Group.')

    if chat_type != 'private':
        context.job_queue.run_once(
            autoDelete, 300, data=msg.id, chat_id=chat_id, name=str(msg.id))
        context.job_queue.run_once(
            autoDelete, 300, data=sent_msg.message_id, chat_id=chat_id, name=str(sent_msg.message_id))
