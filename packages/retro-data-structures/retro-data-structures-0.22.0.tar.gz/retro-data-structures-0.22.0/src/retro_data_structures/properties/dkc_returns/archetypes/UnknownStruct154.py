# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct154(BaseProperty):
    unknown_0xe0c67593: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    cine_lever: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud_0x8eac5ae7: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud_0xf9328817: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud_0x6297c478: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud_0x160f2df7: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    puzzle_1_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    puzzle_2_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    puzzle_3_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    puzzle_4_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    puzzle_5_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    puzzle_6_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    puzzle_7_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    puzzle_8_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    puzzle_9_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud_0xecc8c95f: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    beat_up_sound: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0xdbafba23: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\x12')  # 18 properties

        data.write(b'\xe0\xc6u\x93')  # 0xe0c67593
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xe0c67593))

        data.write(b'\xd9\xbe\xd8\xd3')  # 0xd9bed8d3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cine_lever))

        data.write(b'\x8e\xacZ\xe7')  # 0x8eac5ae7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x8eac5ae7))

        data.write(b'\xf92\x88\x17')  # 0xf9328817
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0xf9328817))

        data.write(b'b\x97\xc4x')  # 0x6297c478
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x6297c478))

        data.write(b'\x16\x0f-\xf7')  # 0x160f2df7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x160f2df7))

        data.write(b'\xd7\xcf\x8b\xf3')  # 0xd7cf8bf3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.puzzle_1_sound))

        data.write(b'\xa0QY\x03')  # 0xa0515903
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.puzzle_2_sound))

        data.write(b';\xf4\x15l')  # 0x3bf4156c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.puzzle_3_sound))

        data.write(b'Ol\xfc\xe3')  # 0x4f6cfce3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.puzzle_4_sound))

        data.write(b'\xd4\xc9\xb0\x8c')  # 0xd4c9b08c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.puzzle_5_sound))

        data.write(b'\xa3Wb|')  # 0xa357627c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.puzzle_6_sound))

        data.write(b'8\xf2.\x13')  # 0x38f22e13
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.puzzle_7_sound))

        data.write(b'Jf\xb1b')  # 0x4a66b162
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.puzzle_8_sound))

        data.write(b'\xd1\xc3\xfd\r')  # 0xd1c3fd0d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.puzzle_9_sound))

        data.write(b'\xec\xc8\xc9_')  # 0xecc8c95f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0xecc8c95f))

        data.write(b'Cn\xa0\x86')  # 0x436ea086
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.beat_up_sound))

        data.write(b'\xdb\xaf\xba#')  # 0xdbafba23
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xdbafba23))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xe0c67593=data['unknown_0xe0c67593'],
            cine_lever=data['cine_lever'],
            caud_0x8eac5ae7=data['caud_0x8eac5ae7'],
            caud_0xf9328817=data['caud_0xf9328817'],
            caud_0x6297c478=data['caud_0x6297c478'],
            caud_0x160f2df7=data['caud_0x160f2df7'],
            puzzle_1_sound=data['puzzle_1_sound'],
            puzzle_2_sound=data['puzzle_2_sound'],
            puzzle_3_sound=data['puzzle_3_sound'],
            puzzle_4_sound=data['puzzle_4_sound'],
            puzzle_5_sound=data['puzzle_5_sound'],
            puzzle_6_sound=data['puzzle_6_sound'],
            puzzle_7_sound=data['puzzle_7_sound'],
            puzzle_8_sound=data['puzzle_8_sound'],
            puzzle_9_sound=data['puzzle_9_sound'],
            caud_0xecc8c95f=data['caud_0xecc8c95f'],
            beat_up_sound=data['beat_up_sound'],
            unknown_0xdbafba23=data['unknown_0xdbafba23'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xe0c67593': self.unknown_0xe0c67593,
            'cine_lever': self.cine_lever,
            'caud_0x8eac5ae7': self.caud_0x8eac5ae7,
            'caud_0xf9328817': self.caud_0xf9328817,
            'caud_0x6297c478': self.caud_0x6297c478,
            'caud_0x160f2df7': self.caud_0x160f2df7,
            'puzzle_1_sound': self.puzzle_1_sound,
            'puzzle_2_sound': self.puzzle_2_sound,
            'puzzle_3_sound': self.puzzle_3_sound,
            'puzzle_4_sound': self.puzzle_4_sound,
            'puzzle_5_sound': self.puzzle_5_sound,
            'puzzle_6_sound': self.puzzle_6_sound,
            'puzzle_7_sound': self.puzzle_7_sound,
            'puzzle_8_sound': self.puzzle_8_sound,
            'puzzle_9_sound': self.puzzle_9_sound,
            'caud_0xecc8c95f': self.caud_0xecc8c95f,
            'beat_up_sound': self.beat_up_sound,
            'unknown_0xdbafba23': self.unknown_0xdbafba23,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xe0c67593, 0xd9bed8d3, 0x8eac5ae7, 0xf9328817, 0x6297c478, 0x160f2df7, 0xd7cf8bf3, 0xa0515903, 0x3bf4156c, 0x4f6cfce3, 0xd4c9b08c, 0xa357627c, 0x38f22e13, 0x4a66b162, 0xd1c3fd0d, 0xecc8c95f, 0x436ea086, 0xdbafba23)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct154]:
    if property_count != 18:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHQLHQLHQLHQLHQLHQLHQLHQLHQLHQLHQLHQLHQLHQLHQLHQLHQLHQ')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(252))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33], dec[36], dec[39], dec[42], dec[45], dec[48], dec[51]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct154(
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
        dec[47],
        dec[50],
        dec[53],
    )


