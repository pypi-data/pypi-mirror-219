# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class FollowSurfaceBehaviorData(BaseProperty):
    snap_lerp_value: float = dataclasses.field(default=0.10000000149011612)
    start_turn_distance: float = dataclasses.field(default=0.0)
    use_terrain_neighbor_influences: bool = dataclasses.field(default=False)
    detached_by_ground_pound: bool = dataclasses.field(default=False)
    change_contact_rules_when_tilted: bool = dataclasses.field(default=False)
    tilt_threshold: float = dataclasses.field(default=0.800000011920929)
    contact_rules: AssetId = dataclasses.field(metadata={'asset_types': ['RULE']}, default=default_asset_id)
    override_collision_radius: bool = dataclasses.field(default=False)
    alignment_radius: float = dataclasses.field(default=1.0)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\x9a\x83\xf4r')  # 0x9a83f472
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.snap_lerp_value))

        data.write(b'\xf5r%k')  # 0xf572256b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.start_turn_distance))

        data.write(b'\xa8c\xba\xe2')  # 0xa863bae2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_terrain_neighbor_influences))

        data.write(b'W\xe4\r\xc7')  # 0x57e40dc7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.detached_by_ground_pound))

        data.write(b'\x10/\x9f\x94')  # 0x102f9f94
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.change_contact_rules_when_tilted))

        data.write(b'\xa7-\xfc^')  # 0xa72dfc5e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.tilt_threshold))

        data.write(b'\x01\x9f\xf3b')  # 0x19ff362
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.contact_rules))

        data.write(b'\t\xa866')  # 0x9a83636
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.override_collision_radius))

        data.write(b'\xf7&\x06\x9b')  # 0xf726069b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.alignment_radius))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            snap_lerp_value=data['snap_lerp_value'],
            start_turn_distance=data['start_turn_distance'],
            use_terrain_neighbor_influences=data['use_terrain_neighbor_influences'],
            detached_by_ground_pound=data['detached_by_ground_pound'],
            change_contact_rules_when_tilted=data['change_contact_rules_when_tilted'],
            tilt_threshold=data['tilt_threshold'],
            contact_rules=data['contact_rules'],
            override_collision_radius=data['override_collision_radius'],
            alignment_radius=data['alignment_radius'],
        )

    def to_json(self) -> dict:
        return {
            'snap_lerp_value': self.snap_lerp_value,
            'start_turn_distance': self.start_turn_distance,
            'use_terrain_neighbor_influences': self.use_terrain_neighbor_influences,
            'detached_by_ground_pound': self.detached_by_ground_pound,
            'change_contact_rules_when_tilted': self.change_contact_rules_when_tilted,
            'tilt_threshold': self.tilt_threshold,
            'contact_rules': self.contact_rules,
            'override_collision_radius': self.override_collision_radius,
            'alignment_radius': self.alignment_radius,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x9a83f472, 0xf572256b, 0xa863bae2, 0x57e40dc7, 0x102f9f94, 0xa72dfc5e, 0x19ff362, 0x9a83636, 0xf726069b)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[FollowSurfaceBehaviorData]:
    if property_count != 9:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLH?LH?LH?LHfLHQLH?LHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(82))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24]) != _FAST_IDS:
        data.seek(before)
        return None

    return FollowSurfaceBehaviorData(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
        dec[26],
    )


def _decode_snap_lerp_value(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_start_turn_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_use_terrain_neighbor_influences(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_detached_by_ground_pound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_change_contact_rules_when_tilted(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_tilt_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_contact_rules(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_override_collision_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_alignment_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x9a83f472: ('snap_lerp_value', _decode_snap_lerp_value),
    0xf572256b: ('start_turn_distance', _decode_start_turn_distance),
    0xa863bae2: ('use_terrain_neighbor_influences', _decode_use_terrain_neighbor_influences),
    0x57e40dc7: ('detached_by_ground_pound', _decode_detached_by_ground_pound),
    0x102f9f94: ('change_contact_rules_when_tilted', _decode_change_contact_rules_when_tilted),
    0xa72dfc5e: ('tilt_threshold', _decode_tilt_threshold),
    0x19ff362: ('contact_rules', _decode_contact_rules),
    0x9a83636: ('override_collision_radius', _decode_override_collision_radius),
    0xf726069b: ('alignment_radius', _decode_alignment_radius),
}
