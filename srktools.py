import argparse
import base64
import glob
import hashlib
import itertools
import math
import os
import platform
import re
import struct
import sys
import tarfile
import tempfile
import traceback
import types
import zipfile
from binascii import hexlify
from collections import OrderedDict
from datetime import datetime, timedelta
from shutil import copyfile, copytree, which
from subprocess import Popen, PIPE, STDOUT
from time import sleep
from os.path import basename, dirname
import requests
from cryptography.fernet import Fernet
import lpdump as lpunpack


def adb_byname(deviceloc):
    try:
        byname = cmd(f'{adb} shell "find /dev -name by-name 2>/dev/null"').splitlines()[0].strip()
    except Exception as e:
        appendf(logtb(e), logs + '/adb.log')

    if not byname or 'by-name' not in byname:
        try:
            byname = cmd(
                adb + ' shell su -c "find /dev -name by-name 2>/dev/null"').splitlines()[0].strip()
        except Exception as e:
            appendf(logtb(e), logs + '/adb.log')

    devicename = get_devicename()
    deviceloc = tools + os.sep + 'devices' + os.sep + devicename

    if not byname or 'by-name' not in byname:
        delpath(deviceloc + '/superr_byname')
        appendf('by-name: ' + byname, logs + '/adb.log')
        banner()
        kprint(lang['error'], 'yrbbo')
        kprint(lang['byname_error_device'], 'r')
        kprint(lang['byname_error_device2'] + '\n', 'r')
        input(lang['enter_continue'])
        return 1

    if not existf(deviceloc + '/superr_byname'):
        appendf(byname, deviceloc + '/superr_byname')

    amnt = cmd(adb + ' shell "mount"')
    appendf(amnt, logs + '/adb.log')
    amnt = amnt.splitlines()
    bytest = {'/APP': 'appbyname'}
    for i in bytest.keys():
        if greps('.*' + i, amnt):
            appendf('0', deviceloc + '/superr_' + bytest[i])
            break

    return byname


def appendf(string, fileout):
    if isinstance(string, list):
        with open(fileout, 'a', encoding='utf8', newline='\n') as f:
            for i in string:
                print(i, file=f)
    else:
        with open(fileout, 'a', encoding='utf8', newline='\n') as f:
            print(string, file=f)


def appendff(filein, fileout):
    with open(fileout, 'a', encoding='utf8', newline='\n') as text_file:
        print(readf(filein), file=text_file)


def autorom():
    if existf(prfiles + '/AR-config'):
        return 1
    else:
        return None


def awkadd(searcht, newline, loc, freq, filename):
    awktest = []
    if existf(filename):
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                if re.search(searcht, line):
                    awktest.append(i)
        if awktest:
            countmatch = len(awktest)
            with open(filename, 'r') as f, open(filename + '-tmp', 'w', newline='\n') as ft:
                for i, line in enumerate(f):
                    position = ''
                    if freq == 'last':
                        position = awktest[countmatch - 1]
                    elif freq == 'first':
                        position = awktest[0]
                    elif freq == 'all':
                        if i in awktest:
                            position = i

                    if i == position:
                        if loc == 'after':
                            ft.write('{}{}\n'.format(line, newline))
                        elif loc == 'before':
                            ft.write('{}\n{}'.format(newline, line))
                    else:
                        ft.write(line)
            os.replace(filename + '-tmp', filename)


def awktop(line, filename):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)


def banner(quiet=None):
    if not quiet:
        clears()
        print()
        print('-'.center(tsize, '-'))
        kprint(intro1 + "SuperR's Kitchen".center(tsize))
        kprint(intro2 + 'by SuperR'.center(tsize))
        print('-'.center(tsize, '-'))
        print()


def bencode(thestring):
    return base64.b64encode(thestring.encode('utf-8')).decode('utf-8')


def bbdown(dlurl):
    page = internet(dlurl + '/', 1).splitlines()
    page2 = []
    for i in greps('.*href.*.zip|.*href.*.exe|.*href.*changelog', page):
        page2.append(basename(i.split('"')[1]))

    return sorted(page2)


def boot_pack(filetype, filetype2, bootext=None, quiet=None):
    if not quiet:
        banner()

    if not bootext:
        kprint(lang['boot_repack'] + filetype2 + ' ...\n', 'b')

    bootdir = rd + '/' + filetype + 'img'

    get_devicename()
    if not existf(prfiles + '/' + filetype2 + '_orig/' + filetype2):
        mkdir(prfiles + '/' + filetype2 + '_orig')
        copyfile(rd + '/' + filetype2, prfiles + '/' + filetype2 + '_orig/' + filetype2)

    with cd(bootdir):
        appendf(cmd(issudo2 + AIK + '/repackimg.sh --local'), logs + '/boot.log')
        chown('image-new.img')

        if not existf('image-new.img'):
            if not quiet:
                banner()
                kprint(lang['error'], 'yrbbo')
                kprint(lang['boot_repack_problem'] + filetype + '\n', 'r')
                input(lang['enter_continue'])
            else:
                appendf('ERROR: boot repack problem', logs + '/boot.log')
        else:
            copyfile('image-new.img', rd + '/' + filetype2)
            appendf(cmd(issudo2 + AIK + '/cleanup.sh --local'), logs + '/boot.log')

    with cd(bd):
        appendf(cmd(rampy() + f'delram {romname} {filetype}'), logs + '/boot.log')

    if not bootext and not quiet:
        banner()
        kprint(filetype + '.img' + lang['boot_packed_d'] + '\n', 'g')
        input(lang['enter_continue'])

    return


def boot_unpack(filetype, filetype2, bootext=None, quiet=None):
    if not quiet:
        banner()

    if not bootext:
        kprint(lang['boot_unpack'] + filetype2 + ' ...\n', 'b')

    bootdir = rd + '/' + filetype + 'img'
    get_devicename()

    if existf(rd + '/' + filetype2):
        mkdir(bootdir)
        os.replace(rd + '/' + filetype2, bootdir + '/' + filetype2)

        with cd(bootdir):
            appendf(cmd(issudo2 + AIK + '/unpackimg.sh --local '
                        + filetype2), logs + '/boot.log')

            os.replace(filetype2, rd + '/' + filetype2)

        if (filetype == 'boot'
                and not existf(bootdir + '/ramdisk/default.prop')
                and not os.path.islink(bootdir + '/ramdisk/default.prop')):
            appendf('INFO: No default.prop in ramdisk', logs + '/boot.log')
    else:
        if not quiet:
            banner()
            kprint(lang['error'], 'yrbbo')
            kprint(lang['boot_need_img'] + '\n', 'r')
            input(lang['enter_continue'])
        else:
            appendf('ERROR: No img to unpack', logs + '/boot.log')

    return


class cd:
    def __init__(self, path):
        self.old_dir = os.getcwd()
        self.new_dir = path

    def __enter__(self):
        os.chdir(self.new_dir)

    def __exit__(self, *args):
        os.chdir(self.old_dir)


def new_project():
    while os.path.exists('./'):
        banner()
        kprint(lang['new_q'] + '\n')
        romname = input().replace(' ', '_')
        ospath = f'./superr_{romname}'
        if os.path.exists(ospath):
            kprint('\n' + lang['new_already'] + '\n')
            input(lang['enter_try_again'])

    return romname


def check_ci(whatimg, old=None, new=None):
    ci_files = getconf('case_files_' + whatimg, uconf, l=1)

    if old and ci_files and getconf('case_fix', mconf) == 'Yes':
        for i in ci_files:
            x = greps(i + ' ', readfl(prfiles + '/fs_config-' + whatimg))
            y = greps('/' + i + ' ', readfl(prfiles + '/file_contexts3-' + whatimg))

            if x or y:
                cnt = len(findfiles(basename(i) + '.*', dirname(i),
                                    prfiles + '/fs_config-' + whatimg))

                if x:
                    a = x[0].split()[0] + '.ex' + str(cnt) + '.srk '
                    sedf(x[0].split()[0] + ' ', a, prfiles + '/fs_config-' + whatimg)

                if y:
                    a = y[0].split()[0] + '.ex' + str(cnt) + '.srk '
                    sedf(y[0].split()[0] + ' ', a, prfiles
                         + '/file_contexts3-' + whatimg)

    if new and ci_files:
        for i in ci_files:
            x = greps(i + '.ex.*.srk ', readfl(prfiles + '/fs_config-' + whatimg))
            y = greps('/' + i + '.ex.*.srk ',
                      readfl(prfiles + '/file_contexts3-' + whatimg))

            if x:
                a = x[0].split()[0][:-8] + ' '
                sedf(x[0].split()[0] + ' ', a, prfiles + '/fs_config-' + whatimg)

            if y:
                a = y[0].split()[0][:-8] + ' '
                sedf(y[0].split()[0] + ' ', a, prfiles
                     + '/file_contexts3-' + whatimg)


def chlist(chtitle, namelist, countdir, plug=None):
    if getconf('language', mconf):
        if countdir > 9:
            select = lang['select_enter']
        else:
            select = lang['select']
    else:
        select = 'Make your selection: '

    choice = ''
    while not choice:
        banner()
        kprint(chtitle + '\n')
        fulllist = []
        for a, itemdir in enumerate(namelist):
            fulllist.append(str(a + 1) + ') ' + itemdir)

        if countdir < 11 or countdir > 30 or len(max(fulllist, key=len)) > 22:
            kprint('\n'.join(fulllist))
        else:
            table(fulllist, 10)

        if plug and plug == 'Plugin2':
            kprint('b = ' + lang['menu_back'], 'y')
            kprint('q = ' + lang['menu_quit'] + '\n', 'm')
            chopt = ['b', 'q']
        elif plug or 'Plugin' in chtitle:
            kprint('p = ' + lang['menu_plugin_menu'], 'y')
            kprint('q = ' + lang['menu_quit'] + '\n', 'm')
            chopt = ['p', 'q']
        elif romname:
            kprint('m = ' + lang['title_main'], 'y')
            kprint('q = ' + lang['menu_quit'] + '\n', 'm')
            chopt = ['m', 'q']
        elif not getconf('language', mconf):
            kprint('d = Download language', 'y')
            kprint('q = Quit\n', 'm')
            chopt = ['d', 'q']
        else:
            kprint('n = ' + lang['menu_new'], 'y')
            kprint('q = ' + lang['menu_quit'] + '\n', 'm')
            chopt = ['n', 'q']

        kprint(select)
        if countdir > 9:
            choice = input().lower()
        else:
            choice = getChar()

        if choice.isnumeric():
            if choice < '1' or int(choice) > countdir:
                choice = ''
                continue
        elif choice not in chopt:
            choice = ''
            continue

        if plug and choice == 'b':
            return 1
        elif plug and choice == 'p':
            return 1
        elif choice == 'p':
            continue
        elif choice == 'm' and romname:
            continue
        elif choice == 'n' and not romname:
            chosen = new_project()
        elif choice == 'd':
            chosen = dllang()
        elif choice == 'q':
            if plug:
                return 3
            sys.exit()
        else:
            chosen = namelist[int(choice) - 1]

        return chosen


def chown(*filename):
    uid = os.environ.get('SUDO_UID')
    gid = os.environ.get('SUDO_GID')
    if uid:
        for i in filename:
            try:
                os.chown(i, int(uid), int(gid))
            except:
                pass


def clears():
    cconf = getconf('screen_clear', mconf)
    if cconf:
        if cconf == 'None':
            pass
        else:
            plat1 = platf
            if plat1 in ['lin', 'wsl', 'wsl2']:
                os.system('tput clear')
    else:
        print('\n' * 40, '\x1b[H', end='')


def cmd(command):
    test1 = Popen(command, close_fds=True, shell=True, stdin=PIPE,
                  stdout=PIPE, stderr=STDOUT, universal_newlines=True)

    try:
        test1 = test1.communicate()[0].strip()
    except:
        test1 = ''

    return test1


def configure(abi='arm'):
    delpath(rd + '/config', rd + '/install')
    cpdir(tools + '/updater/install', rd + '/install')
    copyfile(tools + '/updater/binary/busybox-' + abi, rd + '/install/bin/busybox')


def cpdir(srcdir, dstdir):
    copytree(srcdir, dstdir, symlinks=True)


def delpath(*longpath):
    for i in longpath:
        if os.path.isdir(i):
            while existd(i):
                cmd(f'rm -rf "{i}"')
        else:
            try:
                os.remove(i)
            except:
                cmd(f'rm -rf "{i}"')


