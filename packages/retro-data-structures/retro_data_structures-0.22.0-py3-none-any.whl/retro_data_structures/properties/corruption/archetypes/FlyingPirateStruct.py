# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability


@dataclasses.dataclass()
class FlyingPirateStruct(BaseProperty):
    enable_hyper_mode: bool = dataclasses.field(default=False)
    initial_hyper_mode_time: float = dataclasses.field(default=10.0)
    hyper_mode_check_time: float = dataclasses.field(default=20.0)
    hyper_mode_check_chance: float = dataclasses.field(default=100.0)
    hyper_mode_duration: float = dataclasses.field(default=20.0)
    hyper_mode_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)

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

        data.write(b'\xddD\x8c\xc9')  # 0xdd448cc9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enable_hyper_mode))

        data.write(b'\x8a\x83F\x18')  # 0x8a834618
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_hyper_mode_time))

        data.write(b'\xe9\xfdZ\x01')  # 0xe9fd5a01
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hyper_mode_check_time))

        data.write(b'\xf0DR\xf3')  # 0xf04452f3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hyper_mode_check_chance))

        data.write(b'\xa3\xf3\xbe]')  # 0xa3f3be5d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hyper_mode_duration))

        data.write(b'\xc8\xa1\xea\xc8')  # 0xc8a1eac8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hyper_mode_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            enable_hyper_mode=data['enable_hyper_mode'],
            initial_hyper_mode_time=data['initial_hyper_mode_time'],
            hyper_mode_check_time=data['hyper_mode_check_time'],
            hyper_mode_check_chance=data['hyper_mode_check_chance'],
            hyper_mode_duration=data['hyper_mode_duration'],
            hyper_mode_vulnerability=DamageVulnerability.from_json(data['hyper_mode_vulnerability']),
        )

    def to_json(self) -> dict:
        return {
            'enable_hyper_mode': self.enable_hyper_mode,
            'initial_hyper_mode_time': self.initial_hyper_mode_time,
            'hyper_mode_check_time': self.hyper_mode_check_time,
            'hyper_mode_check_chance': self.hyper_mode_check_chance,
            'hyper_mode_duration': self.hyper_mode_duration,
            'hyper_mode_vulnerability': self.hyper_mode_vulnerability.to_json(),
        }


def _decode_enable_hyper_mode(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_initial_hyper_mode_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hyper_mode_check_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hyper_mode_check_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hyper_mode_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hyper_mode_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xdd448cc9: ('enable_hyper_mode', _decode_enable_hyper_mode),
    0x8a834618: ('initial_hyper_mode_time', _decode_initial_hyper_mode_time),
    0xe9fd5a01: ('hyper_mode_check_time', _decode_hyper_mode_check_time),
    0xf04452f3: ('hyper_mode_check_chance', _decode_hyper_mode_check_chance),
    0xa3f3be5d: ('hyper_mode_duration', _decode_hyper_mode_duration),
    0xc8a1eac8: ('hyper_mode_vulnerability', _decode_hyper_mode_vulnerability),
}
