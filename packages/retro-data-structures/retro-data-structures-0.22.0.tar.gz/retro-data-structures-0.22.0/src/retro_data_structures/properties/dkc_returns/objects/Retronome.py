# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class Retronome(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    time_offset: float = dataclasses.field(default=0.0)
    unknown_0x2d458535: bool = dataclasses.field(default=True)
    unknown_0xa598ca16: bool = dataclasses.field(default=False)
    unknown_0xc9c29626: bool = dataclasses.field(default=False)
    unknown_0x4e599427: bool = dataclasses.field(default=False)
    unknown_0xb7329cec: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'RTNM'

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'%9\xdeF')  # 0x2539de46
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.time_offset))

        data.write(b'-E\x855')  # 0x2d458535
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x2d458535))

        data.write(b'\xa5\x98\xca\x16')  # 0xa598ca16
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xa598ca16))

        data.write(b'\xc9\xc2\x96&')  # 0xc9c29626
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xc9c29626))

        data.write(b"NY\x94'")  # 0x4e599427
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x4e599427))

        data.write(b'\xb72\x9c\xec')  # 0xb7329cec
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xb7329cec))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            time_offset=data['time_offset'],
            unknown_0x2d458535=data['unknown_0x2d458535'],
            unknown_0xa598ca16=data['unknown_0xa598ca16'],
            unknown_0xc9c29626=data['unknown_0xc9c29626'],
            unknown_0x4e599427=data['unknown_0x4e599427'],
            unknown_0xb7329cec=data['unknown_0xb7329cec'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'time_offset': self.time_offset,
            'unknown_0x2d458535': self.unknown_0x2d458535,
            'unknown_0xa598ca16': self.unknown_0xa598ca16,
            'unknown_0xc9c29626': self.unknown_0xc9c29626,
            'unknown_0x4e599427': self.unknown_0x4e599427,
            'unknown_0xb7329cec': self.unknown_0xb7329cec,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_time_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2d458535(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xa598ca16(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xc9c29626(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x4e599427(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xb7329cec(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x2539de46: ('time_offset', _decode_time_offset),
    0x2d458535: ('unknown_0x2d458535', _decode_unknown_0x2d458535),
    0xa598ca16: ('unknown_0xa598ca16', _decode_unknown_0xa598ca16),
    0xc9c29626: ('unknown_0xc9c29626', _decode_unknown_0xc9c29626),
    0x4e599427: ('unknown_0x4e599427', _decode_unknown_0x4e599427),
    0xb7329cec: ('unknown_0xb7329cec', _decode_unknown_0xb7329cec),
}