def deodex_start(quiet=None):
    if not autorom() and not quiet:
        def exit_deo():
            print()
            input(lang['enter_rom_tools'])
    else:
        def exit_deo():
            pass

    def delete_meta_inf():
        banner()
        kprint(lang['notice'], 'ryb')
        kprint(lang['deodex_del_meta_inf_q'], 'b')
        kprint(lang['deodex_del_meta_inf_q2'], 'b')
        kprint(lang['deodex_del_meta_inf_q3'] + '\n', 'b')
        kprint(lang['deodex_del_meta_inf_q4'])
        kprint(lang['deodex_del_meta_inf_q5'])
        reply = getChar()
        if reply != 'y':
            return

        banner()
        kprint(lang['deodex_del_meta_inf'], 'b')
        with cd(rd):
            apktmp = greps(fl('', 'system/framework/'),
                           findr('system/**/*.apk'))
            for i in apktmp:
                cmd(aapt + ' remove ' + i + ' ' + ' '.join(greps('META-INF', zipl(i))))

    def choose_jartitle(jarname, jartitle):
        with cd(tools + '/smali/current'):
            if jarname == 'smali':
                findbak = greps(fl('', 'baksmali'), glob.glob('*' + jarname + '*.jar'))
            else:
                findbak = glob.glob('*' + jarname + '*.jar')

        if len(findbak) == 1:
            return tools + os.sep + 'smali' + os.sep + 'current' + os.sep + findbak[0]
        elif len(findbak) > 1:
            return tools + os.sep + 'smali' + os.sep + 'current' + os.sep + chlist(color['gb'] + jartitle + color['n'],
                                                                                   findbak, len(findbak))

        return None

    def choose_oat2dex():
        choice = ''
        while not choice:
            if autorom():
                choice = getar('oat2dex_ver')
            else:
                banner()
                kprint(lang['deodex_oat2dex_ver'] + '\n')
                kprint('1) ' + lang['deodex_oat2dex_official'])
                kprint('2) ' + lang['deodex_oat2dex_latest'] + '\n')
                kprint(lang['select'])
                choice = getChar()

            if choice.isnumeric():
                if choice < '1' or choice > '2':
                    continue
            else:
                continue

            if choice == '1':
                oattmp = glob.glob(tools + '/smali/old/*oat2dex*.jar')
                return oattmp[0]
            elif choice == '2':
                return choose_jartitle('oat2dex', lang['title_cho_oat2dex'])

    def deodex_sqsh(sqshfile):
        sqshname = basename(sqshfile)
        sqshdir = dirname(sqshfile)
        sqshtype = sqshname.split('.')[1]
        banner(quiet)
        kprint(lang['general_extracting'] + sqshfile + ' ...', 'b')
        if 'orig.applications' in sqshname:
            with cd(sqshdir):
                cmd(unsquashfs + ' ' + sqshname)

                banner(quiet)
                kprint(lang['deodex_move_odex'], 'b')
                odexarch = ''
                with cd('squashfs-root'):
                    if greps('arm64', glob.glob('*')):
                        odexarch = 'arm64'
                    elif greps('arm', glob.glob('*')):
                        odexarch = 'arm'

                    with cd(odexarch):
                        for i in glob.glob('*'):
                            odexapp = str(i.replace('.odex', ''))
                            os.replace(i, sqshdir + '/applications/'
                                       + odexapp + '/oat/' + odexarch + '/' + i)
                            os.replace(sqshdir + '/squashfs-root/' + odexapp + '/' + odexapp
                                       + '.apk', sqshdir + '/applications/' + odexapp + '/' + odexapp + '.apk')

            delpath(sqshdir + '/squashfs-root', sqshdir
                    + '/orig.applications', sqshfile)
            return

        with cd(sqshdir):
            cmd(unsquashfs + ' ' + sqshname)
            delpath(sqshfile)

            if existd('squashfs-root/arm') or existd('squashfs-root/arm64'):
                banner(quiet)
                kprint(lang['deodex_move_odex'], 'b')
                with cd('squashfs-root'):
                    odexarch = ''
                    if greps('arm64', glob.glob('*')):
                        odexarch = 'arm64'
                    elif greps('arm', glob.glob('*')):
                        odexarch = 'arm'

                    with cd(odexarch):
                        if sqshtype != 'framework':
                            for i in glob.glob('*.odex'):
                                tmpapp = str(i.replace('.odex', ''))
                                mkdir(sysdir + '/' + sqshtype + '/'
                                      + tmpapp + '/oat/' + odexarch)
                                os.replace(i, sysdir + '/' + sqshtype
                                           + '/' + tmpapp + '/oat/' + odexarch + '/' + i)
                        else:
                            mkdir(sysdir + '/' + sqshtype + '/oat/' + odexarch)
                            for i in glob.glob('*.odex'):
                                tmpapp = str(i.replace('.odex', ''))
                                if existd(framedir + '/' + tmpapp):
                                    mkdir(framedir + '/' + tmpapp + '/oat/' + odexarch)
                                    os.replace(i, framedir + '/'
                                               + tmpapp + '/oat/' + odexarch + '/' + i)
                                else:
                                    os.replace(i, sysdir + '/'
                                               + sqshtype + '/oat/' + odexarch + '/' + i)
            else:
                with cd('squashfs-root'):
                    for i in findr('**'):
                        if existd(i):
                            continue
                        tmpdir = dirname(i)
                        tmpfile = basename(i)
                        mkdir(sysdir + '/' + tmpdir)
                        os.rename(i, sysdir + '/' + tmpdir + '/' + tmpfile)

        rmleft = sqshfile.replace('.sqsh', '')
        delpath(sqshdir + '/squashfs-root', rmleft)

    def deodex(dtype):
        arch = ''
        arch2 = ''
        archtmp = ['arm64', 'x86_64', 'arm', 'x86']
        archtest = ''
        for i in archtmp:
            archtest = findr(framedir + '/**/' + i)
            if archtest:
                break
        archtest = basename(archtest[0])

        arch2test = ''
        if '64' in archtest:
            arch2test = archtest.replace('_64', '').replace('64', '')

        if (archtest and
                (existf(framedir + '/' + archtest + '/boot.oat')
                 or existf(framedir + '/' + archtest + '/boot-ext.oat'))):
            arch = archtest
            if (arch2test and
                    (existf(framedir + '/' + arch2test + '/boot.oat')
                     or existf(framedir + '/' + arch2test + '/boot-ext.oat'))):
                arch2 = arch2test
        else:
            while (not existf(framedir + '/' + arch + '/boot.oat')
                   and not existf(framedir + '/' + arch + '/boot-ext.oat')):
                banner(quiet)
                print(lang['deodex_config_arch'] + '\n')
                print(lang['deodex_config_arch2'])
                print(lang['deodex_config_arch3'])
                print(lang['deodex_config_arch4'])
                print(lang['deodex_config_arch5'] + '\n')
                print(lang['deodex_config_arch6'] + '\n')
                print(lang['deodex_config_arch7'])
                print(lang['deodex_config_arch8'] + '\n')
                print(lang['deodex_config_arch9'] + '\n')
                arch = input()

        if (existf(framedir + '/' + arch + '/boot.oat')
                or existf(framedir + '/' + arch + '/boot-ext.oat')):
            if not autorom() and not quiet:
                banner()
                kprint(lang['startup_project'] + color['g'] + romname, 'b')
                kprint(lang['startup_version'] + color['g'] + androidversion, 'b')
                kprint(lang['deodex_api'] + color['g'] + api, 'b')
                kprint(lang['deodex_arch'] + color['g'] + arch, 'b')
                if arch2:
                    kprint(lang['deodex_arch2'] + color['g'] + arch2, 'b')

                if dtype in ['m2', 'n2']:
                    kprint(lang['deodex_method'] + color['g']
                           + '\t' + basename(smali), 'b')
                    print('\t' + basename(baksmali))
                elif dtype in ['l', 'm']:
                    kprint(lang['deodex_method'] + color['g']
                           + '\t' + basename(oat2dex), 'b')

                print()
                print(lang['deodex_continue_q'])
                reply = getChar()
                if reply != 'y':
                    return
        else:
            if not quiet:
                banner()
                kprint(lang['warning'], 'yrbbo')
                kprint(lang['error_mess'], 'r')
                exit_deo()
                return

        def dodeodex(deoarch, deoarch2, deoappdir):
            for app in applist:
                if not existd(deoappdir + '/' + app + '/' + deoarch):
                    continue

                try:
                    app2 = basename(
                        glob.glob(deoappdir + '/' + app + '/*.apk')[0]).replace('.apk', '')
                except:
                    if not glob.glob(deoappdir + '/' + app + '/*.apk'):
                        app2 = app
                        cmd(aapt + ' a -fk ' + deoappdir + '/'
                            + app + '/' + app + '.apk fakesrkfile')
                    else:
                        continue

                if greps('.*classes\.dex', zipl(deoappdir + '/' + app + '/' + app2 + '.apk')):
                    print()
                    kprint(app + lang['deodex_app_already'] + '\n', 'g')
                    if dtype != 'l':
                        delpath(deoappdir + '/' + app + '/oat')
                    else:
                        delpath(deoappdir + '/' + app + '/' + deoarch)

                    continue

                print()
                print(lang['deodex_deodexing'] + app + '\n')
                with cd(deoappdir + '/' + app + '/' + deoarch):
                    mvfiles = glob.glob('*')
                    dodex = []
                    for i in mvfiles:
                        os.replace(i, framedir + '/' + deoarch2 + '/' + i)
                        dodex.append(i)

                if dtype == 'l':
                    delpath(deoappdir + '/' + app + '/' + deoarch2)
                else:
                    delpath(deoappdir + '/' + app + '/oat')

                with cd(framedir + '/' + deoarch2):
                    if dtype in ['m2', 'n2']:
                        classes = cmd('java -Xmx' + heapsize + 'm -jar '
                                      + baksmali + ' list dex ' + app2 + '.odex').splitlines()
                        appendf(str(classes), logs + '/deodex.log')
                        for line in classes:
                            apkdex = basename(line)
                            if 'classes' not in apkdex:
                                dexclass = 'classes.dex'
                            else:
                                dexclass = apkdex.split(':')[1]

                            appendf(cmd(
                                'java -Xmx' + heapsize + 'm -jar ' + baksmali
                                + ' deodex -b boot.oat ' + app2 + '.odex/' + apkdex
                                + ' -o smali'), logs + '/deodex.log')
                            if glob.glob('smali/*'):
                                appendf(cmd(
                                    f'java -Xmx{heapsize}m -jar {smali} assemble -a {api} smali -o {dexclass}'),
                                    logs + '/deodex.log')
                            delpath('smali')
                            if not existf(dexclass):
                                appendf(deoappdir + '/' + app + '/' + deoarch
                                        + '/' + dexclass, logs + '/deodex_fail_list')
                                continue

                        for i in glob.glob('classes*.dex'):
                            os.replace(i, deoappdir + '/' + app + '/' + i)
                        delpath(*dodex)

                    elif dtype in ['m', 'l']:
                        appendf(cmd('java -Xmx' + heapsize + 'm -jar ' + oat2dex
                                    + ' ' + app2 + '.odex odex'), logs + '/deodex.log')
                        if not existf(app2 + '.dex'):
                            delpath(*glob.glob(app2 + '-classes*.dex'))
                            continue

                        os.replace(app2 + '.dex', deoappdir
                                   + '/' + app + '/classes.dex')
                        for i in glob.glob('*-classes*.dex'):
                            os.replace(i, deoappdir + '/' + app
                                       + '/' + i.split('-')[-1])

                        delpath(*dodex)

                        broken = None
                        for i in glob.glob('*_classes*.cdex'):
                            appendf(
                                '\n'.join(grepv('^==', cmd(vdexcon + ' ' + i).splitlines())), logs + '/deodex.log')
                            if existf(i + '.new'):
                                os.replace(i + '.new', i[:-5] + '.dex')
                                delpath(i)
                            else:
                                appendf(deoappdir + '/' + app + '/' + app2
                                        + '.apk', logs + '/deodex_fail_list')
                                appendf(deoappdir + '/' + app + '/' + app2
                                        + '.apk', logs + '/deodex_cdex_fail')
                                for x in glob.glob('*_classes*'):
                                    delpath(x)

                                broken = 1
                                break

                        if not broken:
                            for i in glob.glob('*_classes*'):
                                os.replace(i, deoappdir + '/' + app
                                           + '/' + i.split('_')[-1])
                            delpath(*dodex)
                        else:
                            delpath(*dodex)
                            continue

                with cd(deoappdir + '/' + app):
                    appendf(cmd(aapt + ' add -fk ' + app2
                                + '.apk classes*.dex'), logs + '/deodex.log')
                    delpath(*glob.glob('classes*.dex'))

        getconf('deodex', uconf, add=dtype)
        delpath(*glob.glob(logs + '/*.log'))
        delpath(logs + '/deodex_fail_list')

        comptmp = findr(appdir + '/**') + findr(privdir
                                                + '/**') + findr(framedir + '/**')
        comptmp = greps('.*\.gz$|.*\.xz$', comptmp)

        if comptmp:
            if not quiet:
                clears()
            print()
            print('-'.center(tsize, '-'))
            print(lang['deodex_extract_txt'])
            print('-'.center(tsize, '-'))
            print()
            for i in greps('.*\.gz$', comptmp):
                gzdir = dirname(i)
                gzfile = basename(i)
                print('\n' + lang['deodex_extract'] + gzfile + '\n')
                appendf(zipu(i, gzdir), logs + '/zip.log')

            for i in greps('.*\.xz$', comptmp):
                xzdir = dirname(i)
                xzfile = basename(i)
                print('\n' + lang['deodex_extract'] + xzfile + '\n')
                with cd(xzdir):
                    xzu(i)

        with cd(rd):
            odextmp = findr('system/**/*.odex') + findr('vendor/**/*.odex') + findr(
                'oem/**/*.odex') + findr('product/**/*.odex') + findr('system_ext/**/*.odex')
        if dtype != 'l':
            if sar():
                odextmp = greps(
                    fl('', 'system/system/framework/oat/|system/system/framework/' + arch + '/|system/system/framework/'
                       + arch2 + '/|system/system/app|system/system/priv-app|system/system/vendor/framework'), odextmp)
            else:
                odextmp = greps(fl('',
                                   'system/framework/oat/|system/framework/' + arch + '/|system/framework/'
                                   + arch2 + '/|system/app|system/priv-app|system/vendor/framework'
                                   ), odextmp)
        else:
            odextmp = greps(fl('', 'system/framework/' + arch + '/|system/framework/'
                               + arch2 + '/|system/app/|system/priv-app/'), odextmp)

        extramv = {}
        if existd(sysdir + '/app') and odextmp:
            if not quiet:
                clears()
            print()
            print('-'.center(tsize, '-'))
            print(lang['deodex_move'])  # Start Move files
            print('-'.center(tsize, '-'))
            print()
            for i in odextmp:
                if dtype != 'l':
                    adir = os.sep.join(i.split('/')[:-3])
                else:
                    adir = os.sep.join(i.split('/')[:-2])

                if basename(adir).startswith('.'):
                    with cd(adir):
                        newapp = glob.glob('*.apk').split('.')[0]
                    newappdir = dirname(adir) + os.sep + newapp
                    mvdir(adir, newappdir)
                    extramv[rd + os.sep + newappdir] = rd + os.sep + adir
                    adir = newappdir
                    extraapp = basename(adir)
                else:
                    extraapp = basename(adir)
                    extramv[sysdir + os.sep + 'app'
                            + os.sep + extraapp] = rd + os.sep + adir

                mvdir(rd + os.sep + adir, sysdir + os.sep + 'app' + os.sep + extraapp)

        chimerao = findr(
            sysdir + '/priv-app/PrebuiltGmsCore*/app_chimera/**/*.odex')
        if chimerao:
            dname = ''
            for i in chimerao:
                i = i.replace('/', os.sep)
                aname = basename(i)[:-5]
                dname = os.sep.join(i.split(os.sep)[:-3])
                darch = i.split(os.sep)[-2]

                mkdir('/'.join([sysdir, 'app', aname, 'oat', darch]))
                os.replace(
                    i, '/'.join([sysdir, 'app', aname, 'oat', darch, aname + '.odex']))

                if existf('/'.join([dname, 'oat', darch, aname + '.vdex'])):
                    os.replace(i.replace(
                        '.odex', '.vdex'), '/'.join([sysdir, 'app', aname, 'oat', darch, aname + '.vdex']))

                if existf('/'.join([dname, aname + '.apk'])):
                    os.replace('/'.join([dname, aname + '.apk']),
                               '/'.join([sysdir, 'app', aname, aname + '.apk']))

                extramv[os.sep.join([sysdir, 'app', aname, aname + '.apk'])
                ] = os.sep.join([dname, aname + '.apk'])

            delpath('/'.join([dname, 'oat']))

        if existd(sysdir + '/vendor/framework'):
            for i in glob.glob(sysdir + '/vendor/framework/*.jar'):
                if not greps('.*classes\.dex', zipl(i)):
                    os.replace(i, framedir + '/' + basename(i))
                    extramv[framedir + os.sep + basename(i)] = i

            for i in [arch, arch2]:
                if not i:
                    continue
                for a in glob.glob(sysdir + '/vendor/framework/oat/' + i + '/*'):
                    os.replace(a, framedir + '/oat/' + i + '/' + basename(a))

            delpath(sysdir + '/vendor/framework/oat')

        if dtype in ['l', 'm']:
            if not quiet:
                clears()
            print()
            print('-'.center(tsize, '-'))
            print(lang['deodex_deop'])  # Start Deoptomizing boot.oat
            print('-'.center(tsize, '-'))
            print()
            with cd(framedir + '/' + arch):
                if not existd('odex'):
                    appendf(cmd('java -Xmx' + heapsize + 'm -jar '
                                + oat2dex + ' boot boot.oat'), logs + '/deodex.log')

                if arch2 and not existd('odex'):
                    appendf(cmd('java -Xmx' + heapsize + 'm -jar '
                                + oat2dex + ' boot boot.oat'), logs + '/deodex.log')

        if existd(appdir):
            if not quiet:
                clears()
            print()
            print('-'.center(tsize, '-'))
            print(lang['deodex_start_app'])  # Start Deodexing app
            print('-'.center(tsize, '-'))
            print()
            with cd(appdir):
                applist = sorted(glob.glob('*'), key=str.lower)
                for app in applist:
                    if dtype == 'l':
                        if arch2 and existd(app + '/' + arch) and existd(app + '/' + arch2):
                            delpath(app + '/' + arch2)
                    else:
                        if arch2 and existd(app + '/oat/' + arch) and existd(app + '/oat/' + arch2):
                            delpath(app + '/oat/' + arch2)

            if dtype != 'l':
                dodeodex('oat/' + arch, arch, appdir)
                if arch2:
                    dodeodex('oat/' + arch2, arch2, appdir)
            else:
                dodeodex(arch, arch, appdir)
                if arch2:
                    dodeodex(arch2, arch2, appdir)

        if existd(privdir):
            if not quiet:
                clears()
            print()
            print('-'.center(tsize, '-'))
            print(lang['deodex_start_priv'])  # Start Deodexing priv-app
            print('-'.center(tsize, '-'))
            print()
            with cd(privdir):
                applist = sorted(glob.glob('*'), key=str.lower)
                for app in applist:
                    if dtype == 'l':
                        if arch2 and existd(app + '/' + arch) and existd(app + '/' + arch2):
                            delpath(app + '/' + arch2)
                    else:
                        if arch2 and existd(app + '/oat/' + arch) and existd(app + '/oat/' + arch2):
                            delpath(app + '/oat/' + arch2)

            if dtype != 'l':
                dodeodex('oat/' + arch, arch, privdir)
                if arch2:
                    dodeodex('oat/' + arch2, arch2, privdir)
            else:
                dodeodex(arch, arch, privdir)
                if arch2:
                    dodeodex(arch2, arch2, privdir)

        if not quiet:
            clears()
        print()
        print('-'.center(tsize, '-'))
        print(lang['deodex_start_frame'])  # Start Deodexing framework
        print('-'.center(tsize, '-'))
        print()
        deoarch = 'oat/' + arch
        deoarch2 = arch

        if dtype in ['n2', 'm2']:
            with cd(framedir + '/' + deoarch2):
                oattmp = sorted(glob.glob('*.oat'), key=str.lower)
                for line in oattmp:
                    if line != 'boot.oat':
                        framejar = line.replace(
                            'boot-', '').replace('.oat', '') + '.jar'
                        if existf(framedir + '/' + framejar) and greps('.*classes.dex',
                                                                       zipl(framedir + '/' + framejar)):
                            kprint(
                                '\n' + line + lang['deodex_app_already'] + '\n', 'g')
                            continue

                    print('\n' + lang['deodex_deodexing'] + line + '\n')

                    classes = cmd(f'java -Xmx{heapsize}m -jar {baksmali} list dex {line}').splitlines()
                    appendf(classes, logs + '/deodex.log')
                    for line2 in classes:
                        line2 = basename(line2)
                        if 'classes' not in line2:
                            line3 = line2
                            dexclass = 'classes.dex'
                        else:
                            line3 = line2.split(':')[0]
                            dexclass = line2.split(':')[1]

                        sdcmd = f'java -Xmx{heapsize}m -jar {baksmali} deodex -b boot.oat {line}{os.sep}{line2} -o smali'
                        appendf(sdcmd, logs + '/deodex.log')
                        appendf(cmd(sdcmd), logs + '/deodex.log')

                        if glob.glob('smali/*'):
                            sdcmd = 'java -Xmx' + heapsize + 'm -jar ' + smali + ' assemble -a ' + \
                                    api + ' smali -o ' + framedir + os.sep + line3 + '__' + dexclass
                            appendf(sdcmd, logs + '/deodex.log')
                            appendf(cmd(sdcmd), logs + '/deodex.log')

                        delpath('smali')

            if existd(framedir + '/' + deoarch):
                with cd(framedir + '/' + deoarch):
                    frametmp = sorted(glob.glob('*.odex'), key=str.lower)
                    for frame in frametmp:
                        frname = frame.replace('.odex', '')
                        for ftype in glob.glob(frname + '.*'):
                            os.replace(ftype, framedir + '/'
                                       + deoarch2 + '/' + basename(ftype))

                        framejar = frname + '.jar'
                        if existf(framedir + '/' + framejar) and greps('.*classes.dex',
                                                                       zipl(framedir + '/' + framejar)):
                            kprint(
                                '\n' + frame + lang['deodex_app_already'] + '\n', 'g')
                            continue

                        print('\n' + lang['deodex_deodexing'] + frame + '\n')

                        with cd(framedir + '/' + deoarch2):
                            classes = cmd(
                                f'java -Xmx{heapsize}m -jar {baksmali} list dex {frame}').splitlines()
                            appendf(classes, logs + os.sep + 'deodex.log')
                            for line in classes:
                                apkdex = basename(line)
                                if 'classes' not in apkdex:
                                    dexclass = apkdex + '__classes.dex'
                                else:
                                    dexclass = apkdex.replace(':', '__')

                                sdcmd = f'java -Xmx{heapsize}m -jar {baksmali} deodex -b boot.oat {frame}/{apkdex} -o smali'
                                appendf(sdcmd, logs + '/deodex.log')
                                appendf(cmd(sdcmd), logs + '/deodex.log')

                                if glob.glob('smali/*'):
                                    sdcmd = f'java -Xmx{heapsize}m -jar {smali} assemble -a {api} smali -o {dexclass}'
                                    appendf(sdcmd, logs + '/deodex.log')
                                    appendf(cmd(sdcmd), logs + '/deodex.log')
                                    try:
                                        os.replace(
                                            dexclass, framedir + '/' + dexclass)
                                    except:
                                        pass

                                delpath('smali')

                            delpath(*glob.glob(frname + '.*'))
        elif dtype in ['l', 'm']:
            if dtype == 'l':
                deoarch = arch
                deoarch2 = arch
            if existd(framedir + '/' + deoarch):
                with cd(framedir + '/' + deoarch):
                    frametmp = sorted(glob.glob('*.odex'), key=str.lower)
                    for frame in frametmp:
                        os.replace(frame, framedir + '/' + deoarch2 + '/' + frame)
                        print('\n' + lang['deodex_deodexing'] + frame + '\n')

                        with cd(framedir + '/' + deoarch2):
                            appendf(cmd(f'java -Xmx{heapsize}m -jar {oat2dex} {frame} odex'), logs + '/deodex.log')
                            delpath(frame)
                            for i in glob.glob('*.dex'):
                                os.replace(i, framedir + '/' + deoarch + '/' + i)

            with cd(framedir + '/' + deoarch2 + '/dex'):
                dextmp = glob.glob('*')
                for i in dextmp:
                    os.replace(i, framedir + '/' + deoarch + '/' + i)
            with cd(framedir + '/' + deoarch):
                dextmp = glob.glob('*.dex')
                for line in dextmp:
                    if 'classes' not in line:
                        frame = line.replace('.dex', '.jar__classes.dex')
                    else:
                        dexclass = '-'.join(line.split('-')[-1:])
                        frame = line.replace(
                            '-' + dexclass, '') + '.jar__' + dexclass

                    os.replace(line, framedir + '/' + frame)

        banner(quiet)
        kprint(lang['deodex_pack_jar'], 'b')
        with cd(framedir):
            frametmp = sorted(glob.glob('*jar__classes*.dex'), key=str.lower)
            lskip = ''
            for line in frametmp:
                if lskip and lskip + '__' in line:
                    continue
                line2 = line.split('__')[0]
                frametmp2 = sorted(
                    greps(f'^{line2}__.*', frametmp), key=str.lower)
                for line3 in frametmp2:
                    line4 = line3.split('__')[1]
                    os.replace(line3, line4)
                    if len(frametmp2) > 1:
                        lskip = line2
                    else:
                        lskip = ''

                if existf('classes.dex'):
                    appendf(cmd(aapt + ' add -fk ' + line2
                                + ' classes*.dex'), logs + '/deodex.log')
                else:
                    appendf('ERROR: ' + line2 + ' has no classes.dex',
                            logs + '/deodex.log')

                delpath(*glob.glob('classes*.dex'))

            if dtype in ['l', 'm']:
                delpath(arch + '/odex')
                delpath(arch + '/dex')
                if arch2:
                    delpath(arch2 + '/odex')
                    delpath(arch2 + '/dex')

        if not quiet:
            clears()
        print()
        print('-'.center(tsize, '-'))
        print(lang['deodex_clean'])  # Start Deodex clean
        print('-'.center(tsize, '-'))
        print()
        print()
        if extramv:
            for i in list(extramv):
                if existd(i):
                    mvdir(i, extramv[i])
                else:
                    os.replace(i, extramv[i])

                if 'app_chimera' in extramv[i]:
                    delpath(dirname(i))

        delpath(framedir + '/oat')
        delarch = 1

        if getprop('ro.product.manufacturer').lower() == 'xiaomi':
            delpath(framedir + '/miui.apk__classes.dex', framedir + '/miuisystem.apk__classes.dex',
                    framedir + '/miui.jar', framedir + '/miuisystem.jar')

        if not autorom():
            if dtype in ['l', 'm']:
                a = grepf('convertToDex: skip', logs + '/deodex.log')
                deodex_fail_list = []
                for i in a:
                    deodex_fail_list.append('/'.join(i.split('/')[1:]))

                deodex_fail_list = '\n'.join(deodex_fail_list)
            else:
                deodex_fail_list = ''
                if existf(logs + '/deodex_fail_list'):
                    try:
                        sedf(rd + '/', '', logs + '/deodex_fail_list')
                    except:
                        pass

                    deodex_fail_list = readf(logs + '/deodex_fail_list')

            if deodex_fail_list:
                banner(quiet)
                kprint(lang['deodex_problems'], 'r')
                kprint(lang['deodex_problems2', 'r'])
                kprint(lang['deodex_problems3', 'r'])
                kprint(deodex_fail_list, 'y')
                if dtype == 'm':
                    kprint('\n' + lang['deodex_try_smali'], 'g')

                if not quiet:
                    print()
                    input(lang['enter_continue'])
        else:
            if getar('delete_arch') == 'no':
                delarch = None

        if delarch:
            delpath(framedir + '/' + arch)
            if arch2:
                delpath(framedir + '/' + arch2)

        with cd(rd):
            stillodexed = '\n'.join(findr('system/**/*.odex') + findr('vendor/**/*.odex') + findr(
                'oem/**/*.odex') + findr('product/**/*.odex') + findr('system_ext/**/*.odex'))
        if not stillodexed:
            if dtype == 'n2':
                delete_meta_inf()
            banner(quiet)
            kprint(lang['deodex_complete'], 'g')
            if not quiet:
                exit_deo()
        else:
            if not quiet:
                banner()
                kprint(lang['deodex_remain'] + '\n', 'r')
                kprint(stillodexed, 'y')
                exit_deo()
        return

    def deodex_vdex(dtype):
        arch = arch2 = ''
        for i in ['arm64', 'x86_64', 'arm', 'x86']:
            arch = findr(framedir + '/**/' + i)
            if arch:
                arch = basename(arch[0])
                if '64' in arch:
                    arch2 = arch.replace('_64', '').replace('64', '')
                    if not findr(rd + '/**/' + arch2):
                        arch2 = ''

                break

        sysdir2 = sysdir
        rd2 = rd

        if not quiet:
            if (not existf(framedir + '/' + arch + '/boot.oat')
                    and not existf(framedir + '/' + arch + '/boot-ext.oat')):
                while (not existf(framedir + '/' + arch + '/boot.oat')
                       and not existf(framedir + '/' + arch + '/boot-ext.oat')):
                    banner()
                    print(lang['deodex_config_arch'] + '\n')
                    print(lang['deodex_config_arch2'])
                    print(lang['deodex_config_arch3'])
                    print(lang['deodex_config_arch4'])
                    print(lang['deodex_config_arch5'] + '\n')
                    print(lang['deodex_config_arch6'] + '\n')
                    print(lang['deodex_config_arch7'])
                    print(lang['deodex_config_arch8'] + '\n')
                    print(lang['deodex_config_arch9'] + '\n')
                    arch = input()

        if (existf(framedir + '/' + arch + '/boot.oat')
                or existf(framedir + '/' + arch + '/boot-ext.oat')):
            if not autorom() and not quiet:
                banner()
                kprint(lang['startup_project'] + color['g'] + romname, 'b')
                kprint(lang['startup_version'] + color['g'] + androidversion, 'b')
                kprint(lang['deodex_api'] + color['g'] + api, 'b')
                kprint(lang['deodex_arch'] + color['g'] + arch, 'b')
                if arch2:
                    kprint(lang['deodex_arch2'] + color['g'] + arch2, 'b')

                kprint(lang['deodex_method'] + color['g']
                       + '\t' + basename(vdexext) + '\n', 'b')
                print(lang['deodex_continue_q'])
                reply = getChar()
                if reply != 'y':
                    return
        else:
            if not quiet:
                banner()
                kprint(lang['warning'], 'yrbbo')
                kprint(lang['error_mess'], 'r')
                exit_deo()
                return

        getconf('deodex', uconf, add=dtype)
        delpath(*glob.glob(logs + '/*.log'))
        delpath(logs + '/deodex_fail_list')

        comptmp = findr(appdir + '/**') + findr(privdir
                                                + '/**') + findr(framedir + '/**')
        comptmp = greps('.*\.gz$|.*\.xz$', comptmp)

        if comptmp:
            banner(quiet)
            print()
            print('-'.center(tsize, '-'))
            print(lang['deodex_extract_txt'])
            print('-'.center(tsize, '-'))
            print()
            for i in greps('.*\.gz$', comptmp):
                gzdir = dirname(i)
                gzfile = basename(i)
                print('\n' + lang['deodex_extract'] + gzfile + '\n')
                appendf(zipu(i, gzdir), logs + '/zip.log')

            for i in greps('.*\.xz$', comptmp):
                xzdir = dirname(i)
                xzfile = basename(i)
                print('\n' + lang['deodex_extract'] + xzfile + '\n')
                with cd(xzdir):
                    xzu(i)

        banner(quiet)
        kprint(lang['deodex_move_odex'], 'b')

        with cd(framedir):
            for i in glob.glob('*.vdex'):
                os.replace(i, framedir + '/' + arch + '/' + i)

        with cd(rd):
            if arch and arch2:
                for i in grepv('00_project_files', findr(rd2 + '/**/' + arch + '/*.vdex')):
                    delpath(i.replace('/' + arch + '/', '/' + arch2 + '/'))

            if existd(framedir + '/' + arch):
                with cd(framedir + '/' + arch):
                    bootclass = None
                    boat = None
                    if existf('boot.oat') and existf('boot.vdex'):
                        boat = 'boot.oat'
                    elif existf('boot-ext.oat') and existf('boot-ext.vdex'):
                        boat = 'boot-ext.oat'

                    if boat:
                        with open(boat, 'rb') as f:
                            data = f.read()

                        result = []
                        for i in re.finditer(b'--dex-location=', data):
                            result.append(i.start())

                        if result:
                            begin = result[0] + 15
                            bnum = 1
                            dex = b''
                            while True:
                                if data[begin + bnum] == 32:
                                    dex = data[begin:bnum + begin]
                                    break
                                else:
                                    bnum += 1

                            bootclass = basename(dex.decode())

                        if bootclass:
                            os.replace(boat[:-4] + '.vdex', 'boot-'
                                       + bootclass.replace('.jar', '.vdex'))
                        else:
                            if existf(boat[:-4] + '.vdex'):
                                os.rename(boat[:-4] + '.vdex',
                                          boat[:-4] + '.vdex2')

            banner(quiet)

            for i in grepv('00_project_files', findr(rd2 + '/**/*.vdex')):
                thedir = dirname(i)
                thefile = str(basename(i))
                if thefile.startswith('boot-'):
                    thefile = thefile[5:]

                if i.startswith(sysdir2):
                    sdir = i.replace(sysdir2 + '/', '').split('/')[0]

                    mainfile = findr(sysdir2 + '/' + sdir + '/**/' + thefile.replace('.vdex', '.apk')) + findr(
                        sysdir2 + '/' + sdir + '/**/' + thefile.replace('.vdex', '.jar'))
                else:
                    sdir = i.replace(rd2 + '/', '').split('/')[0]

                    mainfile = findr(rd2 + '/' + sdir + '/**/' + thefile.replace('.vdex', '.apk')) + findr(
                        rd2 + '/' + sdir + '/**/' + thefile.replace('.vdex', '.jar'))

                if not mainfile:
                    if '/oat/' in i:
                        if '/framework/' in i:
                            mainfile = [
                                '/'.join(i.split('/')[:-3]) + '/' + thefile[:-5] + '.jar']
                        else:
                            mainfile = [
                                '/'.join(i.split('/')[:-3]) + '/' + thefile[:-5] + '.apk']
                    else:
                        if '/framework/' in i:
                            mainfile = [
                                '/'.join(i.split('/')[:-2]) + '/' + thefile[:-5] + '.jar']
                        else:
                            mainfile = [
                                '/'.join(i.split('/')[:-2]) + '/' + thefile[:-5] + '.apk']

                if mainfile:
                    mainfile = mainfile[0]
                else:
                    appendf('FAILED: ' + i, logs + '/deodex.log')
                    continue

                if existf(mainfile) and greps('.*classes.dex', zipl(mainfile)):
                    if not mainfile.endswith('.jar'):
                        delpath(dirname(mainfile) + '/oat')

                    kprint('\n' + basename(mainfile)
                           + lang['deodex_app_already'] + '\n', 'g')
                    continue

                print('\n' + lang['deodex_deodexing'] + basename(mainfile) + '\n')

                with cd(dirname(mainfile)):
                    os.replace(i, thefile)
                    retv = cmd(vdexext + ' -i ' + thefile)
                    if greps(r'\[ERROR\]|\[WARNING\]', retv.split()):
                        retv = cmd(vdexext + ' -i ' + thefile
                                   + ' --ignore-crc-error')

                        if greps(r'\[ERROR\]|\[WARNING\]', retv.split()):
                            appendf(retv, logs + '/deodex.log')
                            appendf(mainfile.replace(rd2, ''),
                                    logs + '/deodex_fail_list')
                            os.replace(thefile, i)
                            delpath(*glob.glob(thefile[:-5] + '_classes*'))
                            continue
                        else:
                            appendf(mainfile.replace(rd2, ''),
                                    logs + '/deodex_crc_ignored')
                    else:
                        appendf(retv, logs + '/deodex.log')

                    if not glob.glob(thefile[:-5] + '_classes*dex'):
                        print('\n' + basename(mainfile) + ': '
                              + lang['deodex_no_dex'] + '\n')

                        if existf(thefile):
                            os.replace(thefile, i)

                        appendf(basename(mainfile)
                                + ': No dex in vdex. Skipping', logs + '/deodex.log')

                        continue

                    broken = None
                    for cdex in glob.glob('*_classes*.cdex'):
                        appendf('\n'.join(
                            grepv('^==', cmd(vdexcon + ' ' + cdex).splitlines())), logs + '/deodex.log')

                        delpath(cdex)

                        if existf(cdex + '.new'):
                            os.replace(cdex + '.new', cdex[:-5] + '.dex')
                        else:
                            appendf(mainfile.replace(rd, ''),
                                    logs + '/deodex_fail_list')
                            appendf(mainfile.replace(rd, ''),
                                    logs + '/deodex_cdex_fail')
                            for x in glob.glob('*_classes*'):
                                delpath(x)

                            broken = 1
                            break

                    os.replace(thefile, i)

                    if not broken:
                        for classes in glob.glob('*_classes*'):
                            os.replace(classes, classes.split('_')[-1])

                        appendf(cmd(aapt + ' add -fk ' + basename(mainfile)
                                    + ' classes*.dex'), logs + '/deodex.log')
                        delpath(*glob.glob('classes*.dex'), thefile)

                        if not mainfile.endswith('.jar'):
                            delpath('oat')
                    else:
                        delpath(*glob.glob('*classes*dex'))
                        continue

        banner(quiet)
        kprint(lang['deodex_clean'], 'b')

        if existf(framedir + '/' + arch + '/boot.vdex2'):
            os.rename(framedir + '/' + arch + '/boot.vdex2',
                      framedir + '/' + arch + '/boot.vdex')

        if existf(framedir + '/' + arch + '/boot-ext.vdex2'):
            os.rename(framedir + '/' + arch + '/boot-ext.vdex2',
                      framedir + '/' + arch + '/boot-ext.vdex')

        with cd(rd):
            for i in grepv('00_project_files', findr('**/framework/oat')):
                delpath(i)

        delarch = 1

        if getprop('ro.product.manufacturer').lower() == 'xiaomi':
            delpath(framedir + '/miui.apk__classes.dex', framedir + '/miuisystem.apk__classes.dex',
                    framedir + '/miui.jar', framedir + '/miuisystem.jar')

        if not autorom() and not quiet:
            banner()
            print(lang['deodex_del_arch'])
            kprint('/'.join([arch] + ([arch2] if arch2 else [])) + '\n', 'y')
            reply = getChar()
            if reply == 'n':
                delarch = None

            deodex_fail_list = ''
            if existf(logs + '/deodex_fail_list'):
                deodex_fail_list = readf(logs + '/deodex_fail_list')

            if deodex_fail_list:
                banner()
                kprint(lang['deodex_problems'], 'r')
                kprint(lang['deodex_problems2'], 'r')
                kprint(lang['deodex_problems3'], 'r')
                kprint(deodex_fail_list, 'y')
                if dtype == 'm':
                    kprint('\n' + lang['deodex_try_smali'], 'g')

                print()
                input(lang['enter_continue'])
        else:
            if getar('delete_arch') == 'no':
                delarch = None

        with cd(rd):
            if delarch:
                for i in grepv('00_project_files', findr('**/framework/' + arch)):
                    delpath(i)

                if arch2:
                    for i in grepv('00_project_files', findr('**/framework/' + arch2)):
                        delpath(i)

            stillodexed = '\n'.join(
                grepv('00_project_files', findr('**/*.vdex')))

        if not stillodexed:
            banner(quiet)
            kprint(lang['deodex_complete'], 'g')
            if not quiet:
                exit_deo()
        else:
            banner(quiet)
            kprint(lang['deodex_remain'] + '\n', 'r')
            kprint(stillodexed, 'y')
            if not quiet:
                exit_deo()

        return

    def deodex_old():
        if not autorom() and not quiet:
            banner()
            kprint(lang['startup_project'] + color['g'] + romname, 'b')
            kprint(lang['startup_version'] + color['g'] + androidversion, 'b')
            kprint(lang['deodex_api'] + color['g'] + api, 'b')
            kprint(lang['deodex_method'] + color['g'] + '\t' + basename(smali), 'b')
            print('\t' + basename(baksmali) + '\n')
            print(lang['deodex_continue_q'])
            reply = getChar()
            if reply != 'y':
                return

        def dodeodexold():
            for app in applist:
                app = '.'.join(app.split('.')[:-1])
                if not existf(deoappdir + '/' + app + '.odex'):
                    continue

                if 'classes.dex' in zipl(deoappdir + '/' + app + '.' + deoext):
                    kprint('\n' + app + lang['deodex_app_already'] + '\n', 'g')
                    delpath(deoappdir + '/' + app + '.odex')
                    continue

                print('\n' + lang['deodex_deodexing'] + app + '\n')

                appendf(cmd('java -Xmx' + heapsize + 'm -jar ' + baksmali + ' -a ' + api + ' -d ' + framedir + ' -x '
                            + deoappdir + os.sep + app + '.odex -o ' + deoappdir + os.sep + 'smali'),
                        logs + '/deodex.log')
                if glob.glob(deoappdir + os.sep + 'smali/*'):
                    appendf(cmd('java -Xmx' + heapsize + 'm -jar ' + smali + ' -a ' + api + ' ' + deoappdir
                                + os.sep + 'smali -o ' + deoappdir + os.sep + 'classes.dex'), logs + '/deodex.log')
                    appendf(cmd(aapt + ' add -fk ' + deoappdir + os.sep + app + '.' + deoext
                                + ' ' + deoappdir + os.sep + 'classes.dex'), logs + '/deodex.log')
                    delpath(deoappdir + '/' + app + '.odex',
                            deoappdir + '/classes.dex')
                delpath(deoappdir + '/smali')

        with cd(prfiles):
            delpath(*glob.glob('deoxex_*'))
            getconf('deodex', uconf, add='old')
        with cd(prfiles + '/logs'):
            delpath(*glob.glob('*.log'))

        with cd(rd):
            odextmp = greps(fl('', '.*system/framework|.*system/app/|.*system/priv-app/'),
                            findr('system/**/*.odex') + findr('vendor/**/*.odex'))

        if existd(sysdir + '/app') and odextmp:
            if not quiet:
                clears()
            print()
            print('-'.center(tsize, '-'))
            print(lang['deodex_move'])
            print('-'.center(tsize, '-'))
            print()
            for i in odextmp:
                odir = dirname(i)
                odex = basename(i)
                apk = basename(i).replace('.odex', '.apk')
                os.replace(sysdir + '/' + i, appdir + '/' + odex)
                os.replace(sysdir + '/' + odir + '/' + apk, appdir + '/' + apk)

        if not quiet:
            clears()
        print()
        print('-'.center(tsize, '-'))
        print(lang['deodex_start_app'])
        print('-'.center(tsize, '-'))
        print()
        with cd(appdir):
            applist = sorted(glob.glob('*.apk'), key=str.lower)
        deoappdir = appdir
        deoext = 'apk'
        dodeodexold()
        if odextmp:
            for i in odextmp:
                apk = basename(i).replace('.odex', '.apk')
                os.replace(sysdir + '/app/' + apk, rd + '/' + i)

        if not quiet:
            clears()
        print()
        print('-'.center(tsize, '-'))
        print(lang['deodex_start_priv'])
        print('-'.center(tsize, '-'))
        print()
        with cd(privdir):
            applist = sorted(glob.glob('*.apk'), key=str.lower)
        deoappdir = privdir
        deoext = 'apk'
        dodeodexold()
        if not quiet:
            clears()
        print()
        print('-'.center(tsize, '-'))
        print(lang['deodex_start_frame'])
        print('-'.center(tsize, '-'))
        print()
        with cd(framedir):
            applist = sorted(glob.glob('*.jar'), key=str.lower)
        deoappdir = framedir
        deoext = 'jar'
        dodeodexold()
        with cd(framedir):
            applist = sorted(glob.glob('*.apk'), key=str.lower)
        deoappdir = framedir
        deoext = 'apk'
        dodeodexold()
        if not quiet:
            clears()
        print()
        print('-'.center(tsize, '-'))
        print(lang['deodex_clean'])
        print('-'.center(tsize, '-'))
        print()
        print()
        with cd(framedir):
            delpath(*glob.glob('*.odex'))
        with cd(rd):
            stillodexed = '\n'.join(
                findr('system/**/*.odex') + findr('vendor/**/*.odex'))
        if not stillodexed:
            banner(quiet)
            kprint(lang['deodex_complete'], 'g')
            if not quiet:
                exit_deo()
        else:
            banner(quiet)
            kprint(lang['deodex_remain'] + '\n', 'r')
            kprint(stillodexed, 'y')
            if not quiet:
                exit_deo()
        return

    framedir = sysdir + os.sep + 'framework'
    appdir = sysdir + os.sep + 'app'
    privdir = sysdir + os.sep + 'priv-app'

    if not existd(framedir) or not existf(sysdir + '/build.prop'):
        banner(quiet)
        kprint(lang['missing'], 'yrbbo')
        kprint(lang['deodex_copy_frame_prop'], 'r')
        kprint(lang['deodex_copy_frame_prop2'] + color['y'] + romname + '/system')
        if not quiet:
            exit_deo()
        return

    if 'Deodexed' in isodexstatus():
        banner(quiet)
        kprint(lang['deodex_no_odex'], 'r')
        if not quiet:
            exit_deo()
        return

    global api
    api = getprop('ro.build.version.sdk')
    if api >= '21' and not findr(framedir + '/**/boot.oat') + findr(framedir + '/**/boot-ext.oat'):
        banner(quiet)
        kprint(lang['error'], 'yrbbo')
        kprint(lang['deodex_no_boot_oat'], 'r')
        if not quiet:
            exit_deo()
        return

    if not autorom() and not quiet:
        banner()
        kprint(lang['notice'], 'ryb')
        kprint(lang['deodex_disclaimer'], 'b')
        kprint(lang['deodex_disclaimer2'], 'b')
        kprint(lang['deodex_disclaimer3'], 'b')
        kprint(lang['deodex_disclaimer4'] + '\n', 'b')
        print(lang['deodex_try_anyway'])
        reply = getChar()
        if reply != 'y':
            return

    heapsize = get_heapsize()
    sqshtmp = findr(sysdir + '/**/*.sqsh')
    if sqshtmp:
        for i in sqshtmp:
            deodex_sqsh(i)

    for i in [usdir + '/updater-script'] + glob.glob(prfiles + '/symlinks*'):
        grepvf(
            '.*odex\.app|.*odex\.priv-app|.*odex\.framework|.*orig\.applications|.*\.vdex\"', i)

    deodext = ''
    if autorom():
        deodext = getar('deodex_type')
    else:
        if api < '21':
            deodext = 'old'
        elif api in ['21', '22']:
            deodext = 'l'
        elif api == '23' and androidversion != 'N':
            choice = ''
            mnum = '2'
            if not quiet:
                while not choice:
                    banner(quiet)
                    print(lang['deodex_use_method'] + '\n')
                    print('1) oat2dex')
                    print('2) smali/baksmali\n')
                    print(lang['select'])
                    choice = getChar()

                    if choice.isnumeric():
                        if choice < '1' or choice > mnum:
                            continue
                    else:
                        continue

                    if choice == '1':  # START M oat2dex
                        deodext = 'm'
                    elif choice == '2':  # START M smali/baksmali
                        deodext = 'm2'
            else:
                deodext = 'm2'

        elif (api in ['23', '24', '25'] or androidversion == 'N') and androidversion != 'O':
            deodext = 'n2'
        elif (api in ['25', '26', '27'] or androidversion == 'O') and androidversion != 'P':
            deodext = 'o'
        elif api >= '28' or androidversion == 'P':
            deodext = 'p'
        else:
            banner(quiet)
            kprint(lang['error'], 'yrbbo')
            kprint(lang['deodex_no_api'] + '\n', 'r')
            if not quiet:
                exit_deo()
            return

    if deodext == 'old':
        smali = greps(fl('', '.*baksmali'),
                      glob.glob(tools + '/smali/old/*smali*'))[0]
        baksmali = glob.glob(tools + '/smali/old/*baksmali*')[0]
        deodex_old()
        return
    elif deodext in ['l', 'm']:
        oat2dex = choose_oat2dex()
    elif deodext in ['m2', 'n2']:
        smali = choose_jartitle('smali', lang['title_cho_smali'])
        baksmali = choose_jartitle('baksmali', lang['title_cho_baksmali'])
    elif deodext in ['o', 'p']:
        deodex_vdex(deodext)
        return

    deodex(deodext)
    return


