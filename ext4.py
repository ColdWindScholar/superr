
import ctypes, functools, io, math, queue

def wcscmp(str_a, str_b):
    """
    Standard library wcscmp
    """
    for a, b in zip(str_a, str_b):
        tmp = ord(a) - ord(b)
        if tmp != 0:
            if tmp < 0:
                return -1
            else:
                return 1

    tmp = len(str_a) - len(str_b)
    if tmp < 0:
        return -1
    if tmp > 0:
        return 1
    return 0


class Ext4Error(Exception):
    __doc__ = '\n    Base class for all custom errors\n    '


class BlockMapError(Ext4Error):
    __doc__ = '\n    Raised, when a requested file_block is not mapped to disk\n    '


class EndOfStreamError(Ext4Error):
    __doc__ = "\n    Raised, when BlockReader reads beyond the end of the volume's underlying stream\n    "


class MagicError(Ext4Error):
    __doc__ = '\n    Raised, when a structures magic value is wrong and ignore_magic is False\n    '


class ext4_struct(ctypes.LittleEndianStructure):
    __doc__ = '\n    Simplifies access to *_lo and *_hi fields\n    '

    def __getattr__(self, name):
        """
        Enables reading *_lo and *_hi fields together.
        """
        try:
            lo_field = ctypes.LittleEndianStructure.__getattribute__(type(self), name + '_lo')
            size = lo_field.size
            lo = lo_field.__get__(self)
            hi = ctypes.LittleEndianStructure.__getattribute__(self, name + '_hi')
            return hi << 8 * size | lo
        except AttributeError:
            return ctypes.LittleEndianStructure.__getattribute__(self, name)

    def __setattr__(self, name, value):
        """
        Enables setting *_lo and *_hi fields together.
        """
        try:
            lo_field = lo_field = ctypes.LittleEndianStructure.__getattribute__(type(self), name + '_lo')
            size = lo_field.size
            lo_field.__set__(self, value & (1 << 8 * size) - 1)
            ctypes.LittleEndianStructure.__setattr__(self, name + '_hi', value >> 8 * size)
        except AttributeError:
            ctypes.LittleEndianStructure.__setattr__(self, name, value)


class ext4_dir_entry_2(ext4_struct):
    _fields_ = [
     (
      'inode', ctypes.c_uint),
     (
      'rec_len', ctypes.c_ushort),
     (
      'name_len', ctypes.c_ubyte),
     (
      'file_type', ctypes.c_ubyte)]

    def _from_buffer_copy(raw, offset=0, platform64=True):
        struct = ext4_dir_entry_2.from_buffer_copy(raw, offset)
        struct.name = raw[offset + 8:offset + 8 + struct.name_len]
        return struct


class ext4_extent(ext4_struct):
    _fields_ = [
     (
      'ee_block', ctypes.c_uint),
     (
      'ee_len', ctypes.c_ushort),
     (
      'ee_start_hi', ctypes.c_ushort),
     (
      'ee_start_lo', ctypes.c_uint)]


class ext4_extent_header(ext4_struct):
    _fields_ = [
     (
      'eh_magic', ctypes.c_ushort),
     (
      'eh_entries', ctypes.c_ushort),
     (
      'eh_max', ctypes.c_ushort),
     (
      'eh_depth', ctypes.c_ushort),
     (
      'eh_generation', ctypes.c_uint)]


class ext4_extent_idx(ext4_struct):
    _fields_ = [
     (
      'ei_block', ctypes.c_uint),
     (
      'ei_leaf_lo', ctypes.c_uint),
     (
      'ei_leaf_hi', ctypes.c_ushort),
     (
      'ei_unused', ctypes.c_ushort)]


class ext4_group_descriptor(ext4_struct):
    _fields_ = [
     (
      'bg_block_bitmap_lo', ctypes.c_uint),
     (
      'bg_inode_bitmap_lo', ctypes.c_uint),
     (
      'bg_inode_table_lo', ctypes.c_uint),
     (
      'bg_free_blocks_count_lo', ctypes.c_ushort),
     (
      'bg_free_inodes_count_lo', ctypes.c_ushort),
     (
      'bg_used_dirs_count_lo', ctypes.c_ushort),
     (
      'bg_flags', ctypes.c_ushort),
     (
      'bg_exclude_bitmap_lo', ctypes.c_uint),
     (
      'bg_block_bitmap_csum_lo', ctypes.c_ushort),
     (
      'bg_inode_bitmap_csum_lo', ctypes.c_ushort),
     (
      'bg_itable_unused_lo', ctypes.c_ushort),
     (
      'bg_checksum', ctypes.c_ushort),
     (
      'bg_block_bitmap_hi', ctypes.c_uint),
     (
      'bg_inode_bitmap_hi', ctypes.c_uint),
     (
      'bg_inode_table_hi', ctypes.c_uint),
     (
      'bg_free_blocks_count_hi', ctypes.c_ushort),
     (
      'bg_free_inodes_count_hi', ctypes.c_ushort),
     (
      'bg_used_dirs_count_hi', ctypes.c_ushort),
     (
      'bg_itable_unused_hi', ctypes.c_ushort),
     (
      'bg_exclude_bitmap_hi', ctypes.c_uint),
     (
      'bg_block_bitmap_csum_hi', ctypes.c_ushort),
     (
      'bg_inode_bitmap_csum_hi', ctypes.c_ushort),
     (
      'bg_reserved', ctypes.c_uint)]

    def _from_buffer_copy(raw, platform64=True):
        struct = ext4_group_descriptor.from_buffer_copy(raw)
        if not platform64:
            struct.bg_block_bitmap_hi = 0
            struct.bg_inode_bitmap_hi = 0
            struct.bg_inode_table_hi = 0
            struct.bg_free_blocks_count_hi = 0
            struct.bg_free_inodes_count_hi = 0
            struct.bg_used_dirs_count_hi = 0
            struct.bg_itable_unused_hi = 0
            struct.bg_exclude_bitmap_hi = 0
            struct.bg_block_bitmap_csum_hi = 0
            struct.bg_inode_bitmap_csum_hi = 0
            struct.bg_reserved = 0
        return struct


