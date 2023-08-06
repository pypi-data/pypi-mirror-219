# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class CheckpointData(BaseProperty):
    used_for_respawn: bool = dataclasses.field(default=True)
    always_active: bool = dataclasses.field(default=False)
    priority: int = dataclasses.field(default=0)
    respawn_break_bounds: float = dataclasses.field(default=3.0)
    use_balloon: bool = dataclasses.field(default=True)

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'\x17\x8e\xabW')  # 0x178eab57
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.used_for_respawn))

        data.write(b'\xcc\xb3\x12\xc3')  # 0xccb312c3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.always_active))

        data.write(b'B\x08vP')  # 0x42087650
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.priority))

        data.write(b'\xfe[\xbe\xc8')  # 0xfe5bbec8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.respawn_break_bounds))

        data.write(b'a\xaa\x81\x9f')  # 0x61aa819f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_balloon))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            used_for_respawn=data['used_for_respawn'],
            always_active=data['always_active'],
            priority=data['priority'],
            respawn_break_bounds=data['respawn_break_bounds'],
            use_balloon=data['use_balloon'],
        )

    def to_json(self) -> dict:
        return {
            'used_for_respawn': self.used_for_respawn,
            'always_active': self.always_active,
            'priority': self.priority,
            'respawn_break_bounds': self.respawn_break_bounds,
            'use_balloon': self.use_balloon,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x178eab57, 0xccb312c3, 0x42087650, 0xfe5bbec8, 0x61aa819f)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[CheckpointData]:
    if property_count != 5:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LH?LHlLHfLH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(41))
    if (dec[0], dec[3], dec[6], dec[9], dec[12]) != _FAST_IDS:
        data.seek(before)
        return None

    return CheckpointData(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
    )


def _decode_used_for_respawn(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_always_active(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_respawn_break_bounds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_use_balloon(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x178eab57: ('used_for_respawn', _decode_used_for_respawn),
    0xccb312c3: ('always_active', _decode_always_active),
    0x42087650: ('priority', _decode_priority),
    0xfe5bbec8: ('respawn_break_bounds', _decode_respawn_break_bounds),
    0x61aa819f: ('use_balloon', _decode_use_balloon),
}
