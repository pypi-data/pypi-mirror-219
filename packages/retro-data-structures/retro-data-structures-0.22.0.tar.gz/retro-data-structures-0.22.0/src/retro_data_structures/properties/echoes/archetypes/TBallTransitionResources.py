# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.TGunResources import TGunResources
from retro_data_structures.properties.echoes.core.Spline import Spline


@dataclasses.dataclass()
class TBallTransitionResources(BaseProperty):
    unknown_0xd48e4124: str = dataclasses.field(default='')
    unknown_0x01e12c84: TGunResources = dataclasses.field(default_factory=TGunResources)
    unknown_0xf24b055d: TGunResources = dataclasses.field(default_factory=TGunResources)
    unknown_0xa342c3a6: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x15b6840d: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x23fb0e93: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x564262f0: Spline = dataclasses.field(default_factory=Spline)
    movement_control: Spline = dataclasses.field(default_factory=Spline)

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'\xd4\x8eA$')  # 0xd48e4124
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0xd48e4124.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x01\xe1,\x84')  # 0x1e12c84
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x01e12c84.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf2K\x05]')  # 0xf24b055d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xf24b055d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa3B\xc3\xa6')  # 0xa342c3a6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xa342c3a6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x15\xb6\x84\r')  # 0x15b6840d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x15b6840d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'#\xfb\x0e\x93')  # 0x23fb0e93
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x23fb0e93.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'VBb\xf0')  # 0x564262f0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x564262f0.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x91\x83\xa2b')  # 0x9183a262
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.movement_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xd48e4124=data['unknown_0xd48e4124'],
            unknown_0x01e12c84=TGunResources.from_json(data['unknown_0x01e12c84']),
            unknown_0xf24b055d=TGunResources.from_json(data['unknown_0xf24b055d']),
            unknown_0xa342c3a6=Spline.from_json(data['unknown_0xa342c3a6']),
            unknown_0x15b6840d=Spline.from_json(data['unknown_0x15b6840d']),
            unknown_0x23fb0e93=Spline.from_json(data['unknown_0x23fb0e93']),
            unknown_0x564262f0=Spline.from_json(data['unknown_0x564262f0']),
            movement_control=Spline.from_json(data['movement_control']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xd48e4124': self.unknown_0xd48e4124,
            'unknown_0x01e12c84': self.unknown_0x01e12c84.to_json(),
            'unknown_0xf24b055d': self.unknown_0xf24b055d.to_json(),
            'unknown_0xa342c3a6': self.unknown_0xa342c3a6.to_json(),
            'unknown_0x15b6840d': self.unknown_0x15b6840d.to_json(),
            'unknown_0x23fb0e93': self.unknown_0x23fb0e93.to_json(),
            'unknown_0x564262f0': self.unknown_0x564262f0.to_json(),
            'movement_control': self.movement_control.to_json(),
        }

    def _dependencies_for_unknown_0x01e12c84(self, asset_manager):
        yield from self.unknown_0x01e12c84.dependencies_for(asset_manager)

    def _dependencies_for_unknown_0xf24b055d(self, asset_manager):
        yield from self.unknown_0xf24b055d.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unknown_0x01e12c84, "unknown_0x01e12c84", "TGunResources"),
            (self._dependencies_for_unknown_0xf24b055d, "unknown_0xf24b055d", "TGunResources"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for TBallTransitionResources.{field_name} ({field_type}): {e}"
                )


def _decode_unknown_0xd48e4124(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0x01e12c84(data: typing.BinaryIO, property_size: int):
    return TGunResources.from_stream(data, property_size)


def _decode_unknown_0xf24b055d(data: typing.BinaryIO, property_size: int):
    return TGunResources.from_stream(data, property_size)


def _decode_unknown_0xa342c3a6(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x15b6840d(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x23fb0e93(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x564262f0(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_movement_control(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd48e4124: ('unknown_0xd48e4124', _decode_unknown_0xd48e4124),
    0x1e12c84: ('unknown_0x01e12c84', _decode_unknown_0x01e12c84),
    0xf24b055d: ('unknown_0xf24b055d', _decode_unknown_0xf24b055d),
    0xa342c3a6: ('unknown_0xa342c3a6', _decode_unknown_0xa342c3a6),
    0x15b6840d: ('unknown_0x15b6840d', _decode_unknown_0x15b6840d),
    0x23fb0e93: ('unknown_0x23fb0e93', _decode_unknown_0x23fb0e93),
    0x564262f0: ('unknown_0x564262f0', _decode_unknown_0x564262f0),
    0x9183a262: ('movement_control', _decode_movement_control),
}
