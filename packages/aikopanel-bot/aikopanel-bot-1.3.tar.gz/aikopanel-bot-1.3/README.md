# AikoPanel Telegram Bot qua Python
- [AikoPanel Telegram Bot qua Python](#AikoPanel-telegram-bot-qua-python)
    - [Các tính năng hiện có](#các-tính-năng-hiện-có)
    - [Các lệnh hiện có](#các-lệnh-hiện-có)
    - [Sử dụng thông thường](#sử-dụng-thông-thường)
    - [Yêu cầu mã thông báo Telegram Bot](#yêu-cầu-mã-thông-báo-telegram-bot)
    - [Giải thích biến môi trường](#24-giải-thích-biến-môi-trường)
    - [Lưu ý đặc biệt](#26-lưu-ý-đặc-biệt)

Một dự án đơn giản, cho phép AikoPanel Telegram Bot hỗ trợ nhiều tính năng hơn.
Phản hồi nhanh chóng của nhóm: [https://t.me/AikoPanel_python_bot](https://t.me/AikoPanel_python_bot)

Python version requirement >= 3.8

## Các tính năng hiện có
- Dựa trên MySQL, hỗ trợ đăng nhập bằng SSH
- Tự động xóa tin nhắn trong nhóm chat
- Tự động gửi đơn hàng, yêu cầu hỗ trợ cho quản trị viên
- Tự động gửi thống kê dữ liệu hàng ngày
- Hỗ trợ ràng buộc và giải ràng buộc trong Bot
- Hỗ trợ lấy thông tin người dùng, đăng ký, mời
- Hỗ trợ lấy thông tin gói và tạo nút mua

## Các lệnh hiện có
|   Lệnh   |   Tham số    |         Mô tả         |
| :------: | :-------: | :------------------: |
|   ping   |    Không     |     Lấy ID cuộc trò chuyện     |
|   bind   | Email Mật khẩu | Ràng buộc email này với Telegram |
|  unbind  | Email Mật khẩu | Giải phóng ràng buộc email này với Telegram |
|  mysub   |    Không     | Lấy liên kết đăng ký của tài khoản này |
|  myinfo  |    Không     | Lấy thông tin đăng ký của tài khoản này |
| myusage  |    Không     | Lấy chi tiết lưu lượng của tài khoản này |
| myinvite |    Không     | Lấy thông tin mời của tài khoản này |
| buyplan  |    Không     |   Lấy liên kết mua gói   |
| website  |    Không     |     Lấy liên kết trang web     |


## Sử dụng thông thường
```
# apt install git nếu bạn chưa có git
git clone https://github.com/AikoPanel/AikoPanel_Bot.git
# Để tiến trình luôn chạy, bạn có thể sử dụng screen hoặc nohup
# Bạn cần cài đặt pip3 để quản lý các gói
cd AikoPanel_Telegram_Bot
pip3 install -r requirements.txt
cp config.yaml.example config.yaml
nano config.yaml
# Chỉnh sửa dòng 2 thành địa chỉ AikoPanel của bạn, cuối cùng đừng thêm ký tự /
# Chỉnh sửa dòng 3 thành Bot Token của bạn
# Chỉnh sửa dòng 4,5 thành ID của bạn và ID nhóm, lấy thông tin này bằng cách sử dụng /ping
# Chỉnh sửa dòng 8~12 thành thông tin kết nối MySQL của bạn
# Chỉnh sửa dòng 14 nếu bạn cần kết nối SSH đến cơ sở dữ liệu
# Chỉnh sửa dòng 15~24 thành thông tin kết nối SSH của bạn
python3 bot.py
```

## Yêu cầu mã thông báo telegram bot

1. Truy cập [https://t.me/BotFather](https://https://t.me/BotFather) trong phần tin nhắn riêng
2. Nhập `/newbot`, và đặt tên cho bot của bạn
3. Tiếp theo, đặt tên người dùng cho bot của bạn, nhưng phải kết thúc bằng "bot", ví dụ: `AikoPanel_bot`
4. Cuối cùng, bạn sẽ nhận được mã thông báo của bot, nó sẽ trông giống như thế này: `123456789:gaefadklwdqojdoiqwjdiwqdo`


#### Giải thích biến môi trường
Khi không gắn kết tệp config.yaml vào container, entrypoint.sh sẽ tạo ra tệp config.yml dựa trên các biến môi trường.  
Chú ý: Hình ảnh xây dựng bằng distroless hiện tại không hỗ trợ tạo tệp cấu hình từ các biến môi trường.
| Tùy chọn/Tham số              | Giải thích                                                                                                                                                                                           |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| BOT_WEBSITE            | Địa chỉ AikoPanel<br>Ví dụ: https://awesomeAikoPanel.com                                                                                                                                               |
| BOT_TOKEN              |                                                                                                                                                                                                   |
| BOT_ADMIN_PATH         | Đường dẫn quản trị AikoPanel<br>Ví dụ: admin                                                                                                                                                                  |
| BOT_ADMIN_ID           | Telegram ID của người quản trị, cách nhau bằng dấu phẩy ",".<br>Ví dụ: 123456789,321654987,555555,111222                                                                                                                |
| BOT_GROUP_ID           | Telegram ID của nhóm                                                                                                                                                              |
| AikoPanel_DB_IP          | Địa chỉ IP có thể truy cập cơ sở dữ liệu AikoPanel<br>Khi bot và cơ sở dữ liệu AikoPanel cùng được triển khai trên cùng một máy chủ, hãy xem thêm [2.6 Giải thích đặc biệt](#26-giải-thích-đặc-biệt)                                                                                                 |
| AikoPanel_DB_PORT        | Cổng có thể truy cập cơ sở dữ liệu AikoPanel                                                                                                                                                                         |
| AikoPanel_DB_USER        | Tên người dùng có thể truy cập cơ sở dữ liệu AikoPanel                                                                                                                                                                       |
| AikoPanel_DB_PASS        | Mật khẩu người dùng có thể truy cập cơ sở dữ liệu AikoPanel                                                                                                                                                                     |
| AikoPanel_DB_NAME        | Tên cơ sở dữ liệu AikoPanel                                                                                                                                                                                 |
| AikoPanel_DB_SSH_ENABLE  | Bật/tắt kết nối cơ sở dữ liệu qua SSH.<br>Các giá trị có thể chọn: true / false                                                                                                                                             |
| AikoPanel_DB_SSH_TYPE    | Phương thức xác thực SSH.<br>Các giá trị có thể chọn: passwd / pkey<br>Khi giá trị là passwd, sẽ sử dụng mật khẩu để xác thực, các biến AikoPanel_DB_SSH_KEY và AikoPanel_DB_SSH_KEYPASS sẽ không có hiệu lực.<br>Khi giá trị là pkey, sẽ sử dụng khóa riêng để xác thực, biến AikoPanel_DB_SSH_PASS sẽ không có hiệu lực. |
| AikoPanel_DB_SSH_IP      | Địa chỉ IP của máy chủ cơ sở dữ liệu.<br>Khi bot và cơ sở dữ liệu AikoPanel cùng được triển khai trên cùng một máy chủ, hãy xem thêm [2.6 Giải thích đặc biệt](#26-giải-thích-đặc-biệt)                                                                                                    |
| AikoPanel_DB_SSH_PORT    | Cổng có thể kết nối SSH với máy chủ cơ sở dữ liệu                                                                                                                                                                   |
| AikoPanel_DB_SSH_USER    | Tên người dùng để thiết lập kết nối SSH                                                                                                                                                                           |
| AikoPanel_DB_SSH_PASS    | Mật khẩu người dùng để thiết lập kết nối SSH                                                                                                                                                                         |
| AikoPanel_DB_SSH_KEY     | Nội dung mã khóa private để thiết lập kết nối SSH. Lưu ý rằng khi cấu hình này, bạn cần:<br>1. Không xóa "\|\-" ở đầu dòng;<br>2. Chú ý lề thụt.                                                                                                   |
| AikoPanel_DB_SSH_KEYPASS | Mật khẩu cho khóa riêng khi kết nối SSH, để trống nếu không có mật khẩu                                                                                                                                                         |
| ENHANCED_ENABLE        | Bật/tắt chế độ nâng cao                                                                                                                                                                                      |
| ENHANCED_MODULE        | Các module nâng cao được bật, hiện tại chỉ có module nâng cao cho đơn hàng được hỗ trợ, thông tin sẽ được lưu trong hai bảng của cơ sở dữ liệu AikoPanel để lưu trạng thái đẩy, có thể tự động cập nhật hoặc không.                   |

#### Giải thích đặc biệt
Khi bot và cơ sở dữ liệu AikoPanel được triển khai trên cùng một máy chủ, do network driver của docker container mặc định là bridge, bot sẽ không thể truy cập cơ sở dữ liệu trực tiếp thông qua địa chỉ Loopback (127.0.0.1/localhost/::1, v.v.). Dưới đây là một số giải pháp để lựa chọn:  
1. Sử dụng kết nối SSH để kết nối cơ sở dữ liệu
    Xem chi tiết tại [Sử dụng thông thường](#sử-dụng-thông-thường).  
    Trong đó, địa chỉ IP SSH cần được đặt là: host.docker.internal  
    Đặt địa chỉ IP cơ sở dữ liệu là: 127.0.0.1
**Độ cách ly: Giải pháp 1 > Giải pháp 2, Độ phổ biến: Giải pháp 1 < Giải pháp 2**, nên sử dụng giải pháp 1.  
Ngoài ra, vì lý do an ninh, không khuyến khích cơ sở dữ liệu lắng nghe trên 0.0.0.0.
