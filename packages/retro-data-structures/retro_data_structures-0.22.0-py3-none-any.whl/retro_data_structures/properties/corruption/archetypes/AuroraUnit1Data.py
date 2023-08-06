# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.ModIncaData import ModIncaData
from retro_data_structures.properties.corruption.archetypes.UnknownStruct2 import UnknownStruct2
from retro_data_structures.properties.corruption.archetypes.UnknownStruct3 import UnknownStruct3
from retro_data_structures.properties.corruption.archetypes.UnknownStruct4 import UnknownStruct4
from retro_data_structures.properties.corruption.archetypes.UnknownStruct6 import UnknownStruct6
from retro_data_structures.properties.corruption.archetypes.UnknownStruct8 import UnknownStruct8
from retro_data_structures.properties.corruption.archetypes.UnknownStruct9 import UnknownStruct9
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class AuroraUnit1Data(BaseProperty):
    unknown_0x4a1e8961: float = dataclasses.field(default=45.0)
    max_turn_angle: float = dataclasses.field(default=120.0)
    left_brain_door: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    right_brain_door: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    brain_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    max_brain_damage: float = dataclasses.field(default=700.0)
    unknown_0xa33bd3df: float = dataclasses.field(default=10.0)
    unknown_struct2: UnknownStruct2 = dataclasses.field(default_factory=UnknownStruct2)
    unknown_struct3: UnknownStruct3 = dataclasses.field(default_factory=UnknownStruct3)
    unknown_struct4: UnknownStruct4 = dataclasses.field(default_factory=UnknownStruct4)
    unknown_struct8: UnknownStruct8 = dataclasses.field(default_factory=UnknownStruct8)
    unknown_struct9: UnknownStruct9 = dataclasses.field(default_factory=UnknownStruct9)
    unknown_struct6_0x7cc2a36e: UnknownStruct6 = dataclasses.field(default_factory=UnknownStruct6)
    unknown_struct6_0x12d3165c: UnknownStruct6 = dataclasses.field(default_factory=UnknownStruct6)
    initial_attack_time: float = dataclasses.field(default=2.0)
    unknown_0x2caec304: float = dataclasses.field(default=0.0)
    unknown_0x2c68fedf: float = dataclasses.field(default=1.0)
    unknown_0x1a79e5d6: float = dataclasses.field(default=0.5)
    mod_inca_data: ModIncaData = dataclasses.field(default_factory=ModIncaData)

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
        data.write(b'\x00\x13')  # 19 properties

        data.write(b'J\x1e\x89a')  # 0x4a1e8961
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4a1e8961))

        data.write(b"P\xe4e'")  # 0x50e46527
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_turn_angle))

        data.write(b'\x078B\xe7')  # 0x73842e7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.left_brain_door))

        data.write(b'\xdd\xd7*\xad')  # 0xddd72aad
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.right_brain_door))

        data.write(b'$:\xb1\r')  # 0x243ab10d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.brain_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'{L\x8a\x7f')  # 0x7b4c8a7f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_brain_damage))

        data.write(b'\xa3;\xd3\xdf')  # 0xa33bd3df
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa33bd3df))

        data.write(b'[QN\x8c')  # 0x5b514e8c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x82\x8c"8')  # 0x828c2238
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x97\xd1j\xa1')  # 0x97d16aa1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfa\xed\x98\xdb')  # 0xfaed98db
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9a\x9e\xb7\x86')  # 0x9a9eb786
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'|\xc2\xa3n')  # 0x7cc2a36e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct6_0x7cc2a36e.to_stream(data, default_override={'gravity_buster_chance': 40.0, 'combat_hatches_chance': 40.0, 'dark_samus_echoes_chance': 20.0, 'turret_chance': 0.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x12\xd3\x16\\')  # 0x12d3165c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct6_0x12d3165c.to_stream(data, default_override={'gravity_buster_chance': 20.0, 'combat_hatches_chance': 20.0, 'dark_samus_echoes_chance': 20.0, 'turret_chance': 40.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Dn\xfc\xad')  # 0x446efcad
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_attack_time))

        data.write(b',\xae\xc3\x04')  # 0x2caec304
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2caec304))

        data.write(b',h\xfe\xdf')  # 0x2c68fedf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2c68fedf))

        data.write(b'\x1ay\xe5\xd6')  # 0x1a79e5d6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1a79e5d6))

        data.write(b'\xb4\xc0(T')  # 0xb4c02854
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mod_inca_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x4a1e8961=data['unknown_0x4a1e8961'],
            max_turn_angle=data['max_turn_angle'],
            left_brain_door=data['left_brain_door'],
            right_brain_door=data['right_brain_door'],
            brain_vulnerability=DamageVulnerability.from_json(data['brain_vulnerability']),
            max_brain_damage=data['max_brain_damage'],
            unknown_0xa33bd3df=data['unknown_0xa33bd3df'],
            unknown_struct2=UnknownStruct2.from_json(data['unknown_struct2']),
            unknown_struct3=UnknownStruct3.from_json(data['unknown_struct3']),
            unknown_struct4=UnknownStruct4.from_json(data['unknown_struct4']),
            unknown_struct8=UnknownStruct8.from_json(data['unknown_struct8']),
            unknown_struct9=UnknownStruct9.from_json(data['unknown_struct9']),
            unknown_struct6_0x7cc2a36e=UnknownStruct6.from_json(data['unknown_struct6_0x7cc2a36e']),
            unknown_struct6_0x12d3165c=UnknownStruct6.from_json(data['unknown_struct6_0x12d3165c']),
            initial_attack_time=data['initial_attack_time'],
            unknown_0x2caec304=data['unknown_0x2caec304'],
            unknown_0x2c68fedf=data['unknown_0x2c68fedf'],
            unknown_0x1a79e5d6=data['unknown_0x1a79e5d6'],
            mod_inca_data=ModIncaData.from_json(data['mod_inca_data']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x4a1e8961': self.unknown_0x4a1e8961,
            'max_turn_angle': self.max_turn_angle,
            'left_brain_door': self.left_brain_door,
            'right_brain_door': self.right_brain_door,
            'brain_vulnerability': self.brain_vulnerability.to_json(),
            'max_brain_damage': self.max_brain_damage,
            'unknown_0xa33bd3df': self.unknown_0xa33bd3df,
            'unknown_struct2': self.unknown_struct2.to_json(),
            'unknown_struct3': self.unknown_struct3.to_json(),
            'unknown_struct4': self.unknown_struct4.to_json(),
            'unknown_struct8': self.unknown_struct8.to_json(),
            'unknown_struct9': self.unknown_struct9.to_json(),
            'unknown_struct6_0x7cc2a36e': self.unknown_struct6_0x7cc2a36e.to_json(),
            'unknown_struct6_0x12d3165c': self.unknown_struct6_0x12d3165c.to_json(),
            'initial_attack_time': self.initial_attack_time,
            'unknown_0x2caec304': self.unknown_0x2caec304,
            'unknown_0x2c68fedf': self.unknown_0x2c68fedf,
            'unknown_0x1a79e5d6': self.unknown_0x1a79e5d6,
            'mod_inca_data': self.mod_inca_data.to_json(),
        }


