# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.InterpolationMethod import InterpolationMethod


@dataclasses.dataclass()
class OrientationInterpolationMethod(BaseProperty):
    orientation_type: enums.OrientationType = dataclasses.field(default=enums.OrientationType.Unknown3)
    orientation_control: InterpolationMethod = dataclasses.field(default_factory=InterpolationMethod)

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\\r\xa9d')  # 0x5c72a964
        data.write(b'\x00\x04')  # size
        self.orientation_type.to_stream(data)

        data.write(b'\x86T\xb0\x81')  # 0x8654b081
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.orientation_control.to_stream(data, default_override={'interpolation_control_type': enums.InterpolationControlType.Unknown5})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            orientation_type=enums.OrientationType.from_json(data['orientation_type']),
            orientation_control=InterpolationMethod.from_json(data['orientation_control']),
        )

    def to_json(self) -> dict:
        return {
            'orientation_type': self.orientation_type.to_json(),
            'orientation_control': self.orientation_control.to_json(),
        }


def _decode_orientation_type(data: typing.BinaryIO, property_size: int):
    return enums.OrientationType.from_stream(data)


def _decode_orientation_control(data: typing.BinaryIO, property_size: int):
    return InterpolationMethod.from_stream(data, property_size, default_override={'interpolation_control_type': enums.InterpolationControlType.Unknown5})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x5c72a964: ('orientation_type', _decode_orientation_type),
    0x8654b081: ('orientation_control', _decode_orientation_control),
}
