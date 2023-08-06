# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class ContextSensitiveActivator(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    player_distance: float = dataclasses.field(default=5.0)
    face_angle: float = dataclasses.field(default=90.0)
    screen_center_distance: float = dataclasses.field(default=20.0)
    unknown: bool = dataclasses.field(default=False)
    reticule_type: enums.ReticuleType = dataclasses.field(default=enums.ReticuleType.Unknown1)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'CSAT'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_ScriptContextSensitiveActivator.rso']

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

        data.write(b'?]\x07!')  # 0x3f5d0721
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.player_distance))

        data.write(b'\x1eJ3\xdc')  # 0x1e4a33dc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.face_angle))

        data.write(b'\xe7\xe3\xe1\x9f')  # 0xe7e3e19f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.screen_center_distance))

        data.write(b'\xf2\xe2?0')  # 0xf2e23f30
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

        data.write(b'\x87\xa1\xc2\x04')  # 0x87a1c204
        data.write(b'\x00\x04')  # size
        self.reticule_type.to_stream(data)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            player_distance=data['player_distance'],
            face_angle=data['face_angle'],
            screen_center_distance=data['screen_center_distance'],
            unknown=data['unknown'],
            reticule_type=enums.ReticuleType.from_json(data['reticule_type']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'player_distance': self.player_distance,
            'face_angle': self.face_angle,
            'screen_center_distance': self.screen_center_distance,
            'unknown': self.unknown,
            'reticule_type': self.reticule_type.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_player_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_face_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_screen_center_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_reticule_type(data: typing.BinaryIO, property_size: int):
    return enums.ReticuleType.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x3f5d0721: ('player_distance', _decode_player_distance),
    0x1e4a33dc: ('face_angle', _decode_face_angle),
    0xe7e3e19f: ('screen_center_distance', _decode_screen_center_distance),
    0xf2e23f30: ('unknown', _decode_unknown),
    0x87a1c204: ('reticule_type', _decode_reticule_type),
}
