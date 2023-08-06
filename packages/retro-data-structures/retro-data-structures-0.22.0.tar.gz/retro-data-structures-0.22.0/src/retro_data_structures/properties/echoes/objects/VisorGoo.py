# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class VisorGoo(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    particle: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    electric: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    min_range: float = dataclasses.field(default=1.0)
    max_range: float = dataclasses.field(default=8.0)
    unknown_0x4538fdc7: float = dataclasses.field(default=40.0)
    unknown_0x057785b1: float = dataclasses.field(default=20.0)
    color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    sound_hit_sound: int = dataclasses.field(default=0)
    no_view_check: bool = dataclasses.field(default=False)
    persistent: bool = dataclasses.field(default=False)
    unknown_0xcb9a3009: bool = dataclasses.field(default=True)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'VGOO'

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
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'm\x1c\xe5%')  # 0x6d1ce525
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.particle))

        data.write(b'q\xdb\xe2\xf2')  # 0x71dbe2f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.electric))

        data.write(b'\x97D\x97\x1e')  # 0x9744971e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_range))

        data.write(b'\xd7\x0b\xefh')  # 0xd70bef68
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_range))

        data.write(b'E8\xfd\xc7')  # 0x4538fdc7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4538fdc7))

        data.write(b'\x05w\x85\xb1')  # 0x57785b1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x057785b1))

        data.write(b'7\xc7\xd0\x9d')  # 0x37c7d09d
        data.write(b'\x00\x10')  # size
        self.color.to_stream(data)

        data.write(b'\xa6\xdc\x9a\x92')  # 0xa6dc9a92
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_hit_sound))

        data.write(b'\xd5\xb7\x8b\xc9')  # 0xd5b78bc9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.no_view_check))

        data.write(b'\xea\x03\xe2X')  # 0xea03e258
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.persistent))

        data.write(b'\xcb\x9a0\t')  # 0xcb9a3009
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xcb9a3009))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            particle=data['particle'],
            electric=data['electric'],
            min_range=data['min_range'],
            max_range=data['max_range'],
            unknown_0x4538fdc7=data['unknown_0x4538fdc7'],
            unknown_0x057785b1=data['unknown_0x057785b1'],
            color=Color.from_json(data['color']),
            sound_hit_sound=data['sound_hit_sound'],
            no_view_check=data['no_view_check'],
            persistent=data['persistent'],
            unknown_0xcb9a3009=data['unknown_0xcb9a3009'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'particle': self.particle,
            'electric': self.electric,
            'min_range': self.min_range,
            'max_range': self.max_range,
            'unknown_0x4538fdc7': self.unknown_0x4538fdc7,
            'unknown_0x057785b1': self.unknown_0x057785b1,
            'color': self.color.to_json(),
            'sound_hit_sound': self.sound_hit_sound,
            'no_view_check': self.no_view_check,
            'persistent': self.persistent,
            'unknown_0xcb9a3009': self.unknown_0xcb9a3009,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_particle(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle)

    def _dependencies_for_electric(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.electric)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_particle, "particle", "AssetId"),
            (self._dependencies_for_electric, "electric", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for VisorGoo.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_particle(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_electric(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_min_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4538fdc7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x057785b1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_sound_hit_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_no_view_check(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_persistent(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xcb9a3009(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x6d1ce525: ('particle', _decode_particle),
    0x71dbe2f2: ('electric', _decode_electric),
    0x9744971e: ('min_range', _decode_min_range),
    0xd70bef68: ('max_range', _decode_max_range),
    0x4538fdc7: ('unknown_0x4538fdc7', _decode_unknown_0x4538fdc7),
    0x57785b1: ('unknown_0x057785b1', _decode_unknown_0x057785b1),
    0x37c7d09d: ('color', _decode_color),
    0xa6dc9a92: ('sound_hit_sound', _decode_sound_hit_sound),
    0xd5b78bc9: ('no_view_check', _decode_no_view_check),
    0xea03e258: ('persistent', _decode_persistent),
    0xcb9a3009: ('unknown_0xcb9a3009', _decode_unknown_0xcb9a3009),
}
