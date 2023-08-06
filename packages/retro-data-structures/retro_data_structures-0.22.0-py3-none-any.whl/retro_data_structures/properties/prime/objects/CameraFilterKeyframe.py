# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Color import Color


@dataclasses.dataclass()
class CameraFilterKeyframe(BaseObjectType):
    name: str = dataclasses.field(default='')
    active: bool = dataclasses.field(default=False)
    filter_type: int = dataclasses.field(default=0)
    filter_shape: int = dataclasses.field(default=0)
    unknown_4: int = dataclasses.field(default=0)
    unknown_5: int = dataclasses.field(default=0)
    filter_color: Color = dataclasses.field(default_factory=Color)
    fade_in_duration: float = dataclasses.field(default=0.0)
    fade_out_duration: float = dataclasses.field(default=0.0)
    overlay_texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x18

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        active = struct.unpack('>?', data.read(1))[0]
        filter_type = struct.unpack('>l', data.read(4))[0]
        filter_shape = struct.unpack('>l', data.read(4))[0]
        unknown_4 = struct.unpack('>l', data.read(4))[0]
        unknown_5 = struct.unpack('>l', data.read(4))[0]
        filter_color = Color.from_stream(data)
        fade_in_duration = struct.unpack('>f', data.read(4))[0]
        fade_out_duration = struct.unpack('>f', data.read(4))[0]
        overlay_texture = struct.unpack(">L", data.read(4))[0]
        return cls(name, active, filter_type, filter_shape, unknown_4, unknown_5, filter_color, fade_in_duration, fade_out_duration, overlay_texture)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\n')  # 10 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        data.write(struct.pack('>?', self.active))
        data.write(struct.pack('>l', self.filter_type))
        data.write(struct.pack('>l', self.filter_shape))
        data.write(struct.pack('>l', self.unknown_4))
        data.write(struct.pack('>l', self.unknown_5))
        self.filter_color.to_stream(data)
        data.write(struct.pack('>f', self.fade_in_duration))
        data.write(struct.pack('>f', self.fade_out_duration))
        data.write(struct.pack(">L", self.overlay_texture))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            active=data['active'],
            filter_type=data['filter_type'],
            filter_shape=data['filter_shape'],
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
            filter_color=Color.from_json(data['filter_color']),
            fade_in_duration=data['fade_in_duration'],
            fade_out_duration=data['fade_out_duration'],
            overlay_texture=data['overlay_texture'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'active': self.active,
            'filter_type': self.filter_type,
            'filter_shape': self.filter_shape,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'filter_color': self.filter_color.to_json(),
            'fade_in_duration': self.fade_in_duration,
            'fade_out_duration': self.fade_out_duration,
            'overlay_texture': self.overlay_texture,
        }

    def _dependencies_for_overlay_texture(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.overlay_texture)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_overlay_texture, "overlay_texture", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for CameraFilterKeyframe.{field_name} ({field_type}): {e}"
                )
