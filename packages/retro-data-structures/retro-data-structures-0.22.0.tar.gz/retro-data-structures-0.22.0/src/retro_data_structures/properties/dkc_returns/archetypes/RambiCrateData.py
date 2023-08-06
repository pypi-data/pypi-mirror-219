# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters


@dataclasses.dataclass()
class RambiCrateData(BaseProperty):
    animation: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unknown_0xa2dc645a: int = dataclasses.field(default=0)
    unknown_0x456b0545: int = dataclasses.field(default=0)
    vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    unknown_0xfa8ca261: float = dataclasses.field(default=15.0)
    min_reactivate_distance: float = dataclasses.field(default=5.0)
    max_reactivate_distance: float = dataclasses.field(default=10.0)

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\xa3\xd6?D')  # 0xa3d63f44
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa2\xdcdZ')  # 0xa2dc645a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xa2dc645a))

        data.write(b'Ek\x05E')  # 0x456b0545
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x456b0545))

        data.write(b'{q\xae\x90')  # 0x7b71ae90
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfa\x8c\xa2a')  # 0xfa8ca261
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfa8ca261))

        data.write(b'\xc5Uf\xdb')  # 0xc55566db
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_reactivate_distance))

        data.write(b'&\x08\xd8\x01')  # 0x2608d801
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_reactivate_distance))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            animation=AnimationParameters.from_json(data['animation']),
            unknown_0xa2dc645a=data['unknown_0xa2dc645a'],
            unknown_0x456b0545=data['unknown_0x456b0545'],
            vulnerability=DamageVulnerability.from_json(data['vulnerability']),
            unknown_0xfa8ca261=data['unknown_0xfa8ca261'],
            min_reactivate_distance=data['min_reactivate_distance'],
            max_reactivate_distance=data['max_reactivate_distance'],
        )

    def to_json(self) -> dict:
        return {
            'animation': self.animation.to_json(),
            'unknown_0xa2dc645a': self.unknown_0xa2dc645a,
            'unknown_0x456b0545': self.unknown_0x456b0545,
            'vulnerability': self.vulnerability.to_json(),
            'unknown_0xfa8ca261': self.unknown_0xfa8ca261,
            'min_reactivate_distance': self.min_reactivate_distance,
            'max_reactivate_distance': self.max_reactivate_distance,
        }


def _decode_animation(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_unknown_0xa2dc645a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x456b0545(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_unknown_0xfa8ca261(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_reactivate_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_reactivate_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa3d63f44: ('animation', _decode_animation),
    0xa2dc645a: ('unknown_0xa2dc645a', _decode_unknown_0xa2dc645a),
    0x456b0545: ('unknown_0x456b0545', _decode_unknown_0x456b0545),
    0x7b71ae90: ('vulnerability', _decode_vulnerability),
    0xfa8ca261: ('unknown_0xfa8ca261', _decode_unknown_0xfa8ca261),
    0xc55566db: ('min_reactivate_distance', _decode_min_reactivate_distance),
    0x2608d801: ('max_reactivate_distance', _decode_max_reactivate_distance),
}
