
import platform


import mainsrk


if platform.platform().startswith('Linux'):
    try:
        import readline
    except:
        pass
try:
    mainsrk.superr()
except:
    if input('Q:Restart E:Exit') == 'Q':
        mainsrk.superr()
