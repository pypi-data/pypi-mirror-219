# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums


@dataclasses.dataclass()
class ConditionalTest(BaseProperty):
    boolean: int = dataclasses.field(default=1)  # Choice
    use_connected_as_amount: bool = dataclasses.field(default=False)
    player_item: enums.PlayerItem = dataclasses.field(default=enums.PlayerItem.Banana)
    amount_or_capacity: int = dataclasses.field(default=0)
    condition: int = dataclasses.field(default=0)
    use_connected_as_value: bool = dataclasses.field(default=False)
    value: int = dataclasses.field(default=0)

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\xde>@\xa3')  # 0xde3e40a3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.boolean))

        data.write(b'yO\x9b\xeb')  # 0x794f9beb
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_connected_as_amount))

        data.write(b'\xd3\xaf\x8dr')  # 0xd3af8d72
        data.write(b'\x00\x04')  # size
        self.player_item.to_stream(data)

        data.write(b'\x03\xbd\xea\x98')  # 0x3bdea98
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.amount_or_capacity))

        data.write(b'pr\x93d')  # 0x70729364
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.condition))

        data.write(b'\xae\xb6\x94\xb4')  # 0xaeb694b4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_connected_as_value))

        data.write(b'\x8d\xb99\x8a')  # 0x8db9398a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.value))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            boolean=data['boolean'],
            use_connected_as_amount=data['use_connected_as_amount'],
            player_item=enums.PlayerItem.from_json(data['player_item']),
            amount_or_capacity=data['amount_or_capacity'],
            condition=data['condition'],
            use_connected_as_value=data['use_connected_as_value'],
            value=data['value'],
        )

    def to_json(self) -> dict:
        return {
            'boolean': self.boolean,
            'use_connected_as_amount': self.use_connected_as_amount,
            'player_item': self.player_item.to_json(),
            'amount_or_capacity': self.amount_or_capacity,
            'condition': self.condition,
            'use_connected_as_value': self.use_connected_as_value,
            'value': self.value,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xde3e40a3, 0x794f9beb, 0xd3af8d72, 0x3bdea98, 0x70729364, 0xaeb694b4, 0x8db9398a)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[ConditionalTest]:
    if property_count != 7:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHLLH?LHLLHlLHlLH?LHl')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(64))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18]) != _FAST_IDS:
        data.seek(before)
        return None

    return ConditionalTest(
        dec[2],
        dec[5],
        enums.PlayerItem(dec[8]),
        dec[11],
        dec[14],
        dec[17],
        dec[20],
    )


def _decode_boolean(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_use_connected_as_amount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_player_item(data: typing.BinaryIO, property_size: int):
    return enums.PlayerItem.from_stream(data)


def _decode_amount_or_capacity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_condition(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_use_connected_as_value(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_value(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xde3e40a3: ('boolean', _decode_boolean),
    0x794f9beb: ('use_connected_as_amount', _decode_use_connected_as_amount),
    0xd3af8d72: ('player_item', _decode_player_item),
    0x3bdea98: ('amount_or_capacity', _decode_amount_or_capacity),
    0x70729364: ('condition', _decode_condition),
    0xaeb694b4: ('use_connected_as_value', _decode_use_connected_as_value),
    0x8db9398a: ('value', _decode_value),
}
