# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class RevolutionPhysicalControl(BaseProperty):
    physical_control: enums.PhysicalControl = dataclasses.field(default=enums.PhysicalControl.Unknown1)
    control_spline: Spline = dataclasses.field(default_factory=Spline)

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'`\xd6bD')  # 0x60d66244
        data.write(b'\x00\x04')  # size
        self.physical_control.to_stream(data)

        data.write(b'\x15V\x7f\xe7')  # 0x15567fe7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.control_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            physical_control=enums.PhysicalControl.from_json(data['physical_control']),
            control_spline=Spline.from_json(data['control_spline']),
        )

    def to_json(self) -> dict:
        return {
            'physical_control': self.physical_control.to_json(),
            'control_spline': self.control_spline.to_json(),
        }


def _decode_physical_control(data: typing.BinaryIO, property_size: int):
    return enums.PhysicalControl.from_stream(data)


def _decode_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x60d66244: ('physical_control', _decode_physical_control),
    0x15567fe7: ('control_spline', _decode_control_spline),
}
