# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.CharacterGlueData import CharacterGlueData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerCrushData import PlayerCrushData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerPeriodicAdditiveAnimationData import PlayerPeriodicAdditiveAnimationData
from retro_data_structures.properties.dkc_returns.archetypes.TandemBeam import TandemBeam
from retro_data_structures.properties.dkc_returns.archetypes.TrackObjectModuleData import TrackObjectModuleData


@dataclasses.dataclass()
class UnknownStruct140(BaseProperty):
    unknown: int = dataclasses.field(default=0)
    periodic_additive_animation_data: PlayerPeriodicAdditiveAnimationData = dataclasses.field(default_factory=PlayerPeriodicAdditiveAnimationData)
    crush_data: PlayerCrushData = dataclasses.field(default_factory=PlayerCrushData)
    track_object_module_data: TrackObjectModuleData = dataclasses.field(default_factory=TrackObjectModuleData)
    character_glue: CharacterGlueData = dataclasses.field(default_factory=CharacterGlueData)
    tandem_beam: TandemBeam = dataclasses.field(default_factory=TandemBeam)

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\x94\xdd\x89y')  # 0x94dd8979
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown))

        data.write(b'\x97]\xce\xf7')  # 0x975dcef7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.periodic_additive_animation_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8a\xbb%\xc4')  # 0x8abb25c4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.crush_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf4\xd3\x95\x93')  # 0xf4d39593
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.track_object_module_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9d\x9c\xe3%')  # 0x9d9ce325
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_glue.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'4\xa9y\xa6')  # 0x34a979a6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tandem_beam.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown=data['unknown'],
            periodic_additive_animation_data=PlayerPeriodicAdditiveAnimationData.from_json(data['periodic_additive_animation_data']),
            crush_data=PlayerCrushData.from_json(data['crush_data']),
            track_object_module_data=TrackObjectModuleData.from_json(data['track_object_module_data']),
            character_glue=CharacterGlueData.from_json(data['character_glue']),
            tandem_beam=TandemBeam.from_json(data['tandem_beam']),
        )

    def to_json(self) -> dict:
        return {
            'unknown': self.unknown,
            'periodic_additive_animation_data': self.periodic_additive_animation_data.to_json(),
            'crush_data': self.crush_data.to_json(),
            'track_object_module_data': self.track_object_module_data.to_json(),
            'character_glue': self.character_glue.to_json(),
            'tandem_beam': self.tandem_beam.to_json(),
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_periodic_additive_animation_data(data: typing.BinaryIO, property_size: int):
    return PlayerPeriodicAdditiveAnimationData.from_stream(data, property_size)


def _decode_crush_data(data: typing.BinaryIO, property_size: int):
    return PlayerCrushData.from_stream(data, property_size)


def _decode_track_object_module_data(data: typing.BinaryIO, property_size: int):
    return TrackObjectModuleData.from_stream(data, property_size)


def _decode_character_glue(data: typing.BinaryIO, property_size: int):
    return CharacterGlueData.from_stream(data, property_size)


def _decode_tandem_beam(data: typing.BinaryIO, property_size: int):
    return TandemBeam.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x94dd8979: ('unknown', _decode_unknown),
    0x975dcef7: ('periodic_additive_animation_data', _decode_periodic_additive_animation_data),
    0x8abb25c4: ('crush_data', _decode_crush_data),
    0xf4d39593: ('track_object_module_data', _decode_track_object_module_data),
    0x9d9ce325: ('character_glue', _decode_character_glue),
    0x34a979a6: ('tandem_beam', _decode_tandem_beam),
}
