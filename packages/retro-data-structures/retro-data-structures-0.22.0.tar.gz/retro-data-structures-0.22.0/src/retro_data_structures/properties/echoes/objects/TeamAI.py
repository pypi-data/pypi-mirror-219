# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class TeamAI(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    max_team_size: int = dataclasses.field(default=20)
    max_melee_attackers: int = dataclasses.field(default=2)
    max_ranged_attackers: int = dataclasses.field(default=2)
    unknown_0x9fa9c457: int = dataclasses.field(default=30)
    unknown_0x54cd2755: int = dataclasses.field(default=1)
    unknown_0xc36ed15c: int = dataclasses.field(default=1)
    team_formation: int = dataclasses.field(default=0)
    unknown_0xd3ad55b6: float = dataclasses.field(default=0.0)
    unknown_0x8d00b839: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'TMAI'

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

        data.write(b'\xbf7\xe5\x18')  # 0xbf37e518
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_team_size))

        data.write(b'\xce\xbe\xe4\xab')  # 0xcebee4ab
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_melee_attackers))

        data.write(b'uU\xc1\xea')  # 0x7555c1ea
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_ranged_attackers))

        data.write(b'\x9f\xa9\xc4W')  # 0x9fa9c457
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x9fa9c457))

        data.write(b"T\xcd'U")  # 0x54cd2755
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x54cd2755))

        data.write(b'\xc3n\xd1\\')  # 0xc36ed15c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xc36ed15c))

        data.write(b'7\xa2\x03v')  # 0x37a20376
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.team_formation))

        data.write(b'\xd3\xadU\xb6')  # 0xd3ad55b6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd3ad55b6))

        data.write(b'\x8d\x00\xb89')  # 0x8d00b839
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8d00b839))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            max_team_size=data['max_team_size'],
            max_melee_attackers=data['max_melee_attackers'],
            max_ranged_attackers=data['max_ranged_attackers'],
            unknown_0x9fa9c457=data['unknown_0x9fa9c457'],
            unknown_0x54cd2755=data['unknown_0x54cd2755'],
            unknown_0xc36ed15c=data['unknown_0xc36ed15c'],
            team_formation=data['team_formation'],
            unknown_0xd3ad55b6=data['unknown_0xd3ad55b6'],
            unknown_0x8d00b839=data['unknown_0x8d00b839'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'max_team_size': self.max_team_size,
            'max_melee_attackers': self.max_melee_attackers,
            'max_ranged_attackers': self.max_ranged_attackers,
            'unknown_0x9fa9c457': self.unknown_0x9fa9c457,
            'unknown_0x54cd2755': self.unknown_0x54cd2755,
            'unknown_0xc36ed15c': self.unknown_0xc36ed15c,
            'team_formation': self.team_formation,
            'unknown_0xd3ad55b6': self.unknown_0xd3ad55b6,
            'unknown_0x8d00b839': self.unknown_0x8d00b839,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for TeamAI.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_max_team_size(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_max_melee_attackers(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_max_ranged_attackers(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x9fa9c457(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x54cd2755(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xc36ed15c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_team_formation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xd3ad55b6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8d00b839(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xbf37e518: ('max_team_size', _decode_max_team_size),
    0xcebee4ab: ('max_melee_attackers', _decode_max_melee_attackers),
    0x7555c1ea: ('max_ranged_attackers', _decode_max_ranged_attackers),
    0x9fa9c457: ('unknown_0x9fa9c457', _decode_unknown_0x9fa9c457),
    0x54cd2755: ('unknown_0x54cd2755', _decode_unknown_0x54cd2755),
    0xc36ed15c: ('unknown_0xc36ed15c', _decode_unknown_0xc36ed15c),
    0x37a20376: ('team_formation', _decode_team_formation),
    0xd3ad55b6: ('unknown_0xd3ad55b6', _decode_unknown_0xd3ad55b6),
    0x8d00b839: ('unknown_0x8d00b839', _decode_unknown_0x8d00b839),
}
