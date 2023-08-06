# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct43(BaseProperty):
    unknown_0xde7e9f94: int = dataclasses.field(default=0)
    crawl_radius: float = dataclasses.field(default=0.3499999940395355)
    roll_radius: float = dataclasses.field(default=0.5)
    unknown_0xa265383c: float = dataclasses.field(default=0.019999999552965164)
    forward_priority: float = dataclasses.field(default=0.30000001192092896)
    unknown_0xe776332a: float = dataclasses.field(default=3.0)
    scan_delay_max: float = dataclasses.field(default=20.0)
    explode_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    explode_sound: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    explode_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    visor_goo_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)

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
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'\xde~\x9f\x94')  # 0xde7e9f94
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xde7e9f94))

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

        data.write(b'\xe7v3*')  # 0xe776332a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe776332a))

        data.write(b'\x01\x16\x9c\xcb')  # 0x1169ccb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scan_delay_max))

        data.write(b'\x1a\x9cLL')  # 0x1a9c4c4c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.explode_effect))

        data.write(b'\t\x856\xdd')  # 0x98536dd
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.explode_sound))

        data.write(b'\xf6 j\x12')  # 0xf6206a12
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.explode_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa23\xac\xcd')  # 0xa233accd
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.visor_goo_effect))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xde7e9f94=data['unknown_0xde7e9f94'],
            crawl_radius=data['crawl_radius'],
            roll_radius=data['roll_radius'],
            unknown_0xa265383c=data['unknown_0xa265383c'],
            forward_priority=data['forward_priority'],
            unknown_0xe776332a=data['unknown_0xe776332a'],
            scan_delay_max=data['scan_delay_max'],
            explode_effect=data['explode_effect'],
            explode_sound=data['explode_sound'],
            explode_damage=DamageInfo.from_json(data['explode_damage']),
            visor_goo_effect=data['visor_goo_effect'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xde7e9f94': self.unknown_0xde7e9f94,
            'crawl_radius': self.crawl_radius,
            'roll_radius': self.roll_radius,
            'unknown_0xa265383c': self.unknown_0xa265383c,
            'forward_priority': self.forward_priority,
            'unknown_0xe776332a': self.unknown_0xe776332a,
            'scan_delay_max': self.scan_delay_max,
            'explode_effect': self.explode_effect,
            'explode_sound': self.explode_sound,
            'explode_damage': self.explode_damage.to_json(),
            'visor_goo_effect': self.visor_goo_effect,
        }


def _decode_unknown_0xde7e9f94(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_crawl_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_roll_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa265383c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forward_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe776332a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scan_delay_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_explode_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_explode_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_explode_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_visor_goo_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xde7e9f94: ('unknown_0xde7e9f94', _decode_unknown_0xde7e9f94),
    0xad98e16d: ('crawl_radius', _decode_crawl_radius),
    0x81d699b0: ('roll_radius', _decode_roll_radius),
    0xa265383c: ('unknown_0xa265383c', _decode_unknown_0xa265383c),
    0xad08e189: ('forward_priority', _decode_forward_priority),
    0xe776332a: ('unknown_0xe776332a', _decode_unknown_0xe776332a),
    0x1169ccb: ('scan_delay_max', _decode_scan_delay_max),
    0x1a9c4c4c: ('explode_effect', _decode_explode_effect),
    0x98536dd: ('explode_sound', _decode_explode_sound),
    0xf6206a12: ('explode_damage', _decode_explode_damage),
    0xa233accd: ('visor_goo_effect', _decode_visor_goo_effect),
}
