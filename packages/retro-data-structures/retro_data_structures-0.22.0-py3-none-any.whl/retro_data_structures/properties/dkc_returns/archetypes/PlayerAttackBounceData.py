# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class PlayerAttackBounceData(BaseProperty):
    minimum_attack_bounce_height: float = dataclasses.field(default=3.25)
    maximum_attack_bounce_height: float = dataclasses.field(default=5.25)
    low_shielded_attack_bounce_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    high_shielded_attack_bounce_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    low_damage_attack_bounce_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    high_damage_attack_bounce_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    controller_attack_bounce_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'0\xf6\xa3k')  # 0x30f6a36b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_attack_bounce_height))

        data.write(b'\x80\xc9\xb9W')  # 0x80c9b957
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_attack_bounce_height))

        data.write(b']\x84\x9e\xf9')  # 0x5d849ef9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.low_shielded_attack_bounce_sound))

        data.write(b'\xd8\x0f\x96\xc2')  # 0xd80f96c2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.high_shielded_attack_bounce_sound))

        data.write(b'\x95@\x82F')  # 0x95408246
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.low_damage_attack_bounce_sound))

        data.write(b'\xa3\xc2\xfcD')  # 0xa3c2fc44
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.high_damage_attack_bounce_sound))

        data.write(b'\xb9\xa2\xaf}')  # 0xb9a2af7d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.controller_attack_bounce_sound))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            minimum_attack_bounce_height=data['minimum_attack_bounce_height'],
            maximum_attack_bounce_height=data['maximum_attack_bounce_height'],
            low_shielded_attack_bounce_sound=data['low_shielded_attack_bounce_sound'],
            high_shielded_attack_bounce_sound=data['high_shielded_attack_bounce_sound'],
            low_damage_attack_bounce_sound=data['low_damage_attack_bounce_sound'],
            high_damage_attack_bounce_sound=data['high_damage_attack_bounce_sound'],
            controller_attack_bounce_sound=data['controller_attack_bounce_sound'],
        )

    def to_json(self) -> dict:
        return {
            'minimum_attack_bounce_height': self.minimum_attack_bounce_height,
            'maximum_attack_bounce_height': self.maximum_attack_bounce_height,
            'low_shielded_attack_bounce_sound': self.low_shielded_attack_bounce_sound,
            'high_shielded_attack_bounce_sound': self.high_shielded_attack_bounce_sound,
            'low_damage_attack_bounce_sound': self.low_damage_attack_bounce_sound,
            'high_damage_attack_bounce_sound': self.high_damage_attack_bounce_sound,
            'controller_attack_bounce_sound': self.controller_attack_bounce_sound,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x30f6a36b, 0x80c9b957, 0x5d849ef9, 0xd80f96c2, 0x95408246, 0xa3c2fc44, 0xb9a2af7d)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[PlayerAttackBounceData]:
    if property_count != 7:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHQLHQLHQLHQLHQ')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(90))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18]) != _FAST_IDS:
        data.seek(before)
        return None

    return PlayerAttackBounceData(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
    )


def _decode_minimum_attack_bounce_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_attack_bounce_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_low_shielded_attack_bounce_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_high_shielded_attack_bounce_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_low_damage_attack_bounce_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_high_damage_attack_bounce_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_controller_attack_bounce_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x30f6a36b: ('minimum_attack_bounce_height', _decode_minimum_attack_bounce_height),
    0x80c9b957: ('maximum_attack_bounce_height', _decode_maximum_attack_bounce_height),
    0x5d849ef9: ('low_shielded_attack_bounce_sound', _decode_low_shielded_attack_bounce_sound),
    0xd80f96c2: ('high_shielded_attack_bounce_sound', _decode_high_shielded_attack_bounce_sound),
    0x95408246: ('low_damage_attack_bounce_sound', _decode_low_damage_attack_bounce_sound),
    0xa3c2fc44: ('high_damage_attack_bounce_sound', _decode_high_damage_attack_bounce_sound),
    0xb9a2af7d: ('controller_attack_bounce_sound', _decode_controller_attack_bounce_sound),
}
