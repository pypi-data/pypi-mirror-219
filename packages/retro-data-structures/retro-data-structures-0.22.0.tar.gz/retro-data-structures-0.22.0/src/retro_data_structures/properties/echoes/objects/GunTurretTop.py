# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class GunTurretTop(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    power_up_time: float = dataclasses.field(default=0.5)
    power_down_time: float = dataclasses.field(default=0.5)
    part_0xbf87e353: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0xaf6e671a: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    always_ff_0x67c8a8f4: int = dataclasses.field(default=0)
    always_ff_0x68d8b844: int = dataclasses.field(default=0)
    light_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    sound_0xe4aeeba4: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_0x5d9ed447: int = dataclasses.field(default=0, metadata={'sound': True})
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'GNTT'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['GunTurret.rel']

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
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b';\xc1\xd0C')  # 0x3bc1d043
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.power_up_time))

        data.write(b'\x83\x8au\xa4')  # 0x838a75a4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.power_down_time))

        data.write(b'\xbf\x87\xe3S')  # 0xbf87e353
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0xbf87e353))

        data.write(b'\xafng\x1a')  # 0xaf6e671a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0xaf6e671a))

        data.write(b'g\xc8\xa8\xf4')  # 0x67c8a8f4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.always_ff_0x67c8a8f4))

        data.write(b'h\xd8\xb8D')  # 0x68d8b844
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.always_ff_0x68d8b844))

        data.write(b'\xbd>\xfe}')  # 0xbd3efe7d
        data.write(b'\x00\x10')  # size
        self.light_color.to_stream(data)

        data.write(b'\xe4\xae\xeb\xa4')  # 0xe4aeeba4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_0xe4aeeba4))

        data.write(b']\x9e\xd4G')  # 0x5d9ed447
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_0x5d9ed447))

        data.write(b'\xb3wGP')  # 0xb3774750
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned.to_stream(data)
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

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            power_up_time=data['power_up_time'],
            power_down_time=data['power_down_time'],
            part_0xbf87e353=data['part_0xbf87e353'],
            part_0xaf6e671a=data['part_0xaf6e671a'],
            always_ff_0x67c8a8f4=data['always_ff_0x67c8a8f4'],
            always_ff_0x68d8b844=data['always_ff_0x68d8b844'],
            light_color=Color.from_json(data['light_color']),
            sound_0xe4aeeba4=data['sound_0xe4aeeba4'],
            sound_0x5d9ed447=data['sound_0x5d9ed447'],
            patterned=PatternedAITypedef.from_json(data['patterned']),
            actor_information=ActorParameters.from_json(data['actor_information']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'power_up_time': self.power_up_time,
            'power_down_time': self.power_down_time,
            'part_0xbf87e353': self.part_0xbf87e353,
            'part_0xaf6e671a': self.part_0xaf6e671a,
            'always_ff_0x67c8a8f4': self.always_ff_0x67c8a8f4,
            'always_ff_0x68d8b844': self.always_ff_0x68d8b844,
            'light_color': self.light_color.to_json(),
            'sound_0xe4aeeba4': self.sound_0xe4aeeba4,
            'sound_0x5d9ed447': self.sound_0x5d9ed447,
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_part_0xbf87e353(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0xbf87e353)

    def _dependencies_for_part_0xaf6e671a(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0xaf6e671a)

    def _dependencies_for_sound_0xe4aeeba4(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_0xe4aeeba4)

    def _dependencies_for_sound_0x5d9ed447(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_0x5d9ed447)

    def _dependencies_for_patterned(self, asset_manager):
        yield from self.patterned.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_part_0xbf87e353, "part_0xbf87e353", "AssetId"),
            (self._dependencies_for_part_0xaf6e671a, "part_0xaf6e671a", "AssetId"),
            (self._dependencies_for_sound_0xe4aeeba4, "sound_0xe4aeeba4", "int"),
            (self._dependencies_for_sound_0x5d9ed447, "sound_0x5d9ed447", "int"),
            (self._dependencies_for_patterned, "patterned", "PatternedAITypedef"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for GunTurretTop.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_power_up_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_power_down_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_part_0xbf87e353(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_part_0xaf6e671a(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_always_ff_0x67c8a8f4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_always_ff_0x68d8b844(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_light_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_sound_0xe4aeeba4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_0x5d9ed447(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x3bc1d043: ('power_up_time', _decode_power_up_time),
    0x838a75a4: ('power_down_time', _decode_power_down_time),
    0xbf87e353: ('part_0xbf87e353', _decode_part_0xbf87e353),
    0xaf6e671a: ('part_0xaf6e671a', _decode_part_0xaf6e671a),
    0x67c8a8f4: ('always_ff_0x67c8a8f4', _decode_always_ff_0x67c8a8f4),
    0x68d8b844: ('always_ff_0x68d8b844', _decode_always_ff_0x68d8b844),
    0xbd3efe7d: ('light_color', _decode_light_color),
    0xe4aeeba4: ('sound_0xe4aeeba4', _decode_sound_0xe4aeeba4),
    0x5d9ed447: ('sound_0x5d9ed447', _decode_sound_0x5d9ed447),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
}
