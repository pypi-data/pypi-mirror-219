# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class SquawkProxyData(BaseProperty):
    auto_player_detection_far_radius: float = dataclasses.field(default=0.0)
    auto_player_detection_near_radius: float = dataclasses.field(default=0.0)

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

        data.write(b'\xcdQ\x13\xdc')  # 0xcd5113dc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.auto_player_detection_far_radius))

        data.write(b'\xc7\x06\xd7\x90')  # 0xc706d790
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.auto_player_detection_near_radius))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            auto_player_detection_far_radius=data['auto_player_detection_far_radius'],
            auto_player_detection_near_radius=data['auto_player_detection_near_radius'],
        )

    def to_json(self) -> dict:
        return {
            'auto_player_detection_far_radius': self.auto_player_detection_far_radius,
            'auto_player_detection_near_radius': self.auto_player_detection_near_radius,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xcd5113dc, 0xc706d790)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[SquawkProxyData]:
    if property_count != 2:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(20))
    if (dec[0], dec[3]) != _FAST_IDS:
        data.seek(before)
        return None

    return SquawkProxyData(
        dec[2],
        dec[5],
    )


def _decode_auto_player_detection_far_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_auto_player_detection_near_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xcd5113dc: ('auto_player_detection_far_radius', _decode_auto_player_detection_far_radius),
    0xc706d790: ('auto_player_detection_near_radius', _decode_auto_player_detection_near_radius),
}
