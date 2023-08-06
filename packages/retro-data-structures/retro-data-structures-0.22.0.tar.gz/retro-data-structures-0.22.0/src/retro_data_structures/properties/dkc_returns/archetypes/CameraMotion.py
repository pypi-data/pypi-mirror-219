# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct76 import UnknownStruct76
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct77 import UnknownStruct77


@dataclasses.dataclass()
class CameraMotion(BaseProperty):
    motion_type: int = dataclasses.field(default=888911163)  # Choice
    unknown_struct76: UnknownStruct76 = dataclasses.field(default_factory=UnknownStruct76)
    unknown_struct77: UnknownStruct77 = dataclasses.field(default_factory=UnknownStruct77)

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

        data.write(b'\x94\x8a\xf5q')  # 0x948af571
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.motion_type))

        data.write(b'\xb4\nA\xb8')  # 0xb40a41b8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct76.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0c8\xa0\t')  # 0xc38a009
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct77.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            motion_type=data['motion_type'],
            unknown_struct76=UnknownStruct76.from_json(data['unknown_struct76']),
            unknown_struct77=UnknownStruct77.from_json(data['unknown_struct77']),
        )

    def to_json(self) -> dict:
        return {
            'motion_type': self.motion_type,
            'unknown_struct76': self.unknown_struct76.to_json(),
            'unknown_struct77': self.unknown_struct77.to_json(),
        }


def _decode_motion_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_struct76(data: typing.BinaryIO, property_size: int):
    return UnknownStruct76.from_stream(data, property_size)


def _decode_unknown_struct77(data: typing.BinaryIO, property_size: int):
    return UnknownStruct77.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x948af571: ('motion_type', _decode_motion_type),
    0xb40a41b8: ('unknown_struct76', _decode_unknown_struct76),
    0xc38a009: ('unknown_struct77', _decode_unknown_struct77),
}
