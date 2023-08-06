# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ShockWaveInfo(BaseProperty):
    shock_wave_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    duration: float = dataclasses.field(default=2.0)
    knockback_decay_rate: float = dataclasses.field(default=0.0)
    unknown_0x60df1486: bool = dataclasses.field(default=True)
    radius: float = dataclasses.field(default=0.0)
    height: float = dataclasses.field(default=1.0)
    unknown_0xcf6c1de9: float = dataclasses.field(default=0.5)
    radial_velocity: float = dataclasses.field(default=1.0)
    radial_velocity_acceleration: float = dataclasses.field(default=0.0)
    visor_electric_effect: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    sound_visor_electric: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    optional_shockwave_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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
        data.write(b'\x00\r')  # 13 properties

        data.write(b'6\x9f}\t')  # 0x369f7d09
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.shock_wave_effect))

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8bQ\xe2?')  # 0x8b51e23f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.duration))

        data.write(b'\x03 \x89[')  # 0x320895b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.knockback_decay_rate))

        data.write(b'`\xdf\x14\x86')  # 0x60df1486
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x60df1486))

        data.write(b'x\xc5\x07\xeb')  # 0x78c507eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.radius))

        data.write(b'\xc2\xbe\x03\r')  # 0xc2be030d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.height))

        data.write(b'\xcfl\x1d\xe9')  # 0xcf6c1de9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcf6c1de9))

        data.write(b'L\xd1E\x9b')  # 0x4cd1459b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.radial_velocity))

        data.write(b'\nW\xb0\x9b')  # 0xa57b09b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.radial_velocity_acceleration))

        data.write(b'\xbd2\x158')  # 0xbd321538
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.visor_electric_effect))

        data.write(b'\xa2\x85\x0b7')  # 0xa2850b37
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_visor_electric))

        data.write(b'V\x93l\x97')  # 0x56936c97
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.optional_shockwave_sound))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            shock_wave_effect=data['shock_wave_effect'],
            damage=DamageInfo.from_json(data['damage']),
            duration=data['duration'],
            knockback_decay_rate=data['knockback_decay_rate'],
            unknown_0x60df1486=data['unknown_0x60df1486'],
            radius=data['radius'],
            height=data['height'],
            unknown_0xcf6c1de9=data['unknown_0xcf6c1de9'],
            radial_velocity=data['radial_velocity'],
            radial_velocity_acceleration=data['radial_velocity_acceleration'],
            visor_electric_effect=data['visor_electric_effect'],
            sound_visor_electric=data['sound_visor_electric'],
            optional_shockwave_sound=data['optional_shockwave_sound'],
        )

    def to_json(self) -> dict:
        return {
            'shock_wave_effect': self.shock_wave_effect,
            'damage': self.damage.to_json(),
            'duration': self.duration,
            'knockback_decay_rate': self.knockback_decay_rate,
            'unknown_0x60df1486': self.unknown_0x60df1486,
            'radius': self.radius,
            'height': self.height,
            'unknown_0xcf6c1de9': self.unknown_0xcf6c1de9,
            'radial_velocity': self.radial_velocity,
            'radial_velocity_acceleration': self.radial_velocity_acceleration,
            'visor_electric_effect': self.visor_electric_effect,
            'sound_visor_electric': self.sound_visor_electric,
            'optional_shockwave_sound': self.optional_shockwave_sound,
        }


def _decode_shock_wave_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_knockback_decay_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x60df1486(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcf6c1de9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_radial_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_radial_velocity_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_visor_electric_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound_visor_electric(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_optional_shockwave_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x369f7d09: ('shock_wave_effect', _decode_shock_wave_effect),
    0x337f9524: ('damage', _decode_damage),
    0x8b51e23f: ('duration', _decode_duration),
    0x320895b: ('knockback_decay_rate', _decode_knockback_decay_rate),
    0x60df1486: ('unknown_0x60df1486', _decode_unknown_0x60df1486),
    0x78c507eb: ('radius', _decode_radius),
    0xc2be030d: ('height', _decode_height),
    0xcf6c1de9: ('unknown_0xcf6c1de9', _decode_unknown_0xcf6c1de9),
    0x4cd1459b: ('radial_velocity', _decode_radial_velocity),
    0xa57b09b: ('radial_velocity_acceleration', _decode_radial_velocity_acceleration),
    0xbd321538: ('visor_electric_effect', _decode_visor_electric_effect),
    0xa2850b37: ('sound_visor_electric', _decode_sound_visor_electric),
    0x56936c97: ('optional_shockwave_sound', _decode_optional_shockwave_sound),
}
