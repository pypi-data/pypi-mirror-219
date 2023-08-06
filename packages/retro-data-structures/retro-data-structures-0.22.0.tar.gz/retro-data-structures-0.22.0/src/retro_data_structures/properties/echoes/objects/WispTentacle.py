# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.PatternedAITypedef import PatternedAITypedef


@dataclasses.dataclass()
class WispTentacle(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    wake_up_distance: float = dataclasses.field(default=30.0)
    search_distance: float = dataclasses.field(default=20.0)
    attack_distance: float = dataclasses.field(default=10.0)
    detection_height: float = dataclasses.field(default=0.0)
    attack_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    spawn_from_portal: bool = dataclasses.field(default=False)
    hurt_sleep_delay: float = dataclasses.field(default=2.0)
    grab_blend_time: float = dataclasses.field(default=0.20000000298023224)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'WISP'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['WispTentacle.rel']

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

        data.write(b'\xd8(\x14\xf2')  # 0xd82814f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.wake_up_distance))

        data.write(b'\xa8\xac\x80\xdd')  # 0xa8ac80dd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.search_distance))

        data.write(b'^\xda\x8d\x99')  # 0x5eda8d99
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_distance))

        data.write(b'\x9b\xb6\xcb\xc7')  # 0x9bb6cbc7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.detection_height))

        data.write(b'f\xdc\xaa\xcb')  # 0x66dcaacb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attack_damage.to_stream(data, default_override={'di_weapon_type': 9, 'di_damage': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xedt!\xff')  # 0xed7421ff
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.spawn_from_portal))

        data.write(b'\x9bZGD')  # 0x9b5a4744
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hurt_sleep_delay))

        data.write(b'\rZ\x1f\x1d')  # 0xd5a1f1d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grab_blend_time))

        data.write(b'\xb3wGP')  # 0xb3774750
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned.to_stream(data)
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

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            wake_up_distance=data['wake_up_distance'],
            search_distance=data['search_distance'],
            attack_distance=data['attack_distance'],
            detection_height=data['detection_height'],
            attack_damage=DamageInfo.from_json(data['attack_damage']),
            spawn_from_portal=data['spawn_from_portal'],
            hurt_sleep_delay=data['hurt_sleep_delay'],
            grab_blend_time=data['grab_blend_time'],
            patterned=PatternedAITypedef.from_json(data['patterned']),
            actor_information=ActorParameters.from_json(data['actor_information']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'wake_up_distance': self.wake_up_distance,
            'search_distance': self.search_distance,
            'attack_distance': self.attack_distance,
            'detection_height': self.detection_height,
            'attack_damage': self.attack_damage.to_json(),
            'spawn_from_portal': self.spawn_from_portal,
            'hurt_sleep_delay': self.hurt_sleep_delay,
            'grab_blend_time': self.grab_blend_time,
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_attack_damage(self, asset_manager):
        yield from self.attack_damage.dependencies_for(asset_manager)

    def _dependencies_for_patterned(self, asset_manager):
        yield from self.patterned.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_attack_damage, "attack_damage", "DamageInfo"),
            (self._dependencies_for_patterned, "patterned", "PatternedAITypedef"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for WispTentacle.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_wake_up_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_search_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_detection_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 9, 'di_damage': 5.0})


def _decode_spawn_from_portal(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_hurt_sleep_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grab_blend_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xd82814f2: ('wake_up_distance', _decode_wake_up_distance),
    0xa8ac80dd: ('search_distance', _decode_search_distance),
    0x5eda8d99: ('attack_distance', _decode_attack_distance),
    0x9bb6cbc7: ('detection_height', _decode_detection_height),
    0x66dcaacb: ('attack_damage', _decode_attack_damage),
    0xed7421ff: ('spawn_from_portal', _decode_spawn_from_portal),
    0x9b5a4744: ('hurt_sleep_delay', _decode_hurt_sleep_delay),
    0xd5a1f1d: ('grab_blend_time', _decode_grab_blend_time),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
}
