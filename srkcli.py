#!/usr/bin/env python3
import glob
import sys
import os


def main(j, args, func_dict):
    def err(text):
        print(text)
        sys.exit(1)

    with j.cd(j.bd):
        if not j.existf('tools/root/bloat'):
            err('[ERROR] Something went wrong')

        if args.function[0] not in func_dict:
            err('[ERROR] -f/--function must be one of the following:\n'
                + ''.join([i+' '+func_dict[i]+'\n' for i in func_dict]))

        if '/' in args.project:
            args.project = j.basename(args.project.strip('/'))
            j.kprint(
                '[INFO] -p/--project only requires a project directory name.\nExample: -p superr_project', 'y')

        if os.path.exists(args.project):
            if not os.path.isdir(args.project):
                err('[ERROR] -p/--project argument is not a directory')
        else:
            err('[ERROR] The project path does not exist')

        if len(glob.glob('tools/updater/binary/*')) < 7:
            err('[ERROR] The kitchen must be installed before using the CLI')

        try:
            j.lang = j.getlang(j.getconf('language', j.mconf)+'_srk.py')
        except:
            err('[ERROR] The kitchen must be fully installed before using the CLI')

        color = j.color
        j.rd = j.bd+os.sep+args.project
        j.romname = j.basename(j.rd).replace('superr_', '')
        j.prfiles = j.rd+os.sep+'00_project_files'
        j.logs = j.prfiles+os.sep+'logs'
        j.server1 = 'https://sr-code.com'
        j.superrv = 'v5.5.5.5'
        j.uconf = j.prfiles+os.sep+'srk.conf'

        j.srkuser, j.srkpass, j.dbtst, j.days_left, latest_ver = j.user_auth()

        os.makedirs(j.logs, exist_ok=True)

    with j.cd(j.rd):
        if j.sar():
            j.sysdir = j.rd+os.sep+'system'+os.sep+'system'
            j.issudo2 = ''
        elif j.existd(j.rd+'/system'):
            j.sysdir = j.rd+os.sep+'system'
            j.issudo2 = 'sudo '
        else:
            j.sysdir = ''
            j.issudo2 = 'sudo '

