# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct8(BaseProperty):
    override: bool = dataclasses.field(default=False)
    z_offset: float = dataclasses.field(default=2.700000047683716)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\x7f\xf8n\xe2')  # 0x7ff86ee2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.override))

        data.write(b'\x803\xf9\xa3')  # 0x8033f9a3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.z_offset))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            override=data['override'],
            z_offset=data['z_offset'],
        )

    def to_json(self) -> dict:
        return {
            'override': self.override,
            'z_offset': self.z_offset,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0x7ff86ee2, 0x8033f9a3)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct8]:
    if property_count != 2:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(17))
    if (dec[0], dec[3]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct8(
        dec[2],
        dec[5],
    )


def _decode_override(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_z_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7ff86ee2: ('override', _decode_override),
    0x8033f9a3: ('z_offset', _decode_z_offset),
}
