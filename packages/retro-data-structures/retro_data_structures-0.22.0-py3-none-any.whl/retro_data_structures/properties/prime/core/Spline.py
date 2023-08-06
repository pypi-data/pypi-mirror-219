# Generated file
import dataclasses
import typing
import base64

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Spline(BaseProperty):
    data: bytes = b""

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        assert size is not None
        result = cls()
        result.data = data.read(size)
        return result

    def to_stream(self, data: typing.BinaryIO):
        data.write(self.data)

    @classmethod
    def from_json(cls, data):
        return cls(base64.b64decode(data))

    def to_json(self) -> str:
        return base64.b64encode(self.data).decode("ascii")

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME
