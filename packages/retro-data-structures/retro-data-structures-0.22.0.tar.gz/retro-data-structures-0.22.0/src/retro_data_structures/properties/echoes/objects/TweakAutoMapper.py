# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.TweakAutoMapper.Base import Base
from retro_data_structures.properties.echoes.archetypes.TweakAutoMapper.DoorColors import DoorColors


@dataclasses.dataclass()
class TweakAutoMapper(BaseObjectType):
    instance_name: str = dataclasses.field(default='')
    base: Base = dataclasses.field(default_factory=Base)
    door_colors: DoorColors = dataclasses.field(default_factory=DoorColors)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return None

    def set_name(self, name: str) -> None:
        raise RuntimeError(f"{self.__class__.__name__} does not have name")

    @classmethod
    def object_type(cls) -> str:
        return 'TWAM'

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

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

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\x7f\xda\x14f')  # 0x7fda1466
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.instance_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x18\xb2\xf4#')  # 0x18b2f423
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.base.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc56\x88c')  # 0xc5368863
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.door_colors.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            instance_name=data['instance_name'],
            base=Base.from_json(data['base']),
            door_colors=DoorColors.from_json(data['door_colors']),
        )

    def to_json(self) -> dict:
        return {
            'instance_name': self.instance_name,
            'base': self.base.to_json(),
            'door_colors': self.door_colors.to_json(),
        }

    def _dependencies_for_base(self, asset_manager):
        yield from self.base.dependencies_for(asset_manager)

    def _dependencies_for_door_colors(self, asset_manager):
        yield from self.door_colors.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_base, "base", "Base"),
            (self._dependencies_for_door_colors, "door_colors", "DoorColors"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for TweakAutoMapper.{field_name} ({field_type}): {e}"
                )


def _decode_instance_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_base(data: typing.BinaryIO, property_size: int):
    return Base.from_stream(data, property_size)


def _decode_door_colors(data: typing.BinaryIO, property_size: int):
    return DoorColors.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7fda1466: ('instance_name', _decode_instance_name),
    0x18b2f423: ('base', _decode_base),
    0xc5368863: ('door_colors', _decode_door_colors),
}