def dlfile(url, filename, bit=None):
    try:
        count = 0
        while count < 6:
            if bit:
                print('{}/srkdl/?u={}&p={}&d={}'.format(server1, srkuser, srkpass, url))
                request = requests.get(
                    '{}/srkdl/?u={}&p={}&d={}'.format(server1, srkuser, srkpass, url))
            else:
                print(url)
                request = requests.get(url, stream=True)

            filesize = int(request.headers['Content-length'])

            if filesize < 1:
                count += 1
                sleep(1)
                continue

            if filesize < 1048576:
                filesize = str(round(filesize / 1024)) + ' KB'
            else:
                filesize = str(round(filesize / 1024 / 1024, 2)) + ' MB'

            try:
                rfname = request.headers['content-disposition']
                rfname = re.findall(
                    "filename=(.+)", rfname)[0].replace('"', '').replace(';', '')
            except:
                rfname = filename

            print('\033[0m\033[33m' + rfname + ': ' + filesize + ' ...\033[0m')
            with open(filename, 'wb') as f:
                f.write(request.content)

            del request
            break
    except:
        pass


def dllang():
    banner()
    kprint('Getting language list ...', 'b')
    with cd(tools + '/language'):
        langurl = server1 + '/next/langfiles'

        try:
            langlist = {}
            for i in internet(langurl + '/list', 1).splitlines():
                if srkuser:
                    langlist[i] = langurl + '/' + srkuser + '/' + i + '_srk.zip'
                else:
                    langlist[i] = langurl + '/' + i + '_srk.zip'

            langdl = chlist(color['gb'] + 'Choose language to download:'
                            + color['n'], sorted(list(langlist)), len(list(langlist)))

            banner()
            kprint('Downloading ' + langdl + ' ...', 'b')

            dlfile(langlist[langdl], 'lang.zip')
            zipu2('lang.zip')
            delpath('lang.zip')

            return langdl + '_srk.zip'
        except:
            pass

    return None


def dozipalign():
    with cd(rd):
        alltmp = findr('**/*.apk')
        alltmp = grepv('.*00_project_files', alltmp)

        if existf(prfiles + '/AR-config'):
            reply = 'y'
        else:
            banner()
            print(lang['zipalign_frame_q'])
            reply = getChar()

        if reply != 'y':
            alltmp = grepv('.*/framework/', alltmp)

        for i in alltmp:
            try:
                zalignchk = cmd(zipalign + ' -c -v 4 '
                                + i).splitlines()[-1].split()[1]
            except Exception as e:
                appendf(logtb(e), logs + '/main.log')
                continue

            # app = basename(i)

            if zalignchk != 'FAILED':
                kprint(lang['menu_skip'] + ': ' + i, 'g')
                continue

            kprint(lang['zipalign'] + ': ' + i + ' ...', 'b')
            appendf(cmd(zipalign + ' 4 ' + i + ' ' + i + '-2'), logs + '/main.log')

            if existf(i + '-2'):
                os.replace(i + '-2', i)
            else:
                delpath(i + '-2')


def dsize(folder='.'):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += dsize(itempath)
    return total_size


