'''
Listener Email Example
example.py
'''

import os
from listener_email import sent_email, ListenerEmail

DIR = os.path.dirname(__file__)

if __name__ == '__main__':
    new = '3CsFhZUi'
    custom_html = f'''
        <p>
            Osu testflight link changed to
            <a href="https://testflight.apple.com/join/{new}">
                https://testflight.apple.com/join/{new}
            </a>
        </p>
        <p>
            More information at
            <a href="https://osu.ppy.sh/home/testflight">
                https://osu.ppy.sh/home/testflight
            </a>
        </p>
        '''
    sent_email(
        # please add email.json by yourself
        email=ListenerEmail(f'{DIR}/email.json'),
        subject='Osu testflight link changed',
        name='osu_testflight_listener',
        custom_html=custom_html,
        lang='zh-CN',
    )
