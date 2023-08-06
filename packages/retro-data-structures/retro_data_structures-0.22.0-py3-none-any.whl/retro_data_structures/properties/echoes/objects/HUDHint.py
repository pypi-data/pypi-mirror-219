# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class HUDHint(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    hud_texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    unknown_0x6078a651: float = dataclasses.field(default=15.0)
    unknown_0xf00bb6bb: float = dataclasses.field(default=16.0)
    icon_scale: float = dataclasses.field(default=1.0)
    animation_time: float = dataclasses.field(default=0.0)
    animation_frames: int = dataclasses.field(default=0)
    unknown_0xd993f97b: int = dataclasses.field(default=15)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'HHNT'

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd8\x04G\xe0')  # 0xd80447e0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.hud_texture))

        data.write(b'`x\xa6Q')  # 0x6078a651
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6078a651))

        data.write(b'\xf0\x0b\xb6\xbb')  # 0xf00bb6bb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf00bb6bb))

        data.write(b'\x1a\xd2G\xa1')  # 0x1ad247a1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.icon_scale))

        data.write(b'*S$Z')  # 0x2a53245a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.animation_time))

        data.write(b'n\x88\xd6\xad')  # 0x6e88d6ad
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.animation_frames))

        data.write(b'\xd9\x93\xf9{')  # 0xd993f97b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xd993f97b))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            hud_texture=data['hud_texture'],
            unknown_0x6078a651=data['unknown_0x6078a651'],
            unknown_0xf00bb6bb=data['unknown_0xf00bb6bb'],
            icon_scale=data['icon_scale'],
            animation_time=data['animation_time'],
            animation_frames=data['animation_frames'],
            unknown_0xd993f97b=data['unknown_0xd993f97b'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'hud_texture': self.hud_texture,
            'unknown_0x6078a651': self.unknown_0x6078a651,
            'unknown_0xf00bb6bb': self.unknown_0xf00bb6bb,
            'icon_scale': self.icon_scale,
            'animation_time': self.animation_time,
            'animation_frames': self.animation_frames,
            'unknown_0xd993f97b': self.unknown_0xd993f97b,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_hud_texture(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.hud_texture)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_hud_texture, "hud_texture", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for HUDHint.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_hud_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x6078a651(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf00bb6bb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_icon_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_animation_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_animation_frames(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xd993f97b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xd80447e0: ('hud_texture', _decode_hud_texture),
    0x6078a651: ('unknown_0x6078a651', _decode_unknown_0x6078a651),
    0xf00bb6bb: ('unknown_0xf00bb6bb', _decode_unknown_0xf00bb6bb),
    0x1ad247a1: ('icon_scale', _decode_icon_scale),
    0x2a53245a: ('animation_time', _decode_animation_time),
    0x6e88d6ad: ('animation_frames', _decode_animation_frames),
    0xd993f97b: ('unknown_0xd993f97b', _decode_unknown_0xd993f97b),
}