def e2fsdroid_run(argv, base_features, ext4_features):
    def RunCommand(cmd, env):
        """Runs the given command.

        Args:
                cmd: the command represented as a list of strings.
                env: a dictionary of additional environment variables.
        Returns:
                A tuple of the output and the exit code.
        """
        env_copy = os.environ.copy()
        env_copy.update(env)

        # mainlog.append("Env: {}".format(env))
        mainlog.append("Running: " + basename(cmd[0]))
        # mainlog.append("Running: " + ' '.join(cmd))

        p = Popen(cmd, stdout=PIPE, stderr=STDOUT,
                  env=env_copy)
        output, _ = p.communicate()

        return output.decode(), p.returncode

    def ParseArguments(argv):
        """Parses the input arguments to the program."""

        parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)

        parser.add_argument(
            "src_dir", help="The source directory for user image.")
        parser.add_argument(
            "output_file", help="The path of the output image file.")
        parser.add_argument("ext_variant", choices=["ext2", "ext4"],
                            help="Variant of the extended filesystem.")
        parser.add_argument(
            "mount_point", help="The mount point for user image.")
        parser.add_argument("fs_size", help="Size of the file system.")
        parser.add_argument("file_contexts", nargs='?',
                            help="The selinux file context.")

        parser.add_argument("--android_sparse", "-s", action="store_true",
                            help="Outputs an android sparse image (mke2fs).")
        parser.add_argument("--journal_size", "-j",
                            help="Journal size (mke2fs).")
        parser.add_argument("--timestamp", "-T",
                            help="Fake timetamp for the output image.")
        parser.add_argument("--fs_config", "-C",
                            help="Path to the fs config file (e2fsdroid).")
        parser.add_argument("--product_out", "-D",
                            help="Path to the directory with device specific fs"
                                 " config files (e2fsdroid).")
        parser.add_argument("--block_list_file", "-B",
                            help="Path to the block list file (e2fsdroid).")
        parser.add_argument("--key", "-K",
                            help="Key to run (e2fsdroid).")
        parser.add_argument("--prfiles", "-P",
                            help="Project files path (e2fsdroid).")
        parser.add_argument("--partition", "-X",
                            help="Partition (e2fsdroid).")
        parser.add_argument("--base_alloc_file_in", "-d",
                            help="Path to the input base fs file (e2fsdroid).")
        parser.add_argument("--base_alloc_file_out", "-A",
                            help="Path to the output base fs file (e2fsdroid).")
        parser.add_argument("--label", "-L",
                            help="The mount point (mke2fs).")
        parser.add_argument("--inodes", "-i",
                            help="The extfs inodes count (mke2fs).")
        parser.add_argument("--inode_size", "-I",
                            help="The extfs inode size (mke2fs).")
        parser.add_argument("--reserved_percent", "-M",
                            help="The reserved blocks percentage (mke2fs).")
        parser.add_argument("--flash_erase_block_size", "-e",
                            help="The flash erase block size (mke2fs).")
        parser.add_argument("--flash_logical_block_size", "-o",
                            help="The flash logical block size (mke2fs).")
        parser.add_argument("--mke2fs_uuid", "-U",
                            help="The mke2fs uuid (mke2fs) .")
        parser.add_argument("--mke2fs_hash_seed", "-S",
                            help="The mke2fs hash seed (mke2fs).")
        parser.add_argument("--share_dup_blocks", "-c", action="store_true",
                            help="ext4 share dup blocks (e2fsdroid).")

        args, remainder = parser.parse_known_args(argv)
        # The current argparse doesn't handle intermixed arguments well. Checks
        # manually whether the file_contexts exists as the last argument.
        # TODO(xunchang) use parse_intermixed_args() when we switch to python 3.7.
        if len(remainder) == 1 and remainder[0] == argv[-1]:
            args.file_contexts = remainder[0]
        elif remainder:
            parser.print_usage()
            return 1

        return args

    def ConstructE2fsCommands(args):
        """Builds the mke2fs & e2fsdroid command based on the input arguments.

        Args:
                args: The result of ArgumentParser after parsing the command line arguments.
        Returns:
                A tuple of two lists that serve as the command for mke2fs and e2fsdroid.
        """

        BLOCKSIZE = 4096

        e2fsdroid_opts = []
        mke2fs_extended_opts = []
        mke2fs_opts = []

        if args.android_sparse:
            mke2fs_extended_opts.append("android_sparse")
        else:
            e2fsdroid_opts.append("-e")
        if args.timestamp:
            e2fsdroid_opts += ["-T", args.timestamp]
        if args.fs_config:
            e2fsdroid_opts += ["-C", args.fs_config]
        if args.product_out:
            e2fsdroid_opts += ["-p", args.product_out]
        if args.block_list_file:
            e2fsdroid_opts += ["-B", args.block_list_file]
        if args.key:
            e2fsdroid_opts += ["-K", args.key]
        if args.prfiles:
            e2fsdroid_opts += ["-P", args.prfiles]
        if args.partition:
            e2fsdroid_opts += ["-X", args.partition]
        if args.base_alloc_file_in:
            e2fsdroid_opts += ["-d", args.base_alloc_file_in]
        if args.base_alloc_file_out:
            e2fsdroid_opts += ["-D", args.base_alloc_file_out]
        if args.share_dup_blocks:
            e2fsdroid_opts.append("-s")
        if args.file_contexts:
            e2fsdroid_opts += ["-S", args.file_contexts]

        if args.flash_erase_block_size:
            mke2fs_extended_opts.append("stripe_width={}".format(
                int(args.flash_erase_block_size) / BLOCKSIZE))
        if args.flash_logical_block_size:
            # stride should be the max of 8kb and the logical block size
            stride = max(int(args.flash_logical_block_size), 8192)
            mke2fs_extended_opts.append("stride={}".format(stride / BLOCKSIZE))
        if args.mke2fs_hash_seed:
            mke2fs_extended_opts.append("hash_seed=" + args.mke2fs_hash_seed)

        if args.journal_size:
            if args.journal_size == "0":
                mke2fs_opts += ["-O", "^has_journal"]
            else:
                mke2fs_opts += ["-J", "size=" + args.journal_size]
        if args.label:
            mke2fs_opts += ["-L", args.label]
        if args.inodes:
            mke2fs_opts += ["-N", args.inodes]
        if args.inode_size:
            mke2fs_opts += ["-I", args.inode_size]
        if args.mount_point:
            mke2fs_opts += ["-M", args.mount_point]
        if args.reserved_percent:
            mke2fs_opts += ["-m", args.reserved_percent]
        if args.mke2fs_uuid:
            mke2fs_opts += ["-U", args.mke2fs_uuid]
        if mke2fs_extended_opts:
            mke2fs_opts += ["-E", ','.join(mke2fs_extended_opts)]

        # Round down the filesystem length to be a multiple of the block size
        blocks = int(int(args.fs_size) / BLOCKSIZE)
        mke2fs_cmd = ([mke2fs] + mke2fs_opts
                      + ["-t", args.ext_variant, "-b", str(BLOCKSIZE), args.output_file,
                         str(blocks)])

        e2fsdroid_cmd = ([e2fsdroid] + e2fsdroid_opts
                         + ["-f", args.src_dir, "-a", args.mount_point,
                            args.output_file])

        return mke2fs_cmd, e2fsdroid_cmd

    # START MAIN
    args = ParseArguments(argv)
    if not os.path.isdir(args.src_dir):
        return "Can not find directory " + args.src_dir
    if not args.mount_point:
        return "Mount point is required"
    if args.mount_point[0] != '/':
        args.mount_point = '/' + args.mount_point
    if not args.fs_size:
        return "Size of the filesystem is required"

    mainlog = ['\n[INFO] Building '
               + ('sparse ' if args.android_sparse else '') + args.partition + '_new.img\n']

    mke2fs_cmd, e2fsdroid_cmd = ConstructE2fsCommands(args)

    # truncate output file since mke2fs will keep verity section in existing file
    with open(args.output_file, 'w') as output:
        output.truncate()

    # run mke2fs
    with tempfile.NamedTemporaryFile() as conf_file:
        conf_data = open(tools + '/source/mke2fs.conf', 'rb').read()
        conf_data = sed('sparse_super,large_file,filetype,dir_index,ext_attr',
                        ','.join(base_features), conf_data.decode()).encode()
        conf_data = sed('has_journal,extent,huge_file,dir_nlink,extra_isize,uninit_bg',
                        ','.join(ext4_features), conf_data.decode()).encode()
        conf_file.write(conf_data)
        conf_file.flush()
        mke2fs_env = {"MKE2FS_CONFIG": conf_file.name}

        if args.timestamp:
            mke2fs_env["E2FSPROGS_FAKE_TIME"] = args.timestamp

        output, ret = RunCommand(mke2fs_cmd, mke2fs_env)
        # print(output)
        mainlog.append(output)
        if ret != 0:
            return '\n'.join(mainlog)

    # run e2fsdroid
    e2fsdroid_env = {}
    if args.timestamp:
        e2fsdroid_env["E2FSPROGS_FAKE_TIME"] = args.timestamp

    output, ret = RunCommand(e2fsdroid_cmd, e2fsdroid_env)
    # The build script is parsing the raw output of e2fsdroid; keep the pattern
    # unchanged for now.
    mainlog.append(output)
    # print(output)
    if ret != 0:
        os.remove(args.output_file)

    return '\n'.join(mainlog)


def escape_char(thestring):
    charlist = ['(', ')', '[', ']', '{', '}']

    for i in charlist:
        thestring = thestring.replace(i, '\\' + i)

    return thestring


def existd(mydir):
    return os.path.isdir(mydir)


def existf(filename):
    if os.path.isfile(filename):
        if os.stat(filename).st_size > 0:
            return True

    return False


def ext4_header(filename, sparse=None, BLOCKSIZE=512):
    def lsb2hex(b_string):
        msb_string = hexlify(b_string).decode()
        lsb_string = ''.join([msb_string[x:x + 2]
                              for x in range(0, len(msb_string), 2)][::-1])
        return lsb_string

    def lsb2ascii(b_string):
        msb_string = hexlify(b_string).decode()
        pairs = (msb_string[x:x + 2] for x in range(0, len(msb_string), 2))
        values = (int(x, 16) for x in pairs)
        return ''.join(map(chr, values))

    def lsb2int(b_string):
        lsb_string = lsb2hex(b_string)
        return int(lsb_string, 16)

    def uuid(h_string):
        def split(x): return [x[:8], x[8:12], x[12:16], x[16:20], x[20:]]

        return '-'.join(split(h_string))

    def timestamp(seconds):
        return datetime.fromtimestamp(seconds)

    def map_bitmap(value, mapping):
        return ' '.join([t[1] for t in mapping if value & t[0]]) or 'none'

    superblock = OrderedDict()

    if sparse:
        with open(filename, 'rb') as f:
            superblock['FS magic number'] = hex(lsb2int(f.read(4)))
            superblock['Major Version'] = lsb2int(f.read(2))
            superblock['Minor Version'] = lsb2int(f.read(2))
            superblock['File Header Size'] = lsb2int(f.read(2))
            superblock['Chunk Header Size'] = lsb2int(f.read(2))
            superblock['Block size'] = lsb2int(f.read(4))
            superblock['Total Blocks'] = lsb2int(f.read(4))
            superblock['Raw Size'] = superblock['Block size'] * \
                                     superblock['Total Blocks']

        return superblock

    try:
        with open(filename, 'rb') as f:
            f.seek(2 * BLOCKSIZE)
            # Bytes 0-15
            inodes_total = 0
            try:
                inodes_total = lsb2int(f.read(4))
            except:
                pass

            if not inodes_total:
                return superblock

            superblock['Inode count'] = inodes_total
            superblock['Block count'] = lsb2int(f.read(4))
            superblock['Reserved block count'] = lsb2int(f.read(4))
            superblock['Free blocks'] = lsb2int(f.read(4))

            # Bytes 16-31
            superblock['Free inodes'] = lsb2int(f.read(4))
            superblock['First block'] = lsb2int(f.read(4))
            val = lsb2int(f.read(4))
            superblock['Block size'] = 1024 * 2 ** val
            superblock['Fragment size'] = 1024 * 2 ** lsb2int(f.read(4))

            # Bytes 32-47
            superblock['Blocks per group'] = lsb2int(f.read(4))
            superblock['Fragments per group'] = lsb2int(f.read(4))
            inodes_per_group = lsb2int(f.read(4))
            superblock['Inodes per group'] = inodes_per_group
            superblock['Block groups'] = int(inodes_total / inodes_per_group)
            mtime = lsb2int(f.read(4))
            superblock['Last mount time'] = (
                '{0:%Y-%m-%d %H:%M:%S}'.format(timestamp(mtime)) if mtime else 'n/a')

            # Bytes 48-63
            wtime = lsb2int(f.read(4))
            superblock['Last write time'] = '{0:%Y-%m-%d %H:%M:%S}'.format(
                timestamp(wtime))
            superblock['Mount count'] = lsb2int(f.read(2))
            superblock['Mounts before check'] = lsb2int(f.read(2))
            superblock['FS magic number'] = '{0:#X}'.format(lsb2int(f.read(2)))

            if superblock['FS magic number'] != '0XEF53':
                superblock = {'not_ext4': 1}
                raise ValueError

            fs_state = lsb2int(f.read(2))
            fs_state_s = [
                'clean',
                'errors',
                'orphans'
            ]
            superblock['Filesystem state'] = fs_state_s[fs_state - 1]

            er_behave = lsb2int(f.read(2))
            er_behave_s = [
                'continue',
                'remount',
                'panic'
            ]
            superblock['Errors behavior'] = er_behave_s[er_behave - 1]
            superblock['Minor revision level'] = lsb2int(f.read(2))

            # Bytes 64-79
            lastcheck = lsb2int(f.read(4))
            superblock['Time of last check'] = '{0:%Y-%m-%d %H:%M:%S}'.format(
                timestamp(lastcheck))
            checkinterval = lsb2int(f.read(4))
            superblock['Time between checks'] = checkinterval
            os_file = lsb2int(f.read(4))
            os_file_s = [
                'Linux',
                'Hurd',
                'Masix',
                'FreeBSD',
                'Lites'
            ]
            superblock['FS OS type'] = os_file_s[os_file]
            superblock['FS revision #'] = lsb2int(f.read(4))

            # Bytes 80-95
            superblock['Reserved blocks uid'] = lsb2int(f.read(2))
            superblock['Reserved blocks gid'] = lsb2int(f.read(2))
            superblock['First inode'] = lsb2int(f.read(4))
            superblock['Inode size'] = lsb2int(f.read(2))
            superblock['Superblock group'] = lsb2int(f.read(2))
            feature_compat = lsb2int(f.read(4))
            feature_compat_s = map_bitmap(feature_compat, (
                (0x1, 'dir_prealloc'),
                (0x2, 'imagic_inodes'),
                (0x4, 'has_journal'),
                (0x8, 'ext_attr'),
                (0x10, 'resize_inode'),
                (0x20, 'dir_index'),
                (0x40, 'lazy_bg'),
                (0x80, 'exclude_inode'),
                (0x200, 'sparse_super2')
            ))

            # Bytes 96-103
            feature_incompat = lsb2int(f.read(4))
            feature_incompat_s = map_bitmap(feature_incompat, (
                (0x1, 'compression'),
                (0x2, 'filetype'),
                (0x4, 'recover'),
                (0x8, 'journal_dev'),
                (0x10, 'meta_bg'),
                (0x40, 'extents'),
                (0x80, '64bit'),
                (0x100, 'mmp'),
                (0x200, 'flex_bg'),
                (0x400, 'ea_inode'),
                (0x1000, 'dirdata'),
                (0x2000, 'metadata_csum_seed'),
                (0x4000, 'large_dir'),
                (0x8000, 'inline_data'),
                (0x10000, 'encrypt'),
            ))

            feature_ro_compat = lsb2int(f.read(4))
            feature_ro_compat_s = map_bitmap(feature_ro_compat, (
                (0x1, 'sparse_super'),
                (0x2, 'large_file'),
                (0x4, 'btree_dir'),
                (0x8, 'huge_file'),
                (0x20, 'dir_nlink'),
                (0x40, 'extra_isize'),
                (0x100, 'quota'),
                (0x200, 'bigalloc'),
                (0x800, 'replica'),
                (0x1000, 'read-only'),
                (0x2000, 'project'),
                (0x4000, 'shared_blocks')
            ))
            superblock['FS features'] = '{} {} {}'.format(
                feature_compat_s, feature_incompat_s, feature_ro_compat_s)

            # Bytes 104-119
            superblock['FS UUID'] = uuid(hexlify(f.read(16)).decode())

            # Bytes 120-135
            superblock['FS volume name'] = lsb2ascii(f.read(16)).strip('\x00')

            # Bytes 136-199
            superblock['Last mounted on'] = lsb2ascii(f.read(64)).strip('\x00')

            # Bytes 200-205
            f.read(6)  # padding
            # algo_bitmap = lsb2int(f.read(4))
            # algo_bitmap_s = map_bitmap(algo_bitmap, (
            # 	(0x1, 'lzv1'),
            # 	(0x2, 'lzrw3a'),
            # 	(0x4, 'gzip'),
            # 	(0x8, 'bzip3'),
            # 	(0x10, 'lzo'),
            # ))
            # superblock['Compression Algorithm'] = algo_bitmap_s
            # superblock['Preallocate'] = lsb2int(f.read(1))
            # superblock['Preallocate for dir'] = lsb2int(f.read(1))

            # Bytes 208-235
            superblock['Reserved GDT blocks'] = lsb2int(f.read(2))
            superblock['Journal UUID'] = uuid(hexlify(f.read(16)).decode())
            superblock['Journal inode number'] = lsb2int(f.read(4))
            superblock['Journal device number'] = lsb2int(f.read(4))
            superblock['Journal last orphan'] = lsb2int(f.read(4))

            # Bytes 236-255
            superblock['Directory Hash Seed'] = uuid(
                hexlify(f.read(16)).decode())

            hash_version = lsb2int(f.read(1))
            hash_version_s = [
                'legacy',
                'half_md4',
                'tea',
                'legacy_unsigned',
                'half_md4_unsigned',
                'tea_unsigned'
            ]
            superblock['Default directory hash'] = hash_version_s[hash_version]
            f.read(3)  # Padding

            # Bytes 256-263
            defm_options = lsb2int(f.read(4))
            defm_options_s = map_bitmap(defm_options, (
                (0x1, 'debug'),
                (0x2, 'bsdgroups'),
                (0x4, 'xattr_user'),
                (0x8, 'acl'),
                (0x10, 'uid16'),
            ))
            superblock['Default mount options'] = defm_options_s
            superblock['First meta block gid'] = lsb2int(f.read(4))
    except:
        if superblock.get('not_ext4'):
            pass
        else:
            superblock = {}

    return superblock


def ext4Xtract(whatimg, *vargs):
    def ext4Xtract_o():
        import ext4
        import string
        import io

        def scan_dir(root_inode, root_path=''):
            for entry_name, entry_inode_idx, entry_type in root_inode.open_dir():
                if not entry_name or entry_name in ['.', '..', 'lost+found'] or entry_name.endswith(' (2)'):
                    continue

                entry_inode = root_inode.volume.get_inode(
                    entry_inode_idx, entry_type)
                entry_inode_path = root_path + '/' + entry_name

                wdone = None
                if not vargs or ('f' in vargs or 'c' in vargs):
                    mode = getperm(entry_inode.mode_str)
                    uid = str(entry_inode.inode.i_uid)
                    gid = str(entry_inode.inode.i_gid)
                    con = '?'
                    cap = ''

                    for i in list(entry_inode.xattrs()):
                        if i[0] == 'security.selinux':
                            try:
                                con = i[1].decode('utf8')[:-1]
                            except:
                                con = '?'

                        elif i[0] == 'security.capability':
                            captmp = i[1][4:8] + i[1][12:16]
                            if captmp:
                                cap = ' capabilities=' + \
                                      str(int.from_bytes(captmp, "little"))
                            else:
                                appendf('Capabilities error: '
                                        + entry_inode_path, logs + '/ext4_extract.log')

                if entry_inode.is_dir:
                    if not vargs or 'e' in vargs:
                        try:
                            mkdir(whatimg + entry_inode_path)
                        except:
                            if entry_inode_path.endswith('.'):
                                appendf('Directory renamed without trailing . due to NTFS restrictions:\n'
                                        + entry_inode_path, logs + '/ext4_extract.log')
                                entry_inode_path = entry_inode_path[:-1]
                                mkdir(whatimg + entry_inode_path)
                            else:
                                appendf('Directory error: ' + entry_inode_path,
                                        logs + '/ext4_extract.log')
                                continue

                    scan_dir(entry_inode, entry_inode_path)
                else:
                    if entry_type != 7:
                        try:
                            raw = entry_inode.open_read().read()
                        except Exception as e:
                            appendf(entry_inode_path, logs + '/ext4_extract.log')
                            appendf(logtb(e), logs + '/ext4_extract.log')
                            continue

                        if not vargs or 'e' in vargs:
                            mkdir(whatimg + os.sep + dirname(entry_inode_path))

                            if entry_name.endswith('/'):
                                entry_name = entry_name[:-1]

                            if case_fix == 'Yes' and findfiles(entry_name,
                                                               whatimg + os.sep + dirname(entry_inode_path)):
                                cnt = len(
                                    findfiles(entry_name + '.*', whatimg + os.sep + dirname(entry_inode_path)))

                                with cd(whatimg + os.sep + dirname(entry_inode_path)):
                                    with open(entry_name + '.ex' + str(cnt) + '.srk', 'wb') as o:
                                        o.write(raw)

                                new_fp = dirname(entry_inode_path)
                                new_fp = new_fp + \
                                         (entry_name if new_fp.endswith(
                                             '/') else '/' + entry_name)

                                ci_files = getconf(
                                    'case_files_' + whatimg, uconf, l=1)
                                if new_fp not in ci_files:
                                    getconf('case_files_' + whatimg, uconf,
                                            add=ci_files + [new_fp], l=1)

                                wdone = 1

                            if not wdone:
                                with cd(whatimg + os.sep + dirname(entry_inode_path)):
                                    with open(entry_name, 'wb') as o:
                                        o.write(raw)
                    else:
                        if not vargs or 's' in vargs:
                            try:
                                link_target = entry_inode.open_read().read().decode("utf8")
                                if not all(c in string.printable for c in link_target):
                                    raise ValueError
                                symlinks.append(
                                    link_target + ' ' + whatimg + entry_inode_path)
                            except:
                                try:
                                    link_target_block = int.from_bytes(
                                        entry_inode.open_read().read(), "little")
                                    link_target = root_inode.volume.read(
                                        link_target_block * root_inode.volume.block_size,
                                        entry_inode.inode.i_size).decode("utf8")

                                    if link_target and all(c in string.printable for c in link_target):
                                        symlinks.append(
                                            link_target + ' ' + whatimg + entry_inode_path)
                                    else:
                                        appendf(
                                            'Failed symlink: ' + whatimg + entry_inode_path, logs + '/ext4_extract.log')

                                        continue
                                except:
                                    appendf('Failed symlink 2: ' + whatimg
                                            + entry_inode_path, logs + '/ext4_extract.log')

                                    continue

                if not vargs or ('f' in vargs or 'c' in vargs):
                    if dirr:
                        if not vargs or 'c' in vargs:
                            contexts.append(
                                '/' + whatimg + entry_inode_path + ' ' + con)

                        if not vargs or 'f' in vargs:
                            fsconfig.append(
                                whatimg + entry_inode_path + ' ' + uid + ' ' + gid + ' ' + mode + cap)
                    else:
                        if not vargs or 'c' in vargs:
                            contexts.append(entry_inode_path + ' ' + con)

                        if not vargs or 'f' in vargs:
                            fsconfig.append(
                                entry_inode_path[1:] + ' ' + uid + ' ' + gid + ' ' + mode + cap)

        appendf('Extracting ' + whatimg + '.img with Python ...',
                logs + '/ext4_extract.log')

        try:
            with open(whatimg + '.img', 'r+b') as f:
                root = ext4.Volume(f, ignore_flags=True)

                stored_block_count = int(root.superblock.s_blocks_count)

                f.seek(0, io.SEEK_END)
                volume_size = f.tell()

                real_block_count = int(volume_size / root.block_size)

                if stored_block_count > real_block_count:
                    f.truncate(stored_block_count * root.block_size)
        except Exception as e:
            if type(e).__name__ == 'MagicError':
                appendf(logtb(e), logs + '/ext4_extract.log')

                return 4
            else:
                appendf(logtb(e), logs + '/ext4_extract.log')

                return 1

        with open(whatimg + '.img', 'rb') as f:
            root = ext4.Volume(f).root

            if not vargs or ('f' in vargs or 'c' in vargs or 's' in vargs):
                dirlist = []
                for file_name, inode_idx, file_type in root.open_dir():
                    dirlist.append(file_name)

                dirr = whatimg
                if ('init.rc' in dirlist or 'init.environ.rc' in dirlist) and whatimg in dirlist:
                    dirr = ''

                symlinks = []
                contexts = []
                fsconfig = []
                if dirr or whatimg in ['vendor', 'oem', 'product', 'system_ext']:
                    try:
                        contexts = ['/' + whatimg + ' '
                                    + list(root.xattrs())[0][1][:-1].decode('utf8')]
                    except:
                        pass

                if dirr:
                    try:
                        fsconfig = [
                            f'{whatimg} {str(root.inode.i_uid)} {str(root.inode.i_gid)} {getperm(root.mode_str)}']
                    except:
                        if whatimg in ['system', 'product', 'system_ext']:
                            fsconfig = [whatimg + ' 0 0 0755']
                        elif whatimg in ['vendor', 'oem']:
                            fsconfig = [whatimg + ' 0 2000 0755']

            case_fix = getconf('case_fix', mconf)

            try:
                scan_dir(root)
            except Exception as e:
                appendf(logtb(e), logs + '/ext4_extract.log')
                delpath(whatimg)

                if platf in ['lin', 'mac', 'wsl2']:
                    return 2

                return 3

        delpath(prfiles + '/symlinks-' + whatimg, prfiles + '/fs_config-'
                + whatimg, prfiles + '/file_contexts3-' + whatimg)

        if not vargs or 's' in vargs:
            for i in sorted(symlinks):
                try:
                    appendf(
                        'symlink("' + i.split()[0] + '", "/' + i.split()[1] + '");', prfiles + '/symlinks-' + whatimg)
                except:
                    pass

            del symlinks

        if not vargs or 'f' in vargs:
            appendf('\n'.join(sorted(fsconfig)), prfiles + '/fs_config-' + whatimg)
            del fsconfig

        if not vargs or 'c' in vargs:
            if not greps(f'/{whatimg} ', contexts):
                rootcon = f'/{whatimg} u:object_r:{whatimg}_file:s0'
                try:
                    rootcon = '/' + whatimg + ' ' + \
                              greps('/' + whatimg + '/bin |/' + whatimg
                                    + '/lib ', contexts)[0].split()[1]
                except:
                    pass

                if rootcon not in contexts:
                    contexts.append(rootcon)

            appendf('\n'.join(sorted(contexts)),
                    prfiles + '/file_contexts3-' + whatimg)
            del contexts

        if whatimg == 'system' and sar():
            case_files = []
            for i in getconf('case_files_' + whatimg, uconf, l=1):
                case_files.append(i.replace(whatimg + '/', '', 1))

            if case_files:
                getconf('case_files_' + whatimg, uconf, add=case_files, l=1)

        return 0

    def ext4Xtract_m():
        appendf(f'Extracting {whatimg}.img with Mount ...',
                logs + '/ext4_extract.log')

        mkdir('output')

        appendf(cmd(f'sudo mount -t auto -o loop,ro {whatimg}.img output/'), logs + '/ext4_extract.log')

        geotest = cmd('dmesg | tail -n 1')

        if 'geometry' in geotest:
            geotest = geotest.strip().split()[7]
            appendf(geotest, logs + '/ext4_extract.log')
            appendf(cmd(f'truncate -o -s {geotest} {whatimg}.img'),
                    logs + '/ext4_extract.log')
            appendf(cmd(f'sudo mount -t auto -o loop,ro {whatimg}.img output/'), logs + '/ext4_extract.log')

            geotest = cmd('dmesg | tail -n 1')
            if 'geometry' in geotest:
                appendf(geotest, logs + '/ext4_extract.log')
                delpath('output')
                return 1

        if not glob.glob('output/*'):
            appendf(f'ERROR: {whatimg}.img is not a valid ext4 img.',
                    logs + '/ext4_extract.log')
            delpath('output')
            return 1

        mkdir(whatimg)
        appendf(cmd(f'sudo {tools_local}startup.py --otherfile {tools_local}getmeta.py output {whatimg} {prfiles}'),
                logs + '/ext4_extract.log')

        cmd(f'sudo chmod -R a+rwX {whatimg}')
        cmd('sudo chown -hR ' + whoami() + ':' + whoami() + ' ' + prfiles)

        cmd('sudo umount output/')
        delpath('output')

        return 0

    def ext4Xtract_7():
        appendf(f'Extracting {whatimg}.img with 7-zip ...',
                logs + '/ext4_extract.log')

        delpath(whatimg, prfiles + '/symlinks-' + whatimg, prfiles
                + '/fs_config-' + whatimg, prfiles + '/file_contexts3-' + whatimg)
        appendf(cmd(p7z + ' x -y -o' + whatimg + ' ' + whatimg + '.img'), logs + '/main.log')
        delpath(whatimg + os.sep + '[SYS]')

        def group_path(source):
            buffer = []
            for line in source:
                if line.startswith('Path ='):
                    if buffer:
                        yield buffer
                    buffer = [line.strip()]
                else:
                    buffer.append(line.strip())
            yield buffer

        appendf(cmd(p7z + ' l -slt ' + whatimg + '.img'), prfiles + '/testfile')

        if existf(prfiles + '/testfile') and grepf('Symbolic\ Link\ ', prfiles + '/testfile'):
            grepff(fl('Symbolic Link |Mode |Group |User |Path ', '.*'
                      + whatimg + '\.img'), prfiles + '/testfile', prfiles + '/testfile2')
        else:
            delpath(prfiles + '/testfile')
            return 1

        with open(prfiles + '/testfile2', 'r') as source:
            symlinks = []
            filer = []
            for line in group_path(source):
                p = line[0].split(' = ')[1].replace('\\', '/')
                if '[SYS]' in p:
                    continue
                if line[2] != 'Symbolic Link =':
                    sline = line[2].split(' = ')[1].replace('\\', '/')
                    dline = '/' + whatimg + '/' + p

                    symlinks.append(
                        'symlink("{}", "{}");'.format(sline, dline))
                    delpath(whatimg + os.sep + line[0].split(' = ')[1])

                u = line[3].split(' = ')[1]
                g = line[4].split(' = ')[1]
                m = getperm(line[1].split(' = ')[1])
                filer.append(whatimg + '/' + p + ' ' + u + ' ' + g + ' ' + m)

            line = greps(whatimg + '/app ', filer)[0].split()

            filer.append(whatimg + ' ' + line[1] + ' ' + line[2] + ' ' + line[3])

        delpath(prfiles + '/testfile', prfiles + '/testfile2')

        appendf('\n'.join(sorted(symlinks)), prfiles + '/symlinks-' + whatimg)
        del symlinks
        appendf('\n'.join(sorted(filer)), prfiles + '/fs_config-' + whatimg)
        del filer

        get_contexts()

        return 0

    if platf in ['lin', 'mac', 'wsl2'] and getconf('mount_extract', mconf) == 'Yes':
        if ext4Xtract_m() == 1:
            return 1
    else:
        xtractv = ext4Xtract_o()
        if xtractv == 1:
            return 1
        elif xtractv == 2:
            xtractv = ext4Xtract_m()
            if xtractv == 1:
                xtractv = ext4Xtract_7()
                if xtractv == 1:
                    return 1
        elif xtractv == 3:
            xtractv = ext4Xtract_7()
            if xtractv == 1:
                return 1
        elif xtractv == 4:
            return 4

    return 0