def _decode_unknown_0x4a1e8961(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_turn_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_left_brain_door(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_right_brain_door(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_brain_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_max_brain_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa33bd3df(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct2(data: typing.BinaryIO, property_size: int):
    return UnknownStruct2.from_stream(data, property_size)


def _decode_unknown_struct3(data: typing.BinaryIO, property_size: int):
    return UnknownStruct3.from_stream(data, property_size)


def _decode_unknown_struct4(data: typing.BinaryIO, property_size: int):
    return UnknownStruct4.from_stream(data, property_size)


def _decode_unknown_struct8(data: typing.BinaryIO, property_size: int):
    return UnknownStruct8.from_stream(data, property_size)


def _decode_unknown_struct9(data: typing.BinaryIO, property_size: int):
    return UnknownStruct9.from_stream(data, property_size)


def _decode_unknown_struct6_0x7cc2a36e(data: typing.BinaryIO, property_size: int):
    return UnknownStruct6.from_stream(data, property_size, default_override={'gravity_buster_chance': 40.0, 'combat_hatches_chance': 40.0, 'dark_samus_echoes_chance': 20.0, 'turret_chance': 0.0})


def _decode_unknown_struct6_0x12d3165c(data: typing.BinaryIO, property_size: int):
    return UnknownStruct6.from_stream(data, property_size, default_override={'gravity_buster_chance': 20.0, 'combat_hatches_chance': 20.0, 'dark_samus_echoes_chance': 20.0, 'turret_chance': 40.0})


def _decode_initial_attack_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2caec304(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2c68fedf(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1a79e5d6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_mod_inca_data(data: typing.BinaryIO, property_size: int):
    return ModIncaData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4a1e8961: ('unknown_0x4a1e8961', _decode_unknown_0x4a1e8961),
    0x50e46527: ('max_turn_angle', _decode_max_turn_angle),
    0x73842e7: ('left_brain_door', _decode_left_brain_door),
    0xddd72aad: ('right_brain_door', _decode_right_brain_door),
    0x243ab10d: ('brain_vulnerability', _decode_brain_vulnerability),
    0x7b4c8a7f: ('max_brain_damage', _decode_max_brain_damage),
    0xa33bd3df: ('unknown_0xa33bd3df', _decode_unknown_0xa33bd3df),
    0x5b514e8c: ('unknown_struct2', _decode_unknown_struct2),
    0x828c2238: ('unknown_struct3', _decode_unknown_struct3),
    0x97d16aa1: ('unknown_struct4', _decode_unknown_struct4),
    0xfaed98db: ('unknown_struct8', _decode_unknown_struct8),
    0x9a9eb786: ('unknown_struct9', _decode_unknown_struct9),
    0x7cc2a36e: ('unknown_struct6_0x7cc2a36e', _decode_unknown_struct6_0x7cc2a36e),
    0x12d3165c: ('unknown_struct6_0x12d3165c', _decode_unknown_struct6_0x12d3165c),
    0x446efcad: ('initial_attack_time', _decode_initial_attack_time),
    0x2caec304: ('unknown_0x2caec304', _decode_unknown_0x2caec304),
    0x2c68fedf: ('unknown_0x2c68fedf', _decode_unknown_0x2c68fedf),
    0x1a79e5d6: ('unknown_0x1a79e5d6', _decode_unknown_0x1a79e5d6),
    0xb4c02854: ('mod_inca_data', _decode_mod_inca_data),
}
