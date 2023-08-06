# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.AudioPlaybackParms import AudioPlaybackParms
from retro_data_structures.properties.echoes.archetypes.EmperorIngStage1TentacleData import EmperorIngStage1TentacleData
from retro_data_structures.properties.echoes.archetypes.UnknownStruct20 import UnknownStruct20
from retro_data_structures.properties.echoes.archetypes.UnknownStruct21 import UnknownStruct21
from retro_data_structures.properties.echoes.archetypes.UnknownStruct22 import UnknownStruct22
from retro_data_structures.properties.echoes.archetypes.UnknownStruct23 import UnknownStruct23
from retro_data_structures.properties.echoes.archetypes.UnknownStruct24 import UnknownStruct24


@dataclasses.dataclass()
class EmperorIngStage1Data(BaseProperty):
    tentacle: EmperorIngStage1TentacleData = dataclasses.field(default_factory=EmperorIngStage1TentacleData)
    unknown_struct20: UnknownStruct20 = dataclasses.field(default_factory=UnknownStruct20)
    unknown_struct21: UnknownStruct21 = dataclasses.field(default_factory=UnknownStruct21)
    unknown_struct22: UnknownStruct22 = dataclasses.field(default_factory=UnknownStruct22)
    unknown_struct23: UnknownStruct23 = dataclasses.field(default_factory=UnknownStruct23)
    unknown_struct24: UnknownStruct24 = dataclasses.field(default_factory=UnknownStruct24)
    heart_exposed_time: float = dataclasses.field(default=0.0)
    unknown_0x905938b8: float = dataclasses.field(default=0.0)
    unknown_0xb826317a: float = dataclasses.field(default=0.0)
    heart_damage_sound: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    turn_speed_accel: float = dataclasses.field(default=0.0)
    max_turn_speed_normal: float = dataclasses.field(default=0.0)
    max_turn_speed_melee: float = dataclasses.field(default=0.0)
    unknown_0xe5a7c358: float = dataclasses.field(default=0.0)
    vulnerability_change_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    taunt_frequency: float = dataclasses.field(default=0.0)
    attack_interval_min: float = dataclasses.field(default=0.0)
    attack_interval_max: float = dataclasses.field(default=0.0)

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
        data.write(b'\x00\x12')  # 18 properties

        data.write(b'\xb3\xc69\x8f')  # 0xb3c6398f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tentacle.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf5\x9f\x9a`')  # 0xf59f9a60
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct20.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa1\xcd\xa0\xb6')  # 0xa1cda0b6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct21.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x85\xf3ds')  # 0x85f36473
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct22.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb4\xbc\x04\xc4')  # 0xb4bc04c4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct23.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8em \xec')  # 0x8e6d20ec
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct24.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa5\x88\xaf\xd1')  # 0xa588afd1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.heart_exposed_time))

        data.write(b'\x90Y8\xb8')  # 0x905938b8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x905938b8))

        data.write(b'\xb8&1z')  # 0xb826317a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb826317a))

        data.write(b'\x88##\x88')  # 0x88232388
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.heart_damage_sound.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc3j\xe5\xca')  # 0xc36ae5ca
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.turn_speed_accel))

        data.write(b'\xd3\r\x9b\xb9')  # 0xd30d9bb9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_turn_speed_normal))

        data.write(b'\xb0,\xd3\x1f')  # 0xb02cd31f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_turn_speed_melee))

        data.write(b'\xe5\xa7\xc3X')  # 0xe5a7c358
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe5a7c358))

        data.write(b'\x935r@')  # 0x93357240
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.vulnerability_change_sound))

        data.write(b'):\x0c\x19')  # 0x293a0c19
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.taunt_frequency))

        data.write(b'1\xeb\xf8i')  # 0x31ebf869
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_interval_min))

        data.write(b'\xd7\x8bW\x88')  # 0xd78b5788
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_interval_max))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            tentacle=EmperorIngStage1TentacleData.from_json(data['tentacle']),
            unknown_struct20=UnknownStruct20.from_json(data['unknown_struct20']),
            unknown_struct21=UnknownStruct21.from_json(data['unknown_struct21']),
            unknown_struct22=UnknownStruct22.from_json(data['unknown_struct22']),
            unknown_struct23=UnknownStruct23.from_json(data['unknown_struct23']),
            unknown_struct24=UnknownStruct24.from_json(data['unknown_struct24']),
            heart_exposed_time=data['heart_exposed_time'],
            unknown_0x905938b8=data['unknown_0x905938b8'],
            unknown_0xb826317a=data['unknown_0xb826317a'],
            heart_damage_sound=AudioPlaybackParms.from_json(data['heart_damage_sound']),
            turn_speed_accel=data['turn_speed_accel'],
            max_turn_speed_normal=data['max_turn_speed_normal'],
            max_turn_speed_melee=data['max_turn_speed_melee'],
            unknown_0xe5a7c358=data['unknown_0xe5a7c358'],
            vulnerability_change_sound=data['vulnerability_change_sound'],
            taunt_frequency=data['taunt_frequency'],
            attack_interval_min=data['attack_interval_min'],
            attack_interval_max=data['attack_interval_max'],
        )

    def to_json(self) -> dict:
        return {
            'tentacle': self.tentacle.to_json(),
            'unknown_struct20': self.unknown_struct20.to_json(),
            'unknown_struct21': self.unknown_struct21.to_json(),
            'unknown_struct22': self.unknown_struct22.to_json(),
            'unknown_struct23': self.unknown_struct23.to_json(),
            'unknown_struct24': self.unknown_struct24.to_json(),
            'heart_exposed_time': self.heart_exposed_time,
            'unknown_0x905938b8': self.unknown_0x905938b8,
            'unknown_0xb826317a': self.unknown_0xb826317a,
            'heart_damage_sound': self.heart_damage_sound.to_json(),
            'turn_speed_accel': self.turn_speed_accel,
            'max_turn_speed_normal': self.max_turn_speed_normal,
            'max_turn_speed_melee': self.max_turn_speed_melee,
            'unknown_0xe5a7c358': self.unknown_0xe5a7c358,
            'vulnerability_change_sound': self.vulnerability_change_sound,
            'taunt_frequency': self.taunt_frequency,
            'attack_interval_min': self.attack_interval_min,
            'attack_interval_max': self.attack_interval_max,
        }

    def _dependencies_for_tentacle(self, asset_manager):
        yield from self.tentacle.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct20(self, asset_manager):
        yield from self.unknown_struct20.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct21(self, asset_manager):
        yield from self.unknown_struct21.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct22(self, asset_manager):
        yield from self.unknown_struct22.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct23(self, asset_manager):
        yield from self.unknown_struct23.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct24(self, asset_manager):
        yield from self.unknown_struct24.dependencies_for(asset_manager)

    def _dependencies_for_heart_damage_sound(self, asset_manager):
        yield from self.heart_damage_sound.dependencies_for(asset_manager)

    def _dependencies_for_vulnerability_change_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.vulnerability_change_sound)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_tentacle, "tentacle", "EmperorIngStage1TentacleData"),
            (self._dependencies_for_unknown_struct20, "unknown_struct20", "UnknownStruct20"),
            (self._dependencies_for_unknown_struct21, "unknown_struct21", "UnknownStruct21"),
            (self._dependencies_for_unknown_struct22, "unknown_struct22", "UnknownStruct22"),
            (self._dependencies_for_unknown_struct23, "unknown_struct23", "UnknownStruct23"),
            (self._dependencies_for_unknown_struct24, "unknown_struct24", "UnknownStruct24"),
            (self._dependencies_for_heart_damage_sound, "heart_damage_sound", "AudioPlaybackParms"),
            (self._dependencies_for_vulnerability_change_sound, "vulnerability_change_sound", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for EmperorIngStage1Data.{field_name} ({field_type}): {e}"
                )


