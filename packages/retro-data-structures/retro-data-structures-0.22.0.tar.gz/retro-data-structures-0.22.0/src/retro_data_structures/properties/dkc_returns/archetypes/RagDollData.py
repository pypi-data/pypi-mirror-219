# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class RagDollData(BaseProperty):
    gravity: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=-50.0))
    rag_doll_density: float = dataclasses.field(default=8000.0)
    air_density: float = dataclasses.field(default=1.2000000476837158)
    restitution_multiplier: float = dataclasses.field(default=0.125)
    friction_multiplier: float = dataclasses.field(default=0.8500000238418579)
    unknown_0x91936b5e: float = dataclasses.field(default=1.0)
    unknown_0x81d40910: float = dataclasses.field(default=3000.0)
    static_speed: float = dataclasses.field(default=0.5)
    max_time: float = dataclasses.field(default=5.0)
    sound_impact: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0xce5d16c3: bool = dataclasses.field(default=False)
    damp_rotation: bool = dataclasses.field(default=False)
    ignore_max_time: bool = dataclasses.field(default=True)
    ignore_dock_collision: bool = dataclasses.field(default=False)
    ignore_all_collision: bool = dataclasses.field(default=True)
    collision_type: int = dataclasses.field(default=2418955086)  # Choice
    collision_plane_normal: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=1.0))
    collision_plane_constant: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\x12')  # 18 properties

        data.write(b'\x9e#\\a')  # 0x9e235c61
        data.write(b'\x00\x0c')  # size
        self.gravity.to_stream(data)

        data.write(b'j\xb04\x1a')  # 0x6ab0341a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rag_doll_density))

        data.write(b'C\xc0"$')  # 0x43c02224
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.air_density))

        data.write(b'Dj3\xf5')  # 0x446a33f5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.restitution_multiplier))

        data.write(b'\x08\xb31\xce')  # 0x8b331ce
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.friction_multiplier))

        data.write(b'\x91\x93k^')  # 0x91936b5e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x91936b5e))

        data.write(b'\x81\xd4\t\x10')  # 0x81d40910
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x81d40910))

        data.write(b'\x16@~\xd9')  # 0x16407ed9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.static_speed))

        data.write(b'\x03\xe7\xb2\xb4')  # 0x3e7b2b4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_time))

        data.write(b'\xe1\x90\xf7}')  # 0xe190f77d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_impact))

        data.write(b'\xce]\x16\xc3')  # 0xce5d16c3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xce5d16c3))

        data.write(b'\xa9\x9a\x0e3')  # 0xa99a0e33
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.damp_rotation))

        data.write(b'\xe7\xb8\x8dQ')  # 0xe7b88d51
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_max_time))

        data.write(b'}\xe2\xe6\xba')  # 0x7de2e6ba
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_dock_collision))

        data.write(b'\xe1\x10|J')  # 0xe1107c4a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_all_collision))

        data.write(b'\xb6t\xea=')  # 0xb674ea3d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.collision_type))

        data.write(b'\x96\xbb0*')  # 0x96bb302a
        data.write(b'\x00\x0c')  # size
        self.collision_plane_normal.to_stream(data)

        data.write(b'D\x14\xd9\x9c')  # 0x4414d99c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.collision_plane_constant))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            gravity=Vector.from_json(data['gravity']),
            rag_doll_density=data['rag_doll_density'],
            air_density=data['air_density'],
            restitution_multiplier=data['restitution_multiplier'],
            friction_multiplier=data['friction_multiplier'],
            unknown_0x91936b5e=data['unknown_0x91936b5e'],
            unknown_0x81d40910=data['unknown_0x81d40910'],
            static_speed=data['static_speed'],
            max_time=data['max_time'],
            sound_impact=data['sound_impact'],
            unknown_0xce5d16c3=data['unknown_0xce5d16c3'],
            damp_rotation=data['damp_rotation'],
            ignore_max_time=data['ignore_max_time'],
            ignore_dock_collision=data['ignore_dock_collision'],
            ignore_all_collision=data['ignore_all_collision'],
            collision_type=data['collision_type'],
            collision_plane_normal=Vector.from_json(data['collision_plane_normal']),
            collision_plane_constant=data['collision_plane_constant'],
        )

    def to_json(self) -> dict:
        return {
            'gravity': self.gravity.to_json(),
            'rag_doll_density': self.rag_doll_density,
            'air_density': self.air_density,
            'restitution_multiplier': self.restitution_multiplier,
            'friction_multiplier': self.friction_multiplier,
            'unknown_0x91936b5e': self.unknown_0x91936b5e,
            'unknown_0x81d40910': self.unknown_0x81d40910,
            'static_speed': self.static_speed,
            'max_time': self.max_time,
            'sound_impact': self.sound_impact,
            'unknown_0xce5d16c3': self.unknown_0xce5d16c3,
            'damp_rotation': self.damp_rotation,
            'ignore_max_time': self.ignore_max_time,
            'ignore_dock_collision': self.ignore_dock_collision,
            'ignore_all_collision': self.ignore_all_collision,
            'collision_type': self.collision_type,
            'collision_plane_normal': self.collision_plane_normal.to_json(),
            'collision_plane_constant': self.collision_plane_constant,
        }


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_rag_doll_density(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_air_density(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_restitution_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_friction_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x91936b5e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x81d40910(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_static_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound_impact(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xce5d16c3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_damp_rotation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ignore_max_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ignore_dock_collision(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ignore_all_collision(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_collision_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_collision_plane_normal(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_collision_plane_constant(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x9e235c61: ('gravity', _decode_gravity),
    0x6ab0341a: ('rag_doll_density', _decode_rag_doll_density),
    0x43c02224: ('air_density', _decode_air_density),
    0x446a33f5: ('restitution_multiplier', _decode_restitution_multiplier),
    0x8b331ce: ('friction_multiplier', _decode_friction_multiplier),
    0x91936b5e: ('unknown_0x91936b5e', _decode_unknown_0x91936b5e),
    0x81d40910: ('unknown_0x81d40910', _decode_unknown_0x81d40910),
    0x16407ed9: ('static_speed', _decode_static_speed),
    0x3e7b2b4: ('max_time', _decode_max_time),
    0xe190f77d: ('sound_impact', _decode_sound_impact),
    0xce5d16c3: ('unknown_0xce5d16c3', _decode_unknown_0xce5d16c3),
    0xa99a0e33: ('damp_rotation', _decode_damp_rotation),
    0xe7b88d51: ('ignore_max_time', _decode_ignore_max_time),
    0x7de2e6ba: ('ignore_dock_collision', _decode_ignore_dock_collision),
    0xe1107c4a: ('ignore_all_collision', _decode_ignore_all_collision),
    0xb674ea3d: ('collision_type', _decode_collision_type),
    0x96bb302a: ('collision_plane_normal', _decode_collision_plane_normal),
    0x4414d99c: ('collision_plane_constant', _decode_collision_plane_constant),
}
