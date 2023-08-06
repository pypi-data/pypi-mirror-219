# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.PlayerMultiKillRewardSoundData import PlayerMultiKillRewardSoundData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerMultiKillRewardTierData import PlayerMultiKillRewardTierData
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class PlayerMultiKillRewardData(BaseProperty):
    reveal_height_spline: Spline = dataclasses.field(default_factory=Spline)
    tier1: PlayerMultiKillRewardTierData = dataclasses.field(default_factory=PlayerMultiKillRewardTierData)
    tier2: PlayerMultiKillRewardTierData = dataclasses.field(default_factory=PlayerMultiKillRewardTierData)
    sound: PlayerMultiKillRewardSoundData = dataclasses.field(default_factory=PlayerMultiKillRewardSoundData)

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

        data.write(b'2\x15*\xb2')  # 0x32152ab2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.reveal_height_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x00^;\xe9')  # 0x5e3be9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tier1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'D\xff\x1e\xf1')  # 0x44ff1ef1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tier2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b's\x84\xae\xa3')  # 0x7384aea3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            reveal_height_spline=Spline.from_json(data['reveal_height_spline']),
            tier1=PlayerMultiKillRewardTierData.from_json(data['tier1']),
            tier2=PlayerMultiKillRewardTierData.from_json(data['tier2']),
            sound=PlayerMultiKillRewardSoundData.from_json(data['sound']),
        )

    def to_json(self) -> dict:
        return {
            'reveal_height_spline': self.reveal_height_spline.to_json(),
            'tier1': self.tier1.to_json(),
            'tier2': self.tier2.to_json(),
            'sound': self.sound.to_json(),
        }


def _decode_reveal_height_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_tier1(data: typing.BinaryIO, property_size: int):
    return PlayerMultiKillRewardTierData.from_stream(data, property_size)


def _decode_tier2(data: typing.BinaryIO, property_size: int):
    return PlayerMultiKillRewardTierData.from_stream(data, property_size)


def _decode_sound(data: typing.BinaryIO, property_size: int):
    return PlayerMultiKillRewardSoundData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x32152ab2: ('reveal_height_spline', _decode_reveal_height_spline),
    0x5e3be9: ('tier1', _decode_tier1),
    0x44ff1ef1: ('tier2', _decode_tier2),
    0x7384aea3: ('sound', _decode_sound),
}
