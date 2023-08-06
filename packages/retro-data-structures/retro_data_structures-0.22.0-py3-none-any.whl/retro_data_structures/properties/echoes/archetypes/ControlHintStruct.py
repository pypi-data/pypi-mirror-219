# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.ControllerActionStruct import ControllerActionStruct


@dataclasses.dataclass()
class ControlHintStruct(BaseProperty):
    command: ControllerActionStruct = dataclasses.field(default_factory=ControllerActionStruct)
    state: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'5\x9cz\xaf')  # 0x359c7aaf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.command.to_stream(data, default_override={'command': 0})
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
            command=ControllerActionStruct.from_json(data['command']),
            state=data['state'],
        )

    def to_json(self) -> dict:
        return {
            'command': self.command.to_json(),
            'state': self.state,
        }

    def _dependencies_for_command(self, asset_manager):
        yield from self.command.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_command, "command", "ControllerActionStruct"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for ControlHintStruct.{field_name} ({field_type}): {e}"
                )


def _decode_command(data: typing.BinaryIO, property_size: int):
    return ControllerActionStruct.from_stream(data, property_size, default_override={'command': 0})


def _decode_state(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x359c7aaf: ('command', _decode_command),
    0x4063422a: ('state', _decode_state),
}
