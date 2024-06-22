#!/usr/bin/env python3
import glob
# by SuperR. @XDA

import os
from shutil import copyfile


def main(j, indir, partition, filedir):
    def saro():
        if (j.existd(indir+'/system/app') and
            (j.existf(indir+'/init.rc') or
             j.existf(indir+'/init.environ.rc'))):
            return True
        else:
            return False

    if not glob.glob(indir+'/*'):
        print('\n'+indir+' does not exist or is empty.\n')
        return

    uconf = filedir+'/srk.conf'
    mconf = '/'.join(filedir.split('/')[:-2])+'/tools/srk.conf'

    case_fix = j.getconf('case_fix', mconf)

    issar = False
    if partition == 'system' and saro():
        issar = True

    perm = os.stat(indir)
    fsconfig = [partition+' '+str(perm.st_uid)+' '
                + str(perm.st_gid)+' '+str(oct(perm.st_mode))[-4:]]

    try:
        b = os.getxattr(indir, "security.selinux", follow_symlinks=False)[:-1]
        con = str(b.decode('utf8'))
    except:
        con = 'u:object_r:'+partition+'_file:s0'

    if issar:
        fcontexts = ['/ '+con]
    else:
        fcontexts = ['/'+partition+' '+con]

    symlinks = []

    for i in j.findw(indir):
        if i.endswith('lost+found'):
            continue

        fname = i.replace(indir, partition)

        if os.path.islink(i):
            symlinks.append('symlink("'+os.readlink(i)+'", "/'+fname+'");')
        elif os.path.isfile(i):
            os.makedirs(os.path.dirname(fname), exist_ok=True)

            if case_fix == 'Yes' and j.findfiles(j.basename(i), os.path.dirname(fname)):
                cnt = len(j.findfiles(os.path.basename(i)+'.*', os.path.dirname(fname)))
                copyfile(i, fname+'.ex'+str(cnt)+'.srk')

                nfname = fname.replace(partition+'/', '', 1)

                ci_files = j.getconf('case_files_'+partition, uconf, l=1)
                if nfname not in ci_files:
                    j.getconf('case_files_'+partition, uconf,
                              add=ci_files+[nfname], l=1)
            else:
                copyfile(i, fname)
        elif os.path.isdir(i):
            os.makedirs(fname, exist_ok=True)

        if issar:
            fname = fname.replace(partition+'/', '', 1)

        try:
            b = os.getxattr(i, "security.selinux", follow_symlinks=False)[:-1]
            con = str(b.decode('utf8'))
        except:
            con = 'u:object_r:'+partition+'_file:s0'

        try:
            b = os.getxattr(i, "security.capability", follow_symlinks=False)
            cap = str(int.from_bytes(b[4:8] + b[12:16], "little"))
        except:
            cap = ''

        try:
            if os.path.islink(i):
                perm = os.lstat(i)
            else:
                perm = os.stat(i)
        except:
            with open(filedir+'/logs/ext4_extract.log', 'a', encoding='utf8', newline='\n') as f:
                print('ERROR: failed to get permissions for '+i, file=f)

            continue

        mode = str(oct(perm.st_mode))[-4:]
        uid = str(perm.st_uid)
        gid = str(perm.st_gid)

        fsconfig.append(' '.join(
            [fname, uid, gid, mode, ('capabilities='+cap if cap else '')]).strip())
        fcontexts.append(' '.join(['/'+fname, con]))

    j.delpath(filedir+'/symlinks-'+partition, filedir+'/fs_config-'
                + partition, filedir+'/file_contexts3-'+partition)

    if symlinks:
        j.appendf('\n'.join(sorted(symlinks)), filedir+'/symlinks-'+partition)

    j.appendf('\n'.join(sorted(fsconfig)), filedir+'/fs_config-'+partition)
    j.appendf('\n'.join(sorted(fcontexts)),
              filedir+'/file_contexts3-'+partition)
