# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.PlayerType import PlayerType
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct277 import UnknownStruct277
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class Tutorial(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    actor_parameters: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unknown_struct6: PlayerType = dataclasses.field(default_factory=PlayerType)
    unknown_struct277: UnknownStruct277 = dataclasses.field(default_factory=UnknownStruct277)
    offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    activation_distance: float = dataclasses.field(default=10.0)
    activation_delay: float = dataclasses.field(default=2.0)
    sound_show_tutorial: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    sound_hide_tutorial: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    ignore_player_detection: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'TUTR'

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
        data.write(b'\x00\n')  # 10 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd2\x9c\x03\x1d')  # 0xd29c031d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_parameters.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'V\xab\xb3\xb8')  # 0x56abb3b8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'v\xaamU')  # 0x76aa6d55
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct277.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'FGpd')  # 0x46477064
        data.write(b'\x00\x0c')  # size
        self.offset.to_stream(data)

        data.write(b'\xf9\nO\xe9')  # 0xf90a4fe9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.activation_distance))

        data.write(b'\xe5\x85\xf1f')  # 0xe585f166
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.activation_delay))

        data.write(b'Dc\x07\xa9')  # 0x446307a9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_show_tutorial))

        data.write(b'\x11\xf8E`')  # 0x11f84560
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_hide_tutorial))

        data.write(b'\x14\xce\xff\x80')  # 0x14ceff80
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_player_detection))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            actor_parameters=ActorParameters.from_json(data['actor_parameters']),
            unknown_struct6=PlayerType.from_json(data['unknown_struct6']),
            unknown_struct277=UnknownStruct277.from_json(data['unknown_struct277']),
            offset=Vector.from_json(data['offset']),
            activation_distance=data['activation_distance'],
            activation_delay=data['activation_delay'],
            sound_show_tutorial=data['sound_show_tutorial'],
            sound_hide_tutorial=data['sound_hide_tutorial'],
            ignore_player_detection=data['ignore_player_detection'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'actor_parameters': self.actor_parameters.to_json(),
            'unknown_struct6': self.unknown_struct6.to_json(),
            'unknown_struct277': self.unknown_struct277.to_json(),
            'offset': self.offset.to_json(),
            'activation_distance': self.activation_distance,
            'activation_delay': self.activation_delay,
            'sound_show_tutorial': self.sound_show_tutorial,
            'sound_hide_tutorial': self.sound_hide_tutorial,
            'ignore_player_detection': self.ignore_player_detection,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_actor_parameters(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_unknown_struct6(data: typing.BinaryIO, property_size: int):
    return PlayerType.from_stream(data, property_size)


def _decode_unknown_struct277(data: typing.BinaryIO, property_size: int):
    return UnknownStruct277.from_stream(data, property_size)


def _decode_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_activation_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_activation_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound_show_tutorial(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound_hide_tutorial(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_ignore_player_detection(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xd29c031d: ('actor_parameters', _decode_actor_parameters),
    0x56abb3b8: ('unknown_struct6', _decode_unknown_struct6),
    0x76aa6d55: ('unknown_struct277', _decode_unknown_struct277),
    0x46477064: ('offset', _decode_offset),
    0xf90a4fe9: ('activation_distance', _decode_activation_distance),
    0xe585f166: ('activation_delay', _decode_activation_delay),
    0x446307a9: ('sound_show_tutorial', _decode_sound_show_tutorial),
    0x11f84560: ('sound_hide_tutorial', _decode_sound_hide_tutorial),
    0x14ceff80: ('ignore_player_detection', _decode_ignore_player_detection),
}
