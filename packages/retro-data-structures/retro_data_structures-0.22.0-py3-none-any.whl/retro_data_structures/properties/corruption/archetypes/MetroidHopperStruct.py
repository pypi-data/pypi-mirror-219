# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.ShockWaveInfo import ShockWaveInfo


@dataclasses.dataclass()
class MetroidHopperStruct(BaseProperty):
    hypermode_shockwave: ShockWaveInfo = dataclasses.field(default_factory=ShockWaveInfo)
    hypermode_chance: float = dataclasses.field(default=0.10000000149011612)
    hypermode_duration: float = dataclasses.field(default=10.0)
    hypermode_delay: float = dataclasses.field(default=20.0)
    hyper_mode_initial_delay: float = dataclasses.field(default=15.0)
    hypermode_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\xf8\xe4^\x84')  # 0xf8e45e84
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hypermode_shockwave.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1c\xa0Mp')  # 0x1ca04d70
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hypermode_chance))

        data.write(b'\x8dP\x8c\xa7')  # 0x8d508ca7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hypermode_duration))

        data.write(b'\xc9\xbaGF')  # 0xc9ba4746
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hypermode_delay))

        data.write(b'\xe1t\xf4c')  # 0xe174f463
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hyper_mode_initial_delay))

        data.write(b'\xd1R(1')  # 0xd1522831
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hypermode_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            hypermode_shockwave=ShockWaveInfo.from_json(data['hypermode_shockwave']),
            hypermode_chance=data['hypermode_chance'],
            hypermode_duration=data['hypermode_duration'],
            hypermode_delay=data['hypermode_delay'],
            hyper_mode_initial_delay=data['hyper_mode_initial_delay'],
            hypermode_vulnerability=DamageVulnerability.from_json(data['hypermode_vulnerability']),
        )

    def to_json(self) -> dict:
        return {
            'hypermode_shockwave': self.hypermode_shockwave.to_json(),
            'hypermode_chance': self.hypermode_chance,
            'hypermode_duration': self.hypermode_duration,
            'hypermode_delay': self.hypermode_delay,
            'hyper_mode_initial_delay': self.hyper_mode_initial_delay,
            'hypermode_vulnerability': self.hypermode_vulnerability.to_json(),
        }


def _decode_hypermode_shockwave(data: typing.BinaryIO, property_size: int):
    return ShockWaveInfo.from_stream(data, property_size)


def _decode_hypermode_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hypermode_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hypermode_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hyper_mode_initial_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hypermode_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf8e45e84: ('hypermode_shockwave', _decode_hypermode_shockwave),
    0x1ca04d70: ('hypermode_chance', _decode_hypermode_chance),
    0x8d508ca7: ('hypermode_duration', _decode_hypermode_duration),
    0xc9ba4746: ('hypermode_delay', _decode_hypermode_delay),
    0xe174f463: ('hyper_mode_initial_delay', _decode_hyper_mode_initial_delay),
    0xd1522831: ('hypermode_vulnerability', _decode_hypermode_vulnerability),
}
