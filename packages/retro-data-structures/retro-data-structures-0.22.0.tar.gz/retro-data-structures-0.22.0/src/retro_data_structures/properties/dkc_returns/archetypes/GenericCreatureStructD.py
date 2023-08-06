# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums


@dataclasses.dataclass()
class GenericCreatureStructD(BaseProperty):
    message: enums.Message = dataclasses.field(default=enums.Message.Unknown10)
    behavior: enums.Behavior = dataclasses.field(default=enums.Behavior.Unknown1)
    set: enums.Set = dataclasses.field(default=enums.Set.Unknown1)

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

        data.write(b'\x13\x83Mo')  # 0x13834d6f
        data.write(b'\x00\x04')  # size
        self.message.to_stream(data)

        data.write(b'\xd1\x82\x15\xaa')  # 0xd18215aa
        data.write(b'\x00\x04')  # size
        self.behavior.to_stream(data)

        data.write(b'\x0b?z\x00')  # 0xb3f7a00
        data.write(b'\x00\x04')  # size
        self.set.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            message=enums.Message.from_json(data['message']),
            behavior=enums.Behavior.from_json(data['behavior']),
            set=enums.Set.from_json(data['set']),
        )

    def to_json(self) -> dict:
        return {
            'message': self.message.to_json(),
            'behavior': self.behavior.to_json(),
            'set': self.set.to_json(),
        }


_FAST_FORMAT = None
_FAST_IDS = (0x13834d6f, 0xd18215aa, 0xb3f7a00)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[GenericCreatureStructD]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHLLHLLHL')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(30))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return GenericCreatureStructD(
        enums.Message(dec[2]),
        enums.Behavior(dec[5]),
        enums.Set(dec[8]),
    )


def _decode_message(data: typing.BinaryIO, property_size: int):
    return enums.Message.from_stream(data)


def _decode_behavior(data: typing.BinaryIO, property_size: int):
    return enums.Behavior.from_stream(data)


def _decode_set(data: typing.BinaryIO, property_size: int):
    return enums.Set.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x13834d6f: ('message', _decode_message),
    0xd18215aa: ('behavior', _decode_behavior),
    0xb3f7a00: ('set', _decode_set),
}
