# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.echoes as enums


@dataclasses.dataclass()
class ConditionalTest(BaseProperty):
    boolean: enums.Boolean = dataclasses.field(default=enums.Boolean.And)
    player_item: enums.PlayerItem = dataclasses.field(default=enums.PlayerItem.PowerBeam)
    amount_or_capacity: enums.AmountOrCapacity = dataclasses.field(default=enums.AmountOrCapacity.Amount)
    condition: enums.Condition = dataclasses.field(default=enums.Condition.EqualTo)
    value: int = dataclasses.field(default=0)

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

        data.write(b'\xde>@\xa3')  # 0xde3e40a3
        data.write(b'\x00\x04')  # size
        self.boolean.to_stream(data)

        data.write(b'\xd3\xaf\x8dr')  # 0xd3af8d72
        data.write(b'\x00\x04')  # size
        self.player_item.to_stream(data)

        data.write(b'\x03\xbd\xea\x98')  # 0x3bdea98
        data.write(b'\x00\x04')  # size
        self.amount_or_capacity.to_stream(data)

        data.write(b'pr\x93d')  # 0x70729364
        data.write(b'\x00\x04')  # size
        self.condition.to_stream(data)

        data.write(b'\x8d\xb99\x8a')  # 0x8db9398a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.value))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            boolean=enums.Boolean.from_json(data['boolean']),
            player_item=enums.PlayerItem.from_json(data['player_item']),
            amount_or_capacity=enums.AmountOrCapacity.from_json(data['amount_or_capacity']),
            condition=enums.Condition.from_json(data['condition']),
            value=data['value'],
        )

    def to_json(self) -> dict:
        return {
            'boolean': self.boolean.to_json(),
            'player_item': self.player_item.to_json(),
            'amount_or_capacity': self.amount_or_capacity.to_json(),
            'condition': self.condition.to_json(),
            'value': self.value,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0xde3e40a3, 0xd3af8d72, 0x3bdea98, 0x70729364, 0x8db9398a)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[ConditionalTest]:
    if property_count != 5:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHLLHLLHLLHLLHl')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(50))
    if (dec[0], dec[3], dec[6], dec[9], dec[12]) != _FAST_IDS:
        data.seek(before)
        return None

    return ConditionalTest(
        enums.Boolean(dec[2]),
        enums.PlayerItem(dec[5]),
        enums.AmountOrCapacity(dec[8]),
        enums.Condition(dec[11]),
        dec[14],
    )


def _decode_boolean(data: typing.BinaryIO, property_size: int):
    return enums.Boolean.from_stream(data)


def _decode_player_item(data: typing.BinaryIO, property_size: int):
    return enums.PlayerItem.from_stream(data)


def _decode_amount_or_capacity(data: typing.BinaryIO, property_size: int):
    return enums.AmountOrCapacity.from_stream(data)


def _decode_condition(data: typing.BinaryIO, property_size: int):
    return enums.Condition.from_stream(data)


def _decode_value(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xde3e40a3: ('boolean', _decode_boolean),
    0xd3af8d72: ('player_item', _decode_player_item),
    0x3bdea98: ('amount_or_capacity', _decode_amount_or_capacity),
    0x70729364: ('condition', _decode_condition),
    0x8db9398a: ('value', _decode_value),
}
