# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class PlayerSlaveData(BaseProperty):
    disable_grab_detach_duration: float = dataclasses.field(default=1.0)
    grab_detached_disallow_time: float = dataclasses.field(default=0.30000001192092896)
    unknown_0x2c60dd92: int = dataclasses.field(default=0)
    unknown_0xc739d41a: int = dataclasses.field(default=0)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xe4\x88\xb8\x9e')  # 0xe488b89e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.disable_grab_detach_duration))

        data.write(b'\xd2-\xa5|')  # 0xd22da57c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grab_detached_disallow_time))

        data.write(b',`\xdd\x92')  # 0x2c60dd92
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x2c60dd92))

        data.write(b'\xc79\xd4\x1a')  # 0xc739d41a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xc739d41a))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            disable_grab_detach_duration=data['disable_grab_detach_duration'],
            grab_detached_disallow_time=data['grab_detached_disallow_time'],
            unknown_0x2c60dd92=data['unknown_0x2c60dd92'],
            unknown_0xc739d41a=data['unknown_0xc739d41a'],
        )

    def to_json(self) -> dict:
        return {
            'disable_grab_detach_duration': self.disable_grab_detach_duration,
            'grab_detached_disallow_time': self.grab_detached_disallow_time,
            'unknown_0x2c60dd92': self.unknown_0x2c60dd92,
            'unknown_0xc739d41a': self.unknown_0xc739d41a,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xe488b89e, 0xd22da57c, 0x2c60dd92, 0xc739d41a)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[PlayerSlaveData]:
    if property_count != 4:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHlLHl')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(40))
    if (dec[0], dec[3], dec[6], dec[9]) != _FAST_IDS:
        data.seek(before)
        return None

    return PlayerSlaveData(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_disable_grab_detach_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grab_detached_disallow_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2c60dd92(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xc739d41a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe488b89e: ('disable_grab_detach_duration', _decode_disable_grab_detach_duration),
    0xd22da57c: ('grab_detached_disallow_time', _decode_grab_detached_disallow_time),
    0x2c60dd92: ('unknown_0x2c60dd92', _decode_unknown_0x2c60dd92),
    0xc739d41a: ('unknown_0xc739d41a', _decode_unknown_0xc739d41a),
}
