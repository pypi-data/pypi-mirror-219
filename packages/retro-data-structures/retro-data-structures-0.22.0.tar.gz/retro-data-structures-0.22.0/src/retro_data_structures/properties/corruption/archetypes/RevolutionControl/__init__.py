# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.ControlCommands import ControlCommands
from retro_data_structures.properties.corruption.archetypes.RevolutionControl.UnknownStruct1 import UnknownStruct1
from retro_data_structures.properties.corruption.archetypes.RevolutionPhysicalControl import RevolutionPhysicalControl


@dataclasses.dataclass()
class RevolutionControl(BaseProperty):
    command_enum: ControlCommands = dataclasses.field(default_factory=ControlCommands)
    revolution_control_type: enums.RevolutionControlType = dataclasses.field(default=enums.RevolutionControlType.Unknown2)
    physical_control: RevolutionPhysicalControl = dataclasses.field(default_factory=RevolutionPhysicalControl)
    unknown_0x6e14bc06: enums.PhysicalControlBoolean = dataclasses.field(default=enums.PhysicalControlBoolean.Unknown1)
    unknown_0xf0bf68a4: RevolutionPhysicalControl = dataclasses.field(default_factory=RevolutionPhysicalControl)
    revolution_virtual_control: enums.RevolutionVirtualControl = dataclasses.field(default=enums.RevolutionVirtualControl.Unknown1)
    unknown_0xebaabf01: enums.PhysicalControlBoolean = dataclasses.field(default=enums.PhysicalControlBoolean.Unknown1)
    unknown_0xeda6d736: enums.RevolutionVirtualControl = dataclasses.field(default=enums.RevolutionVirtualControl.Unknown1)
    unknown_0xbf80d594: enums.RevolutionControl_UnknownEnum1 = dataclasses.field(default=enums.RevolutionControl_UnknownEnum1.Unknown1)
    unknown_0x91b8c18a: UnknownStruct1 = dataclasses.field(default_factory=UnknownStruct1)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        present_fields = default_override or {}
        for _ in range(property_count):
            property_id, property_size = struct.unpack(">LH", data.read(6))
            start = data.tell()
            try:
                property_name, decoder = _property_decoder[property_id]
                present_fields[property_name] = decoder(data, property_size)
            except KeyError:
                raise RuntimeError(f"Unknown property: 0x{property_id:08x}")
            assert data.tell() - start == property_size

        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        num_properties_offset = data.tell()
        data.write(b'\x00\x03')  # 3 properties
        num_properties_written = 3

        data.write(b'\xb0\xd1}M')  # 0xb0d17d4d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.command_enum.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x81\xcc=>')  # 0x81cc3d3e
        data.write(b'\x00\x04')  # size
        self.revolution_control_type.to_stream(data)

        data.write(b'\xe6F\xd3\xb7')  # 0xe646d3b7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.physical_control.to_stream(data, default_override={'physical_control': enums.PhysicalControl.Unknown3})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        if self.unknown_0x6e14bc06 != default_override.get('unknown_0x6e14bc06', enums.PhysicalControlBoolean.Unknown1):
            num_properties_written += 1
            data.write(b'n\x14\xbc\x06')  # 0x6e14bc06
            data.write(b'\x00\x04')  # size
            self.unknown_0x6e14bc06.to_stream(data)

        if self.unknown_0xf0bf68a4 != default_override.get('unknown_0xf0bf68a4', RevolutionPhysicalControl()):
            num_properties_written += 1
            data.write(b'\xf0\xbfh\xa4')  # 0xf0bf68a4
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.unknown_0xf0bf68a4.to_stream(data, default_override={'physical_control': enums.PhysicalControl.Unknown3})
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        if self.revolution_virtual_control != default_override.get('revolution_virtual_control', enums.RevolutionVirtualControl.Unknown1):
            num_properties_written += 1
            data.write(b'\xfe\x81\x9d\xdb')  # 0xfe819ddb
            data.write(b'\x00\x04')  # size
            self.revolution_virtual_control.to_stream(data)

        if self.unknown_0xebaabf01 != default_override.get('unknown_0xebaabf01', enums.PhysicalControlBoolean.Unknown1):
            num_properties_written += 1
            data.write(b'\xeb\xaa\xbf\x01')  # 0xebaabf01
            data.write(b'\x00\x04')  # size
            self.unknown_0xebaabf01.to_stream(data)

        if self.unknown_0xeda6d736 != default_override.get('unknown_0xeda6d736', enums.RevolutionVirtualControl.Unknown1):
            num_properties_written += 1
            data.write(b'\xed\xa6\xd76')  # 0xeda6d736
            data.write(b'\x00\x04')  # size
            self.unknown_0xeda6d736.to_stream(data)

        if self.unknown_0xbf80d594 != default_override.get('unknown_0xbf80d594', enums.RevolutionControl_UnknownEnum1.Unknown1):
            num_properties_written += 1
            data.write(b'\xbf\x80\xd5\x94')  # 0xbf80d594
            data.write(b'\x00\x04')  # size
            self.unknown_0xbf80d594.to_stream(data)

        if self.unknown_0x91b8c18a != default_override.get('unknown_0x91b8c18a', UnknownStruct1()):
            num_properties_written += 1
            data.write(b'\x91\xb8\xc1\x8a')  # 0x91b8c18a
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.unknown_0x91b8c18a.to_stream(data)
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        if num_properties_written != 3:
            struct_end_offset = data.tell()
            data.seek(num_properties_offset)
            data.write(struct.pack(">H", num_properties_written))
            data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            command_enum=ControlCommands.from_json(data['command_enum']),
            revolution_control_type=enums.RevolutionControlType.from_json(data['revolution_control_type']),
            physical_control=RevolutionPhysicalControl.from_json(data['physical_control']),
            unknown_0x6e14bc06=enums.PhysicalControlBoolean.from_json(data['unknown_0x6e14bc06']),
            unknown_0xf0bf68a4=RevolutionPhysicalControl.from_json(data['unknown_0xf0bf68a4']),
            revolution_virtual_control=enums.RevolutionVirtualControl.from_json(data['revolution_virtual_control']),
            unknown_0xebaabf01=enums.PhysicalControlBoolean.from_json(data['unknown_0xebaabf01']),
            unknown_0xeda6d736=enums.RevolutionVirtualControl.from_json(data['unknown_0xeda6d736']),
            unknown_0xbf80d594=enums.RevolutionControl_UnknownEnum1.from_json(data['unknown_0xbf80d594']),
            unknown_0x91b8c18a=UnknownStruct1.from_json(data['unknown_0x91b8c18a']),
        )

    def to_json(self) -> dict:
        return {
            'command_enum': self.command_enum.to_json(),
            'revolution_control_type': self.revolution_control_type.to_json(),
            'physical_control': self.physical_control.to_json(),
            'unknown_0x6e14bc06': self.unknown_0x6e14bc06.to_json(),
            'unknown_0xf0bf68a4': self.unknown_0xf0bf68a4.to_json(),
            'revolution_virtual_control': self.revolution_virtual_control.to_json(),
            'unknown_0xebaabf01': self.unknown_0xebaabf01.to_json(),
            'unknown_0xeda6d736': self.unknown_0xeda6d736.to_json(),
            'unknown_0xbf80d594': self.unknown_0xbf80d594.to_json(),
            'unknown_0x91b8c18a': self.unknown_0x91b8c18a.to_json(),
        }


