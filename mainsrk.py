#!/usr/bin/env python3
#
# SuperR's Kitchen v3.x - By SuperR.
#
import glob
import os
import sys
import importlib
import re
import types
from shutil import which, copyfile
from ipaddress import IPv4Address

import imp
import srktools as j


def superr():
    j.superrv = 'v3.2.2.2'

    j.server1 = 'https://sr-code.com'  # PRODUCTION SERVER
    # j.server1 = 'http://127.0.0.1:5000' # DEVELOPMENT

    color = j.color

    if j.platf not in ['mac', 'lin', 'wsl', 'wsl2']:
        print('Unknown platform')
        sys.exit()

    userid = None
    if os.getuid() == '0':
        userid = 'root'
    elif os.geteuid() == '0':
        userid = 'root'

    if userid:
        print('\nThe kitchen should not be run as root\n')
        sys.exit()

    try:
        import readline
    except:
        pass

    depends = j.tools + '/depends/l'

    def assert_devices(assertch=None):
        global main
        choice = ''
        while not choice:
            if j.getconf('assert-no', j.mconf):
                assertdevices = 'None'
                acuststat = 'None'
            else:
                isassert()
                assertdevices = j.getconf('assertdevices', j.uconf)
                acuststat = j.getconf('acuststat', j.uconf)

                if not acuststat:
                    acuststat = 'None'

            devicename = j.get_devicename()
            devicechk = j.getconf('devicechk', j.uconf)

            if j.existd(j.prfiles + '/boot'):
                assertdir = j.prfiles + '/boot'
            else:
                assertdir = j.prfiles

            if not j.grepf('#ASSERT', j.usdir + '/updater-script'):
                j.awktop('#ASSERT', j.usdir + '/updater-script')

            if not j.grepf('#ASSERT', j.usdir + '/updater-script'):
                j.banner()
                j.kprint(j.lang['error'], 'yrbbo')
                j.kprint(j.lang['asserts_no_assert'] + '\n', 'r')
                input(j.lang['enter_rom_tools'])
                return

            if not assertch:
                j.banner()
                j.kprint(j.lang['startup_project'] + color['g'] + j.romname, 'b')
                j.kprint(j.lang['startup_version']
                         + color['g'] + j.androidversion + '\n', 'b')
                j.kprint(j.lang['menu_asserts'] + '\n', 'ryb')
                print('1) ' + j.lang['menu_add_assert'] + ' (' + color['b']
                      + j.lang['title_current'] + color['g'] + assertdevices + color['n'] + ')')
                print('2) ' + j.lang['menu_asserts_custom'] + ' (' + color['b']
                      + j.lang['title_current'] + color['g'] + acuststat + color['n'] + ')')
                print('3) ' + j.lang['menu_asserts_remove'])
                print('4) ' + j.lang['menu_asserts_reset'])
                j.kprint('5) ' + j.lang['menu_rom_tools'], 'y')
                j.kprint('m = ' + j.lang['title_main'], 'y')
                j.kprint('q = ' + j.lang['menu_quit'] + '\n', 'm')
                print(j.lang['select'])
                choice = j.getChar()

                if choice.isnumeric():
                    if choice < '1' or choice > '5':
                        choice = ''
                        continue
                elif choice not in ['m', 'q']:
                    choice = ''
                    continue

                if choice == 'q':
                    sys.exit()
                elif choice == 'm':  # START Main menu
                    main = 1
                    return
                elif choice == '5':  # START ROM Tools menu
                    return
            else:
                choice = assertch

            j.grepff(j.fl('.*getprop\(', '.*/tmp/.*'), j.usdir
                     + '/updater-script', assertdir + '/assert_original')
            j.grepvf(j.fl('.*getprop\(', '.*/tmp/'), j.usdir + '/updater-script')

            if choice == '1':  # START Add/Remove Device asserts
                j.delpath(assertdir + '/assert')

                j.banner()
                j.kprint(j.lang['asserts_current']
                         + color['g'] + assertdevices + '\n', 'b')
                j.kprint(j.lang['warning'] + '\n', 'yrbbo')
                print(j.lang['asserts_enter'])
                print(j.lang['asserts_enter2'])
                print(j.lang['asserts_enter3'] + '\n')
                print(j.lang['asserts_enter4'])
                print(j.lang['asserts_enter5'])
                print(j.lang['asserts_enter6'] + '\n')
                j.kprint(j.lang['example'] + '\n', 'gb')
                j.kprint('surnia,surnia_cdma,xt1526\n', 'y')
                a = input(devicename)

                if a:
                    a = a.replace(' ', '').replace(
                        ',', '', 1).strip().split(',')
                else:
                    a = []

                j.banner()
                j.kprint(j.lang['asserts_prep'], 'b')

                b = [devicename]
                c = ','.join(b + a)

                if 'boot' not in assertdir:
                    j.getconf('assertdevices', j.uconf, add=c)
                else:
                    j.appendf(c, assertdir + '/assertdevices')

                j.appendf(j.readf(j.tools + '/updater/custom/assert'),
                          assertdir + '/assert')
                j.sedf('#DEVICENAME', devicename, assertdir + '/assert')

                for x in a:
                    if not j.greps('.*\\"' + x + '\\"', assertdir + '/assert'):
                        j.appendf(
                            '    ' + j.readf(j.tools + '/updater/custom/device'), assertdir + '/assert')
                        j.sedf('#DEVICENAME', x, assertdir + '/assert')
                        j.sedf('#DEVICECHK', devicechk, assertdir + '/assert')

                j.appendf('    ' + j.readf(j.tools
                                           + '/updater/custom/abort2'), assertdir + '/assert')
                j.sedf('#DEVICECHK', devicechk, assertdir + '/assert')
                j.sedf('#ASSERTDEVICE', c, assertdir + '/assert')
                j.getconf('assert-no', j.mconf, 'rem')
            elif choice == '2':  # START Add Custom assert
                assertcustom = ''
                propname = ''
                propvalue = ''
                while not assertcustom:
                    j.banner()
                    print(j.lang['asserts_type'] + '\n\n')
                    j.kprint(j.lang['example'] + '\n', 'gb')
                    j.kprint('ro.baseband=1.09.20.1112\n', 'y')
                    assertcustom = input()
                    try:
                        propname = assertcustom.split('=')[0]
                        propvalue = assertcustom.split('=')[1]
                    except:
                        j.banner()
                        j.kprint(j.lang['error'], 'yrbbo')
                        j.kprint(j.lang['asserts_cust_error']
                                 + '"assert.name=assert.value"\n', 'r')
                        input(j.lang['enter_try_again'])
                        assertcustom = ''
                        continue

                j.banner()
                j.kprint(j.lang['asserts_prep_cust'], 'b')
                j.appendf(j.readf(j.tools + '/updater/custom/assertcustom'),
                          assertdir + '/assertcustom')
                j.sedf('#PROPNAME', propname, assertdir + '/assertcustom')
                j.sedf('#PROPVALUE', propvalue, assertdir + '/assertcustom')
                j.getconf('assert-no', j.mconf, 'rem')
            elif choice == '3':  # START Remove asserts from ROM
                j.delpath(assertdir + '/assert', assertdir + '/assertcustom')
                j.getconf('assertdevices', j.uconf, add='None')
                j.getconf('acuststat', j.uconf, add='None')
                j.getconf('assert-no', j.mconf, add='1')
                choice = ''
                continue
            elif choice == '4':  # START Reset asserts to default
                j.delpath(assertdir + '/assert', assertdir + '/assertcustom')
                j.appendf(j.readf(j.tools + '/updater/custom/assert'),
                          assertdir + '/assert')
                j.appendf('    ' + j.readf(j.tools
                                           + '/updater/custom/abort'), assertdir + '/assert')
                j.sedf('#DEVICENAME', devicename, assertdir + '/assert')
                j.sedf('#DEVICECHK', devicechk, assertdir + '/assert')
                j.awkadd('#ASSERT', j.readf(assertdir + '/assert'),
                         'after', 'first', j.usdir + '/updater-script')
                j.getconf('assert-no', j.mconf, 'rem')
                choice = ''
                continue

            if j.existf(assertdir + '/assertcustom'):
                j.grepff('.*ro.product.device', assertdir
                         + '/assert', assertdir + '/assert-2')
                os.replace(assertdir + '/assert-2', assertdir + '/assert')
                j.appendf(j.readf(assertdir + '/assertcustom'),
                          assertdir + '/assert')

            if not j.getconf('assert-no', j.mconf):
                j.awkadd('#ASSERT', j.readf(assertdir + '/assert'),
                         'after', 'first', j.usdir + '/updater-script')

            if not assertch:
                choice = ''

    def boot_tools():
        loop = 0
        while loop == 0:
            timestamp = j.timest()
            j.androidversion = j.getprop('ro.build.version.release')

            if not j.androidversion:
                j.androidversion = color['r'] + 'N/A'

            if (not j.existf(j.rd + '/system/init.rc')
                    and not j.existf(j.rd + '/system/init.environ.rc')):
                countimg = 1
                if not j.existd(j.rd + '/bootimg') and not j.existd(j.rd + '/recoveryimg'):
                    chooseimg = choose_img(j.lang['title_cho_boot'])
                    if not chooseimg:
                        return
                    chosenimg = chooseimg[0]
                    chosenimg2 = chooseimg[1]
                    countimg = chooseimg[2]
                elif j.existd(j.rd + '/bootimg') and j.existf(j.rd + '/ramdisk.img'):
                    chosenimg = 'boot'
                    chosenimg2 = 'ramdisk.img'
                elif j.existd(j.rd + '/bootimg'):
                    chosenimg = 'boot'
                    chosenimg2 = 'boot.img'
                elif j.existd(j.rd + '/recoveryimg'):
                    chosenimg = 'recovery'
                    chosenimg2 = 'recovery.img'
                ramdir = j.rd + '/' + chosenimg + 'img/ramdisk'
            else:
                chosenimg = 'boot'
                chosenimg2 = 'boot.img'
                ramdir = j.rd + '/system'

            if (j.existd(j.rd + '/' + chosenimg + 'img')
                    or (j.existf(j.rd + '/system/init.rc')
                        or j.existf(j.rd + '/system/init.environ.rc'))):
                choice = ''
                while not choice:
                    bmenu = '1'
                    if chosenimg == 'boot':
                        bmenu = '5'
                        with j.cd(j.bd):
                            j.appendf(j.cmd(j.rampy() + 'status '
                                            + j.romname + ' boot'), j.logs + '/boot.log')

                        status = j.readfl(j.prfiles + '/statusfile')

                        try:
                            veritystatus = status[0].split('=')[1]
                            forceestatus = status[1].split('=')[1]
                            insecstatus = status[2].split('=')[1]
                        except Exception as e:
                            j.appendf(j.logtb(e), j.logs + '/boot.log')
                            j.appendf('\n' + '\n'.join(status),
                                      j.logs + '/boot.log')
                            veritystatus = color['r'] + 'N/A' + color['n']
                            forceestatus = color['r'] + 'N/A' + color['n']
                            insecstatus = color['r'] + 'N/A' + color['n']

                    j.banner()
                    j.kprint(j.lang['startup_project']
                             + color['g'] + j.romname, 'b')
                    j.kprint(j.lang['startup_version']
                             + color['g'] + j.androidversion + '\n', 'b')
                    j.kprint(j.lang['title_boot'] + '\n', 'ryb')
                    if (not j.existf(j.rd + '/system/init.rc')
                            and not j.existf(j.rd + '/system/init.environ.rc')):
                        print('1) ' + j.lang['menu_pack_boot'] + chosenimg2 + ' ')
                    else:
                        j.kprint('1) '
                                 + j.lang['menu_pack_boot'] + chosenimg2 + ' ', 'r')

                    if chosenimg == 'boot':
                        print('2) ' + j.lang['menu_insecure'] + chosenimg2 + ' ('
                              + color['b'] + j.lang['title_current'] + insecstatus + color['n'] + ')')
                        print('3) ' + j.lang['menu_dmverity'] + ' (' + color['b']
                              + j.lang['title_current'] + veritystatus + color['n'] + ')')
                        print('4) ' + j.lang['menu_forcee'] + ' (' + color['b']
                              + j.lang['title_current'] + forceestatus + color['n'] + ')')
                        print('5) ' + j.lang['menu_deopatch'])

                    j.kprint('m = ' + j.lang['title_main'], 'y')
                    j.kprint('q = ' + j.lang['menu_quit'] + '\n', 'm')
                    print(j.lang['select'])
                    choice = j.getChar()

                    blog = ''
                    if choice.isnumeric():
                        if choice < '1' or choice > bmenu:
                            continue
                    elif choice not in ['m', 'q']:
                        continue

                    if choice == '1' and j.sar():
                        choice = ''
                        continue
                    elif choice == 'q':
                        sys.exit()
                    elif choice == 'm':
                        return
                    elif choice == '1':
                        j.boot_pack(chosenimg, chosenimg2)
                    elif choice == '2':
                        with j.cd(j.bd):
                            blog = j.cmd(j.rampy() + 'insecure '
                                         + j.romname + ' boot')
                    elif choice == '3':
                        with j.cd(j.bd):
                            blog = j.cmd(j.rampy() + 'dmverity '
                                         + j.romname + ' boot')
                    elif choice == '4':
                        with j.cd(j.bd):
                            blog = j.cmd(j.rampy() + 'forcee ' + j.romname + ' boot')
                    elif choice == '5':
                        with j.cd(j.bd):
                            blog = j.cmd(j.rampy() + 'deopatch '
                                         + j.romname + ' boot')

                        blog2 = blog.splitlines()
                        if not j.greps('^patched', blog2):
                            j.banner()
                            if j.greps('^sepolicy\ ', blog2):
                                j.kprint(
                                    j.lang['menu_deopatch_sepol'] + '\n', 'r')
                            elif j.greps('.*\ failed', blog2):
                                j.kprint(
                                    j.lang['menu_deopatch_fail'] + '\n', 'r')
                        else:
                            j.banner()
                            j.kprint(j.lang['menu_deopatch_add'] + '\n', 'g')
                        input(j.lang['enter_continue'])

                    if blog:
                        j.appendf(blog, j.logs + '/boot.log')

                    choice = ''
                    if not j.existd(ramdir):
                        break
            else:
                if countimg > 1:
                    snum = '4'
                else:
                    snum = '3'

                choice = ''
                while not choice:
                    defboot = None
                    if j.existf(j.prfiles + '/' + chosenimg2 + '_orig/' + chosenimg2):
                        defboot = 1

                    j.banner()
                    j.kprint(j.lang['startup_project']
                             + color['g'] + j.romname, 'b')
                    j.kprint(j.lang['startup_version']
                             + color['g'] + j.androidversion + '\n', 'b')
                    j.kprint(j.lang['title_boot'] + '\n', 'ryb')
                    j.kprint(j.lang['title_unpack'] + '\n', 'r')
                    print('1) ' + j.lang['menu_unpack'] + chosenimg2)
                    print('2) ' + j.lang['menu_boot_flashable'] + chosenimg)
                    if defboot:
                        print('3) ' + j.lang['menu_boot_restore'] + chosenimg2)
                    else:
                        j.kprint('3) '
                                 + j.lang['menu_boot_restore'] + chosenimg2, 'r')
                    if snum > '3':
                        print('4) ' + j.lang['menu_switch_boot'])
                    j.kprint('m = ' + j.lang['title_main'], 'y')
                    j.kprint('q = ' + j.lang['menu_quit'] + '\n', 'm')
                    print(j.lang['select'])
                    choice = j.getChar()

                    if choice.isnumeric():
                        if choice < '1' or choice > snum:
                            continue
                    elif choice not in ['m', 'q']:
                        continue

                    if choice == 'q':
                        sys.exit()
                    elif choice == 'm':
                        return
                    elif choice == '1':  # Unpack boot.img
                        j.boot_unpack(chosenimg, chosenimg2)
                        break
                    elif choice == '2':  # Create boot/recovery flashable
                        devicename = j.get_devicename()
                        if devicename:
                            devicechk = j.getconf('devicechk', j.uconf)
                        else:
                            j.banner()
                            j.kprint(j.lang['error'], 'yrbbo')
                            j.kprint(j.lang['boot_prop_warn'] + '\n', 'r')
                            input(j.lang['enter_boot_menu'])
                            choice = ''
                            continue

                        j.mkdir(j.prfiles + '/boot')
                        signature = get_sig('boot')
                        sigcust = get_sigcust('boot')

                        j.banner()
                        j.kprint(j.lang['boot_prep_build'], 'b')

                        rminstall = None
                        if not j.existd(j.rd + '/install'):
                            j.configure()
                            rminstall = 1
                        if j.existd(j.rd + '/META-INF'):
                            j.mvdir(j.rd + '/META-INF', j.rd + '/META-INF1')

                        j.cpdir(j.tools + '/updater/META-INF', j.rd + '/META-INF')
                        copyfile(j.tools + '/updater/binary/update-binary-meta',
                                 j.usdir + '/update-binary')
                        copyfile(j.tools + '/updater/binary/busybox-arm',
                                 j.rd + '/install/bin/busybox')
                        j.delpath(j.usdir + '/updater-script')
                        sigtitle = ''
                        if chosenimg == 'recovery':
                            sigzip = signature + '-recovery'
                            sigtitle = signature.replace('_', ' ') + ' Recovery'
                            copyfile(
                                j.tools + '/updater/custom/updater-script-recovery', j.usdir + '/updater-script')
                        elif chosenimg == 'boot':
                            sigzip = signature + '-kernel'
                            sigtitle = signature.replace('_', ' ') + ' Kernel'
                            copyfile(j.tools + '/updater/custom/updater-script-kernel',
                                     j.usdir + '/updater-script')

                        if not j.existf(j.prfiles + '/assert'):
                            j.appendf(
                                j.readf(j.tools + '/updater/custom/assert'), j.prfiles + '/boot/assert')
                            j.appendf(
                                '    ' + j.readf(j.tools + '/updater/custom/abort'), j.prfiles + '/boot/assert')
                            j.sedf('#DEVICENAME', devicename,
                                   j.prfiles + '/boot/assert')
                            j.sedf('#DEVICECHK', devicechk,
                                   j.prfiles + '/boot/assert')
                            j.awkadd('#ASSERT', j.readf(
                                j.prfiles + '/boot/assert'), 'after', 'first', j.usdir + '/updater-script')
                        else:
                            j.awkadd('#ASSERT', j.readf(j.prfiles + '/assert'),
                                     'after', 'first', j.usdir + '/updater-script')

                        j.grepvf('#ASSERT', j.usdir + '/updater-script')
                        j.sedf('#SIGNATURE', sigtitle,
                               j.usdir + '/updater-script')
                        j.sedf('#SIGCUST', sigcust, j.usdir + '/updater-script')

                        if j.existf(j.rd + '/' + sigzip + '.zip'):
                            os.replace(j.rd + '/' + sigzip + '.zip',
                                       j.rd + '/' + sigzip + timestamp + '.zip')

                        if j.getconf('ubinary', j.mconf) != 'no':
                            if j.getconf('ubinary', j.mconf) == 'yes':
                                j.ubinary(j.usdir)
                            else:
                                j.banner()
                                print(j.lang['cust_convert_binary_q'])
                                print(j.lang['cust_convert_binary_q2'])
                                reply = j.getChar()
                                if reply == 'y':
                                    j.ubinary(j.usdir)

                        j.banner()
                        if chosenimg == 'recovery':
                            j.kprint(
                                sigzip + '.zip ' + j.lang['general_build'] + j.romname + ' ...', 'b')

                            romlist = ['recovery.img', 'META-INF', 'install']
                            with j.cd(j.rd):
                                j.appendf(
                                    j.zipp(sigzip + '.zip', romlist), j.logs + '/zip.log')
                        elif chosenimg == 'boot':
                            j.kprint(
                                sigzip + '.zip ' + j.lang['general_build'] + j.romname + ' ...', 'b')
                            romlist = ['boot.img', 'META-INF',
                                       'install', 'kernel.img', 'ramdisk.img']
                            with j.cd(j.rd):
                                j.appendf(
                                    j.zipp(sigzip + '.zip', romlist), j.logs + '/zip.log')
                        else:
                            if rminstall:
                                j.delpath(j.rd + '/install')
                            j.delpath(j.rd + '/META-INF')
                            if j.existd(j.rd + '/META-INF1'):
                                j.mvdir(j.rd + '/META-INF1', j.rd + '/META-INF')

                            j.banner()
                            j.kprint(j.lang['missing'], 'yrbbo')
                            j.kprint(j.lang['boot_no_img'] + '\n', 'r')
                            input(j.lang['enter_continue'])
                            choice = ''
                            continue

                        if rminstall:
                            j.delpath(j.rd + '/install')
                        j.delpath(j.rd + '/META-INF')
                        if j.existd(j.rd + '/META-INF1'):
                            os.replace(j.rd + '/META-INF1', j.rd + '/META-INF')

                        j.delpath(j.prfiles + '/boot')
                        j.banner()
                        j.kprint(sigzip + '.zip '
                                 + j.lang['general_create'] + j.romname + '\n', 'g')
                        signzip(sigzip)
                        break
                    elif choice == '3':  # Reset boot/recovery.img to original
                        if not defboot:
                            choice = ''
                            continue

                        with j.cd(j.rd):
                            j.delpath(chosenimg + 'img', chosenimg2)

                            copyfile(j.prfiles + '/' + chosenimg2
                                     + '_orig/' + chosenimg2, chosenimg2)
                            j.delpath(j.prfiles + '/' + chosenimg2 + '_orig')
                        choice = ''
                        continue
                    elif choice == '4':  # Switch between boot/recovery
                        continue

    def build_custom_zip():
        global main

        def docustzip(signature2):
            if j.existf(j.rd + '/' + signature2 + '.zip'):
                os.replace(j.rd + '/' + signature2 + '.zip', j.rd
                           + '/' + signature2 + '_' + timestamp + '.zip')

            if j.getconf('ubinary', j.mconf) != 'no':
                if j.getconf('ubinary', j.mconf) == 'yes':
                    j.ubinary(j.usdir)
                else:
                    j.banner()
                    print(j.lang['cust_convert_binary_q'])
                    print(j.lang['cust_convert_binary_q2'])
                    reply = j.getChar()
                    if reply == 'y':
                        j.ubinary(j.usdir)

            j.banner()
            j.kprint(signature2 + '.zip '
                     + j.lang['general_build'] + j.romname + ' ...', 'b')
            romlist = ['system', 'META-INF', 'install']
            with j.cd(j.rd):
                j.appendf(j.zipp(signature2 + '.zip', romlist),
                          j.logs + '/zip.log')
            j.delpath(j.rd + '/META-INF')
            if j.existd(j.rd + '/META-INF1'):
                os.replace(j.rd + '/META-INF1', j.rd + '/META-INF')

        def isready(dirlist2):
            readydir = []
            for i in dirlist2:
                if j.existd(j.sysdir + os.sep + i):
                    readydir.append(j.sysdir + os.sep + i)

            if readydir:
                return readydir
            else:
                return 1

        menu_cust = {
            '1': 'framework, app, priv-app',
            '2': 'framework, app, priv-app, lib, lib64',
            '3': 'framework',
            '4': 'app, priv-app',
            '5': 'lib, lib64',
            '6': 'media'
        }

        choice = ''
        while not choice:
            timestamp = j.timest()

            j.banner()
            j.kprint(j.lang['startup_project'] + color['g'] + j.romname, 'b')
            j.kprint(j.lang['startup_version']
                     + color['g'] + j.androidversion + '\n', 'b')
            j.kprint(j.lang['title_cho_cust_zip'] + '\n', 'ryb')
            print('1) ' + menu_cust['1'])
            print('2) ' + menu_cust['2'])
            print('3) ' + menu_cust['3'])
            print('4) ' + menu_cust['4'])
            print('5) ' + menu_cust['5'])
            print('6) ' + menu_cust['6'])
            j.kprint('7) ' + j.lang['menu_build_menu'], 'y')
            j.kprint('m = ' + j.lang['title_main'], 'y')
            j.kprint('q = ' + j.lang['menu_quit'] + '\n', 'm')
            print(j.lang['select'])
            choice = j.getChar()

            if choice.isnumeric():
                if choice < '1' or choice > '7':
                    continue
            elif choice not in ['m', 'q']:
                continue

            if choice == 'q':  # START Quit
                sys.exit()
            elif choice == 'm':  # START Main menu
                main = 1
                return
            elif choice == '7':  # START Build zip menu
                return

            dirlist = isready(menu_cust[choice].split(', '))
            if dirlist == 1:
                j.banner()
                j.kprint(j.lang['missing'], 'yrbbo')
                j.kprint(j.lang['cust_dir_info'] + j.romname, 'r')
                j.kprint(menu_cust[choice] + '\n', 'y')
                input(j.lang['enter_build_menu'])
                return

            devicechk = j.getconf('devicechk', j.uconf)
            signature = get_sig('1', 1)
            sigcust = get_sigcust()

            j.banner()
            print(j.lang['cust_deldir_q'])
            print(j.lang['cust_deldir_q2'])
            reply = j.getChar()
            if reply != 'y':
                deldir = 'no'
            else:
                deldir = ''

            j.banner()
            j.kprint(j.lang['cust_meta_prep'], 'b')
            if j.existd(j.rd + '/META-INF'):
                os.replace(j.rd + '/META-INF', j.rd + '/META-INF1')

            j.cpdir(j.tools + '/updater/META-INF', j.rd + '/META-INF')
            copyfile(j.tools + '/updater/binary/update-binary-meta',
                     j.usdir + '/update-binary')
            if not j.existd(j.rd + '/install'):
                j.configure()

            j.delpath(j.usdir + '/updater-script')
            copyfile(j.tools + '/updater/custom/updater-script-system',
                     j.usdir + '/updater-script')
            part_setup('boot')
            if not j.existf(j.prfiles + '/assert'):
                j.appendf(j.readf(j.tools + '/updater/custom/assert'),
                          j.prfiles + '/assert')
                j.appendf(j.readf(j.tools + '/updater/custom/abort'),
                          j.prfiles + '/assert')
                j.sedf('#DEVICENAME', devicename, j.prfiles + '/assert')
                j.sedf('#DEVICECHK', devicechk, j.prfiles + '/assert')
                assert_devices('1')
            else:
                j.awkadd('#ASSERT', j.readf(j.prfiles + '/assert'),
                         'after', 'first', j.usdir + '/updater-script')

            if deldir == 'no':
                j.grepvf('delete_recursive|Deleting',
                         j.usdir + '/updater-script')

            j.grepvf('#ASSERT', j.usdir + '/updater-script')
            j.sedf('#SIGNATURE', signature.replace(
                '_', ' '), j.usdir + '/updater-script')
            j.sedf('#SIGCUST', sigcust, j.usdir + '/updater-script')
            j.sedf('#DEVICENAME', devicename, j.usdir + '/updater-script')
            j.sedf('#DEVICECHK', devicechk, j.usdir + '/updater-script')

            if j.sar():
                j.sedf('/system/', '/system/system/',
                       j.usdir + '/updater-script')

            if choice in ['1', '2', '4']:
                appsym = sorted(glob.glob(
                    j.sysdir + '/app/*') + glob.glob(j.sysdir + '/priv-app/*') + glob.glob(j.rd + '/vendor/app/*'))
                symlib = ['ui_print("Creating symlinks...");',
                          'ui_print(" ");']
                for i in j.grepf('/system/app|/system/priv-app', j.prfiles + '/symlinks-system'):
                    line = i.split('"')[3].split('/lib')[0].replace('/', '', 1)
                    if line in appsym:
                        symlib.append(i)
                symlib = '\n'.join(symlib)
                j.awkadd('#SYM', symlib, 'after', 'first',
                         j.usdir + '/updater-script')

                j.grepvf('#SYM', j.usdir + '/updater-script')

                if j.existd(j.sysdir + '/app') or j.existd(j.sysdir + '/priv-app'):
                    if 'Deodexed' in j.isodexstatus():
                        j.banner()
                        print(j.lang['zipalign_q'])
                        reply = j.getChar()

                        if reply == 'y':
                            j.dozipalign()
                else:
                    j.banner()
                    j.kprint(j.lang['error'], 'yrbbo')
                    j.kprint(j.lang['cust_no_app_priv'] + j.romname + '\n', 'r')
                    input(j.lang['enter_build_menu'])
                    return
            else:
                j.grepvf('#SYM', j.usdir + '/updater-script')

            if choice == '1':  # START framework, app, priv-app
                signature2 = signature + '-afp'

                j.grepvf('.*/system/lib"|.*/system/lib64"|.*/system/media"',
                         j.usdir + '/updater-script')
            elif choice == '2':  # START framework, app, priv-app, lib
                signature2 = signature + '-aflp'

                if j.existd(j.sysdir + '/lib64'):
                    j.grepvf('.*/system/media"', j.usdir + '/updater-script')
                else:
                    j.grepvf('.*/system/lib64"|.*/system/media"',
                             j.usdir + '/updater-script')
            elif choice == '3':  # START framework
                signature2 = signature + '-framework'

                j.grepvf(
                    '.*/system/priv-app"|.*/system/app"|.*/system/lib"|.*/system/lib64"|.*/system/media"',
                    j.usdir + '/updater-script')
            elif choice == '4':  # START app, priv-app
                signature2 = signature + '-ap'

                j.grepvf(
                    '.*/system/framework"|.*/system/lib"|.*/system/lib64"|.*/system/media"',
                    j.usdir + '/updater-script')
            elif choice == '5':  # START lib
                signature2 = signature + '-lib'

                if j.existd(j.sysdir + '/lib64'):
                    j.grepvf(
                        '.*/system/framework"|.*/system/priv-app"|.*/system/app"|.*/system/media"',
                        j.usdir + '/updater-script')
                else:
                    j.grepvf(
                        '.*/system/priv-app"|.*/system/app"|.*/system/lib64"|.*/system/media"',
                        j.usdir + '/updater-script')
            elif choice == '6':  # START media
                signature2 = signature + '-media'

                j.grepvf(
                    '.*/system/framework"|.*/system/priv-app"|.*/system/app"|.*/system/lib"|.*/system/lib64"',
                    j.usdir + '/updater-script')

            with j.cd(j.rd):
                j.mvdir('system', 'system1')
                j.mkdir(j.sysdir)
                for i in dirlist:
                    j.mvdir(i.replace('system', 'system1', 1), i)

                docustzip(signature2)

                for i in dirlist:
                    j.mvdir(i, i.replace('system', 'system1', 1))

                j.delpath('system')
                j.mvdir('system1', 'system')

            j.banner()
            if j.existf(j.rd + '/' + signature2 + '.zip'):
                j.kprint(signature2 + '.zip '
                         + j.lang['general_create'] + j.romname + '\n', 'g')
                signzip(signature2)
                input(j.lang['enter_build_menu'])
            else:
                j.kprint(j.lang['error'], 'yrbbo')
                j.kprint(j.lang['build_check_ziplog'] + '\n', 'r')
                input(j.lang['enter_build_menu'])

    def build_rom_zip():
        timestamp = j.timest()
        fullrom = isfullrom()
        if fullrom == 'No':
            j.banner()
            j.kprint(j.lang['missing'], 'yrbbo')
            j.kprint(j.lang['cust_file_check'] + j.romname + '\n', 'r')
            input(j.lang['enter_rom_tools'])
            return

        update_project()
        permtype = j.getconf('permtype', j.uconf)

        if 'Deodexed' in j.isodexstatus():
            if j.autorom():
                reply = 'y'
            else:
                j.banner()
                print(j.lang['zipalign_q'])
                reply = j.getChar()

            if reply == 'y':
                j.dozipalign()

        signature = get_sig()

        j.banner()
        j.kprint(j.lang['cust_prep'], 'b')

        if j.existf(j.rd + '/' + signature + '.zip'):
            os.replace(j.rd + '/' + signature + '.zip', j.rd
                       + '/' + signature + '_' + timestamp + '.zip')

        if j.existf(j.rd + '/' + signature + '-signed.zip'):
            os.replace(j.rd + '/' + signature + '-signed.zip', j.rd
                       + '/' + signature + '-signed_' + timestamp + '.zip')

        comp = j.getconf('rom_comp_level', j.mconf) or '5'
        if not comp.isnumeric() or comp not in ['0', '1', '3', '5', '7', '9']:
            comp = '5'

        if j.existd(j.rd + '/META-INF1'):
            j.delpath(j.rd + '/META-INF')
            os.replace(j.rd + '/META-INF1', j.rd + '/META-INF')

        if permtype == 'sparse_dat':
            j.sedf('.new.dat.br', '.new.dat', j.usdir + '/updater-script')

            if j.getconf('brotli_comp', j.mconf):
                j.sedf('.new.dat', '.new.dat.br', j.usdir + '/updater-script')

        j.cpdir(j.rd + '/META-INF', j.rd + '/META-INF1')
        j.grepvf(
            '#ASSERT|#SYM|#PERM|#SYSFORMAT|#ROOT|#BUSYBOX|#VENDOR|#OEM|#PRODUCT|#CUSTOM|#SUD|#DATA|#AROMA|#GAPPS|#XPOSED|#MAGISK|#MOD|#CUST|#PRODUCT|#EXFILES|#MOUNT|#UNMOUNT',
            j.usdir + '/updater-script')

        cusdir = j.getconf('custom_dir', j.uconf, l=1)

        if permtype != 'sparse_dat' and not j.existf(j.usdir + '/aroma-config'):
            if j.getconf('ubinary', j.mconf) != 'no':
                cnv = None
                if j.getconf('ubinary', j.mconf) == 'yes':
                    cnv = 1
                else:
                    if j.autorom():
                        if j.getar('cnv_bin'):
                            cnv = 1
                    else:
                        j.banner()
                        print(j.lang['cust_convert_binary_q'])
                        print(j.lang['cust_convert_binary_q2'])
                        reply = j.getChar()
                        if reply == 'y':
                            cnv = 1

                if cnv:
                    j.ubinary(j.usdir)

        if permtype == 'sparse_dat':
            partlist = ['system']

            if j.getconf('exdirs', j.uconf):
                partlist += j.getconf('exdirs', j.uconf, l=1)

            if j.grepf('.*data.transfer', j.usdir + '/updater-script'):
                if j.getconf('data-sparse_dat', j.uconf):
                    partlist.append('data')

            for i in partlist:
                j.findimgsize(i)

            useold = None
            if j.platf == 'mac' or j.getconf('use_make_ext4fs', j.mconf) == 'Yes':
                useold = 1

            for line in partlist:
                if useold:
                    if j.partimg(line, ' -s') == 1:
                        j.delpath(j.rd + '/META-INF')
                        os.replace(j.rd + '/META-INF1', j.rd + '/META-INF')
                        for i in j.greps('.*.dat$|.*.list$', glob.glob(j.rd + '/*')):
                            j.delpath(i)
                        return 1
                    else:
                        j.partsdat(line)
                else:
                    if j.partimg2(line, 'sparse') == 1:
                        j.delpath(j.rd + '/META-INF')
                        os.replace(j.rd + '/META-INF1', j.rd + '/META-INF')
                        for i in j.greps('.*.dat$|.*.list$', glob.glob(j.rd + '/*')):
                            j.delpath(i)
                        return 1
                    else:
                        j.partsdat(line)

            j.banner()
            j.kprint(signature + '.zip '
                     + j.lang['general_build'] + j.romname + ' ...\n', 'b')
            j.kprint(j.lang['build_patient'] + '\n', 'y')

            copyfile(j.prfiles + '/file_contexts', j.rd + '/file_contexts')
            exzipfiles = ['install', 'boot.img', 'META-INF', 'supersu', 'rootzip', 'busybox', 'gapps', 'xposed',
                          'magisk', 'data', 'file_contexts', 'kernel.img', 'ramdisk.img', 'dynamic_partitions_op_list']
            if not j.getconf('data-set_metadata', j.uconf):
                exzipfiles.remove('data')

            with j.cd(j.rd):
                exall = glob.glob('*')
                extmp = j.greps(
                    '.*\.new\.dat|.*\.patch\.dat|.*\.transfer\.list', exall)
                exmod = j.getconf('mod_list', j.uconf, l=1)
                exzipfiles = exzipfiles + extmp + exmod + cusdir
                exfiles = []
                for i in exzipfiles:
                    i = j.greps('.*' + i + '$', exall)
                    if i:
                        for e in i:
                            if e not in exfiles:
                                exfiles.append(e)

                j.appendf(j.zipp(signature + '.zip', exfiles, comp),
                          j.logs + '/zip.log')
                j.delpath(*extmp)
                j.delpath(j.rd + '/file_contexts')
        elif permtype == 'raw_img':
            j.banner()
            j.kprint(j.lang['build_prep_img'], 'b')

            partlist = ['system']

            if j.getconf('exdirs', j.uconf):
                for line in j.getconf('exdirs', j.uconf, l=1):
                    partlist.append(line)

            if j.grepf('.*data_new.img', j.usdir + '/updater-script'):
                if j.getconf('data-raw_img', j.uconf):
                    partlist.append('data')

            for i in partlist:
                j.findimgsize(i)

            useold = None
            if j.platf == 'mac' or j.getconf('use_make_ext4fs', j.mconf) == 'Yes':
                useold = 1

            for i in partlist:
                if useold:
                    j.partimg(i)
                else:
                    j.partimg2(i)

            j.banner()
            j.kprint(signature + '.zip '
                     + j.lang['general_build'] + j.romname + ' ...\n', 'b')
            j.kprint(j.lang['build_patient'] + '\n', 'y')
            exzipfiles = ['boot.img', 'META-INF', 'install', 'supersu', 'rootzip',
                          'busybox', 'gapps', 'xposed', 'magisk', 'data', 'kernel.img', 'ramdisk.img']
            if not j.getconf('data-set_metadata', j.uconf):
                exzipfiles.remove('data')

            with j.cd(j.rd):
                exall = glob.glob('*')
                extmp = j.greps('.*_new\.img', exall)
                exmod = j.getconf('mod_list', j.uconf, l=1)
                exzipfiles = exzipfiles + extmp + exmod + cusdir
                exfiles = []
                for i in exzipfiles:
                    i = j.greps('.*' + i + '$', exall)
                    if i:
                        for e in i:
                            if e not in exfiles:
                                exfiles.append(e)

                j.appendf(j.zipp(signature + '.zip', exfiles, comp),
                          j.logs + '/zip.log')
                j.delpath(*extmp)
        else:
            j.banner()
            j.kprint(signature + '.zip '
                     + j.lang['general_build'] + j.romname + ' ...', 'b')

            exzipfiles = ['boot.img', 'META-INF', 'system', 'install', 'supersu', 'rootzip',
                          'busybox', 'gapps', 'xposed', 'magisk', 'data', '_exfiles', 'kernel.img', 'ramdisk.img']
            if not j.getconf('data-set_metadata', j.uconf):
                exzipfiles.remove('data')

            with j.cd(j.rd):
                if j.getconf('case_fix', j.mconf) == 'Yes':
                    old_exl = []
                    new_exl = []
                    tmp_exl = []

                    for i in j.findr('**/*.ex*.srk'):
                        old_exl.append(i)
                        newpath = i.split(
                            '/')[0] + '_exfiles/' + '/'.join(i.split('/')[1:])[:-8]
                        new_exl.append(newpath)

                        j.mkdir(os.path.dirname(newpath))

                        os.replace(i, newpath)

                        x = i.split('/')[0]
                        if x not in tmp_exl:
                            tmp_exl.append(x)

                exall = glob.glob('*')
                exmod = j.getconf('mod_list', j.uconf, l=1)
                exdirs = j.getconf('exdirs', j.uconf, l=1)

                exzipfiles = exzipfiles + exmod + cusdir + exdirs
                exfiles = []
                for i in exzipfiles:
                    i = j.greps('.*' + i + '$', exall)
                    if i:
                        for e in i:
                            if e not in exfiles:
                                exfiles.append(e)

                j.appendf(j.zipp(signature + '.zip', exfiles, comp),
                          j.logs + '/zip.log')

                if j.getconf('case_fix', j.mconf) == 'Yes':
                    cnt = 0
                    for i in new_exl:
                        os.replace(i, old_exl[cnt])
                        cnt += 1

                    for i in tmp_exl:
                        j.delpath(i + '_exfiles')

                    del new_exl
                    del old_exl
                    del tmp_exl

        del exall

        j.delpath(j.rd + '/META-INF')
        try:
            j.mvdir(j.rd + '/META-INF1', j.rd + '/META-INF')
        except:
            pass

        j.banner()
        if j.existf(j.rd + '/' + signature + '.zip'):
            j.kprint(signature + '.zip '
                     + j.lang['general_create'] + j.romname + '\n', 'g')

            # Run commands at the end of the build
            j.run_end_command()

            signzip(signature)
            input(j.lang['enter_rom_tools'])
        else:
            j.kprint(j.lang['error'], 'yrbbo')
            j.kprint(j.lang['build_check_ziplog'] + '\n', 'r')

            j.run_end_command()

            input(j.lang['enter_rom_tools'])

    def build_menu():
        global main
        j.timegt()

        if glob.glob(j.prfiles + '/fs_config*') or j.existf(deviceloc + '/capfiles-' + api):
            fsconf = color['g'] + j.lang['yes'] + color['n']
        else:
            fsconf = color['r'] + j.lang['no'] + color['n']

        choice = ''
        while not choice:
            if main == 1:
                return

            bdisplay = j.getprop('ro.build.display.id')
            bdid = 'display'
            if not bdisplay:
                bdisplay = j.getprop('ro.build.id')
                bdid = 'id'
            if not bdisplay:
                bdisplay = color['r'] + 'N/A'
                bdid = ''
            j.banner()
            j.kprint(j.lang['startup_project'] + color['g'] + j.romname, 'b')
            j.kprint(j.lang['startup_version']
                     + color['g'] + j.androidversion + '\n', 'b')
            j.kprint(j.lang['menu_build_menu'] + '\n', 'ryb')
            print('1) ' + j.lang['menu_build_zip'])
            print('2) ' + j.lang['menu_sys_img']
                  + ' (' + color['b'] + 'fs_config: ' + fsconf + ')')
            print('3) ' + j.lang['menu_super_img'])
            print('4) ' + j.lang['menu_sign'])
            print('5) ' + j.lang['donate_menu_custom_id'] + ' (' + color['b']
                  + j.lang['title_current'] + color['g'] + bdisplay + color['n'] + ')')
            j.kprint('6) ' + j.lang['menu_custom_zip'], 'y')
            j.kprint('7) ' + j.lang['menu_rom_tools'], 'y')
            j.kprint('m = ' + j.lang['title_main'], 'y')
            j.kprint('q = ' + j.lang['menu_quit'] + '\n', 'm')
            print(j.lang['select'])
            choice = j.getChar()

            if choice.isnumeric():
                if choice < '1' or choice > '7':
                    continue
            elif choice not in ['m', 'q']:
                continue

            if choice == 'q':  # START Quit
                sys.exit()
            elif choice == 'm':  # START Main menu
                main = 1
                break
            elif choice == '1':  # START Build ROM Zip
                build_rom_zip()
            elif choice == '2':  # START Build EXT4 img
                j.banner()
                j.kprint(j.lang['build_prep_sys_img'], 'b')

                imglist = j.getconf('exdirs', j.uconf, l=1) + ['system']

                if j.existd(j.rd + '/data/app'):
                    imglist += ['data']

                with j.cd(j.prfiles):
                    for i in glob.glob('fs_config-*'):
                        i = i.split('-')[1]
                        if j.existd(j.rd + '/' + i):
                            if i not in imglist:
                                imglist.append(i)

                for i in imglist:
                    if not j.existd(j.rd + '/' + i):
                        imglist.remove(i)

                chosenimg = j.chlist(
                    color['gb'] + j.lang['build_img_which'] + color['n'], sorted(imglist), len(imglist))
                if not chosenimg:
                    main = 1
                    choice = ''
                    continue

                choice2 = ''
                while not choice2:
                    lz4_ext = j.getconf('img_extension', j.uconf)
                    if lz4_ext and lz4_ext.startswith('.'):
                        lz4_ext = lz4_ext + '.lz4'
                    else:
                        lz4_ext = '.img.lz4'

                    j.banner()
                    j.kprint(j.lang['img_sparse_q'] + '\n', 'ryb')
                    print('1) raw')
                    print('2) sparse')
                    print('3) ' + chosenimg + '.new.dat'
                          + ('.br' if j.getconf('brotli_comp', j.mconf) else ''))
                    print('4) ' + chosenimg + lz4_ext)
                    j.kprint('b = ' + j.lang['menu_back'] + '\n', 'y')
                    print(j.lang['select'])
                    choice2 = j.getChar()

                    sparseimg = ''
                    if choice2.isnumeric():
                        if choice2 < '1' or choice2 > '4':
                            continue
                    elif choice2 not in ['b']:
                        continue

                    if choice2 == 'b':
                        break
                    elif choice2 != '1':
                        sparseimg = ' -s'

                    j.findimgsize(chosenimg)

                    if j.platf == 'mac' or j.getconf('use_make_ext4fs', j.mconf) == 'Yes':
                        if j.partimg(chosenimg, sparseimg, frommenu=True) == 1:
                            choice = ''
                            break
                    else:
                        if j.partimg2(chosenimg, sparseimg, frommenu=True) == 1:
                            choice = ''
                            break

                    if not j.existf(j.rd + '/' + chosenimg + '_new.img'):
                        j.banner()
                        j.kprint(j.lang['build_img_error'] + '\n', 'r')
                        input(j.lang['enter_build_menu'])
                        choice = ''
                        break
                    elif choice2 == '3':
                        imgname = j.partsdat(chosenimg)
                    elif choice2 == '4':
                        imgname = j.partlz4(chosenimg)
                    else:
                        if j.existf(j.rd + '/' + chosenimg + '_new.img') and not j.existf(
                                j.rd + '/' + chosenimg + '.img'):
                            os.replace(j.rd + '/' + chosenimg + '_new.img',
                                       j.rd + '/' + chosenimg + '.img')
                            imgname = chosenimg + '.img'
                        else:
                            imgname = chosenimg + '_new.img'

                    j.banner()
                    j.kprint(
                        imgname + ' ' + j.lang['general_create'] + j.romname + '\n', 'g')
                    input(j.lang['enter_build_menu'])
                    choice = ''
                    break
            elif choice == '3':  # START Build super.img
                j.super_build()
                choice = ''
                continue
            elif choice == '4':  # START Sign Existing zip
                with j.cd(j.rd):
                    ziplist = glob.glob('*.zip')
                countzip = len(ziplist)
                if countzip == 1:
                    signzipname = ziplist[0].replace('.zip', '')
                elif countzip == 0:
                    j.banner()
                    j.kprint(j.lang['error'], 'yrbbo')
                    j.kprint(j.lang['build_no_zip'] + '\n', 'r')
                    input(j.lang['enter_build_menu'])
                    choice = ''
                    continue
                else:
                    signzipname = j.chlist(
                        color['gb'] + j.lang['build_cho_zip'], ziplist, countzip)
                    signzipname = signzipname.replace('.zip', '')

                j.banner()
                signzip(signzipname)
                choice = ''
            elif choice == '5':  # START Custom ro.build.display.id
                if 'N/A' in bdisplay:
                    choice = ''
                    continue
                j.banner()
                print(j.lang['donate_bdisplay'] + '\n')
                bdisplaynew = input().replace(' ', '.')
                if bdid == 'display':
                    j.sedf('ro.build.display.id=' + bdisplay,
                           'ro.build.display.id=' + bdisplaynew, j.sysdir + '/build.prop')
                elif bdid == 'id':
                    j.sedf('ro.build.id=' + bdisplay, 'ro.build.id='
                           + bdisplaynew, j.sysdir + '/build.prop')

                choice = ''
            elif choice == '6':  # START Custom zip menu
                build_custom_zip()
                choice = ''
            elif choice == '7':  # START ROM Tools menu
                return

    def change_permtype():
        global main

        permtype = j.getconf('permtype', j.uconf)

        choice = ''
        while not choice:
            j.banner()
            j.kprint(j.lang['startup_project'] + color['g'] + j.romname, 'b')
            j.kprint(j.lang['startup_version']
                     + color['g'] + j.androidversion + '\n', 'b')
            j.kprint(j.lang['perm_title'] + '\n', 'ryb')
            if permtype == 'set_metadata':
                j.kprint('1) ' + j.lang['perm_set_metadata_cur']
                         + ' (' + color['b'] + j.lang['current'] + ')')
            else:
                if api < '19':
                    j.kprint('1) ' + j.lang['perm_set_metadata'], 'r')
                else:
                    print('1) ' + j.lang['perm_set_metadata'])

            if permtype == 'set_perm':
                j.kprint('2) ' + j.lang['perm_set_perm']
                         + ' (' + color['b'] + j.lang['current'] + ')')
            else:
                if api > '18':
                    j.kprint('2) ' + j.lang['perm_set_perm'], 'r')
                else:
                    print('2) ' + j.lang['perm_set_perm'])

            if permtype == 'sparse_dat':
                j.kprint('3) ' + j.lang['perm_sparse']
                         + ' (' + color['b'] + j.lang['current'] + ')')
            else:
                if api >= '21':
                    print('3) ' + j.lang['perm_sparse'])
                else:
                    j.kprint('3) ' + j.lang['perm_sparse_red'], 'r')

            if permtype == 'raw_img':
                j.kprint('4) ' + j.lang['perm_raw_img']
                         + ' (' + color['b'] + j.lang['current'] + ')')
            else:
                print('4) ' + j.lang['perm_raw_img'])

            j.kprint('5) ' + j.lang['menu_rom_tools'], 'y')
            j.kprint('m = ' + j.lang['title_main'], 'y')
            j.kprint('q = ' + j.lang['menu_quit'] + '\n', 'm')
            print(j.lang['select'])
            choice = j.getChar()

            if choice.isnumeric():
                if choice < '1' or choice > '5':
                    continue
            elif choice not in ['m', 'q']:
                continue

            if choice == '5':  # START ROM Tools menu chosen
                return
            elif choice == 'm':  # START Main menu chosen
                main = 1
                return
            elif choice == 'q':  # START Quit chosen
                sys.exit()

            abi = get_abi()

            if choice == '1':  # set_metadata chosen
                if api < '19':
                    j.banner()
                    j.kprint(j.lang['error'], 'yrbbo')
                    j.kprint(j.lang['perm_set_metadata_error'] + '\n', 'r')
                    input(j.lang['enter_change_perm_menu'])
                    choice = ''
                    continue

                j.banner()
                j.kprint(j.lang['perm_changing_perm'], 'b')
                if not j.existd(j.rd + '/META-INF'):
                    permtype = 'set_metadata'
                    j.getconf('permtype', j.uconf, add=permtype)
                    j.cpdir(j.tools + '/updater/META-INF', j.rd + '/META-INF')
                    copyfile(j.tools + '/updater/binary/update-binary-meta',
                             j.usdir + '/update-binary')

                if j.getconf('permtype', j.uconf):
                    permtest = j.grepb('#PERM', 'set_progress', j.readfl(
                        j.usdir + '/updater-script'))
                    j.grepvb(permtest, j.usdir + '/updater-script')
                    del permtest

                j.getconf('exdone', j.uconf, 'rem')
                if permtype == 'sparse_dat' or permtype == 'raw_img':
                    j.delpath(j.rd + '/install', j.rd + '/META-INF', j.rd + '/config',
                              j.prfiles + '/set_metadata', j.prfiles + '/set_perm')
                    j.cpdir(j.tools + '/updater/META-INF', j.rd + '/META-INF')
                    copyfile(j.tools + '/updater/binary/update-binary-meta',
                             j.usdir + '/update-binary')

                if not j.existf(j.prfiles + '/set_metadata1'):
                    for i in ['system'] + j.getconf('exdirs', j.uconf, l=1):
                        if j.existf(j.prfiles + '/fs_config-' + i):
                            metasetup(i)

                j.configure()
                permtype = 'set_metadata'
            elif choice == '2':  # set_perm chosen
                if api > '18':
                    j.banner()
                    j.kprint(j.lang['perm_set_perm_error'] + '\n', 'r')
                    input(j.lang['enter_continue'])
                    choice = ''
                    continue

                j.banner()
                j.kprint(j.lang['perm_changing_perm'], 'b')
                if not j.existd(j.rd + '/META-INF'):
                    permtype = 'set_perm'
                    j.getconf('permtype', j.uconf, add=permtype)
                    j.cpdir(j.tools + '/updater/META-INF', j.rd + '/META-INF')
                    copyfile(j.tools + '/updater/binary/update-binary-meta',
                             j.usdir + '/update-binary')

                if j.getconf('permtype', j.uconf):
                    permtest = j.grepb('#PERM', 'set_progress', j.readfl(
                        j.usdir + '/updater-script'))
                    j.grepvb(permtest, j.usdir + '/updater-script')

                if permtype == 'sparse_dat' or permtype == 'raw_img':
                    j.delpath(j.rd + '/install', j.rd + '/META-INF', j.rd + '/config',
                              j.prfiles + '/set_metadata', j.prfiles + '/set_perm')
                    j.getconf('exdone', j.uconf, 'rem')
                    j.cpdir(j.tools + '/updater/META-INF', j.rd + '/META-INF')
                    copyfile(j.tools + '/updater/binary/update-binary-meta',
                             j.usdir + '/update-binary')

                j.configure()
                permtype = 'set_perm'
            elif choice == '3':  # Sparse dat chosen
                if api < '21':
                    choice = ''
                    continue

                j.banner()
                j.kprint(j.lang['perm_changing_perm'], 'b')
                j.delpath(j.rd + '/install', j.rd + '/META-INF', j.rd + '/config',
                          j.prfiles + '/set_metadata', j.prfiles + '/set_perm')
                j.getconf('exdone', j.uconf, 'rem')
                j.cpdir(j.tools + '/updater/META-INF-DAT/META-INF',
                        j.rd + '/META-INF')
                copyfile(j.tools + '/updater/binary/update-binary-'
                         + abi, j.usdir + '/update-binary')
                if abi == 'meta':
                    j.configure()
                else:
                    j.configure(abi.replace('_64', '').replace('64', ''))

                permtype = 'sparse_dat'
            elif choice == '4':  # raw_img chosen
                j.banner()
                j.kprint(j.lang['perm_changing_perm'], 'b')
                j.delpath(j.rd + '/install', j.rd + '/META-INF', j.rd + '/config',
                          j.prfiles + '/set_metadata', j.prfiles + '/set_perm')
                j.getconf('exdone', j.uconf, 'rem')
                j.cpdir(j.tools + '/updater/META-INF-IMG/META-INF',
                        j.rd + '/META-INF')
                copyfile(j.tools + '/updater/binary/update-binary-meta',
                         j.usdir + '/update-binary')
                j.configure()

                permtype = 'raw_img'

            j.getconf('permtype', j.uconf, add=permtype)

        update_project()

        if j.getconf('root', j.uconf) and not j.getconf('root_existing', j.uconf):
            if (j.existf(j.sysdir + '/xbin/su')
                    or j.existd(j.rd + '/SuperSU')
                    or j.existd(j.rd + '/supersu')
                    or j.existd(j.rd + '/rootzip')):
                rootrem()
                root()
            else:
                j.getconf('root', j.uconf, 'rem')

            if j.getconf('busybox', j.uconf):
                root_busyboxrem()
                root_busybox()

        if j.getconf('data-set_metadata', j.uconf) or j.getconf('data-sparse_dat', j.uconf) or j.getconf('data-raw_img',
                                                                                                         j.uconf):
            data_apprem()
            data_app()
        return

    def choose_img(title):
        with j.cd(j.rd):
            findimg = j.greps(
                '^boot\.img$|^recovery\.img$|^kernel\.elf$|^ramdisk\.img$', glob.glob('*'))

        countimg = len(findimg)
        chosen = ''
        if countimg == 1:
            chosen = findimg[0]
        elif countimg > 1:
            chosen = j.chlist(color['ryb'] + title + color['n'], findimg, countimg)
            if not chosen:
                return []

        btype = {'boot.img': 'boot', 'kernel.elf': 'boot',
                 'ramdisk.img': 'boot', 'recovery.img': 'recovery'}
        for i in list(btype):
            if chosen == i:
                return [btype[i], chosen, countimg]

    def data_app():
        da = partadd('data')
        if da:
            return
        j.mkdir(j.rd + '/data/app')

    def data_apprem():
        with j.cd(j.usdir):
            j.grepvf(
                '"/data"|"/data/app"|Extracting data|#DATA|data.transfer|data_new.img', 'updater-script')

        dataapp = {
            'data-set_metadata': ': set_metadata',
            'data-sparse_dat': ': sparse_dat',
            'data-raw_img': ': raw_img'
        }

        for i in list(dataapp):
            if j.getconf(i, j.uconf):
                j.getconf(i, j.uconf, 'rem')

        j.delpath(*glob.glob('data-*'))

    def debloat_rom():
        global main
        if not j.existd(j.prfiles):
            j.mkdir(j.prfiles)

        def delbloat(debloat, choice2):
            with j.cd(j.rd):
                for i in debloat:
                    if i.startswith('/'):
                        continue

                    debdir = j.dirname(i)
                    debfile = os.path.basename(i)

                    if choice2 == '1':
                        j.mkdir(j.prfiles + '/debloated_files/' + debdir)

                    if j.existf(i):
                        if choice2 == '1':
                            os.replace(
                                i, j.prfiles + os.sep + 'debloated_files' + os.sep + debdir + os.sep + debfile)
                        elif choice2 == '2':
                            j.kprint(i, 'y')
                    elif j.existd(i):
                        if choice2 == '1':
                            j.mvdir(i, j.prfiles + os.sep + 'debloated_files'
                                    + os.sep + debdir + os.sep + debfile)
                        elif choice2 == '2':
                            j.kprint(i, 'y')

            j.delpath(j.prfiles + '/db_files', j.prfiles
                      + '/dbc_files', j.prfiles + '/db_knox')

        def reply2(debtype=''):
            choice2 = ''
            while not choice2:
                j.banner()
                j.kprint(j.lang['menu_rom_debloat'] + '\n', 'ryb')
                print('1) ' + debtype)
                print('2) ' + j.lang['bloat_list_menu'])
                j.kprint('b = ' + j.lang['menu_back'], 'y')
                j.kprint('q = ' + j.lang['menu_quit'] + '\n', 'm')
                print(j.lang['select'])
                choice2 = j.getChar()

                if choice2.isnumeric():
                    if choice2 < '1' or choice2 > '2':
                        choice2 = ''
                        continue
                elif choice2 not in ['b', 'q']:
                    choice2 = ''
                    continue

                return choice2

        choice = ''
        while not choice:
            j.banner()
            j.kprint(j.lang['startup_project'] + color['g'] + j.romname, 'b')
            j.kprint(j.lang['startup_version']
                     + color['g'] + j.androidversion + '\n', 'b')
            j.kprint(j.lang['menu_rom_debloat'] + '\n', 'ryb')
            print('1) ' + j.lang['menu_debloat'] + ' (' + color['b']
                  + j.lang['title_current'] + isdebloatstatus() + color['n'] + ')')
            if not j.existf(j.tools + '/root/bloat_custom') and not j.existf(j.prfiles + '/bloat_custom'):
                print('2) ' + j.lang['menu_debloat_cust']
                      + ' (' + isdebcuststatus() + ')')
            else:
                print('2) ' + j.lang['menu_debloat_cust'] + ' (' + color['b']
                      + j.lang['title_current'] + isdebcuststatus() + color['n'] + ')')
            print('3) ' + j.lang['menu_debloat_knox'] + ' (' + color['b']
                  + j.lang['title_current'] + isknoxstatus() + color['n'] + ')')
            print('4) ' + j.lang['menu_debloat_restore'])
            print('5) ' + j.lang['menu_debloat_refresh'])
            j.kprint('6) ' + j.lang['menu_rom_tools'], 'y')
            j.kprint('m = ' + j.lang['title_main'], 'y')
            j.kprint('q = ' + j.lang['menu_quit'] + '\n', 'm')
            print(j.lang['select'])
            choice = j.getChar()

            if choice.isnumeric():
                if choice < '1' or choice > '6':
                    continue
            elif choice not in ['m', 'q']:
                continue

            if choice == 'm':  # START Main Menu
                main = 1
                return
            elif choice == 'q':  # START Exit
                sys.exit()
            elif choice == '6':  # START ROM Tools Menu
                return
            elif choice == '1':  # START Debloat ROM
                if j.lang['debloated'] in isdebloatstatus():
                    j.banner()
                    j.kprint(j.lang['error'], 'yrbbo')
                    j.kprint(j.lang['bloat_already_debloated'] + '\n', 'r')
                    input(j.lang['enter_debloat_menu'])
                    choice = ''
                    continue

                choice2 = reply2(j.lang['menu_debloat'])
                if choice2 == 'b':
                    choice = ''
                    continue
                elif choice2 == 'q':  # START Exit
                    sys.exit()

                j.banner()
                if choice2 == '1':
                    j.kprint(j.lang['bloat_rem'], 'b')
                    delbloat(j.readfl(j.prfiles + '/db_files'), choice2)

                    j.banner()
                    j.kprint(j.lang['bloat_moved'], 'g')
                    j.kprint(j.prfiles + '/debloated_files', 'y')
                else:
                    j.kprint(j.lang['bloat_list_files'], 'b')
                    delbloat(j.readfl(j.prfiles + '/db_files'), choice2)

                print()
                input(j.lang['enter_debloat_menu'])
                choice = ''
                continue
            elif choice == '2':  # START Custom Debloat
                if not j.existf(j.tools + '/root/bloat_custom') and not j.existf(j.prfiles + '/bloat_custom'):
                    j.banner()
                    j.kprint(j.lang['error'], 'yrbbo')
                    j.kprint(j.lang['bloat_cust_info'] + '\n', 'r')
                    j.kprint(j.prfiles + '/bloat_custom', 'y')
                    j.kprint(j.tools + '/root/bloat_custom\n', 'y')
                    input(j.lang['enter_debloat_menu'])
                    choice = ''
                    continue

                if isdebcuststatus() == color['g'] + j.lang['debloated'] + color['n']:
                    j.banner()
                    j.kprint(j.lang['error'], 'yrbbo')
                    j.kprint(j.lang['bloat_already_debloated'] + '\n', 'r')
                    input(j.lang['enter_debloat_menu'])
                    choice = ''
                    continue

                choice2 = reply2(j.lang['menu_debloat_cust'])
                if choice2 == 'b':
                    choice = ''
                    continue
                elif choice2 == 'q':  # START Exit
                    sys.exit()

                j.banner()
                if choice2 == '1':
                    j.kprint(j.lang['bloat_rem'], 'b')
                    delbloat(j.readfl(j.prfiles + '/dbc_files'), choice2)
                    j.delpath(j.prfiles + '/dbc_files')

                    j.banner()
                    j.kprint(j.lang['bloat_moved'], 'g')
                    j.kprint(j.prfiles + '/debloated_files', 'y')
                else:
                    j.kprint(j.lang['bloat_list_files'], 'b')
                    delbloat(j.readfl(j.prfiles + '/dbc_files'), choice2)

                print()
                input(j.lang['enter_debloat_menu'])
                choice = ''
                continue
            elif choice == '3':  # START Remove Samsung Knox
                if j.lang['no_knox'] in isknoxstatus():
                    j.banner()
                    j.kprint(j.lang['error'], 'yrbbo')
                    j.kprint(j.lang['bloat_knox_not_exist'] + '\n', 'r')
                    input(j.lang['enter_debloat_menu'])
                    choice = ''
                    continue

                choice2 = reply2(j.lang['menu_debloat_knox'])
                if choice2 == 'b':
                    choice = ''
                    continue
                elif choice2 == 'q':  # START Exit
                    sys.exit()

                j.banner()
                if choice2 == '1':
                    j.kprint(j.lang['bloat_knox_rem'], 'b')
                    delbloat(j.readfl(j.prfiles + '/db_knox'), choice2)

                    j.banner()
                    j.kprint(j.lang['bloat_knox_moved'], 'g')
                    j.kprint(j.prfiles + '/debloated_files', 'y')
                else:
                    j.kprint(j.lang['bloat_list_files'], 'b')
                    delbloat(j.readfl(j.prfiles + '/db_knox'), choice2)

                print()
                input(j.lang['enter_debloat_menu'])
                choice = ''
                continue
            elif choice == '4':  # START Restore Bloat/Knox
                if not j.existd(j.prfiles + '/debloated_files'):
                    j.banner()
                    j.kprint(j.lang['error'], 'yrbbo')
                    j.kprint(j.lang['bloat_no_files_restore'] + '\n', 'r')
                    input(j.lang['enter_debloat_menu'])
                    choice = ''
                    continue

                j.banner()
                print(j.lang['bloat_restore_q'])
                reply = j.getChar()
                if reply != 'y':
                    choice = ''
                    continue

                j.banner()
                j.kprint(j.lang['bloat_restore'], 'b')
                with j.cd(j.prfiles + '/debloated_files'):
                    debtmp = []
                    for i in j.findr('**'):
                        if j.existd(i):
                            continue
                        debtmp.append(i)
                    for i in debtmp:
                        j.mkdir(j.rd + '/' + j.dirname(i))
                        os.replace(i, j.rd + '/' + i)

                with j.cd(j.prfiles):
                    j.delpath('debloated_files', 'db_files',
                              'dbc_files', 'db_knox')

                j.banner()
                j.kprint(j.lang['bloat_has_restored'] + '\n', 'g')
                input(j.lang['enter_debloat_menu'])
                choice = ''
                continue
            elif choice == '5':  # START Refresh Bloat Status
                with j.cd(j.prfiles):
                    j.delpath('db_files', 'dbc_files', 'db_knox')

                choice = ''
                continue

    def delete_project(curromname):
        switch = 0
        dellist = glob.glob('superr_*')
        dellist.sort()
        countdir = len(dellist)
        if countdir == 0:
            chosen = 0
        elif countdir == 1:
            chosen = dellist[0]
        else:
            chosen = j.chlist(
                color['yrbbo'] + j.lang['title_delete'] + color['n'], dellist, countdir)
            if not chosen:
                return
        if chosen != 0:
            j.banner()
            j.kprint(j.lang['warning'] + '\n', 'yrbbo')
            j.kprint(chosen + ' ' + color['r'] + j.lang['delete_q'], 'y')
            reply = j.getChar()

            if reply == 'y':
                if j.existd(chosen + '/bootimg') or j.existd(chosen + '/recoveryimg'):
                    j.cmd(j.issudo + 'rm -rf ' + chosen)
                else:
                    j.delpath(chosen)

                if 'superr_' + curromname == chosen:
                    switch = 1

                j.banner()
                j.kprint(chosen + j.lang['delete_has_been'] + '\n', 'g')
                input(j.lang['enter_continue'])
                return switch
        else:
            print('no file\n')
            input(j.lang['enter_continue'])
            return switch

    def extract_new():
        def do_sparse_dat(plist):
            import sdat2img

            def get_dat_line(oline):
                nline = oline.split('.')
                if nline[-1] == 'br':
                    nline = '.'.join(nline[:-3])
                else:
                    nline = '.'.join(nline[:-2])

                return nline

            if plist == 'all' or get_dat_line(plist) == 'system':
                plist = glob.glob('*.new.dat*')
                if j.greps('super.new.*', plist):
                    finalimg = 'super.img'
                else:
                    finalimg = 'system.img'
            else:
                finalimg = get_dat_line(plist) + '.img'
                plist = [plist]

            for i in plist:
                line = get_dat_line(i)

                if i.endswith('.xz'):
                    j.xzu(i)
                    j.delpath(i)

                if i.endswith('.br'):
                    j.banner()
                    j.kprint(j.lang['extract_convert_br'], 'b')

                    j.appendf(j.cmd(j.brotli + ' -d ' + i), j.logs + '/main.log')
                    j.delpath(i)

                j.banner()
                j.kprint(j.lang['extract_convert_sys'] + line + '.img ...', 'b')

                j.repout(j.logs + '/main.log')
                sdat2img.main(line + '.transfer.list',
                              line + '.new.dat', line + '.img')
                j.repout()
                j.delpath(line + '.transfer.list', line + '.new.dat')

            return finalimg

        loop = 0
        while loop == 0:
            if not glob.glob('superr_*'):
                j.banner()
                j.kprint(j.lang['error'], 'yrbbo')
                j.kprint(j.lang['no_project'] + '\n', 'r')
                input(j.lang['enter_main_menu'])
                return

            if j.autorom():
                j.getconf('signature', j.uconf, add=j.getar(
                    'rom_name').replace(' ', '_'))
                j.getconf('sigcust', j.uconf, add=j.getar('cust_sig'))

            j.imgrename()

            romzip = romtar = rommd5 = romchunk = romimg = romwin = romtgz = romtgz2 = romxz = romdat = romlz4 = ''

            with j.cd(j.rd):
                findtmp = j.greps(
                    '.*\.img$|.*\.tgz$|.*\.zip$|.*\.7z$|.*\.tar$|.*\.tar\.a$|.*\.tar\.md5$|.*\.win|.*chunk|.*\.ext4$|.*\.xz$|.*\.new\.dat|.*\.img\.lz4|.*\.ext4\.lz4',
                    glob.glob('*'))
                findtmp = j.greps(j.fl(
                    '',
                    '.*boot|.*BOOT|.*recovery|.*RECOVERY|.*ramdisk|.*RAMDISK|.*kernel|.*KERNEL|.*\.sha2$|.*\.md5$|.*\.info$'),
                    findtmp)
                for i in findtmp:
                    if j.existd(i):
                        findtmp.remove(i)
                findtmp = sorted(findtmp, key=str.lower)

            if len(findtmp) > 1:
                project = j.chlist(
                    color['gb'] + j.lang['title_extract'] + color['n'], findtmp, len(findtmp))
                if not project:
                    return
            elif len(findtmp) > 0:
                project = findtmp[0]
            else:
                project = ''

            if project:
                if any(['.tgz' in project, '.zip' in project]) and any(
                        ['-factory-' in project, '-preview-' in project]):
                    romtgz = project
                elif '.tgz' in project:
                    romtgz2 = project
                elif '.xz' in project:
                    romxz = project
                elif '.zip' in project or '.7z' in project:
                    romzip = project
                elif '.tar.md5' in project:
                    rommd5 = project
                elif '.tar.a' in project:
                    romtaratar = project.replace('.tar.a', '.tar')
                    os.replace(project, romtaratar)
                    romtar = romtaratar
                elif '.tar' in project:
                    romtar = project
                elif '.win' in project:
                    romwin = project
                elif 'chunk' in project:
                    romchunk = project
                elif project.endswith('.lz4'):
                    romlz4 = project
                elif '.ext4' in project:
                    romimg = 'system.img'
                elif project.endswith('.img'):
                    romimg = project.lower()
                elif 'new.dat' in project:
                    romdat = project

            if not any([romzip, romtar, rommd5, romimg, romwin, romchunk, romtgz, romtgz2, romxz, romdat, romlz4]):
                choice = ''
                tagain = None
                while not choice:
                    j.banner()
                    j.kprint(j.lang['startup_project']
                             + color['g'] + j.romname + '\n', 'b')
                    j.kprint(j.lang['extract_title'] + '\n', 'ryb')
                    print(j.lang['extract_no_files_message'])
                    print(j.lang['extract_no_files_message2'])
                    print(j.lang['extract_no_files_message3'])
                    print(j.lang['extract_no_files_message4'])
                    j.kprint('m = ' + j.lang['title_main'], 'y')
                    j.kprint('q = ' + j.lang['menu_quit'] + '\n', 'm')
                    choice = j.getChar()

                    if choice.isnumeric():
                        if choice < '1' or choice > '2':
                            continue
                    elif choice not in ['m', 'q']:
                        choice = ''
                        continue

                    if choice == 'q':  # START Quit
                        sys.exit()
                    elif choice == 'm':  # START Main menu
                        return
                    elif choice == '1':  # START Add a ROM zip
                        tagain = 1
                        break
                    elif choice == '2':  # Pull system, vendor, oem, product, boot, and recovery images from device
                        choice2 = ''
                        while not choice2:
                            j.banner()
                            j.kprint(j.lang['extract_cho_option'] + '\n', 'ryb')
                            j.kprint(j.lang['extract_cho_option2'] + '\n', 'b')
                            print(j.lang['extract_cho_option3'])
                            print(j.lang['extract_cho_option4'])
                            j.kprint('m = ' + j.lang['title_main'], 'y')
                            j.kprint('q = ' + j.lang['menu_quit'] + '\n', 'm')
                            choice2 = j.getChar()

                            if choice2.isnumeric():
                                if choice2 < '1' or choice2 > '2':
                                    choice2 = ''
                                    continue
                            elif choice2 not in ['m', 'q']:
                                choice2 = ''
                                continue

                            if choice2 == 'm':
                                return
                            elif choice2 == 'q':
                                sys.exit()
                            # booted to custom recovery (stock will not work)
                            elif choice2 == '1':
                                j.banner()
                                j.kprint(j.lang['extract_plug'] + '\n', 'b')
                                reply = input(j.lang['general_continue_q'])
                                if reply != 'y':
                                    return

                                j.banner()
                                j.kprint(
                                    j.lang['extract_detect_part'] + '\n', 'b')

                                j.appendf(j.cmd(
                                    j.adb + ' push ' + j.tools + '/updater/install/bin/configure.sh /tmp/srk_configure.sh'),
                                    j.logs + '/adb.log')
                                j.appendf(
                                    j.cmd(j.adb + ' shell "sh /tmp/srk_configure.sh"'), j.logs + '/adb.log')
                                j.appendf(
                                    j.cmd(j.adb + ' pull /tmp/srk_config ' + j.prfiles + '/adb_config'),
                                    j.logs + '/adb.log')
                                j.appendf(j.cmd(
                                    j.adb + ' shell "rm -rf /tmp/srk_configure.sh /tmp/srk_config"'),
                                    j.logs + '/adb.log')

                                if not j.existf(j.prfiles + '/adb_config'):
                                    j.banner()
                                    j.kprint(j.lang['error'], 'yrbbo')
                                    j.kprint(j.lang['extract_pull_error'], 'r')
                                    j.kprint(
                                        j.lang['extract_pull_error2'] + '\n', 'r')
                                    input(j.lang['enter_main_menu'])
                                    return

                                imglist = {}
                                for i in j.readfl(j.prfiles + '/adb_config'):
                                    imglist[i.split('=')[0]] = i.split('=')[1]

                                j.delpath(j.prfiles + '/adb_config')

                                for i in imglist:
                                    if i in ['slotnum', 'byname', 'sysmnt', 'fail']:
                                        continue

                                    pulltest = pullimgr(i, imglist[i])
                                    if pulltest != 0:
                                        j.appendf(
                                            'ERROR: failed to pull ' + i + '.img', j.logs + '/adb.log')
                                        break
                            # booted to Android (must be rooted)
                            elif choice2 == '2':
                                j.banner()
                                j.kprint(j.lang['byname_usb_debug'] + '\n')
                                j.kprint(
                                    j.lang['byname_usb_debug_root'], 'ryb')
                                j.kprint(
                                    j.lang['byname_usb_debug_root2'] + '\n', 'r')
                                print(j.lang['general_continue_q'])
                                reply = j.getChar()
                                if reply != 'y':
                                    choice2 = ''
                                    continue

                                j.banner()
                                j.kprint(
                                    '*** ' + j.lang['extract_detect_part2'], 'y')
                                j.kprint(
                                    j.lang['extract_detect_part3'] + ' ***' + '\n', 'y')
                                j.kprint(
                                    j.lang['extract_detect_part'] + '\n', 'b')

                                j.appendf(
                                    j.cmd(j.adb + ' wait-for-device'), j.logs + '/adb.log')

                                j.appendf(j.cmd(
                                    j.adb + ' push ' + j.tools + '/updater/install/bin/configure.sh /sdcard/srk_configure.sh'),
                                    j.logs + '/adb.log')
                                # j.cmd(j.adb+' push '+j.tools+'/updater/binary/busybox-arm /sdcard/srk_busybox')
                                # j.cmd(j.adb+' shell su -c "chmod +x /sdcard/srk_configure.sh; chmod +x /sdcard/srk_busybox"')
                                j.appendf(
                                    j.cmd(j.adb + ' shell su -c "sh /sdcard/srk_configure.sh"'), j.logs + '/adb.log')
                                j.appendf(j.cmd(
                                    j.adb + ' pull /sdcard/srk_config ' + j.prfiles + '/adb_config'),
                                    j.logs + '/adb.log')
                                j.appendf(j.cmd(
                                    j.adb + ' shell su -c "rm -rf /sdcard/srk_configure.sh /sdcard/srk_config"'),
                                    j.logs + '/adb.log')

                                if not j.existf(j.prfiles + '/adb_config'):
                                    j.banner()
                                    j.kprint(j.lang['error'], 'yrbbo')
                                    j.kprint(j.lang['extract_pull_error'], 'r')
                                    j.kprint(
                                        j.lang['extract_pull_error2'] + '\n', 'r')
                                    input(j.lang['enter_main_menu'])
                                    return

                                imglist = {}
                                for i in j.readfl(j.prfiles + '/adb_config'):
                                    imglist[i.split('=')[0]] = i.split('=')[1]

                                j.delpath(j.prfiles + '/adb_config')

                                for i in imglist:
                                    if i in ['slotnum', 'byname', 'sysmnt', 'fail']:
                                        continue

                                    pulltest = pullimga(i, imglist[i])
                                    if pulltest != 0:
                                        j.appendf(
                                            'ERROR: failed to pull ' + i + '.img', j.logs + '/adb.log')
                                        break

                            if j.existf(j.rd + '/system.img'):
                                romimg = 'system.img'
                            else:
                                j.banner()
                                j.kprint(j.lang['error'], 'yrbbo')
                                j.kprint(j.lang['extract_pull_error'], 'r')
                                j.kprint(
                                    j.lang['extract_pull_error2'] + '\n', 'r')
                                input(j.lang['enter_main_menu'])
                                return

                if tagain:
                    continue

            j.banner()
            print(j.lang['extract_q'] + color['y'] + romzip + romtar + rommd5 + romimg
                  + romchunk + romwin + romtgz + romtgz2 + romxz + romdat + romlz4 + color['n'])
            print(j.lang['extract_q2'])

            if j.getChar() != 'y':
                return

            if not j.existd(j.rd + '/00_project_files/logs'):
                j.mkdir(j.rd + '/00_project_files/logs')

            if j.autorom():
                j.banner()
                j.kprint(j.lang['extract_autorom_sudo'] + ' ...\n', 'b')
                j.cmd('echo | sudo tee')

            j.banner()
            j.kprint(j.lang['extract_prep'], 'b')

            if any([romzip, romtar, romimg, romdat, romlz4]) and ((not romimg and not romdat and not romlz4) or (
                    romimg == 'system.img' or romdat.startswith('system') or romlz4.startswith(
                'system') or romlz4.startswith('super') or romimg == 'super.img')):
                moveoldfiles(romzip, romtar, romimg, romdat)

            if romzip:
                if romzip.endswith('7z'):
                    ziptest = j.zipl7(j.rd + '/' + romzip)
                else:
                    ziptest = j.zipl(j.rd + '/' + romzip)

                if not j.greps(
                        j.fl(
                            '.*system.ext4.tar|.*system.ext4.tar.a|.*tar.md5|AP_.*tar|.*chunk.*|.*system/build.prop|.*system.new.dat|.*super.new.dat|.*system_new.img|.*system.img|.*super.img|.*payload.bin|.*system_1.img|.*.pac$|.*.img.lz4|.*.ext4.lz4',
                            '.*\.so$'), ziptest):
                    j.banner()
                    j.kprint(j.lang['warning'], 'yrbbo')
                    j.kprint(j.lang['extract_zip_fail'], 'r')
                    j.kprint(j.lang['extract_zip_fail2'] + '\n', 'r')
                    input(j.lang['enter_main_menu'])
                    return

                upbinary = ''
                ubtmp = j.greps('.*update-binary', ziptest)
                if ubtmp:
                    with j.cd(j.rd):
                        j.appendf(j.zipef(romzip, ubtmp[0]), j.logs + '/zip.log')
                        if j.grepf('^#!', 'update-binary'):
                            upbinary = '1'
                        j.delpath('update-binary')

                if upbinary == '1' and j.greps('.*system/build.prop', ziptest):
                    j.banner()
                    j.kprint(j.lang['extract_zip'], 'b')
                    with j.cd(j.rd):
                        j.appendf(j.zipu(romzip), j.logs + '/zip.log')
                    line = j.grepf('symlink ', j.usdir + '/update-binary')
                    for i in line:
                        part2 = i.split(' ')[1]
                        part3 = i.split(' ')[2]
                        j.appendf('symlink("' + part2 + '", "' + part3 + '");',
                                  j.prfiles + '/symlinks-system')

                    j.delpath(j.rd + '/META-INF')
                    romzip = ''
                    j.cpdir(j.tools + '/updater/META-INF', j.rd + '/META-INF')
                    copyfile(j.tools + '/updater/binary/update-binary-meta',
                             j.usdir + '/update-binary')
                    j.configure()
                    update_project()
                elif j.greps('.*.new.dat', ziptest):
                    j.sudo_prep()

                    j.banner()
                    j.kprint(j.lang['extract_dat'], 'b')

                    with j.cd(j.rd):
                        zipulist = j.greps(
                            '.*.new.dat.*|.*.transfer.list|boot.img|file_contexts|file_contexts.bin|dynamic_partitions_op_list',
                            ziptest)
                        for i in zipulist:
                            j.appendf(j.zipef(romzip, i), j.logs + '/zip.log')

                        romimg = do_sparse_dat('all')
                        romzip = ''
                elif j.greps('.*system_new.img|.*system.img$|.*super.img', ziptest):
                    j.sudo_prep()

                    j.banner()
                    j.kprint(j.lang['extract_img_from_zip'], 'b')

                    if j.existf('system.img'):
                        os.replace('system.img', 'system_old.img')

                    with j.cd(j.rd):
                        zipulist = j.greps('.*' + '.img|.*'.join(j.partslist) + '.img|' + '_new.img|.*'.join(
                            j.partslist) + '_new.img|.*boot.img|.*file_contexts|.*file_contexts.bin', ziptest)

                        for i in zipulist:
                            j.appendf(j.zipef(romzip, i), j.logs + '/zip.log')

                        j.imgrename(new=1)

                        romzip = ''

                        if j.existf('super.img'):
                            romimg = 'super.img'
                        else:
                            romimg = 'system.img'
                elif j.greps('.*system.ext4.tar.a', ziptest):
                    j.banner()
                    j.kprint(j.lang['extract_tar_boot'], 'b')

                    with j.cd(j.rd):
                        zipulist = j.greps(
                            '.*system.ext4.tar.a|.*system.ext4.tar', ziptest)
                        for i in zipulist:
                            j.appendf(j.zipef(romzip, i), j.logs + '/zip.log')
                        os.replace('system.ext4.tar.a', 'system.ext4.tar')
                    romzip = ''
                    romtar = 'system.ext4.tar'
                elif j.greps('.*tar.md5', ziptest) and not j.greps('^AP_.*tar|.*/AP_.*tar', ziptest):
                    extraparts = 'n'
                    if not j.autorom():
                        j.banner()
                        print(j.lang['extract_extra_extract_q'])

                        extraparts = j.getChar()
                    else:
                        if j.getar('extra_parts') == 'true':
                            extraparts = 'y'

                    j.banner()
                    tarmd5 = j.greps('.*tar.md5', ziptest)[0]

                    j.sudo_prep()

                    j.kprint(j.lang['general_extracting'] + tarmd5 + ' ...', 'b')

                    with j.cd(j.rd):
                        j.appendf(j.zipef(romzip, tarmd5), j.logs + '/zip.log')

                    j.banner()
                    j.kprint(j.lang['extract_img'], 'b')

                    if extraparts == 'y':
                        tarulist = j.greps('.*' + '.*\.img|.*'.join(j.partslist) + '.*\.img|' + '.*ext4|.*'.join(
                            j.partslist) + '.*ext4|.*boot.img|.*file_contexts|.*file_contexts.bin|.*cache.*\.img|.*cache.*ext4|.*factoryfs\.img|.*zImage|.*recovery\.img|.*modem\.bin|.*aboot\.mbn|.*NON-HLOS\.bin|.*sboot\.bin|.*sbl1\.mbn|.*sdi\.mbn|.*rpm\.mbn|.*tz\.mbn',
                                           j.tarlist(j.rd + '/' + tarmd5))
                    else:
                        tarulist = j.greps('.*' + '.*\.img|.*'.join(j.partslist) + '.*\.img|' + '.*ext4|.*'.join(
                            j.partslist) + '.*ext4|.*boot.img|.*file_contexts|.*file_contexts.bin|.*cache.*\.img|.*cache.*ext4|.*factoryfs\.img|.*zImage',
                                           j.tarlist(j.rd + '/' + tarmd5))

                    with j.cd(j.rd):
                        for i in tarulist:
                            j.appendf(j.taref(tarmd5, i), j.logs + '/zip.log')
                            if i.endswith('.lz4'):
                                j.kprint(
                                    j.lang['general_extracting'] + i[:-4] + ' ...', 'y')
                                os.system(j.lz4 + ' -q ' + i)
                                j.delpath(i)

                        j.imgrename()

                    if j.existf(j.rd + '/system.img'):
                        j.delpath(j.rd + '/' + tarmd5)
                    else:
                        j.banner()
                        j.kprint(j.lang['error'], 'yrbbo')
                        j.kprint(j.lang['extract_fail'] + '\n', 'r')
                        input(j.lang['enter_main_menu'])
                        return

                    romzip = ''
                    romimg = 'system.img'
                elif j.greps('^AP_.*tar|.*/AP_.*tar', ziptest):
                    extraparts = 'n'
                    if not j.autorom():
                        j.banner()
                        print(j.lang['extract_extra_extract_q'])
                        extraparts = j.getChar()
                    else:
                        if j.getar('extra_parts') == 'true':
                            extraparts = 'y'

                    j.sudo_prep()

                    j.banner()
                    if romzip.endswith('7z'):
                        j.kprint(j.lang['extract_tar_md5'][:-4], 'b')
                    else:
                        j.kprint(j.lang['extract_tar_md5'], 'b')

                    if extraparts == 'y':
                        mainmd5 = j.greps('^AP_.*tar|.*/AP_.*tar', ziptest)
                        cscmd5 = j.greps('^CSC_.*tar|.*/CSC_.*tar', ziptest)
                        cpmd5 = j.greps('^CP_.*tar|.*/CP_.*tar', ziptest)
                        blmd5 = j.greps('^BL_.*tar|.*/CP_.*tar', ziptest)
                        zipulist = []
                        for i in [mainmd5, cscmd5, cpmd5, blmd5]:
                            if i:
                                zipulist.append(i[0])
                    else:
                        mainmd5 = j.greps('^AP_.*tar|.*/AP_.*tar', ziptest)
                        cscmd5 = j.greps('^CSC_.*tar|.*/CSC_.*tar', ziptest)
                        zipulist = []
                        for i in [mainmd5, cscmd5]:
                            if i:
                                zipulist.append(i[0])

                    with j.cd(j.rd):
                        for i in zipulist:
                            j.appendf(j.zipef(romzip, i), j.logs + '/zip.log')

                        j.sudo_prep(quiet=1)

                        j.banner()
                        j.kprint(j.lang['extract_img'], 'b')
                        for filename in zipulist:
                            if extraparts == 'y':
                                tarulist = j.greps(
                                    '.*' + '.*\.img|.*'.join(j.partslist) + '.*\.img|' + '.*ext4|.*'.join(
                                        j.partslist) + '.*ext4|.*boot.img|.*file_contexts|.*file_contexts.bin|.*cache.*\.img|.*cache.*ext4|.*factoryfs\.img|.*zImage|.*recovery\.img|.*modem\.bin|.*aboot\.mbn|.*NON-HLOS\.bin|.*sboot\.bin|.*sbl1\.mbn|.*sdi\.mbn|.*rpm\.mbn|.*tz\.mbn',
                                    j.tarlist(filename))
                            else:
                                tarulist = j.greps(
                                    '.*' + '.*\.img|.*'.join(j.partslist) + '.*\.img|' + '.*ext4|.*'.join(
                                        j.partslist) + '.*ext4|.*boot.img|.*file_contexts|.*file_contexts.bin|.*cache.*\.img|.*cache.*ext4|.*factoryfs\.img|.*zImage',
                                    j.tarlist(filename))

                            for i in tarulist:
                                j.kprint(
                                    j.lang['general_extracting'] + i + ' ...', 'y')
                                j.appendf(j.taref(filename, i),
                                          j.logs + '/zip.log')
                                j.sudo_prep(quiet=1)

                            j.delpath(filename)

                        for i in glob.glob('*.lz4'):
                            j.kprint(
                                j.lang['general_extracting'] + i[:-4] + ' ...', 'y')
                            os.system(j.lz4 + ' -q ' + i)
                            j.delpath(i)
                            j.sudo_prep(quiet=1)

                        j.imgrename()

                        if j.existf('system.img'):
                            romimg = 'system.img'
                        elif j.existf('super.img'):
                            romimg = 'super.img'
                        else:
                            j.banner()
                            j.kprint(j.lang['error'], 'yrbbo')
                            j.kprint(j.lang['extract_fail'] + '\n', 'r')
                            input(j.lang['enter_main_menu'])
                            return

                    romzip = ''
                elif j.greps('.*.img.lz4|.*.ext4.lz4', ziptest):
                    j.sudo_prep()

                    zipulist = j.greps('.*.img.lz4|.*.ext4.lz4|.*boot.img', ziptest)

                    with j.cd(j.rd):
                        for i in zipulist:
                            j.appendf(j.zipef(romzip, i), j.logs + '/zip.log')

                        for i in glob.glob('*.img.lz4') + glob.glob('*.ext4.lz4'):
                            j.kprint(
                                j.lang['general_extracting'] + i + ' ...', 'y')
                            os.system(j.lz4 + ' -qB6 --content-size ' + i)
                            j.delpath(i)

                        romzip = ''

                        if j.existf('super.img'):
                            romimg = 'super.img'
                        else:
                            romimg = 'system.img'
                elif j.greps(j.fl('.*system.*chunk.*', '.*\.so$'), ziptest):
                    j.banner()
                    j.kprint(j.lang['extract_chunk'], 'b')
                    with j.cd(j.rd):
                        zipulist = j.greps(j.fl('.*' + '.*chunk.*|.*'.join(j.partslist) + '.*chunk.*|' + '.img|.*'.join(
                            j.partslist) + '.img|.*boot.img|.*file_contexts|.*file_contexts.bin',
                                                '.*system_b.img.*|.*\.so$'), ziptest)

                        for i in zipulist:
                            j.appendf(j.zipef(romzip, i), j.logs + '/zip.log')

                        romzip = ''
                        romchunk = sorted(
                            j.grepv('system_other', glob.glob('*system*chunk*')))
                elif j.greps('.*payload.bin', ziptest):
                    j.sudo_prep()

                    j.banner()
                    j.kprint(j.lang['extract_pbin'], 'b')
                    with j.cd(j.rd):
                        zipulist = j.greps(
                            '.*payload.bin|.*file_contexts|.*file_contexts.bin', ziptest)
                        for i in zipulist:
                            j.appendf(j.zipef(romzip, i), j.logs + '/zip.log')

                        import pbin_dump
                        pbin_dump.main('payload.bin', 'boot',
                                       'cache', *j.partslist)

                        j.delpath('payload.bin')

                        romzip = ''
                        if j.existf('super.img'):
                            romimg = 'super.img'
                        else:
                            romimg = 'system.img'
                elif j.greps('.*system_1\..*img', ziptest):
                    j.banner()
                    j.kprint(j.lang['error'], 'yrbbo')
                    j.kprint(j.lang['extract_use_concat'] + '\n', 'r')
                    input(j.lang['enter_main_menu'])
                    return
                elif j.greps('.*.pac$', ziptest):
                    j.sudo_prep()

                    j.banner()
                    j.kprint(j.lang['general_extracting'] + 'pac ...', 'b')
                    with j.cd(j.rd):
                        pacimglist = [x + '.img' for x in j.partslist + ['boot']]
                        zipulist = j.greps('.*.pac$', ziptest)

                        for i in zipulist:
                            j.mkdir('tmppac')
                            pacname = os.path.basename(i)

                            with j.cd('tmppac'):
                                j.appendf(j.zipef('../' + romzip, i),
                                          j.logs + '/zip.log')

                                j.cmd(j.pacextract + ' -f ' + pacname)

                                for x in glob.glob('*.img'):
                                    if x in pacimglist:
                                        os.replace(x, '../' + x)

                            j.delpath('tmppac')

                        romzip = ''
                        if j.existf('super.img'):
                            romimg = 'super.img'
                        else:
                            romimg = 'system.img'

                with j.cd(j.rd):
                    for i in ['file_contexts', 'file_contexts.bin']:
                        if j.existf(i):
                            os.replace(i, j.prfiles + '/' + i)

                if romzip:
                    j.banner()
                    j.kprint(j.lang['general_extracting'] + romzip, 'b')
                    with j.cd(j.rd):
                        j.appendf(j.zipu(romzip), j.logs + '/zip.log')

                    with j.cd(j.rd + '/META-INF'):
                        j.delpath(*j.greps('.*RSA$|.*SF$|.*MF$', glob.glob('*')))

                    j.delpath(j.rd + '/META-INF/com/android')

                    ptest = [j.existf(j.rd + '/system/build.prop'),
                             j.existf(j.rd + '/system/system/build.prop')]
                    if any(ptest) and j.existf(j.usdir + '/updater-script'):
                        permtype = ''
                        if j.grepf('^set_perm_recursive', j.usdir + '/updater-script'):
                            permtype = 'set_perm'
                        elif j.grepf('^set_metadata_recursive', j.usdir + '/updater-script'):
                            permtype = 'set_metadata'

                        j.getconf('permtype', j.uconf, add=permtype)
                        for i in j.grepf(j.fl('^' + permtype, '/tmp/'), j.usdir + '/updater-script'):
                            j.appendf(i, j.prfiles + '/' + permtype)

                        j.get_symlinks()

                        with j.cd(j.prfiles):
                            j.delpath(*glob.glob('debloat_test*'))

                        update_project()

            if romchunk:
                j.sudo_prep()

                j.banner()
                j.kprint(j.lang['extract_convert_chunk'], 'b')
                if 'sparsechunk' in romchunk or 'sparsechunk' in romchunk[0]:
                    with j.cd(j.rd):
                        j.appendf(j.cmd(j.simg2img + ' ' + ' '.join(romchunk)
                                        + ' system.img.raw'), j.logs + '/main.log')

                        for i in j.partslist:
                            tmpchunk = glob.glob(i + '.img_sparsechunk*')
                            if tmpchunk:
                                j.appendf(
                                    j.cmd(j.simg2img + ' ' + ' '.join(tmpchunk) + ' ' + i + '.img.raw'),
                                    j.logs + '/main.log')

                        for rimg in [x + '.img.raw' for x in j.partslist]:
                            if j.existf(rimg):
                                j.delpath(
                                    *glob.glob(rimg.replace('.img.raw', '') + '*chunk*'))
                                with open(rimg, 'rb') as f:
                                    data = f.read(500000)
                                    moto = re.search(b'\x4d\x4f\x54\x4f', data)
                                    offset = 0
                                    if moto:
                                        result = []
                                        for i in re.finditer(b'\x53\xEF', data):
                                            result.append(i.start() - 1080)

                                        for i in result:
                                            if data[i] == 0:
                                                offset = i
                                                break

                                if offset > 0:
                                    j.banner()
                                    j.kprint(
                                        j.lang['extract_fix_img'] + rimg.replace('.raw', '') + ' ...', 'b')
                                    with open(rimg.replace('.raw', ''), 'wb') as o, open(rimg, 'rb') as f:
                                        data = f.seek(offset)
                                        data = f.read(15360)
                                        while data:
                                            o.write(data)
                                            data = f.read(15360)

                                if j.existf(rimg) and not j.existf(rimg.replace('.raw', '')):
                                    os.rename(rimg, rimg.replace('.raw', ''))
                                else:
                                    j.delpath(rimg)
                            else:
                                if rimg == 'system.img.raw':
                                    j.banner()
                                    j.kprint(j.lang['error'], 'yrbbo')
                                    j.kprint(j.lang['extract_fail'] + '\n', 'r')
                                    input(j.lang['enter_main_menu'])
                                    return
                else:
                    with j.cd(j.rd):
                        j.appendf(
                            j.cmd(j.simg2img + ' *chunk* system.img'), j.logs + '/main.log')

                romimg = 'system.img'

            partition = 'system'
            if romwin or romtar:
                for i in ['data'] + j.partslist:
                    if i in romwin or i in romtar:
                        partition = i
                        break

            if romwin and any([
                partition + '_img' in romwin,
                partition + '.img' in romwin,
                partition + 'img' in romwin,
                partition + '_image' in romwin
            ]):
                os.replace(j.rd + '/' + romwin, j.rd + '/' + partition + '.img')
                romimg = partition + '.img'
                romwin = ''
                if j.existf(j.rd + '/boot.emmc.win'):
                    copyfile(j.rd + '/boot.emmc.win', j.rd + '/boot.img')
            elif romwin:
                with j.cd(j.rd):
                    if j.existf('boot.emmc.win'):
                        copyfile('boot.emmc.win', 'boot.img')

                winextract(partition, romwin)

            if romtgz:
                j.banner()
                j.kprint(j.lang['extract_check_firm'], 'b')
                tartest = ''
                extype = ''
                if '.tgz' in romtgz:
                    with j.cd(j.rd):
                        tartest = j.tarlist(romtgz)
                    extype = 'tgz'
                elif '.zip' in romtgz:
                    with j.cd(j.rd):
                        tartest = j.zipl(romtgz)
                    tgzdevice = romtgz.split('-')[0]
                    tartest = j.greps(tgzdevice, tartest)
                    extype = 'zip'

                if not j.greps('image-', tartest):
                    j.banner()
                    j.kprint(j.lang['error'], 'yrbbo')
                    j.kprint(j.lang['extract_tgz_fail'], 'r')
                    j.kprint(j.lang['extract_tgz_fail2'] + '\n', 'r')
                    input(j.lang['enter_main_menu'])
                    return

                j.sudo_prep()

                eximage = j.greps('image-', tartest)[0]
                exdir = j.dirname(eximage)
                imagezip = os.path.basename(eximage)
                j.banner()
                j.kprint(j.lang['extract_files'], 'b')
                with j.cd(j.rd):
                    if extype == 'tgz':
                        j.appendf(j.taref(romtgz, eximage), j.logs + '/zip.log')
                    elif extype == 'zip':
                        j.appendf(j.zipef(romtgz, eximage, eximage),
                                  j.logs + '/zip.log')

                    with j.cd(exdir):
                        j.banner()
                        j.kprint(j.lang['extract_img'], 'b')
                        ziplist = [x + '.img' for x in j.partslist + ['boot']]
                        for i in ziplist:
                            try:
                                j.appendf(j.zipef(imagezip, i),
                                          j.logs + '/zip.log')
                                os.replace(i, j.rd + '/' + i)
                            except:
                                pass

                    j.delpath(exdir)

                if j.existf(j.rd + '/super.img'):
                    romimg = 'super.img'
                else:
                    romimg = 'system.img'

            if romtgz2:
                j.sudo_prep()

                j.banner()
                j.kprint(j.lang['extract_files'], 'b')

                with j.cd(j.rd):
                    j.taru(romtgz2, 'tmptar')

                    tarulist = j.greps(
                        '.*' + '.img|.*'.join(j.partslist) + '.img|.*boot.img', j.findr('tmptar/**/*.img'))

                    for i in tarulist:
                        os.replace(i, os.path.basename(i))

                    j.delpath('tmptar')

                    if j.existf('super.img'):
                        romimg = 'super.img'
                    else:
                        romimg = 'system.img'

            if romxz:
                with j.cd(j.rd):
                    ziplist = j.greps('system.*.img', j.zipl7(romxz))

                    if not ziplist:
                        j.banner()
                        j.kprint(j.lang['error'], 'yrbbo')
                        j.kprint(j.lang['extract_xz_fail'] + '\n', 'r')
                        input(j.lang['enter_main_menu'])
                        return

                    j.sudo_prep()

                    j.banner()
                    j.kprint(j.lang['extract_files'], 'b')

                    j.zipu(romxz)
                    os.replace(ziplist[0], 'system.img')

                    romxz = ''
                    romimg = 'system.img'

            if rommd5:
                with j.cd(j.rd):
                    tartest = j.tarlist(rommd5)
                    if j.greps('.*super.*\.img|.*system.*\.img|.*system.*ext4', tartest):
                        j.sudo_prep()

                        j.banner()
                        j.kprint(j.lang['extract_img'], 'b')

                        tarulist = j.greps('.*' + '.*\.img|.*'.join(j.partslist) + '.*\.img|' + '.*ext4|.*'.join(
                            j.partslist) + '.*ext4|.*boot.img|.*cache.*\.img|.*cache.*ext4', tartest)

                        with j.cd(j.rd):
                            for i in tarulist:
                                j.appendf(j.taref(rommd5, i),
                                          j.logs + '/zip.log')
                            j.imgrename()

                        if j.existf('super.img'):
                            romimg = 'super.img'
                        else:
                            romimg = 'system.img'
                    else:
                        j.banner()
                        j.kprint(j.lang['error'], 'yrbbo')
                        j.kprint(j.lang['extract_md5_fail'] + '\n', 'r')
                        input(j.lang['enter_main_menu'])
                        return

            if romtar:
                tartest = j.tarlist(j.rd + '/' + romtar)

                if j.greps('.*.img.lz4', tartest):
                    j.sudo_prep()

                    zipulist = j.greps('.*.img.lz4|.*boot.img', tartest)

                    with j.cd(j.rd):
                        for i in zipulist:
                            j.appendf(j.taref(romtar, i), j.logs + '/zip.log')

                        for i in glob.glob('*.img.lz4'):
                            j.kprint(
                                j.lang['general_extracting'] + i + ' ...', 'y')
                            os.system(j.lz4 + ' -qB6 --content-size ' + i)
                            j.delpath(i)

                        if j.existf('super.img'):
                            romimg = 'super.img'
                        else:
                            romimg = 'system.img'
                else:
                    try:
                        with j.cd(j.rd):
                            tar_ef = j.greps(
                                '.* /bin', j.cmd(j.tar + ' --numeric-owner -tvf ' + romtar).splitlines())[0].split()[1]
                    except:
                        tar_ef = None

                    if tar_ef != '0/2000':
                        j.banner()
                        j.kprint(j.lang['error'], 'yrbbo')
                        j.kprint(j.lang['extract_tar_fail'] + '\n', 'r')
                        input(j.lang['enter_main_menu'])
                        return

                    j.banner()
                    j.kprint(j.lang['extract_general'] + romtar + ' ...', 'b')
                    tartest = j.tarlist(j.rd + '/' + romtar)
                    with j.cd(j.rd):
                        if not partition in tartest[0]:
                            j.appendf(j.taru(romtar, partition),
                                      j.logs + '/zip.log')
                            if tartest[0].startswith('/'):
                                dirr = partition
                            else:
                                dirr = partition + '/'
                        else:
                            j.appendf(j.taru(romtar), j.logs + '/zip.log')
                            dirr = ''

                        tarfs(romtar, dirr, partition)

            if romdat:
                j.sudo_prep()

                with j.cd(j.rd):
                    romimg = do_sparse_dat(romdat)

            if romlz4:
                j.sudo_prep()

                with j.cd(j.rd):
                    j.kprint(j.lang['general_extracting'] + romlz4 + ' ...', 'b')

                    os.system(j.lz4 + ' -qB6 --content-size ' + romlz4)

                    romimg = romlz4[:-4].replace('.ext4', '')
                    romlz4 = ''

            if romimg:
                j.imgrename()
                j.sudo_prep()

                if romimg in ['super.img', 'super_new.img']:
                    if j.super_unpack(romimg) == 1:
                        return

                    romimg = 'system.img'

                romimgdir = romimg.replace('.img', '')
                j.delpath(j.prfiles + '/symlinks-' + romimgdir,
                          j.prfiles + '/symlinks-' + romimgdir + '.orig')

                tmpx = j.imgextract(romimg)
                if tmpx != 0:
                    j.delpath(j.rd + '/' + romimgdir)
                    j.banner()
                    j.kprint(j.lang['error'], 'yrbbo')

                    if tmpx == 4:
                        j.kprint(j.lang['extract_rom_fail_ext4'] + '\n', 'r')
                    else:
                        j.kprint(j.lang['extract_rom_fail'] + '\n', 'r')

                    input(j.lang['enter_main_menu'])
                    return

            if j.sar():
                j.sysdir = j.rd + os.sep + 'system' + os.sep + 'system'
            elif j.existf(j.rd + '/system/build.prop'):
                j.sysdir = j.rd + os.sep + 'system'
            else:
                j.sysdir = j.rd + os.sep + partition

            if j.existf(j.sysdir + '/xbin/su') or j.existf(j.sysdir + '/bin/su'):
                j.getconf('root_existing', j.uconf, add='1')

            if any([romimg, romwin]) and romimg not in [x + '.img' for x in (j.partslist + ['data', 'cache'])[1:]]:
                if j.existf(j.sysdir + '/build.prop'):
                    ex_all_img = j.getconf('extract_all_img', j.mconf)

                    if j.existf(j.rd + '/cache.img'):
                        reply = 'n'
                        if not j.autorom() and ex_all_img != 'Yes':
                            j.banner()
                            print(j.lang['extract_cache_extract_q'])
                            reply = j.getChar()
                        else:
                            if j.getar('cache_img') == 'true':
                                reply = 'y'

                        if reply == 'y':
                            j.imgextract('cache.img')
                            if j.existd(j.rd + '/cache') and (
                                    j.getprop('ro.product.manufacturer') == 'samsung' or j.getprop(
                                'ro.product.system.manufacturer') == 'samsung'):
                                reply = 'y'
                                if not j.autorom() and ex_all_img != 'Yes':
                                    print(
                                        '\n' + j.lang['extract_cache_include_q'])
                                    print(j.lang['extract_cache_include_q2'])
                                    reply = j.getChar()

                                if reply == 'y':
                                    j.banner()
                                    j.kprint(j.lang['extract_cache'] + '\n', 'b')

                                    with j.cd(j.rd + '/cache'):
                                        cscfull = j.findr('**')
                                        if j.greps('.*\.zip', cscfull):
                                            cscfull = j.greps(
                                                '.*\.zip', cscfull)[0]
                                            cscdir = j.dirname(cscfull)
                                            csczip = os.path.basename(cscfull)
                                            with j.cd(cscdir):
                                                j.appendf(
                                                    j.zipu(csczip), j.logs + '/zip.log')
                                                with j.cd('system'):
                                                    for i in glob.glob('*'):
                                                        if j.existd(i):
                                                            j.mvdir(
                                                                i, j.sysdir + '/' + i)
                                                        else:
                                                            os.replace(
                                                                i, j.sysdir + '/' + i)
                                        else:
                                            if not j.autorom() and ex_all_img != 'Yes':
                                                j.banner()
                                                j.kprint(
                                                    j.lang['error'], 'yrbbo')
                                                j.kprint(
                                                    j.lang['extract_cache_fail'] + '\n', 'r')
                                                input(j.lang['enter_continue'])

                                    j.delpath(j.rd + '/cache')
                    elif j.existf(j.rd + '/system_other.img'):
                        j.banner()
                        j.kprint(j.lang['general_extracting']
                                 + 'system_other.img ...', 'b')

                        with j.cd(j.rd):
                            sar_val = j.sar()

                            os.replace('system.img', 'system.img1')
                            os.replace('system_other.img', 'system.img')
                            os.replace('system', 'system1')

                            if j.sparse_chk('system.img'):
                                j.sparse_conv('system.img')

                            j.ext4Xtract('system')

                            os.replace('system.img', 'system_other.img')
                            os.replace('system.img1', 'system.img')

                            rep_val = 'system1'
                            if sar_val and j.existd('system/app'):
                                rep_val = 'system1/system'

                            for i in j.findr('system/**'):
                                if j.existd(i):
                                    continue

                                j.mkdir(j.dirname(i).replace(
                                    'system', rep_val, 1))
                                os.replace(i, i.replace('system', rep_val, 1))

                            j.delpath('system')
                            os.replace('system1', 'system')

                    with j.cd(j.rd):
                        eximgl = j.greps(j.fl('',
                                              'system\.img|system_other|cache|boot\.img|boot\.emmc|recovery\.img|ramdisk\.img|kernel\.img|super\.img'),
                                         glob.glob(
                                             '*.img') + glob.glob('*.win') + glob.glob('*.win000'))
                        if eximgl:
                            for line in eximgl:
                                if line.endswith('.img'):
                                    line2 = line.replace('.img', '')
                                else:
                                    line2 = line.split('.')[0]

                                if line2 not in j.getconf('exdirs', j.uconf, l=1):
                                    if j.autorom():
                                        if line2 in ['vendor', 'oem', 'odm', 'product', 'system_ext']:
                                            if j.getar('vendor_img') == 'true':
                                                if line.endswith('.img'):
                                                    j.imgextract(line)
                                                else:
                                                    winextract(line2, line)

                                                j.getconf('exdirs', j.uconf, add=j.getconf(
                                                    'exdirs', j.uconf, l=1) + [line2], l=1)

                                                continue

                                    reply = 'y'
                                    if ex_all_img != 'Yes':
                                        j.banner()
                                        print(
                                            j.lang['extract_extra_extract'] + color['y'] + line + color['n'] + j.lang[
                                                'extract_extra_q'])
                                        reply = j.getChar()

                                    if reply == 'y':
                                        if line.endswith('.img'):
                                            j.imgextract(line)
                                        else:
                                            winextract(line2, line)

                                        if j.existd(line2):
                                            reply = 'y'
                                            if ex_all_img != 'Yes':
                                                print(
                                                    '\n' + j.lang['extract_extra_include'])
                                                print(
                                                    line + j.lang['extract_extra_include_q'])
                                                reply = j.getChar()

                                            if reply == 'y':
                                                curr_exdirs = j.getconf(
                                                    'exdirs', j.uconf, l=1)
                                                if line2 not in curr_exdirs:
                                                    j.getconf(
                                                        'exdirs', j.uconf, add=curr_exdirs + [line2], l=1)
                                else:
                                    if line.endswith('.img'):
                                        j.imgextract(line)
                                    else:
                                        winextract(line2, line)

                    if not j.autorom():
                        j.getconf('permtype', j.uconf, 'rem')

                    j.get_symlinks()

                    if j.existd(j.rd + '/system'):
                        j.delpath(j.rd + '/META-INF', j.rd + '/install')
                        j.cpdir(j.tools + '/updater/META-INF', j.rd + '/META-INF')
                        copyfile(j.tools + '/updater/binary/update-binary-meta',
                                 j.usdir + '/update-binary')
                        j.configure()
                        j.delpath(j.prfiles + '/debloat_test',
                                  j.prfiles + '/debloat_test_custom')
                        update_project()
                else:
                    j.banner()
                    j.kprint(j.lang['error'], 'yrbbo')
                    j.kprint(j.lang['extract_rom_fail'] + '\n', 'r')
                    input(j.lang['enter_main_menu'])
                    return

            if j.autorom():
                if j.sar():
                    j.sysdir = j.rd + os.sep + 'system' + os.sep + 'system'
                elif j.existf(j.rd + '/system/build.prop'):
                    j.sysdir = j.rd + os.sep + 'system'
                if j.getar('root_add'):
                    root()
                if j.getar('busybox_add'):
                    root_busybox()
                if j.getar('sud_add'):
                    root_sud()
                if j.getar('verity_rem') or j.getar('force_rem'):
                    btype = {'boot.img': 'boot',
                             'kernel.elf': 'boot', 'ramdisk.img': 'boot'}
                    for i in list(btype):
                        if j.existf(j.rd + '/' + i):
                            chosenimg = btype[i]
                            chosenimg2 = i
                            break

                    j.boot_unpack(chosenimg, chosenimg2, '1')
                    if j.getar('verity_rem'):
                        with j.cd(j.bd):
                            j.appendf(j.cmd(j.rampy() + 'dmverity '
                                            + j.romname + ' boot'), j.logs + '/boot.log')
                    if j.getar('force_rem'):
                        with j.cd(j.bd):
                            j.appendf(j.cmd(j.rampy() + 'forcee '
                                            + j.romname + ' boot'), j.logs + '/boot.log')

                    j.boot_pack(chosenimg, chosenimg2, '1')

                    with j.cd(j.rd):
                        j.delpath(chosenimg + 'img')

                if j.getar('deodex_type') != 'skip':
                    j.deodex_start()
                if j.getar('build_rom'):
                    build_rom_zip()
            return

    def get_abi():
        if j.getprop('ro.product.manufacturer') == 'samsung' or j.getprop(
                'ro.product.system.manufacturer') == 'samsung':
            abi = 'meta'
        else:
            abi = j.getprop('ro.product.cpu.abilist')
            if abi:
                if ',' in abi:
                    abi = abi.split(',')[0]
            else:
                abi = j.getprop('ro.product.cpu.abi')

            if abi.startswith('arm64'):
                abi = 'arm64'
            elif abi.startswith('arm'):
                abi = 'arm'
            elif abi.startswith('x86_64'):
                abi = 'x86_64'
            elif abi.startswith('x86'):
                abi = 'x86'
            else:
                abi = 'arm'

        return abi

    def get_byname():
        devicename = j.get_devicename()
        deviceloc = j.tools + os.sep + 'devices' + os.sep + devicename
        if j.existf(deviceloc + '/superr_byname'):
            return j.readf(deviceloc + '/superr_byname')

        choice = ''
        while not choice:
            j.banner()
            print(j.lang['byname_how_to_get_q'] + '\n')
            print('1) ' + j.lang['menu_byname_detect_boot'])
            print('2) ' + j.lang['menu_byname_detect_device'])
            print('3) ' + j.lang['menu_byname_detect_manual'])
            print('4) ' + j.lang['menu_byname_detect_mmc'])
            j.kprint('s = ' + j.lang['menu_skip'], 'y')
            j.kprint('q = ' + j.lang['menu_quit'] + '\n', 'm')
            print(j.lang['select'])
            choice = j.getChar()

            if choice.isnumeric():
                if choice < '1' or choice > '4':
                    choice = ''
                    continue
            elif choice == 's':  # START Skip
                return
            elif choice == 'q':  # START Quit
                sys.exit()
            else:
                choice = ''
                continue

            if choice == '1':  # START Detect by-name from the boot.img
                bootchk = None
                with j.cd(j.rd):
                    for i in ['boot.img', 'kernel.elf', 'recovery.img', 'ramdisk.img']:
                        if j.existf(i):
                            bootchk = 1
                if not bootchk:
                    j.banner()
                    j.kprint(j.lang['error'], 'yrbbo')
                    j.kprint(j.lang['byname_no_boot'], 'r')
                    j.kprint(j.lang['byname_no_boot2'] + '\n', 'r')
                    input(j.lang['enter_continue'])
                    choice = ''
                    continue

                j.banner()
                chosenimg = ''
                if not j.existd(j.rd + '/bootimg/ramdisk') and not j.existd(j.rd + '/recoveryimg/ramdisk'):
                    chooseimg = choose_img(j.lang['byname_which_img_q'])
                    chosenimg = chooseimg[0]
                    chosenimg2 = chooseimg[1]

                    if not chosenimg2:
                        j.banner()
                        j.kprint(j.lang['error'], 'yrbbo')
                        j.kprint(j.lang['byname_no_files'] + '\n', 'r')

                        j.delpath(deviceloc + '/superr_byname')
                        input(j.lang['enter_continue'])
                        choice = ''
                        continue

                    j.kprint(j.lang['byname_detect'] + chosenimg2 + ' ...', 'b')
                    j.boot_unpack(chosenimg, chosenimg2, '1')
                elif j.existd(j.rd + '/bootimg/ramdisk'):
                    chosenimg = 'boot'
                elif j.existd(j.rd + '/recoveryimg/ramdisk'):
                    chosenimg = 'recovery'

                if not j.existf(deviceloc + '/superr_byname'):
                    with j.cd(j.bd):
                        j.appendf(j.cmd(j.rampy() + 'byname ' + j.romname
                                        + ' ' + chosenimg), j.logs + '/boot.log')

                if not j.existf(deviceloc + '/superr_byname'):
                    j.banner()
                    j.kprint(j.lang['error'], 'yrbbo')
                    j.kprint(j.lang['byname_boot_fail'], 'r')
                    print(j.lang['byname_try_recovery'] + '\n')
                    input(j.lang['enter_continue'])
                    j.delpath(deviceloc + '/superr_byname')
                    choice = ''
                    continue
            elif choice == '2':  # START Detect by-name from your device
                j.banner()
                j.kprint(j.lang['byname_usb_debug'], 'b')
                j.kprint(j.lang['byname_usb_debug2'] + '\n', 'b')
                input(j.lang['enter_ready'])
                j.banner()
                j.kprint('...', 'b')
                byname = j.adb_byname(deviceloc)
            elif choice == '3':  # START Enter it manually
                j.banner()
                print(j.lang['byname_detect_manual'] + '\n')
                j.kprint(j.lang['example'] + '\n', 'gb')
                j.kprint('/dev/block/bootdevice/by-name\n', 'y')
                byname = input()
                if not byname:
                    j.banner()
                    j.kprint(j.lang['error'], 'yrbbo')
                    j.kprint(j.lang['byname_no_byname'] + '\n', 'r')
                    input(j.lang['enter_continue'])
                    choice = ''
                    continue
                else:
                    j.appendf(byname, deviceloc + '/superr_byname')
            elif choice == '4':  # START Create mmc from recovery.img
                j.banner()
                j.kprint(j.lang['byname_create_mmc'], 'b')
                if not j.existd(j.rd + '/recoveryimg/ramdisk'):
                    if j.existf(j.rd + '/recovery.img'):
                        j.boot_unpack('recovery', 'recovery.img', '1')
                    else:
                        j.banner()
                        j.kprint(j.lang['error'], 'yrbbo')
                        j.kprint(j.lang['byname_need_recovery'] + '\n', 'r')
                        input(j.lang['enter_continue'])
                        choice = ''
                        continue

                with j.cd(j.bd):
                    j.appendf(j.cmd(j.rampy() + 'mmc ' + j.romname
                                    + ' recovery'), j.logs + '/boot.log')

                j.delpath(j.rd + 'recoveryimg')

                if not j.existf(deviceloc + '/superr_mmc'):
                    j.banner()
                    j.kprint(j.lang['error'], 'yrbbo')
                    j.kprint(j.lang['byname_no_mmc'] + '\n', 'r')
                    input(j.lang['enter_continue'])
                    choice = ''
                    continue

                if j.existf(deviceloc + '/superr_mmc'):
                    j.appendf('mmc', deviceloc + '/superr_byname')
                    j.chown(deviceloc + '/superr_byname')
                else:
                    j.delpath(deviceloc + '/superr_mmc')
                    j.banner()
                    j.kprint(j.lang['error'], 'yrbbo')
                    j.kprint(j.lang['byname_recovery_fail'], 'r')
                    print(j.lang['byname_try_boot'] + '\n')
                    input(j.lang['enter_continue'])
                    choice = ''
                    continue

            if j.existf(deviceloc + '/superr_byname'):
                return j.readf(deviceloc + '/superr_byname')
            else:
                choice = ''

    def get_sig(loc='', tmpsig=None):
        if loc:
            sigloc = loc + '-signature'
        else:
            sigloc = 'signature'

        if loc or not j.getconf(sigloc, j.uconf):
            while True:
                j.banner()
                j.kprint(color['b'] + j.lang['sig_info'])
                j.kprint(j.lang['sig_info2'], 'b')
                j.kprint(j.lang['sig_info3'] + '\n', 'b')
                print(j.lang['sig_info_q'] + '\n')
                signature = input().replace(' ', '_')
                if '/' in signature:
                    j.banner()
                    j.kprint(j.lang['sig_info_error'] + '\n', 'r')
                    input(j.lang['enter_continue'])
                    continue
                break

            if tmpsig:
                return signature

            if not loc:
                j.getconf(sigloc, j.uconf, add=signature)
        else:
            signature = j.getconf(sigloc, j.uconf)

        return signature

    def get_sigcust(loc=''):
        if loc == 'boot':
            sigloc = 'sigboot'
        else:
            sigloc = 'sigcust'

        if loc or not j.getconf(sigloc, j.uconf):
            j.banner()
            j.kprint(j.lang['donate_sig_cust'], 'b')
            j.kprint(j.lang['donate_sig_cust2'] + '\n', 'b')
            print(j.lang['donate_sig_q'] + '\n')
            sigcust = input()
            if not loc:
                j.getconf(sigloc, j.uconf, add=sigcust)
        else:
            sigcust = j.getconf(sigloc, j.uconf)

        return sigcust

    def get_tools():
        if not j.internet():
            j.banner()
            j.kprint(j.lang['error'], 'yrbbo')
            j.kprint(j.lang['update_no_internet'] + '\n', 'r')
            input(j.lang['enter_exit'])
            sys.exit()

        def dltools(tooldir, toolsize):
            j.banner()
            j.kprint(j.lang['notice'], 'ryb')
            j.kprint(j.lang['tools_need'], 'r')
            j.kprint(toolsize + '\n', 'y')
            print(j.lang['tools_dl_q'])

            reply = j.getChar()
            if reply != 'y':
                sys.exit()

            j.banner()
            j.kprint(j.lang['tools_dl_install'], 'b')

            j.mkdir(j.tools + '/' + tooldir)

            with j.cd(j.tools + '/' + tooldir):
                if tooldir == 'linux_tools':
                    j.dlfile('64-bit_python.zip', tooldir + '.zip', 1)
                else:
                    j.dlfile(tooldir + '.zip', tooldir + '.zip', 1)

            if not j.existf(j.tools + '/' + tooldir + '/' + tooldir + '.zip'):
                j.banner()
                j.kprint(j.lang['error'], 'yrbbo')
                j.kprint(j.lang['tools_dl_failed'], 'r')
                j.delpath(j.tools + '/' + tooldir)
                input(j.lang['enter_exit'])
                sys.exit()

            with j.cd(j.tools + '/' + tooldir):
                j.zipu2(tooldir + '.zip')
                j.delpath(tooldir + '.zip')

        sprint = ''

        if j.platf in ['lin', 'wsl', 'wsl2']:
            tooldir = 'linux_tools'
        elif j.platf == 'mac':
            tooldir = 'mac_tools'

        if not j.existd(j.tools + os.sep + tooldir):
            sprint = 1
            dltools(tooldir, j.lang['lintools_dl'])

        if tooldir == 'linux_tools':
            md5tmp = j.md5chk(md5file='md5lin')
        else:
            md5tmp = j.md5chk(md5file='md5mac')

        if j.md5chk(md5file='md5aik') != 0:
            j.delpath(j.AIK)

            if not sprint:
                j.banner()
                j.kprint(j.lang['tools_dl_install'], 'b')

            with j.cd(j.tools + '/boot'):
                try:
                    j.dlfile('AIK_linux.zip', 'aik.zip', 1)
                    j.internet(j.server1 + '/dllog/?f=AIK_linux&u=' + j.srkuser)
                    j.zipu2('aik.zip')
                except:
                    pass

                j.delpath('aik.zip')

        if md5tmp != 0:
            if not sprint:
                j.banner()
                j.kprint(j.lang['tools_dl_install'], 'b')

            with j.cd(j.tools):
                for i in md5tmp:
                    j.delpath(i)
                    ibase = os.path.basename(i)
                    j.dlfile(i + '.zip', ibase + '.zip', 1)
                    j.zipu(ibase + '.zip')
                    j.delpath(ibase + '.zip')

        if j.md5chk(md5file='md5smali') != 0:
            j.delpath(j.tools + '/smali')

            if not sprint:
                j.banner()
                j.kprint(j.lang['tools_dl_install'], 'b')

            with j.cd(j.tools):
                j.dlfile('srk_smali.zip', 'smali.zip', 1)
                try:
                    j.zipu2('smali.zip')
                except:
                    pass
                j.delpath('smali.zip')

        ubcheck = j.md5chk(md5file='md5binary')
        if ubcheck != 0:
            j.mkdir(j.tools + '/updater/binary')

            with j.cd(j.tools + '/updater/binary'):
                for i in ubcheck:
                    j.delpath(j.tools + '/' + i)
                    j.dlfile(i, os.path.basename(i), 1)

        del ubcheck

        if not j.existd(j.tools + '/devices'):
            if not sprint:
                j.banner()
                j.kprint(j.lang['tools_dl_install'], 'b')

            with j.cd(j.tools):
                j.dlfile('srkp_devices.zip', 'devices.zip', 1)
                j.zipu2('devices.zip')
                j.delpath('devices.zip')

        if j.existf(j.tools + '/root/root_zips/SuperSU.zip'):
            if j.md5chk(md5file='md5su') != 0:
                j.delpath(j.tools + '/root/root_zips/SuperSU.zip')

        if j.existf(j.tools + '/root/busybox/Busybox.zip'):
            if j.md5chk(md5file='md5busybox') != 0:
                j.delpath(j.tools + '/root/busybox/Busybox.zip')

        for i in j.readfl(j.tools + '/depends/xfiles'):
            j.cmd('chmod a+x ' + i)

        toolsfail = []
        if not j.existf(j.tools + '/linux_tools/aapt') and not j.existf(j.tools + '/mac_tools/aapt'):
            toolsfail.append(tooldir)

        if not j.existd(j.tools + '/smali'):
            toolsfail.append('smali')

        if not j.existd(j.tools + '/devices'):
            j.mkdir(j.tools + '/devices')
            toolsfail.append('devices')

        if not j.existf(j.AIK + '/unpackimg.sh'):
            toolsfail.append('boot/AIK')

        if toolsfail:
            j.banner()
            if len(toolsfail) == 1 and toolsfail[0] == 'devices':
                j.kprint(j.lang['warning'], 'yrbbo')
                j.kprint(j.lang['tools_dl_device_failed'], 'r')
                j.kprint(j.lang['tools_dl_device_failed2'], 'r')
                j.kprint(j.lang['tools_dl_device_failed3'] + '\n', 'r')
                input(j.lang['enter_continue'])
            else:
                toolprint = []
                for i in toolsfail:
                    toolprint.append(os.path.basename(i))
                    if i != tooldir:
                        j.delpath(j.tools + '/' + i)

                j.kprint(j.lang['error'], 'yrbbo')
                j.kprint(j.lang['tools_dl_install_failed'], 'r')
                j.kprint('\n'.join(toolprint) + '\n', 'y')
                input(j.lang['enter_exit'])
                sys.exit()

    def ext_dirmenu():
        global main
        choice = ''
        while not choice:
            if j.getconf('custom_dir', j.uconf):
                cctr = color['g'] + \
                       ', '.join(j.getconf('custom_dir', j.uconf, l=1))
            else:
                cctr = color['r'] + j.lang['menu_cctr']

            j.banner()
            j.kprint(j.lang['startup_project'] + color['g'] + j.romname, 'b')
            j.kprint(j.lang['startup_version']
                     + color['g'] + j.androidversion + '\n', 'b')
            j.kprint(j.lang['menu_extra_dir'] + '\n', 'ryb')
            print('1) ' + j.lang['menu_data'] + ' (' + color['b']
                  + j.lang['title_current'] + color['g'] + isdataapp() + color['n'] + ')')
            print('2) ' + j.lang['menu_cust_dir'] + ' (' + color['b']
                  + j.lang['title_current'] + cctr + color['n'] + ')')
            j.kprint('3) ' + j.lang['menu_rom_tools'], 'y')
            j.kprint('m = ' + j.lang['title_main'], 'y')
            j.kprint('q = ' + j.lang['menu_quit'] + '\n', 'm')
            print(j.lang['select'])
            choice = j.getChar()

            if choice.isnumeric():
                if choice < '1' or choice > '3':
                    choice = ''
                    continue
            elif choice not in ['m', 'q']:
                choice = ''
                continue

            if choice == 'm':  # START Main Menu
                main = 1
                return
            elif choice == 'q':  # START Quit
                sys.exit()
            elif choice == '1':  # START /data/app support
                if 'Enabled' not in isdataapp():
                    j.banner()
                    print(j.lang['extra_data_q'])
                    reply = j.getChar()
                    if reply == 'y':
                        data_app()
                        if j.existd(j.rd + '/data'):
                            j.banner()
                            j.kprint(j.lang['extra_data_added'] + '\n', 'g')
                            j.kprint(j.rd + '/data/app\n', 'y')
                            input(j.lang['enter_extra_dir_menu'])
                else:
                    j.banner()
                    j.kprint(j.lang['extra_already_data'] + '\n\n', 'g')
                    j.kprint(j.lang['extra_already_data2'] + '\n\n', 'b')
                    print(j.lang['extra_already_data3'])
                    reply = j.getChar()
                    if reply == 'y':
                        data_apprem()
                        j.banner()
                        j.kprint(j.lang['extra_data_rem'] + '\n', 'g')
                        input(j.lang['enter_extra_dir_menu'])

                choice = ''
                continue
            elif choice == '2':  # START Custom copied to ROM
                cusname = None
                while not cusname:
                    j.banner()
                    print(j.lang['extra_cust_name'] + '\n')
                    j.kprint(j.lang['example'], 'gbbo')
                    j.kprint('mycustomdir\n', 'y')

                    cusname = input()
                    if ' ' in cusname:
                        j.banner()
                        j.kprint(j.lang['spaces_not_allowed'] + '\n', 'r')
                        input(j.lang['enter_try_again'])
                        cusname = None

                if cusname in j.getconf('custom_dir', j.uconf, l=1):
                    j.banner()
                    j.kprint(cusname + j.lang['extra_cust_already'] + '\n', 'r')
                    print(j.lang['general_remove_q'])
                    reply = j.getChar()

                    if reply == 'y':
                        j.delpath(j.rd + '/' + cusname)
                        oldconf = j.getconf('custom_dir', j.uconf, l=1)
                        oldconf.remove(cusname)
                        if oldconf:
                            j.getconf('custom_dir', j.uconf, add=oldconf, l=1)
                        else:
                            j.getconf('custom_dir', j.uconf, 'rem')

                        j.grepvf(cusname, j.usdir + '/updater-script')

                        choice = ''
                        continue
                    else:
                        choice = ''
                        continue

                j.mkdir(j.rd + '/' + cusname)
                if j.getconf('custom_dir', j.uconf):
                    j.getconf('custom_dir', j.uconf, add=j.getconf(
                        'custom_dir', j.uconf, l=1) + [cusname], l=1)
                else:
                    j.getconf('custom_dir', j.uconf, add=cusname)

                j.banner()
                print(cusname + j.lang['extra_cust_name_q'])
                reply = j.getChar()
                if reply == 'y':
                    j.banner()
                    print(j.lang['extra_cust_loc'] + '\n')
                    j.kprint(j.lang['example'], 'gbbo')
                    j.kprint('/system\n', 'y')
                    cusloc = input()

                    j.banner()
                    j.kprint(j.lang['extra_cust_setup'] + cusname + ' ...', 'b')

                    if not j.grepf('#CUSTOM', j.usdir + '/updater-script'):
                        permtype = j.getconf('permtype', j.uconf)
                        if permtype == 'sparse_dat':
                            j.awkadd('block_image_update\(.*"system"', '#CUSTOM',
                                     'after', 'first', j.usdir + '/updater-script')
                        elif permtype == 'raw_img':
                            j.awkadd('.*system_new.*', '#CUSTOM', 'after',
                                     'first', j.usdir + '/updater-script')
                        else:
                            j.awkadd('^package_extract_dir.*"system"', '#CUSTOM',
                                     'after', 'first', j.usdir + '/updater-script')

                    if cusloc.startswith('/'):
                        cusloc = cusloc[1:]

                    j.sedf('#CUSTOM', j.readf(
                        j.tools + '/updater/custom_dir.txt'), j.usdir + '/updater-script')
                    j.sedf('#CUSDIR', cusname, j.usdir + '/updater-script')
                    j.sedf('#CUSLOC', cusloc, j.usdir + '/updater-script')

                j.banner()
                j.kprint(cusname + ' ' + j.lang['extra_cust_add'] + '\n', 'g')
                input(j.lang['enter_extra_dir_menu'])
            elif choice == '3':  # START ROM Tools Menu
                return

            choice = ''
            continue

    def isassert():
        if not j.getconf('assert-no', j.mconf):
            j.delpath(j.prfiles + '/assertcust')

        if j.existf(j.usdir + '/updater-script'):
            if j.grepf(j.fl('abort', '.*ERROR'), j.usdir + '/updater-script'):
                assertdevices = j.grepf(
                    'abort', j.usdir + '/updater-script')[0].split('"')[2].replace('\\', '')
                if assertdevices:
                    j.getconf('assertdevices', j.uconf, add=assertdevices)
                else:
                    j.getconf('assertdevices', j.uconf, add='None')

                acuststat = j.grepf(
                    j.fl('assert.*', '.*ro.product.device.*'), j.usdir + '/updater-script')
                if acuststat:
                    ctest = []
                    ctmp = []
                    for i in acuststat:
                        a = i.split('"')[1].strip()
                        b = i.split('"')[3].strip()
                        ctmp.append(a)
                        ctest.append(a + '=' + b)
                    ctmp = ', '.join(ctmp)
                    j.getconf('acuststat', j.uconf, add=ctmp)
                    for i in ctest:
                        j.appendf(i, j.prfiles + '/assertcust')
                else:
                    j.getconf('acuststat', j.uconf, add='None')

    def isbusyboxstatus():
        if j.existd(j.rd):
            dtmp = [
                j.existf(j.rd + '/system/xbin/busybox'),
                j.existd(j.rd + '/Busybox'),
                j.existd(j.rd + '/busybox'),
                j.existd(j.rd + '/BusyBox')
            ]
            if any(dtmp):
                j.getconf('busybox', j.uconf, add='1')
                return color['g'] + j.lang['enabled'] + color['n']
            else:
                j.getconf('busybox', j.uconf, 'rem')
                return color['r'] + j.lang['disabled'] + color['n']

    def isdataapp():
        dataapp = {
            'data-set_metadata': ': set_metadata',
            'data-sparse_dat': ': sparse_dat',
            'data-raw_img': ': raw_img'
        }
        for i in list(dataapp):
            if j.getconf(i, j.uconf):
                if j.existd(j.rd + '/data'):
                    return color['g'] + j.lang['enabled'] + dataapp[i] + color['n']
                else:
                    data_apprem()
        return color['r'] + j.lang['add_support'] + color['n']

    def isdebcuststatus():
        nsysdir = ''
        if j.sar():
            nsysdir = 'system/'

        if j.existf(j.tools + '/root/bloat_custom') or j.existf(j.prfiles + '/bloat_custom'):
            if not j.existf(j.prfiles + '/dbc_files'):
                if j.existf(j.prfiles + '/bloat_custom'):
                    debloat = j.readfl(j.prfiles + '/bloat_custom')
                elif j.existf(j.tools + '/root/bloat_custom'):
                    debloat = j.readfl(j.tools + '/root/bloat_custom')
                debtmp = []
                with j.cd(j.rd):
                    for i in debloat:
                        i = i.strip()
                        if i.startswith('system'):
                            tmp = glob.glob(nsysdir + i)
                        else:
                            tmp = glob.glob(i)

                        for a in tmp:
                            if a not in debtmp:
                                debtmp.append(a)

                if debtmp:
                    j.appendf('\n'.join(debtmp), j.prfiles + '/dbc_files')

            if not j.existf(j.prfiles + '/dbc_files'):
                return color['g'] + j.lang['debloated'] + color['n']
            else:
                return color['r'] + j.lang['bloated'] + color['n']
        else:
            j.touch(j.tools + '/root/bloat_custom')
            return color['r'] + j.lang['bloat_dir_emply'] + color['n']

    def isdebloatstatus():
        nsysdir = ''
        if j.sar():
            nsysdir = 'system/'

        if not j.existf(j.prfiles + '/db_files'):
            debtmp = []
            with j.cd(j.rd):
                for i in j.readfl(j.tools + '/root/bloat'):
                    if i.startswith('system'):
                        tmp = glob.glob(nsysdir + i)
                    else:
                        tmp = glob.glob(i)

                    for a in tmp:
                        if a not in debtmp:
                            debtmp.append(a)

            if debtmp:
                j.appendf('\n'.join(debtmp), j.prfiles + '/db_files')

        if not j.existf(j.prfiles + '/db_files'):
            return color['g'] + j.lang['debloated'] + color['n']
        else:
            return color['r'] + j.lang['bloated'] + color['n']

    def isfullrom():
        fullrom = 'No'
        if j.existd(j.sysdir):
            dirtmp = [j.sysdir + '/lib', j.sysdir + '/etc',
                      j.sysdir + '/bin', j.rd + '/META-INF']
            fullrom = 'Yes'
            for i in dirtmp:
                if not j.existd(i):
                    fullrom = 'No'
                    break
            if fullrom == 'Yes':
                if not j.getconf('noboot', j.uconf):
                    with j.cd(j.rd):
                        thechk = None
                        for i in ['boot.img', 'kernel.img', 'ramdisk.img']:
                            if j.existf(i):
                                thechk = 1
                    if not thechk:
                        j.banner()
                        print(j.lang['build_no_boot_q'])
                        print(j.lang['build_no_boot_q2'])
                        reply = j.getChar()
                        if reply != 'y':
                            fullrom = 'No'
                        else:
                            j.getconf('noboot', j.uconf, add='1')
                            j.grepvf(
                                'boot.img|boot image|kernel.img|kernel image|ramdisk.img|ramdisk image',
                                j.usdir + '/updater-script')
                            fullrom = 'Yes'
        return fullrom

    def isknoxstatus():
        nsysdir = ''
        if j.sar():
            nsysdir = 'system/'

        if not j.existf(j.prfiles + '/db_knox'):
            knotmp = []
            with j.cd(j.rd):
                for i in j.readfl(j.tools + '/root/knox'):
                    if i.startswith('system'):
                        tmp = glob.glob(nsysdir + i)
                    else:
                        tmp = glob.glob(i)

                    for a in tmp:
                        if a not in knotmp:
                            knotmp.append(a)

            if knotmp:
                j.appendf('\n'.join(knotmp), j.prfiles + '/db_knox')

        if not j.existf(j.prfiles + '/db_knox'):
            return color['g'] + j.lang['no_knox'] + color['n']
        else:
            return color['r'] + j.lang['knox'] + color['n']

    def isrootstatus():
        if j.existd(j.rd):
            roots = ''
            if j.existf(j.sysdir + '/xbin/su'):
                roots = 'xbin/su'
            elif j.existd(j.rd + '/SuperSU') or j.existd(j.rd + '/supersu') or j.existf(j.rd + '/rootzip/SuperSU.zip'):
                if j.existf(j.sysdir + '/.supersu'):
                    roots = 'SuperSU-S'
                else:
                    roots = 'SuperSU-SL'
            elif j.existd(j.rd + '/magisk') or j.existf(j.rd + '/rootzip/Magisk.zip'):
                roots = 'Magisk'
            elif j.existd(j.rd + '/rootzip'):
                try:
                    roots = os.path.basename(glob.glob(j.rd + '/rootzip/*.zip')[0])
                except:
                    pass

            if roots:
                j.getconf('root', j.uconf, add='1')
                return color['g'] + roots + color['n']
            else:
                j.getconf('root', j.uconf, 'rem')
                return color['r'] + j.lang['no_root'] + color['n']

    def issud():
        if j.grepf('su.d', j.usdir + '/updater-script') or j.existd(j.rd + '/system/su.d'):
            j.getconf('sud', j.uconf, add='1')
            return color['g'] + j.lang['enabled'] + color['n']
        else:
            j.getconf('sud', j.uconf, 'rem')
            return color['r'] + j.lang['disabled'] + color['n']

    def metasetup(extractdir):
        def dirmeta(idir):
            try:
                rider = j.greps('^' + dirr + extractdir + '/'
                                + idir + ' ', filer)[0].split()
                if rider:
                    try:
                        vinblk.remove(rider[0])
                    except:
                        pass

                    if j.getconf('metasize', j.mconf) != 'Long':
                        vinblk.append(rider[0] + ' -R')
                        nocon.append(
                            '.*:' + j.greps(rider[0] + ' ', fcontexts).split(':')[2])

                    riders = j.greps('^' + dirr + extractdir
                                     + '/' + idir + '.*', filer)[1:]

                    for i in j.greps(j.fl('', '.*' + rider[1] + ' ' + rider[2] + ' ' + rider[3] + '$'), riders):
                        i = i.split()[0]
                        vinblk.append(i)
            except:
                return

        with j.cd(j.rd):
            filerd = j.findr(extractdir + '/**')
        dirr = ''

        if extractdir == 'system' and j.sar():
            dirr = 'system/'
            filer = []
            for i in j.readfl(j.prfiles + '/fs_config-' + extractdir):
                filer.append(dirr + i)
        else:
            filer = j.readfl(j.prfiles + '/fs_config-' + extractdir)

        f3 = None
        if j.existf(j.prfiles + '/file_contexts3-' + extractdir):
            fcontexts = j.readfl(j.prfiles + '/file_contexts3-' + extractdir)
            f3 = 1
        else:
            j.get_contexts()
            if j.existf(j.prfiles + '/file_contexts'):
                fcontexts = j.readfl(j.prfiles + '/file_contexts')
            else:
                return '1'

        metalist = []
        vinblk = []
        nocon = []

        if extractdir == 'system':
            metalist = [dirr + 'system -R', dirr + 'system/bin -R']
            if j.sar():
                roottmp = glob.glob('system/*')
                if 'system/system' in roottmp:
                    roottmp.remove('system/system')
                metalist = sorted(roottmp) + metalist

            metalist = metalist + sorted(j.findr(dirr + 'system/bin/**'))
            if glob.glob(dirr + extractdir + '/vendor/*'):
                for i in ['app', 'bin', 'etc', 'lib', 'lib64', 'rfs']:
                    dirmeta('vendor/' + i)

                if vinblk:
                    metalist = metalist + vinblk

            set_metadata1 = 'set_metadata1'
        elif extractdir == 'vendor':
            for i in ['app', 'bin', 'etc', 'firmware', 'framework', 'lib', 'lib64', 'media', 'overlay',
                      'qcril_database', 'usr']:
                dirmeta(i)
            metalist = ['vendor -R'] + vinblk
            set_metadata1 = 'set_metadataV'
        else:
            metalist = [extractdir + ' -R']
            set_metadata1 = 'set_metadataV'

        capfiles = j.greps('^' + extractdir + '.*capabilities=', filer)
        if not capfiles:
            devicename = j.get_devicename()
            if devicename:
                deviceloc = j.tools + os.sep + 'devices' + os.sep + devicename
                api = j.getprop('ro.build.version.sdk')
                if j.existf(deviceloc + '/capfiles-' + api):
                    capfiles = j.greps(
                        '^' + extractdir + ' ', j.grepf('=', deviceloc + '/capfiles-' + api))
                else:
                    capfiles = []

        for i in capfiles:
            i = i.split()[0]
            if i not in metalist:
                metalist.append(i)

        ugid = ' '.join(j.greps('^' + dirr + extractdir + ' ', filer)
                        [0].split()[-3:-1])
        for i in j.greps(j.fl('^' + extractdir, '.*' + ugid + ' 0644$|.*' + ugid + ' 0755$'), filer):
            i = i.split()[0]
            if i not in metalist:
                metalist.append(i)

        if extractdir == 'system':
            contest = j.greps(j.fl('', '.* \?$|.*:system_file|^/vendor|^/oem'
                                   + ('|' + '|'.join(nocon) if nocon else '')), fcontexts)
        else:
            try:
                if nocon:
                    contest = j.greps(
                        j.fl('^/' + extractdir, '.* \?$|' + '|'.join(nocon)), fcontexts)
                else:
                    contest = j.greps(j.fl('^/' + extractdir, '.* \?$|.*:' + j.greps(
                        '^/' + extractdir + ' ', fcontexts)[0].split()[1].split(':')[2]), fcontexts)
            except:
                contest = j.greps(
                    j.fl('^/' + extractdir, '.* \?$|.*:' + extractdir + '_file'), fcontexts)

        filec = []
        for i in contest:
            i = i.replace('\t', ' ').replace('--', '').replace('/', dirr, 1)
            if f3:
                if not j.greps(i.split()[0] + ' |' + i.split()[0] + ' -R$', metalist):
                    metalist.append(i.split()[0])
            else:
                try:
                    cexc = i.split()[1]
                except:
                    continue

                for cexf in j.greps(i.split()[0], filerd):
                    filec.append(cexf + ' ' + cexc)

        if f3:
            filec = fcontexts

        # Remove duplicates and sort metalist
        metalist = sorted(list(set(metalist)))
        newmlist = []

        for i in metalist:
            if not i:
                continue
            i = i.replace('\\', '/')
            i2 = i.replace(' -R', '')
            if dirr:
                i2 = i2.replace(dirr, '', 1)

            a = None
            try:
                a = j.greps('.*' + i2 + ' ', filer)[0]
            except:
                pass

            if a:
                if len(a.split()) >= 4:
                    if len(a.split()[1]) > 4:
                        cyuid = a.split()[1][1:]
                        cygid = a.split()[2][1:]
                        cymode = a.split()[3][1:]
                    else:
                        cyuid = a.split()[1]
                        cygid = a.split()[2]
                        cymode = a.split()[3]
                else:
                    cyuid = '0'
                    cygid = '0'
                    cymode = '0755'

                capta = j.greps('.*' + i2 + ' ', capfiles)
                if capta:
                    if len(capta[0].split()) < 4:
                        cap = capta[0].split()[1]
                    else:
                        cap = str(hex(int(capta[0].split('=')[1])))
                else:
                    cap = '0x0'

                try:
                    cycon = j.greps('.*' + i2 + ' ', filec)[0].split()[1]
                    if cycon == '?':
                        cycon = 'u:object_r:' + extractdir + '_file:s0'
                except:
                    cycon = 'u:object_r:' + extractdir + '_file:s0'

                if i.endswith('-R'):
                    if i2.endswith('/bin') or '/bin/' in i2:
                        fmode = '0755'
                    else:
                        fmode = '0644'

                    newmlist.append(
                        'set_metadata_recursive("/' + dirr + i2
                        + '", "uid", ' + cyuid + ', "gid", ' + cygid
                        + ', "dmode", ' + cymode + ', "fmode", ' + fmode + ', "capabilities", ' + cap
                        + ', "selabel", "' + cycon + '");')
                else:
                    newmlist.append(
                        'set_metadata("/' + dirr + i2 + '", "uid", '
                        + cyuid + ', "gid", ' + cygid
                        + ', "mode", ' + cymode + ', "capabilities", ' + cap
                        + ', "selabel", "' + cycon + '");')

        newmlist = j.greps(j.fl('', '\.*"\?"'), newmlist)
        j.appendf('\n'.join(newmlist), j.prfiles + '/' + set_metadata1)

    def misc_tools():
        global main
        choice = ''
        while not choice:
            heapsize = j.get_heapsize()
            if not j.getconf('heapsize', j.mconf):
                heapstatus = heapsize + 'MB ' + j.lang['heapsize_auto']
            else:
                heapstatus = heapsize + 'MB ' + j.lang['menu_cust_dir']

            language = j.getconf('language', j.mconf)
            if language:
                language = color['g'] + language
            else:
                language = color['r'] + j.lang['error']

            j.banner()
            j.kprint(j.lang['startup_project'] + color['g'] + j.romname, 'b')
            if j.existf(j.sysdir + '/build.prop'):
                j.kprint(j.lang['startup_version']
                         + color['g'] + j.androidversion, 'b')
            else:
                j.kprint(j.lang['startup_version'] + color['r']
                         + j.lang['startup_title_no_rom'], 'b')

            print()
            j.kprint(j.lang['title_misc'] + '\n', 'ryb')
            print('1) ' + j.lang['menu_offline_auth'] + ' (' + color['b']
                  + j.lang['expires'] + color['g'] + j.days_left.split('-')[0] + color['n'] + ')')
            print('2) ' + j.lang['menu_language'] + ' (' + color['b']
                  + j.lang['title_current'] + language + color['n'] + ')')
            print('3) ' + j.lang['menu_heapsize'] + ' (' + color['b']
                  + j.lang['title_current'] + color['g'] + heapstatus + color['n'] + ')')
            print('4) ' + j.lang['menu_support'])
            print('5) ' + j.lang['menu_extract_options'])
            print('6) ' + j.lang['menu_tools_reset'])
            print('7) ' + j.lang['menu_flashable'])
            print('8) ' + j.lang['menu_device_reset'])
            j.kprint('m = ' + j.lang['title_main'], 'y')
            j.kprint('q = ' + j.lang['menu_quit'] + '\n', 'm')
            print(j.lang['select'])
            choice = j.getChar()

            if choice.isnumeric():
                if choice < '1' or choice > '8':
                    choice = ''
                    continue
            elif choice not in ['m', 'q']:
                choice = ''
                continue

            if choice == 'q':  # START Quit
                sys.exit()
            elif choice == 'm':  # START Main menu
                main = 1
                return

            if choice == '1':  # START Offline Authorization Menu
                choice2 = ''
                while not choice2:
                    offline_status = color['g'] + j.lang['enabled']
                    cnt = '1'
                    j.banner()
                    j.kprint(j.lang['menu_offline_auth'] + '\n', 'ryb')
                    j.kprint(j.lang['auth_max_days']
                             + str(j.auth_days) + '\n', 'y')
                    print('1) ' + j.lang['menu_offline_enable'] + ' (' + color['b']
                          + j.lang['title_current'] + offline_status + color['n'] + ')')
                    cnt = '2'
                    print('2) ' + j.lang['menu_offline_renew'] + ' (' + color['b']
                              + j.lang['expires'] + color['g']
                              + j.days_left.split('-')[0] + color['n'] + ')')

                    j.kprint('b = ' + j.lang['menu_back'] + '\n', 'y')
                    print(j.lang['select'])
                    choice2 = j.getChar()

                    if choice2.isnumeric():
                        if choice2 < '1' or choice2 > cnt:
                            choice2 = ''
                            continue
                    elif choice2 not in ['b']:
                        choice2 = ''
                        continue

                    if choice2 == 'b':
                        choice = ''
                    elif choice2 == '1':
                        j.delpath(j.tools + '/auth.key')
                        j.days_left = color['r'] + j.lang['disabled']
                        j.getconf('offline_auth', j.mconf, 'rem')



                        choice2 = ''
                    elif choice2 == '2':
                        j.banner()
                        j.delpath(j.tools + '/auth.key')
                        j.kprint(j.lang['auth_reset'], 'g')
                        j.kprint(j.lang['auth_reset2'] + '\n', 'y')
                        input(j.lang['enter_continue'])
                        sys.exit(3)
            elif choice == '2':  # START Reset Languages
                j.getconf('language', j.mconf, 'rem')
                j.banner()
                j.kprint(j.lang['reset_language'] + '\n', 'g')
                input(j.lang['enter_continue'])
                sys.exit(3)
            elif choice == '3':  # START Use custom heapsize for java apps
                choice2 = ''
                while not choice2:
                    j.banner()
                    j.kprint(j.lang['heapsize_choose'] + '\n', 'ryb')
                    print('1) ' + j.lang['heapsize_custom'] + ' (' + color['b']
                          + j.lang['title_current'] + color['g'] + heapstatus + color['n'] + ')')
                    print('2) ' + j.lang['heapsize_reset'])
                    j.kprint('b = ' + j.lang['menu_back'] + '\n', 'y')
                    print(j.lang['select'])
                    choice2 = j.getChar()

                    if choice2.isnumeric():
                        if choice2 < '1' or choice2 > '2':
                            choice2 = ''
                            continue
                    elif choice2 not in ['b']:
                        choice2 = ''
                        continue

                    if choice2 == 'b':
                        break
                    elif choice2 == '1':
                        j.banner()
                        totalmem = j.virtual_memory() - 500

                        print(j.lang['heapsize_q'])
                        j.kprint(j.lang['heapsize_q2']
                                 + color['y'] + str(totalmem))
                        reply = input()
                        if reply.isnumeric():
                            if int(reply) > totalmem:
                                j.banner()
                                j.kprint(j.lang['error'], 'yrbbo')
                                j.kprint(j.lang['heapsize_error'], 'r')
                                j.kprint(j.lang['heapsize_error2'] + '\n', 'r')
                                j.kprint(j.lang['physical_ram']
                                         + str(totalmem) + '\n', 'y')
                                input(j.lang['enter_heapsize_menu'])
                                choice2 = ''
                                continue

                            j.getconf('heapsize', j.mconf, add=reply)
                        else:
                            j.banner()
                            j.kprint(j.lang['error'], 'yrbbo')
                            j.kprint(j.lang['heapsize_num_error'] + '\n', 'r')
                            input(j.lang['enter_heapsize_menu'])
                            choice2 = ''
                            continue

                    elif choice2 == '2':
                        j.getconf('heapsize', j.mconf, 'rem')

                choice = ''
                continue
            elif choice == '4':  # START Support: Create zip to send
                if not j.getconf('xdauser', j.mconf):
                    j.banner()
                    print(j.lang['xdauser_q'])
                    j.getconf('xdauser', j.mconf,
                              add=input().replace(' ', '_') or 'guest')

                xdauser = j.getconf('xdauser', j.mconf)
                j.banner()
                j.kprint(j.lang['support_create'], 'b')
                j.delpath(j.rd + '/support.zip')
                j.mkdir(j.rd + '/srk_support_zip')
                srksupf = j.rd + '/srk_support_zip/info'
                srksupd = j.rd + '/srk_support_zip'
                j.appendf(j.platf, srksupf)
                j.appendf(j.osbit(), srksupf)
                j.appendf(j.superrv, srksupf)
                j.appendf('\n'.join(j.greps(j.fl('', '.*srkpass'),
                                            j.readfl(j.tools + '/srk.conf'))), srksupd + '/srk_m.conf')

                if j.existf(j.tools + '/auth.key'):
                    copyfile(j.tools + '/auth.key', srksupd + '/auth.key')

                with j.cd(j.prfiles):
                    copyfile('srk.conf', srksupd + '/srk_u.conf')
                    j.cpdir('logs', srksupd + '/logs')
                    for i in glob.glob('deodex_*'):
                        j.appendf(i, srksupf)

                if j.existd(j.rd + '/META-INF'):
                    j.cpdir(j.rd + '/META-INF', srksupd + '/META-INF')

                if j.existf(j.sysdir + '/build.prop'):
                    copyfile(j.sysdir + '/build.prop', srksupd + '/build.prop')
                    devicename = j.get_devicename()
                    if devicename:
                        if j.existd(j.tools + '/devices/' + devicename):
                            j.cpdir(j.tools + '/devices/' + devicename,
                                    srksupd + '/' + devicename)

                with j.cd(srksupd):
                    upname = 'support_' + xdauser + '_' + j.timest() + '.zip'
                    j.appendf(j.zipp(upname, glob.glob('*')), j.logs + '/zip.log')
                    j.banner()
                    print(j.lang['support_upload'])
                    reply = j.getChar()
                    if reply == 'y':
                        if srkup(upname) == 1:
                            j.banner()
                            j.kprint(j.lang['error'], 'yrbbo')
                            j.kprint(j.lang['error_mess'], 'r')
                        else:
                            j.banner()
                            j.kprint(j.lang['support_finish_up'], 'g')
                    else:
                        os.replace(upname, j.rd + '/' + upname)
                        j.banner()
                        j.kprint(j.lang['support_finish'], 'g')

                print()
                input(j.lang['enter_misc_tools_menu'])
                j.delpath(srksupd)
                choice = ''
                continue
            elif choice == '5':  # START Mount img files to extract
                choice2 = ''
                while not choice2:
                    mountstatus = j.getconf('mount_extract', j.mconf)
                    if mountstatus == 'Yes':
                        mountstatus = color['g'] + j.lang['yes']
                    else:
                        mountstatus = color['r'] + j.lang['no']

                    casestatus = j.getconf('case_fix', j.mconf)
                    if casestatus == 'Yes':
                        casestatus = color['g'] + j.lang['yes']
                    else:
                        casestatus = color['r'] + j.lang['no']

                    imgstatus = j.getconf('extract_all_img', j.mconf)
                    if imgstatus == 'Yes':
                        imgstatus = color['g'] + j.lang['yes']
                    else:
                        imgstatus = color['r'] + j.lang['no']

                    j.banner()
                    j.kprint(j.lang['menu_extract_options'] + '\n', 'ryb')
                    j.kprint('1) ' + j.lang['menu_mount_extract'] + ' (' + color['b']
                             + j.lang['title_current']
                             + color['g'] + mountstatus + color['n']
                             + ')', ('r' if j.platf == 'wsl' else 'n'))
                    print('2) ' + j.lang['menu_case_fix'] + ' (' + color['b']
                          + j.lang['title_current'] + color['g'] + casestatus + color['n'] + ')')
                    print('3) ' + j.lang['menu_extract_all_img'] + ' (' + color['b']
                          + j.lang['title_current'] + color['g'] + imgstatus + color['n'] + ')')
                    j.kprint('b = ' + j.lang['menu_back'] + '\n', 'y')
                    print(j.lang['select'])
                    choice2 = j.getChar()

                    if choice2.isnumeric():
                        if choice2 < '1' or choice2 > '3':
                            choice2 = ''
                            continue
                    elif choice2 not in ['b']:
                        choice2 = ''
                        continue

                    if choice2 == 'b':
                        break
                    elif choice2 == '1':
                        if j.platf == 'wsl':
                            choice2 = ''
                            continue

                        if mountstatus.endswith(j.lang['yes']):
                            j.getconf('mount_extract', j.mconf, add='No')
                        else:
                            j.getconf('mount_extract', j.mconf, add='Yes')
                    elif choice2 == '2':
                        if casestatus.endswith(j.lang['yes']):
                            j.getconf('case_fix', j.mconf, add='No')
                        else:
                            j.getconf('case_fix', j.mconf, add='Yes')
                    elif choice2 == '3':
                        if imgstatus.endswith(j.lang['yes']):
                            j.getconf('extract_all_img', j.mconf, add='No')
                        else:
                            j.getconf('extract_all_img', j.mconf, add='Yes')

                    choice2 = ''
                    continue

                choice = ''
                continue
            elif choice == '6':  # START Reset all tools
                j.banner()
                j.kprint(j.lang['update_updating'], 'b')
                get_tools()

                choice = ''
                continue
            elif choice == '7':  # START flashable zip options
                choice2 = ''
                while not choice2:
                    j.banner()
                    j.kprint(j.lang['menu_flashable'] + '\n', 'ryb')
                    print('1) ' + j.lang['metasize'] + '(' + color['b'] + j.lang['title_current'] + color['g'] + (
                            j.getconf('metasize', j.mconf) or j.lang['metasize_s']) + color['n'] + ')')
                    print('2) ' + j.lang['menu_zip_compression']
                          + '(' + color['b'] + j.lang['title_current']
                          + color['g'] + (j.getconf('rom_comp_level',
                                                    j.mconf) or '5') + color['n'] + ')')
                    print('3) ' + j.lang['menu_ubinary'])
                    print('4) ' + j.lang['brotli_menu'])
                    j.kprint('b = ' + j.lang['menu_back'], 'y')
                    j.kprint('q = ' + j.lang['menu_quit'] + '\n', 'm')
                    print(j.lang['select'])
                    choice2 = j.getChar()

                    if choice2.isnumeric():
                        if choice2 < '1' or choice2 > '4':
                            choice2 = ''
                            continue
                    elif choice2 not in ['b', 'q']:
                        choice2 = ''
                        continue

                    if choice2 == 'q':  # START Quit
                        sys.exit()
                    elif choice2 == 'b':  # START Back
                        choice = ''
                    elif choice2 == '1':  # set_metadata short/long
                        choice3 = ''
                        while not choice3:
                            slstat = ''
                            if not j.getconf('metasize', j.mconf):
                                slstat = j.lang['metasize_s']
                            elif j.getconf('metasize', j.mconf) == 'Short':
                                slstat = j.lang['metasize_s']
                            elif j.getconf('metasize', j.mconf) == 'Long':
                                slstat = j.lang['metasize_l']

                            j.banner()
                            j.kprint(j.lang['title_current']
                                     + color['g'] + slstat + '\n', 'b')
                            j.kprint(j.lang['metasize_q'] + '\n', 'gb')
                            print('1) ' + j.lang['metasize_s'])
                            print('2) ' + j.lang['metasize_l'])
                            j.kprint('b = ' + j.lang['menu_back'] + '\n', 'y')
                            print(j.lang['select'])
                            choice3 = j.getChar()

                            if choice3.isnumeric():
                                if choice3 < '1' or choice3 > '2':
                                    choice3 = ''
                                    continue
                            elif choice3 not in ['q', 'b']:
                                choice3 = ''
                                continue
                            elif choice3 == 'b':
                                choice2, choice3 = '', ''
                                break

                            if choice3 == '1':
                                j.getconf('metasize', j.mconf, add='Short')
                                choice2 = ''
                            elif choice3 == '2':
                                j.getconf('metasize', j.mconf, add='Long')
                                choice2 = ''
                            else:
                                choice3 = ''
                    elif choice2 == '2':  # Start zip compression
                        while True:
                            j.banner()
                            print(j.lang['menu_zip_compression2']
                                  + '(0,1,3,5,7,9):')

                            comp7 = j.getChar()
                            if comp7 not in ['0', '1', '3', '5', '7', '9']:
                                continue

                            j.getconf('rom_comp_level', j.mconf, add=comp7)

                            choice2 = ''
                            break
                    elif choice2 == '3':  # update-binary options
                        choice3 = ''
                        while not choice3:
                            ubstat = ''
                            if not j.getconf('ubinary', j.mconf):
                                ubstat = j.lang['ask_s']
                            elif j.getconf('ubinary', j.mconf) == 'no':
                                ubstat = j.lang['never_s']
                            elif j.getconf('ubinary', j.mconf) == 'yes':
                                ubstat = j.lang['always_s']

                            j.banner()
                            j.kprint(j.lang['menu_ubinary'] + '\n', 'ryb')
                            j.kprint(j.lang['title_current']
                                     + color['g'] + ubstat + '\n', 'b')
                            print('1) ' + j.lang['ask_b'])
                            print('2) ' + j.lang['always_b'])
                            print('3) ' + j.lang['never_b'])
                            j.kprint('b = ' + j.lang['menu_back'], 'y')
                            j.kprint('q = ' + j.lang['menu_quit'] + '\n', 'm')
                            print(j.lang['select'])
                            choice3 = j.getChar()

                            if choice3.isnumeric():
                                if choice3 < '1' or choice3 > '3':
                                    choice3 = ''
                                    continue
                            elif choice3 not in ['b', 'q']:
                                choice3 = ''
                                continue

                            if choice3 == 'q':  # START Quit
                                sys.exit()
                            elif choice3 == 'b':  # START Back
                                choice2 = ''
                            elif choice3 == '1':  # Ask every time
                                j.getconf('ubinary', j.mconf, 'rem')
                                choice3 = ''
                                continue
                            elif choice3 == '2':  # Always convert
                                j.getconf('ubinary', j.mconf, add='yes')
                                choice3 = ''
                                continue
                            elif choice3 == '3':  # Never convert
                                j.getconf('ubinary', j.mconf, add='no')
                                choice3 = ''
                                continue
                    elif choice2 == '4':  # Brotli compression for sparse_dat
                        choice3 = ''
                        while not choice3:
                            j.banner()
                            if not j.getconf('brotli_comp', j.mconf):
                                slstat = ''
                                j.kprint(j.lang['title_current']
                                         + color['r'] + j.lang['disabled'], 'b')
                            else:
                                slstat = j.getconf('brotli_comp', j.mconf)
                                j.kprint(j.lang['title_current']
                                         + color['g'] + slstat, 'b')

                            print()
                            j.kprint(j.lang['brotli_q'] + '\n', 'gb')
                            print('1) ' + j.lang['yes'])
                            print('2) ' + j.lang['no'])
                            j.kprint('b = ' + j.lang['menu_back'] + '\n', 'y')
                            print(j.lang['select'])
                            choice3 = j.getChar()

                            if choice3.isnumeric():
                                if choice3 < '1' or choice3 > '2':
                                    choice3 = ''
                                    continue
                            elif choice3 not in ['q', 'b']:
                                choice3 = ''
                                continue
                            elif choice3 == 'b':
                                choice2, choice3 = '', ''
                                break

                            if choice3 == '1':
                                while True:
                                    j.banner()
                                    print(j.lang['brotli_level'] + '(0-9):')

                                    comp7 = j.getChar()
                                    if comp7.isnumeric() and comp7 <= '9':
                                        j.getconf('brotli_comp',
                                                  j.mconf, add=comp7)
                                    else:
                                        continue

                                    choice2 = ''
                                    break
                            elif choice3 == '2':
                                j.getconf('brotli_comp', j.mconf, 'rem')

                            choice3 = ''
            elif choice == '8':  # START Update device database
                with j.cd(j.tools):
                    j.delpath('devices')
                j.banner()
                j.kprint(j.lang['menu_tools_update'] + '\n', 'g')
                input(j.lang['enter_continue'])
                sys.exit(3)

    def moveoldfiles(romzip, romtar, romimg, romdat):
        timestamp = j.timest()
        movetest = j.partslist + ['install', 'META-INF', 'supersu', 'rootzip', 'busybox',
                                  'gapps', 'xposed', 'magisk', 'mod', 'data', 'bootimg', 'recoveryimg']
        mvtmp = []
        for i in movetest:
            if j.existd(j.rd + '/' + i):
                mvtmp.append(i)
        if mvtmp:
            j.mkdir(j.prfiles + '/old_rom_files/' + j.romname
                    + '.' + timestamp + '/00_project_files')
            with j.cd(j.prfiles):
                prtmp = glob.glob('*')
                prtmp.remove('old_rom_files')
                for i in prtmp:
                    if j.existd(i):
                        j.mvdir(i, 'old_rom_files/' + j.romname + '.'
                                + timestamp + '/00_project_files/' + i)
                    else:
                        os.replace(i, 'old_rom_files/' + j.romname
                                   + '.' + timestamp + '/00_project_files/' + i)
                j.mkdir('logs')

            for i in mvtmp:
                j.mvdir(j.rd + '/' + i, j.prfiles + '/old_rom_files/'
                        + j.romname + '.' + timestamp + '/' + i)

            if romzip:
                ziptmp = ['boot.img', 'system.img.ext4', 'system.ext4', 'cache.img',
                          'cache.ext4', 'kernel.img', 'ramdisk.img'] + [x + '.img' for x in j.partslist]
                ztmp = []
                for i in ziptmp:
                    if j.greps(i, ziptmp) and j.existf(j.rd + '/' + i):
                        ztmp.append(i)

                if ztmp:
                    if not j.existd(j.prfiles + '/old_rom_files/' + j.romname + '.' + timestamp):
                        j.mkdir(j.prfiles + '/old_rom_files/'
                                + j.romname + '.' + timestamp)

                    for i in ztmp:
                        os.replace(j.rd + '/' + i, j.prfiles
                                   + '/old_rom_files/' + j.romname + '.' + timestamp + '/' + i)

            if j.existd(j.prfiles + '/old_rom_files/' + j.romname + '.' + timestamp):
                with j.cd(j.prfiles + '/old_rom_files/' + j.romname + '.' + timestamp):
                    movelist = os.listdir('.')
                j.banner()
                j.kprint(j.lang['extract_moved_old_rom'], 'b')
                j.kprint(j.prfiles + '/old_rom_files/'
                         + j.romname + '.' + timestamp + '\n', 'y')
                j.kprint(', '.join(movelist) + '\n', 'y')
                print(j.lang['enter_continue_extracting']
                      + ' ' + romzip + romtar + romimg + romdat + ' ...')
                input()

    def partadd(whatimg):
        whatimg2 = whatimg
        if '_exfiles' in whatimg:
            whatimg = whatimg.split('_', 1)[0]

        devicename = j.get_devicename()
        deviceloc = j.tools + os.sep + 'devices' + os.sep + devicename
        j.banner()
        j.kprint(j.lang['img_add'] + whatimg2 + ' ...', 'b')
        permtype = j.getconf('permtype', j.uconf)
        partbyname = ''
        if j.existf(deviceloc + '/superr_mmc') and j.grepf(whatimg, deviceloc + '/superr_mmc'):
            partbyname = j.grepf(whatimg, deviceloc
                                 + '/superr_mmc')[0].split()[0]
        else:
            partbyname = whatimg

        if partbyname:
            if permtype in ['sparse_dat', 'raw_img']:
                if not j.grepf('.*/tmp/config", "' + whatimg + '"', j.usdir + '/updater-script'):
                    j.awkadd('#MOUNT',
                             'ifelse(is_mounted("/' + whatimg + '"), "", mount("ext4", "EMMC", file_getprop("/tmp/config", "'
                             + whatimg + '"), "/' + whatimg + '"));', 'after', 'all', j.usdir + '/updater-script')

                    j.awkadd('#UNMOUNT', 'ifelse(is_mounted("/' + whatimg + '"), unmount("/'
                             + whatimg + '"));', 'after', 'all', j.usdir + '/updater-script')

                if whatimg in j.getconf('exdirs', j.uconf, l=1):
                    partup = whatimg.upper()
                    if not j.grepf('#' + partup, j.usdir + '/updater-script'):
                        if permtype == 'sparse_dat':
                            j.awkadd('block_image_update\(.*', '#' + partup,
                                     'after', 'first', j.usdir + '/updater-script')
                        else:
                            j.awkadd('.*system_new.*', '#' + partup,
                                     'after', 'first', j.usdir + '/updater-script')

                    j.sedf('#' + partup, j.readf(j.tools + '/updater/extra-'
                                                 + permtype + '.txt'), j.usdir + '/updater-script')
                    j.sedf('#PEXTRA', whatimg, j.usdir + '/updater-script')
                elif whatimg == 'data':
                    if permtype == 'sparse_dat':
                        j.awkadd('block_image_update\(.*', '#DATA',
                                 'after', 'first', j.usdir + '/updater-script')
                    else:
                        j.awkadd('.*system_new.*', '#DATA', 'after',
                                 'first', j.usdir + '/updater-script')

                    choice2 = ''
                    while not choice2:
                        j.banner()
                        j.kprint(j.lang['extra_data'] + '\n', 'ryb')
                        print('1) ' + permtype)
                        print('2) set_metadata\n')
                        print(j.lang['extra_data_perm'])
                        choice2 = j.getChar()

                        if choice2.isnumeric():
                            if choice2 < '1' or choice2 > '2':
                                continue
                        else:
                            continue

                        if choice2 == '1':  # START sparse_dat/raw_img data
                            j.sedf('#DATA', j.readf(
                                j.tools + '/updater/data-' + permtype + '.txt'), j.usdir + '/updater-script')
                            j.getconf('data-' + permtype, j.uconf, add='1')
                        elif choice2 == '2':  # START metadata data
                            j.sedf('#DATA', j.readf(
                                j.tools + '/updater/data-set_metadata.txt'), j.usdir + '/updater-script')
                            j.getconf('data-set_metadata', j.uconf, add='1')
            else:
                if not j.grepf('.*/tmp/config", "' + whatimg + '"', j.usdir + '/updater-script'):
                    j.awkadd('#MOUNT',
                             'ifelse(is_mounted("/' + whatimg + '"), "", mount("ext4", "EMMC", file_getprop("/tmp/config", "'
                             + whatimg + '"), "/' + whatimg + '"));', 'after', 'all', j.usdir + '/updater-script')

                    j.awkadd('#UNMOUNT', 'ifelse(is_mounted("/' + whatimg + '"), unmount("/'
                             + whatimg + '"));', 'after', 'all', j.usdir + '/updater-script')

                    if whatimg != 'data':
                        j.awkadd('^format.*', '#FORMAT', 'after',
                                 'first', j.usdir + '/updater-script')
                        j.sedf('#FORMAT', 'format("ext4", "EMMC", file_getprop("/tmp/config", "'
                               + whatimg + '"), "0", "/' + whatimg + '");', j.usdir + '/updater-script')

                if whatimg in j.getconf('exdirs', j.uconf, l=1):
                    partup = whatimg.upper()
                    if not j.grepf('#' + partup, j.usdir + '/updater-script'):
                        j.awkadd('^package_extract_dir\("system".*', '#'
                                 + partup, 'after', 'first', j.usdir + '/updater-script')

                    if whatimg in ['vendor', 'oem', 'product']:
                        j.sedf('#' + partup, j.readf(j.tools
                                                     + '/updater/vendor-set_metadata.txt'), j.usdir + '/updater-script')
                    else:
                        j.sedf('#' + partup, j.readf(j.tools
                                                     + '/updater/extra-set_metadata.txt'), j.usdir + '/updater-script')
                    j.sedf('#PEXTRA', whatimg2, j.usdir + '/updater-script')

                    if whatimg in ['vendor', 'oem', 'product'] and j.existf(j.prfiles + '/set_metadataV'):
                        j.appendf(j.readf(j.prfiles + '/set_metadataV'),
                                  j.prfiles + '/set_metadata')

                elif whatimg == 'data':
                    j.awkadd('^package_extract_dir\("system".*', '#DATA',
                             'after', 'first', j.usdir + '/updater-script')
                    j.sedf('#DATA', j.readf(
                        j.tools + '/updater/data-set_metadata.txt'), j.usdir + '/updater-script')
                    j.getconf('data-set_metadata', j.uconf, add='1')

            if '_exfiles' in whatimg2 and permtype in ['set_metadata', 'set_perm']:
                if not j.grepf('#EXFILES', j.usdir + '/updater-script'):
                    j.awkadd('^package_extract_dir.*"system"', '#EXFILES',
                             'after', 'first', j.usdir + '/updater-script')

                    j.sedf('#EXFILES', j.readf(
                        j.tools + '/updater/custom_dir.txt'), j.usdir + '/updater-script')
                    j.sedf('#CUSDIR', whatimg2, j.usdir + '/updater-script')
                    if whatimg == 'system':
                        j.sedf(
                            '"/#CUSLOC"', 'file_getprop("/tmp/config", "sysmnt")', j.usdir + '/updater-script')

                    j.sedf('#CUSLOC', whatimg, j.usdir + '/updater-script')
        else:
            j.banner()
            j.kprint(j.lang['warning'] + '\n', 'yrbbo')
            j.kprint(j.lang['img_flash_fail'], 'r')
            j.kprint(j.lang['img_flash_fail2'] + whatimg + '\n', 'r')
            input(j.lang['enter_continue'])
            if whatimg == 'data':
                return 'needpart'
        return ''

    def part_setup(chosenimg=None):
        devicename = j.get_devicename()
        deviceloc = j.tools + os.sep + 'devices' + os.sep + devicename
        if j.existf(deviceloc + '/superr_mmc'):
            if chosenimg == 'recovery' and j.grepf(' /recovery', deviceloc + '/superr_mmc'):
                mmcrecovery = j.grepf(
                    ' /recovery', deviceloc + '/superr_mmc')[0].split(' ')[0]
                j.sedf('file_getprop\("/tmp/config", "recovery"\)',
                       mmcrecovery, j.usdir + '/updater-script')
            elif chosenimg == 'boot' and j.grepf(' /boot', deviceloc + '/superr_mmc'):
                mmcboot = j.grepf(' /boot$', deviceloc
                                  + '/superr_mmc')[0].split(' ')[0]
                j.sedf('file_getprop\("/tmp/config", "boot"\)',
                       mmcboot, j.usdir + '/updater-script')
            else:
                if (chosenimg == 'boot'
                        and (j.existf(j.rd + '/system/init.rc')
                             or j.existf(j.rd + '/system/init.environ.rc'))):
                    j.grepvf(' boot |boot.img', j.usdir + '/updater-script')
                else:
                    j.banner()
                    j.kprint(j.lang['warning'] + '\n', 'yrbbo')
                    j.kprint(j.lang['img_flash_failB'], 'r')
                    j.kprint(j.lang['img_flash_failB2'], 'r')
                    j.kprint(j.lang['img_flash_failB3'] + '\n', 'r')
                    input(j.lang['enter_continue'])

            mmcsystem = j.grepf(' /system', deviceloc
                                + '/superr_mmc')[0].split(' ')[0]
            j.sedf('file_getprop\("/tmp/config", "system"\)',
                   mmcsystem, j.usdir + '/updater-script')

    def plugins():
        if not j.romname:
            j.banner()
            j.kprint(j.lang['error'], 'yrbbo')
            j.kprint(j.lang['startup_no_projects'] + '\n', 'r')
            input(j.lang['enter_main_menu'])
            return

        choice = ''
        while not choice:
            j.timegt()

            with j.cd(j.tools + '/plugins'):
                plugins = sorted(j.greps(j.fl('', '.*\.zip$'), glob.glob('*')))
            j.banner()
            j.kprint(j.lang['menu_plugin_menu'] + '\n', 'gb')
            print('1) ' + j.lang['menu_plugin_run'])
            print('2) ' + j.lang['menu_plugin_install'])
            print('3) ' + j.lang['menu_plugin_delete'])
            print('4) ' + j.lang['menu_plugin_updates'])
            j.kprint('m = ' + j.lang['title_main'], 'y')
            j.kprint('q = ' + j.lang['menu_quit'] + '\n', 'm')
            print(j.lang['select'])
            choice = j.getChar()

            if choice.isnumeric():
                if choice < '1' or choice > '4':
                    choice = ''
                    continue
            elif choice not in ['m', 'q']:
                choice = ''
                continue

            if choice == 'q':  # START Quit
                sys.exit()
            elif choice == 'm':  # START Main menu
                return

            if choice in ['2', '4']:  # Get remote plugin list
                pluglist = j.plug_update(plugins, choice)
                if pluglist == 1:
                    j.banner()
                    j.kprint(j.lang['error'], 'yrbbo')
                    j.kprint(j.lang['donate_plugin_server'] + '\n', 'r')
                    input(j.lang['enter_continue'])
                    choice = ''
                    continue
                elif not pluglist:
                    j.banner()
                    j.kprint(j.lang['error'], 'yrbbo')
                    j.kprint(j.lang['donate_plugin_none'] + '\n', 'r')
                    input(j.lang['enter_continue'])
                    choice = ''
                    continue

            if choice == '1':  # START Run a plugin
                countplug = len(plugins)
                if countplug > 0:
                    plugin = j.chlist(
                        color['gb'] + j.lang['donate_plugin_cho'] + color['n'], plugins, countplug)
                    if not plugin:
                        choice = ''
                        continue
                else:
                    choice = ''
                    continue

                if (j.existf(j.tools + '/plugins/' + plugin + '/' + plugin)
                        or (j.existf(j.tools + '/plugins/' + plugin + '/' + plugin + '.py') and j.existf(
                            j.tools + '/source/superrl.py'))
                        or j.existf(j.tools + '/plugins/' + plugin + '/' + plugin + '.sh')
                        or j.existf(j.tools + '/plugins/' + plugin + '/' + plugin + '.bat')):

                    def plug_incompat():
                        j.banner()
                        j.kprint(j.lang['error'], 'yrbbo')
                        j.kprint(j.lang['donate_plugin_incompat'] + '\n', 'r')
                        input(j.lang['enter_plug_menu'])

                    j.clears()

                    try:
                        if j.existf(j.tools + '/plugins/' + plugin + '/' + plugin + '.py') and j.existf(
                                j.tools + '/source/superrl.py'):
                            sys.path.append(os.path.abspath(
                                j.tools + '/plugins/' + plugin))
                            theplug = __import__(plugin)
                            importlib.reload(theplug)

                            theplug.main(j, plugin)
                        elif j.existf(j.tools + '/plugins/' + plugin + '/' + plugin + '.sh'):
                            if j.platf in ['lin', 'mac', 'wsl', 'wsl2']:
                                os.system(j.tools + '/plugins/' + plugin + '/' + plugin + '.sh "' + j.bd
                                          + '" "' + j.ostools + '" "' + j.rd + '" "' + j.tools + '/plugins/' + plugin + '"')
                            else:
                                plug_incompat()
                        elif j.existf(j.tools + '/plugins/' + plugin + '/' + plugin + '.bat'):
                            plug_incompat()
                        else:
                            if j.grepf(' ', j.tools + '/plugins/' + plugin + '/' + plugin):
                                plug_incompat()
                            else:
                                theplug = imp.load_source('module', j.tools + '/plugins/' + plugin + '/' + plugin)
                                theplug.main(j, plugin)
                    except Exception as e:
                        j.appendf('ERROR ' + plugin + ':\n'
                                  + j.logtb(e), j.logs + '/plugin.log')
                        j.banner()
                        j.kprint(j.lang['donate_plugin_crash'] + plugin, 'r')
                        j.kprint(j.lang['donate_plugin_crash2'] + '\n', 'r')
                        input(j.lang['enter_continue'])

                else:
                    j.banner()
                    j.kprint(j.lang['error'], 'yrbbo')
                    j.kprint(j.lang['donate_plugin_error'], 'r')
                    j.kprint(j.lang['donate_plugin_error2'] + '\n', 'r')
                    j.kprint(j.lang['example'], 'gb')
                    j.kprint(
                        '/kitchen/tools/plugins/pluginname/pluginname.sh\n', 'y')

                    input(j.lang['enter_plug_menu'])

                choice = ''
                continue
            elif choice == '2':  # START Install a plugin`
                countplug = len(pluglist)
                if countplug >= 1:
                    plug = j.chlist(
                        color['gb'] + j.lang['donate_plugin_install_cho'] + color['n'], pluglist, countplug)
                    if not plug:
                        choice = ''
                        continue
                else:
                    choice = ''
                    continue

                j.banner()
                j.kprint(j.lang['tools_dl_install'], 'b')
                with j.cd(j.tools + '/plugins'):
                    j.dlfile(f'https://github.com/ColdWindScholar/superr_files/raw/plugin/{plug}.zip', plug + '.zip')
                    j.appendf(j.zipu(plug + '.zip'), j.logs + '/zip.log')
                    if not os.path.exists(plug + '/plugmd5'):
                        j.touch(plug + '/plugmd5')
                    j.appendf(j.md5chk(plug + '.zip'), plug + '/plugmd5')
                    j.delpath(plug + '.zip')

                choice = ''
                continue
            elif choice == '3':  # START Delete a plugin
                plugins2 = plugins
                for i in ['example_bash', 'example_batch', 'example_python']:
                    if i in plugins2:
                        plugins2.remove(i)

                countplug = len(plugins2)
                if countplug >= 1:
                    plugin = j.chlist(
                        color['rb'] + j.lang['donate_plugin_delete_cho'] + color['n'], plugins2, countplug)
                    if not plugin:
                        choice = ''
                        continue
                else:
                    choice = ''
                    continue

                j.delpath(j.tools + '/plugins/' + plugin)
                choice = ''
                continue
            elif choice == '4':  # START Check for plugin updates
                j.plug_update(plugins)
                choice = ''
                continue

    def pullimga(pullimg, byname):
        j.banner()
        j.kprint(j.lang['extract_pulling'] + pullimg + ' ...\n', 'b')

        j.appendf(j.cmd(j.adb + ' exec-out su -c "cat ' + byname
                        + '" > ' + j.rd + '/' + pullimg + '.img'), j.logs + '/adb.log')

        j.kprint(j.lang['extract_fix_img'] + pullimg + '.img ...', 'b')

        j.line_end(j.rd + '/' + pullimg + '.img', j.rd + '/' + pullimg + '.img2')

        if not j.existf(j.rd + os.sep + pullimg + '.img'):
            return 1
        else:
            return 0

    def pullimgr(pullimg, byname):
        j.banner()
        j.kprint(j.lang['extract_pulling'] + pullimg + ' ...\n', 'b')

        j.appendf(j.adb + ' pull ' + byname + ' ' + pullimg + '.img', j.logs + '/adb.log')
        j.appendf(j.cmd(j.adb + ' pull ' + byname + ' '
                        + pullimg + '.img'), j.logs + '/adb.log')

        if not j.existf(j.rd + os.sep + pullimg + '.img'):
            return 1
        else:
            return 0

    def rom_tools():
        global main, permtype
        main = 0
        while main == 0:
            j.timegt()

            if not j.existf(j.sysdir + '/build.prop'):
                j.banner()
                j.kprint(j.lang['error'], 'yrbbo')
                j.kprint(j.lang['startup_no_rom'] + '\n', 'r')
                input(j.lang['enter_main_menu'])
                return

            permtype = j.getconf('permtype', j.uconf)

            if not permtype:
                change_permtype()

            dstatus = j.isodexstatus()

            j.banner()
            j.kprint(j.lang['startup_project'] + color['g'] + j.romname, 'b')
            j.kprint(j.lang['startup_version']
                     + color['g'] + j.androidversion + '\n', 'b')
            j.kprint(j.lang['menu_rom_tools'] + '\n', 'ryb')
            print('1) ' + j.lang['menu_deodex'] + '(' + color['b']
                  + j.lang['title_current'] + dstatus + color['n'] + ')')
            print('2) ' + j.lang['menu_perm_type'] + '(' + color['b']
                  + j.lang['title_current'] + color['g'] + permtype + color['n'] + ')')
            j.kprint('3) ' + j.lang['menu_root'], 'y')
            j.kprint('4) ' + j.lang['menu_asserts'], 'y')
            j.kprint('5) ' + j.lang['menu_extra_dir'], 'y')
            j.kprint('6) ' + j.lang['menu_rom_debloat'], 'y')
            j.kprint('7) ' + j.lang['menu_build_menu'], 'y')
            j.kprint('m = ' + j.lang['title_main'], 'y')
            j.kprint('q = ' + j.lang['menu_quit'] + '\n', 'm')
            print(j.lang['select'])
            choice = j.getChar()

            if choice.isnumeric():
                if choice < '1' or choice > '7':
                    continue
            elif choice not in ['m', 'q']:
                continue

            if choice == 'q':  # START Quit
                sys.exit()
            elif choice == 'm':  # START Main menu
                main = 1
            elif choice == '1':  # START Deodex ROM
                j.deodex_start()
            # START Change perm type (set_perm/set_metadata)
            elif choice == '2':
                change_permtype()
            elif choice == '3':  # START Root Menu
                root_tools()
            elif choice == '4':  # START Asserts: Add/Change devices
                assert_devices()
            elif choice == '5':  # START Extra Directory Menu
                ext_dirmenu()
            elif choice == '6':  # START Debloat Menu
                debloat_rom()
            elif choice == '7':  # START Build Menu
                build_menu()

    def root():
        global main

        choice = None
        while not choice:
            if j.autorom():
                choice = j.getar('root_add')
                if not choice:
                    return
            else:
                j.banner()
                print(j.lang['menu_root_method'] + '\n')
                print('1) Magisk')
                print('2) SuperSU')
                print('3) Other')
                j.kprint('b = ' + j.lang['menu_back'], 'y')
                j.kprint('q = ' + j.lang['menu_quit'] + '\n', 'm')
                print(j.lang['select'])
                choice = j.getChar()

                if choice.isnumeric():
                    if choice < '1' or choice > '3':
                        choice = ''
                        continue
                elif choice not in ['q', 'b']:
                    choice = ''
                    continue
                elif choice == 'q':
                    sys.exit()
                elif choice == 'b':
                    return

            if choice == '1':
                rootver = 'Magisk'
            elif choice == '2':
                j.banner()
                j.kprint(j.lang['root_supersu_q'] + '\n', 'r')
                if j.getChar() != 'y':
                    choice = ''
                    continue

                rootver = 'SuperSU'
            elif choice == '3':
                rootver = 'Other'

        with j.cd(j.tools + '/root/root_zips'):
            if rootver == 'Other':
                rootzip = j.greps(
                    j.fl('', '.*SuperSU|.*Magisk'), glob.glob('*.zip'))
            else:
                rootzip = glob.glob('*' + rootver + '*.zip')

            if not rootzip:
                j.banner()
                if rootver == 'Other':
                    j.kprint('No root zips found\n', 'r')
                    input(j.lang['enter_root_menu'])
                    return

                j.kprint(j.lang['tools_dl'] + rootver + '.zip ...', 'b')

                if rootver == 'SuperSU':
                    rootdl = 'http://download.chainfire.eu/1220/SuperSU/SR5-SuperSU-v2.82-SR5-20171001224502.zip?retrieve_file=1'
                elif rootver == 'Magisk':
                    rootdl = 'https://github.com' + j.greps('.*Magisk-v', j.internet(
                        'https://github.com/topjohnwu/Magisk/releases', 1).splitlines())[0].split('"')[1]

                success = ''
                while not success:
                    j.dlfile(rootdl, rootver + '.zip')
                    try:
                        j.zipl(rootver + '.zip')
                        success = 1
                    except:
                        j.delpath(rootver + '.zip')

                rootzip = glob.glob('*' + rootver + '*.zip')

        if len(rootzip) == 1:
            rootzip = rootzip[0]
        else:
            rootzip = j.chlist(
                color['gb'] + j.lang['title_cho_root_zip'] + color['n'], rootzip, len(rootzip))

        if not rootzip:
            main = 1
            return

        zippath = j.tools + '/root/root_zips/' + rootzip

        if rootver == 'SuperSU':
            stest = j.getprop('ro.product.manufacturer')

            if api >= '23' or (j.androidversion == '5.1.1' and stest == 'samsung'):
                choice = ''
                while not choice:
                    rcnt = '2'
                    if j.autorom():
                        choice = j.getar('ss_type')
                        if not choice:
                            choice = '1'
                    else:
                        j.banner()
                        print(j.lang['menu_ss_method'] + '\n')
                        print('1) ' + j.lang['menu_supersucho'])
                        print('2) ' + j.lang['menu_system_install'])
                        if j.platf == 'lin':
                            rcnt = '3'
                            if j.existd(j.tools + '/inject-sepolicy'):
                                print('3) ' + j.lang['menu_inject'])
                            else:
                                print('3) ' + j.lang['menu_download_inject'])

                        j.kprint('b = ' + j.lang['menu_back'], 'y')
                        j.kprint('q = ' + j.lang['menu_quit'] + '\n', 'm')
                        print(j.lang['select'])
                        choice = j.getChar()

                    if choice.isnumeric():
                        if choice < '1' or choice > rcnt:
                            continue
                    elif choice not in ['q', 'b']:
                        continue

                    if choice == 'q':
                        sys.exit()
                    elif choice == 'b':
                        return
                    elif choice == '2':
                        j.appendf('SYSTEMLESS=false', j.sysdir + '/.supersu')
                    elif choice == '3':
                        if not j.existd(j.tools + '/inject-sepolicy'):
                            with j.cd(j.tools):
                                j.dlfile(
                                    'https://bitbucket.org/superr/superrs-kitchen/downloads/inject-sepolicy-addon.zip',
                                    'inject-sepolicy-addon.zip')
                                j.appendf(
                                    j.zipu('inject-sepolicy-addon.zip'), j.logs + '/zip.log')
                                j.delpath('inject-sepolicy-addon.zip')
                            with j.cd(j.tools + '/inject-sepolicy'):
                                j.cmd('chmod a+x inject sepolicy-inject')

                        j.appendf('SYSTEMLESS=false', j.sysdir + '/.supersu')
                        if not j.existd(j.rd + '/bootimg'):
                            j.boot_unpack('boot', 'boot.img', '1')

                        with j.cd(j.tools + '/inject-sepolicy'):
                            os.system('./inject ' + j.bd + ' ' + j.romname)

                        j.boot_pack('boot', 'boot.img', '1')

        with j.cd(j.usdir):
            if not j.grepf('#ROOT', 'updater-script'):
                if j.grepf('^package_extract_file', 'updater-script'):
                    j.awkadd('package_extract_file', '#ROOT',
                             'after', 'last', 'updater-script')

            reptxt = j.readf(j.tools + '/root/root_prog')
            j.awkadd('#ROOT', reptxt, 'after', 'last', 'updater-script')
            j.sedf('#ROOTZIP', rootzip, 'updater-script')

        j.mkdir(j.rd + '/rootzip')
        copyfile(zippath, j.rd + '/rootzip/' + rootzip)

    def rootrem():
        j.banner()
        j.kprint(j.lang['root_remove'], 'b')

        j.delpath(j.sysdir + '/.supersu')
        j.getconf('root_existing', j.uconf, 'rem')

        testf = {
            j.prfiles + '/boot.noroot': j.rd + '/boot.img',
            j.sysdir + '/bin/install-recovery_original.sh': j.sysdir + '/bin/install-recovery.sh',
            j.sysdir + '/etc/install-recovery_original.sh': j.sysdir + '/etc/install-recovery.sh',
            j.sysdir + '/bin/install-recovery.sh-ku.bak': j.sysdir + '/bin/install-recovery.sh',
            j.sysdir + '/etc/install-recovery.sh-ku.bak': j.sysdir + '/etc/install-recovery.sh',
            j.sysdir + '/bin/debuggerd_real': j.sysdir + '/bin/debuggerd',
            j.sysdir + '/bin/app_process_original': j.sysdir + '/bin/app_process',
            j.sysdir + '/bin/app_process32_original': j.sysdir + '/bin/app_process32',
            j.sysdir + '/bin/app_process64_original': j.sysdir + '/bin/app_process64',
            j.sysdir + '/bin/app_process.orig': j.sysdir + '/bin/app_process',
            j.sysdir + '/bin/app_process32.orig': j.sysdir + '/bin/app_process32',
            j.sysdir + '/bin/app_process64.orig': j.sysdir + '/bin/app_process64'
        }

        for i in list(testf):
            if j.existf(i):
                os.replace(i, testf[i])

        testf = [j.sysdir + '/bin/install-recovery.sh',
                 j.sysdir + '/etc/install-recovery.sh']
        for i in testf:
            if j.existf(i) and j.grepf('.*xbin', i):
                j.delpath(i)
                for x in glob.glob(j.prfiles + '/symlinks-*'):
                    j.grepvf('/'.join(i.split('/')[-3:]), x)

        if j.existf(j.prfiles + '/symunroot'):
            j.appendff(j.prfiles + '/symunroot', j.prfiles + '/symlinks-system')

        for line in j.readfl(j.tools + '/root/root_files'):
            for i in [j.usdir + '/updater-script'] + glob.glob(j.prfiles + '/symlinks*'):
                newscript = []
                for x in j.readfl(i):
                    if i.endswith('updater-script') and line == 'busybox':
                        if line in x:
                            if any(['configure.sh' in x, 'backuptool.sh' in x]):
                                newscript.append(x)
                        else:
                            newscript.append(x)
                    else:
                        if line not in x:
                            newscript.append(x)

                j.delpath(i)
                j.appendf('\n'.join(newscript), i)

            if permtype != 'sparse_dat' and permtype != 'raw_img':
                j.grepvf('.*' + line, j.prfiles + '/' + permtype)

            with j.cd(j.rd):
                line2 = line.strip()
                filetest = j.findr('**/' + line2)
                if filetest:
                    for line3 in filetest:
                        if line3.startswith('install') or line3.startswith('00_project_files'):
                            continue

                        j.delpath(line3)

    def root_busybox():
        bbpath = glob.glob(j.tools + '/root/busybox/*.zip')
        if not bbpath:
            with j.cd(j.tools + '/root/busybox'):
                j.banner()
                j.kprint(j.lang['tools_dl'] + 'Busybox.zip ...', 'b')
                try:
                    bbdl = j.internet(
                        'https://forum.xda-developers.com/t/tools-zips-scripts-osm0sis-odds-and-ends-multiple-devices-platforms.2239421/',
                        1).splitlines()

                    bbdl = j.greps(
                        'attachments/update-busybox-installer', bbdl)[0].split('"')[3]

                    j.dlfile(bbdl, 'Busybox.zip')
                except IndexError:
                    pass

            bbpath = glob.glob(j.tools + '/root/busybox/*.zip')

        with j.cd(j.usdir):
            if bbpath:
                busybox = os.path.basename(bbpath[0])
                if not j.grepf('^#BUSYBOX', 'updater-script'):
                    j.awkadd('#ROOT', '#BUSYBOX', 'after',
                             'last', 'updater-script')
                reptxt = j.readf(j.tools + '/root/busybox_prog')
                j.awkadd('#BUSYBOX', reptxt, 'after', 'last', 'updater-script')
                j.sedf('#BUSYBOX1', busybox, 'updater-script')
                j.mkdir(j.rd + '/busybox')
                copyfile(bbpath[0], j.rd + '/busybox/' + busybox)
            else:
                j.banner()
                j.kprint(j.lang['error'], 'yrbbo')
                j.kprint(j.lang['tools_dl_failed'] + '\n', 'r')
                input(j.lang['enter_continue'])
                return

    def root_busyboxrem():
        with j.cd(j.usdir):
            j.grepvf('Busybox|/tmp/busybox', 'updater-script')
            j.delpath(j.rd + '/busybox', j.rd + '/system/xbin/busybox')

    def root_sud():
        j.mkdir(j.sysdir + '/su.d')
        j.sedf('#ROOT', '#SUD\n#ROOT', j.usdir + '/updater-script')

        if j.sar():
            reptxt = j.readf(j.tools + '/boot/sud_perms2')
        else:
            reptxt = j.readf(j.tools + '/boot/sud_perms')

        j.awkadd('#SUD', reptxt, 'after', 'last', j.usdir + '/updater-script')

    def root_sudrem():
        j.delpath(j.rd + '/system/su.d')
        j.grepvf('#SUD|su.d', j.usdir + '/updater-script')

    def root_tools():
        global main
        main = 0
        while main == 0:
            j.banner()
            j.kprint(j.lang['startup_project'] + color['g'] + j.romname, 'b')
            j.kprint(j.lang['startup_version']
                     + color['g'] + j.androidversion + '\n', 'b')
            j.kprint(j.lang['menu_root'] + '\n', 'ryb')
            print('1) ' + j.lang['menu_root_unroot'] + ' (' + color['b']
                  + j.lang['title_current'] + color['g'] + isrootstatus() + color['n'] + ')')
            print('2) ' + j.lang['menu_busybox'] + ' (' + color['b']
                  + j.lang['title_current'] + color['g'] + isbusyboxstatus() + color['n'] + ')')
            print('3) ' + j.lang['menu_add_remove_sud'] + ' ('
                  + color['b'] + j.lang['title_current'] + issud() + color['n'] + ')')
            j.kprint('4) ' + j.lang['menu_rom_tools'], 'y')
            j.kprint('m = ' + j.lang['title_main'], 'y')
            j.kprint('q = ' + j.lang['menu_quit'] + '\n', 'm')
            print(j.lang['select'])
            choice = j.getChar()

            if choice.isnumeric():
                if choice < '1' or choice > '4':
                    continue
            elif choice not in ['m', 'q']:
                continue

            if choice == 'q':
                sys.exit()
            elif choice == 'm':  # START Main menu
                main = 1
            elif choice == '1':  # START Root/Unroot ROM
                if not j.getconf('root', j.uconf):
                    root()
                else:
                    j.banner()
                    j.kprint(j.lang['root_already'] + '\n', 'g')
                    print(j.lang['general_remove_q'])
                    reply = j.getChar()
                    if reply == 'y':
                        rootrem()
                        update_project()
                continue
            elif choice == '2':  # START Busybox Add/Remove
                if not j.getconf('busybox', j.uconf):
                    if j.getconf('root', j.uconf):
                        j.banner()
                        print(j.lang['busybox_q'])
                        reply = j.getChar()
                        if reply == 'y':
                            root_busybox()
                    else:
                        j.banner()
                        j.kprint(j.lang['error'], 'yrbbo')
                        j.kprint(j.lang['root_must_add'] + '\n', 'r')
                        input(j.lang['enter_root_menu'])
                        continue
                else:
                    j.banner()
                    j.kprint(j.lang['busybox_already'] + '\n', 'g')
                    print(j.lang['general_remove_q'])
                    reply = j.getChar()
                    if reply == 'y':
                        root_busyboxrem()
                continue
            elif choice == '3':  # START Add/Remove su.d support
                if j.getconf('root', j.uconf):
                    if not j.getconf('sud', j.uconf):
                        j.banner()
                        print(j.lang['root_sud_add_q'])
                        reply = j.getChar()
                        if reply != 'y':
                            continue
                        root_sud()
                    else:
                        j.banner()
                        print(j.lang['root_sud_rem_q'])
                        reply = j.getChar()
                        if reply != 'y':
                            continue
                        root_sudrem()
                else:
                    j.banner()
                    j.kprint(j.lang['error'], 'yrbbo')
                    j.kprint(j.lang['root_must_add'] + '\n', 'r')
                    input(j.lang['enter_root_menu'])
                continue
            elif choice == '4':  # START ROM Tools Menu
                break

    def signzip(signzipname, signext=None):
        if j.autorom():
            if j.getar('sign_zip') == 'true':
                reply = 'y'
            else:
                reply = 'n'
        else:
            print(j.lang['sign_q'])
            reply = j.getChar()

        if reply == 'y':
            j.banner()
            j.kprint(j.lang['sign_ram_check'], 'b')
            zipbyte = os.stat(j.rd + '/' + signzipname + '.zip').st_size
            zipmb = int(zipbyte / 1024 / 1024 + 1)
            heapsize = int(j.get_heapsize())
            ramest = int(zipmb * 3.48 + 1)
            if not j.autorom() and ramest > heapsize:
                j.banner()
                j.kprint(j.lang['warning'], 'yrbbo')
                j.kprint(j.lang['sign_no_ram'] + '\n', 'r')
                print(j.lang['deodex_try_anyway'])
                reply = j.getChar()
                if reply != 'y':
                    return

            j.banner()
            j.kprint(j.lang['sign_signing'] + signzipname + '.zip ...', 'b')
            with j.cd(j.rd):
                j.appendf(j.cmd(
                    f'java -Xmx{heapsize}m -jar {j.tools}/signapk/signapk.jar -w {j.tools}/signapk/testkey.x509.pem {j.tools}/signapk/testkey.pk8 {signzipname}.zip {signzipname}-signed.zip'),
                          j.logs + '/sign.log')
                ubtmp = j.greps('.*update-binary', j.zipl(signzipname + '.zip'))
                if ubtmp:
                    j.appendf(j.zipef(signzipname + '.zip',
                                      ubtmp[0]), j.logs + '/zip.log')
                    bintxt = j.grepf('ui_print', 'update-binary')
                    j.delpath('update-binary')
                else:
                    bintxt = []

                if bintxt:
                    j.appendf(j.cmd(j.zipadjust + ' ' + signzipname + '-signed.zip '
                                    + signzipname + '-signed-fixed.zip'), j.logs + '/sign.log')
                    j.appendf(j.cmd('java -Xmx' + str(
                        heapsize) + 'm -jar ' + j.tools + '/signapk/minsignapk.jar ' + j.tools + '/signapk/testkey.x509.pem '
                                    + j.tools + '/signapk/testkey.pk8 ' + signzipname + '-signed-fixed.zip ' + signzipname + '-signed2.zip'),
                              j.logs + '/sign.log')
                    j.delpath(signzipname + '-signed.zip',
                              signzipname + '-signed-fixed.zip')
                    try:
                        os.replace(signzipname + '-signed2.zip',
                                   signzipname + '-signed.zip')
                    except:
                        pass

            j.banner()
            if j.existf(j.rd + '/' + signzipname + '-signed.zip'):
                j.kprint(signzipname + '-signed.zip '
                         + j.lang['sign_signed'] + '\n', 'g')
            else:
                j.kprint(j.lang['error'], 'yrbbo')
                j.kprint(j.lang['sign_fail'] + '\n', 'r')

            if not signext:
                input(j.lang['enter_continue'])
                return

    def srkup(fname):
        if j.internet():
            try:
                import requests

                url = j.server1 + '/upload'
                files = [
                    ('file', (fname, open(fname, 'rb'), 'application/octet-stream'))]
                values = {'u': j.srkuser, 'p': j.srkpass}
                r = requests.post(url, files=files, data=values)

                if str(r.content, 'utf-8') == '0':
                    return 0
            except Exception as e:
                j.appendf(j.logtb(e), j.logs + '/upload.log')

        return 1

    def tarfs(tfile, dirr, partition):
        import struct
        import ugids

        with open(tfile, 'rb') as f:
            buf = f.read(512)
            while buf:
                if b' RHT.security.' in buf:
                    fcon = buf.split(b'\n')[0].split(b'=')[1].decode()
                    buf2 = f.read(512)
                    fname = buf2.split(b'\x00')[0].decode()
                    fperm = buf2.split(fname.encode())[1].replace(
                        b'\x00', b'').decode()[3:7]
                    fname = dirr + fname
                    if fname.endswith('/'):
                        fname = fname[:-1]
                    if fname.startswith('/'):
                        fname = fname[1:]

                    j.appendf('/' + fname + ' ' + fcon, j.prfiles
                              + '/file_contexts3-' + partition)

                    if os.path.islink(j.rd + '/' + fname):
                        buf = f.read(512)
                        continue

                    ugidtmp = buf2.split(b'ustar  \x00')[1]
                    ugidtmp = list(filter(len, ugidtmp.split(b'\x00')))
                    uid = ugids.ugids[str(ugidtmp[0].decode()).upper()]
                    gid = ugids.ugids[str(ugidtmp[1].decode()).upper()]

                    if b'.capability=' in buf:
                        fcap = str(
                            list(struct.unpack('<QQ', buf.split(b'\n')[1].split(b'=')[1][4:]))[0])
                        j.appendf(fname + ' ' + uid + ' ' + gid + ' ' + fperm
                                  + ' capabilities=' + fcap, j.prfiles + '/fs_config-' + partition)
                    else:
                        j.appendf(fname + ' ' + uid + ' ' + gid + ' ' + fperm,
                                  j.prfiles + '/fs_config-' + partition)

                buf = f.read(512)

            if not j.grepf('^' + dirr + partition + ' ', j.prfiles + '/fs_config-' + partition):
                j.appendf(partition + ' 0 0 0755',
                          j.prfiles + '/fs_config-' + partition)

    def update_project():
        loop = 0
        while loop == 0:
            api = j.getprop('ro.build.version.sdk')
            if not api:
                api = j.getprop('ro.system.build.version.sdk')

            permtype = j.getconf('permtype', j.uconf)

            signature = get_sig()
            sigcust = get_sigcust()

            j.banner()
            j.kprint(j.lang['cust_prep'], 'b')

            devicename = j.get_devicename()
            deviceloc = j.tools + os.sep + 'devices' + os.sep + devicename
            devicechk = j.getconf('devicechk', j.uconf)

            if not j.existf(deviceloc + '/capfiles-' + api):
                for i in [j.prfiles + '/fs_config-system', j.prfiles + '/fs_config-vendor',
                          j.prfiles + '/fs_config-oem']:
                    if j.existf(i):
                        j.appendf('\n'.join(j.grepf(
                            '.*capabilities|system/bin/|system/sbin/|system/lib/valgrind/|system/lib64/valgrind/|system/vendor/bin/|system/xbin/|system/vendor/xbin/|^vendor/bin/|^vendor/xbin|^oem/bin/',
                            i)), deviceloc + '/capfiles-' + api)

            if j.sar():
                j.sysdir = j.rd + os.sep + 'system' + os.sep + 'system'
            else:
                j.sysdir = j.rd + os.sep + 'system'

            if not permtype:
                choice = ''
                while not choice:
                    if j.autorom():
                        choice = j.getar('perm_type')
                    else:
                        j.banner()
                        print(j.lang['perm_which'] + '\n')

                        if api < '19':
                            j.kprint('1) ' + j.lang['perm_set_metadata'], 'r')
                        else:
                            print('1) ' + j.lang['perm_set_metadata'])

                        if api < '19':
                            print('2) ' + j.lang['perm_set_perm'])
                        else:
                            j.kprint('2) ' + j.lang['perm_set_perm'], 'r')

                        if api >= '21':
                            print('3) ' + j.lang['perm_sparse'])
                        else:
                            j.kprint('3) ' + j.lang['perm_sparse_red'], 'r')

                        print('4) ' + j.lang['perm_raw_img'] + '\n')
                        print(j.lang['select'])
                        choice = j.getChar()

                    if choice.isnumeric():
                        if choice < '1' or choice > '7':
                            continue
                    else:
                        continue

                    j.banner()
                    j.kprint(j.lang['cust_prep'], 'b')

                    abi = get_abi()

                    if choice == '1':  # set_metadata chosen
                        if api < '19':
                            j.banner()
                            j.kprint(
                                j.lang['perm_set_metadata_error'] + '\n', 'r')
                            input(j.lang['enter_continue'])
                            choice = ''
                            continue

                        permtype = 'set_metadata'

                        if not j.existf(j.prfiles + '/set_metadata1'):
                            for i in ['system'] + j.getconf('exdirs', j.uconf, l=1):
                                if j.existf(j.prfiles + '/fs_config-' + i):
                                    metasetup(i)

                        copyfile(j.tools + '/updater/binary/update-binary-meta',
                                 j.usdir + '/update-binary')
                        j.getconf('permtype', j.uconf, add=permtype)
                    elif choice == '2':  # set_perm chosen
                        if api > '18':
                            j.banner()
                            j.kprint(j.lang['perm_set_perm_error'] + '\n', 'r')
                            input(j.lang['enter_continue'])
                            choice = ''
                            continue

                        permtype = 'set_perm'
                        copyfile(j.tools + '/updater/binary/update-binary-meta',
                                 j.usdir + '/update-binary')
                        j.getconf('permtype', j.uconf, add=permtype)
                    elif choice == '3':  # Sparse dat chosen
                        if api < '21':
                            choice = ''
                            continue

                        permtype = 'sparse_dat'
                        j.delpath(j.rd + '/META-INF', j.rd + '/config', j.rd + '/install',
                                  j.prfiles + '/set_metadata', j.prfiles + '/set_perm')
                        j.cpdir(j.tools + '/updater/META-INF-DAT/META-INF',
                                j.rd + '/META-INF')
                        copyfile(j.tools + '/updater/binary/update-binary-'
                                 + abi, j.usdir + '/update-binary')
                        j.configure(abi.replace('_64', '').replace('64', ''))
                        j.getconf('permtype', j.uconf, add=permtype)

                        if j.existf(j.rd + '/dynamic_partitions_op_list'):
                            j.awkadd('#UNMOUNT',
                                     'assert(update_dynamic_partitions(package_extract_file("dynamic_partitions_op_list")));',
                                     'before', 'first', j.usdir + '/updater-script')
                    elif choice == '4':  # raw_img chosen
                        j.delpath(j.rd + '/META-INF', j.rd + '/config', j.rd + '/install',
                                  j.prfiles + '/set_metadata', j.prfiles + '/set_perm')
                        j.cpdir(j.tools + '/updater/META-INF-IMG/META-INF',
                                j.rd + '/META-INF')
                        j.configure()
                        copyfile(j.tools + '/updater/binary/update-binary-meta',
                                 j.usdir + '/update-binary')
                        permtype = 'raw_img'
                        j.getconf('permtype', j.uconf, add=permtype)

                    if not j.getconf('permtype', j.uconf):
                        choice = ''

                if choice in ['3', '4']:
                    continue

            j.banner()
            j.kprint(j.lang['startup_prep_updater_script'], 'b')

            os.chdir(j.sysdir)
            os.chdir('..')
            sys_files = j.findr('system/**')
            os.chdir(j.bd)

            with j.cd(j.rd):
                for i in j.getconf('exdirs', j.uconf, l=1):
                    if j.existd(i):
                        sys_files += j.findr(i + '/**')

            all_files = sorted(sys_files)
            del sys_files

            if not j.grepf('#ASSERT', j.usdir + '/updater-script'):
                j.awktop('#ASSERT', j.usdir + '/updater-script')
                j.appendf(j.grepf(' getprop\(|\(getprop\(', j.usdir
                                  + '/updater-script'), j.prfiles + '/assert_original')

            if not j.grepf('#SYM', j.usdir + '/updater-script'):
                j.awkadd('symlink', '#SYM', 'before',
                         'first', j.usdir + '/updater-script')

            if not j.grepf('^#PERM$', j.usdir + '/updater-script'):
                if j.grepf(j.fl('^' + permtype, '/tmp/'), j.usdir + '/updater-script'):
                    j.awkadd('#SYM', '#PERM', 'after', 'first',
                             j.usdir + '/updater-script')

            uscript = j.readfl(j.usdir + '/updater-script')
            if permtype == 'set_metadata' or permtype == 'set_perm':
                permtest = j.grepb('#PERM', 'set_progress', uscript)
                if permtest:
                    j.grepvb(permtest, j.usdir + '/updater-script')
                    del permtest

            if j.existf(j.usdir + '/aroma-config'):
                aromatest = j.greps(j.fl('', 'set_progress'), j.grepb(
                    '#AROMA', 'set_progress', uscript))
                if aromatest:
                    j.grepvb(aromatest, j.usdir + '/updater-script')
                    del aromatest

            proptest = j.grepf(
                ' getprop\(|\(getprop\(|^symlink', j.usdir + '/updater-script')
            j.grepvb(proptest, j.usdir + '/updater-script')
            j.delpath(j.prfiles + '/set_metadata', j.prfiles + '/set_perm')

            if permtype == 'set_perm':
                permt = j.readfl(j.tools + '/updater/set_perm-data')
                for i in permt:
                    perm = i.split('"')[1].replace('/', '', 1)
                    if perm in all_files:
                        j.appendf(i, j.prfiles + '/set_perm')
                copyfile(j.prfiles + '/set_perm', j.prfiles + '/set_perm.orig')
            elif permtype == 'set_metadata':
                if not j.existf(j.prfiles + '/set_metadata1') and not j.existf(j.prfiles + '/file_contexts2'):
                    j.get_contexts()
                    if not j.existf(j.prfiles + '/file_contexts2'):
                        j.banner()
                        j.kprint(j.lang['error'], 'yrbbo')
                        j.kprint(j.lang['build_selinux_error'], 'r')
                        j.kprint(j.lang['build_selinux_error2'], 'r')
                        j.kprint(j.lang['build_selinux_error3'], 'r')
                        j.kprint(j.lang['build_selinux_error4'], 'r')
                        j.kprint(j.lang['build_selinux_error5'] + '\n\n', 'r')
                        j.kprint(j.lang['build_selinux_error6'] + '\n', 'b')
                        input(j.lang['enter_continue'])
                        j.getconf('permtype', j.uconf, 'rem')
                        continue

                if j.sar():
                    j.sedf('/system', '/system/system',
                           j.prfiles + '/file_contexts2')

                if not j.existf(j.prfiles + '/set_metadata1'):
                    tmpf = []
                    for i in glob.glob(j.prfiles + '/symlinks-*'):
                        tmpf += j.readfl(i)

                    if not tmpf:
                        j.banner()
                        j.kprint(j.lang['error_mess'] + ' Symlinks\n', 'r')
                        input(j.lang['enter_continue'])
                        tmpf = []

                    tsym = []
                    for i in tmpf:
                        i = i.split('"')[3].replace('/', '', 1)
                        tsym.append(i)

                    tcon = j.readfl(j.prfiles + '/file_contexts2')
                    pre_metadata = {'system': 'u:object_r:system_file:s0'}
                    for i in tcon:
                        fcon = i.split()[0].replace('/', '', 1)
                        ccon = i.split()[1]
                        if fcon in all_files or fcon in tsym:
                            pre_metadata[fcon] = ccon

                    if j.sar():
                        metadata = j.readfl(
                            j.tools + '/updater/set_metadata-data2')
                    else:
                        metadata = j.readfl(
                            j.tools + '/updater/set_metadata-data')

                    for i in metadata:
                        line2 = i.split()[0].split('"')[1].replace('/', '', 1)
                        if line2 in list(pre_metadata):
                            context = pre_metadata[line2]
                            j.appendf(i.replace('#CONTEXT', context),
                                      j.prfiles + '/set_metadata')
                            del pre_metadata[line2]
                        elif line2 in all_files:
                            j.appendf(i, j.prfiles + '/set_metadata')

                    for i in list(pre_metadata):
                        ccon = pre_metadata[i]
                        j.appendf('set_metadata("' + i + '", "selabel", "'
                                  + ccon + '");', j.prfiles + '/set_metadata')
                else:
                    with j.cd(j.prfiles):
                        j.delpath('set_metadata')
                        copyfile('set_metadata1', 'set_metadata')
                        if j.greps('vendor|oem|product', j.getconf('exdirs', j.uconf, l=1)) and j.existf(
                                'set_metadataV'):
                            j.appendf(j.readf('set_metadataV'), 'set_metadata')

                if j.grepf('#CONTEXT', j.prfiles + '/set_metadata'):
                    with j.cd(j.prfiles):
                        if not j.existf('file_contexts2'):
                            j.get_contexts()
                        for i in j.readfl('set_metadata'):
                            if '#CONTEXT' in i:
                                try:
                                    context = j.grepf(
                                        i.split('"')[1] + ' ', 'file_contexts2')[0].split()[1]
                                except:
                                    context = 'u:object_r:system_file:s0'

                                j.appendf(
                                    i.replace('#CONTEXT', context), 'set_metadata2')
                            else:
                                j.appendf(i, 'set_metadata2')

                        os.replace('set_metadata2', 'set_metadata')

                if j.existf(j.prfiles + '/root_meta'):
                    j.awktop(j.readf(j.prfiles + '/root_meta'),
                             j.prfiles + '/set_metadata')

            with j.cd(j.rd):
                if j.sar():
                    apptmp = glob.glob('system/system/app/*')
                    privtmp = glob.glob('system/system/priv-app/*')
                else:
                    apptmp = glob.glob('system/app/*')
                    privtmp = glob.glob('system/priv-app/*')
                appsym = sorted(apptmp + privtmp, key=str.lower)

            tmpf = []
            for i in glob.glob(j.prfiles + '/symlinks*'):
                tmpf = tmpf + j.readfl(i)

            tsym = j.greps('/system/app|/system/priv-app', tmpf)
            for i in tsym:
                line = i.split('"')[3].split('/')[1:4]
                line = '/'.join(line)

                if j.sar():
                    line = 'system/' + line

                if line not in appsym:
                    if i in tmpf:
                        tmpf.remove(i)

            if j.existf(j.rd + '/ramdisk.img') and not j.existf(j.rd + '/boot.img') and not j.grepf('ramdisk.img',
                                                                                                    j.usdir + '/updater-script'):
                j.awkadd('boot image', '#RAMDISK\n#KERNEL', 'before',
                         'first', j.usdir + '/updater-script')
                j.grepvf('boot.img|boot image', j.usdir + '/updater-script')
                j.sedf('#RAMDISK', j.readf(
                    j.tools + '/updater/custom/boot-ramdisk'), j.usdir + '/updater-script')

                if j.existf(j.rd + '/kernel.img'):
                    j.sedf('#KERNEL', j.readf(
                        j.tools + '/updater/custom/boot-kernel'), j.usdir + '/updater-script')
                else:
                    j.grepvf('#KERNEL', j.usdir + '/updater-script')

            part_setup('boot')

            if not j.getconf('assert-no', j.mconf) and not j.existf(j.prfiles + '/assert'):
                copyfile(j.tools + '/updater/custom/assert', j.prfiles + '/assert')
                j.appendf('    ' + j.readf(j.tools
                                           + '/updater/custom/abort'), j.prfiles + '/assert')

                j.sedf('#DEVICENAME', devicename, j.prfiles + '/assert')
                j.sedf('#DEVICECHK', devicechk, j.prfiles + '/assert')

                if j.existf(j.prfiles + '/assertcustom'):
                    j.grepff('ro.product.device', j.prfiles
                             + '/assert', j.prfiles + '/assert-2')
                    os.replace(j.prfiles + '/assert-2', j.prfiles + '/assert')
                    j.appendff(j.prfiles + '/assertcustom', j.prfiles + '/assert')

            if not j.getconf('assert-no', j.mconf) and not j.grepf(' getprop\(|\(getprop\(',
                                                                   j.usdir + '/updater-script'):
                j.awkadd('#ASSERT', j.readf(j.prfiles + '/assert'),
                         'after', 'first', j.usdir + '/updater-script')

            j.sedf('#SIGNATURE', signature.replace(
                '_', ' '), j.usdir + '/updater-script')
            j.sedf('#SIGCUST', sigcust, j.usdir + '/updater-script')
            j.sedf('#DEVICENAME', devicename, j.usdir + '/updater-script')
            j.sedf('#DEVICECHK', devicechk, j.usdir + '/updater-script')

            if permtype not in ['sparse_dat', 'raw_img']:
                j.awkadd('#SYM', '\n'.join(sorted(tmpf)), 'after',
                         'first', j.usdir + '/updater-script')
                j.sedf(' "/system', ' file_getprop("/tmp/config", "sysmnt")+"',
                       j.usdir + '/updater-script')

                if not j.grepf('delete_recursive.*sysmnt', j.usdir + '/updater-script'):
                    j.awkadd('#SYSFORMAT', 'delete_recursive(file_getprop("/tmp/config", "sysmnt"));',
                             'after', 'first', j.usdir + '/updater-script')

                    for i in j.getconf('exdirs', j.uconf, l=1):
                        j.awkadd('#SYSFORMAT', 'delete_recursive("/' + i + '");',
                                 'after', 'first', j.usdir + '/updater-script')

                j.awkadd('#PERM', j.readf(j.prfiles + '/' + permtype),
                         'after', 'first', j.usdir + '/updater-script')
                j.sedf('set_metadata\("/system/',
                       'set_metadata(file_getprop("/tmp/config", "sysmnt")+"/', j.usdir + '/updater-script')
                j.sedf('set_metadata_recursive\("/system/',
                       'set_metadata_recursive(file_getprop("/tmp/config", "sysmnt")+"/', j.usdir + '/updater-script')

            if j.existf(j.prfiles + '/aroma_appupdater'):
                if not j.grepf('#AROMA', j.usdir + '/updater-script'):
                    if j.grepf('^' + permtype, j.usdir + '/updater-script'):
                        j.awkadd('^' + permtype, '#AROMA', 'after',
                                 'last', j.usdir + '/updater-script')

                j.awkadd('#AROMA', j.readf(j.prfiles + '/aroma_appupdater'),
                         'after', 'first', j.usdir + '/updater-script')

            if j.getconf('exdirs', j.uconf) and not j.getconf('exdone', j.uconf):
                for i in j.getconf('exdirs', j.uconf, l=1):
                    if not j.grepf('package_extract_dir("' + i + '.*', j.usdir + '/updater-script') and not j.grepf(
                            i + '.transfer', j.usdir + '/updater-script') and not j.grepf(
                        'package_extract_file("' + i + '.*', j.usdir + '/updater-script'):
                        partadd(i)

                j.getconf('exdone', j.uconf, add='1')

            if j.getconf('case_fix', j.mconf) == 'Yes' and permtype in ['set_metadata', 'set_perm']:
                with j.cd(j.rd):
                    tmp_exl = []
                    for i in j.findr('**/*.ex*.srk'):
                        x = i.split('/')[0]
                        if x not in tmp_exl:
                            tmp_exl.append(x)

                    for i in tmp_exl:
                        if not j.grepf('"' + i + '_exfiles"', j.usdir + '/updater-script'):
                            partadd(i + '_exfiles')

                    del tmp_exl

            loop = 1

    def winextract(partition, romwin):
        j.banner()
        j.kprint(j.lang['general_extracting'] + partition + ' ...', 'b')

        with j.cd(j.rd):
            wintst = j.greps(
                j.fl('', '.*\.sha2$|.*\.md5$|.*\.info$'), glob.glob('*' + partition + '*.win*'))
            if len(wintst) > 1:
                romwin = wintst
                winsystem = j.greps('000', wintst)[0]
                istar = wintst
                tartest = j.tarlist(winsystem)
            else:
                winsystem = romwin
                try:
                    tartest = j.tarlist(winsystem)
                except:
                    j.cmd(j.p7z + ' e ' + winsystem)
                    j.delpath(winsystem)
                    os.replace('.'.join(winsystem.split('.')[:-1]), winsystem)
                    tartest = j.tarlist(winsystem)

                istar = [winsystem]

            for i in istar:
                if not partition in tartest[0]:
                    j.appendf(j.taru(i, partition), j.logs + '/zip.log')
                    if tartest[0].startswith('/'):
                        dirr = partition
                    else:
                        dirr = partition + '/'
                else:
                    j.appendf(j.taru(i), j.logs + '/zip.log')
                    dirr = ''

                tarfs(i, dirr, partition)

    ######################################
    ######################################
    ######################################
    ######################################
    ########### START KITCHEN ############
    ######################################
    ######################################
    ######################################
    ######################################
    j.romname = ''
    permtype = ''
    langchk = ''

    if ' ' in j.bd:
        j.banner()
        j.kprint('ERROR:', 'yrbbo')
        j.kprint('The kitchen must be run in a path without spaces.'
                 + '\n\n' + color['b'] + 'CURRENT PATH:', 'r')
        j.kprint(j.bd + '\n', 'y')
        input('Press ENTER to exit')
        sys.exit()

    os.chdir(j.bd)

    if not j.getconf('language', j.mconf):
        with j.cd(j.tools + '/language'):
            ftmp = j.greps(j.fl('', 'default_srk.py'), glob.glob('*_srk.py'))

        langfile = ''
        if len(ftmp) >= 1:
            while not langfile:
                langfile = j.chlist(
                    color['gb'] + 'Choose language:', ftmp, len(ftmp))
                if langfile and '.zip' in langfile:
                    with j.cd(j.tools + '/language'):
                        ftmp = j.greps(j.fl('', 'default_srk.py'),
                                       glob.glob('*_srk.py'))
                    langfile = ''

            j.delpath(j.tools + '/language/default_srk.py',
                      j.tools + '/language/__pycache__')
            if 'english' in langfile:
                langchk = 0
            else:
                langchk = j.language_check(langfile[:-7])

        j.lang = j.getlang(langfile)

        j.getconf('language', j.mconf, add=langfile[:-7])
        if langchk == 1:
            j.banner()
            j.kprint(j.lang['lang_added'] + langfile, 'r')
            print(j.lang['lang_translate'] + '\n')
            input(j.lang['enter_continue'])
    else:
        langfile = j.getconf('language', j.mconf) + '_srk.py'
        if 'english' not in langfile:
            if not j.getconf('firstrun', j.mconf):
                j.language_check(langfile[:-7])

        j.lang = j.getlang(langfile)

    j.srkuser, j.srkpass, j.dbtst, j.days_left, latest_ver = j.user_auth()

    if 'SSH_CONNECTION' in os.environ or 'SSH_CLIENT' in os.environ:
        if 'SSH_CONNECTION' in os.environ:
            sshtmp = os.environ['SSH_CONNECTION']
        else:
            sshtmp = os.environ['SSH_CLIENT']

        try:
            client_addr = sshtmp.split()[0]
        except:
            client_addr = None

        if client_addr and IPv4Address(client_addr).is_private:
            j.internet(j.server1 + '/errlog2/?e=' + j.mfunc2('auth = '
                                                             + str(['SSH ALLOWED:', j.srkuser, j.platf + ' ' + sshtmp]),
                                                             'out').decode())
        else:
            j.internet(j.server1 + '/errlog2/?e=' + j.mfunc2('auth = '
                                                             + str(['SSH CONNECT:', j.srkuser, j.platf + ' ' + sshtmp]),
                                                             'out').decode())

            j.banner()
            j.kprint('Something went wrong.', 'r')
            sys.exit()

    if j.existf(j.tools + '/source/md5_full'):
        if not j.getconf('firstrun', j.mconf) and latest_ver > j.superrv[1::2]:
            j.banner()
            j.kprint(
                j.superrv + ' ' + j.lang['update_latest_version'] + ' v' + '.'.join(latest_ver) + '.\n', 'y')
            print(j.lang['general_cont_anyway_q'])

            if j.getChar() != 'y':
                sys.exit()

        if j.platf == 'wsl2' and not j.bd.startswith('/home'):
            j.banner()
            j.kprint(j.lang['warning'], 'yrbbo')
            j.kprint(j.lang['startup_wsl2_warning'], 'y')
            j.kprint(j.lang['startup_wsl2_warning2'] + '\n', 'y')
            print(j.lang['general_cont_anyway_q'])

            if j.getChar() != 'y':
                sys.exit()
        elif j.platf == 'wsl':
            j.banner()
            j.kprint(j.lang['warning'], 'yrbbo')
            j.kprint(j.lang['startup_wsl_warning'], 'y')
            j.kprint(j.lang['startup_wsl_warning2'] + '\n', 'y')
            print(j.lang['general_cont_anyway_q'])

            if j.getChar() != 'y':
                sys.exit()

    if not j.getconf('depmet', j.mconf):
        if not j.existf('/system/build.prop') and not j.existf('/system/system/build.prop'):
            nodec = None
            if which('java'):
                try:
                    line = j.greps('.*java version|.*openjdk version',
                                   j.cmd('java -version').splitlines())[0]
                except:
                    line = None

                if line:
                    line = line.split('"')[1]
                    if '-' in line:
                        line = re.sub('[^0-9]', '', line)
                        nodec = 1
                    elif not line.startswith('1.') and '.' in line:
                        line = line.split('.')[0]
                        nodec = 1
                    elif line.startswith('1.') and len(line) >= 3:
                        line = line[:3]

                    line = float(line)
                else:
                    line = 1
            else:
                line = 1

            if any([not nodec and line < 1.8, nodec and line < 8]):
                j.banner()
                j.kprint(j.lang['startup_mdepend'], 'yrbbo')
                j.kprint(j.lang['startup_need_java'] + '\n', 'r')
                input(j.lang['enter_exit'])
                sys.exit()

        notfound = []
        alldeps = j.readfl(depends)

        if alldeps:
            if j.platf in ['wsl', 'wsl2']:
                alldeps.append('tput')
                j.getconf('screen_clear', j.mconf, add='1')

            for i in alldeps:
                if which(i):
                    continue
                else:
                    notfound.append(i)

        if notfound:
            j.banner()
            j.kprint(j.lang['startup_mdepend'] + '\n', 'yrbbo')
            j.kprint('\n'.join(notfound) + '\n', 'y')
            input(j.lang['enter_exit'])
            sys.exit()

        j.getconf('depmet', j.mconf, add='1')

    with j.cd(j.tools):
        x = 0
        for i in ['linux_tools', 'mac_tools', 'devices', 'smali', 'boot/AIK', 'updater/binary']:
            if j.existd(i):
                x += 1

    if x < 5:
        get_tools()

    if j.existf(j.tools + '/source/md5_full'):
        j.banner()
        j.kprint(j.lang['update_verify'], 'b')

        md5err = []
        for i in j.readfl(j.tools + '/source/md5_full'):
            i = i.split('\t')

            if j.md5chk(i[0]) != i[-1]:
                md5err.append(i[0])

        if md5err:
            j.banner()
            j.kprint(j.lang['error'], 'yrbbo')

            md5source = j.greps('tools/source/.*', md5err)

            if j.getconf('firstrun', j.mconf):
                j.appendf('ERROR: ' + j.lang['startup_checksum'], 'update.log')
                j.appendf('\n'.join(md5err), 'update.log')

                j.kprint(j.lang['startup_checksum'], 'r')
                j.kprint('\n'.join(md5err) + '\n', 'y')

                if md5source:
                    j.kprint(j.lang['update_fail'], 'r')
                    j.kprint(j.lang['update_fail2'] + '\n', 'r')
                    j.kprint(j.lang['update_fail3'] + '\n', 'r')

                    input(j.lang['enter_exit'])
                    sys.exit()
                else:
                    print(j.lang['general_cont_anyway_q'])
                    reply = j.getChar()
                    if reply != 'y':
                        sys.exit()
            else:
                j.appendf(
                    'ERROR: The following checksums did not match:', 'install.log')
                j.appendf('\n'.join(md5err), 'install.log')

                j.kprint(j.lang['startup_error'] + '\n', 'r')
                input(j.lang['enter_exit'])
                sys.exit()

        get_tools()

        if j.getconf('firstrun', j.mconf):
            doneit = j.internet(j.server1 + '/dlplug/?u='
                                + j.srkuser + '&p=' + j.srkpass + '&d=update2.py', 1)
            if doneit.startswith('import'):
                update = types.ModuleType('update')
                exec(doneit, update.__dict__)
                del doneit
            else:
                j.banner()
                j.kprint(j.lang['error'], 'yrbbo')
                j.kprint(j.lang['update_down'], 'r')
                j.kprint(j.lang['update_down2'] + '\n', 'r')
                input(j.lang['enter_exit'])
                sys.exit(1)

            if update.doupdate(j) == 'none':
                j.banner()
                j.kprint(j.lang['error_mess'] + '\n', 'r')
                input(j.lang['enter_exit'])
                sys.exit()

            with j.cd(j.tools + '/plugins'):
                plugins44 = sorted(j.greps(j.fl('', '.*\.zip$'), glob.glob('*')))

            retv = j.mfunc2('auth = ' + str([j.srkuser, 1, 0, j.superrv,
                                             j.osbit(), j.platf, j.whoami(), j.dbtst]), 'out').decode()

            j.internet(f'{j.server1}/estats/?e={retv}')

            del retv

            j.plug_update(plugins44, quiet=1)
        else:
            retv = j.mfunc2('auth = ' + str([j.srkuser, 0, 1, j.superrv,
                                             j.osbit(), j.platf, j.whoami(), j.dbtst]), 'out').decode()

            j.internet(j.server1 + '/estats/?e=' + retv)

            del retv

            j.getconf('firstrun', j.mconf, add='1')
            j.getconf('ubinary', j.mconf, add='no')
            j.getconf('assert-no', j.mconf, add='1')
            j.getconf('metasize', j.mconf, add='Short')

        if not j.getconf('case_fix', j.mconf):
            if j.platf in ['wsl', 'wsl2']:
                j.getconf('case_fix', j.mconf, add='Yes')
            else:
                j.getconf('case_fix', j.mconf, add='No')

        if not j.getconf('mount_extract', j.mconf):
            if j.platf == 'wsl':
                j.getconf('mount_extract', j.mconf, add='No')
            else:
                j.getconf('mount_extract', j.mconf, add='Yes')

        if not j.getconf('use_make_ext4fs', j.mconf):
            if j.platf != 'mac':
                j.getconf('use_make_ext4fs', j.mconf, add='No')

        if not j.getconf('create_missing_symlink_dirs', j.mconf):
            j.getconf('create_missing_symlink_dirs', j.mconf, add='Yes')

        j.delpath(j.tools + '/source/md5_full')

    if not j.partslist:
        j.partslist = ['system', 'prism', 'optics', 'vendor', 'product', 'super',
                       'oem', 'odm', 'system_ext', 'hidden', 'cust', 'generic', 'system_other']

        j.getconf('partition_extract_list', j.mconf, add=j.partslist, l=1)

    if j.getconf('updatecheck', j.mconf) == 'yes':
        j.kitchen_update()

    loop = 0
    while loop == 0:
        main = 0
        if not j.romname:
            if glob.glob('superr_*'):
                cholist = []
                for i in sorted(glob.glob('superr_*'), key=str.lower):
                    cholist.append(i.replace('superr_', ''))
                countdir = len(cholist)
                if countdir == 1:
                    j.romname = cholist[0]
                else:
                    chosen = j.chlist(
                        color['gb'] + j.lang['title_choose'] + color['n'], cholist, countdir)
                    j.romname = chosen
            else:
                j.romname = j.new_project()

        if ' ' in j.romname:
            with j.cd(j.bd):
                if j.existd('superr_' + j.romname):
                    os.replace('superr_' + j.romname, 'superr_'
                               + j.romname.replace(' ', '_'))
                j.romname = j.romname.replace(' ', '_')

        j.rd = j.bd + os.sep + 'superr_' + j.romname
        if j.sar():
            j.sysdir = j.rd + os.sep + 'system' + os.sep + 'system'
            j.issudo2 = ''
        elif j.existd(j.rd + '/system'):
            j.sysdir = j.rd + os.sep + 'system'
            j.issudo2 = 'sudo '
        else:
            j.sysdir = ''
            j.issudo2 = 'sudo '

        if not j.existd(j.rd + '/00_project_files/logs'):
            j.mkdir(j.rd + '/00_project_files/logs')

        j.prfiles = j.rd + os.sep + '00_project_files'
        j.uconf = j.prfiles + os.sep + 'srk.conf'
        j.logs = j.prfiles + os.sep + 'logs'
        j.usdir = j.rd + os.sep + 'META-INF' + os.sep + 'com' + os.sep + 'google' + os.sep + 'android'

        if j.existf('update.log'):
            os.replace('update.log', j.logs + os.sep + 'update.log')

        if j.getprop('ro.build.version.sdk'):
            devicename = j.get_devicename()
            deviceloc = j.tools + os.sep + 'devices' + os.sep + devicename
            api = j.getprop('ro.build.version.sdk')
            j.androidversion = j.getprop('ro.build.version.release')
            androidversion2 = ''
        else:
            j.androidversion = color['r'] + j.lang['startup_copy_extract'] + '\n'
            androidversion2 = j.lang['startup_copy_extract2']

        if j.existf(j.prfiles + '/exdirs'):
            j.getconf('exdirs', j.uconf, add=j.readfl(
                j.prfiles + '/exdirs'), l=1)
            j.delpath(j.prfiles + '/exdirs')

        choice = ''
        while not choice:
            j.timegt()

            j.banner()
            if j.romname:
                j.kprint(j.lang['startup_project'] + color['g'] + j.romname, 'b')
                j.kprint(j.lang['startup_version'] + color['g']
                         + j.androidversion + androidversion2, 'b')

            print()
            j.kprint(j.lang['title_main'] + '\n', 'ryb')
            print('1) ' + j.lang['menu_create'])
            print('2) ' + j.lang['menu_choose'])
            print('3) ' + j.lang['menu_delete'])
            print('4) ' + j.lang['menu_extract'])

            if latest_ver > j.superrv[1::2]:
                print(color['c'] + color['bo'] + '5) ' + j.lang['update_update_avail']
                      + ' v' + '.'.join(latest_ver) + color['n']
                      + ' (' + color['b'] + j.lang['title_current']
                      + color['g'] + j.superrv + color['n'] + ')')
            else:
                print('5) ' + j.lang['menu_updates'] + ' (' + color['b']
                      + j.lang['title_current'] + color['g'] + j.superrv + color['n'] + ')')

            j.kprint('6) ' + j.lang['menu_misc'], 'y')
            j.kprint('7) ' + j.lang['menu_boot_recovery'], 'y')
            j.kprint('8) ' + j.lang['menu_rom_tools'], 'y')
            j.kprint('9) ' + j.lang['menu_plugin_menu'], 'y')
            j.kprint('q = ' + j.lang['menu_quit'] + '\n', 'm')
            print(j.lang['select'])
            choice = j.getChar()

            if choice.isnumeric():
                if choice < '1' or choice > '9':
                    continue
            elif choice not in ['q']:
                continue

            if choice == 'q':  # START Quit
                loop = 1
            elif choice == '1':  # START Create new project directory
                j.romname = j.new_project()
            elif choice == '2':  # START Choose a different project
                j.romname = ''
            elif choice == '3':  # START Delete a project
                if delete_project(j.romname) == 1:
                    j.romname = ''
            elif choice == '4':  # START Extract for new ROM
                extract_new()
            elif choice == '5':  # START Check for updates
                j.kitchen_update()
            elif choice == '6':  # START Misc Tools
                misc_tools()
            elif choice == '7':  # START Boot Tools
                boot_tools()
            elif choice == '8':  # START ROM tools
                rom_tools()
            elif choice == '9':  # START Plugins
                plugins()
    return
