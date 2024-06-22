#!/usr/bin/env python3

from struct import unpack, calcsize

SPARSE_HEADER_MAGIC = 0xED26FF3A
SPARSE_HEADER_SIZE = 28
SPARSE_CHUNK_HEADER_SIZE = 12

LP_PARTITION_RESERVED_BYTES = 4096
LP_METADATA_GEOMETRY_MAGIC = 0x616c4467
LP_METADATA_GEOMETRY_SIZE = 4096
LP_METADATA_HEADER_MAGIC = 0x414C5030
LP_SECTOR_SIZE = 512


class LpMetadataGeometry(object):
    """
        Offset 0: Magic signature
        Offset 4: Size of the LpMetadataGeometry
        Offset 8: SHA256 checksum
        Offset 40: Maximum amount of space a single copy of the metadata can use
        Offset 44: Number of copies of the metadata to keep
        Offset 48: Logical block size
    """

    def __init__(self, buffer):
        fmt = '<2I32s3I'
        (
            self.magic,
            self.struct_size,
            self.checksum,
            self.metadata_max_size,
            self.metadata_slot_count,
            self.logical_block_size

        ) = unpack(fmt, buffer[0:calcsize(fmt)])


class LpMetadataHeader(object):
    """
        +-----------------------------------------+
        | Header data - fixed size                |
        +-----------------------------------------+
        | Partition table - variable size         |
        +-----------------------------------------+
        | Partition table extents - variable size |
        +-----------------------------------------+
    """

    def __init__(self, buffer):
        fmt = '<I2hI32sI32s'
        (
            self.magic,
            self.major_version,
            self.minor_version,
            self.header_size,
            self.header_checksum,
            self.tables_size,
            self.tables_checksum

        ) = unpack(fmt, buffer[0:calcsize(fmt)])
        self.full_version = float(
            str(self.major_version)+'.'+str(self.minor_version))
        self.partitions = None
        self.extents = None
        self.groups = None
        self.block_devices = None
        self.flags = None


class LpMetadataHeaderFlags(object):
    def __init__(self, buffer, full_version):
        if full_version >= 10.2:
            fmt = '<I'
            (
                self.flags_index,

            ) = unpack(fmt, buffer[0:calcsize(fmt)])
        else:
            self.flags_index = 0


class LpMetadataTableDescriptor(object):
    def __init__(self, buffer):
        fmt = '<3I'
        (
            self.offset,
            self.num_entries,
            self.entry_size

        ) = unpack(fmt, buffer[:calcsize(fmt)])


class LpMetadataPartition(object):
    def __init__(self, buffer):
        fmt = '<36s4I'
        (
            self.name,
            self.attributes,
            self.first_extent_index,
            self.num_extents,
            self.group_index

        ) = unpack(fmt, buffer[0:calcsize(fmt)])


class LpMetadataExtent(object):
    def __init__(self, buffer):
        fmt = '<QIQI'
        (
            self.num_sectors,
            self.target_type,
            self.target_data,
            self.target_source

        ) = unpack(fmt, buffer[0:calcsize(fmt)])


class LpMetadataPartitionGroup(object):
    def __init__(self, buffer):
        fmt = '<36sIQ'
        (
            self.name,
            self.flags,
            self.maximum_size
        ) = unpack(fmt, buffer[0:calcsize(fmt)])


class LpMetadataBlockDevice(object):
    def __init__(self, buffer):
        fmt = '<Q2IQ36sI'
        (
            self.first_logical_sector,
            self.alignment,
            self.alignment_offset,
            self.size,
            self.partition_name,
            self.flags
        ) = unpack(fmt, buffer[0:calcsize(fmt)])


class Metadata(object):
    def __init__(self):
        self.geometry = None
        self.partitions = []
        self.extents = []
        self.groups = []
        self.block_devices = []


