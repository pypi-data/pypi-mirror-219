# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.SuspensionBridgeStruct import SuspensionBridgeStruct
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct269 import UnknownStruct269


@dataclasses.dataclass()
class SuspensionBridgeData(BaseProperty):
    unknown_0x0e4c8a24: bool = dataclasses.field(default=False)
    unknown_0x7b5d0e29: float = dataclasses.field(default=5.0)
    unknown_0x06df8bd9: float = dataclasses.field(default=12.0)
    unknown_0xda13807d: float = dataclasses.field(default=20.0)
    unknown_struct269: UnknownStruct269 = dataclasses.field(default_factory=UnknownStruct269)
    suspension_bridge_struct_0xf6555670: SuspensionBridgeStruct = dataclasses.field(default_factory=SuspensionBridgeStruct)
    suspension_bridge_struct_0x7cb2693b: SuspensionBridgeStruct = dataclasses.field(default_factory=SuspensionBridgeStruct)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\x0eL\x8a$')  # 0xe4c8a24
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x0e4c8a24))

        data.write(b'{]\x0e)')  # 0x7b5d0e29
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7b5d0e29))

        data.write(b'\x06\xdf\x8b\xd9')  # 0x6df8bd9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x06df8bd9))

        data.write(b'\xda\x13\x80}')  # 0xda13807d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xda13807d))

        data.write(b'h\x1fLv')  # 0x681f4c76
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct269.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf6UVp')  # 0xf6555670
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.suspension_bridge_struct_0xf6555670.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'|\xb2i;')  # 0x7cb2693b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.suspension_bridge_struct_0x7cb2693b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x0e4c8a24=data['unknown_0x0e4c8a24'],
            unknown_0x7b5d0e29=data['unknown_0x7b5d0e29'],
            unknown_0x06df8bd9=data['unknown_0x06df8bd9'],
            unknown_0xda13807d=data['unknown_0xda13807d'],
            unknown_struct269=UnknownStruct269.from_json(data['unknown_struct269']),
            suspension_bridge_struct_0xf6555670=SuspensionBridgeStruct.from_json(data['suspension_bridge_struct_0xf6555670']),
            suspension_bridge_struct_0x7cb2693b=SuspensionBridgeStruct.from_json(data['suspension_bridge_struct_0x7cb2693b']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x0e4c8a24': self.unknown_0x0e4c8a24,
            'unknown_0x7b5d0e29': self.unknown_0x7b5d0e29,
            'unknown_0x06df8bd9': self.unknown_0x06df8bd9,
            'unknown_0xda13807d': self.unknown_0xda13807d,
            'unknown_struct269': self.unknown_struct269.to_json(),
            'suspension_bridge_struct_0xf6555670': self.suspension_bridge_struct_0xf6555670.to_json(),
            'suspension_bridge_struct_0x7cb2693b': self.suspension_bridge_struct_0x7cb2693b.to_json(),
        }


def _decode_unknown_0x0e4c8a24(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x7b5d0e29(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x06df8bd9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xda13807d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct269(data: typing.BinaryIO, property_size: int):
    return UnknownStruct269.from_stream(data, property_size)


def _decode_suspension_bridge_struct_0xf6555670(data: typing.BinaryIO, property_size: int):
    return SuspensionBridgeStruct.from_stream(data, property_size)


def _decode_suspension_bridge_struct_0x7cb2693b(data: typing.BinaryIO, property_size: int):
    return SuspensionBridgeStruct.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe4c8a24: ('unknown_0x0e4c8a24', _decode_unknown_0x0e4c8a24),
    0x7b5d0e29: ('unknown_0x7b5d0e29', _decode_unknown_0x7b5d0e29),
    0x6df8bd9: ('unknown_0x06df8bd9', _decode_unknown_0x06df8bd9),
    0xda13807d: ('unknown_0xda13807d', _decode_unknown_0xda13807d),
    0x681f4c76: ('unknown_struct269', _decode_unknown_struct269),
    0xf6555670: ('suspension_bridge_struct_0xf6555670', _decode_suspension_bridge_struct_0xf6555670),
    0x7cb2693b: ('suspension_bridge_struct_0x7cb2693b', _decode_suspension_bridge_struct_0x7cb2693b),
}