class ext4_inode(ext4_struct):
    EXT2_GOOD_OLD_INODE_SIZE = 128
    S_IXOTH = 1
    S_IWOTH = 2
    S_IROTH = 4
    S_IXGRP = 8
    S_IWGRP = 16
    S_IRGRP = 32
    S_IXUSR = 64
    S_IWUSR = 128
    S_IRUSR = 256
    S_ISVTX = 512
    S_ISGID = 1024
    S_ISUID = 2048
    S_IFIFO = 4096
    S_IFCHR = 8192
    S_IFDIR = 16384
    S_IFBLK = 24576
    S_IFREG = 32768
    S_IFLNK = 40960
    S_IFSOCK = 49152
    EXT4_INDEX_FL = 4096
    EXT4_EXTENTS_FL = 524288
    EXT4_EA_INODE_FL = 2097152
    EXT4_INLINE_DATA_FL = 268435456
    _fields_ = [
     (
      'i_mode', ctypes.c_ushort),
     (
      'i_uid_lo', ctypes.c_ushort),
     (
      'i_size_lo', ctypes.c_uint),
     (
      'i_atime', ctypes.c_uint),
     (
      'i_ctime', ctypes.c_uint),
     (
      'i_mtime', ctypes.c_uint),
     (
      'i_dtime', ctypes.c_uint),
     (
      'i_gid_lo', ctypes.c_ushort),
     (
      'i_links_count', ctypes.c_ushort),
     (
      'i_blocks_lo', ctypes.c_uint),
     (
      'i_flags', ctypes.c_uint),
     (
      'osd1', ctypes.c_uint),
     (
      'i_block', ctypes.c_uint * 15),
     (
      'i_generation', ctypes.c_uint),
     (
      'i_file_acl_lo', ctypes.c_uint),
     (
      'i_size_hi', ctypes.c_uint),
     (
      'i_obso_faddr', ctypes.c_uint),
     (
      'i_osd2_blocks_high', ctypes.c_ushort),
     (
      'i_file_acl_hi', ctypes.c_ushort),
     (
      'i_uid_hi', ctypes.c_ushort),
     (
      'i_gid_hi', ctypes.c_ushort),
     (
      'i_osd2_checksum_lo', ctypes.c_ushort),
     (
      'i_osd2_reserved', ctypes.c_ushort),
     (
      'i_extra_isize', ctypes.c_ushort),
     (
      'i_checksum_hi', ctypes.c_ushort),
     (
      'i_ctime_extra', ctypes.c_uint),
     (
      'i_mtime_extra', ctypes.c_uint),
     (
      'i_atime_extra', ctypes.c_uint),
     (
      'i_crtime', ctypes.c_uint),
     (
      'i_crtime_extra', ctypes.c_uint),
     (
      'i_version_hi', ctypes.c_uint),
     (
      'i_projid', ctypes.c_uint)]


