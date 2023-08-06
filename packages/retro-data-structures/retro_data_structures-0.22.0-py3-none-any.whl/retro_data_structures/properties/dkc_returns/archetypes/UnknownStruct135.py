# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct135(BaseProperty):
    death_fling: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown: str = dataclasses.field(default='')
    blow_left: str = dataclasses.field(default='')
    blow_right: str = dataclasses.field(default='')

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\x92I\xd6\xb3')  # 0x9249d6b3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.death_fling))

        data.write(b'\xb2b\x83\xce')  # 0xb26283ce
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'$\xa8\x0f\x03')  # 0x24a80f03
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.blow_left.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x94_\xb4\xee')  # 0x945fb4ee
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.blow_right.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            death_fling=data['death_fling'],
            unknown=data['unknown'],
            blow_left=data['blow_left'],
            blow_right=data['blow_right'],
        )

    def to_json(self) -> dict:
        return {
            'death_fling': self.death_fling,
            'unknown': self.unknown,
            'blow_left': self.blow_left,
            'blow_right': self.blow_right,
        }


def _decode_death_fling(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_blow_left(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_blow_right(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x9249d6b3: ('death_fling', _decode_death_fling),
    0xb26283ce: ('unknown', _decode_unknown),
    0x24a80f03: ('blow_left', _decode_blow_left),
    0x945fb4ee: ('blow_right', _decode_blow_right),
}