def _decode_command_enum(data: typing.BinaryIO, property_size: int):
    return ControlCommands.from_stream(data, property_size)


def _decode_revolution_control_type(data: typing.BinaryIO, property_size: int):
    return enums.RevolutionControlType.from_stream(data)


def _decode_physical_control(data: typing.BinaryIO, property_size: int):
    return RevolutionPhysicalControl.from_stream(data, property_size, default_override={'physical_control': enums.PhysicalControl.Unknown3})


def _decode_unknown_0x6e14bc06(data: typing.BinaryIO, property_size: int):
    return enums.PhysicalControlBoolean.from_stream(data)


def _decode_unknown_0xf0bf68a4(data: typing.BinaryIO, property_size: int):
    return RevolutionPhysicalControl.from_stream(data, property_size, default_override={'physical_control': enums.PhysicalControl.Unknown3})


def _decode_revolution_virtual_control(data: typing.BinaryIO, property_size: int):
    return enums.RevolutionVirtualControl.from_stream(data)


def _decode_unknown_0xebaabf01(data: typing.BinaryIO, property_size: int):
    return enums.PhysicalControlBoolean.from_stream(data)


def _decode_unknown_0xeda6d736(data: typing.BinaryIO, property_size: int):
    return enums.RevolutionVirtualControl.from_stream(data)


def _decode_unknown_0xbf80d594(data: typing.BinaryIO, property_size: int):
    return enums.RevolutionControl_UnknownEnum1.from_stream(data)


def _decode_unknown_0x91b8c18a(data: typing.BinaryIO, property_size: int):
    return UnknownStruct1.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb0d17d4d: ('command_enum', _decode_command_enum),
    0x81cc3d3e: ('revolution_control_type', _decode_revolution_control_type),
    0xe646d3b7: ('physical_control', _decode_physical_control),
    0x6e14bc06: ('unknown_0x6e14bc06', _decode_unknown_0x6e14bc06),
    0xf0bf68a4: ('unknown_0xf0bf68a4', _decode_unknown_0xf0bf68a4),
    0xfe819ddb: ('revolution_virtual_control', _decode_revolution_virtual_control),
    0xebaabf01: ('unknown_0xebaabf01', _decode_unknown_0xebaabf01),
    0xeda6d736: ('unknown_0xeda6d736', _decode_unknown_0xeda6d736),
    0xbf80d594: ('unknown_0xbf80d594', _decode_unknown_0xbf80d594),
    0x91b8c18a: ('unknown_0x91b8c18a', _decode_unknown_0x91b8c18a),
}
