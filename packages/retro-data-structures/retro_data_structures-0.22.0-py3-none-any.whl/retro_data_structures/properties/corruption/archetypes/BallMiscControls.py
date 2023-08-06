# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.RevolutionControl import RevolutionControl
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class BallMiscControls(BaseProperty):
    bomb: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    hyper_ball: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    morph_into_ball: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    morph_out_of_ball: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    horiz_aim_control: Spline = dataclasses.field(default_factory=Spline)
    vert_aim_control: Spline = dataclasses.field(default_factory=Spline)

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\xd29\xfb\x95')  # 0xd239fb95
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.bomb.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'^\x96\xf5/')  # 0x5e96f52f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hyper_ball.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'X\x80\xbab')  # 0x5880ba62
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.morph_into_ball.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa1O\x91\xf1')  # 0xa14f91f1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.morph_out_of_ball.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'N\x19OU')  # 0x4e194f55
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.horiz_aim_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x18q$\xaf')  # 0x187124af
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vert_aim_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            bomb=RevolutionControl.from_json(data['bomb']),
            hyper_ball=RevolutionControl.from_json(data['hyper_ball']),
            morph_into_ball=RevolutionControl.from_json(data['morph_into_ball']),
            morph_out_of_ball=RevolutionControl.from_json(data['morph_out_of_ball']),
            horiz_aim_control=Spline.from_json(data['horiz_aim_control']),
            vert_aim_control=Spline.from_json(data['vert_aim_control']),
        )

    def to_json(self) -> dict:
        return {
            'bomb': self.bomb.to_json(),
            'hyper_ball': self.hyper_ball.to_json(),
            'morph_into_ball': self.morph_into_ball.to_json(),
            'morph_out_of_ball': self.morph_out_of_ball.to_json(),
            'horiz_aim_control': self.horiz_aim_control.to_json(),
            'vert_aim_control': self.vert_aim_control.to_json(),
        }


def _decode_bomb(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_hyper_ball(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_morph_into_ball(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_morph_out_of_ball(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_horiz_aim_control(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_vert_aim_control(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd239fb95: ('bomb', _decode_bomb),
    0x5e96f52f: ('hyper_ball', _decode_hyper_ball),
    0x5880ba62: ('morph_into_ball', _decode_morph_into_ball),
    0xa14f91f1: ('morph_out_of_ball', _decode_morph_out_of_ball),
    0x4e194f55: ('horiz_aim_control', _decode_horiz_aim_control),
    0x187124af: ('vert_aim_control', _decode_vert_aim_control),
}
