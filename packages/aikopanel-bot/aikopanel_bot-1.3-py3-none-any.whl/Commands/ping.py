from telegram import Update
from telegram.ext import ContextTypes

desc = 'Lấy thông tin trò chuyện hiện tại'


async def autoDelete(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.delete_message(job.chat_id, job.data)


async def exec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    user_id = msg.from_user.id
    chat_id = msg.chat_id
    chat_type = msg.chat.type

    # Kiểm tra xem có reply tin nhắn không
    if msg.reply_to_message:
        replied_user_id = msg.reply_to_message.from_user.id
        replied_user = f'\nID người đã reply là: `{replied_user_id}`'
        return await msg.reply_markdown(replied_user)
        
    text = '💥*Xì....*\n'
    utid = f'{text}\nID của bạn là:` {user_id}`'


    if chat_type == 'private':
        await msg.reply_markdown(f'{utid}')
    else:
        group = f'\nID nhóm là:` {chat_id}`'
        if msg.reply_to_message:
            callback = await msg.reply_markdown(f'{replied_user}')
        else:
            callback = await msg.reply_markdown(f'{group}')
        context.job_queue.run_once(
            autoDelete, 300, data=msg.id, chat_id=chat_id, name=str(msg.id))
        context.job_queue.run_once(
            autoDelete, 300, data=callback.message_id, chat_id=chat_id, name=str(callback.message_id))
