# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.Transform import Transform


@dataclasses.dataclass()
class EditorProperties(BaseProperty):
    name: str = dataclasses.field(default='')
    transform: Transform = dataclasses.field(default_factory=Transform)
    active: bool = dataclasses.field(default=True)
    unknown: int = dataclasses.field(default=3)  # Flagset

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

        data.write(b'INAM')  # 0x494e414d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'XFRM')  # 0x5846524d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.transform.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'ACTV')  # 0x41435456
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.active))

        data.write(b'])\x8aC')  # 0x5d298a43
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            transform=Transform.from_json(data['transform']),
            active=data['active'],
            unknown=data['unknown'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'transform': self.transform.to_json(),
            'active': self.active,
            'unknown': self.unknown,
        }

    def _dependencies_for_transform(self, asset_manager):
        yield from self.transform.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_transform, "transform", "Transform"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for EditorProperties.{field_name} ({field_type}): {e}"
                )


def _decode_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_transform(data: typing.BinaryIO, property_size: int):
    return Transform.from_stream(data, property_size)


def _decode_active(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x494e414d: ('name', _decode_name),
    0x5846524d: ('transform', _decode_transform),
    0x41435456: ('active', _decode_active),
    0x5d298a43: ('unknown', _decode_unknown),
}
