# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class ActorMorph(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    unknown_0xc60575f5: float = dataclasses.field(default=0.5)
    unknown_0xe9fe0baa: float = dataclasses.field(default=0.5)
    unknown_0x8e79a0fb: float = dataclasses.field(default=0.10000000149011612)
    unknown_0xa182dea4: float = dataclasses.field(default=0.10000000149011612)
    key_points: str = dataclasses.field(default='')
    unknown_0x8bd0e337: float = dataclasses.field(default=1.0)
    unknown_0x39427691: bool = dataclasses.field(default=True)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'AMOR'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_ScriptActorMorph.rso']

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6\x05u\xf5')  # 0xc60575f5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc60575f5))

        data.write(b'\xe9\xfe\x0b\xaa')  # 0xe9fe0baa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe9fe0baa))

        data.write(b'\x8ey\xa0\xfb')  # 0x8e79a0fb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8e79a0fb))

        data.write(b'\xa1\x82\xde\xa4')  # 0xa182dea4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa182dea4))

        data.write(b'\x95\xde\xbd\x1b')  # 0x95debd1b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.key_points.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8b\xd0\xe37')  # 0x8bd0e337
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8bd0e337))

        data.write(b'9Bv\x91')  # 0x39427691
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x39427691))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            unknown_0xc60575f5=data['unknown_0xc60575f5'],
            unknown_0xe9fe0baa=data['unknown_0xe9fe0baa'],
            unknown_0x8e79a0fb=data['unknown_0x8e79a0fb'],
            unknown_0xa182dea4=data['unknown_0xa182dea4'],
            key_points=data['key_points'],
            unknown_0x8bd0e337=data['unknown_0x8bd0e337'],
            unknown_0x39427691=data['unknown_0x39427691'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'unknown_0xc60575f5': self.unknown_0xc60575f5,
            'unknown_0xe9fe0baa': self.unknown_0xe9fe0baa,
            'unknown_0x8e79a0fb': self.unknown_0x8e79a0fb,
            'unknown_0xa182dea4': self.unknown_0xa182dea4,
            'key_points': self.key_points,
            'unknown_0x8bd0e337': self.unknown_0x8bd0e337,
            'unknown_0x39427691': self.unknown_0x39427691,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_unknown_0xc60575f5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe9fe0baa(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8e79a0fb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa182dea4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_key_points(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0x8bd0e337(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x39427691(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xc60575f5: ('unknown_0xc60575f5', _decode_unknown_0xc60575f5),
    0xe9fe0baa: ('unknown_0xe9fe0baa', _decode_unknown_0xe9fe0baa),
    0x8e79a0fb: ('unknown_0x8e79a0fb', _decode_unknown_0x8e79a0fb),
    0xa182dea4: ('unknown_0xa182dea4', _decode_unknown_0xa182dea4),
    0x95debd1b: ('key_points', _decode_key_points),
    0x8bd0e337: ('unknown_0x8bd0e337', _decode_unknown_0x8bd0e337),
    0x39427691: ('unknown_0x39427691', _decode_unknown_0x39427691),
}
