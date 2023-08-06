# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.RevolutionControl import RevolutionControl
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class CameraControls(BaseProperty):
    look_up: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    look_down: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    look_left: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    look_right: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    view_lock: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    skip_cinematic: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    look_up_control: Spline = dataclasses.field(default_factory=Spline)
    look_down_control: Spline = dataclasses.field(default_factory=Spline)

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\x1c\x1doI')  # 0x1c1d6f49
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.look_up.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1a \xd5\xf4')  # 0x1a20d5f4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.look_down.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x90A^y')  # 0x90415e79
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.look_left.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'#\xc13<')  # 0x23c1333c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.look_right.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'+K\xa1\xa3')  # 0x2b4ba1a3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd4\x7f$\xd7')  # 0xd47f24d7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.view_lock.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x19\xa3\xe0}')  # 0x19a3e07d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.skip_cinematic.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa03\x90\xa5')  # 0xa03390a5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.look_up_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe7F\xf7~')  # 0xe746f77e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.look_down_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            look_up=RevolutionControl.from_json(data['look_up']),
            look_down=RevolutionControl.from_json(data['look_down']),
            look_left=RevolutionControl.from_json(data['look_left']),
            look_right=RevolutionControl.from_json(data['look_right']),
            unknown=RevolutionControl.from_json(data['unknown']),
            view_lock=RevolutionControl.from_json(data['view_lock']),
            skip_cinematic=RevolutionControl.from_json(data['skip_cinematic']),
            look_up_control=Spline.from_json(data['look_up_control']),
            look_down_control=Spline.from_json(data['look_down_control']),
        )

    def to_json(self) -> dict:
        return {
            'look_up': self.look_up.to_json(),
            'look_down': self.look_down.to_json(),
            'look_left': self.look_left.to_json(),
            'look_right': self.look_right.to_json(),
            'unknown': self.unknown.to_json(),
            'view_lock': self.view_lock.to_json(),
            'skip_cinematic': self.skip_cinematic.to_json(),
            'look_up_control': self.look_up_control.to_json(),
            'look_down_control': self.look_down_control.to_json(),
        }


def _decode_look_up(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_look_down(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_look_left(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_look_right(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_view_lock(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_skip_cinematic(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_look_up_control(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_look_down_control(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1c1d6f49: ('look_up', _decode_look_up),
    0x1a20d5f4: ('look_down', _decode_look_down),
    0x90415e79: ('look_left', _decode_look_left),
    0x23c1333c: ('look_right', _decode_look_right),
    0x2b4ba1a3: ('unknown', _decode_unknown),
    0xd47f24d7: ('view_lock', _decode_view_lock),
    0x19a3e07d: ('skip_cinematic', _decode_skip_cinematic),
    0xa03390a5: ('look_up_control', _decode_look_up_control),
    0xe746f77e: ('look_down_control', _decode_look_down_control),
}
