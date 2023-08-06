# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct18 import UnknownStruct18
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct276 import UnknownStruct276
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct32 import UnknownStruct32
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct33 import UnknownStruct33
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class TPND(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    collision_box: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    collision_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    collision_model: AssetId = dataclasses.field(metadata={'asset_types': ['DCLN']}, default=default_asset_id)
    animation: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    tippy_platform_module: UnknownStruct33 = dataclasses.field(default_factory=UnknownStruct33)
    motion_platform_module: UnknownStruct32 = dataclasses.field(default_factory=UnknownStruct32)
    unknown_struct18: UnknownStruct18 = dataclasses.field(default_factory=UnknownStruct18)
    unknown_struct276: UnknownStruct276 = dataclasses.field(default_factory=UnknownStruct276)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'TPND'

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
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf3D\xc0\xb0')  # 0xf344c0b0
        data.write(b'\x00\x0c')  # size
        self.collision_box.to_stream(data)

        data.write(b'.hl*')  # 0x2e686c2a
        data.write(b'\x00\x0c')  # size
        self.collision_offset.to_stream(data)

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc2\x7f\xfa\x8f')  # 0xc27ffa8f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model))

        data.write(b'\x0f\xc9f\xdc')  # 0xfc966dc
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.collision_model))

        data.write(b'\xa3\xd6?D')  # 0xa3d63f44
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf2\xd2\xc8\xe8')  # 0xf2d2c8e8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tippy_platform_module.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x17K]\xc1')  # 0x174b5dc1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_platform_module.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa1\xc6\xd9\xde')  # 0xa1c6d9de
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct18.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\r:\x1c\x85')  # 0xd3a1c85
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct276.to_stream(data)
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
            collision_box=Vector.from_json(data['collision_box']),
            collision_offset=Vector.from_json(data['collision_offset']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            model=data['model'],
            collision_model=data['collision_model'],
            animation=AnimationParameters.from_json(data['animation']),
            tippy_platform_module=UnknownStruct33.from_json(data['tippy_platform_module']),
            motion_platform_module=UnknownStruct32.from_json(data['motion_platform_module']),
            unknown_struct18=UnknownStruct18.from_json(data['unknown_struct18']),
            unknown_struct276=UnknownStruct276.from_json(data['unknown_struct276']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'collision_box': self.collision_box.to_json(),
            'collision_offset': self.collision_offset.to_json(),
            'actor_information': self.actor_information.to_json(),
            'model': self.model,
            'collision_model': self.collision_model,
            'animation': self.animation.to_json(),
            'tippy_platform_module': self.tippy_platform_module.to_json(),
            'motion_platform_module': self.motion_platform_module.to_json(),
            'unknown_struct18': self.unknown_struct18.to_json(),
            'unknown_struct276': self.unknown_struct276.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_collision_box(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_collision_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_collision_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_animation(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_tippy_platform_module(data: typing.BinaryIO, property_size: int):
    return UnknownStruct33.from_stream(data, property_size)


def _decode_motion_platform_module(data: typing.BinaryIO, property_size: int):
    return UnknownStruct32.from_stream(data, property_size)


def _decode_unknown_struct18(data: typing.BinaryIO, property_size: int):
    return UnknownStruct18.from_stream(data, property_size)


def _decode_unknown_struct276(data: typing.BinaryIO, property_size: int):
    return UnknownStruct276.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xf344c0b0: ('collision_box', _decode_collision_box),
    0x2e686c2a: ('collision_offset', _decode_collision_offset),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xc27ffa8f: ('model', _decode_model),
    0xfc966dc: ('collision_model', _decode_collision_model),
    0xa3d63f44: ('animation', _decode_animation),
    0xf2d2c8e8: ('tippy_platform_module', _decode_tippy_platform_module),
    0x174b5dc1: ('motion_platform_module', _decode_motion_platform_module),
    0xa1c6d9de: ('unknown_struct18', _decode_unknown_struct18),
    0xd3a1c85: ('unknown_struct276', _decode_unknown_struct276),
}
