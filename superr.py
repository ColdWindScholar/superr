
import platform


import mainsrk


if platform.platform().startswith('Linux'):
    try:
        import readline
    except:
        pass
try:
    mainsrk.superr()
except (BaseException) as e:
    if input(f'{e}\nQ:Restart E:Exit') == 'Q':
        mainsrk.superr()
