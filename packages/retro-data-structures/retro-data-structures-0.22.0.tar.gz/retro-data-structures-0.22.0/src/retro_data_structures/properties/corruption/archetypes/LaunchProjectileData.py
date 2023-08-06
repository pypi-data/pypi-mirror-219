# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Vector import Vector


@dataclasses.dataclass()
class LaunchProjectileData(BaseProperty):
    projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0))
    delay: float = dataclasses.field(default=1.0)
    delay_variance: float = dataclasses.field(default=0.0)
    visor_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sound_visor_effect: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    stop_homing_range: float = dataclasses.field(default=20.0)
    burn_damage: float = dataclasses.field(default=1.0)
    burn_duration: float = dataclasses.field(default=3.0)
    targetable: bool = dataclasses.field(default=True)
    collision_box: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0))
    hit_points: float = dataclasses.field(default=1.0)
    generate_pickup_chance: float = dataclasses.field(default=0.0)

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
        num_properties_offset = data.tell()
        data.write(b'\x00\x07')  # 7 properties
        num_properties_written = 7

        data.write(b'\xefH]\xb9')  # 0xef485db9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.projectile))

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf7&\xe5\xda')  # 0xf726e5da
        data.write(b'\x00\x0c')  # size
        self.scale.to_stream(data)

        data.write(b'\x14\xff\xf3\x9c')  # 0x14fff39c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay))

        data.write(b'}\xa8\xea#')  # 0x7da8ea23
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay_variance))

        data.write(b'\xe9\xc8\xe2\xbd')  # 0xe9c8e2bd
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.visor_effect))

        data.write(b'\xa3\xe8\xecN')  # 0xa3e8ec4e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_visor_effect))

        if self.stop_homing_range != default_override.get('stop_homing_range', 20.0):
            num_properties_written += 1
            data.write(b'\x05:\xe4\xa7')  # 0x53ae4a7
            data.write(b'\x00\x04')  # size
            data.write(struct.pack('>f', self.stop_homing_range))

        if self.burn_damage != default_override.get('burn_damage', 1.0):
            num_properties_written += 1
            data.write(b'\xcf \x1b\xfa')  # 0xcf201bfa
            data.write(b'\x00\x04')  # size
            data.write(struct.pack('>f', self.burn_damage))

        if self.burn_duration != default_override.get('burn_duration', 3.0):
            num_properties_written += 1
            data.write(b'\x88\x13\x7f\xa8')  # 0x88137fa8
            data.write(b'\x00\x04')  # size
            data.write(struct.pack('>f', self.burn_duration))

        if self.targetable != default_override.get('targetable', True):
            num_properties_written += 1
            data.write(b'\xb2\xd0##')  # 0xb2d02323
            data.write(b'\x00\x01')  # size
            data.write(struct.pack('>?', self.targetable))

        if self.collision_box != default_override.get('collision_box', Vector(x=1.0, y=1.0, z=1.0)):
            num_properties_written += 1
            data.write(b'\xf3D\xc0\xb0')  # 0xf344c0b0
            data.write(b'\x00\x0c')  # size
            self.collision_box.to_stream(data)

        if self.hit_points != default_override.get('hit_points', 1.0):
            num_properties_written += 1
            data.write(b'\x05k \xb2')  # 0x56b20b2
            data.write(b'\x00\x04')  # size
            data.write(struct.pack('>f', self.hit_points))

        if self.generate_pickup_chance != default_override.get('generate_pickup_chance', 0.0):
            num_properties_written += 1
            data.write(b'\xf7\x84i\xd6')  # 0xf78469d6
            data.write(b'\x00\x04')  # size
            data.write(struct.pack('>f', self.generate_pickup_chance))

        if num_properties_written != 7:
            struct_end_offset = data.tell()
            data.seek(num_properties_offset)
            data.write(struct.pack(">H", num_properties_written))
            data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            projectile=data['projectile'],
            damage=DamageInfo.from_json(data['damage']),
            scale=Vector.from_json(data['scale']),
            delay=data['delay'],
            delay_variance=data['delay_variance'],
            visor_effect=data['visor_effect'],
            sound_visor_effect=data['sound_visor_effect'],
            stop_homing_range=data['stop_homing_range'],
            burn_damage=data['burn_damage'],
            burn_duration=data['burn_duration'],
            targetable=data['targetable'],
            collision_box=Vector.from_json(data['collision_box']),
            hit_points=data['hit_points'],
            generate_pickup_chance=data['generate_pickup_chance'],
        )

    def to_json(self) -> dict:
        return {
            'projectile': self.projectile,
            'damage': self.damage.to_json(),
            'scale': self.scale.to_json(),
            'delay': self.delay,
            'delay_variance': self.delay_variance,
            'visor_effect': self.visor_effect,
            'sound_visor_effect': self.sound_visor_effect,
            'stop_homing_range': self.stop_homing_range,
            'burn_damage': self.burn_damage,
            'burn_duration': self.burn_duration,
            'targetable': self.targetable,
            'collision_box': self.collision_box.to_json(),
            'hit_points': self.hit_points,
            'generate_pickup_chance': self.generate_pickup_chance,
        }


def _decode_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_delay_variance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_visor_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound_visor_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_stop_homing_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_burn_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_burn_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_targetable(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_collision_box(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_hit_points(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_generate_pickup_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xef485db9: ('projectile', _decode_projectile),
    0x337f9524: ('damage', _decode_damage),
    0xf726e5da: ('scale', _decode_scale),
    0x14fff39c: ('delay', _decode_delay),
    0x7da8ea23: ('delay_variance', _decode_delay_variance),
    0xe9c8e2bd: ('visor_effect', _decode_visor_effect),
    0xa3e8ec4e: ('sound_visor_effect', _decode_sound_visor_effect),
    0x53ae4a7: ('stop_homing_range', _decode_stop_homing_range),
    0xcf201bfa: ('burn_damage', _decode_burn_damage),
    0x88137fa8: ('burn_duration', _decode_burn_duration),
    0xb2d02323: ('targetable', _decode_targetable),
    0xf344c0b0: ('collision_box', _decode_collision_box),
    0x56b20b2: ('hit_points', _decode_hit_points),
    0xf78469d6: ('generate_pickup_chance', _decode_generate_pickup_chance),
}
