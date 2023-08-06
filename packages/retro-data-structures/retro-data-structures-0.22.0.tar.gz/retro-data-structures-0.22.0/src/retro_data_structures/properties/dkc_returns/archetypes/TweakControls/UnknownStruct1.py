# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.MapControls import MapControls
from retro_data_structures.properties.dkc_returns.archetypes.MiscControls import MiscControls
from retro_data_structures.properties.dkc_returns.archetypes.TweakControls.UnknownStruct2 import UnknownStruct2
from retro_data_structures.properties.dkc_returns.archetypes.TweakControls.UnknownStruct3 import UnknownStruct3


@dataclasses.dataclass()
class UnknownStruct1(BaseProperty):
    unknown: UnknownStruct2 = dataclasses.field(default_factory=UnknownStruct2)
    map: MapControls = dataclasses.field(default_factory=MapControls)
    misc: MiscControls = dataclasses.field(default_factory=MiscControls)
    debug: UnknownStruct3 = dataclasses.field(default_factory=UnknownStruct3)

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

        data.write(b'K\xd8\xec\xb9')  # 0x4bd8ecb9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9a\xcbJ\xce')  # 0x9acb4ace
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.map.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbew\xde\xd2')  # 0xbe77ded2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.misc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'G\x06\x99\x11')  # 0x47069911
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.debug.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown=UnknownStruct2.from_json(data['unknown']),
            map=MapControls.from_json(data['map']),
            misc=MiscControls.from_json(data['misc']),
            debug=UnknownStruct3.from_json(data['debug']),
        )

    def to_json(self) -> dict:
        return {
            'unknown': self.unknown.to_json(),
            'map': self.map.to_json(),
            'misc': self.misc.to_json(),
            'debug': self.debug.to_json(),
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return UnknownStruct2.from_stream(data, property_size)


def _decode_map(data: typing.BinaryIO, property_size: int):
    return MapControls.from_stream(data, property_size)


def _decode_misc(data: typing.BinaryIO, property_size: int):
    return MiscControls.from_stream(data, property_size)


def _decode_debug(data: typing.BinaryIO, property_size: int):
    return UnknownStruct3.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4bd8ecb9: ('unknown', _decode_unknown),
    0x9acb4ace: ('map', _decode_map),
    0xbe77ded2: ('misc', _decode_misc),
    0x47069911: ('debug', _decode_debug),
}
