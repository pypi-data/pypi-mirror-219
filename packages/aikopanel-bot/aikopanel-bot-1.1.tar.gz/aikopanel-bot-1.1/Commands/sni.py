import aikopanel_bot
import time
from handler import MysqlUtils
from telegram import Update
from telegram.ext import ContextTypes

desc = 'Đổi SNI của tôi'
config = aikopanel_bot.config['bot']

SNI_OPTIONS = aikopanel_bot.config['aikopanel']['sni']

def onQuery(sql):
    try:
        db = MysqlUtils()
        result = db.sql_query(sql)
    finally:
        db.close()
        return result
    
def getContent(user, chat_type):
    text = '🤣 SNI của tôi'
    if chat_type == 'private':
        text += '\n🔮 SNI hiện tại: %s\n' % user
    text += '\n🔮 Để đổi SNI, hãy nhập lệnh sau:\n'
    text += '\n/sni <SNI mới>'
    text += '\n\n🔮 Để đổi SNI về mặc định, hãy nhập lệnh sau:\n'

    for option, sni in SNI_OPTIONS.items():
        text += f"\n⚽️ {option} : {sni}"

    text += "\n\n /sni 1 || Chuyển sang SNI Liên Quân."
    text += "\n\n🍎 Lưu ý : Update Lại Gói để cập nhật SNI"
    return text


def change_sni(user_id, sni):
    db = MysqlUtils()
    # Cập nhật SNI mới trong cơ sở dữ liệu
    db.update_one('v2_user', params={'user_sni': sni}, conditions={'telegram_id': user_id})
    # Commit thay đổi
    db.conn.commit()
    # Đóng kết nối cơ sở dữ liệu
    db.close()

async def autoDelete(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.delete_message(job.chat_id, job.data)

async def exec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    user_id = msg.from_user.id
    chat_id = msg.chat_id
    chat_type = msg.chat.type

    if chat_type == 'private' or chat_id == config['group_id']:
        args = context.args

        user = onQuery('SELECT user_sni,plan_id FROM v2_user WHERE `telegram_id` = %s' % user_id)
        if len(user) == 0:
            sent_msg = await msg.reply_text('❌*Thất bại*\nVui Lòng Liên kết tài khoản.')
            return

        if user[0][1] == 0:
            sent_msg = await msg.reply_text('❌*Thất bại*\nBạn Chưa mua gói dịch vụ , Vui lòng mua gói dịch vụ để sử dụng chức năng!!!.')
            return

        if len(args) == 0:
            sent_msg = await msg.reply_text(getContent(user[0][0], chat_type))
            return
        
        # Change SNI based on input
        sni = args[0]
        if sni in SNI_OPTIONS:
            change_sni(user_id, SNI_OPTIONS[sni])
            sent_msg = await msg.reply_text(f'✔️*Thành Công*\nĐã đổi SNI của bạn thành công.\nSNI hiện tại: {SNI_OPTIONS[sni]}')
        else:
            if chat_type == 'private':
                sni = sni.replace('https://', '').replace('http://', '')
                if '.' not in sni:
                    sent_msg = await msg.reply_text('❌ Định dạng không hợp lệ. Vui lòng kiểm tra lại.')
                    return
                change_sni(user_id, sni)
                sent_msg = await msg.reply_text(f'✔️*Thành Công*\nĐã đổi SNI của bạn thành công.\nSNI hiện tại: {sni}')
            else:
                sent_msg = await msg.reply_text('❌ Vui lòng Inbox Tôi để đổi SNI khác SNI mặc định.')
        
    # auto delete message
    if chat_type != 'private':
        context.job_queue.run_once(
            autoDelete, 300, data=msg.id, chat_id=chat_id, name=str(msg.id))
        context.job_queue.run_once(
            autoDelete, 300, data=sent_msg.message_id, chat_id=chat_id, name=str(sent_msg.message_id))