class ext4_superblock(ext4_struct):
    EXT2_DESC_SIZE = 32
    INCOMPAT_64BIT = 128
    INCOMPAT_FILETYPE = 2
    _fields_ = [
     (
      's_inodes_count', ctypes.c_uint),
     (
      's_blocks_count_lo', ctypes.c_uint),
     (
      's_r_blocks_count_lo', ctypes.c_uint),
     (
      's_free_blocks_count_lo', ctypes.c_uint),
     (
      's_free_inodes_count', ctypes.c_uint),
     (
      's_first_data_block', ctypes.c_uint),
     (
      's_log_block_size', ctypes.c_uint),
     (
      's_log_cluster_size', ctypes.c_uint),
     (
      's_blocks_per_group', ctypes.c_uint),
     (
      's_clusters_per_group', ctypes.c_uint),
     (
      's_inodes_per_group', ctypes.c_uint),
     (
      's_mtime', ctypes.c_uint),
     (
      's_wtime', ctypes.c_uint),
     (
      's_mnt_count', ctypes.c_ushort),
     (
      's_max_mnt_count', ctypes.c_ushort),
     (
      's_magic', ctypes.c_ushort),
     (
      's_state', ctypes.c_ushort),
     (
      's_errors', ctypes.c_ushort),
     (
      's_minor_rev_level', ctypes.c_ushort),
     (
      's_lastcheck', ctypes.c_uint),
     (
      's_checkinterval', ctypes.c_uint),
     (
      's_creator_os', ctypes.c_uint),
     (
      's_rev_level', ctypes.c_uint),
     (
      's_def_resuid', ctypes.c_ushort),
     (
      's_def_resgid', ctypes.c_ushort),
     (
      's_first_ino', ctypes.c_uint),
     (
      's_inode_size', ctypes.c_ushort),
     (
      's_block_group_nr', ctypes.c_ushort),
     (
      's_feature_compat', ctypes.c_uint),
     (
      's_feature_incompat', ctypes.c_uint),
     (
      's_feature_ro_compat', ctypes.c_uint),
     (
      's_uuid', ctypes.c_ubyte * 16),
     (
      's_volume_name', ctypes.c_char * 16),
     (
      's_last_mounted', ctypes.c_char * 64),
     (
      's_algorithm_usage_bitmap', ctypes.c_uint),
     (
      's_prealloc_blocks', ctypes.c_ubyte),
     (
      's_prealloc_dir_blocks', ctypes.c_ubyte),
     (
      's_reserved_gdt_blocks', ctypes.c_ushort),
     (
      's_journal_uuid', ctypes.c_ubyte * 16),
     (
      's_journal_inum', ctypes.c_uint),
     (
      's_journal_dev', ctypes.c_uint),
     (
      's_last_orphan', ctypes.c_uint),
     (
      's_hash_seed', ctypes.c_uint * 4),
     (
      's_def_hash_version', ctypes.c_ubyte),
     (
      's_jnl_backup_type', ctypes.c_ubyte),
     (
      's_desc_size', ctypes.c_ushort),
     (
      's_default_mount_opts', ctypes.c_uint),
     (
      's_first_meta_bg', ctypes.c_uint),
     (
      's_mkfs_time', ctypes.c_uint),
     (
      's_jnl_blocks', ctypes.c_uint * 17),
     (
      's_blocks_count_hi', ctypes.c_uint),
     (
      's_r_blocks_count_hi', ctypes.c_uint),
     (
      's_free_blocks_count_hi', ctypes.c_uint),
     (
      's_min_extra_isize', ctypes.c_ushort),
     (
      's_want_extra_isize', ctypes.c_ushort),
     (
      's_flags', ctypes.c_uint),
     (
      's_raid_stride', ctypes.c_ushort),
     (
      's_mmp_interval', ctypes.c_ushort),
     (
      's_mmp_block', ctypes.c_ulonglong),
     (
      's_raid_stripe_width', ctypes.c_uint),
     (
      's_log_groups_per_flex', ctypes.c_ubyte),
     (
      's_checksum_type', ctypes.c_ubyte),
     (
      's_reserved_pad', ctypes.c_ushort),
     (
      's_kbytes_written', ctypes.c_ulonglong),
     (
      's_snapshot_inum', ctypes.c_uint),
     (
      's_snapshot_id', ctypes.c_uint),
     (
      's_snapshot_r_blocks_count', ctypes.c_ulonglong),
     (
      's_snapshot_list', ctypes.c_uint),
     (
      's_error_count', ctypes.c_uint),
     (
      's_first_error_time', ctypes.c_uint),
     (
      's_first_error_ino', ctypes.c_uint),
     (
      's_first_error_block', ctypes.c_ulonglong),
     (
      's_first_error_func', ctypes.c_ubyte * 32),
     (
      's_first_error_line', ctypes.c_uint),
     (
      's_last_error_time', ctypes.c_uint),
     (
      's_last_error_ino', ctypes.c_uint),
     (
      's_last_error_line', ctypes.c_uint),
     (
      's_last_error_block', ctypes.c_ulonglong),
     (
      's_last_error_func', ctypes.c_ubyte * 32),
     (
      's_mount_opts', ctypes.c_ubyte * 64),
     (
      's_usr_quota_inum', ctypes.c_uint),
     (
      's_grp_quota_inum', ctypes.c_uint),
     (
      's_overhead_blocks', ctypes.c_uint),
     (
      's_backup_bgs', ctypes.c_uint * 2),
     (
      's_encrypt_algos', ctypes.c_ubyte * 4),
     (
      's_encrypt_pw_salt', ctypes.c_ubyte * 16),
     (
      's_lpf_ino', ctypes.c_uint),
     (
      's_prj_quota_inum', ctypes.c_uint),
     (
      's_checksum_seed', ctypes.c_uint),
     (
      's_reserved', ctypes.c_uint * 98),
     (
      's_checksum', ctypes.c_uint)]

    def _from_buffer_copy(raw, platform64=True):
        struct = ext4_superblock.from_buffer_copy(raw)
        if not platform64:
            struct.s_blocks_count_hi = 0
            struct.s_r_blocks_count_hi = 0
            struct.s_free_blocks_count_hi = 0
            struct.s_min_extra_isize = 0
            struct.s_want_extra_isize = 0
            struct.s_flags = 0
            struct.s_raid_stride = 0
            struct.s_mmp_interval = 0
            struct.s_mmp_block = 0
            struct.s_raid_stripe_width = 0
            struct.s_log_groups_per_flex = 0
            struct.s_checksum_type = 0
            struct.s_reserved_pad = 0
            struct.s_kbytes_written = 0
            struct.s_snapshot_inum = 0
            struct.s_snapshot_id = 0
            struct.s_snapshot_r_blocks_count = 0
            struct.s_snapshot_list = 0
            struct.s_error_count = 0
            struct.s_first_error_time = 0
            struct.s_first_error_ino = 0
            struct.s_first_error_block = 0
            struct.s_first_error_func = 0
            struct.s_first_error_line = 0
            struct.s_last_error_time = 0
            struct.s_last_error_ino = 0
            struct.s_last_error_line = 0
            struct.s_last_error_block = 0
            struct.s_last_error_func = 0
            struct.s_mount_opts = 0
            struct.s_usr_quota_inum = 0
            struct.s_grp_quota_inum = 0
            struct.s_overhead_blocks = 0
            struct.s_backup_bgs = 0
            struct.s_encrypt_algos = 0
            struct.s_encrypt_pw_salt = 0
            struct.s_lpf_ino = 0
            struct.s_prj_quota_inum = 0
            struct.s_checksum_seed = 0
            struct.s_reserved = 0
            struct.s_checksum = 0
        if struct.s_feature_incompat & ext4_superblock.INCOMPAT_64BIT == 0:
            struct.s_desc_size = ext4_superblock.EXT2_DESC_SIZE
        return struct


