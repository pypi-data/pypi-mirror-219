# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.dkc_returns.core.Color import Color


@dataclasses.dataclass()
class UnknownStruct20(BaseProperty):
    gradient_start: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    gradient_end: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    font_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    font_geometry_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    unknown_0x045c4906: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x9c403177: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    is_front_end: bool = dataclasses.field(default=False)
    animation1: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    animation2: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unknown_0x7024d89b: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unknown_0x495c75db: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unknown_0x19080ebd: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unknown_0x2070a3fd: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
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

        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\r')  # 13 properties

        data.write(b'\xfb\xb7\xbeE')  # 0xfbb7be45
        data.write(b'\x00\x10')  # size
        self.gradient_start.to_stream(data)

        data.write(b'\x0f\xbc\xe3\xfb')  # 0xfbce3fb
        data.write(b'\x00\x10')  # size
        self.gradient_end.to_stream(data)

        data.write(b'\x84J\xb6\xb0')  # 0x844ab6b0
        data.write(b'\x00\x10')  # size
        self.font_outline_color.to_stream(data)

        data.write(b'\xa6\xe3\x18z')  # 0xa6e3187a
        data.write(b'\x00\x10')  # size
        self.font_geometry_color.to_stream(data)

        data.write(b'\x04\\I\x06')  # 0x45c4906
        data.write(b'\x00\x10')  # size
        self.unknown_0x045c4906.to_stream(data)

        data.write(b'\x9c@1w')  # 0x9c403177
        data.write(b'\x00\x10')  # size
        self.unknown_0x9c403177.to_stream(data)

        data.write(b'\x1fh\xf1\xb7')  # 0x1f68f1b7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_front_end))

        data.write(b')F>6')  # 0x29463e36
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x10>\x93v')  # 0x103e9376
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'p$\xd8\x9b')  # 0x7024d89b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x7024d89b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'I\\u\xdb')  # 0x495c75db
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x495c75db.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x19\x08\x0e\xbd')  # 0x19080ebd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x19080ebd.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b' p\xa3\xfd')  # 0x2070a3fd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x2070a3fd.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            gradient_start=Color.from_json(data['gradient_start']),
            gradient_end=Color.from_json(data['gradient_end']),
            font_outline_color=Color.from_json(data['font_outline_color']),
            font_geometry_color=Color.from_json(data['font_geometry_color']),
            unknown_0x045c4906=Color.from_json(data['unknown_0x045c4906']),
            unknown_0x9c403177=Color.from_json(data['unknown_0x9c403177']),
            is_front_end=data['is_front_end'],
            animation1=AnimationParameters.from_json(data['animation1']),
            animation2=AnimationParameters.from_json(data['animation2']),
            unknown_0x7024d89b=AnimationParameters.from_json(data['unknown_0x7024d89b']),
            unknown_0x495c75db=AnimationParameters.from_json(data['unknown_0x495c75db']),
            unknown_0x19080ebd=AnimationParameters.from_json(data['unknown_0x19080ebd']),
            unknown_0x2070a3fd=AnimationParameters.from_json(data['unknown_0x2070a3fd']),
        )

    def to_json(self) -> dict:
        return {
            'gradient_start': self.gradient_start.to_json(),
            'gradient_end': self.gradient_end.to_json(),
            'font_outline_color': self.font_outline_color.to_json(),
            'font_geometry_color': self.font_geometry_color.to_json(),
            'unknown_0x045c4906': self.unknown_0x045c4906.to_json(),
            'unknown_0x9c403177': self.unknown_0x9c403177.to_json(),
            'is_front_end': self.is_front_end,
            'animation1': self.animation1.to_json(),
            'animation2': self.animation2.to_json(),
            'unknown_0x7024d89b': self.unknown_0x7024d89b.to_json(),
            'unknown_0x495c75db': self.unknown_0x495c75db.to_json(),
            'unknown_0x19080ebd': self.unknown_0x19080ebd.to_json(),
            'unknown_0x2070a3fd': self.unknown_0x2070a3fd.to_json(),
        }


def _decode_gradient_start(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_gradient_end(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_font_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_font_geometry_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x045c4906(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x9c403177(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_is_front_end(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_animation1(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_animation2(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_unknown_0x7024d89b(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_unknown_0x495c75db(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_unknown_0x19080ebd(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_unknown_0x2070a3fd(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xfbb7be45: ('gradient_start', _decode_gradient_start),
    0xfbce3fb: ('gradient_end', _decode_gradient_end),
    0x844ab6b0: ('font_outline_color', _decode_font_outline_color),
    0xa6e3187a: ('font_geometry_color', _decode_font_geometry_color),
    0x45c4906: ('unknown_0x045c4906', _decode_unknown_0x045c4906),
    0x9c403177: ('unknown_0x9c403177', _decode_unknown_0x9c403177),
    0x1f68f1b7: ('is_front_end', _decode_is_front_end),
    0x29463e36: ('animation1', _decode_animation1),
    0x103e9376: ('animation2', _decode_animation2),
    0x7024d89b: ('unknown_0x7024d89b', _decode_unknown_0x7024d89b),
    0x495c75db: ('unknown_0x495c75db', _decode_unknown_0x495c75db),
    0x19080ebd: ('unknown_0x19080ebd', _decode_unknown_0x19080ebd),
    0x2070a3fd: ('unknown_0x2070a3fd', _decode_unknown_0x2070a3fd),
}
