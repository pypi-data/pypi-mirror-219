# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct40(BaseProperty):
    unknown_0xbed8a4ba: float = dataclasses.field(default=1.5)
    unknown_0xc2b98161: float = dataclasses.field(default=2.5)
    unknown_0x5fb66017: float = dataclasses.field(default=3.0)
    unknown_0xbab42316: float = dataclasses.field(default=150.0)
    part_0x8f06342a: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sound_0xd8b11129: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_0xe99e5316: int = dataclasses.field(default=0, metadata={'sound': True})
    damage_info: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    part_0x686489fd: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
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

        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\xbe\xd8\xa4\xba')  # 0xbed8a4ba
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbed8a4ba))

        data.write(b'\xc2\xb9\x81a')  # 0xc2b98161
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc2b98161))

        data.write(b'_\xb6`\x17')  # 0x5fb66017
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5fb66017))

        data.write(b'\xba\xb4#\x16')  # 0xbab42316
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbab42316))

        data.write(b'\x8f\x064*')  # 0x8f06342a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x8f06342a))

        data.write(b'\xd8\xb1\x11)')  # 0xd8b11129
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_0xd8b11129))

        data.write(b'\xe9\x9eS\x16')  # 0xe99e5316
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_0xe99e5316))

        data.write(b'\x14@\xd1R')  # 0x1440d152
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_radius': 13.0, 'di_knock_back_power': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'hd\x89\xfd')  # 0x686489fd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x686489fd))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xbed8a4ba=data['unknown_0xbed8a4ba'],
            unknown_0xc2b98161=data['unknown_0xc2b98161'],
            unknown_0x5fb66017=data['unknown_0x5fb66017'],
            unknown_0xbab42316=data['unknown_0xbab42316'],
            part_0x8f06342a=data['part_0x8f06342a'],
            sound_0xd8b11129=data['sound_0xd8b11129'],
            sound_0xe99e5316=data['sound_0xe99e5316'],
            damage_info=DamageInfo.from_json(data['damage_info']),
            part_0x686489fd=data['part_0x686489fd'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xbed8a4ba': self.unknown_0xbed8a4ba,
            'unknown_0xc2b98161': self.unknown_0xc2b98161,
            'unknown_0x5fb66017': self.unknown_0x5fb66017,
            'unknown_0xbab42316': self.unknown_0xbab42316,
            'part_0x8f06342a': self.part_0x8f06342a,
            'sound_0xd8b11129': self.sound_0xd8b11129,
            'sound_0xe99e5316': self.sound_0xe99e5316,
            'damage_info': self.damage_info.to_json(),
            'part_0x686489fd': self.part_0x686489fd,
        }

    def _dependencies_for_part_0x8f06342a(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0x8f06342a)

    def _dependencies_for_sound_0xd8b11129(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_0xd8b11129)

    def _dependencies_for_sound_0xe99e5316(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_0xe99e5316)

    def _dependencies_for_damage_info(self, asset_manager):
        yield from self.damage_info.dependencies_for(asset_manager)

    def _dependencies_for_part_0x686489fd(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0x686489fd)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_part_0x8f06342a, "part_0x8f06342a", "AssetId"),
            (self._dependencies_for_sound_0xd8b11129, "sound_0xd8b11129", "int"),
            (self._dependencies_for_sound_0xe99e5316, "sound_0xe99e5316", "int"),
            (self._dependencies_for_damage_info, "damage_info", "DamageInfo"),
            (self._dependencies_for_part_0x686489fd, "part_0x686489fd", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for UnknownStruct40.{field_name} ({field_type}): {e}"
                )


def _decode_unknown_0xbed8a4ba(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc2b98161(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5fb66017(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbab42316(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_part_0x8f06342a(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sound_0xd8b11129(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_0xe99e5316(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_damage_info(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_radius': 13.0, 'di_knock_back_power': 10.0})


def _decode_part_0x686489fd(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xbed8a4ba: ('unknown_0xbed8a4ba', _decode_unknown_0xbed8a4ba),
    0xc2b98161: ('unknown_0xc2b98161', _decode_unknown_0xc2b98161),
    0x5fb66017: ('unknown_0x5fb66017', _decode_unknown_0x5fb66017),
    0xbab42316: ('unknown_0xbab42316', _decode_unknown_0xbab42316),
    0x8f06342a: ('part_0x8f06342a', _decode_part_0x8f06342a),
    0xd8b11129: ('sound_0xd8b11129', _decode_sound_0xd8b11129),
    0xe99e5316: ('sound_0xe99e5316', _decode_sound_0xe99e5316),
    0x1440d152: ('damage_info', _decode_damage_info),
    0x686489fd: ('part_0x686489fd', _decode_part_0x686489fd),
}
