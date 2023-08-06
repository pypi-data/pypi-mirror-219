# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class PlayerMeleeData(BaseProperty):
    melee_enabled: bool = dataclasses.field(default=False)
    autonomous_melee_enabled: bool = dataclasses.field(default=False)
    front_creature_melee_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    rear_creature_melee_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    controller_melee_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'\xfds\xa4\x04')  # 0xfd73a404
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.melee_enabled))

        data.write(b'",#}')  # 0x222c237d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.autonomous_melee_enabled))

        data.write(b'\x117\x1f\xad')  # 0x11371fad
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.front_creature_melee_sound))

        data.write(b'M\x12~\xcf')  # 0x4d127ecf
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.rear_creature_melee_sound))

        data.write(b'L\xc4\xe3\x9d')  # 0x4cc4e39d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.controller_melee_sound))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            melee_enabled=data['melee_enabled'],
            autonomous_melee_enabled=data['autonomous_melee_enabled'],
            front_creature_melee_sound=data['front_creature_melee_sound'],
            rear_creature_melee_sound=data['rear_creature_melee_sound'],
            controller_melee_sound=data['controller_melee_sound'],
        )

    def to_json(self) -> dict:
        return {
            'melee_enabled': self.melee_enabled,
            'autonomous_melee_enabled': self.autonomous_melee_enabled,
            'front_creature_melee_sound': self.front_creature_melee_sound,
            'rear_creature_melee_sound': self.rear_creature_melee_sound,
            'controller_melee_sound': self.controller_melee_sound,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xfd73a404, 0x222c237d, 0x11371fad, 0x4d127ecf, 0x4cc4e39d)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[PlayerMeleeData]:
    if property_count != 5:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LH?LHQLHQLHQ')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(56))
    if (dec[0], dec[3], dec[6], dec[9], dec[12]) != _FAST_IDS:
        data.seek(before)
        return None

    return PlayerMeleeData(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
    )


def _decode_melee_enabled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_autonomous_melee_enabled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_front_creature_melee_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_rear_creature_melee_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_controller_melee_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xfd73a404: ('melee_enabled', _decode_melee_enabled),
    0x222c237d: ('autonomous_melee_enabled', _decode_autonomous_melee_enabled),
    0x11371fad: ('front_creature_melee_sound', _decode_front_creature_melee_sound),
    0x4d127ecf: ('rear_creature_melee_sound', _decode_rear_creature_melee_sound),
    0x4cc4e39d: ('controller_melee_sound', _decode_controller_melee_sound),
}
