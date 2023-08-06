import aikopanel_bot
from handler import MysqlUtils
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import requests
import re


desc = 'Lấy phiên bản mới nhất của các ứng dụng'
config = aikopanel_bot.config['bot']

def get_latest_release(repo_owner, repo_name):
    # Tạo URL API
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest'
    # Gửi yêu cầu GET đến API
    response = requests.get(api_url)

    # Kiểm tra mã phản hồi
    if response.status_code == 200:
        # Lấy thông tin phiên bản từ phản hồi JSON
        release_info = response.json()
        latest_release = release_info['tag_name']
        return latest_release
    else:
        return ' - Github Tạm block get release, vui lòng thử lại sau .'
    
def extract_version_number(version_string):
    # Sử dụng biểu thức chính quy để tìm số phiên bản trong chuỗi
    match = re.search(r'(\d+\.\d+\.\d+)', version_string)
    if match:
        return match.group(1)
    else:
        return None 
    
async def autoDelete(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.delete_message(job.chat_id, job.data)

async def exec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    chat_id = msg.chat_id
    chat_type = msg.chat.type
    
    # Get the latest releases for the apps
    cfa = get_latest_release('Kr328', 'ClashForAndroid')
    num_cfa = extract_version_number(cfa)
    cfw = get_latest_release('Fndroid', 'clash_for_windows_pkg')
    num_cfw = extract_version_number(cfw)
    v2rayng = get_latest_release('2dust', 'v2rayNG')
    surfboard = get_latest_release('getsurfboard', 'surfboard')
    clashX = get_latest_release('yichengchen', 'clashX')
    netch = get_latest_release('NetchX', 'Netch')
    v2rayn = get_latest_release('2dust', 'v2rayN')
    meta = get_latest_release('MetaCubeX', 'ClashMetaForAndroid')
    num_meta = extract_version_number(meta)
    nekobox = get_latest_release('MatsuriDayo', 'NekoBoxForAndroid')
    ssrray = get_latest_release('xxf098', 'shadowsocksr-v2ray-trojan-android')
    num_ssray = extract_version_number(ssrray)
    
    # Compose the response message in markdown format
    message = f"*Latest releases: (AikoPanel Support)*\n\n"
    message += "*Android Application:*\n"
    message += f"Clash for Android: `{cfa}` - [Download](https://github.com/Kr328/ClashForAndroid/releases/download/{cfa}/cfa-{num_cfa}-premium-universal-release.apk)\n"
    message += f"Surfboard: `v{surfboard}` - [Download](https://github.com/getsurfboard/surfboard/releases/download/{surfboard}/mobile-arm64-v8a-release.apk)\n"
    message += f"Clash Meta: `{meta}` - [Download](https://github.com/MetaCubeX/ClashMetaForAndroid/releases/download/{meta}/cmfa-{num_meta}-meta-universal-release.apk)\n"
    message += f"NekoBox: `v{nekobox}` - [Download](https://github.com/MatsuriDayo/NekoBoxForAndroid/releases/download/{nekobox}/NB4A-{nekobox}-arm64-v8a.apk)\n"
    message += f"SSRRAY: `{ssrray}` - [Download](https://github.com/xxf098/shadowsocksr-v2ray-trojan-android/releases/download/{ssrray}/ssrray-release-{num_ssray}.apk)\n"
    message += f"v2rayNG: `v{v2rayng}` - [Download](https://github.com/2dust/v2rayNG/releases/download/{v2rayng}/v2rayNG_{v2rayng}.apk)\n"
    message += f"\n"
    message += "*IOS Application:*\n"
    message += f"Shadowrocket - [Download](https://apps.apple.com/app/shadowrocket/id932747118) - Price: $2.99\n"
    message += f"Quantumult X - [Download](https://apps.apple.com/app/quantumult-x/id1443988620) - Price: $7.99\n"
    message += f"Stash - [Download](https://apps.apple.com/app/stash-invest-learn-save/id1017148055) - Price: $2.99\n"
    message += f"LanceX - [Download](https://apps.apple.com/us/app/lancex/id1536754048) - Price: $2.99\n"
    message += f"Surge - [Download](https://apps.apple.com/app/surge-web-developer-tool-proxy/id1329879957) - Price Update : $49.99\n"
    message += f"Bạn có thể tải Free Shadowrocket And Quantumult Khi đã mua gói AikoVPN\n"
    message += f"\n"
    message += "*Windows Application:*\n"
    message += f"Clash for Windows: `v{cfw}` - [Download](https://github.com/Fndroid/clash_for_windows_pkg/releases/download/{cfw}/Clash.for.Windows.Setup.{num_cfw}.exe)\n"
    message += f"Netch `v{netch}` - [Download](https://github.com/netchx/netch/releases/download/{netch}/Netch.7z)\n"
    message += f"V2rayN `v4.26.0` - [Download](https://github.com/2dust/v2rayN/releases/download/{v2rayn}/v2rayN.zip)\n"
    message += f"\n"
    message += "*MacOS Application:*\n"
    message += f"ClashX: `v{clashX}` - [Download](https://github.com/yichengchen/clashX/releases/download/{clashX}/ClashX.dmg)\n"
    message += f"Clash For Windows `v{cfw}` - [Download](https://github.com/Fndroid/clash_for_windows_pkg/releases/download/{cfw}/Clash.for.Windows-{num_cfw}.dmg)" 
    message += f"\n"

    # typing action to let the user know the bot is working
    await update.message.chat.send_action(action="typing")
    callback = await msg.reply_markdown(message, disable_web_page_preview=True)
    if chat_type != 'private':
        # Xóa tin nhắn sau khi được gửi để bảo vệ thông tin cá nhân
        context.job_queue.run_once(
            autoDelete, 300, data=msg.id, chat_id=chat_id, name=str(msg.id))
        context.job_queue.run_once(
            autoDelete, 300, data=callback.message_id, chat_id=chat_id, name=str(callback.message_id))
