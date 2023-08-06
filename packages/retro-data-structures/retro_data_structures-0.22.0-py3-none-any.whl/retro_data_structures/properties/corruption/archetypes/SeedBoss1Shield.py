# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class SeedBoss1Shield(BaseProperty):
    cmdl_0xdce1a940: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0xf4c318b3: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0xb3673269: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0xb9196d9e: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    important_moment: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0x4d7984e6: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0x8fbe621d: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0x11ea2651: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0x564e0c8b: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0x807edcc5: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0x708b0155: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0xe46803dc: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0x6a975cff: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0x97e2b6c7: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0x1176c469: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

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
        data.write(b'\x00\x0f')  # 15 properties

        data.write(b'\xdc\xe1\xa9@')  # 0xdce1a940
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0xdce1a940))

        data.write(b'\xf4\xc3\x18\xb3')  # 0xf4c318b3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0xf4c318b3))

        data.write(b'\xb3g2i')  # 0xb3673269
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0xb3673269))

        data.write(b'\xb9\x19m\x9e')  # 0xb9196d9e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0xb9196d9e))

        data.write(b'\x8c\x0b\xee\x98')  # 0x8c0bee98
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.important_moment))

        data.write(b'My\x84\xe6')  # 0x4d7984e6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0x4d7984e6))

        data.write(b'\x8f\xbeb\x1d')  # 0x8fbe621d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0x8fbe621d))

        data.write(b'\x11\xea&Q')  # 0x11ea2651
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0x11ea2651))

        data.write(b'VN\x0c\x8b')  # 0x564e0c8b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0x564e0c8b))

        data.write(b'\x80~\xdc\xc5')  # 0x807edcc5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0x807edcc5))

        data.write(b'p\x8b\x01U')  # 0x708b0155
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0x708b0155))

        data.write(b'\xe4h\x03\xdc')  # 0xe46803dc
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0xe46803dc))

        data.write(b'j\x97\\\xff')  # 0x6a975cff
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0x6a975cff))

        data.write(b'\x97\xe2\xb6\xc7')  # 0x97e2b6c7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0x97e2b6c7))

        data.write(b'\x11v\xc4i')  # 0x1176c469
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0x1176c469))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            cmdl_0xdce1a940=data['cmdl_0xdce1a940'],
            cmdl_0xf4c318b3=data['cmdl_0xf4c318b3'],
            cmdl_0xb3673269=data['cmdl_0xb3673269'],
            cmdl_0xb9196d9e=data['cmdl_0xb9196d9e'],
            important_moment=data['important_moment'],
            cmdl_0x4d7984e6=data['cmdl_0x4d7984e6'],
            cmdl_0x8fbe621d=data['cmdl_0x8fbe621d'],
            cmdl_0x11ea2651=data['cmdl_0x11ea2651'],
            cmdl_0x564e0c8b=data['cmdl_0x564e0c8b'],
            cmdl_0x807edcc5=data['cmdl_0x807edcc5'],
            cmdl_0x708b0155=data['cmdl_0x708b0155'],
            cmdl_0xe46803dc=data['cmdl_0xe46803dc'],
            cmdl_0x6a975cff=data['cmdl_0x6a975cff'],
            cmdl_0x97e2b6c7=data['cmdl_0x97e2b6c7'],
            cmdl_0x1176c469=data['cmdl_0x1176c469'],
        )

    def to_json(self) -> dict:
        return {
            'cmdl_0xdce1a940': self.cmdl_0xdce1a940,
            'cmdl_0xf4c318b3': self.cmdl_0xf4c318b3,
            'cmdl_0xb3673269': self.cmdl_0xb3673269,
            'cmdl_0xb9196d9e': self.cmdl_0xb9196d9e,
            'important_moment': self.important_moment,
            'cmdl_0x4d7984e6': self.cmdl_0x4d7984e6,
            'cmdl_0x8fbe621d': self.cmdl_0x8fbe621d,
            'cmdl_0x11ea2651': self.cmdl_0x11ea2651,
            'cmdl_0x564e0c8b': self.cmdl_0x564e0c8b,
            'cmdl_0x807edcc5': self.cmdl_0x807edcc5,
            'cmdl_0x708b0155': self.cmdl_0x708b0155,
            'cmdl_0xe46803dc': self.cmdl_0xe46803dc,
            'cmdl_0x6a975cff': self.cmdl_0x6a975cff,
            'cmdl_0x97e2b6c7': self.cmdl_0x97e2b6c7,
            'cmdl_0x1176c469': self.cmdl_0x1176c469,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xdce1a940, 0xf4c318b3, 0xb3673269, 0xb9196d9e, 0x8c0bee98, 0x4d7984e6, 0x8fbe621d, 0x11ea2651, 0x564e0c8b, 0x807edcc5, 0x708b0155, 0xe46803dc, 0x6a975cff, 0x97e2b6c7, 0x1176c469)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[SeedBoss1Shield]:
    if property_count != 15:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHQLHQLHQLHQLHQLHQLHQLHQLHQLHQLHQLHQLHQLHQLHQ')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(210))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33], dec[36], dec[39], dec[42]) != _FAST_IDS:
        data.seek(before)
        return None

    return SeedBoss1Shield(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
        dec[26],
        dec[29],
        dec[32],
        dec[35],
        dec[38],
        dec[41],
        dec[44],
    )


def _decode_cmdl_0xdce1a940(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0xf4c318b3(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0xb3673269(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0xb9196d9e(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_important_moment(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0x4d7984e6(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0x8fbe621d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0x11ea2651(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0x564e0c8b(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0x807edcc5(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0x708b0155(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0xe46803dc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0x6a975cff(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0x97e2b6c7(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0x1176c469(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xdce1a940: ('cmdl_0xdce1a940', _decode_cmdl_0xdce1a940),
    0xf4c318b3: ('cmdl_0xf4c318b3', _decode_cmdl_0xf4c318b3),
    0xb3673269: ('cmdl_0xb3673269', _decode_cmdl_0xb3673269),
    0xb9196d9e: ('cmdl_0xb9196d9e', _decode_cmdl_0xb9196d9e),
    0x8c0bee98: ('important_moment', _decode_important_moment),
    0x4d7984e6: ('cmdl_0x4d7984e6', _decode_cmdl_0x4d7984e6),
    0x8fbe621d: ('cmdl_0x8fbe621d', _decode_cmdl_0x8fbe621d),
    0x11ea2651: ('cmdl_0x11ea2651', _decode_cmdl_0x11ea2651),
    0x564e0c8b: ('cmdl_0x564e0c8b', _decode_cmdl_0x564e0c8b),
    0x807edcc5: ('cmdl_0x807edcc5', _decode_cmdl_0x807edcc5),
    0x708b0155: ('cmdl_0x708b0155', _decode_cmdl_0x708b0155),
    0xe46803dc: ('cmdl_0xe46803dc', _decode_cmdl_0xe46803dc),
    0x6a975cff: ('cmdl_0x6a975cff', _decode_cmdl_0x6a975cff),
    0x97e2b6c7: ('cmdl_0x97e2b6c7', _decode_cmdl_0x97e2b6c7),
    0x1176c469: ('cmdl_0x1176c469', _decode_cmdl_0x1176c469),
}