def findimgsize(whatimg):
    choice = ''
    imgsize = ''

    devicename = get_devicename()
    deviceloc = tools + os.sep + 'devices' + os.sep + devicename

    while not choice:
        numtmp = '3'
        banner()
        kprint(lang['extract_cho_part_detect']
               + color['n'] + color['gb'] + whatimg + '\n', 'ryb')
        print('1) ' + lang['extract_adb_shell'])
        print('2) ' + lang['extract_project_dir'] + whatimg)
        print('3) ' + lang['extract_manual'])
        if existf(rd + '/' + whatimg + '.img'):
            numtmp = '4'
            print('4) ' + whatimg + '.img')
        elif whatimg == 'data' and existf(rd + '/user' + whatimg + '.img'):
            numtmp = '4'
            print('4) user' + whatimg + '.img')

        kprint('q = ' + lang['menu_quit'] + '\n', 'm')
        print(lang['select'])
        choice = getChar()

        if choice.isnumeric():
            if choice < '1' or choice > numtmp:
                continue
        elif choice not in ['q']:
            continue

        if choice == '1':  # START Device through adb shell
            banner()
            print(lang['byname_usb_debug'] + '\n')
            kprint(lang['byname_usb_debug_root'], 'ryb')
            kprint(lang['byname_usb_debug_root2'] + '\n', 'r')
            print(lang['general_continue_q'])
            reply = getChar()
            if reply != 'y':
                return

            banner()
            kprint(lang['extract_detect'] + whatimg + ' ...', 'b')
            if existf(deviceloc + '/superr_mmc'):
                imgblock = grepf(whatimg, deviceloc
                                 + '/superr_mmc')[0].split()[0].split('/')[3]
            else:
                newname = ''
                if existf(deviceloc + '/superr_appbyname'):
                    tmpbn = {'system': 'APP', 'vendor': 'VNR',
                             'data': 'UDA', 'boot': 'LNX', 'recovery': 'SOS'}
                elif existf(deviceloc + '/superr_kerbyname'):
                    tmpbn = {'system': 'SYSTEM', 'boot': 'KERNEL',
                             'recovery': 'RECOVERY', 'data': 'userdata'}
                else:
                    tmpbn = {'data': 'userdata'}

                if whatimg in list(tmpbn):
                    newname = tmpbn[whatimg]

                if not newname:
                    newname = whatimg

                appendf(cmd(adb + ' "wait-for-device"'), logs + '/adb.log')

                manu = cmd(
                    adb + ' shell getprop ro.product.manufacturer').strip()
                if manu.lower() == 'samsung':
                    newname = newname.upper()

                byname = adb_byname(deviceloc)
                imgblock = None
                try:
                    imgblock = greps(
                        ' ' + newname + ' ', cmd(adb + ' shell su -c "ls -al ' + byname + '"').splitlines())[0].split()[
                        -1]
                    appendf('imgblock: ' + imgblock, logs + '/adb.log')
                except Exception as e:
                    appendf(logtb(e), logs + '/adb.log')

            rawsize = None
            if imgblock:
                try:
                    appendf(cmd(adb + ' "wait-for-device"'), logs + '/adb.log')
                    rawsize = greps(basename(imgblock), cmd(
                        adb + ' shell su -c "cat /proc/partitions"').splitlines())[0].split()[2]
                    appendf('rawsize: ' + rawsize, logs + '/adb.log')
                except Exception as e:
                    appendf(logtb(e), logs + '/adb.log')

            if not rawsize:
                banner()
                kprint(lang['error_mess'] + '\n', 'r')
                input(lang['enter_cho_another_detection'])
                choice = ''
                continue

            imgsize = str(int(rawsize) * 1024)
            appendf('imgsize: ' + imgsize, logs + '/adb.log')
        elif choice == '2':  # START Project $whatimg directory (BETA)
            banner()
            kprint(lang['warning'], 'yrbbo')
            kprint(lang['extract_beta'], 'r')
            kprint(lang['extract_beta2'] + '\n', 'r')
            kprint(lang['extract_beta3'] + '\n', 'y')
            kprint(lang['extract_beta4'], 'r')
            kprint(lang['extract_beta5'] + '\n', 'r')
            print(lang['general_cont_anyway_q'])
            reply = getChar()
            if reply != 'y':
                return

            imgsize = str(int(dsize(rd + '/' + whatimg) * 1.039711841))
        elif choice == '3':  # START Enter it manually in bytes
            man_img_size = getconf('img_size_' + whatimg, uconf)

            from_mconf = None

            if not man_img_size:
                man_img_size = getconf('img_size_' + whatimg, mconf)
                from_mconf = 1

            whatsize = None
            if man_img_size:
                banner()
                print(lang['build_man_img_size'] + '\n\n' + man_img_size)
                if getChar() == 'y':
                    whatsize = man_img_size

            if not whatsize:
                banner()
                print(lang['extract_manual_bytes'] + whatimg + ':')
                whatsize = input()
                if from_mconf:
                    getconf('img_size_' + whatimg, mconf, add=whatsize)
                else:
                    getconf('img_size_' + whatimg, uconf, add=whatsize)

            if not whatsize or not whatsize.isnumeric():
                banner()
                kprint(lang['error'], 'yrbbo')
                kprint(whatimg + lang['extract_detect_fail'] + '\n', 'r')
                input(lang['enter_build_menu'])
                return
            else:
                imgsize = whatsize
        elif choice == '4':  # START $whatimg.img
            imgsize = findwhatsize(whatimg)
        elif choice == 'q':  # START Quit
            if existd(rd + '/META-INF1'):
                with cd(rd):
                    delpath('META-INF')
                    os.replace('META-INF1', 'META-INF')

            sys.exit()

    getconf('size-' + whatimg, uconf, add=imgsize)

    return imgsize


def findwhatsize(whatimg, quiet=None):
    imgsize = None
    if existf(rd + '/' + whatimg + '.img'):
        with cd(rd):
            if sparse_chk(whatimg + '.img'):
                sparse_conv(whatimg + '.img')

            imgsize = fsize(whatimg + '.img')

            if whatimg == 'system':
                if existf('system_other.img'):
                    if sparse_chk('system_other.img'):
                        sparse_conv('system_other.img')

                    othersize = fsize('system_other.img')
                    if othersize > imgsize:
                        imgsize = othersize

            imgsize = str(imgsize)
    elif whatimg == 'data' and existf(rd + '/user' + whatimg + '.img'):
        with cd(rd):
            if sparse_chk('user' + whatimg + '.img'):
                sparse_conv('user' + whatimg + '.img')

            imgsize = str(fsize('user' + whatimg + '.img'))
    else:
        if not quiet:
            banner()
            kprint(lang['error'], 'yrbbo')
            kprint(lang['extract_img_fail'] + whatimg + '.img\n', 'r')
            input(lang['enter_build_menu'])

    return imgsize


def fsize(filename):
    return os.stat(filename).st_size


def findfiles(whatfile, where='.', infile=None):
    import fnmatch

    name = []
    try:
        rule = re.compile(fnmatch.translate(whatfile), re.IGNORECASE)
    except:
        return name

    if infile:
        filelist = []
        for i in readfl(infile):
            if i.startswith(where):
                filelist.append(basename(i.split()[0]))

        for i in filelist:
            if rule.match(i):
                name.append(i)
    else:
        for i in os.listdir(where):
            if rule.match(i):
                name.append(i)

    return name


def findr(longpath):
    return glob.glob(longpath, recursive=True)


def findw(indir):
    file_list = []

    for root, dirs, files in os.walk(indir, topdown=False):
        for name in files:
            file_list.append('/'.join([root, name]))
        for name in dirs:
            file_list.append('/'.join([root, name]))

    return sorted(file_list)


def fl(st, wo=None, nar1=None, nar2=None):
    if wo and nar1 and nar2:
        return '(?!' + wo + ')(?=^.*' + st + '.*$)(?=^.*' + nar1 + '.*$|^.*' + nar2 + '.*$)'
    elif nar1 and nar2 and not wo:
        return f'(?=^.*{st}.*$)(?=^.*{nar1}.*$|^.*{nar2}.*$)'
    elif nar1 and not nar2 and not wo:
        return '(?=^.*' + st + '.*$)(?=^.*' + nar1 + '.*$)'
    elif wo and not nar1 and not nar2:
        return f'(?!{wo})(?=^.*' + st + '.*$)'
    elif not nar1 and not nar2 and not wo:
        return f'(?=^.*{st}.*$)'


def gen_min_contexts(whatimg):
    appendf('/(.*)?\t\tu:object_r:rootfs:s0', prfiles + '/file_contexts_min')
    appendf('/lost\\+found\t\tu:object_r:rootfs:s0',
            prfiles + '/file_contexts_min')

    try:
        if existf(prfiles + '/file_contexts3-' + whatimg):
            testcon = grepf('^/' + whatimg + ' ', prfiles
                            + '/file_contexts3-' + whatimg)[0].split()[-1]
        else:
            testcon = grepf('^/' + whatimg + '\(.*\t', prfiles
                            + '/file_contexts')[0].split('\t\t')[1]

        appendf('/' + whatimg + '(/.*)?\t\t' + testcon, prfiles + '/file_contexts_min')
    except:
        appendf('/' + whatimg + '(/.*)?\t\tu:object_r:' + whatimg
                + '_file:s0', prfiles + '/file_contexts_min')

    appendf('/' + whatimg + '/lost\\+found\t\tu:object_r:'
            + whatimg + '_file:s0', prfiles + '/file_contexts_min')

    appendf('/' + whatimg + '/omc(/.*)?\t\tu:object_r:omc_vendor_file:s0',
            prfiles + '/file_contexts_min')


def getar(prop):
    proppath = prfiles + '/AR-config'
    if existf(proppath):
        proptest = grepf(fl(prop, '^#'), proppath)
        if proptest:
            return proptest[0].strip().split('"')[1]
        else:
            return proptest


def getcap(i):
    try:
        b = os.getxattr(i, "security.capability")
        cap = str(int.from_bytes(b[4:8] + b[12:16], "little"))
        return 'capabilities=' + cap
    except:
        return ''


def getChar():
    import tty
    import termios

    def _ttyRead():
        fd = sys.stdin.fileno()
        oldSettings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            choice = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)
        return choice

    return _ttyRead().lower()


def getconf(conf, version, rem=None, add=None, repl=None, l=None):
    if repl:
        full = readfl(version)
        conf_tmp = grepv('^#', greps(conf, full))[0]
        if conf_tmp:
            conf_index = full.index(conf_tmp)

            if rem:
                del full[conf_index]
            else:
                full[conf_index] = conf + '=' + add

            delpath(version)
            appendf('\n'.join(full), version)
    elif rem or add:
        grepvf('^' + conf + '=', version)
        if add:
            if l:
                full = sorted(readfl(version) + [conf + '=' + ' '.join(add)])
            else:
                full = sorted(readfl(version) + [conf + '=' + add])
            delpath(version)
            appendf('\n'.join(full), version)
        return
    else:
        if l:
            i = grepf('^' + conf + '=', version)
            if i:
                i = i[0].strip()
            else:
                return []

            if not i.endswith('='):
                i = i.split('=', 1)[1].strip()
                if ' ' in i:
                    i = i.split()
                else:
                    i = [i]
                return i
            else:
                return []
        else:
            try:
                return grepf(f'^{conf}=', version)[0].split('=', 1)[1]
            except:
                return ''


def get_contexts():
    if not existf(prfiles + '/file_contexts2'):
        def strings(filename, minim=4):
            import string
            with open(filename, errors='ignore') as f:
                result = ''
                for c in f.read():
                    if c in string.printable:
                        result += c
                        continue
                    if len(result) >= minim:
                        yield result
                    result = ''
                if len(result) >= minim:
                    yield result

        def cpcon(condir):
            for f in condir:
                if existf(f + c):
                    copyfile(f + c, prfiles + c)
                    break
                if existf(f + b):
                    copyfile(f + b, prfiles + b)
                    break
                if existf(f + p):
                    appendf(readf(f + p), prfiles + c)
                if existf(f + n):
                    appendf(readf(f + n), prfiles + c)
                if existf(f + v):
                    appendf(readf(f + v), prfiles + c)

            if existf(prfiles + b):
                return 'bin'
            elif existf(prfiles + c):
                return 'none'
            else:
                return

        c = '/file_contexts'
        b = '/file_contexts.bin'
        p = '/plat_file_contexts'
        n = '/nonplat_file_contexts'
        v = '/vendor_file_contexts'

        if existf(prfiles + b):
            method = 'bin'
        elif existf(prfiles + c):
            method = 'none'
        else:
            method = cpcon([rd + '/system', rd + '/system/system', rd + '/bootimg/ramdisk', rd + '/recoveryimg/ramdisk',
                            rd + '/system/etc/selinux', rd + '/system/system/etc/selinux', rd + '/vendor/etc/selinux'])

        if not method and existf(rd + '/boot.img'):
            boot_unpack('boot', 'boot.img', '1')
            method = cpcon([rd + '/bootimg/ramdisk'])

            with cd(bd):
                appendf(cmd(rampy() + 'delram ' + romname + ' boot'), logs + '/boot.log')

        if method == 'bin':
            conlist = list(strings(prfiles + b))
            delpath(prfiles + b)
            if len(conlist) == 1:
                if conlist[0].startswith('/'):
                    appendf(conlist[0], prfiles + c)
            else:
                copyfile(tools + '/boot' + c, prfiles + c)
                conlist = greps(fl('u:|\/', 'ER'), conlist)
                conlist = greps(fl('', '.*abcd'), conlist)
                contest = []
                for i, line in enumerate(conlist):
                    if re.search('u:', line):
                        contest.append(i)

                for line in contest:
                    if conlist[line + 1].startswith('/'):
                        appendf(conlist[line + 1] + '\t' + conlist[line], prfiles + c)

        if existf(prfiles + c):
            contest = grepf(fl('^\/system|^\/vendor|^\/oem|^\/product|^\/system_ext',
                               '.*:system_file|.*:system_library_file'), prfiles + c)

            with cd(rd):
                flist = findr('system/**') + findr('vendor/**') + \
                        findr('oem/**') + findr('product/**') + findr('system_ext/**')

            for i in contest:
                i = i.replace('--', '').replace('/', '', 1)
                cexc = i.split()[1]
                for cexf in greps(i.split()[0], flist):
                    appendf('/' + cexf + ' ' + cexc, prfiles + c + '2')


def get_devicename():
    devicename = ''
    if getconf('devicename', uconf):
        devicename = getconf('devicename', uconf)
    else:
        devtmp = ['ro.product.device', 'ro.build.product', 'ro.product.name',
                  'ro.product.system.device', 'ro.product.system.name']
        devicechk = ''
        for i in devtmp:
            devicename = getprop(i)
            if devicename:
                devicechk = i
                break

        if not devicename:
            try:
                devicechk = 'ro.product.device'
                devicename = getprop('ro.build.description').split('-')[0]
            except:
                pass

        if devicename:
            getconf('devicename', uconf, add=devicename)
            getconf('devicechk', uconf, add=devicechk)

    if devicename:
        mkdir(tools + '/devices/' + devicename)

    return devicename


def get_heapsize():
    if getconf('heapsize', mconf):
        return getconf('heapsize', mconf)
    else:
        return str(virtual_memory() - 500)


def getlang(lfile, tools1=None):
    if not tools1:
        tools1 = tools

    with cd(tools1 + '/language'):
        coding = grepf(' coding: ', lfile)
        if coding:
            coding = coding[0].split()[3]
        else:
            coding = utftest(lfile)

        lang1 = {}
        with open(lfile, 'r', encoding=coding) as f:
            for i in f.read().splitlines():
                if ' = ' in i:
                    a, b = i.split(' = ', 1)
                    lang1[a] = b[1:-1]
    return lang1


