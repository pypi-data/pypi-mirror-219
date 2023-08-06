# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.InterpolationMethod import InterpolationMethod


@dataclasses.dataclass()
class FOVInterpolationMethod(BaseProperty):
    fov_type: enums.FOVType = dataclasses.field(default=enums.FOVType.Unknown1)
    fov_control: InterpolationMethod = dataclasses.field(default_factory=InterpolationMethod)

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

        data.write(b'\x19\xea\x15\x1b')  # 0x19ea151b
        data.write(b'\x00\x04')  # size
        self.fov_type.to_stream(data)

        data.write(b'\x9f\x90\x01L')  # 0x9f90014c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.fov_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            fov_type=enums.FOVType.from_json(data['fov_type']),
            fov_control=InterpolationMethod.from_json(data['fov_control']),
        )

    def to_json(self) -> dict:
        return {
            'fov_type': self.fov_type.to_json(),
            'fov_control': self.fov_control.to_json(),
        }


def _decode_fov_type(data: typing.BinaryIO, property_size: int):
    return enums.FOVType.from_stream(data)


def _decode_fov_control(data: typing.BinaryIO, property_size: int):
    return InterpolationMethod.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x19ea151b: ('fov_type', _decode_fov_type),
    0x9f90014c: ('fov_control', _decode_fov_control),
}
