# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters


@dataclasses.dataclass()
class UnknownStruct195(BaseProperty):
    projectile_character: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)

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
        data.write(b'\x00\x01')  # 1 properties

        data.write(b'!\x01\x90\xc6')  # 0x210190c6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_character.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            projectile_character=AnimationParameters.from_json(data['projectile_character']),
        )

    def to_json(self) -> dict:
        return {
            'projectile_character': self.projectile_character.to_json(),
        }


def _decode_projectile_character(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x210190c6: ('projectile_character', _decode_projectile_character),
}
