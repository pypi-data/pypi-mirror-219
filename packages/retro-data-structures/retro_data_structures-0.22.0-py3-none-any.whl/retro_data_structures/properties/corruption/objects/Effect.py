# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.LightParameters import LightParameters
from retro_data_structures.properties.corruption.archetypes.SplineType import SplineType
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class Effect(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    particle_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART', 'ELSC', 'SPSC', 'SWHC']}, default=default_asset_id)
    auto_start: bool = dataclasses.field(default=True)
    unknown_0x3df5a489: bool = dataclasses.field(default=False)
    unknown_0x08349bd6: bool = dataclasses.field(default=False)
    unknown_0xee538174: bool = dataclasses.field(default=False)
    unknown_0xa94b0efd: float = dataclasses.field(default=5.0)
    unknown_0x93756968: float = dataclasses.field(default=0.5)
    unknown_0x0b94597d: float = dataclasses.field(default=0.20000000298023224)
    unknown_0xd0e8a496: float = dataclasses.field(default=0.10000000149011612)
    unknown_0xa8bb6c61: bool = dataclasses.field(default=False)
    unknown_0x7589d549: float = dataclasses.field(default=20.0)
    unknown_0xa7d7d767: float = dataclasses.field(default=30.0)
    unknown_0xfe69615c: float = dataclasses.field(default=0.0)
    unknown_0x84368d03: float = dataclasses.field(default=5.0)
    unknown_0xa559c066: float = dataclasses.field(default=10.0)
    visible_in_normal: bool = dataclasses.field(default=True)
    visible_in_x_ray: bool = dataclasses.field(default=True)
    unknown_0x6714021c: bool = dataclasses.field(default=True)
    unknown_0xbe931927: bool = dataclasses.field(default=False)
    render_order: int = dataclasses.field(default=0)
    lighting: LightParameters = dataclasses.field(default_factory=LightParameters)
    unknown_0x4d55f7d4: bool = dataclasses.field(default=False)
    motion_spline_path_loops: bool = dataclasses.field(default=False)
    motion_spline_type: SplineType = dataclasses.field(default_factory=SplineType)
    motion_control_spline: Spline = dataclasses.field(default_factory=Spline)
    motion_spline_duration: float = dataclasses.field(default=10.0)
    unknown_0x73e63382: bool = dataclasses.field(default=False)
    unknown_0x608ecac5: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

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
        data.write(b'\x00\x1d')  # 29 properties

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

        data.write(b'\x846\x8d\x03')  # 0x84368d03
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x84368d03))

        data.write(b'\xa5Y\xc0f')  # 0xa559c066
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa559c066))

        data.write(b'6\x8b\xf2E')  # 0x368bf245
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.visible_in_normal))

        data.write(b'\xef\xff\xa3\xbe')  # 0xefffa3be
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.visible_in_x_ray))

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

        data.write(b'MU\xf7\xd4')  # 0x4d55f7d4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x4d55f7d4))

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
            auto_start=data['auto_start'],
            unknown_0x3df5a489=data['unknown_0x3df5a489'],
            unknown_0x08349bd6=data['unknown_0x08349bd6'],
            unknown_0xee538174=data['unknown_0xee538174'],
            unknown_0xa94b0efd=data['unknown_0xa94b0efd'],
            unknown_0x93756968=data['unknown_0x93756968'],
            unknown_0x0b94597d=data['unknown_0x0b94597d'],
            unknown_0xd0e8a496=data['unknown_0xd0e8a496'],
            unknown_0xa8bb6c61=data['unknown_0xa8bb6c61'],
            unknown_0x7589d549=data['unknown_0x7589d549'],
            unknown_0xa7d7d767=data['unknown_0xa7d7d767'],
            unknown_0xfe69615c=data['unknown_0xfe69615c'],
            unknown_0x84368d03=data['unknown_0x84368d03'],
            unknown_0xa559c066=data['unknown_0xa559c066'],
            visible_in_normal=data['visible_in_normal'],
            visible_in_x_ray=data['visible_in_x_ray'],
            unknown_0x6714021c=data['unknown_0x6714021c'],
            unknown_0xbe931927=data['unknown_0xbe931927'],
            render_order=data['render_order'],
            lighting=LightParameters.from_json(data['lighting']),
            unknown_0x4d55f7d4=data['unknown_0x4d55f7d4'],
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
            'auto_start': self.auto_start,
            'unknown_0x3df5a489': self.unknown_0x3df5a489,
            'unknown_0x08349bd6': self.unknown_0x08349bd6,
            'unknown_0xee538174': self.unknown_0xee538174,
            'unknown_0xa94b0efd': self.unknown_0xa94b0efd,
            'unknown_0x93756968': self.unknown_0x93756968,
            'unknown_0x0b94597d': self.unknown_0x0b94597d,
            'unknown_0xd0e8a496': self.unknown_0xd0e8a496,
            'unknown_0xa8bb6c61': self.unknown_0xa8bb6c61,
            'unknown_0x7589d549': self.unknown_0x7589d549,
            'unknown_0xa7d7d767': self.unknown_0xa7d7d767,
            'unknown_0xfe69615c': self.unknown_0xfe69615c,
            'unknown_0x84368d03': self.unknown_0x84368d03,
            'unknown_0xa559c066': self.unknown_0xa559c066,
            'visible_in_normal': self.visible_in_normal,
            'visible_in_x_ray': self.visible_in_x_ray,
            'unknown_0x6714021c': self.unknown_0x6714021c,
            'unknown_0xbe931927': self.unknown_0xbe931927,
            'render_order': self.render_order,
            'lighting': self.lighting.to_json(),
            'unknown_0x4d55f7d4': self.unknown_0x4d55f7d4,
            'motion_spline_path_loops': self.motion_spline_path_loops,
            'motion_spline_type': self.motion_spline_type.to_json(),
            'motion_control_spline': self.motion_control_spline.to_json(),
            'motion_spline_duration': self.motion_spline_duration,
            'unknown_0x73e63382': self.unknown_0x73e63382,
            'unknown_0x608ecac5': self.unknown_0x608ecac5,
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


