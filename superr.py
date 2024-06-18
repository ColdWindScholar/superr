import mainsrk

try:
    import readline
except:
    pass

try:
    mainsrk.superr()
except (BaseException) as e:
    if input(f'{e}\nQ:Restart E:Exit') == 'Q':
        mainsrk.superr()
