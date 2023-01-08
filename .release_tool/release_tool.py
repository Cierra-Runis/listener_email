'''
发布用脚本
release_tool.py
'''

import os
import re
import shutil


class FileDir():
    '''
    存储需要的文件地址
    '''
    PYPROJECT_TOML: str = r'pyproject.toml'
    DIST: str = r'dist/'


class RegexStr():
    '''
    储存需要的正则表达式字符串\n
    '''
    VERSION: str = r'(\d+)\.(\d+)\.(\d+)'
    PYPROJECT_TOML: str = r'version = "(\d+\.\d+\.\d+)"'


def input_tool(
    first_message: str,
    rule: str,
    error_message: str,
    rule_function: any,
) -> str:
    '''
    根据 rule_function 获取合法的值
    '''
    # 提醒
    print(f'> {first_message} {rule}: ', end='')
    # 第一次输入
    input_str = input()
    # 当 rule_function(input_str) 返回 false
    # 即不合法时
    while not rule_function(input_str):
        # 重新提醒并输入
        print(f'> {error_message}')
        print(f'> {first_message} {rule}: ', end='')
        input_str = input()
    # 直至输入合法
    return input_str


def rewrite_tool(file_dir: str, reg: str, repl: str) -> None:
    '''
    改写用辅助函数
    '''
    file = open(file_dir, 'r+', encoding='utf-8')
    text = file.read()
    file.seek(0, 0)
    text = re.sub(reg, repl, text)
    file.write(text)
    file.close()


def is_new_version_legal(current_version: str, new_version: str) -> bool:
    '''
    比较版本号大小, 两字符串格式类似 1.0.0
    '''
    current = re.match(RegexStr.VERSION, current_version)
    new = re.match(RegexStr.VERSION, new_version)
    for i in range(1, 4):
        if int(new[i]) > int(current[i]):
            # 从最高级一一对比, 某级新版本若大于旧版本, 则确实新版本大
            # 返回 True
            return True
        if int(new[i]) < int(current[i]):
            # 从最高级一一对比, 某级新版本若小于旧版本, 则是新版本小了
            # 返回 False
            return False
    # 运行到这说明俩版本号一样大, 即重新构建该版本
    # 返回 True
    return True


def get_version_from_pyproject_toml() -> str:
    '''
    从 pyproject.toml 文件中获取当前版本的字符串
    '''
    with open(FileDir.PYPROJECT_TOML, 'r', encoding='utf-8') as file:
        text = file.read()
    return re.search(RegexStr.PYPROJECT_TOML, text).group(1)


def rewrite_current_version_str_in_pubspec_yaml(new_version: str) -> None:
    '''
    修改 pyproject.toml 文件中的版本号
    '''
    rewrite_tool(
        file_dir=FileDir.PYPROJECT_TOML,
        reg=RegexStr.PYPROJECT_TOML,
        repl=f'version = "{new_version}"',
    )


def main_module() -> None:
    '''
    主模块
    '''
    print('-- main module --')

    current_version_str = get_version_from_pyproject_toml()
    input_str = ''

    print(f'> 当前版本为 {current_version_str}')

    input_str = input_tool(
        first_message=f'是否修改版本 {current_version_str}',
        rule='(y/n)',
        error_message='请只输入 y 或 n',
        rule_function=lambda input_str: input_str == 'y' or input_str == 'n',
    )

    if input_str == 'y':

        input_str = input_tool(
            first_message='请输入版本号',
            rule='',
            error_message='请确认版本号格式',
            rule_function=lambda input_str: re.search(
                RegexStr.VERSION,
                input_str,
            ),
        )

        # 当新版本号不合法时
        while not is_new_version_legal(current_version_str, input_str):
            # 重新提醒并输入
            print(f'> 请使得新输入的版本号 {input_str} 不小于旧版本号 {current_version_str}')
            input_str = input_tool(
                first_message='请输入版本号',
                rule='',
                error_message='请确认版本号格式',
                rule_function=lambda input_str: re.search(
                    RegexStr.VERSION,
                    input_str,
                ),
            )
        # 直至新版本号合法

        # 写入新版本号至 pyproject.toml 文件
        rewrite_current_version_str_in_pubspec_yaml(input_str)
        shutil.rmtree(FileDir.DIST)
        os.system('python -m build')

        # 当更新了版本号
        if input_str != current_version_str:
            # 才能考虑是否发布
            current_version_str = input_str

            input_str = input_tool(
                first_message=f'是否发布当前版本 {current_version_str}',
                rule='(y/n)',
                error_message='请只输入 y 或 n',
                rule_function=lambda input_str: input_str == 'y' or input_str
                == 'n',
            )
            # 若输入的是 'y'
            if input_str == 'y':
                release_module()
            else:
                # 反之输入的不是 'y'
                print('> 已取消发布')
        else:
            print('> 只有当更新了版本号才能考虑是否发布')

    else:
        # 反之输入的不是 'y'
        print('> 已取消更改版本号')


def release_module() -> None:
    '''
    发布模块
    '''
    print('-- release module --')

    current_version_str = get_version_from_pyproject_toml()

    print(f'> 正在发布{current_version_str}')
    os.system('python -m twine upload --repository pypi dist/*')
    print(f'> 已发布 v{current_version_str}')


if __name__ == '__main__':
    os.system('cls')

    main_module()