def _decode_unknown_0x84368d03(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa559c066(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_visible_in_normal(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_visible_in_x_ray(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x6714021c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xbe931927(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_render_order(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_lighting(data: typing.BinaryIO, property_size: int):
    return LightParameters.from_stream(data, property_size)


def _decode_unknown_0x4d55f7d4(data: typing.BinaryIO, property_size: int):
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


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xa479d6f: ('particle_effect', _decode_particle_effect),
    0x3217dff8: ('auto_start', _decode_auto_start),
    0x3df5a489: ('unknown_0x3df5a489', _decode_unknown_0x3df5a489),
    0x8349bd6: ('unknown_0x08349bd6', _decode_unknown_0x08349bd6),
    0xee538174: ('unknown_0xee538174', _decode_unknown_0xee538174),
    0xa94b0efd: ('unknown_0xa94b0efd', _decode_unknown_0xa94b0efd),
    0x93756968: ('unknown_0x93756968', _decode_unknown_0x93756968),
    0xb94597d: ('unknown_0x0b94597d', _decode_unknown_0x0b94597d),
    0xd0e8a496: ('unknown_0xd0e8a496', _decode_unknown_0xd0e8a496),
    0xa8bb6c61: ('unknown_0xa8bb6c61', _decode_unknown_0xa8bb6c61),
    0x7589d549: ('unknown_0x7589d549', _decode_unknown_0x7589d549),
    0xa7d7d767: ('unknown_0xa7d7d767', _decode_unknown_0xa7d7d767),
    0xfe69615c: ('unknown_0xfe69615c', _decode_unknown_0xfe69615c),
    0x84368d03: ('unknown_0x84368d03', _decode_unknown_0x84368d03),
    0xa559c066: ('unknown_0xa559c066', _decode_unknown_0xa559c066),
    0x368bf245: ('visible_in_normal', _decode_visible_in_normal),
    0xefffa3be: ('visible_in_x_ray', _decode_visible_in_x_ray),
    0x6714021c: ('unknown_0x6714021c', _decode_unknown_0x6714021c),
    0xbe931927: ('unknown_0xbe931927', _decode_unknown_0xbe931927),
    0x2fa4e5d7: ('render_order', _decode_render_order),
    0xb028db0e: ('lighting', _decode_lighting),
    0x4d55f7d4: ('unknown_0x4d55f7d4', _decode_unknown_0x4d55f7d4),
    0x3d7406af: ('motion_spline_path_loops', _decode_motion_spline_path_loops),
    0x493d6a2d: ('motion_spline_type', _decode_motion_spline_type),
    0x27e5f874: ('motion_control_spline', _decode_motion_control_spline),
    0xfd1e2f56: ('motion_spline_duration', _decode_motion_spline_duration),
    0x73e63382: ('unknown_0x73e63382', _decode_unknown_0x73e63382),
    0x608ecac5: ('unknown_0x608ecac5', _decode_unknown_0x608ecac5),
}
