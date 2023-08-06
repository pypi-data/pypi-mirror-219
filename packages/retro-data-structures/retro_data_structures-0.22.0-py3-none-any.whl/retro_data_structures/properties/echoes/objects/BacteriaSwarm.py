# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.BasicSwarmProperties import BasicSwarmProperties
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class BacteriaSwarm(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    active: bool = dataclasses.field(default=True)
    basic_swarm_properties: BasicSwarmProperties = dataclasses.field(default_factory=BasicSwarmProperties)
    unknown_0x4a85a2da: float = dataclasses.field(default=1.0)
    containment_priority: float = dataclasses.field(default=1.0)
    bacteria_patrol_speed: float = dataclasses.field(default=0.10000000149011612)
    unknown_0x7de56d56: float = dataclasses.field(default=0.5)
    unknown_0x39098c47: float = dataclasses.field(default=0.20000000298023224)
    bacteria_acceleration: float = dataclasses.field(default=0.009999999776482582)
    bacteria_deceleration: float = dataclasses.field(default=0.009999999776482582)
    patrol_turn_speed: float = dataclasses.field(default=180.0)
    unknown_0xbdcdb9c0: float = dataclasses.field(default=1440.0)
    bacteria_particle_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    bacteria_patrol_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    bacteria_player_pursuit_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=0.0, b=0.0, a=0.0))
    color_change_time: float = dataclasses.field(default=0.5)
    patrol_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    pursuit_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_0xad4ce8f3: float = dataclasses.field(default=0.5)
    unknown_0xa9d6d9d9: float = dataclasses.field(default=0.5)
    patrol_sound_weight: float = dataclasses.field(default=0.5)
    unknown_0x90f8e29f: float = dataclasses.field(default=0.5)
    unknown_0x4b47b178: float = dataclasses.field(default=0.5)
    pursuit_sound_weight: float = dataclasses.field(default=0.5)
    unknown_0xd2986c43: float = dataclasses.field(default=0.0)
    max_audible_distance: float = dataclasses.field(default=100.0)
    min_volume: int = dataclasses.field(default=20)
    max_volume: int = dataclasses.field(default=127)
    bacteria_scan_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    spawn_instantly: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'BSWM'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['BacteriaSwarm.rel']

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
        data.write(b'\x00 ')  # 32 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
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

        data.write(b'\xe2_\xb0\x8c')  # 0xe25fb08c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6\xbb/E')  # 0xc6bb2f45
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.active))

        data.write(b'\xe1\xecsF')  # 0xe1ec7346
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.basic_swarm_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'J\x85\xa2\xda')  # 0x4a85a2da
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4a85a2da))

        data.write(b'\x7f\xf1F\x9e')  # 0x7ff1469e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.containment_priority))

        data.write(b'\xf8\x7f\xd6\xa9')  # 0xf87fd6a9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bacteria_patrol_speed))

        data.write(b'}\xe5mV')  # 0x7de56d56
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7de56d56))

        data.write(b'9\t\x8cG')  # 0x39098c47
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x39098c47))

        data.write(b'\xfb\xa2\xa5>')  # 0xfba2a53e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bacteria_acceleration))

        data.write(b'\\\x9d V')  # 0x5c9d2056
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bacteria_deceleration))

        data.write(b'w\x1a\x90\xe6')  # 0x771a90e6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.patrol_turn_speed))

        data.write(b'\xbd\xcd\xb9\xc0')  # 0xbdcdb9c0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbdcdb9c0))

        data.write(b'#\x01)J')  # 0x2301294a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.bacteria_particle_effect))

        data.write(b'\xac*Fz')  # 0xac2a467a
        data.write(b'\x00\x10')  # size
        self.bacteria_patrol_color.to_stream(data)

        data.write(b'm\\\x1c\x94')  # 0x6d5c1c94
        data.write(b'\x00\x10')  # size
        self.bacteria_player_pursuit_color.to_stream(data)

        data.write(b'1\x1b\x07P')  # 0x311b0750
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.color_change_time))

        data.write(b'J\xb2Bu')  # 0x4ab24275
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.patrol_sound))

        data.write(b'\xfe>{\xbf')  # 0xfe3e7bbf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.pursuit_sound))

        data.write(b'\xadL\xe8\xf3')  # 0xad4ce8f3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xad4ce8f3))

        data.write(b'\xa9\xd6\xd9\xd9')  # 0xa9d6d9d9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa9d6d9d9))

        data.write(b'\x9f\xe2S\xa5')  # 0x9fe253a5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.patrol_sound_weight))

        data.write(b'\x90\xf8\xe2\x9f')  # 0x90f8e29f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x90f8e29f))

        data.write(b'KG\xb1x')  # 0x4b47b178
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4b47b178))

        data.write(b'\xe6x\xeb\xcf')  # 0xe678ebcf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pursuit_sound_weight))

        data.write(b'\xd2\x98lC')  # 0xd2986c43
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd2986c43))

        data.write(b'!NH\xa0')  # 0x214e48a0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_audible_distance))

        data.write(b'Wa\x94\x96')  # 0x57619496
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.min_volume))

        data.write(b'\xc7\x12\x84|')  # 0xc712847c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_volume))

        data.write(b'uz\x1c4')  # 0x757a1c34
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.bacteria_scan_model))

        data.write(b'\xc5\xbc^\xd0')  # 0xc5bc5ed0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.spawn_instantly))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            animation_information=AnimationParameters.from_json(data['animation_information']),
            active=data['active'],
            basic_swarm_properties=BasicSwarmProperties.from_json(data['basic_swarm_properties']),
            unknown_0x4a85a2da=data['unknown_0x4a85a2da'],
            containment_priority=data['containment_priority'],
            bacteria_patrol_speed=data['bacteria_patrol_speed'],
            unknown_0x7de56d56=data['unknown_0x7de56d56'],
            unknown_0x39098c47=data['unknown_0x39098c47'],
            bacteria_acceleration=data['bacteria_acceleration'],
            bacteria_deceleration=data['bacteria_deceleration'],
            patrol_turn_speed=data['patrol_turn_speed'],
            unknown_0xbdcdb9c0=data['unknown_0xbdcdb9c0'],
            bacteria_particle_effect=data['bacteria_particle_effect'],
            bacteria_patrol_color=Color.from_json(data['bacteria_patrol_color']),
            bacteria_player_pursuit_color=Color.from_json(data['bacteria_player_pursuit_color']),
            color_change_time=data['color_change_time'],
            patrol_sound=data['patrol_sound'],
            pursuit_sound=data['pursuit_sound'],
            unknown_0xad4ce8f3=data['unknown_0xad4ce8f3'],
            unknown_0xa9d6d9d9=data['unknown_0xa9d6d9d9'],
            patrol_sound_weight=data['patrol_sound_weight'],
            unknown_0x90f8e29f=data['unknown_0x90f8e29f'],
            unknown_0x4b47b178=data['unknown_0x4b47b178'],
            pursuit_sound_weight=data['pursuit_sound_weight'],
            unknown_0xd2986c43=data['unknown_0xd2986c43'],
            max_audible_distance=data['max_audible_distance'],
            min_volume=data['min_volume'],
            max_volume=data['max_volume'],
            bacteria_scan_model=data['bacteria_scan_model'],
            spawn_instantly=data['spawn_instantly'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'actor_information': self.actor_information.to_json(),
            'animation_information': self.animation_information.to_json(),
            'active': self.active,
            'basic_swarm_properties': self.basic_swarm_properties.to_json(),
            'unknown_0x4a85a2da': self.unknown_0x4a85a2da,
            'containment_priority': self.containment_priority,
            'bacteria_patrol_speed': self.bacteria_patrol_speed,
            'unknown_0x7de56d56': self.unknown_0x7de56d56,
            'unknown_0x39098c47': self.unknown_0x39098c47,
            'bacteria_acceleration': self.bacteria_acceleration,
            'bacteria_deceleration': self.bacteria_deceleration,
            'patrol_turn_speed': self.patrol_turn_speed,
            'unknown_0xbdcdb9c0': self.unknown_0xbdcdb9c0,
            'bacteria_particle_effect': self.bacteria_particle_effect,
            'bacteria_patrol_color': self.bacteria_patrol_color.to_json(),
            'bacteria_player_pursuit_color': self.bacteria_player_pursuit_color.to_json(),
            'color_change_time': self.color_change_time,
            'patrol_sound': self.patrol_sound,
            'pursuit_sound': self.pursuit_sound,
            'unknown_0xad4ce8f3': self.unknown_0xad4ce8f3,
            'unknown_0xa9d6d9d9': self.unknown_0xa9d6d9d9,
            'patrol_sound_weight': self.patrol_sound_weight,
            'unknown_0x90f8e29f': self.unknown_0x90f8e29f,
            'unknown_0x4b47b178': self.unknown_0x4b47b178,
            'pursuit_sound_weight': self.pursuit_sound_weight,
            'unknown_0xd2986c43': self.unknown_0xd2986c43,
            'max_audible_distance': self.max_audible_distance,
            'min_volume': self.min_volume,
            'max_volume': self.max_volume,
            'bacteria_scan_model': self.bacteria_scan_model,
            'spawn_instantly': self.spawn_instantly,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def _dependencies_for_animation_information(self, asset_manager):
        yield from self.animation_information.dependencies_for(asset_manager)

    def _dependencies_for_basic_swarm_properties(self, asset_manager):
        yield from self.basic_swarm_properties.dependencies_for(asset_manager)

    def _dependencies_for_bacteria_particle_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.bacteria_particle_effect)

    def _dependencies_for_patrol_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.patrol_sound)

    def _dependencies_for_pursuit_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.pursuit_sound)

    def _dependencies_for_bacteria_scan_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.bacteria_scan_model)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
            (self._dependencies_for_animation_information, "animation_information", "AnimationParameters"),
            (self._dependencies_for_basic_swarm_properties, "basic_swarm_properties", "BasicSwarmProperties"),
            (self._dependencies_for_bacteria_particle_effect, "bacteria_particle_effect", "AssetId"),
            (self._dependencies_for_patrol_sound, "patrol_sound", "int"),
            (self._dependencies_for_pursuit_sound, "pursuit_sound", "int"),
            (self._dependencies_for_bacteria_scan_model, "bacteria_scan_model", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for BacteriaSwarm.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_active(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_basic_swarm_properties(data: typing.BinaryIO, property_size: int):
    return BasicSwarmProperties.from_stream(data, property_size)


def _decode_unknown_0x4a85a2da(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_containment_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bacteria_patrol_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7de56d56(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x39098c47(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bacteria_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bacteria_deceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_patrol_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbdcdb9c0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bacteria_particle_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_bacteria_patrol_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_bacteria_player_pursuit_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_color_change_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_patrol_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_pursuit_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xad4ce8f3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa9d6d9d9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_patrol_sound_weight(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x90f8e29f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4b47b178(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pursuit_sound_weight(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd2986c43(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_audible_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_max_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_bacteria_scan_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_spawn_instantly(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xe25fb08c: ('animation_information', _decode_animation_information),
    0xc6bb2f45: ('active', _decode_active),
    0xe1ec7346: ('basic_swarm_properties', _decode_basic_swarm_properties),
    0x4a85a2da: ('unknown_0x4a85a2da', _decode_unknown_0x4a85a2da),
    0x7ff1469e: ('containment_priority', _decode_containment_priority),
    0xf87fd6a9: ('bacteria_patrol_speed', _decode_bacteria_patrol_speed),
    0x7de56d56: ('unknown_0x7de56d56', _decode_unknown_0x7de56d56),
    0x39098c47: ('unknown_0x39098c47', _decode_unknown_0x39098c47),
    0xfba2a53e: ('bacteria_acceleration', _decode_bacteria_acceleration),
    0x5c9d2056: ('bacteria_deceleration', _decode_bacteria_deceleration),
    0x771a90e6: ('patrol_turn_speed', _decode_patrol_turn_speed),
    0xbdcdb9c0: ('unknown_0xbdcdb9c0', _decode_unknown_0xbdcdb9c0),
    0x2301294a: ('bacteria_particle_effect', _decode_bacteria_particle_effect),
    0xac2a467a: ('bacteria_patrol_color', _decode_bacteria_patrol_color),
    0x6d5c1c94: ('bacteria_player_pursuit_color', _decode_bacteria_player_pursuit_color),
    0x311b0750: ('color_change_time', _decode_color_change_time),
    0x4ab24275: ('patrol_sound', _decode_patrol_sound),
    0xfe3e7bbf: ('pursuit_sound', _decode_pursuit_sound),
    0xad4ce8f3: ('unknown_0xad4ce8f3', _decode_unknown_0xad4ce8f3),
    0xa9d6d9d9: ('unknown_0xa9d6d9d9', _decode_unknown_0xa9d6d9d9),
    0x9fe253a5: ('patrol_sound_weight', _decode_patrol_sound_weight),
    0x90f8e29f: ('unknown_0x90f8e29f', _decode_unknown_0x90f8e29f),
    0x4b47b178: ('unknown_0x4b47b178', _decode_unknown_0x4b47b178),
    0xe678ebcf: ('pursuit_sound_weight', _decode_pursuit_sound_weight),
    0xd2986c43: ('unknown_0xd2986c43', _decode_unknown_0xd2986c43),
    0x214e48a0: ('max_audible_distance', _decode_max_audible_distance),
    0x57619496: ('min_volume', _decode_min_volume),
    0xc712847c: ('max_volume', _decode_max_volume),
    0x757a1c34: ('bacteria_scan_model', _decode_bacteria_scan_model),
    0xc5bc5ed0: ('spawn_instantly', _decode_spawn_instantly),
}
