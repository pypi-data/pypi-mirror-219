
from ctypes import Union
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from bbat.date import date_diff
import requests

def send_email(subject="", msg= "", receivers: Union[str, list] = 'meutils@qq.com', _subtype='html', msg_prefix='', msg_suffix='', msg_fn=lambda x: x, date=date_diff(days=0), host2sender=None, **kwargs):
    """
    Args
        subject: 主题
        msg:
        receivers:
        _subtype:
        msg_prefix:
        msg_suffix:
        msg_fn:
        kwargs:
    """

    # init
    # token = get_zk_config("/push/email_token")
    # host, sender = list(token.items())[0]
    if host2sender is None:
        host2sender = {'localhost': 'BOT'}

    host, sender = list(host2sender.items())[0]
    smtp = smtplib.SMTP(host, 25)

    # 主题+内容
    subject = f"👉{subject}📅{date}"

    msg = f"{msg_prefix}{msg_fn(msg)}{msg_suffix}"

    message = MIMEText(msg, _subtype, 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = sender

    if isinstance(receivers, str) and receivers.__contains__("@"):
        receivers = [receivers]
    message['To'] = ",".join(receivers)

    try:
        smtp.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(f"{e}: 无法发送邮件")



def send_feishu(url, text):
    headers = {'Content-type': 'application/json'}
    msg = {
        "msg_type": "text",
        "content": {
            "text": text
        }
    }
    requests.post(url, headers=headers, json=msg)


if __name__ == '__main__':
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/db624271-9150-4ce6-be31-90d5a5b5c5e2"
    send_feishu(hook_url='')

    send_email("测试邮件", msg='邮件内容')
