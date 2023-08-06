# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.AudioPlaybackParms import AudioPlaybackParms
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class Metaree(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    radius_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    drop_height: float = dataclasses.field(default=3.0)
    unknown: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    attack_speed: float = dataclasses.field(default=5.0)
    drop_delay: float = dataclasses.field(default=0.0)
    halt_delay: float = dataclasses.field(default=0.0)
    launch_speed: float = dataclasses.field(default=0.0)
    turn_sound: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'MREE'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['Metaree.rel']

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

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

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb3wGP')  # 0xb3774750
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned.to_stream(data, default_override={'detection_range': 10.0, 'max_attack_range': 30.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x08mX\xdd')  # 0x86d58dd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.radius_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 5.0, 'di_knock_back_power': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'8\xa5Vo')  # 0x38a5566f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.drop_height))

        data.write(b'\xa2\x87\x07}')  # 0xa287077d
        data.write(b'\x00\x0c')  # size
        self.unknown.to_stream(data)

        data.write(b'l\n+\xc8')  # 0x6c0a2bc8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_speed))

        data.write(b'\x00\x97\xf2\x82')  # 0x97f282
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.drop_delay))

        data.write(b'\xe4\xe8\x08\xc9')  # 0xe4e808c9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.halt_delay))

        data.write(b'18\x1a\x17')  # 0x31381a17
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.launch_speed))

        data.write(b'\xea\x11\xd1\xfa')  # 0xea11d1fa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.turn_sound.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            patterned=PatternedAITypedef.from_json(data['patterned']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            radius_damage=DamageInfo.from_json(data['radius_damage']),
            drop_height=data['drop_height'],
            unknown=Vector.from_json(data['unknown']),
            attack_speed=data['attack_speed'],
            drop_delay=data['drop_delay'],
            halt_delay=data['halt_delay'],
            launch_speed=data['launch_speed'],
            turn_sound=AudioPlaybackParms.from_json(data['turn_sound']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'radius_damage': self.radius_damage.to_json(),
            'drop_height': self.drop_height,
            'unknown': self.unknown.to_json(),
            'attack_speed': self.attack_speed,
            'drop_delay': self.drop_delay,
            'halt_delay': self.halt_delay,
            'launch_speed': self.launch_speed,
            'turn_sound': self.turn_sound.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_patterned(self, asset_manager):
        yield from self.patterned.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def _dependencies_for_radius_damage(self, asset_manager):
        yield from self.radius_damage.dependencies_for(asset_manager)

    def _dependencies_for_turn_sound(self, asset_manager):
        yield from self.turn_sound.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_patterned, "patterned", "PatternedAITypedef"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
            (self._dependencies_for_radius_damage, "radius_damage", "DamageInfo"),
            (self._dependencies_for_turn_sound, "turn_sound", "AudioPlaybackParms"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Metaree.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'detection_range': 10.0, 'max_attack_range': 30.0})


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_radius_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 5.0, 'di_knock_back_power': 5.0})


def _decode_drop_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_attack_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_drop_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_halt_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_launch_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_turn_sound(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x86d58dd: ('radius_damage', _decode_radius_damage),
    0x38a5566f: ('drop_height', _decode_drop_height),
    0xa287077d: ('unknown', _decode_unknown),
    0x6c0a2bc8: ('attack_speed', _decode_attack_speed),
    0x97f282: ('drop_delay', _decode_drop_delay),
    0xe4e808c9: ('halt_delay', _decode_halt_delay),
    0x31381a17: ('launch_speed', _decode_launch_speed),
    0xea11d1fa: ('turn_sound', _decode_turn_sound),
}
