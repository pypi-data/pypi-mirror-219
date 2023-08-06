# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums


@dataclasses.dataclass()
class UnknownStruct83(BaseProperty):
    attack_mode: enums.AttackMode = dataclasses.field(default=enums.AttackMode.Unknown1)
    number_of_stages: int = dataclasses.field(default=4)
    unknown_0x8314e5ec: int = dataclasses.field(default=3)
    unknown_0x8968dc43: float = dataclasses.field(default=0.5)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xf8d\xfa\xd8')  # 0xf864fad8
        data.write(b'\x00\x04')  # size
        self.attack_mode.to_stream(data)

        data.write(b'\x86\x97\x00\xfa')  # 0x869700fa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_stages))

        data.write(b'\x83\x14\xe5\xec')  # 0x8314e5ec
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x8314e5ec))

        data.write(b'\x89h\xdcC')  # 0x8968dc43
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8968dc43))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            attack_mode=enums.AttackMode.from_json(data['attack_mode']),
            number_of_stages=data['number_of_stages'],
            unknown_0x8314e5ec=data['unknown_0x8314e5ec'],
            unknown_0x8968dc43=data['unknown_0x8968dc43'],
        )

    def to_json(self) -> dict:
        return {
            'attack_mode': self.attack_mode.to_json(),
            'number_of_stages': self.number_of_stages,
            'unknown_0x8314e5ec': self.unknown_0x8314e5ec,
            'unknown_0x8968dc43': self.unknown_0x8968dc43,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xf864fad8, 0x869700fa, 0x8314e5ec, 0x8968dc43)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct83]:
    if property_count != 4:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHLLHlLHlLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(40))
    if (dec[0], dec[3], dec[6], dec[9]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct83(
        enums.AttackMode(dec[2]),
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_attack_mode(data: typing.BinaryIO, property_size: int):
    return enums.AttackMode.from_stream(data)


def _decode_number_of_stages(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x8314e5ec(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x8968dc43(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf864fad8: ('attack_mode', _decode_attack_mode),
    0x869700fa: ('number_of_stages', _decode_number_of_stages),
    0x8314e5ec: ('unknown_0x8314e5ec', _decode_unknown_0x8314e5ec),
    0x8968dc43: ('unknown_0x8968dc43', _decode_unknown_0x8968dc43),
}
