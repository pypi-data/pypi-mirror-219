# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.corruption as enums


@dataclasses.dataclass()
class DamageInfo(BaseProperty):
    di_weapon_type: enums.DI_WeaponType = dataclasses.field(default=enums.DI_WeaponType.AI)
    di_damage: float = dataclasses.field(default=0.0)
    di_radius: float = dataclasses.field(default=0.0)
    di_knock_back_power: float = dataclasses.field(default=0.0)
    unknown: int = dataclasses.field(default=0)
    adjust_for_difficulty: bool = dataclasses.field(default=True)

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'D^\x00\xc8')  # 0x445e00c8
        data.write(b'\x00\x04')  # size
        self.di_weapon_type.to_stream(data)

        data.write(b'\xf2\xd0&\x13')  # 0xf2d02613
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.di_damage))

        data.write(b'\xee\x1b\xe9\x14')  # 0xee1be914
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.di_radius))

        data.write(b'U_\xf8\n')  # 0x555ff80a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.di_knock_back_power))

        data.write(b'z?\xe0\r')  # 0x7a3fe00d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown))

        data.write(b'\xef\xe9\xe4e')  # 0xefe9e465
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.adjust_for_difficulty))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            di_weapon_type=enums.DI_WeaponType.from_json(data['di_weapon_type']),
            di_damage=data['di_damage'],
            di_radius=data['di_radius'],
            di_knock_back_power=data['di_knock_back_power'],
            unknown=data['unknown'],
            adjust_for_difficulty=data['adjust_for_difficulty'],
        )

    def to_json(self) -> dict:
        return {
            'di_weapon_type': self.di_weapon_type.to_json(),
            'di_damage': self.di_damage,
            'di_radius': self.di_radius,
            'di_knock_back_power': self.di_knock_back_power,
            'unknown': self.unknown,
            'adjust_for_difficulty': self.adjust_for_difficulty,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x445e00c8, 0xf2d02613, 0xee1be914, 0x555ff80a, 0x7a3fe00d, 0xefe9e465)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[DamageInfo]:
    if property_count != 6:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHLLHfLHfLHfLHlLH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(57))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15]) != _FAST_IDS:
        data.seek(before)
        return None

    return DamageInfo(
        enums.DI_WeaponType(dec[2]),
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
    )


def _decode_di_weapon_type(data: typing.BinaryIO, property_size: int):
    return enums.DI_WeaponType.from_stream(data)


def _decode_di_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_di_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_di_knock_back_power(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_adjust_for_difficulty(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x445e00c8: ('di_weapon_type', _decode_di_weapon_type),
    0xf2d02613: ('di_damage', _decode_di_damage),
    0xee1be914: ('di_radius', _decode_di_radius),
    0x555ff80a: ('di_knock_back_power', _decode_di_knock_back_power),
    0x7a3fe00d: ('unknown', _decode_unknown),
    0xefe9e465: ('adjust_for_difficulty', _decode_adjust_for_difficulty),
}