class ext4_xattr_entry(ext4_struct):
    _fields_ = [
     (
      'e_name_len', ctypes.c_ubyte),
     (
      'e_name_index', ctypes.c_ubyte),
     (
      'e_value_offs', ctypes.c_ushort),
     (
      'e_value_inum', ctypes.c_uint),
     (
      'e_value_size', ctypes.c_uint),
     (
      'e_hash', ctypes.c_uint)]

    def _from_buffer_copy(raw, offset=0, platform64=True):
        struct = ext4_xattr_entry.from_buffer_copy(raw, offset)
        struct.e_name = raw[offset + 16:offset + 16 + struct.e_name_len]
        return struct

    @property
    def _size(self):
        return 4 * ((ctypes.sizeof(type(self)) + self.e_name_len + 3) // 4)


class ext4_xattr_header(ext4_struct):
    _fields_ = [
     (
      'h_magic', ctypes.c_uint),
     (
      'h_refcount', ctypes.c_uint),
     (
      'h_blocks', ctypes.c_uint),
     (
      'h_hash', ctypes.c_uint),
     (
      'h_checksum', ctypes.c_uint),
     (
      'h_reserved', ctypes.c_uint * 3)]


class ext4_xattr_ibody_header(ext4_struct):
    _fields_ = [
     (
      'h_magic', ctypes.c_uint)]


class InodeType:
    UNKNOWN = 0
    FILE = 1
    DIRECTORY = 2
    CHARACTER_DEVICE = 3
    BLOCK_DEVICE = 4
    FIFO = 5
    SOCKET = 6
    SYMBOLIC_LINK = 7
    CHECKSUM = 222


class MappingEntry:
    __doc__ = '\n    Helper class: This class maps block_count file blocks indexed by file_block_idx to the associated disk blocks indexed\n    by disk_block_idx.\n    '

    def __init__(self, file_block_idx, disk_block_idx, block_count=1):
        """
        Initialize a MappingEntry instance with given file_block_idx, disk_block_idx and block_count.
        """
        self.file_block_idx = file_block_idx
        self.disk_block_idx = disk_block_idx
        self.block_count = block_count

    def __iter__(self):
        """
        Can be used to convert an MappingEntry into a tuple (file_block_idx, disk_block_idx, block_count).
        """
        yield self.file_block_idx
        yield self.disk_block_idx
        yield self.block_count

    def __repr__(self):
        return '{type:s}({file_block_idx!r:s}, {disk_block_idx!r:s}, {blocK_count!r:s})'.format(blocK_count=self.block_count, disk_block_idx=self.disk_block_idx, file_block_idx=self.file_block_idx, type=type(self).__name__)

    def copy(self):
        return MappingEntry(self.file_block_idx, self.disk_block_idx, self.block_count)

    def create_mapping(*entries):
        """
        Converts a list of 2-tuples (disk_block_idx, block_count) into a list of MappingEntry instances
        """
        file_block_idx = 0
        result = [None] * len(entries)
        for i, entry in enumerate(entries):
            disk_block_idx, block_count = entry
            result[i] = MappingEntry(file_block_idx, disk_block_idx, block_count)
            file_block_idx += block_count

        return result

    def optimize(entries):
        """
        Sorts and stiches together a list of MappingEntry instances
        """
        entries.sort(key=(lambda entry: entry.file_block_idx))
        idx = 0
        while idx < len(entries):
            while idx + 1 < len(entries) and entries[idx].file_block_idx + entries[idx].block_count == entries[idx + 1].file_block_idx and entries[idx].disk_block_idx + entries[idx].block_count == entries[idx + 1].disk_block_idx:
                tmp = entries.pop(idx + 1)
                entries[idx].block_count += tmp.block_count

            idx += 1


class Volume:
    __doc__ = '\n    Provides functionality for reading ext4 volumes\n    '
    ROOT_INODE = 2

    def __init__(self, stream, offset=0, ignore_flags=False, ignore_magic=False):
        """
        Initializes a new ext4 reader at a given offset in stream. If ignore_magic is True, no exception will be thrown,
        when a structure with wrong magic number is found. Analogously passing True to ignore_flags suppresses Exception
        caused by wrong flags.
        """
        self.ignore_flags = ignore_flags
        self.ignore_magic = ignore_magic
        self.offset = offset
        self.platform64 = True
        self.stream = stream
        self.superblock = self.read_struct(ext4_superblock, 1024)
        self.platform64 = self.superblock.s_feature_incompat & ext4_superblock.INCOMPAT_64BIT != 0
        if not ignore_magic and self.superblock.s_magic != 61267:
            raise MagicError('Invalid magic value in superblock: 0x{magic:04X} (expected 0xEF53)'.format(magic=self.superblock.s_magic))
        self.group_descriptors = [
         None] * (self.superblock.s_inodes_count // self.superblock.s_inodes_per_group)
        group_desc_table_offset = (1024 // self.block_size + 1) * self.block_size
        for group_desc_idx in range(len(self.group_descriptors)):
            group_desc_offset = group_desc_table_offset + group_desc_idx * self.superblock.s_desc_size
            self.group_descriptors[group_desc_idx] = self.read_struct(ext4_group_descriptor, group_desc_offset)

    def __repr__(self):
        return '{type_name:s}(volume_name = {volume_name!r:s}, uuid = {uuid!r:s}, last_mounted = {last_mounted!r:s})'.format(last_mounted=self.superblock.s_last_mounted, type_name=type(self).__name__, uuid=self.uuid, volume_name=self.superblock.s_volume_name)

    @property
    def block_size(self):
        """
        Returns the volume's block size in bytes.
        """
        return 1 << 10 + self.superblock.s_log_block_size

    def get_inode(self, inode_idx, file_type=InodeType.UNKNOWN):
        """
        Returns an Inode instance representing the inode specified by its index inode_idx.
        """
        group_idx, inode_table_entry_idx = self.get_inode_group(inode_idx)
        inode_table_offset = self.group_descriptors[group_idx].bg_inode_table * self.block_size
        inode_offset = inode_table_offset + inode_table_entry_idx * self.superblock.s_inode_size
        return Inode(self, inode_offset, inode_idx, file_type)

    def get_inode_group(self, inode_idx):
        """
        Returns a tuple (group_idx, inode_table_entry_idx)
        """
        group_idx = (inode_idx - 1) // self.superblock.s_inodes_per_group
        inode_table_entry_idx = (inode_idx - 1) % self.superblock.s_inodes_per_group
        return (group_idx, inode_table_entry_idx)

    def read(self, offset, byte_len):
        """
        Returns byte_len bytes at offset within this volume.
        """
        if self.offset + offset != self.stream.tell():
            self.stream.seek(self.offset + offset, io.SEEK_SET)
        return self.stream.read(byte_len)

    def read_struct(self, structure, offset, platform64=None):
        """
        Interprets the bytes at offset as structure and returns the interpreted instance
        """
        raw = self.read(offset, ctypes.sizeof(structure))
        if hasattr(structure, '_from_buffer_copy'):
            return structure._from_buffer_copy(raw, platform64=platform64 if platform64 != None else self.platform64)
        else:
            return structure.from_buffer_copy(raw)

    @property
    def root(self):
        """
        Returns the volume's root inode
        """
        return self.get_inode(Volume.ROOT_INODE, InodeType.DIRECTORY)

    @property
    def uuid(self):
        """
        Returns the volume's UUID in the format XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX.
        """
        uuid = self.superblock.s_uuid
        uuid = [uuid[:4], uuid[4:6], uuid[6:8], uuid[8:10], uuid[10:]]
        return '-'.join()


class Inode:
    __doc__ = '\n    Provides functionality for parsing inodes and accessing their raw data\n    '

    def __init__(self, volume, offset, inode_idx, file_type=InodeType.UNKNOWN):
        """
        Initializes a new inode parser at the specified offset within the specified volume. file_type is the file type
        of the inode as given by the directory entry referring to this inode.
        """
        self.inode_idx = inode_idx
        self.offset = offset
        self.volume = volume
        self.file_type = file_type
        self.inode = volume.read_struct(ext4_inode, offset)

    def __len__(self):
        """
        Returns the length in bytes of the content referenced by this inode.
        """
        return self.inode.i_size

    def __repr__(self):
        if self.inode_idx != None:
            return '{type_name:s}(inode_idx = {inode!r:s}, offset = 0x{offset:X}, volume_uuid = {uuid!r:s})'.format(inode=self.inode_idx, offset=self.offset, type_name=type(self).__name__, uuid=self.volume.uuid)
        else:
            return '{type_name:s}(offset = 0x{offset:X}, volume_uuid = {uuid!r:s})'.format(offset=self.offset, type_name=type(self).__name__, uuid=self.volume.uuid)

    def _parse_xattrs(self, raw_data, offset, prefix_override={}):
        """
        Generator: Parses raw_data (bytes) as ext4_xattr_entry structures and their referenced xattr values and yields
        tuples (xattr_name, xattr_value) where xattr_name (str) is the attribute name including its prefix and
        xattr_value (bytes) is the raw attribute value.
        raw_data must start with the first ext4_xattr_entry structure and offset specifies the offset to the "block start"
        for ext4_xattr_entry.e_value_offs.
        prefix_overrides allows specifying attributes apart from the default prefixes. The default prefix dictionary is
        updated with prefix_overrides.
        """
        prefixes = {
         0: '', 
         1: 'user.', 
         2: 'system.posix_acl_access', 
         3: 'system.posix_acl_default', 
         4: 'trusted.', 
         6: 'security.', 
         7: 'system.', 
         8: 'system.richacl'}
        prefixes.update(prefixes)
        i = 0
        while i < len(raw_data):
            xattr_entry = ext4_xattr_entry._from_buffer_copy(raw_data, i, platform64=self.volume.platform64)
            if xattr_entry.e_name_len | xattr_entry.e_name_index | xattr_entry.e_value_offs | xattr_entry.e_value_inum == 0:
                break
            if xattr_entry.e_name_index not in prefixes:
                raise Ext4Error('Unknown attribute prefix {prefix:d} in inode {inode:d}'.format(inode=self.inode_idx, prefix=xattr_entry.e_name_index))
            xattr_name = prefixes[xattr_entry.e_name_index] + xattr_entry.e_name.decode('iso-8859-2')
            if xattr_entry.e_value_inum != 0:
                xattr_inode = self.volume.get_inode(xattr_entry.e_value_inum, InodeType.FILE)
                if not self.volume.ignore_flags and xattr_inode.inode.i_flags & ext4_inode.EXT4_EA_INODE_FL != 0:
                    raise Ext4Error('Inode {value_indoe:d} associated with the extended attribute {xattr_name!r:s} of inode {inode:d} is not marked as large extended attribute value.'.format(inode=self.inode_idx, value_inode=xattr_inode.inode_idx, xattr_name=xattr_name))
                xattr_value = xattr_inode.open_read().read()
            else:
                xattr_value = raw_data[xattr_entry.e_value_offs + offset:xattr_entry.e_value_offs + offset + xattr_entry.e_value_size]
            yield (xattr_name, xattr_value)
            i += xattr_entry._size

    def directory_entry_comparator(dir_a, dir_b):
        """
        Sort-key for directory entries. It sortes entries in a way that directories come before anything else and within
        a group (directory / anything else) entries are sorted by their lower-case name. Entries whose lower-case names
        are equal are sorted by their actual names.
        """
        file_name_a, _, file_type_a = dir_a
        file_name_b, _, file_type_b = dir_b
        if file_type_a == InodeType.DIRECTORY == file_type_b or file_type_a != InodeType.DIRECTORY != file_type_b:
            tmp = wcscmp(file_name_a.lower(), file_name_b.lower())
            if tmp != 0:
                return tmp
            return wcscmp(file_name_a, file_name_b)
        else:
            if file_type_a == InodeType.DIRECTORY:
                return -1
            return 1

    directory_entry_key = functools.cmp_to_key(directory_entry_comparator)

    def get_inode(self, *relative_path, decode_name=None):
        r"""
        Returns the inode specified by the path relative_path (list of entry names) relative to this inode. "." and ".."
        usually are supported too, however in special cases (e.g. manually crafted volumes) they might not be supported
        due to them being real on-disk directory entries that might be missing or pointing somewhere else.
        decode_name is directly passed to open_dir.
        NOTE: Whitespaces will not be trimmed off the path's parts and "\0" and "\0\0" as well as b"\0" and b"\0\0" are
        seen as different names (unless decode_name actually trims the name).
        NOTE: Along the path file_type != FILETYPE_DIR will be ignored, however i_flags will not be ignored.
        """
        if not self.is_dir:
            raise Ext4Error('Inode {inode:d} is not a directory.'.format(inode=self.inode_idx))
        current_inode = self
        for i, part in enumerate(relative_path):
            if not self.volume.ignore_flags and not current_inode.is_dir:
                current_path = '/'.join(relative_path[:i])
                raise Ext4Error('{current_path!r:s} (Inode {inode:d}) is not a directory.'.format(current_path=current_path, inode=inode_idx))
            file_name, inode_idx, file_type = next(filter((lambda entry: entry[0] == part), current_inode.open_dir(decode_name)), (None,
                                                                                                                                   None,
                                                                                                                                   None))
            if inode_idx == None:
                current_path = '/'.join(relative_path[:i])
                raise FileNotFoundError('{part!r:s} not found in {current_path!r:s} (Inode {inode:d}).'.format(current_path=current_path, inode=current_inode.inode_idx, part=part))
            current_inode = current_inode.volume.get_inode(inode_idx, file_type)

        return current_inode

    @property
    def is_dir(self):
        """
        Indicates whether the inode is marked as a directory.
        """
        if self.volume.superblock.s_feature_incompat & ext4_superblock.INCOMPAT_FILETYPE == 0:
            return self.inode.i_mode & ext4_inode.S_IFDIR != 0
        else:
            return self.file_type == InodeType.DIRECTORY

    @property
    def is_file(self):
        """
        Indicates whether the inode is marker as a regular file.
        """
        if self.volume.superblock.s_feature_incompat & ext4_dir_entry_2.INCOMPAT_FILETYPE == 0:
            return self.inode.i_mode & ext4_inode.S_IFREG != 0
        else:
            return self.file_type == InodeType.FILE

    @property
    def is_in_use(self):
        """
        Indicates whether the inode's associated bit in the inode bitmap is set.
        """
        group_idx, bitmap_bit = self.volume.get_inode_group(self.inode_idx)
        inode_usage_bitmap_offset = self.volume.group_descriptors[group_idx].bg_inode_bitmap * self.volume.block_size
        inode_usage_byte = self.volume.read(inode_usage_bitmap_offset + bitmap_bit // 8, 1)[0]
        return inode_usage_byte >> 7 - bitmap_bit % 8 & 1 != 0

    @property
    def mode_str(self):
        """
        Returns the inode's permissions in form of a unix string (e.g. "-rwxrw-rw" or "drwxr-xr--").
        """
        special_flag = lambda letter, execute, special: {(False, False): '-', 
         (False, True): letter.upper(), 
         (True, False): 'x', 
         (True, True): letter.lower()}[(
         execute, special)]
        try:
            if self.volume.superblock.s_feature_incompat & ext4_superblock.INCOMPAT_FILETYPE == 0:
                device_type = {ext4_inode.S_IFIFO: 'p', 
                 ext4_inode.S_IFCHR: 'c', 
                 ext4_inode.S_IFDIR: 'd', 
                 ext4_inode.S_IFBLK: 'b', 
                 ext4_inode.S_IFREG: '-', 
                 ext4_inode.S_IFLNK: 'l', 
                 ext4_inode.S_IFSOCK: 's'}[self.inode.i_mode & 61440]
            else:
                device_type = {InodeType.FILE: '-', 
                 InodeType.DIRECTORY: 'd', 
                 InodeType.CHARACTER_DEVICE: 'c', 
                 InodeType.BLOCK_DEVICE: 'b', 
                 InodeType.FIFO: 'p', 
                 InodeType.SOCKET: 's', 
                 InodeType.SYMBOLIC_LINK: 'l'}[self.file_type]
        except KeyError:
            device_type = '?'

        return ''.join([
         device_type,
         'r' if self.inode.i_mode & ext4_inode.S_IRUSR != 0 else '-',
         'w' if self.inode.i_mode & ext4_inode.S_IWUSR != 0 else '-',
         special_flag('s', self.inode.i_mode & ext4_inode.S_IXUSR != 0, self.inode.i_mode & ext4_inode.S_ISUID != 0),
         'r' if self.inode.i_mode & ext4_inode.S_IRGRP != 0 else '-',
         'w' if self.inode.i_mode & ext4_inode.S_IWGRP != 0 else '-',
         special_flag('s', self.inode.i_mode & ext4_inode.S_IXGRP != 0, self.inode.i_mode & ext4_inode.S_ISGID != 0),
         'r' if self.inode.i_mode & ext4_inode.S_IROTH != 0 else '-',
         'w' if self.inode.i_mode & ext4_inode.S_IWOTH != 0 else '-',
         special_flag('t', self.inode.i_mode & ext4_inode.S_IXOTH != 0, self.inode.i_mode & ext4_inode.S_ISVTX != 0)])

    def open_dir(self, decode_name=None):
        """
        Generator: Yields the directory entries as tuples (decode_name(name), inode, file_type) in their on-disk order,
        where name is the raw on-disk directory entry name (bytes). file_type is one of the Inode.IT_* constants. For
        special cases (e.g. invalid utf8 characters in entry names) you can try a different decoder (e.g.
        decode_name = lambda raw: raw).
        Default of decode_name = lambda raw: raw.decode("utf8")
        """
        if decode_name == None:
            decode_name = lambda raw: raw.decode('utf8')
        if not self.volume.ignore_flags and not self.is_dir:
            raise Ext4Error('Inode ({inode:d}) is not a directory.'.format(inode=self.inode_idx))
        if self.inode.i_flags & ext4_inode.EXT4_INDEX_FL != 0:
            raise NotImplementedError('Hash trees are not implemented yet.')
        raw_data = self.open_read().read()
        offset = 0
        while offset < len(raw_data):
            dirent = ext4_dir_entry_2._from_buffer_copy(raw_data, offset, platform64=self.volume.platform64)
            if dirent.file_type != InodeType.CHECKSUM:
                yield (
                 decode_name(dirent.name), dirent.inode, dirent.file_type)
            offset += dirent.rec_len

    def open_read(self):
        """
        Returns an BlockReader instance for reading this inode's raw content.
        """
        if self.inode.i_flags & ext4_inode.EXT4_EXTENTS_FL != 0:
            mapping = []
            nodes = queue.Queue()
            nodes.put_nowait(self.offset + ext4_inode.i_block.offset)
            while nodes.qsize() != 0:
                header_offset = nodes.get_nowait()
                header = self.volume.read_struct(ext4_extent_header, header_offset)
                if not self.volume.ignore_magic and header.eh_magic != 62218:
                    raise MagicError('Invalid magic value in extent header at offset 0x{header_offset:X} of inode {inode:d}: 0x{header_magic:04X} (expected 0xF30A)'.format(header_magic=header.eh_magic, header_offset=self.inode_idx, inode=self.inode_idx))
                if header.eh_depth != 0:
                    indices = self.volume.read_struct(ext4_extent_idx * header.eh_entries, header_offset + ctypes.sizeof(ext4_extent_header))
                    for idx in indices:
                        nodes.put_nowait(idx.ei_leaf * self.volume.block_size)

                else:
                    extents = self.volume.read_struct(ext4_extent * header.eh_entries, header_offset + ctypes.sizeof(ext4_extent_header))
                    for extent in extents:
                        mapping.append(MappingEntry(extent.ee_block, extent.ee_start, extent.ee_len))

            MappingEntry.optimize(mapping)
            return BlockReader(self.volume, len(self), mapping)
        else:
            i_block = self.volume.read(self.offset + ext4_inode.i_block.offset, ext4_inode.i_block.size)
            return io.BytesIO(i_block[:self.inode.i_size])

    @property
    def size_readable(self):
        """
        Returns the inode's content length in a readable format (e.g. "123 bytes", "2.03 KiB" or "3.00 GiB"). Possible
        units are bytes, KiB, MiB, GiB, TiB, PiB, EiB, ZiB, YiB.
        """
        if self.inode.i_size < 1024:
            if self.inode.i_size != 1:
                return '{0:d} bytes'.format(self.inode.i_size)
            return '1 byte'
        else:
            units = [
             "'KiB'", "'MiB'", "'GiB'", "'TiB'", "'PiB'", 
             "'EiB'", "'ZiB'", "'YiB'"]
            unit_idx = min(int(math.log(self.inode.i_size, 1024)), len(units))
            return '{size:.2f} {unit:s}'.format(size=self.inode.i_size / 1024 ** unit_idx, unit=units[unit_idx - 1])

    def xattrs(self, check_inline=True, check_block=True, force_inline=False, prefix_override={}):
        """
        Generator: Yields the inode's extended attributes as tuples (name, value) in their on-disk order, where name (str)
        is the on-disk attribute name including its resolved name prefix and value (bytes) is the raw attribute value.
        check_inline and check_block control where to read attributes (the inode's inline data and/or the external data block
        pointed to by i_file_acl) and if check_inline as well as force_inline are set to True, the inode's inline data
        will not be verified to contain actual extended attributes and instead is just interpreted as such. prefix_overrides
        is directly passed to Inode._parse_xattrs.
        """
        inline_data_offset = self.offset + ext4_inode.EXT2_GOOD_OLD_INODE_SIZE + self.inode.i_extra_isize
        inline_data_length = self.offset + self.volume.superblock.s_inode_size - inline_data_offset
        if check_inline and inline_data_length > ctypes.sizeof(ext4_xattr_ibody_header):
            inline_data = self.volume.read(inline_data_offset, inline_data_length)
            xattrs_header = ext4_xattr_ibody_header.from_buffer_copy(inline_data)
            if force_inline or xattrs_header.h_magic == 3925999616:
                offset = 4 * ((ctypes.sizeof(ext4_xattr_ibody_header) + 3) // 4)
                for xattr_name, xattr_value in self._parse_xattrs(inline_data[offset:], 0, prefix_override=prefix_override):
                    yield (
                     xattr_name, xattr_value)

        if check_block and self.inode.i_file_acl != 0:
            xattrs_block_start = self.inode.i_file_acl * self.volume.block_size
            xattrs_block = self.volume.read(xattrs_block_start, self.volume.block_size)
            xattrs_header = ext4_xattr_header.from_buffer_copy(xattrs_block)
            if not self.volume.ignore_magic and xattrs_header.h_magic != 3925999616:
                raise MagicError('Invalid magic value in xattrs block header at offset 0x{xattrs_block_start:X} of inode {inode:d}: 0x{xattrs_header} (expected 0xEA020000)'.format(inode=self.inode_idx, xattrs_block_start=xattrs_block_start, xattrs_header=xattrs_header.h_magic))
            if xattrs_header.h_blocks != 1:
                raise Ext4Error('Invalid number of xattr blocks at offset 0x{xattrs_block_start:X} of inode {inode:d}: {xattrs_header:d} (expected 1)'.format(inode=self.inode_idx, xattrs_header=xattrs_header.h_blocks, xattrs_block_start=xattrs_block_start))
            offset = 4 * ((ctypes.sizeof(ext4_xattr_header) + 3) // 4)
            for xattr_name, xattr_value in self._parse_xattrs(xattrs_block[offset:], -offset, prefix_override=prefix_override):
                yield (
                 xattr_name, xattr_value)


class BlockReader:
    __doc__ = '\n    Maps disk blocks into a linear byte stream.\n    NOTE: This class does not implement buffering or caching.\n    '
    EINVAL = 22

    def __init__(self, volume, byte_size, block_map):
        """
        Initializes a new block reader on the specified volume. mapping must be a list of MappingEntry instances. If
        you prefer a way to use 2-tuples (disk_block_idx, block_count) with inferred file_block_index entries, see
        MappingEntry.create_mapping.
        """
        self.byte_size = byte_size
        self.volume = volume
        self.cursor = 0
        block_map = list(map(MappingEntry.copy, block_map))
        MappingEntry.optimize(block_map)
        self.block_map = block_map

    def __repr__(self):
        return '{type_name:s}(byte_size = {size!r:s}, block_map = {block_map!r:s}, volume_uuid = {uuid!r:s})'.format(block_map=self.block_map, size=self.byte_size, type_name=type(self).__name__, uuid=self.volume.uuid)

    def get_block_mapping(self, file_block_idx):
        """
        Returns the disk block index of the file block specified by file_block_idx.
        """
        disk_block_idx = None
        for entry in self.block_map:
            if entry.file_block_idx <= file_block_idx < entry.file_block_idx + entry.block_count:
                block_diff = file_block_idx - entry.file_block_idx
                disk_block_idx = entry.disk_block_idx + block_diff
                break

        return disk_block_idx

    def read(self, byte_len=-1):
        """
        Reades up to byte_len bytes from the block device beginning at the cursor's current position. This operation will
        not exceed the inode's size. If -1 is passed for byte_len, the inode is read to the end.
        """
        if byte_len < -1:
            raise ValueError('byte_len must be non-negative or -1')
        bytes_remaining = self.byte_size - self.cursor
        byte_len = bytes_remaining if byte_len == -1 else max(0, min(byte_len, bytes_remaining))
        if byte_len == 0:
            return b''
        start_block_idx = self.cursor // self.volume.block_size
        end_block_idx = (self.cursor + byte_len - 1) // self.volume.block_size
        end_of_stream_check = byte_len
        blocks = [self.read_block(i) for i in range(start_block_idx, end_block_idx - start_block_idx + 1)]
        start_offset = self.cursor % self.volume.block_size
        if start_offset != 0:
            blocks[0] = blocks[0][start_offset:]
        byte_len = (byte_len + start_offset - self.volume.block_size - 1) % self.volume.block_size + 1
        blocks[-1] = blocks[-1][:byte_len]
        result = (b'').join(blocks)
        if len(result) != end_of_stream_check:
            raise EndOfStreamError("The volume's underlying stream ended {0:d} bytes before EOF.".format(byte_len - len(result)))
        self.cursor += len(result)
        return result

    def read_block(self, file_block_idx):
        """
        Reads one block from disk (return a zero-block if the file block is not mapped)
        """
        disk_block_idx = self.get_block_mapping(file_block_idx)
        if disk_block_idx != None:
            return self.volume.read(disk_block_idx * self.volume.block_size, self.volume.block_size)
        else:
            return bytes([0] * self.volume.block_size)

    def seek(self, seek, seek_mode=io.SEEK_SET):
        """
        Moves the internal cursor along the file (not the disk) and behaves like BufferedReader.seek
        """
        if seek_mode == io.SEEK_CUR:
            seek += self.cursor
        elif seek_mode == io.SEEK_END:
            seek += self.byte_size
        if seek < 0:
            raise OSError(BlockReader.EINVAL, 'Invalid argument')
        self.cursor = seek
        return seek

    def tell(self):
        """
        Returns the internal cursor's current file offset.
        """
        return self.cursor


class Tools:
    __doc__ = '\n    Provides helpful utility functions\n    '

    def list_dir(volume, identifier, decode_name=None, sort_key=Inode.directory_entry_key, line_format=None, file_types={
 0: 'unkn', 1: 'file', 2: 'dir', 3: 'chr', 4: 'blk', 5: 'fifo', 6: 'sock', 7: 'sym'}):
        """
        Similar to "ls -la" this function lists all entries from a directory of volume.

        identifier might be an Inode instance, an integer describing the directory's inode index, a str/bytes describing
        the directory's full path or a list of entry names. decode_name is directly passed to open_dir. See Inode.get_inode
        for more details.

        sort_key is the key-function used for sorting the directories entries. If None is passed, the call to sorted is
        omitted.

        line_format is a format string specifying each line's format or a function formatting each line. It is used as
        follows:

            line_format(
                file_name = file_name, # Entry name
                inode = volume.get_inode(inode_idx, file_type), # Referenced inode
                file_type = file_type, # Entry type (int)
                file_type_str = file_types[file_type] if file_type in file_types else "?" # Entry type (str, see next paragraph)
            )

        The default of line_format is the following function:

            def line_format (file_name, inode, file_type, file_type_str):
                if file_type == InodeType.SYMBOLIC_LINK:
                    link_target = inode.open_read().read().decode("utf8")
                    return "{mode:s}  {size: >10s}  {file_name:s}  ->  {link_target:s}".format(file_name = file_name, link_target = link_target, mode = inode.mode_str, size = inode.size_readable)
                else:
                    return "{mode:s}  {size: >10s}  {file_name:s}".format(file_name = file_name, mode = inode.mode_str, size = inode.size_readable)

        file_types is a dictionary specifying the names of the different entry types.
        """
        if isinstance(identifier, Inode):
            inode = identifier
        else:
            if isinstance(identifier, int):
                inode = volume.get_inode(identifier, InodeType.DIRECTORY)
            else:
                if isinstance(identifier, str):
                    identifier = identifier.strip(' /').split('/')
                    if len(identifier) == 1 and identifier[0] == '':
                        inode = volume.root
                    else:
                        inode = volume.root.get_inode(*identifier)
                elif isinstance(identifier, list):
                    inode = volume.root.get_inode(*identifier)
                if line_format == None:

                    def _line_format(file_name, inode, file_type, file_type_str):
                        if file_type == InodeType.SYMBOLIC_LINK:
                            link_target = inode.open_read().read().decode('utf8')
                            return '{mode:s}  {size: >10s}  {file_name:s}  ->  {link_target:s}'.format(file_name=file_name, link_target=link_target, mode=inode.mode_str, size=inode.size_readable)
                        else:
                            return '{mode:s}  {size: >10s}  {file_name:s}'.format(file_name=file_name, mode=inode.mode_str, size=inode.size_readable)

                    line_format = _line_format
                elif isinstance(line_format, str):
                    line_format = line_format.format
        entries = inode.open_dir(decode_name) if sort_key is None else sorted(inode.open_dir(decode_name), key=sort_key)
        for file_name, inode_idx, file_type in entries:
            print(line_format(file_name=file_name, inode=volume.get_inode(inode_idx, file_type), file_type=file_type, file_type_str=file_types[file_type] if file_type in file_types else '?'))
