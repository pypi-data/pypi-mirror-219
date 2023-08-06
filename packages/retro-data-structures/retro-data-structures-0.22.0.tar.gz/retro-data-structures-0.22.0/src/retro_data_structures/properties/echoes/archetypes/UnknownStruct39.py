# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo


@dataclasses.dataclass()
class UnknownStruct39(BaseProperty):
    start_state: int = dataclasses.field(default=10)
    explosion_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    min_height: float = dataclasses.field(default=4.0)
    max_height: float = dataclasses.field(default=4.0)
    min_down_height: float = dataclasses.field(default=4.0)
    max_down_height: float = dataclasses.field(default=4.0)
    separation_distance: float = dataclasses.field(default=5.0)
    min_life_time: float = dataclasses.field(default=14.0)
    max_life_time: float = dataclasses.field(default=16.0)
    normal_knockback: float = dataclasses.field(default=20.0)
    heavy_knockback: float = dataclasses.field(default=40.0)
    knockback_decline: float = dataclasses.field(default=100.0)
    is_dark_shredder: bool = dataclasses.field(default=False)
    desired_distance: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'F\xd8f\xd1')  # 0x46d866d1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.start_state))

        data.write(b'\xde\xfft\xea')  # 0xdeff74ea
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.explosion_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6\xc4#,')  # 0xc6c4232c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_height))

        data.write(b'\x7f\xe2\xb8]')  # 0x7fe2b85d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_height))

        data.write(b'\x10\xbe\x8a\xd3')  # 0x10be8ad3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_down_height))

        data.write(b'C\x18\x927')  # 0x43189237
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_down_height))

        data.write(b"\x01U\x9f'")  # 0x1559f27
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.separation_distance))

        data.write(b'\x07\xdc\xd4\x04')  # 0x7dcd404
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_life_time))

        data.write(b'V%oY')  # 0x56256f59
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_life_time))

        data.write(b'0a\x97l')  # 0x3061976c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.normal_knockback))

        data.write(b'\x93\xa8\n\xa2')  # 0x93a80aa2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.heavy_knockback))

        data.write(b'Lk$!')  # 0x4c6b2421
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.knockback_decline))

        data.write(b'\xcf\xf9\x97\x1b')  # 0xcff9971b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_dark_shredder))

        data.write(b'`\xbe5\xa1')  # 0x60be35a1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.desired_distance))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            start_state=data['start_state'],
            explosion_damage=DamageInfo.from_json(data['explosion_damage']),
            min_height=data['min_height'],
            max_height=data['max_height'],
            min_down_height=data['min_down_height'],
            max_down_height=data['max_down_height'],
            separation_distance=data['separation_distance'],
            min_life_time=data['min_life_time'],
            max_life_time=data['max_life_time'],
            normal_knockback=data['normal_knockback'],
            heavy_knockback=data['heavy_knockback'],
            knockback_decline=data['knockback_decline'],
            is_dark_shredder=data['is_dark_shredder'],
            desired_distance=data['desired_distance'],
        )

    def to_json(self) -> dict:
        return {
            'start_state': self.start_state,
            'explosion_damage': self.explosion_damage.to_json(),
            'min_height': self.min_height,
            'max_height': self.max_height,
            'min_down_height': self.min_down_height,
            'max_down_height': self.max_down_height,
            'separation_distance': self.separation_distance,
            'min_life_time': self.min_life_time,
            'max_life_time': self.max_life_time,
            'normal_knockback': self.normal_knockback,
            'heavy_knockback': self.heavy_knockback,
            'knockback_decline': self.knockback_decline,
            'is_dark_shredder': self.is_dark_shredder,
            'desired_distance': self.desired_distance,
        }

    def _dependencies_for_explosion_damage(self, asset_manager):
        yield from self.explosion_damage.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_explosion_damage, "explosion_damage", "DamageInfo"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for UnknownStruct39.{field_name} ({field_type}): {e}"
                )


def _decode_start_state(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_explosion_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_min_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_down_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_down_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_separation_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_life_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_life_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_normal_knockback(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_heavy_knockback(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_knockback_decline(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_is_dark_shredder(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_desired_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x46d866d1: ('start_state', _decode_start_state),
    0xdeff74ea: ('explosion_damage', _decode_explosion_damage),
    0xc6c4232c: ('min_height', _decode_min_height),
    0x7fe2b85d: ('max_height', _decode_max_height),
    0x10be8ad3: ('min_down_height', _decode_min_down_height),
    0x43189237: ('max_down_height', _decode_max_down_height),
    0x1559f27: ('separation_distance', _decode_separation_distance),
    0x7dcd404: ('min_life_time', _decode_min_life_time),
    0x56256f59: ('max_life_time', _decode_max_life_time),
    0x3061976c: ('normal_knockback', _decode_normal_knockback),
    0x93a80aa2: ('heavy_knockback', _decode_heavy_knockback),
    0x4c6b2421: ('knockback_decline', _decode_knockback_decline),
    0xcff9971b: ('is_dark_shredder', _decode_is_dark_shredder),
    0x60be35a1: ('desired_distance', _decode_desired_distance),
}
