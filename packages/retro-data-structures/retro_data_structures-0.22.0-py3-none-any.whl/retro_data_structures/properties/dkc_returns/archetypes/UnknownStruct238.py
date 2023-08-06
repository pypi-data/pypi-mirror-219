# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.MoleTrainManagerStructB import MoleTrainManagerStructB


@dataclasses.dataclass()
class UnknownStruct238(BaseProperty):
    unknown_0x5d57fc7c: float = dataclasses.field(default=1.0)
    unknown_0xe205412c: float = dataclasses.field(default=0.5)
    cart_speed: float = dataclasses.field(default=10.0)
    unknown_0x2d3c5998: float = dataclasses.field(default=2.5)
    sequence_count: int = dataclasses.field(default=1)
    mole_train_manager_struct_b_0x9aecdc44: MoleTrainManagerStructB = dataclasses.field(default_factory=MoleTrainManagerStructB)
    mole_train_manager_struct_b_0x2978f187: MoleTrainManagerStructB = dataclasses.field(default_factory=MoleTrainManagerStructB)
    mole_train_manager_struct_b_0x47f4eac6: MoleTrainManagerStructB = dataclasses.field(default_factory=MoleTrainManagerStructB)
    mole_train_manager_struct_b_0x9521ac40: MoleTrainManagerStructB = dataclasses.field(default_factory=MoleTrainManagerStructB)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b']W\xfc|')  # 0x5d57fc7c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5d57fc7c))

        data.write(b'\xe2\x05A,')  # 0xe205412c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe205412c))

        data.write(b'9\x94\xbe\x14')  # 0x3994be14
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cart_speed))

        data.write(b'-<Y\x98')  # 0x2d3c5998
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2d3c5998))

        data.write(b'e\xec\xebz')  # 0x65eceb7a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sequence_count))

        data.write(b'\x9a\xec\xdcD')  # 0x9aecdc44
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mole_train_manager_struct_b_0x9aecdc44.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b')x\xf1\x87')  # 0x2978f187
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mole_train_manager_struct_b_0x2978f187.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'G\xf4\xea\xc6')  # 0x47f4eac6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mole_train_manager_struct_b_0x47f4eac6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95!\xac@')  # 0x9521ac40
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mole_train_manager_struct_b_0x9521ac40.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x5d57fc7c=data['unknown_0x5d57fc7c'],
            unknown_0xe205412c=data['unknown_0xe205412c'],
            cart_speed=data['cart_speed'],
            unknown_0x2d3c5998=data['unknown_0x2d3c5998'],
            sequence_count=data['sequence_count'],
            mole_train_manager_struct_b_0x9aecdc44=MoleTrainManagerStructB.from_json(data['mole_train_manager_struct_b_0x9aecdc44']),
            mole_train_manager_struct_b_0x2978f187=MoleTrainManagerStructB.from_json(data['mole_train_manager_struct_b_0x2978f187']),
            mole_train_manager_struct_b_0x47f4eac6=MoleTrainManagerStructB.from_json(data['mole_train_manager_struct_b_0x47f4eac6']),
            mole_train_manager_struct_b_0x9521ac40=MoleTrainManagerStructB.from_json(data['mole_train_manager_struct_b_0x9521ac40']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x5d57fc7c': self.unknown_0x5d57fc7c,
            'unknown_0xe205412c': self.unknown_0xe205412c,
            'cart_speed': self.cart_speed,
            'unknown_0x2d3c5998': self.unknown_0x2d3c5998,
            'sequence_count': self.sequence_count,
            'mole_train_manager_struct_b_0x9aecdc44': self.mole_train_manager_struct_b_0x9aecdc44.to_json(),
            'mole_train_manager_struct_b_0x2978f187': self.mole_train_manager_struct_b_0x2978f187.to_json(),
            'mole_train_manager_struct_b_0x47f4eac6': self.mole_train_manager_struct_b_0x47f4eac6.to_json(),
            'mole_train_manager_struct_b_0x9521ac40': self.mole_train_manager_struct_b_0x9521ac40.to_json(),
        }


def _decode_unknown_0x5d57fc7c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe205412c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cart_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2d3c5998(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sequence_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_mole_train_manager_struct_b_0x9aecdc44(data: typing.BinaryIO, property_size: int):
    return MoleTrainManagerStructB.from_stream(data, property_size)


def _decode_mole_train_manager_struct_b_0x2978f187(data: typing.BinaryIO, property_size: int):
    return MoleTrainManagerStructB.from_stream(data, property_size)


def _decode_mole_train_manager_struct_b_0x47f4eac6(data: typing.BinaryIO, property_size: int):
    return MoleTrainManagerStructB.from_stream(data, property_size)


def _decode_mole_train_manager_struct_b_0x9521ac40(data: typing.BinaryIO, property_size: int):
    return MoleTrainManagerStructB.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x5d57fc7c: ('unknown_0x5d57fc7c', _decode_unknown_0x5d57fc7c),
    0xe205412c: ('unknown_0xe205412c', _decode_unknown_0xe205412c),
    0x3994be14: ('cart_speed', _decode_cart_speed),
    0x2d3c5998: ('unknown_0x2d3c5998', _decode_unknown_0x2d3c5998),
    0x65eceb7a: ('sequence_count', _decode_sequence_count),
    0x9aecdc44: ('mole_train_manager_struct_b_0x9aecdc44', _decode_mole_train_manager_struct_b_0x9aecdc44),
    0x2978f187: ('mole_train_manager_struct_b_0x2978f187', _decode_mole_train_manager_struct_b_0x2978f187),
    0x47f4eac6: ('mole_train_manager_struct_b_0x47f4eac6', _decode_mole_train_manager_struct_b_0x47f4eac6),
    0x9521ac40: ('mole_train_manager_struct_b_0x9521ac40', _decode_mole_train_manager_struct_b_0x9521ac40),
}
