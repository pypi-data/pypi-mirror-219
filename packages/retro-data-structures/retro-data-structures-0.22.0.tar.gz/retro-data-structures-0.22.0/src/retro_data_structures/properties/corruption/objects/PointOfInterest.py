# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.ScannableParameters import ScannableParameters
from retro_data_structures.properties.corruption.core.Vector import Vector


@dataclasses.dataclass()
class PointOfInterest(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    scan_info: ScannableParameters = dataclasses.field(default_factory=ScannableParameters)
    scan_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    look_at_poi: bool = dataclasses.field(default=False)
    scan_offset_local: bool = dataclasses.field(default=True)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'POIN'

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbd\xbe\xc2\x95')  # 0xbdbec295
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scan_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x86<\x16\xe3')  # 0x863c16e3
        data.write(b'\x00\x0c')  # size
        self.scan_offset.to_stream(data)

        data.write(b'\x01\xf9\xc5\xbb')  # 0x1f9c5bb
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.look_at_poi))

        data.write(b'\x915\x1bi')  # 0x91351b69
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.scan_offset_local))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            scan_info=ScannableParameters.from_json(data['scan_info']),
            scan_offset=Vector.from_json(data['scan_offset']),
            look_at_poi=data['look_at_poi'],
            scan_offset_local=data['scan_offset_local'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'scan_info': self.scan_info.to_json(),
            'scan_offset': self.scan_offset.to_json(),
            'look_at_poi': self.look_at_poi,
            'scan_offset_local': self.scan_offset_local,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_scan_info(data: typing.BinaryIO, property_size: int):
    return ScannableParameters.from_stream(data, property_size)


def _decode_scan_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_look_at_poi(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_scan_offset_local(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xbdbec295: ('scan_info', _decode_scan_info),
    0x863c16e3: ('scan_offset', _decode_scan_offset),
    0x1f9c5bb: ('look_at_poi', _decode_look_at_poi),
    0x91351b69: ('scan_offset_local', _decode_scan_offset_local),
}
