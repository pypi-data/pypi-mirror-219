# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums


@dataclasses.dataclass()
class TrackPlayer(BaseProperty):
    target_scale_of_bounding_box_height: float = dataclasses.field(default=0.0)
    maximum_track_distance_x: float = dataclasses.field(default=15.0)
    full_left_distance: float = dataclasses.field(default=10.0)
    full_right_distance: float = dataclasses.field(default=5.0)
    maximum_track_distance_z: float = dataclasses.field(default=15.0)
    full_up_distance: float = dataclasses.field(default=10.0)
    full_down_distance: float = dataclasses.field(default=1.0)
    position_offset_z: float = dataclasses.field(default=0.0)
    axis_relationship: enums.AxisRelationship = dataclasses.field(default=enums.AxisRelationship.Unknown1)
    tracking_speed_x: float = dataclasses.field(default=6.0)
    tracking_speed_z: float = dataclasses.field(default=6.0)
    position_from_locator: bool = dataclasses.field(default=False)
    orient_from_locator: bool = dataclasses.field(default=False)
    locator_name: str = dataclasses.field(default='')
    override_locator_direction: bool = dataclasses.field(default=False)
    locator_forward: enums.UnknownEnum2 = dataclasses.field(default=enums.UnknownEnum2.Unknown2)
    locator_up: enums.UnknownEnum2 = dataclasses.field(default=enums.UnknownEnum2.Unknown3)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\x11')  # 17 properties

        data.write(b'\xb2\x97\xf1\x86')  # 0xb297f186
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.target_scale_of_bounding_box_height))

        data.write(b'\xca>\x85\xc5')  # 0xca3e85c5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_track_distance_x))

        data.write(b'\x03m\xc8\xdd')  # 0x36dc8dd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.full_left_distance))

        data.write(b'7\xa1#6')  # 0x37a12336
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.full_right_distance))

        data.write(b'\x87\xf6$\xce')  # 0x87f624ce
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_track_distance_z))

        data.write(b'\xc4jV+')  # 0xc46a562b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.full_up_distance))

        data.write(b'X\xd2\x9f?')  # 0x58d29f3f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.full_down_distance))

        data.write(b'\xe0\x02\x9eJ')  # 0xe0029e4a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.position_offset_z))

        data.write(b'i\xfcAw')  # 0x69fc4177
        data.write(b'\x00\x04')  # size
        self.axis_relationship.to_stream(data)

        data.write(b'\xa5ti\xd3')  # 0xa57469d3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.tracking_speed_x))

        data.write(b'\xe8\xbc\xc8\xd8')  # 0xe8bcc8d8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.tracking_speed_z))

        data.write(b'^0\x0b?')  # 0x5e300b3f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.position_from_locator))

        data.write(b'cVK\xa2')  # 0x63564ba2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.orient_from_locator))

        data.write(b'\xfb\xc6\xc1\x10')  # 0xfbc6c110
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.locator_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'0\xc3\x03h')  # 0x30c30368
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.override_locator_direction))

        data.write(b'<8b\xf3')  # 0x3c3862f3
        data.write(b'\x00\x04')  # size
        self.locator_forward.to_stream(data)

        data.write(b'/q\x14)')  # 0x2f711429
        data.write(b'\x00\x04')  # size
        self.locator_up.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            target_scale_of_bounding_box_height=data['target_scale_of_bounding_box_height'],
            maximum_track_distance_x=data['maximum_track_distance_x'],
            full_left_distance=data['full_left_distance'],
            full_right_distance=data['full_right_distance'],
            maximum_track_distance_z=data['maximum_track_distance_z'],
            full_up_distance=data['full_up_distance'],
            full_down_distance=data['full_down_distance'],
            position_offset_z=data['position_offset_z'],
            axis_relationship=enums.AxisRelationship.from_json(data['axis_relationship']),
            tracking_speed_x=data['tracking_speed_x'],
            tracking_speed_z=data['tracking_speed_z'],
            position_from_locator=data['position_from_locator'],
            orient_from_locator=data['orient_from_locator'],
            locator_name=data['locator_name'],
            override_locator_direction=data['override_locator_direction'],
            locator_forward=enums.UnknownEnum2.from_json(data['locator_forward']),
            locator_up=enums.UnknownEnum2.from_json(data['locator_up']),
        )

    def to_json(self) -> dict:
        return {
            'target_scale_of_bounding_box_height': self.target_scale_of_bounding_box_height,
            'maximum_track_distance_x': self.maximum_track_distance_x,
            'full_left_distance': self.full_left_distance,
            'full_right_distance': self.full_right_distance,
            'maximum_track_distance_z': self.maximum_track_distance_z,
            'full_up_distance': self.full_up_distance,
            'full_down_distance': self.full_down_distance,
            'position_offset_z': self.position_offset_z,
            'axis_relationship': self.axis_relationship.to_json(),
            'tracking_speed_x': self.tracking_speed_x,
            'tracking_speed_z': self.tracking_speed_z,
            'position_from_locator': self.position_from_locator,
            'orient_from_locator': self.orient_from_locator,
            'locator_name': self.locator_name,
            'override_locator_direction': self.override_locator_direction,
            'locator_forward': self.locator_forward.to_json(),
            'locator_up': self.locator_up.to_json(),
        }


def _decode_target_scale_of_bounding_box_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_track_distance_x(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_full_left_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_full_right_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_track_distance_z(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_full_up_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_full_down_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_position_offset_z(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_axis_relationship(data: typing.BinaryIO, property_size: int):
    return enums.AxisRelationship.from_stream(data)


def _decode_tracking_speed_x(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_tracking_speed_z(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_position_from_locator(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_orient_from_locator(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_locator_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_override_locator_direction(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_locator_forward(data: typing.BinaryIO, property_size: int):
    return enums.UnknownEnum2.from_stream(data)


def _decode_locator_up(data: typing.BinaryIO, property_size: int):
    return enums.UnknownEnum2.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb297f186: ('target_scale_of_bounding_box_height', _decode_target_scale_of_bounding_box_height),
    0xca3e85c5: ('maximum_track_distance_x', _decode_maximum_track_distance_x),
    0x36dc8dd: ('full_left_distance', _decode_full_left_distance),
    0x37a12336: ('full_right_distance', _decode_full_right_distance),
    0x87f624ce: ('maximum_track_distance_z', _decode_maximum_track_distance_z),
    0xc46a562b: ('full_up_distance', _decode_full_up_distance),
    0x58d29f3f: ('full_down_distance', _decode_full_down_distance),
    0xe0029e4a: ('position_offset_z', _decode_position_offset_z),
    0x69fc4177: ('axis_relationship', _decode_axis_relationship),
    0xa57469d3: ('tracking_speed_x', _decode_tracking_speed_x),
    0xe8bcc8d8: ('tracking_speed_z', _decode_tracking_speed_z),
    0x5e300b3f: ('position_from_locator', _decode_position_from_locator),
    0x63564ba2: ('orient_from_locator', _decode_orient_from_locator),
    0xfbc6c110: ('locator_name', _decode_locator_name),
    0x30c30368: ('override_locator_direction', _decode_override_locator_direction),
    0x3c3862f3: ('locator_forward', _decode_locator_forward),
    0x2f711429: ('locator_up', _decode_locator_up),
}
