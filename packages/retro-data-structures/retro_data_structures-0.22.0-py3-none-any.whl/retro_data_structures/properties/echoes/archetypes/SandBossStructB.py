# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo


@dataclasses.dataclass()
class SandBossStructB(BaseProperty):
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    duration: float = dataclasses.field(default=15.0)
    change_direction_interval: float = dataclasses.field(default=3.0)
    unknown_0x1b57d422: float = dataclasses.field(default=2.0)
    change_direction_chance: float = dataclasses.field(default=50.0)
    inner_radius: float = dataclasses.field(default=50.0)
    outer_radius: float = dataclasses.field(default=50.0)
    unknown_0x52642b7e: float = dataclasses.field(default=2.0)
    unknown_0xfda3eb4b: float = dataclasses.field(default=1.0)
    turn_speed: float = dataclasses.field(default=10.0)
    unknown_0x47cde539: float = dataclasses.field(default=0.0)
    sound_charge_beam: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_0x8d4f3b88: int = dataclasses.field(default=1)
    unknown_0xbf88fe4f: float = dataclasses.field(default=3.0)
    unknown_0x74c702b3: float = dataclasses.field(default=1.0)

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
        data.write(b'\x00\x0f')  # 15 properties

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 0.5, 'di_knock_back_power': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8bQ\xe2?')  # 0x8b51e23f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.duration))

        data.write(b'\x82\xbe\x06\xba')  # 0x82be06ba
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.change_direction_interval))

        data.write(b'\x1bW\xd4"')  # 0x1b57d422
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1b57d422))

        data.write(b'\x06\x0b\x9b\x84')  # 0x60b9b84
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.change_direction_chance))

        data.write(b'?Z\xf4o')  # 0x3f5af46f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.inner_radius))

        data.write(b'B\xd8B\xcd')  # 0x42d842cd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.outer_radius))

        data.write(b'Rd+~')  # 0x52642b7e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x52642b7e))

        data.write(b'\xfd\xa3\xebK')  # 0xfda3eb4b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfda3eb4b))

        data.write(b'\x02\x0cx\xbb')  # 0x20c78bb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.turn_speed))

        data.write(b'G\xcd\xe59')  # 0x47cde539
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x47cde539))

        data.write(b')\xd8tJ')  # 0x29d8744a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_charge_beam))

        data.write(b'\x8dO;\x88')  # 0x8d4f3b88
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x8d4f3b88))

        data.write(b'\xbf\x88\xfeO')  # 0xbf88fe4f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbf88fe4f))

        data.write(b't\xc7\x02\xb3')  # 0x74c702b3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x74c702b3))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            damage=DamageInfo.from_json(data['damage']),
            duration=data['duration'],
            change_direction_interval=data['change_direction_interval'],
            unknown_0x1b57d422=data['unknown_0x1b57d422'],
            change_direction_chance=data['change_direction_chance'],
            inner_radius=data['inner_radius'],
            outer_radius=data['outer_radius'],
            unknown_0x52642b7e=data['unknown_0x52642b7e'],
            unknown_0xfda3eb4b=data['unknown_0xfda3eb4b'],
            turn_speed=data['turn_speed'],
            unknown_0x47cde539=data['unknown_0x47cde539'],
            sound_charge_beam=data['sound_charge_beam'],
            unknown_0x8d4f3b88=data['unknown_0x8d4f3b88'],
            unknown_0xbf88fe4f=data['unknown_0xbf88fe4f'],
            unknown_0x74c702b3=data['unknown_0x74c702b3'],
        )

    def to_json(self) -> dict:
        return {
            'damage': self.damage.to_json(),
            'duration': self.duration,
            'change_direction_interval': self.change_direction_interval,
            'unknown_0x1b57d422': self.unknown_0x1b57d422,
            'change_direction_chance': self.change_direction_chance,
            'inner_radius': self.inner_radius,
            'outer_radius': self.outer_radius,
            'unknown_0x52642b7e': self.unknown_0x52642b7e,
            'unknown_0xfda3eb4b': self.unknown_0xfda3eb4b,
            'turn_speed': self.turn_speed,
            'unknown_0x47cde539': self.unknown_0x47cde539,
            'sound_charge_beam': self.sound_charge_beam,
            'unknown_0x8d4f3b88': self.unknown_0x8d4f3b88,
            'unknown_0xbf88fe4f': self.unknown_0xbf88fe4f,
            'unknown_0x74c702b3': self.unknown_0x74c702b3,
        }

    def _dependencies_for_damage(self, asset_manager):
        yield from self.damage.dependencies_for(asset_manager)

    def _dependencies_for_sound_charge_beam(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_charge_beam)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_damage, "damage", "DamageInfo"),
            (self._dependencies_for_sound_charge_beam, "sound_charge_beam", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for SandBossStructB.{field_name} ({field_type}): {e}"
                )


def _decode_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 0.5, 'di_knock_back_power': 10.0})


def _decode_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_change_direction_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1b57d422(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_change_direction_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_inner_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_outer_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x52642b7e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xfda3eb4b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x47cde539(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound_charge_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x8d4f3b88(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xbf88fe4f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x74c702b3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x337f9524: ('damage', _decode_damage),
    0x8b51e23f: ('duration', _decode_duration),
    0x82be06ba: ('change_direction_interval', _decode_change_direction_interval),
    0x1b57d422: ('unknown_0x1b57d422', _decode_unknown_0x1b57d422),
    0x60b9b84: ('change_direction_chance', _decode_change_direction_chance),
    0x3f5af46f: ('inner_radius', _decode_inner_radius),
    0x42d842cd: ('outer_radius', _decode_outer_radius),
    0x52642b7e: ('unknown_0x52642b7e', _decode_unknown_0x52642b7e),
    0xfda3eb4b: ('unknown_0xfda3eb4b', _decode_unknown_0xfda3eb4b),
    0x20c78bb: ('turn_speed', _decode_turn_speed),
    0x47cde539: ('unknown_0x47cde539', _decode_unknown_0x47cde539),
    0x29d8744a: ('sound_charge_beam', _decode_sound_charge_beam),
    0x8d4f3b88: ('unknown_0x8d4f3b88', _decode_unknown_0x8d4f3b88),
    0xbf88fe4f: ('unknown_0xbf88fe4f', _decode_unknown_0xbf88fe4f),
    0x74c702b3: ('unknown_0x74c702b3', _decode_unknown_0x74c702b3),
}
