# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.core.Color import Color
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class FogOverlay(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    full_alpha: float = dataclasses.field(default=1.0)
    fade_down_time: float = dataclasses.field(default=1.0)
    fade_up_time: float = dataclasses.field(default=1.0)
    start_faded_out: bool = dataclasses.field(default=False)
    color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    ambient_radius_x: float = dataclasses.field(default=0.5)
    ambient_radius_y: float = dataclasses.field(default=0.20000000298023224)
    ambient_speed: float = dataclasses.field(default=0.10000000149011612)
    ambient_speed_target: float = dataclasses.field(default=0.10000000149011612)
    unknown_0x6a111b96: float = dataclasses.field(default=1.0)
    unknown_0xff226ea3: float = dataclasses.field(default=1.0)
    unknown_0x2190ab0a: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    unknown_0x9f19f0af: float = dataclasses.field(default=0.10000000149011612)
    unknown_0x90c10fe7: float = dataclasses.field(default=1.0)
    unknown_0xd8daff1d: float = dataclasses.field(default=1.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'FOGO'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['FogOverlay.rel']

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
        data.write(b'\x00\x10')  # 16 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'T{(\xd5')  # 0x547b28d5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.full_alpha))

        data.write(b'\xf9w\xcb5')  # 0xf977cb35
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_down_time))

        data.write(b'\r!\xd3H')  # 0xd21d348
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_up_time))

        data.write(b'\xeb%\n\x0b')  # 0xeb250a0b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.start_faded_out))

        data.write(b'7\xc7\xd0\x9d')  # 0x37c7d09d
        data.write(b'\x00\x10')  # size
        self.color.to_stream(data)

        data.write(b'\x1b\x90F\xd6')  # 0x1b9046d6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ambient_radius_x))

        data.write(b'\xd0\xcc\x95s')  # 0xd0cc9573
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ambient_radius_y))

        data.write(b'\xf7k\xcb\xdd')  # 0xf76bcbdd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ambient_speed))

        data.write(b',Lg\x85')  # 0x2c4c6785
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ambient_speed_target))

        data.write(b'j\x11\x1b\x96')  # 0x6a111b96
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6a111b96))

        data.write(b'\xff"n\xa3')  # 0xff226ea3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xff226ea3))

        data.write(b'!\x90\xab\n')  # 0x2190ab0a
        data.write(b'\x00\x0c')  # size
        self.unknown_0x2190ab0a.to_stream(data)

        data.write(b'\x9f\x19\xf0\xaf')  # 0x9f19f0af
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9f19f0af))

        data.write(b'\x90\xc1\x0f\xe7')  # 0x90c10fe7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x90c10fe7))

        data.write(b'\xd8\xda\xff\x1d')  # 0xd8daff1d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd8daff1d))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            full_alpha=data['full_alpha'],
            fade_down_time=data['fade_down_time'],
            fade_up_time=data['fade_up_time'],
            start_faded_out=data['start_faded_out'],
            color=Color.from_json(data['color']),
            ambient_radius_x=data['ambient_radius_x'],
            ambient_radius_y=data['ambient_radius_y'],
            ambient_speed=data['ambient_speed'],
            ambient_speed_target=data['ambient_speed_target'],
            unknown_0x6a111b96=data['unknown_0x6a111b96'],
            unknown_0xff226ea3=data['unknown_0xff226ea3'],
            unknown_0x2190ab0a=Vector.from_json(data['unknown_0x2190ab0a']),
            unknown_0x9f19f0af=data['unknown_0x9f19f0af'],
            unknown_0x90c10fe7=data['unknown_0x90c10fe7'],
            unknown_0xd8daff1d=data['unknown_0xd8daff1d'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'full_alpha': self.full_alpha,
            'fade_down_time': self.fade_down_time,
            'fade_up_time': self.fade_up_time,
            'start_faded_out': self.start_faded_out,
            'color': self.color.to_json(),
            'ambient_radius_x': self.ambient_radius_x,
            'ambient_radius_y': self.ambient_radius_y,
            'ambient_speed': self.ambient_speed,
            'ambient_speed_target': self.ambient_speed_target,
            'unknown_0x6a111b96': self.unknown_0x6a111b96,
            'unknown_0xff226ea3': self.unknown_0xff226ea3,
            'unknown_0x2190ab0a': self.unknown_0x2190ab0a.to_json(),
            'unknown_0x9f19f0af': self.unknown_0x9f19f0af,
            'unknown_0x90c10fe7': self.unknown_0x90c10fe7,
            'unknown_0xd8daff1d': self.unknown_0xd8daff1d,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for FogOverlay.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_full_alpha(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_down_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_up_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_start_faded_out(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_ambient_radius_x(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ambient_radius_y(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ambient_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ambient_speed_target(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6a111b96(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xff226ea3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2190ab0a(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_0x9f19f0af(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x90c10fe7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd8daff1d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x547b28d5: ('full_alpha', _decode_full_alpha),
    0xf977cb35: ('fade_down_time', _decode_fade_down_time),
    0xd21d348: ('fade_up_time', _decode_fade_up_time),
    0xeb250a0b: ('start_faded_out', _decode_start_faded_out),
    0x37c7d09d: ('color', _decode_color),
    0x1b9046d6: ('ambient_radius_x', _decode_ambient_radius_x),
    0xd0cc9573: ('ambient_radius_y', _decode_ambient_radius_y),
    0xf76bcbdd: ('ambient_speed', _decode_ambient_speed),
    0x2c4c6785: ('ambient_speed_target', _decode_ambient_speed_target),
    0x6a111b96: ('unknown_0x6a111b96', _decode_unknown_0x6a111b96),
    0xff226ea3: ('unknown_0xff226ea3', _decode_unknown_0xff226ea3),
    0x2190ab0a: ('unknown_0x2190ab0a', _decode_unknown_0x2190ab0a),
    0x9f19f0af: ('unknown_0x9f19f0af', _decode_unknown_0x9f19f0af),
    0x90c10fe7: ('unknown_0x90c10fe7', _decode_unknown_0x90c10fe7),
    0xd8daff1d: ('unknown_0xd8daff1d', _decode_unknown_0xd8daff1d),
}
