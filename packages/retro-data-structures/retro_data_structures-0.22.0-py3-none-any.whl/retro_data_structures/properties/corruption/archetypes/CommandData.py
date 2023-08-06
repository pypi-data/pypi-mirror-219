# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.ControlCommands import ControlCommands


@dataclasses.dataclass()
class CommandData(BaseProperty):
    used: bool = dataclasses.field(default=False)
    control_command: ControlCommands = dataclasses.field(default_factory=ControlCommands)
    state: int = dataclasses.field(default=0)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\x1a\xd5\xb1h')  # 0x1ad5b168
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.used))

        data.write(b'\x07R{:')  # 0x7527b3a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.control_command.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'@cB*')  # 0x4063422a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.state))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            used=data['used'],
            control_command=ControlCommands.from_json(data['control_command']),
            state=data['state'],
        )

    def to_json(self) -> dict:
        return {
            'used': self.used,
            'control_command': self.control_command.to_json(),
            'state': self.state,
        }


def _decode_used(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_control_command(data: typing.BinaryIO, property_size: int):
    return ControlCommands.from_stream(data, property_size)


def _decode_state(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1ad5b168: ('used', _decode_used),
    0x7527b3a: ('control_command', _decode_control_command),
    0x4063422a: ('state', _decode_state),
}
