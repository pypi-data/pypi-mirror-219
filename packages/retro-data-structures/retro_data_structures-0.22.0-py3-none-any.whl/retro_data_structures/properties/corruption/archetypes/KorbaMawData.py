# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo


@dataclasses.dataclass()
class KorbaMawData(BaseProperty):
    bite_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0x200f67e7: float = dataclasses.field(default=0.5)
    unknown_0xe54de3e1: float = dataclasses.field(default=3.0)
    unknown_0x8a821fee: float = dataclasses.field(default=2.799999952316284)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xdfclK')  # 0xdf636c4b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.bite_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b' \x0fg\xe7')  # 0x200f67e7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x200f67e7))

        data.write(b'\xe5M\xe3\xe1')  # 0xe54de3e1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe54de3e1))

        data.write(b'\x8a\x82\x1f\xee')  # 0x8a821fee
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8a821fee))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            bite_damage=DamageInfo.from_json(data['bite_damage']),
            unknown_0x200f67e7=data['unknown_0x200f67e7'],
            unknown_0xe54de3e1=data['unknown_0xe54de3e1'],
            unknown_0x8a821fee=data['unknown_0x8a821fee'],
        )

    def to_json(self) -> dict:
        return {
            'bite_damage': self.bite_damage.to_json(),
            'unknown_0x200f67e7': self.unknown_0x200f67e7,
            'unknown_0xe54de3e1': self.unknown_0xe54de3e1,
            'unknown_0x8a821fee': self.unknown_0x8a821fee,
        }


def _decode_bite_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0x200f67e7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe54de3e1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8a821fee(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xdf636c4b: ('bite_damage', _decode_bite_damage),
    0x200f67e7: ('unknown_0x200f67e7', _decode_unknown_0x200f67e7),
    0xe54de3e1: ('unknown_0xe54de3e1', _decode_unknown_0xe54de3e1),
    0x8a821fee: ('unknown_0x8a821fee', _decode_unknown_0x8a821fee),
}
