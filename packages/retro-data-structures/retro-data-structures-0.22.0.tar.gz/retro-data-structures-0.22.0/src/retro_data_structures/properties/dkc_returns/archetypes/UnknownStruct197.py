# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums


@dataclasses.dataclass()
class UnknownStruct197(BaseProperty):
    physics_target_type: enums.PhysicsTargetType = dataclasses.field(default=enums.PhysicsTargetType.Unknown2)
    unknown_0xef531185: float = dataclasses.field(default=0.0)
    unknown_0x0e6e350f: int = dataclasses.field(default=3294124709)  # Choice
    gravity: float = dataclasses.field(default=1.0)
    arc_height: float = dataclasses.field(default=10.0)
    flight_time: float = dataclasses.field(default=3.0)
    only_target_active: bool = dataclasses.field(default=False)

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'8\xf2\x06a')  # 0x38f20661
        data.write(b'\x00\x04')  # size
        self.physics_target_type.to_stream(data)

        data.write(b'\xefS\x11\x85')  # 0xef531185
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xef531185))

        data.write(b'\x0en5\x0f')  # 0xe6e350f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown_0x0e6e350f))

        data.write(b'/*\xe3\xe5')  # 0x2f2ae3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity))

        data.write(b'!P\xaa\x96')  # 0x2150aa96
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.arc_height))

        data.write(b'\xfb\xd9\xfb\x93')  # 0xfbd9fb93
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flight_time))

        data.write(b'\x03d\xf0\xb8')  # 0x364f0b8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.only_target_active))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            physics_target_type=enums.PhysicsTargetType.from_json(data['physics_target_type']),
            unknown_0xef531185=data['unknown_0xef531185'],
            unknown_0x0e6e350f=data['unknown_0x0e6e350f'],
            gravity=data['gravity'],
            arc_height=data['arc_height'],
            flight_time=data['flight_time'],
            only_target_active=data['only_target_active'],
        )

    def to_json(self) -> dict:
        return {
            'physics_target_type': self.physics_target_type.to_json(),
            'unknown_0xef531185': self.unknown_0xef531185,
            'unknown_0x0e6e350f': self.unknown_0x0e6e350f,
            'gravity': self.gravity,
            'arc_height': self.arc_height,
            'flight_time': self.flight_time,
            'only_target_active': self.only_target_active,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x38f20661, 0xef531185, 0xe6e350f, 0x2f2ae3e5, 0x2150aa96, 0xfbd9fb93, 0x364f0b8)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct197]:
    if property_count != 7:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHLLHfLHLLHfLHfLHfLH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(67))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct197(
        enums.PhysicsTargetType(dec[2]),
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
    )


def _decode_physics_target_type(data: typing.BinaryIO, property_size: int):
    return enums.PhysicsTargetType.from_stream(data)


def _decode_unknown_0xef531185(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0e6e350f(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_arc_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flight_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_only_target_active(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x38f20661: ('physics_target_type', _decode_physics_target_type),
    0xef531185: ('unknown_0xef531185', _decode_unknown_0xef531185),
    0xe6e350f: ('unknown_0x0e6e350f', _decode_unknown_0x0e6e350f),
    0x2f2ae3e5: ('gravity', _decode_gravity),
    0x2150aa96: ('arc_height', _decode_arc_height),
    0xfbd9fb93: ('flight_time', _decode_flight_time),
    0x364f0b8: ('only_target_active', _decode_only_target_active),
}
