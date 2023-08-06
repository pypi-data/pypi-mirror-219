# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.BonusCredit import BonusCredit
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class Achievement(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    bonus_credit: BonusCredit = dataclasses.field(default_factory=BonusCredit)
    achievement: enums.Achievement = dataclasses.field(default=enums.Achievement.Unknown84)
    normal_difficulty: bool = dataclasses.field(default=True)
    hard_difficulty: bool = dataclasses.field(default=True)
    elite_difficulty: bool = dataclasses.field(default=True)
    bonus_credit_string: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'ACHI'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_ScriptAchievement.rso']

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'z\xac\x9e"')  # 0x7aac9e22
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.bonus_credit.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x05\x8d-\xdb')  # 0x58d2ddb
        data.write(b'\x00\x04')  # size
        self.achievement.to_stream(data)

        data.write(b'\x97OJ\xa1')  # 0x974f4aa1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.normal_difficulty))

        data.write(b'\x0f\x8c\xf6\xff')  # 0xf8cf6ff
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.hard_difficulty))

        data.write(b'\x9b\x89\x03\xeb')  # 0x9b8903eb
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.elite_difficulty))

        data.write(b'\xd6\xa0\xcf\xf1')  # 0xd6a0cff1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.bonus_credit_string))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            bonus_credit=BonusCredit.from_json(data['bonus_credit']),
            achievement=enums.Achievement.from_json(data['achievement']),
            normal_difficulty=data['normal_difficulty'],
            hard_difficulty=data['hard_difficulty'],
            elite_difficulty=data['elite_difficulty'],
            bonus_credit_string=data['bonus_credit_string'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'bonus_credit': self.bonus_credit.to_json(),
            'achievement': self.achievement.to_json(),
            'normal_difficulty': self.normal_difficulty,
            'hard_difficulty': self.hard_difficulty,
            'elite_difficulty': self.elite_difficulty,
            'bonus_credit_string': self.bonus_credit_string,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_bonus_credit(data: typing.BinaryIO, property_size: int):
    return BonusCredit.from_stream(data, property_size)


def _decode_achievement(data: typing.BinaryIO, property_size: int):
    return enums.Achievement.from_stream(data)


def _decode_normal_difficulty(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_hard_difficulty(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_elite_difficulty(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_bonus_credit_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x7aac9e22: ('bonus_credit', _decode_bonus_credit),
    0x58d2ddb: ('achievement', _decode_achievement),
    0x974f4aa1: ('normal_difficulty', _decode_normal_difficulty),
    0xf8cf6ff: ('hard_difficulty', _decode_hard_difficulty),
    0x9b8903eb: ('elite_difficulty', _decode_elite_difficulty),
    0xd6a0cff1: ('bonus_credit_string', _decode_bonus_credit_string),
}
