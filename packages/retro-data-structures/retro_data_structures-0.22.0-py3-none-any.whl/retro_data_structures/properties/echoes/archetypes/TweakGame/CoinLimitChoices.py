# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class CoinLimitChoices(BaseProperty):
    coin_limit0: int = dataclasses.field(default=200)
    coin_limit1: int = dataclasses.field(default=400)
    coin_limit2: int = dataclasses.field(default=600)
    coin_limit3: int = dataclasses.field(default=800)
    coin_limit4: int = dataclasses.field(default=1000)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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

        data.write(b'kL\xae&')  # 0x6b4cae26
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.coin_limit0))

        data.write(b'\xd3\xf0\xc9C')  # 0xd3f0c943
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.coin_limit1))

        data.write(b'\xc1Ef\xad')  # 0xc14566ad
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.coin_limit2))

        data.write(b'y\xf9\x01\xc8')  # 0x79f901c8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.coin_limit3))

        data.write(b'\xe4.9q')  # 0xe42e3971
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.coin_limit4))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            coin_limit0=data['coin_limit0'],
            coin_limit1=data['coin_limit1'],
            coin_limit2=data['coin_limit2'],
            coin_limit3=data['coin_limit3'],
            coin_limit4=data['coin_limit4'],
        )

    def to_json(self) -> dict:
        return {
            'coin_limit0': self.coin_limit0,
            'coin_limit1': self.coin_limit1,
            'coin_limit2': self.coin_limit2,
            'coin_limit3': self.coin_limit3,
            'coin_limit4': self.coin_limit4,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0x6b4cae26, 0xd3f0c943, 0xc14566ad, 0x79f901c8, 0xe42e3971)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[CoinLimitChoices]:
    if property_count != 5:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHlLHlLHlLHl')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(50))
    if (dec[0], dec[3], dec[6], dec[9], dec[12]) != _FAST_IDS:
        data.seek(before)
        return None

    return CoinLimitChoices(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
    )


def _decode_coin_limit0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_coin_limit1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_coin_limit2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_coin_limit3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_coin_limit4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6b4cae26: ('coin_limit0', _decode_coin_limit0),
    0xd3f0c943: ('coin_limit1', _decode_coin_limit1),
    0xc14566ad: ('coin_limit2', _decode_coin_limit2),
    0x79f901c8: ('coin_limit3', _decode_coin_limit3),
    0xe42e3971: ('coin_limit4', _decode_coin_limit4),
}
