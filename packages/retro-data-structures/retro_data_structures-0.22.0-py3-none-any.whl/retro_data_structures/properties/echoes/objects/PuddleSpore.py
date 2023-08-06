# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.echoes.archetypes.ShockWaveInfo import ShockWaveInfo


@dataclasses.dataclass()
class PuddleSpore(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    flavor: int = dataclasses.field(default=0)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unknown_0x5cdc877d: bool = dataclasses.field(default=True)
    charge_time: float = dataclasses.field(default=3.0)
    time_open: float = dataclasses.field(default=3.0)
    platform_time: float = dataclasses.field(default=7.0)
    unknown_0xf1c2d224: float = dataclasses.field(default=30.0)
    unknown_0x3c6af2ac: float = dataclasses.field(default=5.0)
    hit_detection_angle: float = dataclasses.field(default=30.0)
    shock_wave_height: float = dataclasses.field(default=0.0)
    sound: int = dataclasses.field(default=0, metadata={'sound': True})
    shock_wave_info: ShockWaveInfo = dataclasses.field(default_factory=ShockWaveInfo)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SPOR'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['PuddleSpore.rel']

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

        data.write(b'\xbesrJ')  # 0xbe73724a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.flavor))

        data.write(b'\xb3wGP')  # 0xb3774750
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned.to_stream(data, default_override={'detection_range': 35.0, 'detection_height_range': 3.0, 'detection_angle': 180.0, 'damage_wait_time': 0.0, 'collision_radius': 2.5, 'collision_height': 3.0, 'creature_size': 1})
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

        data.write(b'\\\xdc\x87}')  # 0x5cdc877d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x5cdc877d))

        data.write(b'D\xde\x9d\x92')  # 0x44de9d92
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.charge_time))

        data.write(b'iA_\xae')  # 0x69415fae
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.time_open))

        data.write(b'\xc1 -w')  # 0xc1202d77
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.platform_time))

        data.write(b'\xf1\xc2\xd2$')  # 0xf1c2d224
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf1c2d224))

        data.write(b'<j\xf2\xac')  # 0x3c6af2ac
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3c6af2ac))

        data.write(b'\xda\xdd\xeb\xe7')  # 0xdaddebe7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hit_detection_angle))

        data.write(b'B\xad\x13\x92')  # 0x42ad1392
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shock_wave_height))

        data.write(b'\xfe \xb4\xf5')  # 0xfe20b4f5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound))

        data.write(b'\x8fG\x87\xcb')  # 0x8f4787cb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shock_wave_info.to_stream(data)
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
            flavor=data['flavor'],
            patterned=PatternedAITypedef.from_json(data['patterned']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            unknown_0x5cdc877d=data['unknown_0x5cdc877d'],
            charge_time=data['charge_time'],
            time_open=data['time_open'],
            platform_time=data['platform_time'],
            unknown_0xf1c2d224=data['unknown_0xf1c2d224'],
            unknown_0x3c6af2ac=data['unknown_0x3c6af2ac'],
            hit_detection_angle=data['hit_detection_angle'],
            shock_wave_height=data['shock_wave_height'],
            sound=data['sound'],
            shock_wave_info=ShockWaveInfo.from_json(data['shock_wave_info']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'flavor': self.flavor,
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'unknown_0x5cdc877d': self.unknown_0x5cdc877d,
            'charge_time': self.charge_time,
            'time_open': self.time_open,
            'platform_time': self.platform_time,
            'unknown_0xf1c2d224': self.unknown_0xf1c2d224,
            'unknown_0x3c6af2ac': self.unknown_0x3c6af2ac,
            'hit_detection_angle': self.hit_detection_angle,
            'shock_wave_height': self.shock_wave_height,
            'sound': self.sound,
            'shock_wave_info': self.shock_wave_info.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_patterned(self, asset_manager):
        yield from self.patterned.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def _dependencies_for_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound)

    def _dependencies_for_shock_wave_info(self, asset_manager):
        yield from self.shock_wave_info.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_patterned, "patterned", "PatternedAITypedef"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
            (self._dependencies_for_sound, "sound", "int"),
            (self._dependencies_for_shock_wave_info, "shock_wave_info", "ShockWaveInfo"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for PuddleSpore.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_flavor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'detection_range': 35.0, 'detection_height_range': 3.0, 'detection_angle': 180.0, 'damage_wait_time': 0.0, 'collision_radius': 2.5, 'collision_height': 3.0, 'creature_size': 1})


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_unknown_0x5cdc877d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_charge_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_time_open(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_platform_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf1c2d224(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3c6af2ac(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hit_detection_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shock_wave_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_shock_wave_info(data: typing.BinaryIO, property_size: int):
    return ShockWaveInfo.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xbe73724a: ('flavor', _decode_flavor),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x5cdc877d: ('unknown_0x5cdc877d', _decode_unknown_0x5cdc877d),
    0x44de9d92: ('charge_time', _decode_charge_time),
    0x69415fae: ('time_open', _decode_time_open),
    0xc1202d77: ('platform_time', _decode_platform_time),
    0xf1c2d224: ('unknown_0xf1c2d224', _decode_unknown_0xf1c2d224),
    0x3c6af2ac: ('unknown_0x3c6af2ac', _decode_unknown_0x3c6af2ac),
    0xdaddebe7: ('hit_detection_angle', _decode_hit_detection_angle),
    0x42ad1392: ('shock_wave_height', _decode_shock_wave_height),
    0xfe20b4f5: ('sound', _decode_sound),
    0x8f4787cb: ('shock_wave_info', _decode_shock_wave_info),
}
