# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.core.Color import Color
from retro_data_structures.properties.echoes.core.Spline import Spline


@dataclasses.dataclass()
class ColorModulate(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    color_a: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    color_b: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    blend_mode: int = dataclasses.field(default=0)
    time_a2_b: float = dataclasses.field(default=1.0)
    time_b2_a: float = dataclasses.field(default=1.0)
    do_reverse: bool = dataclasses.field(default=False)
    reset_target_when_done: bool = dataclasses.field(default=False)
    depth_compare: bool = dataclasses.field(default=True)
    depth_update: bool = dataclasses.field(default=True)
    depth_backwards: bool = dataclasses.field(default=False)
    auto_start: bool = dataclasses.field(default=False)
    update_time: bool = dataclasses.field(default=True)
    loop_forever: bool = dataclasses.field(default=False)
    external_time: bool = dataclasses.field(default=False)
    copy_model_color_to_color_a: bool = dataclasses.field(default=False)
    control_spline: Spline = dataclasses.field(default_factory=Spline)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'CLRM'

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
        data.write(b'\x00\x11')  # 17 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd6\xa3\xd2o')  # 0xd6a3d26f
        data.write(b'\x00\x10')  # size
        self.color_a.to_stream(data)

        data.write(b'P7\xa0\xc1')  # 0x5037a0c1
        data.write(b'\x00\x10')  # size
        self.color_b.to_stream(data)

        data.write(b'\x94\xf06\\')  # 0x94f0365c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.blend_mode))

        data.write(b'\x1a\xfa\\H')  # 0x1afa5c48
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.time_a2_b))

        data.write(b'\x12\xe1)\x05')  # 0x12e12905
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.time_b2_a))

        data.write(b'\xce\xc5$K')  # 0xcec5244b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.do_reverse))

        data.write(b'\x81\xfc\x97\x9c')  # 0x81fc979c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.reset_target_when_done))

        data.write(b'\x94\xc0\x1b\x0c')  # 0x94c01b0c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.depth_compare))

        data.write(b'\xae\xd2ZQ')  # 0xaed25a51
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.depth_update))

        data.write(b'5\xdcC\xd0')  # 0x35dc43d0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.depth_backwards))

        data.write(b'2\x17\xdf\xf8')  # 0x3217dff8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_start))

        data.write(b':\x7fY\xf7')  # 0x3a7f59f7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.update_time))

        data.write(b'\x08\xbbs\xc5')  # 0x8bb73c5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.loop_forever))

        data.write(b'~7\x9a\xe8')  # 0x7e379ae8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.external_time))

        data.write(b't\x08\x1e\x94')  # 0x74081e94
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.copy_model_color_to_color_a))

        data.write(b'\x15V\x7f\xe7')  # 0x15567fe7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.control_spline.to_stream(data)
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
            color_a=Color.from_json(data['color_a']),
            color_b=Color.from_json(data['color_b']),
            blend_mode=data['blend_mode'],
            time_a2_b=data['time_a2_b'],
            time_b2_a=data['time_b2_a'],
            do_reverse=data['do_reverse'],
            reset_target_when_done=data['reset_target_when_done'],
            depth_compare=data['depth_compare'],
            depth_update=data['depth_update'],
            depth_backwards=data['depth_backwards'],
            auto_start=data['auto_start'],
            update_time=data['update_time'],
            loop_forever=data['loop_forever'],
            external_time=data['external_time'],
            copy_model_color_to_color_a=data['copy_model_color_to_color_a'],
            control_spline=Spline.from_json(data['control_spline']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'color_a': self.color_a.to_json(),
            'color_b': self.color_b.to_json(),
            'blend_mode': self.blend_mode,
            'time_a2_b': self.time_a2_b,
            'time_b2_a': self.time_b2_a,
            'do_reverse': self.do_reverse,
            'reset_target_when_done': self.reset_target_when_done,
            'depth_compare': self.depth_compare,
            'depth_update': self.depth_update,
            'depth_backwards': self.depth_backwards,
            'auto_start': self.auto_start,
            'update_time': self.update_time,
            'loop_forever': self.loop_forever,
            'external_time': self.external_time,
            'copy_model_color_to_color_a': self.copy_model_color_to_color_a,
            'control_spline': self.control_spline.to_json(),
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
                    f"Error finding dependencies for ColorModulate.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_color_a(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_color_b(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_blend_mode(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_time_a2_b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_time_b2_a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_do_reverse(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_reset_target_when_done(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_depth_compare(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_depth_update(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_depth_backwards(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_auto_start(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_update_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_loop_forever(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_external_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_copy_model_color_to_color_a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xd6a3d26f: ('color_a', _decode_color_a),
    0x5037a0c1: ('color_b', _decode_color_b),
    0x94f0365c: ('blend_mode', _decode_blend_mode),
    0x1afa5c48: ('time_a2_b', _decode_time_a2_b),
    0x12e12905: ('time_b2_a', _decode_time_b2_a),
    0xcec5244b: ('do_reverse', _decode_do_reverse),
    0x81fc979c: ('reset_target_when_done', _decode_reset_target_when_done),
    0x94c01b0c: ('depth_compare', _decode_depth_compare),
    0xaed25a51: ('depth_update', _decode_depth_update),
    0x35dc43d0: ('depth_backwards', _decode_depth_backwards),
    0x3217dff8: ('auto_start', _decode_auto_start),
    0x3a7f59f7: ('update_time', _decode_update_time),
    0x8bb73c5: ('loop_forever', _decode_loop_forever),
    0x7e379ae8: ('external_time', _decode_external_time),
    0x74081e94: ('copy_model_color_to_color_a', _decode_copy_model_color_to_color_a),
    0x15567fe7: ('control_spline', _decode_control_spline),
}
