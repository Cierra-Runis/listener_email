'''
example
'''

from listener_email import sent_email, ListenerEmail

if __name__ == '__main__':
    new = '225'
    custom_html = f'''
        <p>
            Osu 测试通道已更新为
            <a href="https://testflight.apple.com/join/{new}">
            https://testflight.apple.com/join/{new}
            </a>
        </p>
        <p>
            详见
            <a href="https://osu.ppy.sh/home/testflight">
            https://osu.ppy.sh/home/testflight
            </a>
        </p>
        '''
    sent_email(
        email=ListenerEmail(f'{DIR}/email.json'),
        subject='Osu 测试通道已更新！',
        name='osu_testflight_listener',
        custom_html=custom_html,
        lang='zh-CN',
    )
