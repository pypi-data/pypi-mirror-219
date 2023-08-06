# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class Armor(BaseProperty):
    has_armor: bool = dataclasses.field(default=False)
    armor_health: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    armor_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    head_armor_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    collar_armor_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    left_collar_armor_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    right_collar_armor_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    spine1_armor_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    spine2_armor_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    left_hip_armor_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    right_hip_armor_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    skeleton_root_armor_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

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
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'\xfd\xe9\xc4\xdf')  # 0xfde9c4df
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.has_armor))

        data.write(b'\xf1\x83\x84\xd4')  # 0xf18384d4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.armor_health.to_stream(data, default_override={'health': 100.0, 'hi_knock_back_resistance': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x89m[\xd9')  # 0x896d5bd9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.armor_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'h\x00+\xd7')  # 0x68002bd7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.head_armor_model))

        data.write(b'\xad1\\|')  # 0xad315c7c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.collar_armor_model))

        data.write(b'\x04*%\xed')  # 0x42a25ed
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.left_collar_armor_model))

        data.write(b'\xe3\x9b\x8b\x1e')  # 0xe39b8b1e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.right_collar_armor_model))

        data.write(b'5l\x16j')  # 0x356c166a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.spine1_armor_model))

        data.write(b'\x1c\xa4\xa2\x98')  # 0x1ca4a298
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.spine2_armor_model))

        data.write(b'\xdfDP~')  # 0xdf44507e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.left_hip_armor_model))

        data.write(b'\xd2\xc9\xa6V')  # 0xd2c9a656
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.right_hip_armor_model))

        data.write(b'\xd4\xe2j\x8e')  # 0xd4e26a8e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.skeleton_root_armor_model))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            has_armor=data['has_armor'],
            armor_health=HealthInfo.from_json(data['armor_health']),
            armor_vulnerability=DamageVulnerability.from_json(data['armor_vulnerability']),
            head_armor_model=data['head_armor_model'],
            collar_armor_model=data['collar_armor_model'],
            left_collar_armor_model=data['left_collar_armor_model'],
            right_collar_armor_model=data['right_collar_armor_model'],
            spine1_armor_model=data['spine1_armor_model'],
            spine2_armor_model=data['spine2_armor_model'],
            left_hip_armor_model=data['left_hip_armor_model'],
            right_hip_armor_model=data['right_hip_armor_model'],
            skeleton_root_armor_model=data['skeleton_root_armor_model'],
        )

    def to_json(self) -> dict:
        return {
            'has_armor': self.has_armor,
            'armor_health': self.armor_health.to_json(),
            'armor_vulnerability': self.armor_vulnerability.to_json(),
            'head_armor_model': self.head_armor_model,
            'collar_armor_model': self.collar_armor_model,
            'left_collar_armor_model': self.left_collar_armor_model,
            'right_collar_armor_model': self.right_collar_armor_model,
            'spine1_armor_model': self.spine1_armor_model,
            'spine2_armor_model': self.spine2_armor_model,
            'left_hip_armor_model': self.left_hip_armor_model,
            'right_hip_armor_model': self.right_hip_armor_model,
            'skeleton_root_armor_model': self.skeleton_root_armor_model,
        }


def _decode_has_armor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_armor_health(data: typing.BinaryIO, property_size: int):
    return HealthInfo.from_stream(data, property_size, default_override={'health': 100.0, 'hi_knock_back_resistance': 5.0})


def _decode_armor_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_head_armor_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_collar_armor_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_left_collar_armor_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_right_collar_armor_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_spine1_armor_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_spine2_armor_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_left_hip_armor_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_right_hip_armor_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_skeleton_root_armor_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xfde9c4df: ('has_armor', _decode_has_armor),
    0xf18384d4: ('armor_health', _decode_armor_health),
    0x896d5bd9: ('armor_vulnerability', _decode_armor_vulnerability),
    0x68002bd7: ('head_armor_model', _decode_head_armor_model),
    0xad315c7c: ('collar_armor_model', _decode_collar_armor_model),
    0x42a25ed: ('left_collar_armor_model', _decode_left_collar_armor_model),
    0xe39b8b1e: ('right_collar_armor_model', _decode_right_collar_armor_model),
    0x356c166a: ('spine1_armor_model', _decode_spine1_armor_model),
    0x1ca4a298: ('spine2_armor_model', _decode_spine2_armor_model),
    0xdf44507e: ('left_hip_armor_model', _decode_left_hip_armor_model),
    0xd2c9a656: ('right_hip_armor_model', _decode_right_hip_armor_model),
    0xd4e26a8e: ('skeleton_root_armor_model', _decode_skeleton_root_armor_model),
}
