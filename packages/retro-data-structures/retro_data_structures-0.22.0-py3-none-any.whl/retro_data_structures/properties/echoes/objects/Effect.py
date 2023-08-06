# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.LightParameters import LightParameters
from retro_data_structures.properties.echoes.archetypes.SplineType import SplineType
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Spline import Spline


@dataclasses.dataclass()
class Effect(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    particle_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART', 'ELSC', 'SRSC', 'SPSC', 'SWHC']}, default=default_asset_id)
    unknown_0x3df5a489: bool = dataclasses.field(default=False)
    restart_on_activate: bool = dataclasses.field(default=False)
    unknown_0xee538174: bool = dataclasses.field(default=False)
    unknown_0xa94b0efd: float = dataclasses.field(default=5.0)
    unknown_0x93756968: float = dataclasses.field(default=0.5)
    unknown_0x0b94597d: float = dataclasses.field(default=0.20000000298023224)
    unknown_0xd0e8a496: float = dataclasses.field(default=0.10000000149011612)
    unknown_0xa8bb6c61: bool = dataclasses.field(default=False)
    unknown_0x7589d549: float = dataclasses.field(default=20.0)
    unknown_0xa7d7d767: float = dataclasses.field(default=30.0)
    unknown_0xfe69615c: float = dataclasses.field(default=0.0)
    unknown_0x88d914a6: bool = dataclasses.field(default=True)
    visible_in_dark: bool = dataclasses.field(default=True)
    visible_in_echo: bool = dataclasses.field(default=True)
    unknown_0x6714021c: bool = dataclasses.field(default=False)
    unknown_0xbe931927: bool = dataclasses.field(default=False)
    render_order: int = dataclasses.field(default=0)
    lighting: LightParameters = dataclasses.field(default_factory=LightParameters)
    motion_spline_path_loops: bool = dataclasses.field(default=False)
    motion_spline_type: SplineType = dataclasses.field(default_factory=SplineType)
    motion_control_spline: Spline = dataclasses.field(default_factory=Spline)
    motion_spline_duration: float = dataclasses.field(default=10.0)
    unknown_0x73e63382: bool = dataclasses.field(default=False)
    unknown_0x608ecac5: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'EFCT'

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
        data.write(b'\x00\x1a')  # 26 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\nG\x9do')  # 0xa479d6f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.particle_effect))

        data.write(b'=\xf5\xa4\x89')  # 0x3df5a489
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x3df5a489))

        data.write(b'\xa4\xb9\x98O')  # 0xa4b9984f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.restart_on_activate))

        data.write(b'\xeeS\x81t')  # 0xee538174
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xee538174))

        data.write(b'\xa9K\x0e\xfd')  # 0xa94b0efd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa94b0efd))

        data.write(b'\x93uih')  # 0x93756968
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x93756968))

        data.write(b'\x0b\x94Y}')  # 0xb94597d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0b94597d))

        data.write(b'\xd0\xe8\xa4\x96')  # 0xd0e8a496
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd0e8a496))

        data.write(b'\xa8\xbbla')  # 0xa8bb6c61
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xa8bb6c61))

        data.write(b'u\x89\xd5I')  # 0x7589d549
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7589d549))

        data.write(b'\xa7\xd7\xd7g')  # 0xa7d7d767
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa7d7d767))

        data.write(b'\xfeia\\')  # 0xfe69615c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfe69615c))

        data.write(b'\x88\xd9\x14\xa6')  # 0x88d914a6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x88d914a6))

        data.write(b'\xc2\x02\x8c\xc2')  # 0xc2028cc2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.visible_in_dark))

        data.write(b'\xce\xfa\x1aH')  # 0xcefa1a48
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.visible_in_echo))

        data.write(b'g\x14\x02\x1c')  # 0x6714021c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x6714021c))

        data.write(b"\xbe\x93\x19'")  # 0xbe931927
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xbe931927))

        data.write(b'/\xa4\xe5\xd7')  # 0x2fa4e5d7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.render_order))

        data.write(b'\xb0(\xdb\x0e')  # 0xb028db0e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.lighting.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'=t\x06\xaf')  # 0x3d7406af
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.motion_spline_path_loops))

        data.write(b'I=j-')  # 0x493d6a2d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_spline_type.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"'\xe5\xf8t")  # 0x27e5f874
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_control_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfd\x1e/V')  # 0xfd1e2f56
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.motion_spline_duration))

        data.write(b's\xe63\x82')  # 0x73e63382
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x73e63382))

        data.write(b'`\x8e\xca\xc5')  # 0x608ecac5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x608ecac5))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            particle_effect=data['particle_effect'],
            unknown_0x3df5a489=data['unknown_0x3df5a489'],
            restart_on_activate=data['restart_on_activate'],
            unknown_0xee538174=data['unknown_0xee538174'],
            unknown_0xa94b0efd=data['unknown_0xa94b0efd'],
            unknown_0x93756968=data['unknown_0x93756968'],
            unknown_0x0b94597d=data['unknown_0x0b94597d'],
            unknown_0xd0e8a496=data['unknown_0xd0e8a496'],
            unknown_0xa8bb6c61=data['unknown_0xa8bb6c61'],
            unknown_0x7589d549=data['unknown_0x7589d549'],
            unknown_0xa7d7d767=data['unknown_0xa7d7d767'],
            unknown_0xfe69615c=data['unknown_0xfe69615c'],
            unknown_0x88d914a6=data['unknown_0x88d914a6'],
            visible_in_dark=data['visible_in_dark'],
            visible_in_echo=data['visible_in_echo'],
            unknown_0x6714021c=data['unknown_0x6714021c'],
            unknown_0xbe931927=data['unknown_0xbe931927'],
            render_order=data['render_order'],
            lighting=LightParameters.from_json(data['lighting']),
            motion_spline_path_loops=data['motion_spline_path_loops'],
            motion_spline_type=SplineType.from_json(data['motion_spline_type']),
            motion_control_spline=Spline.from_json(data['motion_control_spline']),
            motion_spline_duration=data['motion_spline_duration'],
            unknown_0x73e63382=data['unknown_0x73e63382'],
            unknown_0x608ecac5=data['unknown_0x608ecac5'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'particle_effect': self.particle_effect,
            'unknown_0x3df5a489': self.unknown_0x3df5a489,
            'restart_on_activate': self.restart_on_activate,
            'unknown_0xee538174': self.unknown_0xee538174,
            'unknown_0xa94b0efd': self.unknown_0xa94b0efd,
            'unknown_0x93756968': self.unknown_0x93756968,
            'unknown_0x0b94597d': self.unknown_0x0b94597d,
            'unknown_0xd0e8a496': self.unknown_0xd0e8a496,
            'unknown_0xa8bb6c61': self.unknown_0xa8bb6c61,
            'unknown_0x7589d549': self.unknown_0x7589d549,
            'unknown_0xa7d7d767': self.unknown_0xa7d7d767,
            'unknown_0xfe69615c': self.unknown_0xfe69615c,
            'unknown_0x88d914a6': self.unknown_0x88d914a6,
            'visible_in_dark': self.visible_in_dark,
            'visible_in_echo': self.visible_in_echo,
            'unknown_0x6714021c': self.unknown_0x6714021c,
            'unknown_0xbe931927': self.unknown_0xbe931927,
            'render_order': self.render_order,
            'lighting': self.lighting.to_json(),
            'motion_spline_path_loops': self.motion_spline_path_loops,
            'motion_spline_type': self.motion_spline_type.to_json(),
            'motion_control_spline': self.motion_control_spline.to_json(),
            'motion_spline_duration': self.motion_spline_duration,
            'unknown_0x73e63382': self.unknown_0x73e63382,
            'unknown_0x608ecac5': self.unknown_0x608ecac5,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_particle_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_effect)

    def _dependencies_for_lighting(self, asset_manager):
        yield from self.lighting.dependencies_for(asset_manager)

    def _dependencies_for_motion_spline_type(self, asset_manager):
        yield from self.motion_spline_type.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_particle_effect, "particle_effect", "AssetId"),
            (self._dependencies_for_lighting, "lighting", "LightParameters"),
            (self._dependencies_for_motion_spline_type, "motion_spline_type", "SplineType"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Effect.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_particle_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x3df5a489(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_restart_on_activate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xee538174(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xa94b0efd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x93756968(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0b94597d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd0e8a496(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa8bb6c61(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x7589d549(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa7d7d767(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xfe69615c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x88d914a6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_visible_in_dark(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_visible_in_echo(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x6714021c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xbe931927(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_render_order(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_lighting(data: typing.BinaryIO, property_size: int):
    return LightParameters.from_stream(data, property_size)


def _decode_motion_spline_path_loops(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_motion_spline_type(data: typing.BinaryIO, property_size: int):
    return SplineType.from_stream(data, property_size)


def _decode_motion_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_motion_spline_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x73e63382(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x608ecac5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xa479d6f: ('particle_effect', _decode_particle_effect),
    0x3df5a489: ('unknown_0x3df5a489', _decode_unknown_0x3df5a489),
    0xa4b9984f: ('restart_on_activate', _decode_restart_on_activate),
    0xee538174: ('unknown_0xee538174', _decode_unknown_0xee538174),
    0xa94b0efd: ('unknown_0xa94b0efd', _decode_unknown_0xa94b0efd),
    0x93756968: ('unknown_0x93756968', _decode_unknown_0x93756968),
    0xb94597d: ('unknown_0x0b94597d', _decode_unknown_0x0b94597d),
    0xd0e8a496: ('unknown_0xd0e8a496', _decode_unknown_0xd0e8a496),
    0xa8bb6c61: ('unknown_0xa8bb6c61', _decode_unknown_0xa8bb6c61),
    0x7589d549: ('unknown_0x7589d549', _decode_unknown_0x7589d549),
    0xa7d7d767: ('unknown_0xa7d7d767', _decode_unknown_0xa7d7d767),
    0xfe69615c: ('unknown_0xfe69615c', _decode_unknown_0xfe69615c),
    0x88d914a6: ('unknown_0x88d914a6', _decode_unknown_0x88d914a6),
    0xc2028cc2: ('visible_in_dark', _decode_visible_in_dark),
    0xcefa1a48: ('visible_in_echo', _decode_visible_in_echo),
    0x6714021c: ('unknown_0x6714021c', _decode_unknown_0x6714021c),
    0xbe931927: ('unknown_0xbe931927', _decode_unknown_0xbe931927),
    0x2fa4e5d7: ('render_order', _decode_render_order),
    0xb028db0e: ('lighting', _decode_lighting),
    0x3d7406af: ('motion_spline_path_loops', _decode_motion_spline_path_loops),
    0x493d6a2d: ('motion_spline_type', _decode_motion_spline_type),
    0x27e5f874: ('motion_control_spline', _decode_motion_control_spline),
    0xfd1e2f56: ('motion_spline_duration', _decode_motion_spline_duration),
    0x73e63382: ('unknown_0x73e63382', _decode_unknown_0x73e63382),
    0x608ecac5: ('unknown_0x608ecac5', _decode_unknown_0x608ecac5),
}
