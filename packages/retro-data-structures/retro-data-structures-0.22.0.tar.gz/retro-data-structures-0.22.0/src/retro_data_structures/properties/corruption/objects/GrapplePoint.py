# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.GrappleData import GrappleData
from retro_data_structures.properties.corruption.archetypes.GrappleInfo import GrappleInfo
from retro_data_structures.properties.corruption.core.Color import Color


@dataclasses.dataclass()
class GrapplePoint(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    grapple_info: GrappleInfo = dataclasses.field(default_factory=GrappleInfo)
    grapple_data: GrappleData = dataclasses.field(default_factory=GrappleData)
    unknown_0x01b1315c: bool = dataclasses.field(default=False)
    unknown_0xf6b3c17f: bool = dataclasses.field(default=False)
    grapple_effect_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    grapple_effect_stripe_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    unknown_0x6371cdcf: bool = dataclasses.field(default=False)
    unknown_0xa80b5f61: float = dataclasses.field(default=0.5)
    unknown_0x4789411b: float = dataclasses.field(default=1.0)
    unknown_0x6204350c: float = dataclasses.field(default=0.5)
    unknown_0xd23b2f30: float = dataclasses.field(default=1.0)
    unknown_0x02b1fa08: bool = dataclasses.field(default=False)
    solid_outline: bool = dataclasses.field(default=False)
    unknown_0x5e139bc2: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'GRAP'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_ScriptGrapplePoint.rso']

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
        data.write(b'\x00\x0f')  # 15 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'j(r\xd8')  # 0x6a2872d8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.grapple_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf6\t\xc67')  # 0xf609c637
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.grapple_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x01\xb11\\')  # 0x1b1315c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x01b1315c))

        data.write(b'\xf6\xb3\xc1\x7f')  # 0xf6b3c17f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xf6b3c17f))

        data.write(b"\xc6\x86\x93'")  # 0xc6869327
        data.write(b'\x00\x10')  # size
        self.grapple_effect_outline_color.to_stream(data)

        data.write(b'?\xa8\x05\x92')  # 0x3fa80592
        data.write(b'\x00\x10')  # size
        self.grapple_effect_stripe_color.to_stream(data)

        data.write(b'cq\xcd\xcf')  # 0x6371cdcf
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x6371cdcf))

        data.write(b'\xa8\x0b_a')  # 0xa80b5f61
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa80b5f61))

        data.write(b'G\x89A\x1b')  # 0x4789411b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4789411b))

        data.write(b'b\x045\x0c')  # 0x6204350c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6204350c))

        data.write(b'\xd2;/0')  # 0xd23b2f30
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd23b2f30))

        data.write(b'\x02\xb1\xfa\x08')  # 0x2b1fa08
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x02b1fa08))

        data.write(b'\x96e%\xf0')  # 0x966525f0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.solid_outline))

        data.write(b'^\x13\x9b\xc2')  # 0x5e139bc2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x5e139bc2))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            grapple_info=GrappleInfo.from_json(data['grapple_info']),
            grapple_data=GrappleData.from_json(data['grapple_data']),
            unknown_0x01b1315c=data['unknown_0x01b1315c'],
            unknown_0xf6b3c17f=data['unknown_0xf6b3c17f'],
            grapple_effect_outline_color=Color.from_json(data['grapple_effect_outline_color']),
            grapple_effect_stripe_color=Color.from_json(data['grapple_effect_stripe_color']),
            unknown_0x6371cdcf=data['unknown_0x6371cdcf'],
            unknown_0xa80b5f61=data['unknown_0xa80b5f61'],
            unknown_0x4789411b=data['unknown_0x4789411b'],
            unknown_0x6204350c=data['unknown_0x6204350c'],
            unknown_0xd23b2f30=data['unknown_0xd23b2f30'],
            unknown_0x02b1fa08=data['unknown_0x02b1fa08'],
            solid_outline=data['solid_outline'],
            unknown_0x5e139bc2=data['unknown_0x5e139bc2'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'grapple_info': self.grapple_info.to_json(),
            'grapple_data': self.grapple_data.to_json(),
            'unknown_0x01b1315c': self.unknown_0x01b1315c,
            'unknown_0xf6b3c17f': self.unknown_0xf6b3c17f,
            'grapple_effect_outline_color': self.grapple_effect_outline_color.to_json(),
            'grapple_effect_stripe_color': self.grapple_effect_stripe_color.to_json(),
            'unknown_0x6371cdcf': self.unknown_0x6371cdcf,
            'unknown_0xa80b5f61': self.unknown_0xa80b5f61,
            'unknown_0x4789411b': self.unknown_0x4789411b,
            'unknown_0x6204350c': self.unknown_0x6204350c,
            'unknown_0xd23b2f30': self.unknown_0xd23b2f30,
            'unknown_0x02b1fa08': self.unknown_0x02b1fa08,
            'solid_outline': self.solid_outline,
            'unknown_0x5e139bc2': self.unknown_0x5e139bc2,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_grapple_info(data: typing.BinaryIO, property_size: int):
    return GrappleInfo.from_stream(data, property_size)


def _decode_grapple_data(data: typing.BinaryIO, property_size: int):
    return GrappleData.from_stream(data, property_size)


def _decode_unknown_0x01b1315c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xf6b3c17f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_grapple_effect_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_grapple_effect_stripe_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x6371cdcf(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xa80b5f61(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4789411b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6204350c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd23b2f30(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x02b1fa08(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_solid_outline(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x5e139bc2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x6a2872d8: ('grapple_info', _decode_grapple_info),
    0xf609c637: ('grapple_data', _decode_grapple_data),
    0x1b1315c: ('unknown_0x01b1315c', _decode_unknown_0x01b1315c),
    0xf6b3c17f: ('unknown_0xf6b3c17f', _decode_unknown_0xf6b3c17f),
    0xc6869327: ('grapple_effect_outline_color', _decode_grapple_effect_outline_color),
    0x3fa80592: ('grapple_effect_stripe_color', _decode_grapple_effect_stripe_color),
    0x6371cdcf: ('unknown_0x6371cdcf', _decode_unknown_0x6371cdcf),
    0xa80b5f61: ('unknown_0xa80b5f61', _decode_unknown_0xa80b5f61),
    0x4789411b: ('unknown_0x4789411b', _decode_unknown_0x4789411b),
    0x6204350c: ('unknown_0x6204350c', _decode_unknown_0x6204350c),
    0xd23b2f30: ('unknown_0xd23b2f30', _decode_unknown_0xd23b2f30),
    0x2b1fa08: ('unknown_0x02b1fa08', _decode_unknown_0x02b1fa08),
    0x966525f0: ('solid_outline', _decode_solid_outline),
    0x5e139bc2: ('unknown_0x5e139bc2', _decode_unknown_0x5e139bc2),
}
