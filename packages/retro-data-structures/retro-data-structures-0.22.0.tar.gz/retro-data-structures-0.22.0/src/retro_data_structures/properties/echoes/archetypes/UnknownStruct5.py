# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class UnknownStruct5(BaseProperty):
    override: bool = dataclasses.field(default=False)
    offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=1.0, z=1.0))

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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

        data.write(b'\x7f\xf8n\xe2')  # 0x7ff86ee2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.override))

        data.write(b'FGpd')  # 0x46477064
        data.write(b'\x00\x0c')  # size
        self.offset.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            override=data['override'],
            offset=Vector.from_json(data['offset']),
        )

    def to_json(self) -> dict:
        return {
            'override': self.override,
            'offset': self.offset.to_json(),
        }

    def dependencies_for(self, asset_manager):
        yield from []


def _decode_override(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7ff86ee2: ('override', _decode_override),
    0x46477064: ('offset', _decode_offset),
}
