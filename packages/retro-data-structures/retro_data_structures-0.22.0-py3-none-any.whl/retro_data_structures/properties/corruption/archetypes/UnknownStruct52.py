# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability


@dataclasses.dataclass()
class UnknownStruct52(BaseProperty):
    unknown_0xde7e9f94: int = dataclasses.field(default=0)
    damage_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    wander_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    crawl_radius: float = dataclasses.field(default=0.3499999940395355)
    roll_radius: float = dataclasses.field(default=0.5)
    unknown_0xa265383c: float = dataclasses.field(default=0.019999999552965164)
    forward_priority: float = dataclasses.field(default=0.30000001192092896)
    unknown_0x2f798cdd: float = dataclasses.field(default=1.5)

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'\xde~\x9f\x94')  # 0xde7e9f94
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xde7e9f94))

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

        data.write(b'\xa2e8<')  # 0xa265383c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa265383c))

        data.write(b'\xad\x08\xe1\x89')  # 0xad08e189
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forward_priority))

        data.write(b'/y\x8c\xdd')  # 0x2f798cdd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2f798cdd))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xde7e9f94=data['unknown_0xde7e9f94'],
            damage_vulnerability=DamageVulnerability.from_json(data['damage_vulnerability']),
            wander_vulnerability=DamageVulnerability.from_json(data['wander_vulnerability']),
            crawl_radius=data['crawl_radius'],
            roll_radius=data['roll_radius'],
            unknown_0xa265383c=data['unknown_0xa265383c'],
            forward_priority=data['forward_priority'],
            unknown_0x2f798cdd=data['unknown_0x2f798cdd'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xde7e9f94': self.unknown_0xde7e9f94,
            'damage_vulnerability': self.damage_vulnerability.to_json(),
            'wander_vulnerability': self.wander_vulnerability.to_json(),
            'crawl_radius': self.crawl_radius,
            'roll_radius': self.roll_radius,
            'unknown_0xa265383c': self.unknown_0xa265383c,
            'forward_priority': self.forward_priority,
            'unknown_0x2f798cdd': self.unknown_0x2f798cdd,
        }


def _decode_unknown_0xde7e9f94(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_damage_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_wander_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_crawl_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_roll_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa265383c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forward_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2f798cdd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xde7e9f94: ('unknown_0xde7e9f94', _decode_unknown_0xde7e9f94),
    0x5d84ed71: ('damage_vulnerability', _decode_damage_vulnerability),
    0xf382dff7: ('wander_vulnerability', _decode_wander_vulnerability),
    0xad98e16d: ('crawl_radius', _decode_crawl_radius),
    0x81d699b0: ('roll_radius', _decode_roll_radius),
    0xa265383c: ('unknown_0xa265383c', _decode_unknown_0xa265383c),
    0xad08e189: ('forward_priority', _decode_forward_priority),
    0x2f798cdd: ('unknown_0x2f798cdd', _decode_unknown_0x2f798cdd),
}
