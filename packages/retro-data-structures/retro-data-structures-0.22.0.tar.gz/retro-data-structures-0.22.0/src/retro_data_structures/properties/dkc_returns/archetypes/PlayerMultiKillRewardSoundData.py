# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class PlayerMultiKillRewardSoundData(BaseProperty):
    count1: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    count2: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    count3: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    count4: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    count5: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    count6: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    count7: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    count8: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'\x97\xe7\xd7b')  # 0x97e7d762
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.count1))

        data.write(b'\x11s\xa5\xcc')  # 0x1173a5cc
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.count2))

        data.write(b'\xda/vi')  # 0xda2f7669
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.count3))

        data.write(b'\xc7*F\xd1')  # 0xc72a46d1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.count4))

        data.write(b'\x0cv\x95t')  # 0xc769574
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.count5))

        data.write(b'\x8a\xe2\xe7\xda')  # 0x8ae2e7da
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.count6))

        data.write(b'A\xbe4\x7f')  # 0x41be347f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.count7))

        data.write(b'\xb0\xe8\x86\xaa')  # 0xb0e886aa
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.count8))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            count1=data['count1'],
            count2=data['count2'],
            count3=data['count3'],
            count4=data['count4'],
            count5=data['count5'],
            count6=data['count6'],
            count7=data['count7'],
            count8=data['count8'],
        )

    def to_json(self) -> dict:
        return {
            'count1': self.count1,
            'count2': self.count2,
            'count3': self.count3,
            'count4': self.count4,
            'count5': self.count5,
            'count6': self.count6,
            'count7': self.count7,
            'count8': self.count8,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x97e7d762, 0x1173a5cc, 0xda2f7669, 0xc72a46d1, 0xc769574, 0x8ae2e7da, 0x41be347f, 0xb0e886aa)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[PlayerMultiKillRewardSoundData]:
    if property_count != 8:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHQLHQLHQLHQLHQLHQLHQLHQ')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(112))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21]) != _FAST_IDS:
        data.seek(before)
        return None

    return PlayerMultiKillRewardSoundData(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
    )


def _decode_count1(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_count2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_count3(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_count4(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_count5(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_count6(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_count7(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_count8(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x97e7d762: ('count1', _decode_count1),
    0x1173a5cc: ('count2', _decode_count2),
    0xda2f7669: ('count3', _decode_count3),
    0xc72a46d1: ('count4', _decode_count4),
    0xc769574: ('count5', _decode_count5),
    0x8ae2e7da: ('count6', _decode_count6),
    0x41be347f: ('count7', _decode_count7),
    0xb0e886aa: ('count8', _decode_count8),
}
