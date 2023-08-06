# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.VisControl import VisControl


@dataclasses.dataclass()
class SeparateAndReformParts(BaseProperty):
    offset: float = dataclasses.field(default=0.0)
    randomness: float = dataclasses.field(default=1.0)
    apex: float = dataclasses.field(default=3.0)
    vis_control: VisControl = dataclasses.field(default_factory=VisControl)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'F-<M')  # 0x462d3c4d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.offset))

        data.write(b't\x8eC\xfb')  # 0x748e43fb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.randomness))

        data.write(b'M7(\xe3')  # 0x4d3728e3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.apex))

        data.write(b'h\x14\x98\xdd')  # 0x681498dd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vis_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            offset=data['offset'],
            randomness=data['randomness'],
            apex=data['apex'],
            vis_control=VisControl.from_json(data['vis_control']),
        )

    def to_json(self) -> dict:
        return {
            'offset': self.offset,
            'randomness': self.randomness,
            'apex': self.apex,
            'vis_control': self.vis_control.to_json(),
        }


def _decode_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_randomness(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_apex(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vis_control(data: typing.BinaryIO, property_size: int):
    return VisControl.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x462d3c4d: ('offset', _decode_offset),
    0x748e43fb: ('randomness', _decode_randomness),
    0x4d3728e3: ('apex', _decode_apex),
    0x681498dd: ('vis_control', _decode_vis_control),
}
