# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class AutoMapperIcons(BaseProperty):
    save_station_icon: str = dataclasses.field(default='')
    missile_station_icon: str = dataclasses.field(default='')
    elevator_icon_icon: str = dataclasses.field(default='')
    portal_icon: str = dataclasses.field(default='')
    unknown_0xfbf479ec: str = dataclasses.field(default='')
    unknown_0x5566b6e4: str = dataclasses.field(default='')
    unknown_0x51fe3f1f: str = dataclasses.field(default='')
    unknown_0xa4127a5a: str = dataclasses.field(default='')
    translator_door_icon: str = dataclasses.field(default='')

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\xe7\x01L\xda')  # 0xe7014cda
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.save_station_icon.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'3\xc9GI')  # 0x33c94749
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.missile_station_icon.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9b6\x94\x9e')  # 0x9b36949e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.elevator_icon_icon.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaf\xa1\xb8|')  # 0xafa1b87c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.portal_icon.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfb\xf4y\xec')  # 0xfbf479ec
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0xfbf479ec.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Uf\xb6\xe4')  # 0x5566b6e4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0x5566b6e4.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Q\xfe?\x1f')  # 0x51fe3f1f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0x51fe3f1f.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa4\x12zZ')  # 0xa4127a5a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0xa4127a5a.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf8@=\x18')  # 0xf8403d18
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.translator_door_icon.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            save_station_icon=data['save_station_icon'],
            missile_station_icon=data['missile_station_icon'],
            elevator_icon_icon=data['elevator_icon_icon'],
            portal_icon=data['portal_icon'],
            unknown_0xfbf479ec=data['unknown_0xfbf479ec'],
            unknown_0x5566b6e4=data['unknown_0x5566b6e4'],
            unknown_0x51fe3f1f=data['unknown_0x51fe3f1f'],
            unknown_0xa4127a5a=data['unknown_0xa4127a5a'],
            translator_door_icon=data['translator_door_icon'],
        )

    def to_json(self) -> dict:
        return {
            'save_station_icon': self.save_station_icon,
            'missile_station_icon': self.missile_station_icon,
            'elevator_icon_icon': self.elevator_icon_icon,
            'portal_icon': self.portal_icon,
            'unknown_0xfbf479ec': self.unknown_0xfbf479ec,
            'unknown_0x5566b6e4': self.unknown_0x5566b6e4,
            'unknown_0x51fe3f1f': self.unknown_0x51fe3f1f,
            'unknown_0xa4127a5a': self.unknown_0xa4127a5a,
            'translator_door_icon': self.translator_door_icon,
        }

    def dependencies_for(self, asset_manager):
        yield from []


def _decode_save_station_icon(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_missile_station_icon(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_elevator_icon_icon(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_portal_icon(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0xfbf479ec(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0x5566b6e4(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0x51fe3f1f(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0xa4127a5a(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_translator_door_icon(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe7014cda: ('save_station_icon', _decode_save_station_icon),
    0x33c94749: ('missile_station_icon', _decode_missile_station_icon),
    0x9b36949e: ('elevator_icon_icon', _decode_elevator_icon_icon),
    0xafa1b87c: ('portal_icon', _decode_portal_icon),
    0xfbf479ec: ('unknown_0xfbf479ec', _decode_unknown_0xfbf479ec),
    0x5566b6e4: ('unknown_0x5566b6e4', _decode_unknown_0x5566b6e4),
    0x51fe3f1f: ('unknown_0x51fe3f1f', _decode_unknown_0x51fe3f1f),
    0xa4127a5a: ('unknown_0xa4127a5a', _decode_unknown_0xa4127a5a),
    0xf8403d18: ('translator_door_icon', _decode_translator_door_icon),
}
