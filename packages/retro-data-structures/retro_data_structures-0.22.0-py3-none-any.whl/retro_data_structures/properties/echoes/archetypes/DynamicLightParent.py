# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class DynamicLightParent(BaseProperty):
    unknown_0xddd74295: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    unknown_0x88f018b3: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    locator_name: str = dataclasses.field(default='')
    use_parent_rotation: bool = dataclasses.field(default=False)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xdd\xd7B\x95')  # 0xddd74295
        data.write(b'\x00\x0c')  # size
        self.unknown_0xddd74295.to_stream(data)

        data.write(b'\x88\xf0\x18\xb3')  # 0x88f018b3
        data.write(b'\x00\x0c')  # size
        self.unknown_0x88f018b3.to_stream(data)

        data.write(b'\xfb\xc6\xc1\x10')  # 0xfbc6c110
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.locator_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf7.\xef\xbd')  # 0xf72eefbd
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_parent_rotation))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xddd74295=Vector.from_json(data['unknown_0xddd74295']),
            unknown_0x88f018b3=Vector.from_json(data['unknown_0x88f018b3']),
            locator_name=data['locator_name'],
            use_parent_rotation=data['use_parent_rotation'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xddd74295': self.unknown_0xddd74295.to_json(),
            'unknown_0x88f018b3': self.unknown_0x88f018b3.to_json(),
            'locator_name': self.locator_name,
            'use_parent_rotation': self.use_parent_rotation,
        }

    def dependencies_for(self, asset_manager):
        yield from []


def _decode_unknown_0xddd74295(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_0x88f018b3(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_locator_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_use_parent_rotation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xddd74295: ('unknown_0xddd74295', _decode_unknown_0xddd74295),
    0x88f018b3: ('unknown_0x88f018b3', _decode_unknown_0x88f018b3),
    0xfbc6c110: ('locator_name', _decode_locator_name),
    0xf72eefbd: ('use_parent_rotation', _decode_use_parent_rotation),
}
