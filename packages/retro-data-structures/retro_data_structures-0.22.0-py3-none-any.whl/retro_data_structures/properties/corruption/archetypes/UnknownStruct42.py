# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.CircleLineMode import CircleLineMode
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.GhorStructB import GhorStructB
from retro_data_structures.properties.corruption.archetypes.GhorStructC import GhorStructC
from retro_data_structures.properties.corruption.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.corruption.archetypes.UnknownStruct38 import UnknownStruct38
from retro_data_structures.properties.corruption.archetypes.UnknownStruct39 import UnknownStruct39
from retro_data_structures.properties.corruption.archetypes.UnknownStruct40 import UnknownStruct40
from retro_data_structures.properties.corruption.archetypes.UnknownStruct41 import UnknownStruct41
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Color import Color


@dataclasses.dataclass()
class UnknownStruct42(BaseProperty):
    is_gandrayda: bool = dataclasses.field(default=False)
    unknown_struct38: UnknownStruct38 = dataclasses.field(default_factory=UnknownStruct38)
    unknown_struct39: UnknownStruct39 = dataclasses.field(default_factory=UnknownStruct39)
    circle_line_mode: CircleLineMode = dataclasses.field(default_factory=CircleLineMode)
    ghor_struct_c_0xd345f07f: GhorStructC = dataclasses.field(default_factory=GhorStructC)
    face_effect: str = dataclasses.field(default='')
    ghor_struct_c_0x391a32ae: GhorStructC = dataclasses.field(default_factory=GhorStructC)
    ghor_struct_c_0xafb9313a: GhorStructC = dataclasses.field(default_factory=GhorStructC)
    damage_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    unknown_struct40: UnknownStruct40 = dataclasses.field(default_factory=UnknownStruct40)
    ghor_struct_c_0x810ec49a: GhorStructC = dataclasses.field(default_factory=GhorStructC)
    unknown_struct41: UnknownStruct41 = dataclasses.field(default_factory=UnknownStruct41)
    ghor_struct_b_0x0e07b299: GhorStructB = dataclasses.field(default_factory=GhorStructB)
    ghor_struct_b_0x73e98b8f: GhorStructB = dataclasses.field(default_factory=GhorStructB)
    rotate_body_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    lock_on_locator: str = dataclasses.field(default='')
    energy_bar_string: str = dataclasses.field(default='')
    health_info_0x3d43820c: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    health_info_0x6ed9d988: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    health_info_0xe97f12cb: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    unknown_0xd16b54f9: float = dataclasses.field(default=10.0)
    unknown_0xb40c6fbf: float = dataclasses.field(default=20.0)
    unknown_0x2443e8ec: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x888049bd: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))

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
        data.write(b'\x00\x18')  # 24 properties

        data.write(b'S\x1a\x8c\x85')  # 0x531a8c85
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_gandrayda))

        data.write(b'\x83,D.')  # 0x832c442e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct38.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa0\xd0\x96;')  # 0xa0d0963b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct39.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x81\xcc\r"')  # 0x81cc0d22
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.circle_line_mode.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd3E\xf0\x7f')  # 0xd345f07f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ghor_struct_c_0xd345f07f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc5\x9d\x1a-')  # 0xc59d1a2d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.face_effect.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'9\x1a2\xae')  # 0x391a32ae
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ghor_struct_c_0x391a32ae.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaf\xb91:')  # 0xafb9313a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ghor_struct_c_0xafb9313a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbaJ\xd1G')  # 0xba4ad147
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'0\\\xda\xd2')  # 0x305cdad2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct40.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x81\x0e\xc4\x9a')  # 0x810ec49a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ghor_struct_c_0x810ec49a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'[w/m')  # 0x5b772f6d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct41.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0e\x07\xb2\x99')  # 0xe07b299
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ghor_struct_b_0x0e07b299.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b's\xe9\x8b\x8f')  # 0x73e98b8f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ghor_struct_b_0x73e98b8f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x15\xe3\xf2\x83')  # 0x15e3f283
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.rotate_body_sound))

        data.write(b'y\xbf\xd8\x86')  # 0x79bfd886
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.lock_on_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'3|@V')  # 0x337c4056
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.energy_bar_string.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'=C\x82\x0c')  # 0x3d43820c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.health_info_0x3d43820c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'n\xd9\xd9\x88')  # 0x6ed9d988
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.health_info_0x6ed9d988.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe9\x7f\x12\xcb')  # 0xe97f12cb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.health_info_0xe97f12cb.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd1kT\xf9')  # 0xd16b54f9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd16b54f9))

        data.write(b'\xb4\x0co\xbf')  # 0xb40c6fbf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb40c6fbf))

        data.write(b'$C\xe8\xec')  # 0x2443e8ec
        data.write(b'\x00\x10')  # size
        self.unknown_0x2443e8ec.to_stream(data)

        data.write(b'\x88\x80I\xbd')  # 0x888049bd
        data.write(b'\x00\x10')  # size
        self.unknown_0x888049bd.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            is_gandrayda=data['is_gandrayda'],
            unknown_struct38=UnknownStruct38.from_json(data['unknown_struct38']),
            unknown_struct39=UnknownStruct39.from_json(data['unknown_struct39']),
            circle_line_mode=CircleLineMode.from_json(data['circle_line_mode']),
            ghor_struct_c_0xd345f07f=GhorStructC.from_json(data['ghor_struct_c_0xd345f07f']),
            face_effect=data['face_effect'],
            ghor_struct_c_0x391a32ae=GhorStructC.from_json(data['ghor_struct_c_0x391a32ae']),
            ghor_struct_c_0xafb9313a=GhorStructC.from_json(data['ghor_struct_c_0xafb9313a']),
            damage_vulnerability=DamageVulnerability.from_json(data['damage_vulnerability']),
            unknown_struct40=UnknownStruct40.from_json(data['unknown_struct40']),
            ghor_struct_c_0x810ec49a=GhorStructC.from_json(data['ghor_struct_c_0x810ec49a']),
            unknown_struct41=UnknownStruct41.from_json(data['unknown_struct41']),
            ghor_struct_b_0x0e07b299=GhorStructB.from_json(data['ghor_struct_b_0x0e07b299']),
            ghor_struct_b_0x73e98b8f=GhorStructB.from_json(data['ghor_struct_b_0x73e98b8f']),
            rotate_body_sound=data['rotate_body_sound'],
            lock_on_locator=data['lock_on_locator'],
            energy_bar_string=data['energy_bar_string'],
            health_info_0x3d43820c=HealthInfo.from_json(data['health_info_0x3d43820c']),
            health_info_0x6ed9d988=HealthInfo.from_json(data['health_info_0x6ed9d988']),
            health_info_0xe97f12cb=HealthInfo.from_json(data['health_info_0xe97f12cb']),
            unknown_0xd16b54f9=data['unknown_0xd16b54f9'],
            unknown_0xb40c6fbf=data['unknown_0xb40c6fbf'],
            unknown_0x2443e8ec=Color.from_json(data['unknown_0x2443e8ec']),
            unknown_0x888049bd=Color.from_json(data['unknown_0x888049bd']),
        )

    def to_json(self) -> dict:
        return {
            'is_gandrayda': self.is_gandrayda,
            'unknown_struct38': self.unknown_struct38.to_json(),
            'unknown_struct39': self.unknown_struct39.to_json(),
            'circle_line_mode': self.circle_line_mode.to_json(),
            'ghor_struct_c_0xd345f07f': self.ghor_struct_c_0xd345f07f.to_json(),
            'face_effect': self.face_effect,
            'ghor_struct_c_0x391a32ae': self.ghor_struct_c_0x391a32ae.to_json(),
            'ghor_struct_c_0xafb9313a': self.ghor_struct_c_0xafb9313a.to_json(),
            'damage_vulnerability': self.damage_vulnerability.to_json(),
            'unknown_struct40': self.unknown_struct40.to_json(),
            'ghor_struct_c_0x810ec49a': self.ghor_struct_c_0x810ec49a.to_json(),
            'unknown_struct41': self.unknown_struct41.to_json(),
            'ghor_struct_b_0x0e07b299': self.ghor_struct_b_0x0e07b299.to_json(),
            'ghor_struct_b_0x73e98b8f': self.ghor_struct_b_0x73e98b8f.to_json(),
            'rotate_body_sound': self.rotate_body_sound,
            'lock_on_locator': self.lock_on_locator,
            'energy_bar_string': self.energy_bar_string,
            'health_info_0x3d43820c': self.health_info_0x3d43820c.to_json(),
            'health_info_0x6ed9d988': self.health_info_0x6ed9d988.to_json(),
            'health_info_0xe97f12cb': self.health_info_0xe97f12cb.to_json(),
            'unknown_0xd16b54f9': self.unknown_0xd16b54f9,
            'unknown_0xb40c6fbf': self.unknown_0xb40c6fbf,
            'unknown_0x2443e8ec': self.unknown_0x2443e8ec.to_json(),
            'unknown_0x888049bd': self.unknown_0x888049bd.to_json(),
        }


