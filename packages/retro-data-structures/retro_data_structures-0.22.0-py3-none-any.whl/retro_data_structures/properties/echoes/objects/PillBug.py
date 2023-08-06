# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.PatternedAITypedef import PatternedAITypedef


@dataclasses.dataclass()
class PillBug(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unknown_0xde7e9f94: int = dataclasses.field(default=0)
    floor_turn_speed: float = dataclasses.field(default=120.0)
    stick_radius: float = dataclasses.field(default=0.20000000298023224)
    waypoint_approach_distance: float = dataclasses.field(default=1.5)
    visible_distance: float = dataclasses.field(default=200.0)
    damage_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    wander_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    crawl_radius: float = dataclasses.field(default=0.3499999940395355)
    roll_radius: float = dataclasses.field(default=0.5)
    unknown_0x519c7197: float = dataclasses.field(default=0.5)
    unknown_0xa265383c: float = dataclasses.field(default=0.019999999552965164)
    forward_priority: float = dataclasses.field(default=0.30000001192092896)
    unknown_0x558c0692: float = dataclasses.field(default=0.6000000238418579)
    unknown_0x0f991bf1: float = dataclasses.field(default=1.5)
    unknown_0x385a1bed: float = dataclasses.field(default=0.6000000238418579)
    unknown_0xcf4ea141: float = dataclasses.field(default=1.5)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'PILB'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['WallCrawler.rel', 'PillBug.rel']

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
        data.write(b'\x00\x13')  # 19 properties

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

        data.write(b'\xde~\x9f\x94')  # 0xde7e9f94
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xde7e9f94))

        data.write(b'\x8eO{)')  # 0x8e4f7b29
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.floor_turn_speed))

        data.write(b'Z:0\xf4')  # 0x5a3a30f4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stick_radius))

        data.write(b's;\xd2|')  # 0x733bd27c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.waypoint_approach_distance))

        data.write(b'\xa7%0\xe8')  # 0xa72530e8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.visible_distance))

        data.write(b']\x84\xedq')  # 0x5d84ed71
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf3\x82\xdf\xf7')  # 0xf382dff7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.wander_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xad\x98\xe1m')  # 0xad98e16d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.crawl_radius))

        data.write(b'\x81\xd6\x99\xb0')  # 0x81d699b0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.roll_radius))

        data.write(b'Q\x9cq\x97')  # 0x519c7197
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x519c7197))

        data.write(b'\xa2e8<')  # 0xa265383c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa265383c))

        data.write(b'\xad\x08\xe1\x89')  # 0xad08e189
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forward_priority))

        data.write(b'U\x8c\x06\x92')  # 0x558c0692
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x558c0692))

        data.write(b'\x0f\x99\x1b\xf1')  # 0xf991bf1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0f991bf1))

        data.write(b'8Z\x1b\xed')  # 0x385a1bed
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x385a1bed))

        data.write(b'\xcfN\xa1A')  # 0xcf4ea141
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcf4ea141))

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
            unknown_0xde7e9f94=data['unknown_0xde7e9f94'],
            floor_turn_speed=data['floor_turn_speed'],
            stick_radius=data['stick_radius'],
            waypoint_approach_distance=data['waypoint_approach_distance'],
            visible_distance=data['visible_distance'],
            damage_vulnerability=DamageVulnerability.from_json(data['damage_vulnerability']),
            wander_vulnerability=DamageVulnerability.from_json(data['wander_vulnerability']),
            crawl_radius=data['crawl_radius'],
            roll_radius=data['roll_radius'],
            unknown_0x519c7197=data['unknown_0x519c7197'],
            unknown_0xa265383c=data['unknown_0xa265383c'],
            forward_priority=data['forward_priority'],
            unknown_0x558c0692=data['unknown_0x558c0692'],
            unknown_0x0f991bf1=data['unknown_0x0f991bf1'],
            unknown_0x385a1bed=data['unknown_0x385a1bed'],
            unknown_0xcf4ea141=data['unknown_0xcf4ea141'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'unknown_0xde7e9f94': self.unknown_0xde7e9f94,
            'floor_turn_speed': self.floor_turn_speed,
            'stick_radius': self.stick_radius,
            'waypoint_approach_distance': self.waypoint_approach_distance,
            'visible_distance': self.visible_distance,
            'damage_vulnerability': self.damage_vulnerability.to_json(),
            'wander_vulnerability': self.wander_vulnerability.to_json(),
            'crawl_radius': self.crawl_radius,
            'roll_radius': self.roll_radius,
            'unknown_0x519c7197': self.unknown_0x519c7197,
            'unknown_0xa265383c': self.unknown_0xa265383c,
            'forward_priority': self.forward_priority,
            'unknown_0x558c0692': self.unknown_0x558c0692,
            'unknown_0x0f991bf1': self.unknown_0x0f991bf1,
            'unknown_0x385a1bed': self.unknown_0x385a1bed,
            'unknown_0xcf4ea141': self.unknown_0xcf4ea141,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_patterned(self, asset_manager):
        yield from self.patterned.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def _dependencies_for_damage_vulnerability(self, asset_manager):
        yield from self.damage_vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_wander_vulnerability(self, asset_manager):
        yield from self.wander_vulnerability.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_patterned, "patterned", "PatternedAITypedef"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
            (self._dependencies_for_damage_vulnerability, "damage_vulnerability", "DamageVulnerability"),
            (self._dependencies_for_wander_vulnerability, "wander_vulnerability", "DamageVulnerability"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for PillBug.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_unknown_0xde7e9f94(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_floor_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stick_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_waypoint_approach_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_visible_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_wander_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_crawl_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_roll_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x519c7197(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa265383c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forward_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x558c0692(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0f991bf1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x385a1bed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcf4ea141(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xde7e9f94: ('unknown_0xde7e9f94', _decode_unknown_0xde7e9f94),
    0x8e4f7b29: ('floor_turn_speed', _decode_floor_turn_speed),
    0x5a3a30f4: ('stick_radius', _decode_stick_radius),
    0x733bd27c: ('waypoint_approach_distance', _decode_waypoint_approach_distance),
    0xa72530e8: ('visible_distance', _decode_visible_distance),
    0x5d84ed71: ('damage_vulnerability', _decode_damage_vulnerability),
    0xf382dff7: ('wander_vulnerability', _decode_wander_vulnerability),
    0xad98e16d: ('crawl_radius', _decode_crawl_radius),
    0x81d699b0: ('roll_radius', _decode_roll_radius),
    0x519c7197: ('unknown_0x519c7197', _decode_unknown_0x519c7197),
    0xa265383c: ('unknown_0xa265383c', _decode_unknown_0xa265383c),
    0xad08e189: ('forward_priority', _decode_forward_priority),
    0x558c0692: ('unknown_0x558c0692', _decode_unknown_0x558c0692),
    0xf991bf1: ('unknown_0x0f991bf1', _decode_unknown_0x0f991bf1),
    0x385a1bed: ('unknown_0x385a1bed', _decode_unknown_0x385a1bed),
    0xcf4ea141: ('unknown_0xcf4ea141', _decode_unknown_0xcf4ea141),
}
