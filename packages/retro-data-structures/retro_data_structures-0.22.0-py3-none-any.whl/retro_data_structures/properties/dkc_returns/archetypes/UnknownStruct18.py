# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct18(BaseProperty):
    slave_platform_motion_knots: bool = dataclasses.field(default=False)
    slave_position_in_local_space: bool = dataclasses.field(default=True)

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b':h\xee\\')  # 0x3a68ee5c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.slave_platform_motion_knots))

        data.write(b'D\xb31\xec')  # 0x44b331ec
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.slave_position_in_local_space))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            slave_platform_motion_knots=data['slave_platform_motion_knots'],
            slave_position_in_local_space=data['slave_position_in_local_space'],
        )

    def to_json(self) -> dict:
        return {
            'slave_platform_motion_knots': self.slave_platform_motion_knots,
            'slave_position_in_local_space': self.slave_position_in_local_space,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x3a68ee5c, 0x44b331ec)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct18]:
    if property_count != 2:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(14))
    if (dec[0], dec[3]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct18(
        dec[2],
        dec[5],
    )


def _decode_slave_platform_motion_knots(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_slave_position_in_local_space(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x3a68ee5c: ('slave_platform_motion_knots', _decode_slave_platform_motion_knots),
    0x44b331ec: ('slave_position_in_local_space', _decode_slave_position_in_local_space),
}
