# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.Convergence import Convergence


@dataclasses.dataclass()
class PlayerTeleportData(BaseProperty):
    teleport_to_locator: str = dataclasses.field(default='')
    teleport_render_push_amount: float = dataclasses.field(default=0.0)
    teleport_method: Convergence = dataclasses.field(default_factory=Convergence)

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

        data.write(b'\xa6\xab\x86D')  # 0xa6ab8644
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.teleport_to_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'J;\xce\xb4')  # 0x4a3bceb4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.teleport_render_push_amount))

        data.write(b'\xa0d}\xf6')  # 0xa0647df6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.teleport_method.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            teleport_to_locator=data['teleport_to_locator'],
            teleport_render_push_amount=data['teleport_render_push_amount'],
            teleport_method=Convergence.from_json(data['teleport_method']),
        )

    def to_json(self) -> dict:
        return {
            'teleport_to_locator': self.teleport_to_locator,
            'teleport_render_push_amount': self.teleport_render_push_amount,
            'teleport_method': self.teleport_method.to_json(),
        }


def _decode_teleport_to_locator(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_teleport_render_push_amount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_teleport_method(data: typing.BinaryIO, property_size: int):
    return Convergence.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa6ab8644: ('teleport_to_locator', _decode_teleport_to_locator),
    0x4a3bceb4: ('teleport_render_push_amount', _decode_teleport_render_push_amount),
    0xa0647df6: ('teleport_method', _decode_teleport_method),
}
