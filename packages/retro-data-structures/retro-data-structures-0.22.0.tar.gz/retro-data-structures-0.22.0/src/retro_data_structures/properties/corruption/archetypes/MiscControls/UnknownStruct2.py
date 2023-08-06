# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.RevolutionControl import RevolutionControl


@dataclasses.dataclass()
class UnknownStruct2(BaseProperty):
    unknown_0x67739b75: enums.MiscControls_UnknownEnum1 = dataclasses.field(default=enums.MiscControls_UnknownEnum1.Unknown1)
    unknown_0xa5e20450: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0xa74987ff: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x73eb9d04: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'gs\x9bu')  # 0x67739b75
        data.write(b'\x00\x04')  # size
        self.unknown_0x67739b75.to_stream(data)

        data.write(b'\xa5\xe2\x04P')  # 0xa5e20450
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xa5e20450.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa7I\x87\xff')  # 0xa74987ff
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xa74987ff.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b's\xeb\x9d\x04')  # 0x73eb9d04
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x73eb9d04.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x67739b75=enums.MiscControls_UnknownEnum1.from_json(data['unknown_0x67739b75']),
            unknown_0xa5e20450=RevolutionControl.from_json(data['unknown_0xa5e20450']),
            unknown_0xa74987ff=RevolutionControl.from_json(data['unknown_0xa74987ff']),
            unknown_0x73eb9d04=RevolutionControl.from_json(data['unknown_0x73eb9d04']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x67739b75': self.unknown_0x67739b75.to_json(),
            'unknown_0xa5e20450': self.unknown_0xa5e20450.to_json(),
            'unknown_0xa74987ff': self.unknown_0xa74987ff.to_json(),
            'unknown_0x73eb9d04': self.unknown_0x73eb9d04.to_json(),
        }


def _decode_unknown_0x67739b75(data: typing.BinaryIO, property_size: int):
    return enums.MiscControls_UnknownEnum1.from_stream(data)


def _decode_unknown_0xa5e20450(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0xa74987ff(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x73eb9d04(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x67739b75: ('unknown_0x67739b75', _decode_unknown_0x67739b75),
    0xa5e20450: ('unknown_0xa5e20450', _decode_unknown_0xa5e20450),
    0xa74987ff: ('unknown_0xa74987ff', _decode_unknown_0xa74987ff),
    0x73eb9d04: ('unknown_0x73eb9d04', _decode_unknown_0x73eb9d04),
}