def getperm(arg):
    if len(arg) < 9 or len(arg) > 10:
        return

    if len(arg) > 8:
        arg = arg[1:]

    oor, ow, ox, gr, gw, gx, wr, ww, wx = list(arg)
    o, g, w, s = 0, 0, 0, 0

    if oor == 'r':
        o += 4
    if ow == 'w':
        o += 2
    if ox == 'x':
        o += 1
    if ox == 'S':
        s += 4
    if ox == 's':
        s += 4
        o += 1
    if gr == 'r':
        g += 4
    if gw == 'w':
        g += 2
    if gx == 'x':
        g += 1
    if gx == 'S':
        s += 2
    if gx == 's':
        s += 2
        g += 1
    if wr == 'r':
        w += 4
    if ww == 'w':
        w += 2
    if wx == 'x':
        w += 1
    if wx == 'T':
        s += 1
    if wx == 't':
        s += 1
        w += 1

    return str(s) + str(o) + str(g) + str(w)


def getprop(prop):
    proptmp = [rd + '/system/system/build.prop',
               rd + '/system/build.prop',
               rd + '/build.prop']
    proppath = []
    for i in proptmp:
        if existf(i):
            proppath = i
            break
    try:
        return grepf(fl(prop, '^#'), proppath)[0].split('=')[1]
    except:
        return ''


def grepb(a, b, flist, loc=None):
    greptmp = []
    go = 0
    for line in flist:
        if go == 1:
            if loc:
                if line.endswith(b):
                    greptmp.append(line)
                    return greptmp
            else:
                if line.startswith(b):
                    return greptmp
            greptmp.append(line)
            continue
        if loc:
            if line.startswith(a):
                greptmp.append(line)
                go = 1
        else:
            if line.startswith(a):
                go = 1
    return greptmp


def grepc(searcht, gstr):
    searcht = searcht.replace('+', '\+')
    for line in gstr:
        otest = re.search(searcht, line, re.IGNORECASE)
        if otest:
            return otest.group()
    return None


def grepvb(rlist, filename):
    tmpf = readfl(filename)
    with open(filename + '-tmp', 'w', newline='\n') as f:
        for i in tmpf:
            if i not in rlist:
                f.write(i + '\n')
    os.replace(filename + '-tmp', filename)


def grepf(searcht, filename):
    if existf(filename):
        try:
            gftest = []
            with open(filename, 'r', encoding=utftest(filename)) as f:
                for line in f.read().splitlines():
                    if re.search(searcht, line):
                        gftest.append(line)
            return gftest
        except:
            return []
    else:
        return []


def grepff(searcht, filename, newfile):
    if existf(filename):
        with open(filename, 'r', encoding=utftest(filename)) as f, open(newfile, 'w', newline='\n') as nf:
            data = f.readlines()
            for line in data:
                if re.search(searcht, line):
                    nf.write(line)
                else:
                    continue


def greps(searcht, gstr):
    return [line for line in gstr if re.search(searcht.replace('+', '\+'), line)]


def grepv(searcht, thelist):
    return [line for line in thelist if not re.search(searcht, line)]


def grepvf(searcht, filename):
    if existf(filename):
        with open(filename, 'r') as f, open(filename + '-tmp', 'w', newline='\n') as ft:
            data = f.readlines()
            for line in data:
                if re.search(searcht, line):
                    continue
                else:
                    ft.write(line)
        os.replace(filename + '-tmp', filename)


def get_symlinks(quiet=None):
    if not quiet:
        banner()
        kprint(lang['perm_check_symlinks'], 'b')

    if glob.glob(prfiles + '/symlinks*'):
        return

    symlinks = {}

    with cd(rd):
        for i in [x for x in partslist if existd(x) and not existf(prfiles + '/symlinks-' + x)]:
            tmplinks = []

            for root, dirs, files in os.walk(i):
                for filename in files:
                    source = os.path.join(root, filename)
                    if os.path.islink(source):
                        tmplinks.append(
                            'symlink("' + os.readlink(source) + '", "/' + source + '");')
                        delpath(rd + '/' + source)

                for directory in dirs:
                    source = os.path.join(root, directory)
                    if os.path.islink(source):
                        tmplinks.append(
                            'symlink("' + os.readlink(source) + '", "/' + source + '");')
                        delpath(rd + '/' + source)

            if tmplinks:
                symlinks[i] = tmplinks

    if symlinks:
        for part in symlinks:
            for i in sorted(symlinks[part], key=str.lower):
                appendf(i, prfiles + '/symlinks-' + part)

        return
    else:
        if not existf(usdir + '/updater-script'):
            return

        symlinks = grepf('symlink\(.*', usdir + '/updater-script')
        if not symlinks:
            return

        symlinks2 = greps(',$', symlinks)
        symlinks = greps(';$', symlinks)
        if symlinks2:
            for i in symlinks2:
                mulsym = grepb(i, ';', readfl(usdir + '/updater-script'), 1)
                top = mulsym[0]
                top2 = top.replace(',', '').split()[1:]
                bottom = mulsym[len(mulsym) - 1]
                symlist = bottom.replace(',', '').replace(');', '').split()
                symlist = top2 + symlist
                mulname = '"' + top.split('"')[1] + '"'
                del mulsym[0]
                del mulsym[len(mulsym) - 1]
                for a in mulsym:
                    symtmp = a.replace(',', '').split()
                    symlist = symlist + symtmp

                for a in symlist:
                    if a.startswith('"'):
                        symlinks.append('symlink(' + mulname + ', ' + a + ');')

        if symlinks:
            for i in sorted(symlinks, key=str.lower):
                appendf(i, prfiles + '/symlinks')


def imgextract(extractimg, quiet=None, cli=None):
    extractdir = extractimg.replace('.img', '')

    with cd(rd):
        if sparse_chk(extractimg):
            sparse_conv(extractimg, cli=cli)

        if not cli:
            banner(quiet)
        kprint(lang['extract_copy_e'] + extractdir + ' ...', 'b')

        return ext4Xtract(extractdir)


def imgrename(new=None):
    imgext = getconf('img_extension', uconf)

    imgdict = {}

    if new:
        for i in partslist + ['cache', 'data', 'userdata']:
            imgdict[i + '_new.img'] = i + '.img'
    else:
        for i in partslist + ['cache', 'data', 'userdata', 'boot']:
            imgdict[i + '.img.ext4'] = i + '.img'
            imgdict[i + '.ext4'] = i + '.img'
            imgdict[i.upper() + '.IMG'] = i + '.img'
            imgdict[i + '.IMG'] = i + '.img'
            imgdict[i.upper() + '.img'] = i + '.img'
            # imgdict[i+'_new.img'] = i+'.img'

        imgdict['factoryfs.img'] = 'system.img'

    with cd(rd):
        for i in list(imgdict):
            if existf(i):
                if not new and not imgext:
                    imgext = '.' + '.'.join(i.split('.')[1:])
                    getconf('img_extension', uconf, add=imgext)

                if existf(imgdict[i]):
                    os.replace(i, imgdict[i].replace('.img', '_new.img'))
                else:
                    os.replace(i, imgdict[i])


def internet(url='https://bing.com', op=None):
    try:
        result = requests.get(
            url, headers={'User-Agent': 'srk_' + (superrv or '3220')}).text.strip()
    except:
        result = None

    if result and not op:
        result = 1

    return result


def isascii(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def isodexstatus():
    # deotmp = findr(sysdir+'/**/*.odex')
    # deotmp += findr(rd+'/vendor/**/*.odex')
    # deotmp += findr(rd+'/oem/**/*.odex')
    # deotmp += findr(rd+'/product/**/*.odex')
    # deotmp += findr(rd+'/system_ext/**/*.odex')
    deotmp = grepv('.*00_project_files', findr(rd + '/**/*.odex'))
    deotmp += glob.glob(sysdir + '/*.sqsh')
    deotmp += findr(sysdir + '/framework/**/boot*.oat')

    if not deotmp:
        return color['g'] + 'Deodexed' + color['n']
    else:
        return color['r'] + 'Odexed' + color['n']


def kitchen_update(jupdate=None, averify=None):
    upchk = ''
    if not internet():
        banner()
        kprint(lang['error'], 'yrbbo')
        kprint(lang['update_no_internet'] + '\n', 'r')
        if jupdate:
            input(lang['enter_exit'])
            sys.exit()
        else:
            input(lang['enter_main_menu'])
    else:
        localzip = sorted(
            glob.glob('update_' + (platf if platf not in ['wsl', 'wsl2'] else 'lin') + '*.zip'))
        if localzip:
            localzip = localzip[-1]
            ziplist = zipl(localzip)
            if any(['tools/source/mainsrk' in ziplist, 'tools/source/srktools' in ziplist]):
                banner()
                print(lang['update_local'] + '\n')
                reply = getChar()
                if reply == 'y':
                    delpath(tools + '/auth.key')

                    if averify:
                        srkuser, srkpass, dbtst = averify
                    else:
                        srkuser, srkpass, dbtst, days_left, latest_ver = user_auth(
                            jupdate)

                    banner()
                    kprint(lang['cust_prep'], 'b')

                    zipu(localzip)

                    if existf(tools + '/source/md5_full'):
                        source_files = ['tools/source/md5_full']
                        for i in greps('tools/source', readfl(tools + '/source/md5_full')):
                            source_files.append(i.split('\t')[0])

                        for i in findr('tools/source/**'):
                            if i and not existd(i) and i not in source_files:
                                delpath(i)
                                if not glob.glob(dirname(i) + '/*'):
                                    delpath(dirname(i))

                    internet(server1 + '/errlog2/?e=' + mfunc2('auth = '
                                                               + str(['LOCAL UPDATE:', srkuser, 'Zip:' + localzip]),
                                                               'out').decode())

                    banner()
                    kprint(lang['success'] + '\n', 'g')
                    input(lang['enter_continue'])
                    sys.exit(3)

        banner()
        kprint(lang['update_check_kitchen'], 'b')
        changelog = internet(server1 + '/changelog/?v=donate&c=c', 1)

        if not changelog:
            banner()
            kprint(lang['error'], 'yrbbo')
            kprint(lang['update_down'], 'r')
            kprint(lang['update_down2'] + '\n', 'r')
            if jupdate:
                input(lang['enter_exit'])
                sys.exit()
            else:
                input(lang['enter_main_menu'])
                return

        newv = changelog[:8]
        upcheck = newv[1::2]
        currentv = superrv[1::2]

        choice = ''
        while not choice:
            if getconf('updatecheck', mconf):
                ucheck = getconf('updatecheck', mconf)
            else:
                ucheck = color['r'] + 'N/A'

            if jupdate:
                choice = '1'
                allowupdate = 1
            else:
                banner()

                allowupdate = None
                if int(currentv) < int(upcheck):
                    allowupdate = 1
                    kprint(lang['update_update_avail'] + '\n', 'gbo')
                    kprint(lang['update_update_cv'] + color['r'] + superrv, 'b')
                    kprint(lang['update_update_nv'] + color['g'] + newv + '\n', 'b')
                    print('1) ' + lang['update_update_now'])
                    print('2) ' + lang['update_update_view'])
                    print('3) ' + lang['update_auto_toggle'] + ' (' + color['b']
                          + lang['title_current'] + color['g'] + ucheck + color['n'] + ')')
                else:
                    kprint(lang['update_already'] + '\n', 'gbo')
                    kprint('1) ' + lang['update_update_now'], 'r')
                    print('2) ' + lang['update_update_view'])
                    print('3) ' + lang['update_auto_toggle'] + ' (' + color['b']
                          + lang['title_current'] + color['g'] + ucheck + color['n'] + ')')

                kprint('m = ' + lang['title_main'], 'y')
                kprint('q = ' + lang['menu_quit'] + '\n', 'm')
                print(lang['select'])
                choice = getChar()

            if choice.isnumeric():
                if allowupdate:
                    if choice < '1' or choice > '3':
                        choice = ''
                        continue
                else:
                    if choice not in ['2', '3']:
                        choice = ''
                        continue
            elif choice not in ['m', 'q']:
                choice = ''
                continue

            if choice == 'm':
                return
            elif choice == 'q':
                sys.exit()
            elif choice == '2':  # START View changelog
                banner()
                kprint(lang['update_changelog'] + '\n', 'gb')
                kprint(changelog.replace('. ', '\n') + '\n', 'y')
                input(lang['enter_kitchen_updater'])
                choice = ''
                continue
            elif choice == '3':  # START Toggle update check
                if ucheck == 'yes':
                    getconf('updatecheck', mconf, add='no')
                else:
                    getconf('updatecheck', mconf, add='yes')
                choice = ''
                continue
            elif choice == '1':  # START Update now
                delpath(tools + '/auth.key')

                if averify:
                    srkuser, srkpass, dbtst = averify
                else:
                    srkuser, srkpass, dbtst, days_left, latest_ver = user_auth(
                        1)

                banner()
                kprint(lang['update_updating'], 'b')

                updatef = None
                if int(upcheck) == int(currentv) + 1:
                    updatef = 1

                download = platf
                if download != 'mac':
                    download = 'lin'
                    if not updatef:
                        download = 'linux64'
                elif download == 'mac':
                    if not updatef:
                        download = 'mac64'
                else:
                    banner()
                    kprint('Unknown platform', 'r')
                    sys.exit()

                dlfile(server1 + '/dl/?u=' + srkuser + '&p='
                       + srkpass + '&d=' + download, 'dist.zip')

                zipu('dist.zip')
                delpath('dist.zip')

                source_files = ['tools/source/md5_full']
                for i in greps('tools/source', readfl(tools + '/source/md5_full')):
                    source_files.append(i.split('\t')[0])

                for i in findr('tools/source/**'):
                    if i and not existd(i) and i not in source_files:
                        delpath(i)
                        if not glob.glob(dirname(i) + '/*'):
                            delpath(dirname(i))

                getconf('firstrun', mconf, add='1')
                with cd(tools):
                    langt = getconf('language', mconf)
                    if langt != 'english':
                        language_check(langt)

                    for i in grepf(fl('', '#'), 'depends/deldeps'):
                        for d in glob.glob(i):
                            delpath(d)

                upchk = 1

        if platf == 'lin' and not jupdate:
            home = os.path.expanduser('~')
            if existf(home + '/bin/srkil'):
                banner()
                kprint(lang['update_check_launcher'], 'b')

                with cd(home + '/bin'):
                    ilcv = cmd('./srkil -v').strip()
                    ilnv = internet(server1 + '/next/srkil/', 1).strip()

                if ilcv != ilnv:
                    with cd(bd):
                        dlfile(server1 + '/next/srkil/srkil', 'srkil')
                        cmd(
                            'chmod +x srkil; ./srkil -u; ./srkil -i; rm -f srkil')

        if not jupdate and not getconf('updatecheck', mconf):
            banner()
            print(lang['update_auto_q'])
            reply = getChar()
            if reply == 'y':
                getconf('updatecheck', mconf, add='yes')
            else:
                getconf('updatecheck', mconf, add='no')

        if upchk:
            banner()
            kprint(lang['update_finished'] + '\n', 'g')
            input(lang['enter_continue'])
            sys.exit(3)

    return


def kprint(ctext, cl=None):
    print((color[cl] if cl else '') + ctext + color['n'])


def language_check(lang1):
    banner()
    kprint(f'Checking language file {lang1} ...', 'b')
    lang_add = []
    lang_ = []
    for i in readfl(f'{tools}/language/{lang1}_srk.py'):
        lang_.append(i.split("=")[0].strip())
    for i in readfl(f'{tools}/language/english_srk.py'):
        if not i or i.startswith('#'):
            continue

        line2 = i.split('=')[0].strip()
        if line2 not in lang_:
            lang_add.append(i)

    if lang_add:
        appendf('\n# Needs translation\n' + '\n'.join(lang_add), f'{tools}/language/{lang1}_srk.py')

        return 1
    else:
        return 0


def line_end(infile, outfile):
    with open(infile, 'rb') as f, open(outfile, 'wb') as o:
        for i in f:
            null = o.write(i.replace(b'\x0D\x0A', b'\x0A'))

    os.replace(outfile, infile)


def logtb(ex, ex_traceback=None):
    if ex_traceback is None:
        ex_traceback = ex.__traceback__
    tb_lines = [line.rstrip('\n') for line in
                traceback.format_exception(ex.__class__, ex, ex_traceback)]
    return '\n'.join(tb_lines)


def md5chk(fname=None, md5file=None):
    if md5file:
        failed = []
        with cd(tools):
            md5file = 'depends' + os.sep + md5file
            for i in readfl(md5file):
                f = i.split()[0]
                omd5 = i.split()[1]

                if not os.path.isfile(f):
                    failed.append(f)
                    continue

                with open(f, 'rb') as fn:
                    data = fn.read()
                    nmd5 = hashlib.md5(data).hexdigest()

                    if omd5 != nmd5:
                        failed.append(f)

        if failed:
            return failed

        return 0
    else:
        if fname and os.path.isfile(fname):
            with open(fname, 'rb') as fn:
                data = fn.read()
                nmd5 = hashlib.md5(data).hexdigest()
            return nmd5
        else:
            return 1


def encstr(entry):
    return hashlib.sha256(entry.encode()).hexdigest()


def metasetup(extractdir):
    with cd(rd):
        fs_config = {}
        for i in readfl(prfiles + '/fs_config-' + extractdir):
            i = i.split()
            if 'capabilities=' in i[-1]:
                uid, gid, mode, cap = i[-4], i[-3], i[-2], str(
                    hex(int(i[-1].split('=')[1])))
                name = ' '.join(i[:-4])
            else:
                uid, gid, mode, cap = i[-3], i[-2], i[-1], '0x0'
                name = ' '.join(i[:-3])

            if name.endswith('.srk'):
                name = name[:-8]

            fs_config[name] = [uid, gid, mode, cap]

        for i in readfl(prfiles + '/file_contexts3-' + extractdir):
            i = i.split()
            context = i[-1]
            name = ' '.join(i[:-1])[1:]

            if name.endswith('.srk'):
                name = name[:-8]

            try:
                if fs_config[name]:
                    fs_config[name] += [context]
            except:
                pass

        dirr = ''
        if extractdir == 'system' and sar():
            dirr = 'system/'

        mlist = []
        for i in fs_config:
            if len(fs_config[i]) != 5:
                continue

            if existd(dirr + i) or existf(dirr + i):
                mlist.append('set_metadata("/' + dirr + i
                             + '", "uid", '
                             + fs_config[i][0] + ', "gid", ' + fs_config[i][1]
                             + ', "mode", '
                             + fs_config[i][2] + ', "capabilities", '
                             + fs_config[i][3]
                             + ', "selabel", "' + fs_config[i][4] + '");')

        del fs_config

        return list(filter(None, mlist))


def mfunc2(data, dtype):
    xtr_cc = [76, 107, 115, 95, 105, 71, 66, 99, 54, 107, 49, 83, 103, 86, 112, 76, 99, 69, 90, 78, 102,
              99, 101, 71, 56, 105, 108, 86, 45, 114, 55, 100, 66, 51, 119, 49, 52, 109, 53, 116, 51, 116, 107, 61]

    if dtype == 'in':
        if not data:
            del xtr_cc
            return

        try:
            data = list(data)
            data = Fernet(bytes(xtr_cc)).decrypt(''.join(data[::2]).encode())
        except:
            data = 'auth = ' + \
                   str(['no', datetime.utcnow().strftime(
                       date_pattern), 1, 'dbtst-fake' + ''.join(data)])
            data = data.encode()

        del xtr_cc

        try:
            mod = types.ModuleType('mod')
            exec(data, mod.__dict__)
        except:
            mod = None

        del data

        return mod
    elif dtype == 'out':
        import string
        import random

        encrypted = list(Fernet(bytes(xtr_cc)).encrypt(data.encode()).decode())

        del xtr_cc

        data = list(''.join(random.choice(string.ascii_letters)
                            for x in range(len(encrypted))))

        result = [None] * (len(encrypted) + len(data))
        result[::2] = encrypted
        result[1::2] = data

        del data

        return ''.join(result).encode()


def mkdir(dirpath):
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath, exist_ok=True)


def mvdir(src_dir, dst_dir):
    if not os.path.isdir(dst_dir):
        os.rename(src_dir, dst_dir)


def osbit():
    return str(struct.calcsize('P') * 8)


