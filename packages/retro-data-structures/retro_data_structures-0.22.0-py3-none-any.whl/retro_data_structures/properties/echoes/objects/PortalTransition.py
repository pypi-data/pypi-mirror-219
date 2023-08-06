# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class PortalTransition(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    player_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0))
    volume: int = dataclasses.field(default=127)
    pan: int = dataclasses.field(default=64)
    agsc_0xe08e2172: AssetId = dataclasses.field(metadata={'asset_types': ['AGSC']}, default=default_asset_id)
    agsc_0xb3e6c4e3: AssetId = dataclasses.field(metadata={'asset_types': ['AGSC']}, default=default_asset_id)
    start_portal: int = dataclasses.field(default=0, metadata={'sound': True})
    in_portal1: int = dataclasses.field(default=0, metadata={'sound': True})
    in_portal2: int = dataclasses.field(default=0, metadata={'sound': True})
    direction: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'PRTT'

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

        data.write(b'\xe2_\xb0\x8c')  # 0xe25fb08c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe5k\xa3e')  # 0xe56ba365
        data.write(b'\x00\x0c')  # size
        self.player_scale.to_stream(data)

        data.write(b'\x80\xc6l7')  # 0x80c66c37
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.volume))

        data.write(b'\xd6\x08\x8b\xc5')  # 0xd6088bc5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.pan))

        data.write(b'\xe0\x8e!r')  # 0xe08e2172
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.agsc_0xe08e2172))

        data.write(b'\xb3\xe6\xc4\xe3')  # 0xb3e6c4e3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.agsc_0xb3e6c4e3))

        data.write(b'P\x85 \xe1')  # 0x508520e1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.start_portal))

        data.write(b'4\xc7\xc1\xcc')  # 0x34c7c1cc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.in_portal1))

        data.write(b'\xb2S\xb3b')  # 0xb253b362
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.in_portal2))

        data.write(b'D\x06\xdc\x02')  # 0x4406dc02
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.direction))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            animation_information=AnimationParameters.from_json(data['animation_information']),
            player_scale=Vector.from_json(data['player_scale']),
            volume=data['volume'],
            pan=data['pan'],
            agsc_0xe08e2172=data['agsc_0xe08e2172'],
            agsc_0xb3e6c4e3=data['agsc_0xb3e6c4e3'],
            start_portal=data['start_portal'],
            in_portal1=data['in_portal1'],
            in_portal2=data['in_portal2'],
            direction=data['direction'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'animation_information': self.animation_information.to_json(),
            'player_scale': self.player_scale.to_json(),
            'volume': self.volume,
            'pan': self.pan,
            'agsc_0xe08e2172': self.agsc_0xe08e2172,
            'agsc_0xb3e6c4e3': self.agsc_0xb3e6c4e3,
            'start_portal': self.start_portal,
            'in_portal1': self.in_portal1,
            'in_portal2': self.in_portal2,
            'direction': self.direction,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_animation_information(self, asset_manager):
        yield from self.animation_information.dependencies_for(asset_manager)

    def _dependencies_for_agsc_0xe08e2172(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.agsc_0xe08e2172)

    def _dependencies_for_agsc_0xb3e6c4e3(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.agsc_0xb3e6c4e3)

    def _dependencies_for_start_portal(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.start_portal)

    def _dependencies_for_in_portal1(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.in_portal1)

    def _dependencies_for_in_portal2(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.in_portal2)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_animation_information, "animation_information", "AnimationParameters"),
            (self._dependencies_for_agsc_0xe08e2172, "agsc_0xe08e2172", "AssetId"),
            (self._dependencies_for_agsc_0xb3e6c4e3, "agsc_0xb3e6c4e3", "AssetId"),
            (self._dependencies_for_start_portal, "start_portal", "int"),
            (self._dependencies_for_in_portal1, "in_portal1", "int"),
            (self._dependencies_for_in_portal2, "in_portal2", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for PortalTransition.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_player_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_pan(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_agsc_0xe08e2172(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_agsc_0xb3e6c4e3(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_start_portal(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_in_portal1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_in_portal2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_direction(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xe25fb08c: ('animation_information', _decode_animation_information),
    0xe56ba365: ('player_scale', _decode_player_scale),
    0x80c66c37: ('volume', _decode_volume),
    0xd6088bc5: ('pan', _decode_pan),
    0xe08e2172: ('agsc_0xe08e2172', _decode_agsc_0xe08e2172),
    0xb3e6c4e3: ('agsc_0xb3e6c4e3', _decode_agsc_0xb3e6c4e3),
    0x508520e1: ('start_portal', _decode_start_portal),
    0x34c7c1cc: ('in_portal1', _decode_in_portal1),
    0xb253b362: ('in_portal2', _decode_in_portal2),
    0x4406dc02: ('direction', _decode_direction),
}
