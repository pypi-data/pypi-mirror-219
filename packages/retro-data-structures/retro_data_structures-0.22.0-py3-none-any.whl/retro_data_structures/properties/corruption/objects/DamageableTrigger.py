# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.corruption.archetypes.VisorParameters import VisorParameters


@dataclasses.dataclass()
class DamageableTrigger(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    health: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    orbitable: bool = dataclasses.field(default=False)
    enable_seeker_lock_on: bool = dataclasses.field(default=False)
    invulnerable: bool = dataclasses.field(default=False)
    show_on_radar: bool = dataclasses.field(default=False)
    visor: VisorParameters = dataclasses.field(default_factory=VisorParameters)
    damage_originator: enums.DamageableTriggerEnum = dataclasses.field(default=enums.DamageableTriggerEnum.Unknown1)
    only_take_damage_from_inhabitants: bool = dataclasses.field(default=False)
    is_hostile: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'DTRG'

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

        data.write(b'\xcf\x90\xd1^')  # 0xcf90d15e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.health.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'{q\xae\x90')  # 0x7b71ae90
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'pKSi')  # 0x704b5369
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.orbitable))

        data.write(b']\xfdx ')  # 0x5dfd7820
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enable_seeker_lock_on))

        data.write(b'fR\xbd\xd7')  # 0x6652bdd7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.invulnerable))

        data.write(b'\xf0\xe0zK')  # 0xf0e07a4b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.show_on_radar))

        data.write(b'\x05\xad%\x0e')  # 0x5ad250e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.visor.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8b\x9d!#')  # 0x8b9d2123
        data.write(b'\x00\x04')  # size
        self.damage_originator.to_stream(data)

        data.write(b'\xce,\xf5\x10')  # 0xce2cf510
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.only_take_damage_from_inhabitants))

        data.write(b'p\x1ba\xb3')  # 0x701b61b3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_hostile))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            health=HealthInfo.from_json(data['health']),
            vulnerability=DamageVulnerability.from_json(data['vulnerability']),
            orbitable=data['orbitable'],
            enable_seeker_lock_on=data['enable_seeker_lock_on'],
            invulnerable=data['invulnerable'],
            show_on_radar=data['show_on_radar'],
            visor=VisorParameters.from_json(data['visor']),
            damage_originator=enums.DamageableTriggerEnum.from_json(data['damage_originator']),
            only_take_damage_from_inhabitants=data['only_take_damage_from_inhabitants'],
            is_hostile=data['is_hostile'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'health': self.health.to_json(),
            'vulnerability': self.vulnerability.to_json(),
            'orbitable': self.orbitable,
            'enable_seeker_lock_on': self.enable_seeker_lock_on,
            'invulnerable': self.invulnerable,
            'show_on_radar': self.show_on_radar,
            'visor': self.visor.to_json(),
            'damage_originator': self.damage_originator.to_json(),
            'only_take_damage_from_inhabitants': self.only_take_damage_from_inhabitants,
            'is_hostile': self.is_hostile,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_health(data: typing.BinaryIO, property_size: int):
    return HealthInfo.from_stream(data, property_size)


def _decode_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_orbitable(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_enable_seeker_lock_on(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_invulnerable(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_show_on_radar(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_visor(data: typing.BinaryIO, property_size: int):
    return VisorParameters.from_stream(data, property_size)


def _decode_damage_originator(data: typing.BinaryIO, property_size: int):
    return enums.DamageableTriggerEnum.from_stream(data)


def _decode_only_take_damage_from_inhabitants(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_hostile(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xcf90d15e: ('health', _decode_health),
    0x7b71ae90: ('vulnerability', _decode_vulnerability),
    0x704b5369: ('orbitable', _decode_orbitable),
    0x5dfd7820: ('enable_seeker_lock_on', _decode_enable_seeker_lock_on),
    0x6652bdd7: ('invulnerable', _decode_invulnerable),
    0xf0e07a4b: ('show_on_radar', _decode_show_on_radar),
    0x5ad250e: ('visor', _decode_visor),
    0x8b9d2123: ('damage_originator', _decode_damage_originator),
    0xce2cf510: ('only_take_damage_from_inhabitants', _decode_only_take_damage_from_inhabitants),
    0x701b61b3: ('is_hostile', _decode_is_hostile),
}