def partimg(whatimg, sparseimg='', fromplug=None, frommenu=None, quiet=None):
    def imgfailmsg(message=None):
        if not quiet:
            banner()
        kprint(lang['error'], 'yrbbo')

        if message:
            kprint(message, 'r')
        else:
            kprint(lang['img_fail'], 'r')

        if not quiet:
            print()
            if fromplug:
                input(lang['enter_plug_menu'])
            elif frommenu:
                input(lang['enter_build_menu'])
            else:
                input(lang['enter_rom_tools'])

    imgsize = getconf('size-' + whatimg, uconf)
    dirsize = dsize(rd + '/' + whatimg)

    if not imgsize:
        size_mess = whatimg + ': ' + lang['img_fail_size']

        appendf(size_mess, logs + '/img_build.log')
        imgfailmsg(size_mess)

        return 1
    elif int(imgsize) < dirsize:
        size_mess = whatimg + '.img ' + lang['img_fail_fit'] + '\nimg size: ' + str(round(
            int(imgsize) / 1024 / 1024)) + 'MB, dir size: ' + str(round(dirsize / 1024 / 1024)) + 'MB'

        appendf(size_mess, logs + '/img_build.log')
        imgfailmsg(size_mess)

        return 1

    with cd(rd):
        dellink = symlinks_create(whatimg, quiet)

        banner()
        fcontexts = ''

        if existf(prfiles + '/file_contexts3-' + whatimg):
            check_ci(whatimg, old=1)

            delpath(prfiles + '/file_contexts_min')

            if existf(prfiles + '/file_contexts_custom'):
                copyfile(prfiles + '/file_contexts_custom', prfiles + '/file_contexts_min')
            else:
                gen_min_contexts(whatimg)

            fcontexts = ' -S ' + prfiles + '/file_contexts_min'
        else:
            get_contexts()

        if not fcontexts and existf(prfiles + '/file_contexts'):
            fcontexts = ' -S ' + prfiles + '/file_contexts'

        api = getprop('ro.build.version.sdk')

        if not fcontexts and api > '20':
            if not quiet:
                banner()
            kprint(lang['build_img_nocon'], 'r')
            kprint(lang['build_img_nocon2'], 'r')
            kprint(lang['build_img_nocon3'], 'r')
            kprint(lang['build_img_nocon4'] + '\n', 'r')
            if not quiet:
                input(lang['enter_continue'])
            return 1

        kprint(lang['img_create_raw'] + whatimg + '.img (make_ext4fs)', 'b')
        kprint(whatimg + ': ' + imgsize + ' bytes ('
               + str(round(int(imgsize) / 1024 / 1024)) + ' MB) ...', 'y')

        devicename = get_devicename()
        deviceloc = tools + os.sep + 'devices' + os.sep + devicename

        addlf = None
        if existd('system/lost+found'):
            delpath('system/lost+found')
            addlf = 1

        xtra = ''
        if existf(prfiles + '/fs_config-' + whatimg):
            xtra = ' -X ' + prfiles + '/fs_config-' + whatimg
        elif existf(prfiles + '/fs_config'):
            xtra = ' -X ' + prfiles + '/fs_config'
        elif existf(deviceloc + '/capfiles-' + api):
            xtra = ' -X ' + deviceloc + '/capfiles-' + api

        if whatimg == 'system' and sar():
            build_args = ' -T 1' + fcontexts + ' -l ' + imgsize + ' -L ' + whatimg + ' -a /' + \
                         sparseimg + xtra + ' -K vUA6spGTE7EuEd4H ' + whatimg + '_new.img ' + whatimg + '/'
        else:
            build_args = ' -T 1' + fcontexts + ' -l ' + imgsize + ' -L ' + whatimg + ' -a ' + whatimg + \
                         sparseimg + xtra + ' -K vUA6spGTE7EuEd4H ' + whatimg + '_new.img ' + whatimg + '/'

        appendf('\n[INFO] Building ' + whatimg + '_new.img', logs + '/img_build.log')

        tmpbuild = cmd(make_ext4fs + build_args)

        if 'ext4_allocate_best_fit_partial:' in tmpbuild.split():
            appendf('[INFO] Out of space in ext4 ' + whatimg
                    + '_new.img file. Trying again as ext2.', logs + '/img_build.log')

            build_args = ' -J' + build_args
            tmpbuild = cmd(make_ext4fs + build_args)

            if 'ext4_allocate_best_fit_partial:' in tmpbuild.split():
                tmpbuild = tmpbuild + '\n[ERROR] Out of space in ext2 ' + whatimg + '_new.img file.\n[SUGGESTIONS]\n[OPTION 1] Remove some unneeded files from the ' + \
                           whatimg + \
                           ' directory.\n[OPTION 2] Choose manual partition size and increase as needed.\n'

        appendf(tmpbuild, logs + '/img_build.log')
        delpath(prfiles + '/file_contexts_min')
        delpath(*dellink)
        getconf('size-' + whatimg, uconf, 'rem')

        if not existf(whatimg + '_new.img'):
            imgfailmsg(whatimg + '.img: ' + lang['img_fail_log'])
            return 1

        if addlf:
            mkdir('system/lost+found')


def partimg2(whatimg, sparseimg=None, fromplug=None, frommenu=None, quiet=None):
    def imgfailmsg(message=None):
        if not quiet:
            banner()

        kprint(lang['error'], 'yrbbo')

        if message:
            kprint(message, 'r')
        else:
            kprint(lang['img_fail'], 'r')

        if not quiet:
            print()
            if fromplug:
                input(lang['enter_plug_menu'])
            elif frommenu:
                input(lang['enter_build_menu'])
            else:
                input(lang['enter_rom_tools'])

    imgsize = getconf('size-' + whatimg, uconf)

    if not imgsize:
        size_mess = whatimg + ': ' + lang['img_fail_size']

        appendf(size_mess, logs + '/img_build.log')
        imgfailmsg(size_mess)

        return 1

    with cd(rd):
        dellink = symlinks_create(whatimg, quiet)

        if not quiet:
            banner()

        complete_features = ['dir_prealloc', 'has_journal', 'imagic_inodes', 'ext_attr', 'dir_index', 'resize_inode',
                             'lazy_bg', 'snapshot_bitmap', 'sparse_super2', 'stable_inodes', 'sparse_super',
                             'large_file', 'huge_file', 'uninit_bg', 'uninit_groups', 'dir_nlink', 'extra_isize',
                             'quota', 'bigalloc', 'metadata_csum',
                             'replica', 'read-only', 'project', 'verity', 'compression', 'filetype', 'needs_recovery',
                             'journal_dev', 'extent', 'extents', 'meta_bg', '64bit', 'mmp', 'flex_bg', 'ea_inode',
                             'dirdata', 'metadata_csum_seed', 'large_dir', 'inline_data', 'encrypt', 'casefold',
                             'fname_encoding', 'exclude_inode']

        base_features = ['sparse_super', 'large_file',
                         'filetype', 'dir_index', 'ext_attr']

        ext4_features = ['has_journal', 'extent', 'huge_file',
                         'dir_nlink', 'extra_isize', 'uninit_bg']

        exclude_features = getconf('ext4_features_exclude', mconf, l=1)
        include_features = getconf('ext4_features_include', mconf, l=1)

        for i in exclude_features:
            if i in base_features:
                base_features.remove(i)

            if i in ext4_features:
                ext4_features.remove(i)

        for i in include_features:
            if i not in base_features:
                base_features.append(i)

        fcontexts = None
        build_args = ['-j', '0']

        if existf(whatimg + '.img'):
            try:
                superblock = ext4_header(whatimg + '.img')
            except:
                superblock = {}
                appendf('[INFO] ext4 features were not found in your existing '
                        + whatimg + '.img. Using defaults.', logs + '/img_build.log')

            if superblock.get('not_ext4'):
                appendf(
                    '[INFO] ' + whatimg + '.img is not a raw ext4 img. Using defaults.', logs + '/img_build.log')

            features = superblock.get('FS features')
            if features:
                if 'has_journal' in features:
                    build_args = []

                sb_conf = getconf('shared_blocks', mconf)
                if sb_conf == 'Yes':
                    build_args = ['-c'] + build_args
                elif sb_conf == 'No':
                    pass
                elif 'shared_blocks' in features:
                    build_args = ['-c'] + build_args

                for i in features.split():
                    if all([i in complete_features, i not in exclude_features, i not in base_features]):
                        base_features.append(i)
            elif 'ext4' in cmd('file ' + whatimg + '.img').split():
                build_args = []

            isize = '256'
            if superblock.get('Inode size'):
                isize = str(superblock.get('Inode size'))

            build_args = ['-I', isize] + build_args

        if whatimg == 'system' and sar():
            build_args += ['-K', 'yPmy6kiDfsWLtMoM', '-P', prfiles, '-X', whatimg, '-L', whatimg, '-C', prfiles
                           + '/fs_config-' + whatimg, whatimg, whatimg + '_new.img', 'ext4', '/', imgsize,
                           prfiles + '/file_contexts_min']
        else:
            build_args += ['-K', 'yPmy6kiDfsWLtMoM', '-P', prfiles, '-X', whatimg, '-L', whatimg, '-C', prfiles
                           + '/fs_config-' + whatimg, whatimg, whatimg + '_new.img', 'ext4', '/' + whatimg, imgsize,
                           prfiles + '/file_contexts_min']

        convert_sparse = None
        if sparseimg:
            if int(imgsize) > ((virtual_memory() - 2048) * 1024 * 1024):
                convert_sparse = 1
            else:
                build_args = ['-s'] + build_args

        if existf(prfiles + '/file_contexts3-' + whatimg):
            check_ci(whatimg, new=1)

            delpath(prfiles + '/file_contexts_min')

            if existf(prfiles + '/file_contexts_custom'):
                copyfile(prfiles + '/file_contexts_custom', prfiles + '/file_contexts_min')
            else:
                gen_min_contexts(whatimg)

            fcontexts = 1
        else:
            get_contexts()

        if not fcontexts:
            loc = build_args.index(prfiles + '/file_contexts_min')

            if existf(prfiles + '/file_contexts.bin'):
                build_args[loc] = prfiles + '/file_contexts.bin'
                fcontexts = 1
            elif existf(prfiles + '/file_contexts'):
                build_args[loc] = prfiles + '/file_contexts'
                fcontexts = 1

        api = getprop('ro.build.version.sdk')

        if not fcontexts and api > '20':
            if not quiet:
                banner()
            kprint(lang['build_img_nocon'], 'r')
            kprint(lang['build_img_nocon2'], 'r')
            kprint(lang['build_img_nocon3'], 'r')
            kprint(lang['build_img_nocon4'] + '\n', 'r')
            if not quiet:
                input(lang['enter_continue'])
            return 1

        kprint(lang['img_create_raw'] + whatimg + '.img (e2fsdroid)', 'b')
        kprint(whatimg + ': ' + imgsize + ' bytes ('
               + str(round(int(imgsize) / 1024 / 1024)) + ' MB) ...', 'y')

        devicename = get_devicename()
        deviceloc = tools + os.sep + 'devices' + os.sep + devicename

        addlf = None
        if existd('system/lost+found'):
            delpath('system/lost+found')
            addlf = 1

        loc = build_args.index(prfiles + '/fs_config-' + whatimg)

        if not existf(prfiles + '/fs_config-' + whatimg):
            if existf(prfiles + '/fs_config'):
                build_args[loc] = prfiles + '/fs_config'
            elif existf(deviceloc + '/capfiles-' + api):
                build_args[loc] = deviceloc + '/capfiles-' + api
            else:
                build_args.remove('-C')
                build_args.remove(prfiles + '/fs_config-' + whatimg)

        tmpbuild = e2fsdroid_run(build_args, base_features, ext4_features)

        if not tmpbuild:
            tmpbuild = '\n[ERROR] Something went wrong while building ' + \
                       whatimg + '_new.img.\n'
        else:
            if greps('Could not allocate', tmpbuild.split('\n')):
                tmpbuild = tmpbuild + '\n[ERROR] Out of space in ' + whatimg + '_new.img file.\n\n[SUGGESTIONS]\n[OPTION 1] Remove some unneeded files from the ' + \
                           whatimg + \
                           ' directory.\n[OPTION 2] Choose manual partition size and increase as needed.\n'
            elif greps('failed to alloc', tmpbuild.split('\n')):
                tmpbuild = tmpbuild + \
                           '\n[ERROR] Out of memory on your PC.\n[SUGGESTION] Add more RAM to your PC.\n'

        appendf(tmpbuild, logs + '/img_build.log')
        delpath(prfiles + '/file_contexts_min')
        delpath(*dellink)
        getconf('size-' + whatimg, uconf, 'rem')

        if not existf(whatimg + '_new.img'):
            delpath(whatimg + '_new.img')
            imgfailmsg(whatimg + '.img: ' + lang['img_fail_log'])
            return 1

        if convert_sparse:
            appendf(
                '[INFO] Converting raw to sparse with img2simg due to low RAM on PC.', logs + '/img_build.log')

            appendf(cmd(img2simg + ' ' + whatimg + '_new.img '
                        + whatimg + '_new.img_2'), logs + '/img_build.log')

            if existf(whatimg + '_new.img_2'):
                os.replace(whatimg + '_new.img_2', whatimg + '_new.img')

        if addlf:
            mkdir('system/lost+found')


def partlz4(chosenimg, keep=None):
    img_ext = '.img'
    lz4_ext = '.img.lz4'

    new_ext = getconf('img_extension', uconf)

    if new_ext and new_ext != '.img' and new_ext.startswith('.'):
        img_ext = new_ext
        lz4_ext = new_ext + '.lz4'

    work_img = chosenimg + '_new.img'
    imgname = chosenimg + lz4_ext
    comp_img = None

    with cd(rd):
        mkdir('temp_lz4')

        kprint('Packing ' + imgname + ' ...', 'b')

        if existf(work_img):
            os.replace(work_img, 'temp_lz4/' + chosenimg + img_ext)
            comp_img = chosenimg + img_ext
        elif existf(chosenimg + '.img'):
            work_img = chosenimg + '.img'
            os.replace(work_img, 'temp_lz4/' + work_img)

        with cd('temp_lz4'):
            os.system(lz4 + ' -qB6 --content-size ' + (comp_img or work_img))

        os.replace('temp_lz4/' + imgname, imgname)

        if keep:
            for i in glob.glob('temp_lz4/*'):
                os.replace(i, work_img)

        delpath('temp_lz4')

        return imgname


def partsdat(whatimg, quiet=None):
    import img2sdat

    if not quiet:
        banner()

    kprint(lang['img_create_dat'] + whatimg + ' ...', 'b')
    api = getprop('ro.build.version.sdk')
    aver = ''
    if api == '21':
        aver = 1
    elif api == '22':
        aver = 2
    elif api == '23':
        aver = 3
    elif api >= '24':
        aver = 4

    with cd(rd):
        work_img = whatimg + '_new.img'
        if not existf(work_img):
            work_img = whatimg + '.img'

        repout(logs + '/img_build.log')
        img2sdat.main(work_img, VERSION=aver, PREFIX=whatimg)
        repout()
        delpath(work_img)

        brcomp = getconf('brotli_comp', mconf)
        if brcomp:
            if int(brcomp) not in list(range(0, 10)):
                brcomp = '0'
                getconf('brotli_comp', mconf, add=brcomp)

            kprint(lang['menu_pack_boot'] + whatimg + '.new.dat.br ...', 'b')
            appendf(cmd(brotli + ' -' + brcomp + 'j ' + whatimg
                        + '.new.dat'), logs + '/img_build.log')

            return whatimg + '.new.dat.br'
        else:
            return whatimg + '.new.dat'


def plat():
    if existd('/mnt/c'):
        if which('wsl.exe'):
            wsltmp = cmd('wsl.exe -l -v')
            wsltmp = wsltmp.replace('\x00', '').split('\n\n')
            if not wsltmp:
                wsltmp = ['/bin/sh:']
        else:
            wsltmp = cmd('uname -r | grep Microsoft')
            if wsltmp:
                return 'wsl'
            else:
                wsltmp = cmd('uname -r | grep microsoft')
                if wsltmp:
                    return 'wsl2'
                else:
                    wsltmp = ['/bin/sh:']

        if not wsltmp[0].startswith('/bin/sh:'):
            count = 0
            good = None
            for i in wsltmp:
                if 'Running' in i:
                    good = True
                    break
                else:
                    count += 1

            if good:
                wsltmp = wsltmp[count].split()[-1]

                if wsltmp == '2':
                    return 'wsl2'
                elif wsltmp == '1':
                    return 'wsl'

        return ''

    platf = platform.platform()

    if platf.startswith('Win'):
        return 'win'
    elif platf.startswith('Darwin'):
        return 'mac'
    elif platf.startswith('Linux'):
        return 'lin'
    else:
        return ''


def plug_update(plugins, getlist=None, quiet=None):
    def get_plug_list():
        pluglist1 = None
        expired_plugs = ['partition_zip', 'lg_rctd_remove',
                         'super_build', 'raw2sparse', 'ext4_build']

        try:
            pluglist1 = sorted(
                internet(server1 + '/dlplug/?u=md5plugs2', 1).splitlines())
        except:
            pass

        if not pluglist1:
            return 1

        plugdict = {}
        for i in pluglist1:
            plugdict[i.split()[0]] = i.split()[1]

        pluglist = []
        for i in plugdict:
            if getlist == '2':
                if i not in plugins and i not in expired_plugs:
                    pluglist.append(i)
            else:
                pluglist.append(i)

        return sorted(pluglist), plugdict

    banner()
    kprint(lang['menu_plugin_get'], 'b')

    pluglist = get_plug_list()

    if pluglist == 1:
        if not quiet:
            banner()
            kprint(lang['error'], 'yrbbo')
            kprint(lang['donate_plugin_server'] + '\n', 'r')
            input(lang['enter_continue'])

        return 1

    if getlist:
        return pluglist[0]

    banner()
    kprint(lang['menu_plugin_updates'] + ' ...', 'b')
    upplugs = []
    for i in plugins:
        if i not in pluglist[0]:
            continue

        if not existf(tools + f'/plugins/{i}/plugmd5'):
            if quiet:
                upplugs.append(i)
            else:
                banner()
                kprint(i + color['n'] + ':\n'
                       + lang['donate_plugin_reinstall_q'], 'y')
                print(lang['donate_plugin_reinstall_q2'] + '\n')
                print(lang['donate_plugin_reinstall_q3'])
                reply = getChar()
                if reply == 'y':
                    upplugs.append(i)

            continue

        if readf(tools + f'/plugins/{i}/plugmd5') != pluglist[1][i]:
            upplugs.append(i)

    if upplugs:
        if not quiet:
            banner()
            kprint(lang['menu_plugin_updates_info'] + '\n', 'gb')
            kprint('\n'.join(upplugs) + '\n', 'y')
            print(lang['update_q'])
            reply = getChar()

            if reply != 'y':
                return

        banner()
        kprint(lang['update_updating'], 'b')

        with cd(tools + '/plugins'):
            for i in upplugs:
                delpath(i)
                dlfile('plugins/' + i + '.zip', i + '.zip', 1)
                internet(server1 + '/dllog/?f=PLUG_' + i + '.zip&u=' + srkuser)
                zipu(i + '.zip')
                appendf(pluglist[1][i], i + '/plugmd5')
                delpath(i + '.zip')


def rampy():
    issudo3 = issudo2 or 'sudo '

    return issudo3 + tools_local + f'startup.py --mainram {bd} '


def readf(filename):
    try:
        with open(filename, encoding=utftest(filename)) as f:
            return f.read().strip()
    except:
        return ''


def readfl(filename):
    try:
        with open(filename, 'r', encoding=utftest(filename)) as f:
            return f.readlines()
    except:
        return []


def repout(filename=None):
    if filename:
        sys.stdout = open(filename, 'w')
    else:
        sys.stdout = sys.__stdout__


def run_end_command():
    run_cmd = getconf('run_end_command', mconf)
    if run_cmd:
        kprint('\nRunning user command:\n', 'y')
        print(run_cmd + '\n')
        kprint('Press ctrl+c to stop it,\nor wait until it finishes.\n', 'y')

        os.system(run_cmd)


def sar():
    if existd(rd):
        with cd(rd):
            if (existd('system/system/app') and
                    (existf('system/init.rc') or
                     existf('system/init.environ.rc'))):
                return True
            else:
                return False


def sed(searcht, newstr, thelist, count=0):
    if isinstance(thelist, str):
        return re.sub(searcht, newstr, thelist, count)
    else:
        return [newstr if re.search(searcht, x) else x for x in thelist]


def sedf(searcht, newstr, filename):
    if existf(filename):
        with open(filename, 'r', encoding=utftest(filename)) as f, open(filename + '-tmp', 'w', newline='\n') as ft:
            for line in f:
                ft.write(re.sub(searcht, newstr, line))
        os.replace(filename + '-tmp', filename)


def sparse_chk(filename):
    with open(filename, 'rb') as f:
        buf = f.read(28)
    magic = hex(struct.unpack("<I4H4I", buf)[0])
    if magic != '0xed26ff3a':
        return None
    else:
        return 1


def sparse_conv(extractimg, quiet=None, cli=None):
    if not quiet:
        if not cli:
            banner()
        kprint(extractimg + ': ' + lang['extract_sparse_convert'], 'b')

    simgtmp = cmd(simg2img + ' ' + extractimg + ' ' + extractimg + '-2')
    appendf(simgtmp, logs + '/main.log')
    if existf(extractimg + '-2'):
        os.replace(extractimg + '-2', extractimg)
    else:
        delpath(extractimg + '-2')


def sudo_prep(quiet=None):
    if platf in ['lin', 'mac', 'wsl2'] and getconf('mount_extract', mconf) == 'Yes':
        if not quiet:
            banner()
        cmd('echo | sudo tee')


