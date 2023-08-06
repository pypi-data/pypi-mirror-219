# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.ShockWaveInfo import ShockWaveInfo
from retro_data_structures.properties.corruption.archetypes.UnknownStruct7 import UnknownStruct7
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct12(BaseProperty):
    projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    weapon_info: ShockWaveInfo = dataclasses.field(default_factory=ShockWaveInfo)
    unknown_0xc2f2b95c: int = dataclasses.field(default=3)
    unknown_0xeb8c4444: int = dataclasses.field(default=5)
    unknown_0x6e7f4d8c: float = dataclasses.field(default=2.0)
    unknown_0x7d3aab27: float = dataclasses.field(default=3.0)
    unknown_0xb84c1410: float = dataclasses.field(default=1.0)
    unknown_0x08730e2c: float = dataclasses.field(default=2.0)
    turn_speed: float = dataclasses.field(default=30.0)
    unknown_0xb638cfa7: float = dataclasses.field(default=1.2999999523162842)
    unknown_0x18505e36: float = dataclasses.field(default=1.5)
    dongle_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    dongle_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    dongle_hinge1_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    dongle_hinge2_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    dongle_hinge3_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    dongle_hinge4_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    dongle_health: float = dataclasses.field(default=50.0)
    unknown_struct7: UnknownStruct7 = dataclasses.field(default_factory=UnknownStruct7)

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
        data.write(b'\x00\x14')  # 20 properties

        data.write(b'\xefH]\xb9')  # 0xef485db9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.projectile))

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x85\xdc\xa5e')  # 0x85dca565
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.weapon_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc2\xf2\xb9\\')  # 0xc2f2b95c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xc2f2b95c))

        data.write(b'\xeb\x8cDD')  # 0xeb8c4444
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xeb8c4444))

        data.write(b'n\x7fM\x8c')  # 0x6e7f4d8c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6e7f4d8c))

        data.write(b"}:\xab'")  # 0x7d3aab27
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7d3aab27))

        data.write(b'\xb8L\x14\x10')  # 0xb84c1410
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb84c1410))

        data.write(b'\x08s\x0e,')  # 0x8730e2c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x08730e2c))

        data.write(b'\x02\x0cx\xbb')  # 0x20c78bb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.turn_speed))

        data.write(b'\xb68\xcf\xa7')  # 0xb638cfa7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb638cfa7))

        data.write(b'\x18P^6')  # 0x18505e36
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x18505e36))

        data.write(b'j\x98\xee\xf6')  # 0x6a98eef6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.dongle_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x19\xaa\xf8\xf3')  # 0x19aaf8f3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.dongle_model))

        data.write(b'_\xcaf^')  # 0x5fca665e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.dongle_hinge1_model))

        data.write(b'\xc6(\x00_')  # 0xc628005f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.dongle_hinge2_model))

        data.write(b'\x07\xa6\xdf\x9f')  # 0x7a6df9f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.dongle_hinge3_model))

        data.write(b'.\x9d\xca\x1c')  # 0x2e9dca1c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.dongle_hinge4_model))

        data.write(b'\xa9\x0ea\x0c')  # 0xa90e610c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dongle_health))

        data.write(b'e\x9d\xf7m')  # 0x659df76d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            projectile=data['projectile'],
            damage=DamageInfo.from_json(data['damage']),
            weapon_info=ShockWaveInfo.from_json(data['weapon_info']),
            unknown_0xc2f2b95c=data['unknown_0xc2f2b95c'],
            unknown_0xeb8c4444=data['unknown_0xeb8c4444'],
            unknown_0x6e7f4d8c=data['unknown_0x6e7f4d8c'],
            unknown_0x7d3aab27=data['unknown_0x7d3aab27'],
            unknown_0xb84c1410=data['unknown_0xb84c1410'],
            unknown_0x08730e2c=data['unknown_0x08730e2c'],
            turn_speed=data['turn_speed'],
            unknown_0xb638cfa7=data['unknown_0xb638cfa7'],
            unknown_0x18505e36=data['unknown_0x18505e36'],
            dongle_vulnerability=DamageVulnerability.from_json(data['dongle_vulnerability']),
            dongle_model=data['dongle_model'],
            dongle_hinge1_model=data['dongle_hinge1_model'],
            dongle_hinge2_model=data['dongle_hinge2_model'],
            dongle_hinge3_model=data['dongle_hinge3_model'],
            dongle_hinge4_model=data['dongle_hinge4_model'],
            dongle_health=data['dongle_health'],
            unknown_struct7=UnknownStruct7.from_json(data['unknown_struct7']),
        )

    def to_json(self) -> dict:
        return {
            'projectile': self.projectile,
            'damage': self.damage.to_json(),
            'weapon_info': self.weapon_info.to_json(),
            'unknown_0xc2f2b95c': self.unknown_0xc2f2b95c,
            'unknown_0xeb8c4444': self.unknown_0xeb8c4444,
            'unknown_0x6e7f4d8c': self.unknown_0x6e7f4d8c,
            'unknown_0x7d3aab27': self.unknown_0x7d3aab27,
            'unknown_0xb84c1410': self.unknown_0xb84c1410,
            'unknown_0x08730e2c': self.unknown_0x08730e2c,
            'turn_speed': self.turn_speed,
            'unknown_0xb638cfa7': self.unknown_0xb638cfa7,
            'unknown_0x18505e36': self.unknown_0x18505e36,
            'dongle_vulnerability': self.dongle_vulnerability.to_json(),
            'dongle_model': self.dongle_model,
            'dongle_hinge1_model': self.dongle_hinge1_model,
            'dongle_hinge2_model': self.dongle_hinge2_model,
            'dongle_hinge3_model': self.dongle_hinge3_model,
            'dongle_hinge4_model': self.dongle_hinge4_model,
            'dongle_health': self.dongle_health,
            'unknown_struct7': self.unknown_struct7.to_json(),
        }


