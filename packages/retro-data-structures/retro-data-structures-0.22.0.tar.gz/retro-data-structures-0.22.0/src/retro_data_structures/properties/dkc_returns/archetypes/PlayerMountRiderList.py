# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.PlayerMountRiderData import PlayerMountRiderData


@dataclasses.dataclass()
class PlayerMountRiderList(BaseProperty):
    max_riders: int = dataclasses.field(default=0)
    rider1: PlayerMountRiderData = dataclasses.field(default_factory=PlayerMountRiderData)
    rider2: PlayerMountRiderData = dataclasses.field(default_factory=PlayerMountRiderData)
    rider3: PlayerMountRiderData = dataclasses.field(default_factory=PlayerMountRiderData)

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

        data.write(b'\xfbj\x98\x1b')  # 0xfb6a981b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_riders))

        data.write(b'9\x82\xde\xc6')  # 0x3982dec6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rider1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'B\x9c\\%')  # 0x429c5c25
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rider2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xddF\xdf\xbb')  # 0xdd46dfbb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rider3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            max_riders=data['max_riders'],
            rider1=PlayerMountRiderData.from_json(data['rider1']),
            rider2=PlayerMountRiderData.from_json(data['rider2']),
            rider3=PlayerMountRiderData.from_json(data['rider3']),
        )

    def to_json(self) -> dict:
        return {
            'max_riders': self.max_riders,
            'rider1': self.rider1.to_json(),
            'rider2': self.rider2.to_json(),
            'rider3': self.rider3.to_json(),
        }


def _decode_max_riders(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_rider1(data: typing.BinaryIO, property_size: int):
    return PlayerMountRiderData.from_stream(data, property_size)


def _decode_rider2(data: typing.BinaryIO, property_size: int):
    return PlayerMountRiderData.from_stream(data, property_size)


def _decode_rider3(data: typing.BinaryIO, property_size: int):
    return PlayerMountRiderData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xfb6a981b: ('max_riders', _decode_max_riders),
    0x3982dec6: ('rider1', _decode_rider1),
    0x429c5c25: ('rider2', _decode_rider2),
    0xdd46dfbb: ('rider3', _decode_rider3),
}
