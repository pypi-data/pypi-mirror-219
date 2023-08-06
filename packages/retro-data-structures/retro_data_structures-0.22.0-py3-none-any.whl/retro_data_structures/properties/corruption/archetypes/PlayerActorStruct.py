# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class PlayerActorStruct(BaseProperty):
    suit_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    suit_skin_rules: AssetId = dataclasses.field(metadata={'asset_types': ['CSKR']}, default=default_asset_id)
    gun_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    fade_in_time: float = dataclasses.field(default=1.0)
    fade_out_time: float = dataclasses.field(default=1.0)

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'\xf7\xff\xbd\x07')  # 0xf7ffbd07
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.suit_model))

        data.write(b'\x0bak\xaa')  # 0xb616baa
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.suit_skin_rules))

        data.write(b'P4\x08R')  # 0x50340852
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.gun_model))

        data.write(b'\x90\xaa4\x1f')  # 0x90aa341f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_in_time))

        data.write(b'|&\x9e\xbc')  # 0x7c269ebc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_out_time))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            suit_model=data['suit_model'],
            suit_skin_rules=data['suit_skin_rules'],
            gun_model=data['gun_model'],
            fade_in_time=data['fade_in_time'],
            fade_out_time=data['fade_out_time'],
        )

    def to_json(self) -> dict:
        return {
            'suit_model': self.suit_model,
            'suit_skin_rules': self.suit_skin_rules,
            'gun_model': self.gun_model,
            'fade_in_time': self.fade_in_time,
            'fade_out_time': self.fade_out_time,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xf7ffbd07, 0xb616baa, 0x50340852, 0x90aa341f, 0x7c269ebc)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[PlayerActorStruct]:
    if property_count != 5:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHQLHQLHQLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(62))
    if (dec[0], dec[3], dec[6], dec[9], dec[12]) != _FAST_IDS:
        data.seek(before)
        return None

    return PlayerActorStruct(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
    )


def _decode_suit_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_suit_skin_rules(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_gun_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf7ffbd07: ('suit_model', _decode_suit_model),
    0xb616baa: ('suit_skin_rules', _decode_suit_skin_rules),
    0x50340852: ('gun_model', _decode_gun_model),
    0x90aa341f: ('fade_in_time', _decode_fade_in_time),
    0x7c269ebc: ('fade_out_time', _decode_fade_out_time),
}
