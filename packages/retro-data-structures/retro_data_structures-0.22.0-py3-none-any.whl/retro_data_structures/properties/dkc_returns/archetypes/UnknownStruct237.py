# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.MoleTrainManagerStructA import MoleTrainManagerStructA


@dataclasses.dataclass()
class UnknownStruct237(BaseProperty):
    sequence_count: int = dataclasses.field(default=1)
    mole_train_manager_struct_a_0x62e1522a: MoleTrainManagerStructA = dataclasses.field(default_factory=MoleTrainManagerStructA)
    mole_train_manager_struct_a_0xd1757fe9: MoleTrainManagerStructA = dataclasses.field(default_factory=MoleTrainManagerStructA)
    mole_train_manager_struct_a_0xbff964a8: MoleTrainManagerStructA = dataclasses.field(default_factory=MoleTrainManagerStructA)
    mole_train_manager_struct_a_0x6d2c222e: MoleTrainManagerStructA = dataclasses.field(default_factory=MoleTrainManagerStructA)
    mole_train_manager_struct_a_0x03a0396f: MoleTrainManagerStructA = dataclasses.field(default_factory=MoleTrainManagerStructA)

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'e\xec\xebz')  # 0x65eceb7a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sequence_count))

        data.write(b'b\xe1R*')  # 0x62e1522a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mole_train_manager_struct_a_0x62e1522a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd1u\x7f\xe9')  # 0xd1757fe9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mole_train_manager_struct_a_0xd1757fe9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbf\xf9d\xa8')  # 0xbff964a8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mole_train_manager_struct_a_0xbff964a8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'm,".')  # 0x6d2c222e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mole_train_manager_struct_a_0x6d2c222e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x03\xa09o')  # 0x3a0396f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mole_train_manager_struct_a_0x03a0396f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            sequence_count=data['sequence_count'],
            mole_train_manager_struct_a_0x62e1522a=MoleTrainManagerStructA.from_json(data['mole_train_manager_struct_a_0x62e1522a']),
            mole_train_manager_struct_a_0xd1757fe9=MoleTrainManagerStructA.from_json(data['mole_train_manager_struct_a_0xd1757fe9']),
            mole_train_manager_struct_a_0xbff964a8=MoleTrainManagerStructA.from_json(data['mole_train_manager_struct_a_0xbff964a8']),
            mole_train_manager_struct_a_0x6d2c222e=MoleTrainManagerStructA.from_json(data['mole_train_manager_struct_a_0x6d2c222e']),
            mole_train_manager_struct_a_0x03a0396f=MoleTrainManagerStructA.from_json(data['mole_train_manager_struct_a_0x03a0396f']),
        )

    def to_json(self) -> dict:
        return {
            'sequence_count': self.sequence_count,
            'mole_train_manager_struct_a_0x62e1522a': self.mole_train_manager_struct_a_0x62e1522a.to_json(),
            'mole_train_manager_struct_a_0xd1757fe9': self.mole_train_manager_struct_a_0xd1757fe9.to_json(),
            'mole_train_manager_struct_a_0xbff964a8': self.mole_train_manager_struct_a_0xbff964a8.to_json(),
            'mole_train_manager_struct_a_0x6d2c222e': self.mole_train_manager_struct_a_0x6d2c222e.to_json(),
            'mole_train_manager_struct_a_0x03a0396f': self.mole_train_manager_struct_a_0x03a0396f.to_json(),
        }


def _decode_sequence_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_mole_train_manager_struct_a_0x62e1522a(data: typing.BinaryIO, property_size: int):
    return MoleTrainManagerStructA.from_stream(data, property_size)


def _decode_mole_train_manager_struct_a_0xd1757fe9(data: typing.BinaryIO, property_size: int):
    return MoleTrainManagerStructA.from_stream(data, property_size)


def _decode_mole_train_manager_struct_a_0xbff964a8(data: typing.BinaryIO, property_size: int):
    return MoleTrainManagerStructA.from_stream(data, property_size)


def _decode_mole_train_manager_struct_a_0x6d2c222e(data: typing.BinaryIO, property_size: int):
    return MoleTrainManagerStructA.from_stream(data, property_size)


def _decode_mole_train_manager_struct_a_0x03a0396f(data: typing.BinaryIO, property_size: int):
    return MoleTrainManagerStructA.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x65eceb7a: ('sequence_count', _decode_sequence_count),
    0x62e1522a: ('mole_train_manager_struct_a_0x62e1522a', _decode_mole_train_manager_struct_a_0x62e1522a),
    0xd1757fe9: ('mole_train_manager_struct_a_0xd1757fe9', _decode_mole_train_manager_struct_a_0xd1757fe9),
    0xbff964a8: ('mole_train_manager_struct_a_0xbff964a8', _decode_mole_train_manager_struct_a_0xbff964a8),
    0x6d2c222e: ('mole_train_manager_struct_a_0x6d2c222e', _decode_mole_train_manager_struct_a_0x6d2c222e),
    0x3a0396f: ('mole_train_manager_struct_a_0x03a0396f', _decode_mole_train_manager_struct_a_0x03a0396f),
}