def _decode_tentacle(data: typing.BinaryIO, property_size: int):
    return EmperorIngStage1TentacleData.from_stream(data, property_size)


def _decode_unknown_struct20(data: typing.BinaryIO, property_size: int):
    return UnknownStruct20.from_stream(data, property_size)


def _decode_unknown_struct21(data: typing.BinaryIO, property_size: int):
    return UnknownStruct21.from_stream(data, property_size)


def _decode_unknown_struct22(data: typing.BinaryIO, property_size: int):
    return UnknownStruct22.from_stream(data, property_size)


def _decode_unknown_struct23(data: typing.BinaryIO, property_size: int):
    return UnknownStruct23.from_stream(data, property_size)


def _decode_unknown_struct24(data: typing.BinaryIO, property_size: int):
    return UnknownStruct24.from_stream(data, property_size)


def _decode_heart_exposed_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x905938b8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb826317a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_heart_damage_sound(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_turn_speed_accel(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_turn_speed_normal(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_turn_speed_melee(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe5a7c358(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vulnerability_change_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_taunt_frequency(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_interval_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_interval_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb3c6398f: ('tentacle', _decode_tentacle),
    0xf59f9a60: ('unknown_struct20', _decode_unknown_struct20),
    0xa1cda0b6: ('unknown_struct21', _decode_unknown_struct21),
    0x85f36473: ('unknown_struct22', _decode_unknown_struct22),
    0xb4bc04c4: ('unknown_struct23', _decode_unknown_struct23),
    0x8e6d20ec: ('unknown_struct24', _decode_unknown_struct24),
    0xa588afd1: ('heart_exposed_time', _decode_heart_exposed_time),
    0x905938b8: ('unknown_0x905938b8', _decode_unknown_0x905938b8),
    0xb826317a: ('unknown_0xb826317a', _decode_unknown_0xb826317a),
    0x88232388: ('heart_damage_sound', _decode_heart_damage_sound),
    0xc36ae5ca: ('turn_speed_accel', _decode_turn_speed_accel),
    0xd30d9bb9: ('max_turn_speed_normal', _decode_max_turn_speed_normal),
    0xb02cd31f: ('max_turn_speed_melee', _decode_max_turn_speed_melee),
    0xe5a7c358: ('unknown_0xe5a7c358', _decode_unknown_0xe5a7c358),
    0x93357240: ('vulnerability_change_sound', _decode_vulnerability_change_sound),
    0x293a0c19: ('taunt_frequency', _decode_taunt_frequency),
    0x31ebf869: ('attack_interval_min', _decode_attack_interval_min),
    0xd78b5788: ('attack_interval_max', _decode_attack_interval_max),
}
