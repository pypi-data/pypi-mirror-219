# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct14 import UnknownStruct14
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct67 import UnknownStruct67


@dataclasses.dataclass()
class UnknownStruct68(BaseProperty):
    horizontal_type: enums.HorizontalType = dataclasses.field(default=enums.HorizontalType.Unknown1)
    unknown_struct67: UnknownStruct67 = dataclasses.field(default_factory=UnknownStruct67)
    unknown_struct14: UnknownStruct14 = dataclasses.field(default_factory=UnknownStruct14)

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

        data.write(b'+rG\xaa')  # 0x2b7247aa
        data.write(b'\x00\x04')  # size
        self.horizontal_type.to_stream(data)

        data.write(b'\xb0*\xaaS')  # 0xb02aaa53
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct67.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x02\xb7\x92C')  # 0x2b79243
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct14.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            horizontal_type=enums.HorizontalType.from_json(data['horizontal_type']),
            unknown_struct67=UnknownStruct67.from_json(data['unknown_struct67']),
            unknown_struct14=UnknownStruct14.from_json(data['unknown_struct14']),
        )

    def to_json(self) -> dict:
        return {
            'horizontal_type': self.horizontal_type.to_json(),
            'unknown_struct67': self.unknown_struct67.to_json(),
            'unknown_struct14': self.unknown_struct14.to_json(),
        }


def _decode_horizontal_type(data: typing.BinaryIO, property_size: int):
    return enums.HorizontalType.from_stream(data)


def _decode_unknown_struct67(data: typing.BinaryIO, property_size: int):
    return UnknownStruct67.from_stream(data, property_size)


def _decode_unknown_struct14(data: typing.BinaryIO, property_size: int):
    return UnknownStruct14.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2b7247aa: ('horizontal_type', _decode_horizontal_type),
    0xb02aaa53: ('unknown_struct67', _decode_unknown_struct67),
    0x2b79243: ('unknown_struct14', _decode_unknown_struct14),
}
