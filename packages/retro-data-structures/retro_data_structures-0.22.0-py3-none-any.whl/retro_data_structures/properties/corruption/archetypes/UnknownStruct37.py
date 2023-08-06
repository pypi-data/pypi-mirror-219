# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct37(BaseProperty):
    speed: float = dataclasses.field(default=10.0)
    track_time: float = dataclasses.field(default=1.0)
    track_disable_distance: float = dataclasses.field(default=10.0)
    unknown: float = dataclasses.field(default=0.5)
    contact_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    slam_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    throw_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    launch_ball_speed: float = dataclasses.field(default=20.0)
    contact_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    cable_segment_effect: AssetId = dataclasses.field(metadata={'asset_types': ['SWHC']}, default=default_asset_id)
    claw_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    caud: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    latch_morphball_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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
        data.write(b'\x00\r')  # 13 properties

        data.write(b'c\x92@N')  # 0x6392404e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.speed))

        data.write(b'\xc4H\x95\x06')  # 0xc4489506
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.track_time))

        data.write(b'1\xcav\xc8')  # 0x31ca76c8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.track_disable_distance))

        data.write(b'\x96<\x17)')  # 0x963c1729
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'\xd7VAn')  # 0xd756416e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.contact_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'H\x01\x03\xf3')  # 0x480103f3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.slam_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd8\x0b\x1f4')  # 0xd80b1f34
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.throw_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'S$\xcb\xfb')  # 0x5324cbfb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.launch_ball_speed))

        data.write(b'O8|I')  # 0x4f387c49
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.contact_effect))

        data.write(b'\xff\xe8;w')  # 0xffe83b77
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cable_segment_effect))

        data.write(b'=1=\xa6')  # 0x3d313da6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.claw_model))

        data.write(b'\\[\xceS')  # 0x5c5bce53
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud))

        data.write(b'\xb9|\x14g')  # 0xb97c1467
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.latch_morphball_sound))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            speed=data['speed'],
            track_time=data['track_time'],
            track_disable_distance=data['track_disable_distance'],
            unknown=data['unknown'],
            contact_damage=DamageInfo.from_json(data['contact_damage']),
            slam_damage=DamageInfo.from_json(data['slam_damage']),
            throw_damage=DamageInfo.from_json(data['throw_damage']),
            launch_ball_speed=data['launch_ball_speed'],
            contact_effect=data['contact_effect'],
            cable_segment_effect=data['cable_segment_effect'],
            claw_model=data['claw_model'],
            caud=data['caud'],
            latch_morphball_sound=data['latch_morphball_sound'],
        )

    def to_json(self) -> dict:
        return {
            'speed': self.speed,
            'track_time': self.track_time,
            'track_disable_distance': self.track_disable_distance,
            'unknown': self.unknown,
            'contact_damage': self.contact_damage.to_json(),
            'slam_damage': self.slam_damage.to_json(),
            'throw_damage': self.throw_damage.to_json(),
            'launch_ball_speed': self.launch_ball_speed,
            'contact_effect': self.contact_effect,
            'cable_segment_effect': self.cable_segment_effect,
            'claw_model': self.claw_model,
            'caud': self.caud,
            'latch_morphball_sound': self.latch_morphball_sound,
        }


def _decode_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_track_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_track_disable_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_contact_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_slam_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_throw_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_launch_ball_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_contact_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cable_segment_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_claw_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_latch_morphball_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6392404e: ('speed', _decode_speed),
    0xc4489506: ('track_time', _decode_track_time),
    0x31ca76c8: ('track_disable_distance', _decode_track_disable_distance),
    0x963c1729: ('unknown', _decode_unknown),
    0xd756416e: ('contact_damage', _decode_contact_damage),
    0x480103f3: ('slam_damage', _decode_slam_damage),
    0xd80b1f34: ('throw_damage', _decode_throw_damage),
    0x5324cbfb: ('launch_ball_speed', _decode_launch_ball_speed),
    0x4f387c49: ('contact_effect', _decode_contact_effect),
    0xffe83b77: ('cable_segment_effect', _decode_cable_segment_effect),
    0x3d313da6: ('claw_model', _decode_claw_model),
    0x5c5bce53: ('caud', _decode_caud),
    0xb97c1467: ('latch_morphball_sound', _decode_latch_morphball_sound),
}
