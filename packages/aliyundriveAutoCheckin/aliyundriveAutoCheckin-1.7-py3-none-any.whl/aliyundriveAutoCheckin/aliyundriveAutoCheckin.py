import requests
import json
import smtplib
import msvcrt
from email.mime.text import MIMEText
from datetime import datetime


print("by:xiaohan17")
print("TG(若下方群失效,可以联系):https://t.me/ZYK615")
print("TG群:https://t.me/ikun9882")
print("----------------------------------------------------")
print("----------------------------------------------------")

# 读取 txt 文件
with open("阿里云盘签到.txt", "r", encoding='utf-8') as f:
    lines = f.readlines()

# 对每一行进行处理
for line in lines:
    data = line.strip().split(',')
    print(data)  # 打印整行数据
    print(len(data))  # 打印字段数量
    refresh_token, is_get_reward, is_send_email, is_custom_email, to_addr = data[:5]
    email_content = ""  # 初始化邮件内容

    if refresh_token != "":
        try:
            # 发起网络请求-获取token
            response = requests.post(
                "https://auth.aliyundrive.com/v2/account/token",
                json={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token
                }
            )
            response.raise_for_status()  # 如果响应状态码不是200，引发HTTPError异常
        except requests.HTTPError as e:
            email_content += f"获取token时出错，HTTP状态码：{e.response.status_code}\n"
            continue
        except requests.RequestException as e:
            email_content += f"获取token时出错，错误信息：{str(e)}\n"
            continue

        response_data = response.json()
        access_token = response_data.get('access_token')
        user_name = response_data.get("user_name")

        if access_token is None:
            email_content += f"token值错误，程序执行失败，请重新复制正确的token值\n"
            continue

        headers = {'Authorization': 'Bearer ' + access_token}

        # 签到
        try:
            response = requests.post(
                "https://member.aliyundrive.com/v1/activity/sign_in_list",
                json={"_rx-s": "mobile"},
                headers=headers
            )
            response.raise_for_status()
        except requests.HTTPError as e:
            email_content += f"签到时出错，HTTP状态码：{e.response.status_code}\n"
            continue
        except requests.RequestException as e:
            email_content += f"签到时出错，错误信息：{str(e)}\n"
            continue

        response_data = response.json()
        signin_count = response_data['result']['signInCount']
        email_content += f"账号：{user_name}-签到成功, 本月累计签到{signin_count}天\n"

        # 领取奖励
        if is_get_reward == "是":
            try:
                response = requests.post(
                    "https://member.aliyundrive.com/v1/activity/sign_in_reward?_rx-s=mobile",
                    json={"signInDay": signin_count},
                    headers=headers
                )
                response.raise_for_status()
            except requests.HTTPError as e:
                email_content += f"领奖时出错，HTTP状态码：{e.response.status_code}\n"
                continue
            except requests.RequestException as e:
                email_content += f"领奖时出错，错误信息：{str(e)}\n"
                continue

            response_data = response.json()
            email_content += f"本次签到获得{response_data['result']['name']}, {response_data['result']['description']}\n"

    # 发送邮件
    if is_send_email == "是":
        if is_custom_email == "是":
            smtp_server = data[5]
            smtp_port = data[6]
            smtp_user = data[7]
            smtp_password = data[8]
        else:
            smtp_server = "smtp.163.com"
            smtp_port = 465
            smtp_user = "fs8484848@163.com"
            smtp_password = "QADSEMPKDHDAVWVD"

        subject = "阿里云盘签到通知"

        msg = MIMEText(email_content)
        msg['Subject'] = subject
        msg['From'] = smtp_user
        msg['To'] = to_addr

        try:
            server = smtplib.SMTP_SSL(smtp_server, int(smtp_port))
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, [to_addr], msg.as_string())
            server.quit()
        except smtplib.SMTPException as e:
            print(f"发送邮件时出错，错误信息：{str(e)}")
            continue

    # 获取当前时间
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 将结果和当前时间输出到文件
    with open('output.txt', 'a', encoding='utf-8') as f:
        f.write(f'{current_time}\n{email_content}\n')

print("")
print("结果可在在文件夹的output.txt中或者邮箱中查看")
print("")
print("按任意键退出...")
msvcrt.getch()