def _decode_is_gandrayda(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_struct38(data: typing.BinaryIO, property_size: int):
    return UnknownStruct38.from_stream(data, property_size)


def _decode_unknown_struct39(data: typing.BinaryIO, property_size: int):
    return UnknownStruct39.from_stream(data, property_size)


def _decode_circle_line_mode(data: typing.BinaryIO, property_size: int):
    return CircleLineMode.from_stream(data, property_size)


def _decode_ghor_struct_c_0xd345f07f(data: typing.BinaryIO, property_size: int):
    return GhorStructC.from_stream(data, property_size)


def _decode_face_effect(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_ghor_struct_c_0x391a32ae(data: typing.BinaryIO, property_size: int):
    return GhorStructC.from_stream(data, property_size)


def _decode_ghor_struct_c_0xafb9313a(data: typing.BinaryIO, property_size: int):
    return GhorStructC.from_stream(data, property_size)


def _decode_damage_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_unknown_struct40(data: typing.BinaryIO, property_size: int):
    return UnknownStruct40.from_stream(data, property_size)


def _decode_ghor_struct_c_0x810ec49a(data: typing.BinaryIO, property_size: int):
    return GhorStructC.from_stream(data, property_size)


def _decode_unknown_struct41(data: typing.BinaryIO, property_size: int):
    return UnknownStruct41.from_stream(data, property_size)


def _decode_ghor_struct_b_0x0e07b299(data: typing.BinaryIO, property_size: int):
    return GhorStructB.from_stream(data, property_size)


def _decode_ghor_struct_b_0x73e98b8f(data: typing.BinaryIO, property_size: int):
    return GhorStructB.from_stream(data, property_size)


def _decode_rotate_body_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_lock_on_locator(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_energy_bar_string(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_health_info_0x3d43820c(data: typing.BinaryIO, property_size: int):
    return HealthInfo.from_stream(data, property_size)


def _decode_health_info_0x6ed9d988(data: typing.BinaryIO, property_size: int):
    return HealthInfo.from_stream(data, property_size)


def _decode_health_info_0xe97f12cb(data: typing.BinaryIO, property_size: int):
    return HealthInfo.from_stream(data, property_size)


def _decode_unknown_0xd16b54f9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb40c6fbf(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2443e8ec(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x888049bd(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x531a8c85: ('is_gandrayda', _decode_is_gandrayda),
    0x832c442e: ('unknown_struct38', _decode_unknown_struct38),
    0xa0d0963b: ('unknown_struct39', _decode_unknown_struct39),
    0x81cc0d22: ('circle_line_mode', _decode_circle_line_mode),
    0xd345f07f: ('ghor_struct_c_0xd345f07f', _decode_ghor_struct_c_0xd345f07f),
    0xc59d1a2d: ('face_effect', _decode_face_effect),
    0x391a32ae: ('ghor_struct_c_0x391a32ae', _decode_ghor_struct_c_0x391a32ae),
    0xafb9313a: ('ghor_struct_c_0xafb9313a', _decode_ghor_struct_c_0xafb9313a),
    0xba4ad147: ('damage_vulnerability', _decode_damage_vulnerability),
    0x305cdad2: ('unknown_struct40', _decode_unknown_struct40),
    0x810ec49a: ('ghor_struct_c_0x810ec49a', _decode_ghor_struct_c_0x810ec49a),
    0x5b772f6d: ('unknown_struct41', _decode_unknown_struct41),
    0xe07b299: ('ghor_struct_b_0x0e07b299', _decode_ghor_struct_b_0x0e07b299),
    0x73e98b8f: ('ghor_struct_b_0x73e98b8f', _decode_ghor_struct_b_0x73e98b8f),
    0x15e3f283: ('rotate_body_sound', _decode_rotate_body_sound),
    0x79bfd886: ('lock_on_locator', _decode_lock_on_locator),
    0x337c4056: ('energy_bar_string', _decode_energy_bar_string),
    0x3d43820c: ('health_info_0x3d43820c', _decode_health_info_0x3d43820c),
    0x6ed9d988: ('health_info_0x6ed9d988', _decode_health_info_0x6ed9d988),
    0xe97f12cb: ('health_info_0xe97f12cb', _decode_health_info_0xe97f12cb),
    0xd16b54f9: ('unknown_0xd16b54f9', _decode_unknown_0xd16b54f9),
    0xb40c6fbf: ('unknown_0xb40c6fbf', _decode_unknown_0xb40c6fbf),
    0x2443e8ec: ('unknown_0x2443e8ec', _decode_unknown_0x2443e8ec),
    0x888049bd: ('unknown_0x888049bd', _decode_unknown_0x888049bd),
}
