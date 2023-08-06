# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.SpindlePositionInterpolant import SpindlePositionInterpolant


@dataclasses.dataclass()
class SpindleOrientation(BaseProperty):
    flags_spindle_orientation: int = dataclasses.field(default=786432)
    look_at_angular_offset: SpindlePositionInterpolant = dataclasses.field(default_factory=SpindlePositionInterpolant)
    look_at_z_offset: SpindlePositionInterpolant = dataclasses.field(default_factory=SpindlePositionInterpolant)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\x1bIb\xbf')  # 0x1b4962bf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.flags_spindle_orientation))

        data.write(b'`\x9c\x06\x08')  # 0x609c0608
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.look_at_angular_offset.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf6\xc8(\xc0')  # 0xf6c828c0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.look_at_z_offset.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            flags_spindle_orientation=data['flags_spindle_orientation'],
            look_at_angular_offset=SpindlePositionInterpolant.from_json(data['look_at_angular_offset']),
            look_at_z_offset=SpindlePositionInterpolant.from_json(data['look_at_z_offset']),
        )

    def to_json(self) -> dict:
        return {
            'flags_spindle_orientation': self.flags_spindle_orientation,
            'look_at_angular_offset': self.look_at_angular_offset.to_json(),
            'look_at_z_offset': self.look_at_z_offset.to_json(),
        }


def _decode_flags_spindle_orientation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_look_at_angular_offset(data: typing.BinaryIO, property_size: int):
    return SpindlePositionInterpolant.from_stream(data, property_size)


def _decode_look_at_z_offset(data: typing.BinaryIO, property_size: int):
    return SpindlePositionInterpolant.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1b4962bf: ('flags_spindle_orientation', _decode_flags_spindle_orientation),
    0x609c0608: ('look_at_angular_offset', _decode_look_at_angular_offset),
    0xf6c828c0: ('look_at_z_offset', _decode_look_at_z_offset),
}
