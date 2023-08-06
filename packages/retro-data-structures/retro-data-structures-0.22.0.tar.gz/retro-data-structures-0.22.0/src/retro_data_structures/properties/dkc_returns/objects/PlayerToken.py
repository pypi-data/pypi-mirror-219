# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.ScaleSplines import ScaleSplines
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class PlayerToken(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    character_animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unknown_0xa9eb0fc8: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unknown_0x0b30ecae: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unknown_0x7ca5b474: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unknown_0xf9786405: int = dataclasses.field(default=0)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    scale_controls: ScaleSplines = dataclasses.field(default_factory=ScaleSplines)
    scale_splines: ScaleSplines = dataclasses.field(default_factory=ScaleSplines)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'PTOK'

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

        data.write(b'\xc2\x7f\xfa\x8f')  # 0xc27ffa8f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model))

        data.write(b'\xa2D\xc9\xd8')  # 0xa244c9d8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa9\xeb\x0f\xc8')  # 0xa9eb0fc8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xa9eb0fc8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0b0\xec\xae')  # 0xb30ecae
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x0b30ecae.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'|\xa5\xb4t')  # 0x7ca5b474
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x7ca5b474.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf9xd\x05')  # 0xf9786405
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xf9786405))

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'/~\xc0\xa2')  # 0x2f7ec0a2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scale_controls.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'h\x0e\x96\xea')  # 0x680e96ea
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scale_splines.to_stream(data)
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
            model=data['model'],
            character_animation_information=AnimationParameters.from_json(data['character_animation_information']),
            unknown_0xa9eb0fc8=AnimationParameters.from_json(data['unknown_0xa9eb0fc8']),
            unknown_0x0b30ecae=AnimationParameters.from_json(data['unknown_0x0b30ecae']),
            unknown_0x7ca5b474=AnimationParameters.from_json(data['unknown_0x7ca5b474']),
            unknown_0xf9786405=data['unknown_0xf9786405'],
            actor_information=ActorParameters.from_json(data['actor_information']),
            scale_controls=ScaleSplines.from_json(data['scale_controls']),
            scale_splines=ScaleSplines.from_json(data['scale_splines']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'model': self.model,
            'character_animation_information': self.character_animation_information.to_json(),
            'unknown_0xa9eb0fc8': self.unknown_0xa9eb0fc8.to_json(),
            'unknown_0x0b30ecae': self.unknown_0x0b30ecae.to_json(),
            'unknown_0x7ca5b474': self.unknown_0x7ca5b474.to_json(),
            'unknown_0xf9786405': self.unknown_0xf9786405,
            'actor_information': self.actor_information.to_json(),
            'scale_controls': self.scale_controls.to_json(),
            'scale_splines': self.scale_splines.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_character_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_unknown_0xa9eb0fc8(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_unknown_0x0b30ecae(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_unknown_0x7ca5b474(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_unknown_0xf9786405(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_scale_controls(data: typing.BinaryIO, property_size: int):
    return ScaleSplines.from_stream(data, property_size)


def _decode_scale_splines(data: typing.BinaryIO, property_size: int):
    return ScaleSplines.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xc27ffa8f: ('model', _decode_model),
    0xa244c9d8: ('character_animation_information', _decode_character_animation_information),
    0xa9eb0fc8: ('unknown_0xa9eb0fc8', _decode_unknown_0xa9eb0fc8),
    0xb30ecae: ('unknown_0x0b30ecae', _decode_unknown_0x0b30ecae),
    0x7ca5b474: ('unknown_0x7ca5b474', _decode_unknown_0x7ca5b474),
    0xf9786405: ('unknown_0xf9786405', _decode_unknown_0xf9786405),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x2f7ec0a2: ('scale_controls', _decode_scale_controls),
    0x680e96ea: ('scale_splines', _decode_scale_splines),
}
