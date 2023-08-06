# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class AIHint(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    hint_type: int = dataclasses.field(default=0)
    radius: float = dataclasses.field(default=0.0)
    value_parm: float = dataclasses.field(default=0.0)
    value_parm2: float = dataclasses.field(default=0.0)
    value_parm3: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'AIHT'

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb3\x12{q')  # 0xb3127b71
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.hint_type))

        data.write(b'x\xc5\x07\xeb')  # 0x78c507eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.radius))

        data.write(b'\x19\x02\x80\x99')  # 0x19028099
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.value_parm))

        data.write(b',\x93\xaa\xf5')  # 0x2c93aaf5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.value_parm2))

        data.write(b'\xe7\xcfyP')  # 0xe7cf7950
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.value_parm3))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            hint_type=data['hint_type'],
            radius=data['radius'],
            value_parm=data['value_parm'],
            value_parm2=data['value_parm2'],
            value_parm3=data['value_parm3'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'hint_type': self.hint_type,
            'radius': self.radius,
            'value_parm': self.value_parm,
            'value_parm2': self.value_parm2,
            'value_parm3': self.value_parm3,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_hint_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_value_parm(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_value_parm2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_value_parm3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb3127b71: ('hint_type', _decode_hint_type),
    0x78c507eb: ('radius', _decode_radius),
    0x19028099: ('value_parm', _decode_value_parm),
    0x2c93aaf5: ('value_parm2', _decode_value_parm2),
    0xe7cf7950: ('value_parm3', _decode_value_parm3),
}
