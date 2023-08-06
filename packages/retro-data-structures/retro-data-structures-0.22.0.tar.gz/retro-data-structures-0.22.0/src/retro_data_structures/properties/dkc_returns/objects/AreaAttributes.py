# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class AreaAttributes(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    need_sky: bool = dataclasses.field(default=False)
    environment_group_sound: int = dataclasses.field(default=0)
    normal_lighting: float = dataclasses.field(default=1.0)
    override_sky: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    use_override_sky: bool = dataclasses.field(default=True)
    unknown: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'REAA'

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

        data.write(b'\x95\xd4\xbe\xe7')  # 0x95d4bee7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.need_sky))

        data.write(b'V&>5')  # 0x56263e35
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.environment_group_sound))

        data.write(b'\xba_\x80\x1e')  # 0xba5f801e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.normal_lighting))

        data.write(b'\xd2\x08\xc9\xfa')  # 0xd208c9fa
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.override_sky))

        data.write(b')DS\x02')  # 0x29445302
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_override_sky))

        data.write(b'\xe3Bb\x06')  # 0xe3426206
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            need_sky=data['need_sky'],
            environment_group_sound=data['environment_group_sound'],
            normal_lighting=data['normal_lighting'],
            override_sky=data['override_sky'],
            use_override_sky=data['use_override_sky'],
            unknown=data['unknown'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'need_sky': self.need_sky,
            'environment_group_sound': self.environment_group_sound,
            'normal_lighting': self.normal_lighting,
            'override_sky': self.override_sky,
            'use_override_sky': self.use_override_sky,
            'unknown': self.unknown,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_need_sky(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_environment_group_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_normal_lighting(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_override_sky(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_use_override_sky(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x95d4bee7: ('need_sky', _decode_need_sky),
    0x56263e35: ('environment_group_sound', _decode_environment_group_sound),
    0xba5f801e: ('normal_lighting', _decode_normal_lighting),
    0xd208c9fa: ('override_sky', _decode_override_sky),
    0x29445302: ('use_override_sky', _decode_use_override_sky),
    0xe3426206: ('unknown', _decode_unknown),
}
