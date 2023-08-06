# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.PuddleControlPhaseData import PuddleControlPhaseData
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class PuddleControlData(BaseProperty):
    unknown: float = dataclasses.field(default=1.0)
    bounding_box_scale: float = dataclasses.field(default=1.0)
    puddle_control_phase_data_0xae0e60e2: PuddleControlPhaseData = dataclasses.field(default_factory=PuddleControlPhaseData)
    puddle_control_phase_data_0x1fd78dd3: PuddleControlPhaseData = dataclasses.field(default_factory=PuddleControlPhaseData)
    puddle_control_phase_data_0x5d4158a7: PuddleControlPhaseData = dataclasses.field(default_factory=PuddleControlPhaseData)
    puddle_control_phase_data_0xda4488bf: PuddleControlPhaseData = dataclasses.field(default_factory=PuddleControlPhaseData)
    puddle_control_phase_data_0x57b054de: PuddleControlPhaseData = dataclasses.field(default_factory=PuddleControlPhaseData)
    start_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'\x0b:\x08\xc9')  # 0xb3a08c9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'\x14\xbf\xde\xa6')  # 0x14bfdea6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bounding_box_scale))

        data.write(b'\xae\x0e`\xe2')  # 0xae0e60e2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.puddle_control_phase_data_0xae0e60e2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1f\xd7\x8d\xd3')  # 0x1fd78dd3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.puddle_control_phase_data_0x1fd78dd3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b']AX\xa7')  # 0x5d4158a7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.puddle_control_phase_data_0x5d4158a7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdaD\x88\xbf')  # 0xda4488bf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.puddle_control_phase_data_0xda4488bf.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'W\xb0T\xde')  # 0x57b054de
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.puddle_control_phase_data_0x57b054de.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa8\xccH\xb3')  # 0xa8cc48b3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.start_sound))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown=data['unknown'],
            bounding_box_scale=data['bounding_box_scale'],
            puddle_control_phase_data_0xae0e60e2=PuddleControlPhaseData.from_json(data['puddle_control_phase_data_0xae0e60e2']),
            puddle_control_phase_data_0x1fd78dd3=PuddleControlPhaseData.from_json(data['puddle_control_phase_data_0x1fd78dd3']),
            puddle_control_phase_data_0x5d4158a7=PuddleControlPhaseData.from_json(data['puddle_control_phase_data_0x5d4158a7']),
            puddle_control_phase_data_0xda4488bf=PuddleControlPhaseData.from_json(data['puddle_control_phase_data_0xda4488bf']),
            puddle_control_phase_data_0x57b054de=PuddleControlPhaseData.from_json(data['puddle_control_phase_data_0x57b054de']),
            start_sound=data['start_sound'],
        )

    def to_json(self) -> dict:
        return {
            'unknown': self.unknown,
            'bounding_box_scale': self.bounding_box_scale,
            'puddle_control_phase_data_0xae0e60e2': self.puddle_control_phase_data_0xae0e60e2.to_json(),
            'puddle_control_phase_data_0x1fd78dd3': self.puddle_control_phase_data_0x1fd78dd3.to_json(),
            'puddle_control_phase_data_0x5d4158a7': self.puddle_control_phase_data_0x5d4158a7.to_json(),
            'puddle_control_phase_data_0xda4488bf': self.puddle_control_phase_data_0xda4488bf.to_json(),
            'puddle_control_phase_data_0x57b054de': self.puddle_control_phase_data_0x57b054de.to_json(),
            'start_sound': self.start_sound,
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bounding_box_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_puddle_control_phase_data_0xae0e60e2(data: typing.BinaryIO, property_size: int):
    return PuddleControlPhaseData.from_stream(data, property_size)


def _decode_puddle_control_phase_data_0x1fd78dd3(data: typing.BinaryIO, property_size: int):
    return PuddleControlPhaseData.from_stream(data, property_size)


def _decode_puddle_control_phase_data_0x5d4158a7(data: typing.BinaryIO, property_size: int):
    return PuddleControlPhaseData.from_stream(data, property_size)


def _decode_puddle_control_phase_data_0xda4488bf(data: typing.BinaryIO, property_size: int):
    return PuddleControlPhaseData.from_stream(data, property_size)


def _decode_puddle_control_phase_data_0x57b054de(data: typing.BinaryIO, property_size: int):
    return PuddleControlPhaseData.from_stream(data, property_size)


def _decode_start_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb3a08c9: ('unknown', _decode_unknown),
    0x14bfdea6: ('bounding_box_scale', _decode_bounding_box_scale),
    0xae0e60e2: ('puddle_control_phase_data_0xae0e60e2', _decode_puddle_control_phase_data_0xae0e60e2),
    0x1fd78dd3: ('puddle_control_phase_data_0x1fd78dd3', _decode_puddle_control_phase_data_0x1fd78dd3),
    0x5d4158a7: ('puddle_control_phase_data_0x5d4158a7', _decode_puddle_control_phase_data_0x5d4158a7),
    0xda4488bf: ('puddle_control_phase_data_0xda4488bf', _decode_puddle_control_phase_data_0xda4488bf),
    0x57b054de: ('puddle_control_phase_data_0x57b054de', _decode_puddle_control_phase_data_0x57b054de),
    0xa8cc48b3: ('start_sound', _decode_start_sound),
}
