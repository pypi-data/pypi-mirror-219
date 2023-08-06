# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.DynamicLightFalloff import DynamicLightFalloff
from retro_data_structures.properties.echoes.archetypes.DynamicLightIntensity import DynamicLightIntensity
from retro_data_structures.properties.echoes.archetypes.DynamicLightMotionSpline import DynamicLightMotionSpline
from retro_data_structures.properties.echoes.archetypes.DynamicLightParent import DynamicLightParent
from retro_data_structures.properties.echoes.archetypes.DynamicLightSpotlight import DynamicLightSpotlight
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class DynamicLight(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    light_type: int = dataclasses.field(default=2)
    light_set: int = dataclasses.field(default=6)
    color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    intensity: DynamicLightIntensity = dataclasses.field(default_factory=DynamicLightIntensity)
    falloff: DynamicLightFalloff = dataclasses.field(default_factory=DynamicLightFalloff)
    spotlight: DynamicLightSpotlight = dataclasses.field(default_factory=DynamicLightSpotlight)
    motion_spline: DynamicLightMotionSpline = dataclasses.field(default_factory=DynamicLightMotionSpline)
    parent: DynamicLightParent = dataclasses.field(default_factory=DynamicLightParent)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'DLHT'

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x7f\xc4\xe36')  # 0x7fc4e336
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.light_type))

        data.write(b'>\x8b;/')  # 0x3e8b3b2f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.light_set))

        data.write(b'7\xc7\xd0\x9d')  # 0x37c7d09d
        data.write(b'\x00\x10')  # size
        self.color.to_stream(data)

        data.write(b'rS\x1e\xde')  # 0x72531ede
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.intensity.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'!\x9bR\xda')  # 0x219b52da
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.falloff.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95F\xf4I')  # 0x9546f449
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spotlight.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x142!8')  # 0x14322138
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf74\xdf\x8c')  # 0xf734df8c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.parent.to_stream(data)
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
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            light_type=data['light_type'],
            light_set=data['light_set'],
            color=Color.from_json(data['color']),
            intensity=DynamicLightIntensity.from_json(data['intensity']),
            falloff=DynamicLightFalloff.from_json(data['falloff']),
            spotlight=DynamicLightSpotlight.from_json(data['spotlight']),
            motion_spline=DynamicLightMotionSpline.from_json(data['motion_spline']),
            parent=DynamicLightParent.from_json(data['parent']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'light_type': self.light_type,
            'light_set': self.light_set,
            'color': self.color.to_json(),
            'intensity': self.intensity.to_json(),
            'falloff': self.falloff.to_json(),
            'spotlight': self.spotlight.to_json(),
            'motion_spline': self.motion_spline.to_json(),
            'parent': self.parent.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_intensity(self, asset_manager):
        yield from self.intensity.dependencies_for(asset_manager)

    def _dependencies_for_falloff(self, asset_manager):
        yield from self.falloff.dependencies_for(asset_manager)

    def _dependencies_for_spotlight(self, asset_manager):
        yield from self.spotlight.dependencies_for(asset_manager)

    def _dependencies_for_motion_spline(self, asset_manager):
        yield from self.motion_spline.dependencies_for(asset_manager)

    def _dependencies_for_parent(self, asset_manager):
        yield from self.parent.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_intensity, "intensity", "DynamicLightIntensity"),
            (self._dependencies_for_falloff, "falloff", "DynamicLightFalloff"),
            (self._dependencies_for_spotlight, "spotlight", "DynamicLightSpotlight"),
            (self._dependencies_for_motion_spline, "motion_spline", "DynamicLightMotionSpline"),
            (self._dependencies_for_parent, "parent", "DynamicLightParent"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for DynamicLight.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_light_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_light_set(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_intensity(data: typing.BinaryIO, property_size: int):
    return DynamicLightIntensity.from_stream(data, property_size)


def _decode_falloff(data: typing.BinaryIO, property_size: int):
    return DynamicLightFalloff.from_stream(data, property_size)


def _decode_spotlight(data: typing.BinaryIO, property_size: int):
    return DynamicLightSpotlight.from_stream(data, property_size)


def _decode_motion_spline(data: typing.BinaryIO, property_size: int):
    return DynamicLightMotionSpline.from_stream(data, property_size)


def _decode_parent(data: typing.BinaryIO, property_size: int):
    return DynamicLightParent.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x7fc4e336: ('light_type', _decode_light_type),
    0x3e8b3b2f: ('light_set', _decode_light_set),
    0x37c7d09d: ('color', _decode_color),
    0x72531ede: ('intensity', _decode_intensity),
    0x219b52da: ('falloff', _decode_falloff),
    0x9546f449: ('spotlight', _decode_spotlight),
    0x14322138: ('motion_spline', _decode_motion_spline),
    0xf734df8c: ('parent', _decode_parent),
}
