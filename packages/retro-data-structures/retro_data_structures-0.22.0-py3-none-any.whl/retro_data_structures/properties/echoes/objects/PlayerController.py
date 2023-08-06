# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class PlayerController(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    unknown_0xe71de331: int = dataclasses.field(default=0)
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    proxy_type: int = dataclasses.field(default=0)
    player_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=1.5))
    initial_state: int = dataclasses.field(default=0)
    player_visor: int = dataclasses.field(default=0)
    unknown_0xf09c2b4b: float = dataclasses.field(default=0.0)
    unknown_0x760859e5: float = dataclasses.field(default=0.0)
    unknown_0xbd548a40: float = dataclasses.field(default=0.0)
    rotation_for_type3: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    unknown_0x70bc90a6: str = dataclasses.field(default='')

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'PLCT'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['ScriptPlayerProxy.rel']

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
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe7\x1d\xe31')  # 0xe71de331
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xe71de331))

        data.write(b'\xc2\x7f\xfa\x8f')  # 0xc27ffa8f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.model))

        data.write(b'\xe2_\xb0\x8c')  # 0xe25fb08c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcaV\xa1\x8a')  # 0xca56a18a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.proxy_type))

        data.write(b'\x1d\x8b\x93?')  # 0x1d8b933f
        data.write(b'\x00\x0c')  # size
        self.player_offset.to_stream(data)

        data.write(b'\xcbu3\x19')  # 0xcb753319
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.initial_state))

        data.write(b'\xd9\xc0\x9c\xf7')  # 0xd9c09cf7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.player_visor))

        data.write(b'\xf0\x9c+K')  # 0xf09c2b4b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf09c2b4b))

        data.write(b'v\x08Y\xe5')  # 0x760859e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x760859e5))

        data.write(b'\xbdT\x8a@')  # 0xbd548a40
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbd548a40))

        data.write(b'\xc0\x12\xf1\x96')  # 0xc012f196
        data.write(b'\x00\x0c')  # size
        self.rotation_for_type3.to_stream(data)

        data.write(b'p\xbc\x90\xa6')  # 0x70bc90a6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0x70bc90a6.encode("utf-8"))
        data.write(b'\x00')
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
            unknown_0xe71de331=data['unknown_0xe71de331'],
            model=data['model'],
            animation_information=AnimationParameters.from_json(data['animation_information']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            proxy_type=data['proxy_type'],
            player_offset=Vector.from_json(data['player_offset']),
            initial_state=data['initial_state'],
            player_visor=data['player_visor'],
            unknown_0xf09c2b4b=data['unknown_0xf09c2b4b'],
            unknown_0x760859e5=data['unknown_0x760859e5'],
            unknown_0xbd548a40=data['unknown_0xbd548a40'],
            rotation_for_type3=Vector.from_json(data['rotation_for_type3']),
            unknown_0x70bc90a6=data['unknown_0x70bc90a6'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'unknown_0xe71de331': self.unknown_0xe71de331,
            'model': self.model,
            'animation_information': self.animation_information.to_json(),
            'actor_information': self.actor_information.to_json(),
            'proxy_type': self.proxy_type,
            'player_offset': self.player_offset.to_json(),
            'initial_state': self.initial_state,
            'player_visor': self.player_visor,
            'unknown_0xf09c2b4b': self.unknown_0xf09c2b4b,
            'unknown_0x760859e5': self.unknown_0x760859e5,
            'unknown_0xbd548a40': self.unknown_0xbd548a40,
            'rotation_for_type3': self.rotation_for_type3.to_json(),
            'unknown_0x70bc90a6': self.unknown_0x70bc90a6,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model)

    def _dependencies_for_animation_information(self, asset_manager):
        yield from self.animation_information.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_model, "model", "AssetId"),
            (self._dependencies_for_animation_information, "animation_information", "AnimationParameters"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for PlayerController.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_unknown_0xe71de331(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_proxy_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_player_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_initial_state(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_player_visor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xf09c2b4b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x760859e5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbd548a40(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_for_type3(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_0x70bc90a6(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xe71de331: ('unknown_0xe71de331', _decode_unknown_0xe71de331),
    0xc27ffa8f: ('model', _decode_model),
    0xe25fb08c: ('animation_information', _decode_animation_information),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xca56a18a: ('proxy_type', _decode_proxy_type),
    0x1d8b933f: ('player_offset', _decode_player_offset),
    0xcb753319: ('initial_state', _decode_initial_state),
    0xd9c09cf7: ('player_visor', _decode_player_visor),
    0xf09c2b4b: ('unknown_0xf09c2b4b', _decode_unknown_0xf09c2b4b),
    0x760859e5: ('unknown_0x760859e5', _decode_unknown_0x760859e5),
    0xbd548a40: ('unknown_0xbd548a40', _decode_unknown_0xbd548a40),
    0xc012f196: ('rotation_for_type3', _decode_rotation_for_type3),
    0x70bc90a6: ('unknown_0x70bc90a6', _decode_unknown_0x70bc90a6),
}
