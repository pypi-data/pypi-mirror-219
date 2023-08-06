# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums


@dataclasses.dataclass()
class DamageInfo(BaseProperty):
    di_damage_type: enums.DI_DamageType = dataclasses.field(default=enums.DI_DamageType.Unknown1)
    di_damage: float = dataclasses.field(default=0.0)
    di_radius: float = dataclasses.field(default=0.0)
    di_knock_back_speed: float = dataclasses.field(default=4.0)
    di_hurl_height: float = dataclasses.field(default=6.0)
    di_hurl_distance: float = dataclasses.field(default=12.0)
    di_effect_intensity: int = dataclasses.field(default=0)
    di_default_contact_rule: enums.DI_DefaultContactRule = dataclasses.field(default=enums.DI_DefaultContactRule.Unknown2)

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

        data.write(b'e\xc4\xfbJ')  # 0x65c4fb4a
        data.write(b'\x00\x04')  # size
        self.di_damage_type.to_stream(data)

        data.write(b'\xf2\xd0&\x13')  # 0xf2d02613
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.di_damage))

        data.write(b'\xee\x1b\xe9\x14')  # 0xee1be914
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.di_radius))

        data.write(b'&\x00\x19y')  # 0x26001979
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.di_knock_back_speed))

        data.write(b'\x99\n\x16)')  # 0x990a1629
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.di_hurl_height))

        data.write(b'_\x8a\x1dG')  # 0x5f8a1d47
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.di_hurl_distance))

        data.write(b'\x13\x1dp\x1b')  # 0x131d701b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.di_effect_intensity))

        data.write(b'\x82f\xb5)')  # 0x8266b529
        data.write(b'\x00\x04')  # size
        self.di_default_contact_rule.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            di_damage_type=enums.DI_DamageType.from_json(data['di_damage_type']),
            di_damage=data['di_damage'],
            di_radius=data['di_radius'],
            di_knock_back_speed=data['di_knock_back_speed'],
            di_hurl_height=data['di_hurl_height'],
            di_hurl_distance=data['di_hurl_distance'],
            di_effect_intensity=data['di_effect_intensity'],
            di_default_contact_rule=enums.DI_DefaultContactRule.from_json(data['di_default_contact_rule']),
        )

    def to_json(self) -> dict:
        return {
            'di_damage_type': self.di_damage_type.to_json(),
            'di_damage': self.di_damage,
            'di_radius': self.di_radius,
            'di_knock_back_speed': self.di_knock_back_speed,
            'di_hurl_height': self.di_hurl_height,
            'di_hurl_distance': self.di_hurl_distance,
            'di_effect_intensity': self.di_effect_intensity,
            'di_default_contact_rule': self.di_default_contact_rule.to_json(),
        }


_FAST_FORMAT = None
_FAST_IDS = (0x65c4fb4a, 0xf2d02613, 0xee1be914, 0x26001979, 0x990a1629, 0x5f8a1d47, 0x131d701b, 0x8266b529)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[DamageInfo]:
    if property_count != 8:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHLLHfLHfLHfLHfLHfLHlLHL')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(80))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21]) != _FAST_IDS:
        data.seek(before)
        return None

    return DamageInfo(
        enums.DI_DamageType(dec[2]),
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        enums.DI_DefaultContactRule(dec[23]),
    )


def _decode_di_damage_type(data: typing.BinaryIO, property_size: int):
    return enums.DI_DamageType.from_stream(data)


def _decode_di_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_di_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_di_knock_back_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_di_hurl_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_di_hurl_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_di_effect_intensity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_di_default_contact_rule(data: typing.BinaryIO, property_size: int):
    return enums.DI_DefaultContactRule.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x65c4fb4a: ('di_damage_type', _decode_di_damage_type),
    0xf2d02613: ('di_damage', _decode_di_damage),
    0xee1be914: ('di_radius', _decode_di_radius),
    0x26001979: ('di_knock_back_speed', _decode_di_knock_back_speed),
    0x990a1629: ('di_hurl_height', _decode_di_hurl_height),
    0x5f8a1d47: ('di_hurl_distance', _decode_di_hurl_distance),
    0x131d701b: ('di_effect_intensity', _decode_di_effect_intensity),
    0x8266b529: ('di_default_contact_rule', _decode_di_default_contact_rule),
}