def super_build(fromcli=None, newdat=None, imglz4=None):
    if not fromcli:
        timegt()

    if platf == 'mac':
        if not cmd('which openssl'):
            if not fromcli:
                banner()
            kprint(lang['error'], 'yrbbo')
            kprint(
                'super.img pack requires openssl to be installed.\nPlease install it using Homebrew or similar, then\ntry again.\n',
                'r')
            if not fromcli:
                input(lang['enter_continue'])
            return 1

    if existf(rd + '/super.img'):
        if fromcli:
            print(lang['super_exists_cli'])
            return 1
        else:
            banner()
            print(lang['super_exists_q'])
            if getChar() == 'y':
                delpath(rd + '/super.img')
            else:
                return 1

    supersize = getconf('supersize', uconf)
    superlist = getconf('superlist', uconf, l=1)
    superab = getconf('superab', uconf)
    metasize = getconf('metadata-size', uconf) or '65536'
    metaslots = getconf('metadata-slots', uconf) or '1'
    group1 = getconf('metadata-group', uconf) or 'main'
    group2 = getconf('metadata-group2', uconf) or 'main_b'

    if not supersize:
        if not fromcli:
            banner()
        kprint(lang['no_supersize1'], 'r')
        kprint(lang['no_supersize2'] + '\n', 'y')
        kprint(lang['no_supersize3'], 'y')
        kprint('supersize=9437184000\n', 'y')
        kprint(lang['no_supersize4'] + '\n', 'y')
        if not fromcli:
            input(lang['enter_continue'])
        return 1

    imglist = []
    imgprint = []
    failed = []

    with cd(rd):
        newimglist = (fromcli[:-1] if fromcli else None)
        if not newimglist:
            newimglist = []
            for i in glob.glob('*.img'):
                pname = i[:-4]
                if pname.endswith('_new'):
                    pname = pname[:-4]
                if pname + '.img' in newimglist or pname + '_new.img' in newimglist:
                    continue

                superblock = ext4_header(i)
                if superblock.get('FS magic number') or sparse_chk(i):
                    newimglist.append(i)

            if superlist:
                super_tmp = []
                for i in superlist:
                    pname = i[:-4]
                    if existf(pname + '_new.img'):
                        super_tmp.append(pname + '_new.img')
                    elif existf(i):
                        super_tmp.append(i)

                if super_tmp:
                    banner()
                    print(lang['ready_to_build_q'])
                    kprint('\n'.join(super_tmp), 'y')

                    if getChar() == 'y':
                        newimglist = super_tmp
                    else:
                        superlist = []
        else:
            for i in newimglist:
                if not existf(i):
                    kprint(i + ': ' + lang['files_not_exist'], 'r')
                    return 1

        for i in newimglist:
            imgname = i[:-4]
            if imgname.endswith('_new'):
                imgname = imgname[:-4]

            if fromcli or superlist:
                reply = 'y'
            else:
                banner()
                print(lang['super_include'] + ' '
                      + color['y'] + i + color['n'] + '  y/n')
                reply = getChar()

            if reply == 'y':
                if not fromcli:
                    banner()

                kprint(i + ': ' + lang['super_part_size'], 'b')

                if sparse_chk(i):
                    superblock = ext4_header(i, sparse=1)
                    imgsize = superblock.get('Raw Size')
                else:
                    imgsize = str(fsize(i))

                if imgsize:
                    imgsize = str(imgsize)
                    imgprint.append(i + ': ' + imgsize + ' bytes')

                    if superab == 'Yes':
                        if group1 == 'main':
                            group1 = 'main_a'

                        imglist.append(' --partition ' + imgname + '_a' + ':readonly:'
                                       + imgsize + ':' + group1 + ' --image ' + imgname + '_a' + '=' + i)
                        imglist.append(' --partition '
                                       + imgname + '_b' + ':readonly:0:' + group2)
                    else:
                        imglist.append(' --partition ' + imgname + ':readonly:'
                                       + imgsize + ':' + group1 + ' --image ' + imgname + '=' + i)
                else:
                    failed.append(i)

        if not imgprint:
            if not fromcli:
                banner()
            kprint(lang['super_no_img1'] + '\n', 'r')
            kprint('1. ' + lang['super_no_img3'] + '\n', 'y')
            if not fromcli:
                input(lang['enter_continue'])
            return 1

        if failed:
            if fromcli:
                kprint(lang['img_not_included1'], 'r')
                kprint(lang['img_not_included2'] + '\n', 'r')
                kprint('\n'.join(failed) + '\n', 'y')
                return 1

            banner()
            kprint(lang['img_not_included1'], 'r')
            kprint(lang['img_not_included2'] + '\n', 'r')
            kprint('\n'.join(failed) + '\n', 'y')
            print(lang['general_cont_anyway_q'])

            if getChar() != 'y':
                return 1

        if not fromcli and not superlist:
            banner()
            print(lang['ready_to_build_q'])
            kprint('\n'.join(imgprint), 'y')

            if getChar() != 'y':
                return 1

        if superab == 'Yes':
            build_args = superp + ' -K H4dEuE7ETGps6AUv --sparse -o super.img --metadata-size ' + metasize + ' --metadata-slots ' + \
                         metaslots + ' --device super:' + supersize + ' --group ' + group1 + ':' + \
                         supersize + ' --group ' + group2 + ':' + supersize + ''.join(imglist)
        else:
            build_args = superp + ' -K H4dEuE7ETGps6AUv --sparse -o super.img --metadata-size ' + metasize + \
                         ' --metadata-slots ' + metaslots + ' --device super:' + supersize + \
                         ' --group ' + group1 + ':' + supersize + ''.join(imglist)

        if existf(ostools + '/lpmake'):
            lpmake_add_args = getconf('lpmake_add_args', uconf)
            if lpmake_add_args:
                lpmake_add_args = ' ' + lpmake_add_args

            build_args = build_args.replace(superp + ' -K H4dEuE7ETGps6AUv',
                                            ostools + '/lpmake' + lpmake_add_args)

        if not fromcli:
            if not newdat:
                choice = ''
                while not choice:
                    banner()
                    kprint(lang['super_sparse_q'] + '\n', 'ryb')
                    print('1) raw')
                    print('2) sparse')
                    print('3) super.new.dat'
                          + ('.br' if getconf('brotli_comp', mconf) else ''))
                    print('4) super.img.lz4')
                    kprint('b = ' + lang['menu_back'], 'y')
                    print()
                    print(lang['select'])
                    choice = getChar()

                    if choice.isnumeric():
                        if choice < '1' or choice > '4':
                            continue
                    elif choice not in ['b']:
                        continue

                    if choice == 'b':
                        return

                    if choice == '1':
                        build_args = build_args.replace(' --sparse', '')
                    elif choice == '3':
                        newdat = 1
                    elif choice == '4':
                        imglz4 = 1
        else:
            if fromcli[-1] == 'dat':
                newdat = 1
            elif fromcli[-1] == 'raw':
                build_args = build_args.replace(' --sparse', '')
            elif fromcli[-1] == 'lz4':
                imglz4 = 1

        if not fromcli:
            banner()
        kprint(lang['super_building'], 'b')

        retval = cmd(build_args)

        if existf('super.img'):
            if newdat:
                quiet = None
                if fromcli:
                    quiet = 1

                partsdat('super', quiet=quiet)
            elif imglz4:
                partlz4('super')

            if not fromcli:
                banner()
            kprint(lang['super_success'] + '\n', 'g')

            if fromcli:
                return 0
        else:
            delpath('super.img')
            appendf(retval, logs + '/img_build.log')

            if not fromcli:
                banner()

            kprint(lang['super_failed'] + '\n', 'r')

            if fromcli:
                return 1

        input(lang['enter_continue'])


def super_unpack(romimg, fromcli=None):
    with cd(rd):
        if platf == 'mac':
            if not cmd('which openssl'):
                if not fromcli:
                    banner()
                kprint(lang['error'], 'yrbbo')
                kprint(
                    'super.img unpack requires openssl to be installed.\nPlease install it using Homebrew or similar, then\ntry again.\n',
                    'r')
                if not fromcli:
                    input(lang['enter_main_menu'])
                return 1

        if fromcli and not existf(romimg):
            kprint(lang['super_not_found'], 'r')
            return 1

        if sparse_chk(romimg):
            sparse_conv(romimg, cli=(1 if fromcli else None))
            if not fromcli:
                sudo_prep(quiet=1)

        if not fromcli:
            banner()
        kprint(lang['boot_unpack'] + 'super.img ...', 'b')

        now_img = glob.glob('*.img')

        appendf(cmd(superx + ' -K H4dEuE7ETGps6AUv ' + romimg), logs + '/main.log')

        ab = None
        for i in glob.glob('*_a.img'):
            if fsize(i) > 0:
                os.replace(i, i.replace('_a', ''))
            else:
                delpath(i)

            ab = 1

        for i in glob.glob('*_b.img'):
            if fsize(i) > 0 and not existf(i.replace('_b', '')):
                os.replace(i, i.replace('_b', ''))
            else:
                delpath(i)

            ab = 1

        later_img = []
        for i in glob.glob('*.img'):
            if i not in now_img:
                later_img.append(i)

        if later_img:
            getconf('img_extension', uconf, add='.img')
            getconf('supersize', uconf, add=str(fsize(romimg)))
            getconf('superlist', uconf, add=later_img, l=1)

            metadata = None
            try:
                args = argparse.Namespace(SUPER_IMAGE=rd + '/' + romimg, DUMP=2)
                metadata = lpunpack.LpUnpack(**vars(args)).lpdump()
            except Exception as e:
                pass

            if metadata:
                group1 = None
                group2 = None
                groups = [i.name for i in metadata.groups]

                if 'default' in groups:
                    del groups[groups.index('default')]

                if groups and len(groups) > 1:
                    group1 = groups[0]
                    group2 = groups[1]
                elif groups:
                    group1 = groups[0]

                getconf('metadata-size', uconf,
                        add=str(metadata.geometry.metadata_max_size))
            else:
                getconf('metadata-size', uconf, add='65536')

            if ab:
                getconf('superab', uconf, add='Yes')
                if metadata:
                    getconf('metadata-slots', uconf,
                            add=str(metadata.geometry.metadata_slot_count))
                    getconf('metadata-group', uconf, add=group1 or 'main_a')
                    getconf('metadata-group2', uconf, add=group2 or 'main_b')
                else:
                    getconf('metadata-slots', uconf, add='3')
                    getconf('metadata-group', uconf, add='main_a')
                    getconf('metadata-group2', uconf, add='main_b')
            else:
                getconf('superab', uconf, add='No')
                if metadata:
                    getconf('metadata-slots', uconf,
                            add=str(metadata.geometry.metadata_slot_count))
                    getconf('metadata-group', uconf, add=group1 or 'main')
                    getconf('metadata-group2', uconf, rem='1')
                else:
                    getconf('metadata-slots', uconf, add='2')
                    getconf('metadata-group', uconf, add='main')
                    getconf('metadata-group2', uconf, rem='1')

            if not fromcli:
                delpath(romimg)

            return 0
        else:
            if not fromcli:
                banner()
            kprint(lang['error'], 'yrbbo')
            kprint('super.img: ' + lang['extract_fail'] + '\n', 'r')
            if not fromcli:
                input(lang['enter_main_menu'])
            return 1


def symlinks_create(whatimg, quiet=None):
    if not quiet:
        banner()

    kprint(lang['img_create_symlinks'] + whatimg + '.img ...', 'b')

    if existf(prfiles + '/symlinks-' + whatimg):
        symlinks = readfl(prfiles + '/symlinks-' + whatimg)
    else:
        symlinks = readfl(prfiles + '/symlinks')

    create_dir = getconf('create_missing_symlink_dirs', mconf)

    dellink = []
    for i in symlinks:
        target = i.split('"')[1]
        link = i.split('"')[3].replace('/', '', 1)

        linkdir = dirname(link)
        if not existd(linkdir):
            if create_dir == 'No':
                continue

            mkdir(linkdir)

        dellink.append(link)

        try:
            os.symlink(target, link)
        except:
            pass

    return dellink


def table(it, rows):
    widths = [len(max(it, key=len))] * math.ceil(len(it) / rows)

    ntable = itertools.zip_longest(
        *[it[i:i + rows] for i in range(0, len(it), rows)], fillvalue='')

    for i in ntable:
        print('  '.join((val.ljust(width, ' ')
                         for val, width in zip(i, widths))))


def tarlist(filename):
    listtar = tarfile.TarFile(filename)
    return listtar.getnames()


def taref(tarname, filename):
    tarex = cmd(tar + ' -xf ' + tarname + ' ' + filename)

    return tarex


def tarp(tarname, filelist):
    with tarfile.open(tarname, "w:gz") as tar1:
        for name in filelist:
            tar1.add(name)


def taru(tarname, outdir=None):
    if outdir:
        mkdir(outdir)
        tarex = cmd(tar + ' -xf ' + tarname + ' -C ' + outdir)
    else:
        tarex = cmd(tar + ' -xf ' + tarname)

    return tarex


def timest():
    return datetime.now().strftime('%m-%d-%Y-%H_%M_%S')


def timegt(short=None):
    global last_used
    start_date = datetime.now()

    if short:
        end_date = start_date + timedelta(days=auth_days)
        start_date = start_date.strftime(date_pattern)
        end_date = end_date.strftime(date_pattern)

        return [start_date, end_date]
    else:
        if (last_used + timedelta(hours=4)) < start_date:
            while True:
                banner()
                kprint(lang['session_expired'] + '\n', 'r')
                print('1) ' + lang['session_restart'])
                kprint('q = ' + lang['menu_quit'] + '\n', 'm')
                print(lang['select'])
                reply = getChar()

                if reply not in ['1', 'q']:
                    continue

                if reply == '1':
                    sys.exit(3)
                else:
                    sys.exit()



    last_used = start_date


def touch(filename):
    open(filename, 'a', newline='\n').close()


def ubinary(ubdir):
    banner()
    kprint(lang['cust_convert_binary'], 'b')
    delpath(ubdir + '/update-binary')
    copyfile(tools + '/updater/custom/ubinary', ubdir + '/update-binary')
    uscript = readfl(ubdir + '/updater-script')

    for line in uscript:
        if 'assert' in line:
            if 'ro.product.device' in line:
                testvar = greps('abort', uscript)[0].split('"')[
                    2].replace('\\', '')
                appendf('assert_device "' + testvar + '"', ubdir + '/update-binary')
            else:
                testvar = line.split('"')[1]
                testvar2 = line.split('"')[3]
                appendf('assert_custom "' + testvar + '='
                        + testvar2 + '"', ubdir + '/update-binary')

        elif 'unmount(' in line:
            if 'sysmnt' in line:
                testvar = '$sysmnt'
            else:
                testvar = line.split('"')[1]
            appendf('umount ' + testvar, ubdir + '/update-binary')
        elif 'show_progress' in line:
            testvar = line.split('(')[1].replace(',', '').replace(');', '')
            appendf('show_progress ' + testvar, ubdir + '/update-binary')
        elif 'ui_print' in line:
            if '; u' in line:
                for i in line.split('; '):
                    if i:
                        try:
                            testvar = i.split('"')[1]
                        except:
                            testvar = ''
                        appendf('ui_print "' + testvar + '"',
                                ubdir + '/update-binary')
            else:
                try:
                    testvar = line.split('"')[1]
                except:
                    testvar = ''
                appendf('ui_print "' + testvar + '"', ubdir + '/update-binary')
        elif 'format' in line:
            if 'file_getprop' in line:
                if '"byname"' in line:
                    testvar = line.split('"')[17]
                else:
                    testvar = line.split('"')[11]
            else:
                try:
                    testvar = line.split('"')[7]
                except:
                    testvar = line.split('"')[5]
            appendf('mount ' + testvar, ubdir + '/update-binary')
            appendf('delete_recursive ' + testvar, ubdir + '/update-binary')
        elif 'delete_recursive' in line:
            if 'sysmnt' in line:
                line = line.replace(
                    'file_getprop("/tmp/config", "sysmnt")', '"$sysmnt"')

            testvar = line.split('"')[1]
            appendf('delete_recursive ' + testvar, ubdir + '/update-binary')
        elif 'set_progress' in line:
            testvar = line.split('(')[1].replace(',', '').replace(');', '')
            appendf('set_progress ' + testvar, ubdir + '/update-binary')
        elif line.startswith('mount("'):
            if 'file_getprop' in line:
                if '"byname"' in line:
                    testvar = line.split('"')[15]
                else:
                    testvar = line.split('"')[9]
            else:
                testvar = line.split('"')[7]
            appendf('mount ' + testvar, ubdir + '/update-binary')
        elif line.startswith('ifelse(is_mounted') and 'mount("ext4"' in line:
            if 'sysmnt' in line:
                testvar = '$sysmnt'
            else:
                testvar = line.split('"')[1]
            appendf('mount ' + testvar, ubdir + '/update-binary')
        elif 'package_extract_dir' in line:
            testvar = line.split('"')[1]
            if 'sysmnt' in line:
                testvar2 = '$sysmnt'
            elif 'file_getprop' in line:
                testvar2 = line.split('"')[5]
                testvar2 = '/' + testvar2
            else:
                testvar2 = line.split('"')[3]

            if any(['supersu' in line, 'busybox' in line, 'root' in line]):
                appendf('package_extract_dir ' + testvar
                        + ' /tmp', ubdir + '/update-binary')
            else:
                appendf('package_extract_dir ' + testvar
                        + ' ' + testvar2, ubdir + '/update-binary')
        elif 'run_program' in line:
            if any(['supersu' in line, 'busybox' in line, 'root' in line]):
                testvar = line.replace('", ', ' ').split(
                    '"', 1)[1].replace('"', '').replace(');', '')
            else:
                testvar = line.split('"')[1]
            appendf(testvar, ubdir + '/update-binary')
        elif 'set_metadata' in line:
            if 'sysmnt' in line:
                line = line.replace(
                    'file_getprop("/tmp/config", "sysmnt")+"', '"$sysmnt')

            line = line.replace('(', ' ').replace('"', '').replace(
                ',', '').replace(')', '').replace(';', '').split()
            try:
                if 'set_metadata_recursive' in line:
                    line[11] = str(int(line[11], 16))
                else:
                    line[9] = str(int(line[9], 16))
            except:
                pass
            appendf(' '.join(line), ubdir + '/update-binary')
        elif 'set_perm' in line:
            line = line.replace('(', ' ').replace(
                ',', '').replace('"', '').replace(');', '')
            appendf(line, ubdir + '/update-binary')
        elif 'symlink' in line:
            if 'sysmnt' in line:
                line = line.replace(
                    'file_getprop("/tmp/config", "sysmnt")+"', '"$sysmnt')

            appendf(line.replace('("', ' ').replace(
                '", "', ' ').replace('");', ''), ubdir + '/update-binary')
        elif 'package_extract_file' in line:
            testvar = line.split('"')[1]
            if 'file_getprop' in line:
                if 'byname' in line:
                    if testvar.replace('.img', '') in partslist:
                        testvar2 = '$byname' + line.split('"')[7] + '$slotnum'
                    else:
                        testvar2 = '$byname' + line.split('"')[7]
                else:
                    testvar2 = '$' + line.split('"')[5]
            else:
                testvar2 = line.split('"')[3]

            if testvar.endswith('.img'):
                appendf('package_extract_file ' + testvar
                        + ' /tmp', ubdir + '/update-binary')
                appendf('write_raw_image /tmp/' + testvar
                        + ' ' + testvar2, ubdir + '/update-binary')
            else:
                appendf('package_extract_file ' + testvar
                        + ' ' + testvar2, ubdir + '/update-binary')

    delpath(ubdir + '/updater-script')
    appendf('# Dummy file; update-binary is a shell script.',
            ubdir + '/updater-script')


def user_auth(jupdate=None):
    return [srkuser, srkpass, dbtst, '114514', '3.2.2.2']


def utftest(filename):
    try:
        f = open(filename, 'r', encoding='utf8')
    except UnicodeDecodeError:
        return 'latin1'
    else:
        f.close()
        return 'utf8'


def virtual_memory():
    if existf('/system/build.prop') or existf('/system/system/build.prop'):
        memtst = int(grepf('MemTotal', '/proc/meminfo')[0].split()[1])
        return int(memtst / 1024)
    else:
        if platf in ['lin', 'wsl', 'wsl2']:
            mem_bytes = os.sysconf('SC_PAGE_SIZE') * \
                        os.sysconf('SC_PHYS_PAGES')
        else:
            try:
                mem_bytes = int(cmd('sysctl hw.memsize').split()[1])
            except:
                return 1024

        return int(mem_bytes / 1024 / 1024)


def whoami():
    for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
        user = os.environ.get(name)
        if user:
            return user


def xzu(xzname):
    import lzma
    xz_ref = lzma.open(xzname).read()
    with open(xzname.replace('.xz', ''), 'wb') as f:
        f.write(xz_ref)


def zipl(filename):
    listzip = zipfile.ZipFile(filename)
    return listzip.namelist()


def zipl7(zipname, p7z1=None):
    if not p7z1:
        p7z1 = p7z

    plist = []
    initlist = grepb('----', '----', cmd(p7z1 + ' l "' + zipname + '"').splitlines())

    for i in initlist:
        nline = i.split()
        if len(nline) >= 5 and nline[4].isnumeric():
            plist.append(' '.join(nline[5:]).replace(os.sep, '/'))
        elif len(nline) == 4:
            plist.append(' '.join(nline[3:]).replace(os.sep, '/'))
        else:
            plist.append(' '.join(nline[4:]).replace(os.sep, '/'))

    return plist


def zipef(zipname, filename, outfile=None, p7z1=None):
    if not p7z1:
        p7z1 = p7z

    if outfile:
        return cmd(p7z1 + ' e "' + zipname + '" "' + filename + '" -o"' + outfile + '"')
    else:
        return cmd(p7z1 + ' e "' + zipname + '" "' + filename + '"')


def zipp(zipname, filelist, comp='5', p7z1=None):
    if not p7z1:
        p7z1 = p7z

    return cmd(p7z1 + ' a -tzip -mx' + comp + ' "' + zipname + '" ' + ' '.join(filelist))


def zipu(zipname, outdir=None, p7z1=None):
    if not p7z1:
        p7z1 = p7z

    if outdir:
        return cmd(p7z1 + ' x -y ' + '-o"' + outdir + '" "' + zipname + '"')
    else:
        return cmd(p7z1 + ' x -y "' + zipname + '"')


def zipu2(zipname, outdir=None):
    zip_ref = zipfile.ZipFile(zipname, 'r')
    zip_ref.extractall(outdir)
    zip_ref.close()


platf = plat()

color = {
    'bl': '\033[0m\033[30m',
    'r': '\033[0m\033[31m',
    'rb': '\033[41m',
    'g': '\033[0m\033[32m',
    'gb': '\033[42m',
    'y': '\033[0m\033[33m',
    'yb': '\033[43m',
    'b': '\033[0m\033[34m',
    'bb': '\033[44m',
    'm': '\033[0m\033[35m',
    'mb': '\033[45m',
    'c': '\033[0m\033[36m',
    'cb': '\033[46m',
    'ryb': '\033[0m\033[31m\033[43m',
    'yrbbo': '\033[0m\033[33m\033[41m\033[1m',
    'gbo': '\033[0m\033[32m\033[1m',
    'gbbo': '\033[42m\033[1m',
    'wb': '\033[47m',
    'bo': '\033[1m',
    'it': '\033[3m',
    'un': '\033[4m',
    's': '\033[7m',
    'n': '\033[0m'
}

rd: str = ''
romname = None
prfiles: str = ''
uconf = None
logs: str = ''
usdir: str = ''
lang: dict = {}
issudo2: str = ''
srkuser = None
srkpass = None
dbtst = None
superrv = None
server1: str = ''
sysdir: str = ''
androidversion = None

bd = os.getcwd()
tools = bd + os.sep + 'tools'
tools_local = bd + os.sep
mconf = tools + os.sep + 'srk.conf'
tsize = 60

auth_days = 3
days_left = 'Disabled'
date_pattern = '%m/%d/%Y-%H:%M:%S'

partslist = getconf('partition_extract_list', mconf, l=1)

intro1 = color['s'] + color['bo']
intro2 = color['s'] + color['it']
AIK = tools + '/boot/AIK'

if platf in ['lin', 'wsl', 'wsl2']:
    ostools = tools + '/linux_tools'
    lz4 = AIK + '/bin/linux/x86_64/lz4'
    vdexcon = ostools + '/compact_dex_converter'
elif platf == 'mac':
    ostools = tools + '/mac_tools'
    lz4 = AIK + '/bin/macos/x86_64/lz4'
    vdexcon = ostools + '/bin/compact_dex_converter'
else:
    banner()
    kprint('The platform you are running on is not recognized:', 'r')
    kprint('Current platform: "' + platf + '"\n', 'y')
    input('Press ENTER to exit')
    sys.exit(1)

issudo = 'sudo '
p7z = ostools + '/7z'
superx = ostools + '/superx'
zipalign = ostools + '/zipalign'
tar = 'tar'
adb = ostools + '/adb'
aapt = ostools + '/aapt'
make_ext4fs = ostools + '/make_ext4fs'
mke2fs = ostools + '/mke2fs'
e2fsdroid = ostools + '/e2fsdroid'
tune2fs = ostools + '/tune2fs'
pacextract = ostools + '/pacextractor'
simg2img = ostools + '/simg2img'
img2simg = ostools + '/img2simg'
unsquashfs = ostools + '/unsquashfs'
zipadjust = ostools + '/zipadjust'
vdexext = ostools + '/vdexExtractor'
brotli = ostools + '/brotli'
superp = ostools + '/superp'
last_used = datetime.now()

