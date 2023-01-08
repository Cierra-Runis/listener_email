"""
Listener Email - Remind you of changes in your listener through email! Base use:\n
"""

__version__ = '0.0.1'
__all__ = [
    'sent_email',
]

__author__ = 'Cierra_Runis <byrdsaron@gmail.com>'

import datetime
from email.mime.text import MIMEText
import json
import os
import re
import smtplib

DIR = os.path.dirname(__file__)


class RegexPattern():
    '''
    Store regex pattern\n
    '''
    CONTENT_CELL: str = re.compile(
        r'<td id="content-cell" align="left">\n([\s\S]*?)\n.*</td>')
    COPYRIGHT: str = re.compile(
        r'<td id="copyright-cell" colspan="2" align="center">\n([\s\S]*?)\n.*</td>'
    )


class ListenerEmail():
    '''
    Store email config\n
    '''
    mail_host: str
    mail_user: str
    mail_pass: str
    sender: str
    receivers: list

    def __init__(self, email_json_path: str) -> None:
        '''
        `email_json_dir` : path of email config json file\n
        '''
        try:
            f = open(email_json_path, 'r', encoding='utf-8')
            email_json = json.loads(f.read())
            self.mail_host = email_json['mail_host']
            self.mail_user = email_json['mail_user']
            self.mail_pass = email_json['mail_pass']
            self.sender = email_json['sender']
            self.receivers = email_json['receivers']
            f.close()
            print('> Configuring ListenerEmail success')
        except Exception as e:
            print(f'> Configuring ListenerEmail fail: {e}')


def get_content_cell_by_lang(lang: str) -> str:
    '''
    Get content cell by language
    '''
    if lang == 'zh-CN':
        return '''
            <p>你好 {} ！</p>
            {}
            <p>
                如果您未订阅本提醒服务，请与 <a href="mailto:{}"> 服务订阅者</a> 联系。
            </p>
            '''
    elif lang == 'jp':
        return '''
            <p>こんにちは {} ！</p>
            {}
            <p>
                このリマインダサービスを購読していない場合は、<a href="mailto:{}">サービス購読者</a> にお問い合わせください。
            </p>
            '''
    else:
        return '''
            <p>Hello {} !</p>
            {}
            <p>
                If you didn't subscribe this remind service, please contact with <a href="mailto:{}">service subscriber</a> .
            </p>
            '''


def get_copyright_by_lang(lang: str) -> str:
    '''
    Get copyright by language
    '''
    if lang == 'zh-CN':
        return '''
            <div>
                Copyright ©2022-{} by
                <a href="https://github.com/Cierra-Runis">Cierra_Runis</a>
                保留所有权利
            </div>
            '''
    else:
        return '''
            <div>
                Copyright ©2022-{} by
                <a href="https://github.com/Cierra-Runis">Cierra_Runis</a>
                All rights reserved
            </div>
            '''


def sent_email(
    email: ListenerEmail,
    subject: str,
    name: str,
    custom_html: str,
    lang: str = 'en',
) -> None:
    '''
    Sent email\n
    `email` Configured ListenerEmail\n
    `subject` Email subject\n
    `name` Sender name\n
    `custom_html` Custom html\n
    `lang` Language of email chose in `'zh-CN'`, `'jp'`, `'en'` \n
    '''

    for receiver in email.receivers:
        content_cell = get_content_cell_by_lang(lang).format(
            receiver,
            custom_html,
            email.sender,
        )
        copyright_cell = get_copyright_by_lang(lang).format(
            datetime.datetime.today().year)

        raw_html = open(f'{DIR}/email.html', 'r', encoding='utf-8').read()

        raw_html = RegexPattern.CONTENT_CELL.sub(
            f'<td id="content-cell" align="left">\n{content_cell}\n</td>',
            raw_html,
        )

        raw_html = RegexPattern.COPYRIGHT.sub(
            f'<td id="copyright-cell" colspan="2" align="center">\n{copyright_cell}\n</td>',
            raw_html,
        )

        message = MIMEText(raw_html, 'html', 'utf-8')
        message['Subject'] = subject
        message['From'] = f'{name} <{email.sender}>'
        message['To'] = receiver

        try:
            smtp_obj = smtplib.SMTP_SSL(email.mail_host)
            smtp_obj.login(email.mail_user, email.mail_pass)
            smtp_obj.send_message(message)
            smtp_obj.quit()
            print(f'> Sending to {receiver} success')
        except smtplib.SMTPException as error:
            # 打印错误
            print(f'> Sending to {receiver} fail: {error}')