class LpUnpackError(Exception):
    """Raised any error unpacking"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class LpUnpack(object):
    def __init__(self, **kwargs):
        self.partition_name = kwargs.get('NAME')
        self.slot_num = None
        # self.slot_num = int(kwargs.get('NUM')) if kwargs.get('NUM') else 0
        self.in_file_fd = open(kwargs.get('SUPER_IMAGE'), 'rb')
        self.dump = kwargs.get('DUMP')
        self.out_dir = kwargs.get('OUTPUT_DIR')

    def ReadPrimaryGeometry(self):
        lpMetadataGeometry = LpMetadataGeometry(
            self.in_file_fd.read(LP_METADATA_GEOMETRY_SIZE))
        if lpMetadataGeometry is not None:
            return lpMetadataGeometry
        else:
            return self.ReadBackupGeometry()

    def ReadBackupGeometry(self):
        return LpMetadataGeometry(self.in_file_fd.read(LP_METADATA_GEOMETRY_SIZE))

    def GetPrimaryMetadataOffset(self, geometry, slot_number=0):
        return LP_PARTITION_RESERVED_BYTES + (LP_METADATA_GEOMETRY_SIZE * 2) + geometry.metadata_max_size * slot_number

    def GetBackupMetadataOffset(self, geometry, slot_number=0):
        start = LP_PARTITION_RESERVED_BYTES + (LP_METADATA_GEOMETRY_SIZE * 2) + \
            geometry.metadata_max_size * geometry.metadata_slot_count
        return start + geometry.metadata_max_size * slot_number

    def ParseHeaderMetadata(self, offsets):
        header = None
        for index, offset in enumerate(offsets):
            self.in_file_fd.seek(offset, 0)
            header = LpMetadataHeader(self.in_file_fd.read(80))
            header.partitions = LpMetadataTableDescriptor(
                self.in_file_fd.read(12))
            header.extents = LpMetadataTableDescriptor(
                self.in_file_fd.read(12))
            header.groups = LpMetadataTableDescriptor(self.in_file_fd.read(12))
            header.block_devices = LpMetadataTableDescriptor(
                self.in_file_fd.read(12))
            header.flags = LpMetadataHeaderFlags(
                self.in_file_fd.read(4), header.full_version)

            if header.magic != LP_METADATA_HEADER_MAGIC:
                if index + 1 > len(offsets):
                    raise LpUnpackError(
                        'Logical partition metadata has invalid magic value.')
                else:
                    print('Read Backup header by offset 0x{:x}'.format(
                        offsets[index + 1]))
                    continue

            self.in_file_fd.seek(offset + header.header_size, 0)

        return header

    def ReadMetadata(self):
        metadata = Metadata()
        self.in_file_fd.seek(LP_PARTITION_RESERVED_BYTES, 0)
        metadata.geometry = self.ReadPrimaryGeometry()

        if metadata.geometry.magic != LP_METADATA_GEOMETRY_MAGIC:
            raise LpUnpackError(
                'Logical partition metadata has invalid geometry magic signature.')

        if metadata.geometry.metadata_slot_count == 0:
            raise LpUnpackError(
                'Logical partition metadata has invalid slot count.')

        if metadata.geometry.metadata_max_size % LP_SECTOR_SIZE != 0:
            raise LpUnpackError('Metadata max size is not sector-aligned.')

        offsets = [self.GetPrimaryMetadataOffset(metadata.geometry, slot_number=0),  # self.slot_num
                   self.GetBackupMetadataOffset(metadata.geometry, slot_number=0)]  # self.slot_num

        metadata.header = self.ParseHeaderMetadata(offsets)

        for index in range(0, metadata.header.partitions.num_entries):
            partition = LpMetadataPartition(self.in_file_fd.read(
                metadata.header.partitions.entry_size))
            partition.name = str(partition.name, 'utf-8').strip('\x00')
            metadata.partitions.append(partition)

        for index in range(0, metadata.header.extents.num_entries):
            metadata.extents.append(LpMetadataExtent(
                self.in_file_fd.read(metadata.header.extents.entry_size)))

        for index in range(0, metadata.header.groups.num_entries):
            group = LpMetadataPartitionGroup(
                self.in_file_fd.read(metadata.header.groups.entry_size))
            group.name = str(group.name, 'utf-8').strip('\x00')
            metadata.groups.append(group)

        for index in range(0, metadata.header.block_devices.num_entries):
            block_device = LpMetadataBlockDevice(
                self.in_file_fd.read(metadata.header.block_devices.entry_size))
            block_device.partition_name = str(
                block_device.partition_name, 'utf-8').strip('\x00')
            metadata.block_devices.append(block_device)

        try:
            super_device = metadata.block_devices[0]
            metadata_region = LP_PARTITION_RESERVED_BYTES + (LP_METADATA_GEOMETRY_SIZE +
                                                             metadata.geometry.metadata_max_size *
                                                             metadata.geometry.metadata_slot_count) * 2
            if metadata_region > super_device.first_logical_sector * LP_SECTOR_SIZE:
                raise LpUnpackError(
                    'Logical partition metadata overlaps with logical partition contents.')
        except IndexError:
            raise LpUnpackError('Metadata does not specify a super device.')

        return metadata

    def lpdump(self):
        self.in_file_fd.seek(0)
        metadata = self.ReadMetadata()

        if self.dump == 1:
            dashed = '------------------------'

            target_types = ['linear', 'zero']
            target_sources = [i.partition_name for i in metadata.block_devices]
            partition_attributes = ['none', 'readonly']
            header_flags = ['none', 'virtual_ab_device']

            print('Metadata version: {}'.format(
                metadata.header.full_version))
            print('Metadata slot count: {}'.format(
                metadata.geometry.metadata_slot_count))
            print('Metadata size: {} bytes'.format(
                metadata.header.tables_size + metadata.header.header_size))
            print('Metadata max size: {} bytes'.format(
                metadata.geometry.metadata_max_size))
            print('Header Flags: {}'.format(
                header_flags[metadata.header.flags.flags_index]))

            print('\n'.join([dashed, 'Partition table:', dashed]))

            sp_layout = []
            for i in metadata.partitions:
                extents = ''
                if i.num_extents:
                    extents = metadata.extents[i.first_extent_index]

                    sp_layout.append(' '.join([target_sources[extents.target_source]+':', str(extents.target_data), '..', str(
                        extents.target_data + extents.num_sectors), i.name, '('+str(extents.num_sectors)+' sectors)']))

                    extents = '\n    '+' '.join(['0 ..', str(extents.num_sectors), target_types[extents.target_type],
                                                target_sources[extents.target_source], str(extents.target_data)])

                print(('  Name: {}\n  Group: {}\n  Attributes: {}\n  Extents: {}\n'+dashed).format(i.name,
                      metadata.groups[i.group_index].name, partition_attributes[i.attributes], extents or ''))

            print('\n'.join(['Super partition layout:', dashed]))
            print('\n'.join(sp_layout))

            print('\n'.join([dashed, 'Block device table:', dashed]))
            print('\n'.join(['  Partition name: {}\n  First sector: {}\n  Size: {} bytes\n  Flags: {}'.format(i.partition_name, i.first_logical_sector, i.size, i.flags or 'none')
                  for i in metadata.block_devices]))

            print('\n'.join([dashed, 'Group Table:', dashed]))
            print('\n'.join([('  Name: {}\n  Maximum size: {} bytes\n  Flags: {}\n'+dashed).format(
                i.name, i.maximum_size, i.flags or 'none') for i in metadata.groups]))

            return

        return metadata