##
# START Functions
##

        if args.function[0] == 'unpack_img':
            if len(args.function) < 2:
                err('[ERROR] unpack_img is missing at least one argument:\n-f/--function '
                    + args.function[0]+' '+func_dict[args.function[0]])
            elif len(args.function) > 2:
                err('[ERROR] '+args.function[0]+' has too many arguments:\n-f/--function '
                    + args.function[0]+' '+func_dict[args.function[0]])

            romimg = args.function[1]
            if not j.existf(romimg):
                err(color['r']+'[ERROR] '+romimg
                    + ' does not exist in the specified project'+color['n'])

            j.kprint(j.lang['boot_unpack']+romimg+' ...', 'b')

            if j.imgextract(romimg, cli=1) != 0:
                j.delpath(romimg[:-4])

                err(color['r']+j.lang['extract_rom_fail']+color['n'])
        elif args.function[0] == 'pack_img':
            if len(args.function) < 3:
                err('[ERROR] pack_img is missing at least one argument:\n-f/--function '
                    + args.function[0]+' '+func_dict[args.function[0]])
            elif len(args.function) > 3:
                err('[ERROR] '+args.function[0]+' has too many arguments:\n-f/--function '
                    + args.function[0]+' '+func_dict[args.function[0]])

            if args.function[-1] not in func_dict['pack_img'].split('MODE OPTIONS: ')[1].split(', '):
                err('[ERROR] The mode entry at the end of the function argument is not correct:\n-f/--function '
                    + args.function[0]+' '+func_dict[args.function[0]])

            romimg = args.function[1]
            whatimg = romimg[:-4]
            mode = args.function[2]

            if not j.existd(whatimg):
                err('[ERROR] There is no '+whatimg
                    + ' directory in the specified project.')

            if not j.getconf('size-'+whatimg, j.uconf):
                if j.getconf('img_size_'+whatimg, j.uconf):
                    j.getconf('size-'+whatimg, j.uconf,
                              add=j.getconf('img_size_'+whatimg, j.uconf))
                elif j.getconf('img_size_'+whatimg, j.mconf):
                    j.getconf('size-'+whatimg, j.uconf,
                              add=j.getconf('img_size_'+whatimg, j.mconf))
                else:
                    j.getconf('size-'+whatimg, j.uconf,
                              add=j.findwhatsize(whatimg))

                if not j.getconf('size-'+whatimg, j.uconf):
                    err('[ERROR] Unable to determine original '+romimg
                        + ' size. Make sure it exists in the project.')

            if j.platf == 'mac' or j.getconf('use_make_ext4fs', j.mconf) == 'Yes':
                if j.partimg(whatimg, ' -s' if mode != 'raw' else '', quiet=1) == 1:
                    err(color['r']+j.lang['img_fail_log']+color['n'])
            else:
                if j.partimg2(whatimg, 'sparse' if mode != 'raw' else '', quiet=1) == 1:
                    err(color['r']+j.lang['img_fail_log']+color['n'])

            if mode == 'dat':
                j.partsdat(whatimg, quiet=1)
            elif mode == 'lz4':
                j.partlz4(whatimg)
        elif args.function[0] == 'unpack_super':
            if len(args.function) < 2:
                err('[ERROR] unpack_super is missing at least one argument:\n-f/--function '
                    + args.function[0]+' '+func_dict[args.function[0]])

            if j.super_unpack(args.function[1], 1) == 1:
                err('[ERROR] unpack_super failed')
        elif args.function[0] == 'pack_super':
            if len(args.function) < 3:
                err('[ERROR] pack_super is missing at least one argument:\n-f/--function '
                    + args.function[0]+' '+func_dict[args.function[0]])

            p_list = args.function[1:]
            if p_list[-1] not in func_dict['pack_super'].split('MODE OPTIONS: ')[1].split(', '):
                err('[ERROR] The mode entry at the end of the function argument is not correct:\n-f/--function '
                    + args.function[0]+' '+func_dict[args.function[0]])

            for i in p_list[:-1]:
                if not j.existf(i):
                    err('[ERROR] One or more files in the function argument do not exist.')

            if j.super_build(p_list) == 1:
                err('[ERROR] pack_super failed')
        elif args.function[0] == 'deodex':
            if not j.findr('**/*.vdex'):
                err(color['r']+j.lang['deodex_no_odex']+color['n'])

            j.androidversion = j.getprop('ro.build.version.release')

            j.usdir = j.rd+os.sep+'META-INF'+os.sep+'com'+os.sep+'google'+os.sep+'android'

            j.deodex_start(quiet=1)
        elif args.function[0] == 'dmverity':
            if not j.greps('system|vendor|boot.img', glob.glob('*')):
                err(color['r']+'ERROR: Nothing to do here'+color['n'])

            if j.existf('boot.img'):
                j.boot_unpack('boot', 'boot.img', quiet=1)

            with j.cd(j.bd):
                j.cmd(j.rampy()+'dmverity '+j.romname+' boot')
                j.cmd(j.rampy()+'status '+j.romname+' boot')

            status = j.readfl(j.prfiles+'/statusfile')
            try:
                veritystatus = status[0].split('=')[1]
            except Exception as e:
                j.appendf(j.logtb(e), j.logs+'/boot.log')
                j.appendf('\n'+'\n'.join(status), j.logs+'/boot.log')
                veritystatus = color['r']+'N/A'+color['n']

            if j.existf('boot.img'):
                j.boot_pack('boot', 'boot.img', quiet=1)

            print('dm-verity status: '+veritystatus)
        elif args.function[0] == 'forcee':
            if not j.greps('system|vendor|boot.img', glob.glob('*')):
                err(color['r']+'ERROR: Nothing to do here'+color['n'])

            if j.existf('boot.img'):
                j.boot_unpack('boot', 'boot.img', quiet=1)

            with j.cd(j.bd):
                j.cmd(j.rampy()+'forcee '+j.romname+' boot')
                j.cmd(j.rampy()+'status '+j.romname+' boot')

            status = j.readfl(j.prfiles+'/statusfile')
            try:
                forceestatus = status[1].split('=')[1]
            except Exception as e:
                j.appendf(j.logtb(e), j.logs+'/boot.log')
                j.appendf('\n'+'\n'.join(status), j.logs+'/boot.log')
                forceestatus = color['r']+'N/A'+color['n']

            if j.existf('boot.img'):
                j.boot_pack('boot', 'boot.img', quiet=1)

            print('forceencryption status: '+forceestatus)
        else:
            err('[ERROR] Command not available')
