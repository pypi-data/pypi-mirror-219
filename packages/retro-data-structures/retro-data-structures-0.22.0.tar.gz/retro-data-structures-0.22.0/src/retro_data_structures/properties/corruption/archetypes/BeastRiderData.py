# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.PlasmaBeamInfo import PlasmaBeamInfo
from retro_data_structures.properties.corruption.archetypes.RagDollData import RagDollData
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class BeastRiderData(BaseProperty):
    phazon_lance: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    plasma_beam_info: PlasmaBeamInfo = dataclasses.field(default_factory=PlasmaBeamInfo)
    helmet: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    rag_doll_properties: RagDollData = dataclasses.field(default_factory=RagDollData)
    death_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'\xb3\xa2j\x80')  # 0xb3a26a80
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.phazon_lance))

        data.write(b'\xa6\x00\x1c\xe0')  # 0xa6001ce0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.plasma_beam_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb34?\x83')  # 0xb3343f83
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.helmet))

        data.write(b'\xa1Ip\x1e')  # 0xa149701e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rag_doll_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc7\xc3\xf6\x10')  # 0xc7c3f610
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.death_sound))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            phazon_lance=data['phazon_lance'],
            plasma_beam_info=PlasmaBeamInfo.from_json(data['plasma_beam_info']),
            helmet=data['helmet'],
            rag_doll_properties=RagDollData.from_json(data['rag_doll_properties']),
            death_sound=data['death_sound'],
        )

    def to_json(self) -> dict:
        return {
            'phazon_lance': self.phazon_lance,
            'plasma_beam_info': self.plasma_beam_info.to_json(),
            'helmet': self.helmet,
            'rag_doll_properties': self.rag_doll_properties.to_json(),
            'death_sound': self.death_sound,
        }


def _decode_phazon_lance(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_plasma_beam_info(data: typing.BinaryIO, property_size: int):
    return PlasmaBeamInfo.from_stream(data, property_size)


def _decode_helmet(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_rag_doll_properties(data: typing.BinaryIO, property_size: int):
    return RagDollData.from_stream(data, property_size)


def _decode_death_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb3a26a80: ('phazon_lance', _decode_phazon_lance),
    0xa6001ce0: ('plasma_beam_info', _decode_plasma_beam_info),
    0xb3343f83: ('helmet', _decode_helmet),
    0xa149701e: ('rag_doll_properties', _decode_rag_doll_properties),
    0xc7c3f610: ('death_sound', _decode_death_sound),
}
