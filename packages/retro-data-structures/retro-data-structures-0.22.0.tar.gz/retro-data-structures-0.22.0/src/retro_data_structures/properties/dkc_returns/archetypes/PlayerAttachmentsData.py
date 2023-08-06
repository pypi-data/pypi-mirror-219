# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.PlayerAttachment import PlayerAttachment


@dataclasses.dataclass()
class PlayerAttachmentsData(BaseProperty):
    player_attachment01: PlayerAttachment = dataclasses.field(default_factory=PlayerAttachment)
    player_attachment02: PlayerAttachment = dataclasses.field(default_factory=PlayerAttachment)
    player_attachment03: PlayerAttachment = dataclasses.field(default_factory=PlayerAttachment)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'M/\xf4k')  # 0x4d2ff46b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.player_attachment01.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1e\xb5\xaf\xef')  # 0x1eb5afef
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.player_attachment02.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x99\x13d\xac')  # 0x991364ac
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.player_attachment03.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            player_attachment01=PlayerAttachment.from_json(data['player_attachment01']),
            player_attachment02=PlayerAttachment.from_json(data['player_attachment02']),
            player_attachment03=PlayerAttachment.from_json(data['player_attachment03']),
        )

    def to_json(self) -> dict:
        return {
            'player_attachment01': self.player_attachment01.to_json(),
            'player_attachment02': self.player_attachment02.to_json(),
            'player_attachment03': self.player_attachment03.to_json(),
        }


def _decode_player_attachment01(data: typing.BinaryIO, property_size: int):
    return PlayerAttachment.from_stream(data, property_size)


def _decode_player_attachment02(data: typing.BinaryIO, property_size: int):
    return PlayerAttachment.from_stream(data, property_size)


def _decode_player_attachment03(data: typing.BinaryIO, property_size: int):
    return PlayerAttachment.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4d2ff46b: ('player_attachment01', _decode_player_attachment01),
    0x1eb5afef: ('player_attachment02', _decode_player_attachment02),
    0x991364ac: ('player_attachment03', _decode_player_attachment03),
}