def _decode_unknown_0xe0c67593(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cine_lever(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x8eac5ae7(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0xf9328817(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x6297c478(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x160f2df7(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_puzzle_1_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_puzzle_2_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_puzzle_3_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_puzzle_4_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_puzzle_5_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_puzzle_6_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_puzzle_7_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_puzzle_8_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_puzzle_9_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0xecc8c95f(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_beat_up_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xdbafba23(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe0c67593: ('unknown_0xe0c67593', _decode_unknown_0xe0c67593),
    0xd9bed8d3: ('cine_lever', _decode_cine_lever),
    0x8eac5ae7: ('caud_0x8eac5ae7', _decode_caud_0x8eac5ae7),
    0xf9328817: ('caud_0xf9328817', _decode_caud_0xf9328817),
    0x6297c478: ('caud_0x6297c478', _decode_caud_0x6297c478),
    0x160f2df7: ('caud_0x160f2df7', _decode_caud_0x160f2df7),
    0xd7cf8bf3: ('puzzle_1_sound', _decode_puzzle_1_sound),
    0xa0515903: ('puzzle_2_sound', _decode_puzzle_2_sound),
    0x3bf4156c: ('puzzle_3_sound', _decode_puzzle_3_sound),
    0x4f6cfce3: ('puzzle_4_sound', _decode_puzzle_4_sound),
    0xd4c9b08c: ('puzzle_5_sound', _decode_puzzle_5_sound),
    0xa357627c: ('puzzle_6_sound', _decode_puzzle_6_sound),
    0x38f22e13: ('puzzle_7_sound', _decode_puzzle_7_sound),
    0x4a66b162: ('puzzle_8_sound', _decode_puzzle_8_sound),
    0xd1c3fd0d: ('puzzle_9_sound', _decode_puzzle_9_sound),
    0xecc8c95f: ('caud_0xecc8c95f', _decode_caud_0xecc8c95f),
    0x436ea086: ('beat_up_sound', _decode_beat_up_sound),
    0xdbafba23: ('unknown_0xdbafba23', _decode_unknown_0xdbafba23),
}
