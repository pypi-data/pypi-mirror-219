# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.LightParameters import LightParameters
from retro_data_structures.properties.dkc_returns.archetypes.SplineType import SplineType
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class Effect(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    particle_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART', 'SPSC', 'SWHC']}, default=default_asset_id)
    auto_start: bool = dataclasses.field(default=True)
    unknown_0x3df5a489: bool = dataclasses.field(default=False)
    unknown_0x08349bd6: bool = dataclasses.field(default=False)
    render_in_foreground: bool = dataclasses.field(default=False)
    unknown_0x6714021c: bool = dataclasses.field(default=True)
    unknown_0xbe931927: bool = dataclasses.field(default=False)
    unknown_0xe448aa81: bool = dataclasses.field(default=False)
    unknown_0x3613bc90: bool = dataclasses.field(default=False)
    render_override: enums.RenderOverride = dataclasses.field(default=enums.RenderOverride.Unknown3)
    lighting: LightParameters = dataclasses.field(default_factory=LightParameters)
    unknown_0xacc1a0aa: bool = dataclasses.field(default=False)
    motion_spline_path_loops: bool = dataclasses.field(default=False)
    motion_spline_type: SplineType = dataclasses.field(default_factory=SplineType)
    motion_control_spline: Spline = dataclasses.field(default_factory=Spline)
    motion_spline_duration: float = dataclasses.field(default=10.0)
    unknown_0x73e63382: bool = dataclasses.field(default=False)
    unknown_0x608ecac5: bool = dataclasses.field(default=False)
    not_moving: bool = dataclasses.field(default=False)
    depth_bias: float = dataclasses.field(default=0.0)
    unknown_0x70073577: int = dataclasses.field(default=3)
    unknown_0xb0f5e028: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\x17')  # 23 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\nG\x9do')  # 0xa479d6f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.particle_effect))

        data.write(b'2\x17\xdf\xf8')  # 0x3217dff8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_start))

        data.write(b'=\xf5\xa4\x89')  # 0x3df5a489
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x3df5a489))

        data.write(b'\x084\x9b\xd6')  # 0x8349bd6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x08349bd6))

        data.write(b'\xa6\xaa\x06\xd5')  # 0xa6aa06d5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.render_in_foreground))

        data.write(b'g\x14\x02\x1c')  # 0x6714021c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x6714021c))

        data.write(b"\xbe\x93\x19'")  # 0xbe931927
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xbe931927))

        data.write(b'\xe4H\xaa\x81')  # 0xe448aa81
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xe448aa81))

        data.write(b'6\x13\xbc\x90')  # 0x3613bc90
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x3613bc90))

        data.write(b'-\xefp]')  # 0x2def705d
        data.write(b'\x00\x04')  # size
        self.render_override.to_stream(data)

        data.write(b'\xb0(\xdb\x0e')  # 0xb028db0e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.lighting.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xac\xc1\xa0\xaa')  # 0xacc1a0aa
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xacc1a0aa))

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

        data.write(b'R{\x89\xd3')  # 0x527b89d3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.not_moving))

        data.write(b']<r9')  # 0x5d3c7239
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.depth_bias))

        data.write(b'p\x075w')  # 0x70073577
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x70073577))

        data.write(b'\xb0\xf5\xe0(')  # 0xb0f5e028
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xb0f5e028))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            particle_effect=data['particle_effect'],
            auto_start=data['auto_start'],
            unknown_0x3df5a489=data['unknown_0x3df5a489'],
            unknown_0x08349bd6=data['unknown_0x08349bd6'],
            render_in_foreground=data['render_in_foreground'],
            unknown_0x6714021c=data['unknown_0x6714021c'],
            unknown_0xbe931927=data['unknown_0xbe931927'],
            unknown_0xe448aa81=data['unknown_0xe448aa81'],
            unknown_0x3613bc90=data['unknown_0x3613bc90'],
            render_override=enums.RenderOverride.from_json(data['render_override']),
            lighting=LightParameters.from_json(data['lighting']),
            unknown_0xacc1a0aa=data['unknown_0xacc1a0aa'],
            motion_spline_path_loops=data['motion_spline_path_loops'],
            motion_spline_type=SplineType.from_json(data['motion_spline_type']),
            motion_control_spline=Spline.from_json(data['motion_control_spline']),
            motion_spline_duration=data['motion_spline_duration'],
            unknown_0x73e63382=data['unknown_0x73e63382'],
            unknown_0x608ecac5=data['unknown_0x608ecac5'],
            not_moving=data['not_moving'],
            depth_bias=data['depth_bias'],
            unknown_0x70073577=data['unknown_0x70073577'],
            unknown_0xb0f5e028=data['unknown_0xb0f5e028'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'particle_effect': self.particle_effect,
            'auto_start': self.auto_start,
            'unknown_0x3df5a489': self.unknown_0x3df5a489,
            'unknown_0x08349bd6': self.unknown_0x08349bd6,
            'render_in_foreground': self.render_in_foreground,
            'unknown_0x6714021c': self.unknown_0x6714021c,
            'unknown_0xbe931927': self.unknown_0xbe931927,
            'unknown_0xe448aa81': self.unknown_0xe448aa81,
            'unknown_0x3613bc90': self.unknown_0x3613bc90,
            'render_override': self.render_override.to_json(),
            'lighting': self.lighting.to_json(),
            'unknown_0xacc1a0aa': self.unknown_0xacc1a0aa,
            'motion_spline_path_loops': self.motion_spline_path_loops,
            'motion_spline_type': self.motion_spline_type.to_json(),
            'motion_control_spline': self.motion_control_spline.to_json(),
            'motion_spline_duration': self.motion_spline_duration,
            'unknown_0x73e63382': self.unknown_0x73e63382,
            'unknown_0x608ecac5': self.unknown_0x608ecac5,
            'not_moving': self.not_moving,
            'depth_bias': self.depth_bias,
            'unknown_0x70073577': self.unknown_0x70073577,
            'unknown_0xb0f5e028': self.unknown_0xb0f5e028,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_particle_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_auto_start(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x3df5a489(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x08349bd6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_render_in_foreground(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x6714021c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xbe931927(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xe448aa81(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x3613bc90(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_render_override(data: typing.BinaryIO, property_size: int):
    return enums.RenderOverride.from_stream(data)


def _decode_lighting(data: typing.BinaryIO, property_size: int):
    return LightParameters.from_stream(data, property_size)


def _decode_unknown_0xacc1a0aa(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


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


def _decode_not_moving(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_depth_bias(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x70073577(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xb0f5e028(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xa479d6f: ('particle_effect', _decode_particle_effect),
    0x3217dff8: ('auto_start', _decode_auto_start),
    0x3df5a489: ('unknown_0x3df5a489', _decode_unknown_0x3df5a489),
    0x8349bd6: ('unknown_0x08349bd6', _decode_unknown_0x08349bd6),
    0xa6aa06d5: ('render_in_foreground', _decode_render_in_foreground),
    0x6714021c: ('unknown_0x6714021c', _decode_unknown_0x6714021c),
    0xbe931927: ('unknown_0xbe931927', _decode_unknown_0xbe931927),
    0xe448aa81: ('unknown_0xe448aa81', _decode_unknown_0xe448aa81),
    0x3613bc90: ('unknown_0x3613bc90', _decode_unknown_0x3613bc90),
    0x2def705d: ('render_override', _decode_render_override),
    0xb028db0e: ('lighting', _decode_lighting),
    0xacc1a0aa: ('unknown_0xacc1a0aa', _decode_unknown_0xacc1a0aa),
    0x3d7406af: ('motion_spline_path_loops', _decode_motion_spline_path_loops),
    0x493d6a2d: ('motion_spline_type', _decode_motion_spline_type),
    0x27e5f874: ('motion_control_spline', _decode_motion_control_spline),
    0xfd1e2f56: ('motion_spline_duration', _decode_motion_spline_duration),
    0x73e63382: ('unknown_0x73e63382', _decode_unknown_0x73e63382),
    0x608ecac5: ('unknown_0x608ecac5', _decode_unknown_0x608ecac5),
    0x527b89d3: ('not_moving', _decode_not_moving),
    0x5d3c7239: ('depth_bias', _decode_depth_bias),
    0x70073577: ('unknown_0x70073577', _decode_unknown_0x70073577),
    0xb0f5e028: ('unknown_0xb0f5e028', _decode_unknown_0xb0f5e028),
}
