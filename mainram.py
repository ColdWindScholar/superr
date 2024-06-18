#!/usr/bin/env python3

import os
import re
import sys


def ramdisk(j, base, func, romname, filetype, action, extra):
    color = j.color
    rd = j.bd + os.sep + 'superr_' + romname
    prfiles = rd + os.sep + '00_project_files'
    uconf = prfiles + os.sep + 'srk.conf'
    bootdir = rd + os.sep + filetype + 'img'

    lang = j.getlang(j.getconf('language', j.mconf) + '_srk.py')

    if j.platf == 'win':
        import colorama
        colorama.init()

        seinject = j.tools + os.sep + 'win_tools' + os.sep + 'bootimg.exe seinject'
    else:
        if j.platf == 'mac':
            seinject = j.tools + '/mac_tools/bootimg seinject'
        elif j.platf in ['lin', 'wsl', 'wsl2']:
            seinject = j.tools + '/linux_tools/bootimg seinject'
        else:
            print('Unknown platform')
            sys.exit()

    if (j.existf(rd + '/system/init.rc')
            or j.existf(rd + '/system/init.environ.rc')):
        ramdir = rd + '/system'
    else:
        ramdir = bootdir + '/ramdisk'

    dfprop = 'bad'
    with j.cd(rd):
        proplist = sorted(j.greps('prop', j.greps('default', j.findr('**'))))
        for i in proplist:
            if j.grepf('secure', i):
                dfprop = rd + os.sep + i
                break

    def byname1(keep=None):
        if ffstab == 1:
            return
        bytest = {'/KERNEL': 'kerbyname', '/system': 'regbyname', '/SYSTEM': 'capbyname', '/APP': 'appbyname',
                  '/userdata': 'datbyname'}
        for i in list(bytest):
            bntest = j.grepf(j.fl('/by-name' + i, '^#'), ffstab[0])
            if bntest:
                byname = bntest[0].split()
                byname = byname[0].replace(i, '')
                j.appendf('0', deviceloc + '/superr_' + bytest[i])
                j.appendf(byname, deviceloc + '/superr_byname')
                with j.cd(deviceloc):
                    for a in j.findf('*'):
                        j.chown(a)
                break

        if not keep:
            j.delpath(bootdir)

    def delram():
        j.delpath(bootdir)

    def deopatch():
        with j.cd(rd):
            sepol = j.greps(j.fl('', '.*test|.*txt|.*mapping|.*00_project_files'), j.findr('**/*sepolicy*'))
            if sepol:
                for i in sepol:
                    omd5 = j.md5chk(i)
                    if i.endswith('.cil'):
                        line = j.greps('\(allow zygote.* dalvikcache_data_file.* \(file \(', j.readfl(i))
                        if line:
                            for e in line:
                                if not 'execute' in e:
                                    nline = e.replace(')))', ' execute)))')
                                    j.sedf(e.replace('(', '\(').replace(')', '\)'), nline, i)
                        else:
                            zname = j.grepf('\(allow zygote.*', i)
                            dname = j.grepf('\(allow .*dalvikcache_data_file.*', i)
                            if zname and dname:
                                znames = []
                                for z in zname:
                                    line = z.split()[1]
                                    if line not in znames:
                                        znames.append(line)
                                dnames = []
                                for d in dname:
                                    line = d.split()[2]
                                    if line not in dnames:
                                        dnames.append(line)
                                for z in znames:
                                    for d in dnames:
                                        j.appendf('(allow ' + z + ' ' + d + ' (file (execute)))', i)
                    else:
                        dumpf = j.cmd(seinject + ' -dt -P ' + i).splitlines()
                        dname = j.greps('ALLOW.*dalvikcache_data_file.*', dumpf)
                        zname = j.greps('ALLOW zygote.*', dumpf)
                        if zname and dname:
                            znames = []
                            for z in zname:
                                line = z.split()[2]
                                if line not in znames:
                                    znames.append(line)
                            dnames = []
                            for d in dname:
                                line = d.split()[4]
                                if line not in dnames:
                                    dnames.append(line)
                            for z in znames:
                                for d in dnames:
                                    j.cmd(
                                        seinject + ' -s ' + z + ' -t ' + d + ' -c file -p execute -P ' + i + ' -o ' + i)
                        else:
                            j.cmd(
                                seinject + ' -s zygote -t dalvikcache_data_file -c file -p execute -P ' + i + ' -o ' + i)

                    if j.md5chk(i) != omd5:
                        j.chown(i)
                        print('patched: ' + i)
                    else:
                        print('patch failed: ' + i)
            else:
                print('sepolicy not found')

    def dmverity(vstatus=None):
        if j.existf(bootdir + '/split_img/' + filetype + '.img-zImage'):
            fnames = [bootdir + '/split_img/' + filetype + '.img-zImage']
        elif j.existf(rd + '/kernel.img'):
            fnames = [rd + '/kernel.img']
            if j.existf(rd + '/dtb.img'):
                fnames.append(rd + '/dtb.img')
        else:
            fnames = []

        if ffstab != 1:
            for i in ffstab:
                fnames.append(i)

        vstatchk = None
        for filename in fnames:
            with open(filename, 'rb') as f:
                data = f.read()

            thechk = []
            for x in [b',verify', b',avb']:
                if re.search(x, data):
                    thechk.append(x)

            if not thechk:
                continue

            if vstatus:
                vstatchk = 1
                continue
            else:
                for x in thechk:
                    result = {}

                    with open(filename, 'rb') as f:
                        data = f.read()

                    for i in re.finditer(x, data):
                        begin = i.start()
                        bnum = len(x)
                        while True:
                            if data[begin + bnum] == 0:
                                result[data[begin:bnum + begin]] = b'\x00' * bnum
                                break
                            elif data[begin + bnum:begin + bnum + 1] == b'\n':
                                result[data[begin:bnum + begin]] = b''
                                break
                            elif data[begin + bnum:begin + bnum + 1] == b',':
                                result[data[begin:bnum + begin]] = b''
                                break
                            else:
                                bnum = bnum + 1

                    for swap in list(result):
                        data = data.replace(swap, result[swap])

                    with open(filename + '_new', 'wb') as o:
                        devnull = o.write(data)
                    os.replace(filename + '_new', filename)

                    if j.platf != 'win':
                        if not 'bootimg' in filename and not 'recoveryimg' in filename:
                            j.chown(filename)

        if vstatus:
            if vstatchk:
                return 'yes'
            else:
                return 'no'

    def forcee():
        if ffstab == 1:
            return

        for ff in ffstab:
            fetmp = j.grepf(j.fl('/data', '^#'), ff)
            fetest = j.greps('.*forceencrypt|.*forcefdeorfbe|.*fileencryption', fetmp)
            feuntest = j.greps('encryptable', fetmp)

            fetmp = ['forceencrypt', 'forcefdeorfbe', 'fileencryption']
            if fetest:
                for i in fetmp:
                    if j.greps('.*' + i, fetest):
                        j.getconf('forcee', uconf, add=i)
                        j.sedf(i, 'encryptable', ff)

                j.chown(uconf)
            elif feuntest:
                fvar = j.getconf('forcee', uconf)
                if fvar:
                    j.sedf('encryptable', fvar, ff)

            if j.platf != 'win':
                if not 'bootimg' in ff and not 'recoveryimg' in ff:
                    j.chown(ff)

    def fstab(filekind):
        if filekind == 'boot':
            fstdir = None
            for i in [rd + '/system', bootdir + '/ramdisk', rd + '/system/vendor/etc', rd + '/vendor/etc']:
                newfstab = j.findf(i + os.sep + '*fstab*')
                if newfstab:
                    fstdir = i
                    break
            if not fstdir:
                return 1
        else:
            fstdir = None
            for i in j.findr(bootdir + '/ramdisk/**/*fstab*'):
                fstdir = j.dirname(i).replace('/', os.sep)
                break
            if not fstdir:
                return 1

        with j.cd(fstdir):
            ffstab1 = []
            fstmp = j.greps(j.fl('',
                                 '.*goldfish.*|.*ranchu.*|.*charger.*|.*\.fwup|.*zram.*|.*nodata.*|.*\.fota|.*mofd_v1.*|.*\.ftm\.|.*\.sdboot'),
                            j.findf('*fstab*'))

            for d in fstmp:
                if os.path.islink(d):
                    fstmp.remove(d)

            if len(fstmp) < 1:
                ffstab1 = 1
            else:
                for i in fstmp:
                    if j.grepf(j.fl('/system', '^#'), i):
                        ffstab1.append(str(fstdir + os.sep + i))

                if not ffstab1:
                    for i in fstmp:
                        if j.grepf(j.fl('/data', '^#'), i):
                            ffstab1.append(str(fstdir + os.sep + i))

            return ffstab1

    def insecure(filekind):
        status = j.readfl(prfiles + '/statusfile')
        insecstatus = status[2].split('=')[0]

        if insecstatus == 'No':
            if j.grepf('ro.secure=1', dfprop):
                j.sedf('ro.secure=1', 'ro.secure=0', dfprop)
            else:
                j.awkadd('^#', 'ro.secure=0', 'after', 'last', dfprop)

            if j.grepf('ro.adb.secure=1', dfprop):
                j.sedf('ro.adb.secure=1', 'ro.adb.secure=0', dfprop)
            else:
                j.awkadd('ro.secure=0', 'ro.adb.secure=0', 'after', 'last', dfprop)

            return
        else:
            j.sedf('ro.secure=0', 'ro.secure=1', dfprop)
            j.sedf('ro.adb.secure=0', 'ro.adb.secure=1', dfprop)

        if j.platf != 'win':
            if 'bootimg' not in dfprop and 'recoveryimg' not in dfprop:
                j.chown(dfprop)

    def isdmverity():
        vdtb = None
        isver = None
        if j.existd(ramdir):
            vdtb = dmverity('status')
            if ffstab != 1:
                for i in ffstab:
                    if j.grepf('verify|avb', i):
                        isver = 1

        if isver or vdtb == 'yes':
            j.appendf('Yes=' + color['r'] + lang['enabled'] + color['n'], prfiles + '/statusfile')
        else:
            j.appendf('No=' + color['g'] + lang['disabled'] + color['n'], prfiles + '/statusfile')

    def isforcee():
        if ffstab == 1:
            j.appendf('No=' + color['r'] + 'N/A' + color['n'], prfiles + '/statusfile')
            return

        fetest1 = None
        if j.existd(ramdir):
            for i in ffstab:
                fetest = j.grepf(j.fl('/data', '^#'), i)
                if j.greps('.*forceencrypt|.*forcefdeorfbe|.*fileencryption', fetest):
                    fetest1 = 1

        if fetest1:
            j.appendf('Yes=' + color['r'] + lang['enabled'] + color['n'], prfiles + '/statusfile')
        else:
            j.appendf('No=' + color['g'] + lang['disabled'] + color['n'], prfiles + '/statusfile')

    def isinsecure():
        if j.existf(dfprop):
            if not j.grepf('ro.secure=0', dfprop):
                j.appendf('No=' + color['r'] + lang['secure'] + color['n'], prfiles + '/statusfile')
            else:
                j.appendf('Yes=' + color['g'] + lang['insecure'] + color['n'], prfiles + '/statusfile')
        else:
            j.appendf('No=' + color['r'] + 'N/A' + color['n'], prfiles + '/statusfile')

    def mmc():
        if ffstab == 1:
            return

        mmctest = j.greps(j.fl('', '^#'), j.readfl(ffstab[0]))
        for i in ['/system', '/boot', '/data', '/cache', '/recovery', '/modem', '/vendor']:
            cline = []
            tline = j.greps(i, mmctest)
            for a in tline:
                a = a.split()
                if not j.greps('^' + i + '$', a):
                    continue
                cline = a
                break
            if not cline:
                continue

            if j.greps('/dev/', cline):
                j.appendf(j.greps('/dev/', cline)[0] + ' ' + i, deviceloc + '/superr_mmc')
            elif j.greps(i[1:], cline):
                j.appendf(j.greps(i[1:], cline)[0] + ' ' + i, deviceloc + '/superr_mmc')

            with j.cd(deviceloc):
                for a in j.findf('*'):
                    j.chown(a)

    devicename = j.getconf('devicename', uconf)
    if devicename:
        deviceloc = j.tools + '/devices/' + devicename
    else:
        deviceloc = ''

    if j.existd(ramdir):
        with j.cd(ramdir):
            ffstab = fstab(filetype)

    if func == 'delram':
        delram()
    elif func == 'dmverity':
        dmverity()
    elif func == 'byname':
        byname1()
    elif func == 'mmc':
        mmc()
    elif func == 'insecure':
        insecure(filetype)
    elif func == 'forcee':
        forcee()
    elif func == 'deopatch':
        deopatch()
    elif func == 'status':
        j.delpath(prfiles + '/statusfile')
        j.touch(prfiles + '/statusfile')
        isdmverity()
        isforcee()
        isinsecure()
