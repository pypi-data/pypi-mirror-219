# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class TDamageInfo(BaseProperty):
    weapon_type: int = dataclasses.field(default=0)
    damage_amount: float = dataclasses.field(default=10.0)
    radius_damage_amount: float = dataclasses.field(default=5.0)
    damage_radius: float = dataclasses.field(default=1.0)
    knock_back_power: float = dataclasses.field(default=1.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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

        data.write(b'MWy\x10')  # 0x4d577910
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.weapon_type))

        data.write(b'\xf3\xec\x87H')  # 0xf3ec8748
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damage_amount))

        data.write(b'7\xb6\xdf=')  # 0x37b6df3d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.radius_damage_amount))

        data.write(b'\x0fY\x879')  # 0xf598739
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damage_radius))

        data.write(b'V\xf9\x8cI')  # 0x56f98c49
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.knock_back_power))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            weapon_type=data['weapon_type'],
            damage_amount=data['damage_amount'],
            radius_damage_amount=data['radius_damage_amount'],
            damage_radius=data['damage_radius'],
            knock_back_power=data['knock_back_power'],
        )

    def to_json(self) -> dict:
        return {
            'weapon_type': self.weapon_type,
            'damage_amount': self.damage_amount,
            'radius_damage_amount': self.radius_damage_amount,
            'damage_radius': self.damage_radius,
            'knock_back_power': self.knock_back_power,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0x4d577910, 0xf3ec8748, 0x37b6df3d, 0xf598739, 0x56f98c49)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[TDamageInfo]:
    if property_count != 5:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(50))
    if (dec[0], dec[3], dec[6], dec[9], dec[12]) != _FAST_IDS:
        data.seek(before)
        return None

    return TDamageInfo(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
    )


def _decode_weapon_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_damage_amount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_radius_damage_amount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_knock_back_power(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4d577910: ('weapon_type', _decode_weapon_type),
    0xf3ec8748: ('damage_amount', _decode_damage_amount),
    0x37b6df3d: ('radius_damage_amount', _decode_radius_damage_amount),
    0xf598739: ('damage_radius', _decode_damage_radius),
    0x56f98c49: ('knock_back_power', _decode_knock_back_power),
}