def _decode_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_weapon_info(data: typing.BinaryIO, property_size: int):
    return ShockWaveInfo.from_stream(data, property_size)


def _decode_unknown_0xc2f2b95c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xeb8c4444(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x6e7f4d8c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7d3aab27(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb84c1410(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x08730e2c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb638cfa7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x18505e36(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dongle_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_dongle_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_dongle_hinge1_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_dongle_hinge2_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_dongle_hinge3_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_dongle_hinge4_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_dongle_health(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct7(data: typing.BinaryIO, property_size: int):
    return UnknownStruct7.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xef485db9: ('projectile', _decode_projectile),
    0x337f9524: ('damage', _decode_damage),
    0x85dca565: ('weapon_info', _decode_weapon_info),
    0xc2f2b95c: ('unknown_0xc2f2b95c', _decode_unknown_0xc2f2b95c),
    0xeb8c4444: ('unknown_0xeb8c4444', _decode_unknown_0xeb8c4444),
    0x6e7f4d8c: ('unknown_0x6e7f4d8c', _decode_unknown_0x6e7f4d8c),
    0x7d3aab27: ('unknown_0x7d3aab27', _decode_unknown_0x7d3aab27),
    0xb84c1410: ('unknown_0xb84c1410', _decode_unknown_0xb84c1410),
    0x8730e2c: ('unknown_0x08730e2c', _decode_unknown_0x08730e2c),
    0x20c78bb: ('turn_speed', _decode_turn_speed),
    0xb638cfa7: ('unknown_0xb638cfa7', _decode_unknown_0xb638cfa7),
    0x18505e36: ('unknown_0x18505e36', _decode_unknown_0x18505e36),
    0x6a98eef6: ('dongle_vulnerability', _decode_dongle_vulnerability),
    0x19aaf8f3: ('dongle_model', _decode_dongle_model),
    0x5fca665e: ('dongle_hinge1_model', _decode_dongle_hinge1_model),
    0xc628005f: ('dongle_hinge2_model', _decode_dongle_hinge2_model),
    0x7a6df9f: ('dongle_hinge3_model', _decode_dongle_hinge3_model),
    0x2e9dca1c: ('dongle_hinge4_model', _decode_dongle_hinge4_model),
    0xa90e610c: ('dongle_health', _decode_dongle_health),
    0x659df76d: ('unknown_struct7', _decode_unknown_struct7),
}
