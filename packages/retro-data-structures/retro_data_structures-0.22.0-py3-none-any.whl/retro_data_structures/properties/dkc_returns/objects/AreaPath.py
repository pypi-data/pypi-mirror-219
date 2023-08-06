# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.dkc_returns.archetypes.AreaPathStructA import AreaPathStructA
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class AreaPath(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    character_animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    cmdl: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    type: enums.Type = dataclasses.field(default=enums.Type.Unknown1)
    padlock_path: bool = dataclasses.field(default=False)
    unknown_0xd626b1d8: bool = dataclasses.field(default=True)
    unknown_0x45bb081b: bool = dataclasses.field(default=False)
    draw_time: float = dataclasses.field(default=0.5)
    walk_time: float = dataclasses.field(default=0.5)
    path: Spline = dataclasses.field(default_factory=Spline)
    area_path_struct_a: AreaPathStructA = dataclasses.field(default_factory=AreaPathStructA)
    reveal_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    reveal_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'ARPA'

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

        data.write(b'\xdeW\t\xd9')  # 0xde5709d9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl))

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'GK\xcc\xe3')  # 0x474bcce3
        data.write(b'\x00\x04')  # size
        self.type.to_stream(data)

        data.write(b'ua\xf8\xf7')  # 0x7561f8f7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.padlock_path))

        data.write(b'\xd6&\xb1\xd8')  # 0xd626b1d8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xd626b1d8))

        data.write(b'E\xbb\x08\x1b')  # 0x45bb081b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x45bb081b))

        data.write(b'\x9d\xc4;\x9c')  # 0x9dc43b9c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.draw_time))

        data.write(b'\x19\x89\xe2\xe5')  # 0x1989e2e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.walk_time))

        data.write(b'\xfa\x0e\xed\x84')  # 0xfa0eed84
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.path.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x91\xfa{\x19')  # 0x91fa7b19
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.area_path_struct_a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1b2\xdcP')  # 0x1b32dc50
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.reveal_effect))

        data.write(b'|d,\x9c')  # 0x7c642c9c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.reveal_sound))

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
            cmdl=data['cmdl'],
            actor_information=ActorParameters.from_json(data['actor_information']),
            type=enums.Type.from_json(data['type']),
            padlock_path=data['padlock_path'],
            unknown_0xd626b1d8=data['unknown_0xd626b1d8'],
            unknown_0x45bb081b=data['unknown_0x45bb081b'],
            draw_time=data['draw_time'],
            walk_time=data['walk_time'],
            path=Spline.from_json(data['path']),
            area_path_struct_a=AreaPathStructA.from_json(data['area_path_struct_a']),
            reveal_effect=data['reveal_effect'],
            reveal_sound=data['reveal_sound'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'model': self.model,
            'character_animation_information': self.character_animation_information.to_json(),
            'cmdl': self.cmdl,
            'actor_information': self.actor_information.to_json(),
            'type': self.type.to_json(),
            'padlock_path': self.padlock_path,
            'unknown_0xd626b1d8': self.unknown_0xd626b1d8,
            'unknown_0x45bb081b': self.unknown_0x45bb081b,
            'draw_time': self.draw_time,
            'walk_time': self.walk_time,
            'path': self.path.to_json(),
            'area_path_struct_a': self.area_path_struct_a.to_json(),
            'reveal_effect': self.reveal_effect,
            'reveal_sound': self.reveal_sound,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_character_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_cmdl(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_type(data: typing.BinaryIO, property_size: int):
    return enums.Type.from_stream(data)


def _decode_padlock_path(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xd626b1d8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x45bb081b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_draw_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_walk_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_path(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_area_path_struct_a(data: typing.BinaryIO, property_size: int):
    return AreaPathStructA.from_stream(data, property_size)


def _decode_reveal_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_reveal_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xc27ffa8f: ('model', _decode_model),
    0xa244c9d8: ('character_animation_information', _decode_character_animation_information),
    0xde5709d9: ('cmdl', _decode_cmdl),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x474bcce3: ('type', _decode_type),
    0x7561f8f7: ('padlock_path', _decode_padlock_path),
    0xd626b1d8: ('unknown_0xd626b1d8', _decode_unknown_0xd626b1d8),
    0x45bb081b: ('unknown_0x45bb081b', _decode_unknown_0x45bb081b),
    0x9dc43b9c: ('draw_time', _decode_draw_time),
    0x1989e2e5: ('walk_time', _decode_walk_time),
    0xfa0eed84: ('path', _decode_path),
    0x91fa7b19: ('area_path_struct_a', _decode_area_path_struct_a),
    0x1b32dc50: ('reveal_effect', _decode_reveal_effect),
    0x7c642c9c: ('reveal_sound', _decode_reveal_sound),
}
