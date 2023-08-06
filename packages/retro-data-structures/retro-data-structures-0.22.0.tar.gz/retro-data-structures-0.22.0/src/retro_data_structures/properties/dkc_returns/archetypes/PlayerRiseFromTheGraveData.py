# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class PlayerRiseFromTheGraveData(BaseProperty):
    rejoin_success_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    rejoin_fail_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    rejoin_fail_delay: float = dataclasses.field(default=1.0)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'V)\x95b')  # 0x56299562
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.rejoin_success_sound))

        data.write(b'\x8d\x81o\x05')  # 0x8d816f05
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.rejoin_fail_sound))

        data.write(b'<#0o')  # 0x3c23306f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rejoin_fail_delay))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            rejoin_success_sound=data['rejoin_success_sound'],
            rejoin_fail_sound=data['rejoin_fail_sound'],
            rejoin_fail_delay=data['rejoin_fail_delay'],
        )

    def to_json(self) -> dict:
        return {
            'rejoin_success_sound': self.rejoin_success_sound,
            'rejoin_fail_sound': self.rejoin_fail_sound,
            'rejoin_fail_delay': self.rejoin_fail_delay,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x56299562, 0x8d816f05, 0x3c23306f)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[PlayerRiseFromTheGraveData]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHQLHQLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(38))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return PlayerRiseFromTheGraveData(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_rejoin_success_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_rejoin_fail_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_rejoin_fail_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x56299562: ('rejoin_success_sound', _decode_rejoin_success_sound),
    0x8d816f05: ('rejoin_fail_sound', _decode_rejoin_fail_sound),
    0x3c23306f: ('rejoin_fail_delay', _decode_rejoin_fail_delay),
}
