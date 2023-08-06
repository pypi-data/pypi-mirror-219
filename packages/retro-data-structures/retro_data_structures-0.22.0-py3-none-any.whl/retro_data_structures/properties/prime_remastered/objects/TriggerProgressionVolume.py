# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import base64


@dataclasses.dataclass()
class TriggerProgressionVolume(BaseProperty):
    unknown_properties: dict[int, bytes] = dataclasses.field(default_factory=dict)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME_REMASTER

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack("<H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

        present_fields = default_override or {}
        present_fields["unknown_properties"] = {}

        for _ in range(property_count):
            property_id, property_size = struct.unpack("<LH", data.read(6))
            start = data.tell()
            try:
                property_name, decoder = _property_decoder[property_id]
                present_fields[property_name] = decoder(data, property_size)
            except KeyError:
                present_fields["unknown_properties"][property_id] = data.read(property_size)
            assert data.tell() - start == property_size

        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack("<H", 0 + len(self.unknown_properties)))

        for property_id, property_data in self.unknown_properties.items():
            data.write(struct.pack("<LH", property_id, len(property_data)))
            data.write(property_data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(

            unknown_properties={
                int(property_id, 16): base64.b64decode(property_data)
                for property_id, property_data in data["unknown_properties"].items()
            },
        )

    def to_json(self) -> dict:
        return {

            'unknown_properties': {
                hex(property_id): base64.b64encode(property_data)
                for property_id, property_data in self.unknown_properties.items()
            }
        }


_FAST_FORMAT = None
_FAST_IDS = ()


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[TriggerProgressionVolume]:
    if property_count != 0:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('<')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(0))
    if () != _FAST_IDS:
        data.seek(before)
        return None

    return TriggerProgressionVolume(
    )


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
}
