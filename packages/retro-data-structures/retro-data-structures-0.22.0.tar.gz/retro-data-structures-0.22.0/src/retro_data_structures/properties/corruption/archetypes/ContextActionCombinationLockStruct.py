# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class ContextActionCombinationLockStruct(BaseProperty):
    initial_angle: float = dataclasses.field(default=0.0)
    unlock_angle: float = dataclasses.field(default=0.0)
    min_angle: float = dataclasses.field(default=-90.0)
    max_angle: float = dataclasses.field(default=90.0)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

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

        data.write(b'\x90\xac\x80A')  # 0x90ac8041
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_angle))

        data.write(b'\x89\xc4\xcc_')  # 0x89c4cc5f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unlock_angle))

        data.write(b'\x99,-\xf5')  # 0x992c2df5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_angle))

        data.write(b'\xd9cU\x83')  # 0xd9635583
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_angle))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            initial_angle=data['initial_angle'],
            unlock_angle=data['unlock_angle'],
            min_angle=data['min_angle'],
            max_angle=data['max_angle'],
        )

    def to_json(self) -> dict:
        return {
            'initial_angle': self.initial_angle,
            'unlock_angle': self.unlock_angle,
            'min_angle': self.min_angle,
            'max_angle': self.max_angle,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x90ac8041, 0x89c4cc5f, 0x992c2df5, 0xd9635583)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[ContextActionCombinationLockStruct]:
    if property_count != 4:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(40))
    if (dec[0], dec[3], dec[6], dec[9]) != _FAST_IDS:
        data.seek(before)
        return None

    return ContextActionCombinationLockStruct(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_initial_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unlock_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x90ac8041: ('initial_angle', _decode_initial_angle),
    0x89c4cc5f: ('unlock_angle', _decode_unlock_angle),
    0x992c2df5: ('min_angle', _decode_min_angle),
    0xd9635583: ('max_angle', _decode_max_angle),
}
