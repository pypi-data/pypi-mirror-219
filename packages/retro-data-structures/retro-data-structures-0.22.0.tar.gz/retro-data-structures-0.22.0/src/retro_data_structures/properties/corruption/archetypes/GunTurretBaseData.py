# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class GunTurretBaseData(BaseProperty):
    is_pirate_turret: bool = dataclasses.field(default=False)
    shoots_at_player: bool = dataclasses.field(default=False)
    unknown: bool = dataclasses.field(default=False)
    gun_respawns: bool = dataclasses.field(default=False)
    gun_respawn_delay: float = dataclasses.field(default=2.0)
    deploy_height: float = dataclasses.field(default=5.0)
    deploy_time: float = dataclasses.field(default=1.0)
    attack_range: float = dataclasses.field(default=10.0)
    hearing_range: float = dataclasses.field(default=10.0)
    retarget_time: float = dataclasses.field(default=0.699999988079071)
    gun_connector_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

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
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'p\x1de\xcd')  # 0x701d65cd
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_pirate_turret))

        data.write(b'\nxF\xec')  # 0xa7846ec
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.shoots_at_player))

        data.write(b'\x08\xa1#g')  # 0x8a12367
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

        data.write(b'2\xd6\xd3%')  # 0x32d6d325
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.gun_respawns))

        data.write(b'5\xd6\x19f')  # 0x35d61966
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gun_respawn_delay))

        data.write(b'=\x94!P')  # 0x3d942150
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.deploy_height))

        data.write(b'c\xcc#M')  # 0x63cc234d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.deploy_time))

        data.write(b'9\xda\xc8\x1e')  # 0x39dac81e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_range))

        data.write(b'%GEP')  # 0x25474550
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hearing_range))

        data.write(b'sW\x01s')  # 0x73570173
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.retarget_time))

        data.write(b'\xb0\x9e\xd6\x86')  # 0xb09ed686
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.gun_connector_effect))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            is_pirate_turret=data['is_pirate_turret'],
            shoots_at_player=data['shoots_at_player'],
            unknown=data['unknown'],
            gun_respawns=data['gun_respawns'],
            gun_respawn_delay=data['gun_respawn_delay'],
            deploy_height=data['deploy_height'],
            deploy_time=data['deploy_time'],
            attack_range=data['attack_range'],
            hearing_range=data['hearing_range'],
            retarget_time=data['retarget_time'],
            gun_connector_effect=data['gun_connector_effect'],
        )

    def to_json(self) -> dict:
        return {
            'is_pirate_turret': self.is_pirate_turret,
            'shoots_at_player': self.shoots_at_player,
            'unknown': self.unknown,
            'gun_respawns': self.gun_respawns,
            'gun_respawn_delay': self.gun_respawn_delay,
            'deploy_height': self.deploy_height,
            'deploy_time': self.deploy_time,
            'attack_range': self.attack_range,
            'hearing_range': self.hearing_range,
            'retarget_time': self.retarget_time,
            'gun_connector_effect': self.gun_connector_effect,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x701d65cd, 0xa7846ec, 0x8a12367, 0x32d6d325, 0x35d61966, 0x3d942150, 0x63cc234d, 0x39dac81e, 0x25474550, 0x73570173, 0xb09ed686)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[GunTurretBaseData]:
    if property_count != 11:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LH?LH?LH?LHfLHfLHfLHfLHfLHfLHQ')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(102))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30]) != _FAST_IDS:
        data.seek(before)
        return None

    return GunTurretBaseData(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
        dec[26],
        dec[29],
        dec[32],
    )


def _decode_is_pirate_turret(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_shoots_at_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_gun_respawns(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_gun_respawn_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_deploy_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_deploy_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hearing_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_retarget_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gun_connector_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x701d65cd: ('is_pirate_turret', _decode_is_pirate_turret),
    0xa7846ec: ('shoots_at_player', _decode_shoots_at_player),
    0x8a12367: ('unknown', _decode_unknown),
    0x32d6d325: ('gun_respawns', _decode_gun_respawns),
    0x35d61966: ('gun_respawn_delay', _decode_gun_respawn_delay),
    0x3d942150: ('deploy_height', _decode_deploy_height),
    0x63cc234d: ('deploy_time', _decode_deploy_time),
    0x39dac81e: ('attack_range', _decode_attack_range),
    0x25474550: ('hearing_range', _decode_hearing_range),
    0x73570173: ('retarget_time', _decode_retarget_time),
    0xb09ed686: ('gun_connector_effect', _decode_gun_connector_effect),
}
