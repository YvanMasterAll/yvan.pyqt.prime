import subprocess, os
from common.util.storage import LocalStorage

'''
资源生成器
https://my.oschina.net/flywuya/blog/1811669
'''

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_qrc(with_skin=True):
    # 1).主题列表
    themes = LocalStorage.themeAllGet()
    for theme in themes:
        # 2).皮肤资源
        if with_skin:
            generate_skin(theme)
        # 3).界面资源
        generate_style(theme)

def generate_skin(theme):
    icons = os.listdir('./img/{theme}/skin'.format(theme=theme))
    qrc = './qss/theme/{theme}/skin.qrc'.format(theme=theme)
    py = './qss/theme/{theme}/skin_rc.py'.format(theme=theme)
    with open(qrc, 'w+') as f:
        f.write(u'<!DOCTYPE RCC>\n<RCC version="1.0">\n<qresource prefix="qss_icons">\n')
        for item in icons:
            f.write(u'<file alias="rc/{item}">../../../img/{theme}/skin/{item}</file>\n'.format(item=item, theme=theme))
        f.write(u'</qresource>\n</RCC>')
        f.close()

    src = os.path.join(BASE_DIR, qrc)
    dst = os.path.join(BASE_DIR, py)
    os.system(f'pyrcc5 {src} -o {dst}')

def generate_style(theme):
    icons = os.listdir('./img/{theme}/icon'.format(theme=theme))
    fonts = os.listdir('./font'.format(theme=theme))
    qrc = './qss/theme/{theme}/style.qrc'.format(theme=theme)
    py = './qss/theme/{theme}/style_rc.py'.format(theme=theme)
    with open(qrc, 'w+') as f:
        f.write(u'<!DOCTYPE RCC>\n<RCC version="1.0">\n<qresource>\n')
        for item in icons:
            f.write(u'<file alias="icon/{item}">../../../img/{theme}/icon/{item}</file>\n'.format(item=item, theme=theme))
        for item in fonts:
            # 不打包雅黑字体，字体打包体积大
            if item != 'Microsoft-YaHei.ttf' and item != 'Roboto-Regular.ttf':
                f.write(u'<file alias="font/{item}">../../../font/{item}</file>\n'.format(item=item, theme=theme))
        f.write(u'</qresource>\n</RCC>')
        f.close()

    src = os.path.join(BASE_DIR, qrc)
    dst = os.path.join(BASE_DIR, py)
    os.system(f'pyrcc5 {src} -o {dst}')

if __name__ == '__main__':
    # generate_qrc(with_skin=True)
    generate_qrc(with_skin=False)










