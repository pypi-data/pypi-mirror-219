# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.LightParameters import LightParameters
from retro_data_structures.properties.corruption.archetypes.ScannableParameters import ScannableParameters
from retro_data_structures.properties.corruption.archetypes.VisorParameters import VisorParameters
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ActorParameters(BaseProperty):
    lighting: LightParameters = dataclasses.field(default_factory=LightParameters)
    scannable: ScannableParameters = dataclasses.field(default_factory=ScannableParameters)
    x_ray_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    x_ray_skin: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    use_global_render_time: bool = dataclasses.field(default=True)
    fade_in_time: float = dataclasses.field(default=1.0)
    fade_out_time: float = dataclasses.field(default=1.0)
    visor: VisorParameters = dataclasses.field(default_factory=VisorParameters)
    force_render_unsorted: bool = dataclasses.field(default=False)
    takes_projected_shadow: bool = dataclasses.field(default=True)
    unknown_0xf07981e8: bool = dataclasses.field(default=False)
    unknown_0x4d55f7d4: bool = dataclasses.field(default=False)
    actor_material_type: enums.ActorMaterialType = dataclasses.field(default=enums.ActorMaterialType.kMT_Unknown)
    actor_collision_response: enums.ActorCollisionResponse = dataclasses.field(default=enums.ActorCollisionResponse.kACR_Default)
    max_volume: int = dataclasses.field(default=127)
    is_hostile: bool = dataclasses.field(default=False)

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
        data.write(b'\x00\x10')  # 16 properties

        data.write(b'\xb0(\xdb\x0e')  # 0xb028db0e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.lighting.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'7[\xfd|')  # 0x375bfd7c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scannable.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbbR\xf0\xbe')  # 0xbb52f0be
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.x_ray_model))

        data.write(b'\xc6Gu[')  # 0xc647755b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.x_ray_skin))

        data.write(b'\x14\x99\x80<')  # 0x1499803c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_global_render_time))

        data.write(b'\x90\xaa4\x1f')  # 0x90aa341f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_in_time))

        data.write(b'|&\x9e\xbc')  # 0x7c269ebc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_out_time))

        data.write(b'\x05\xad%\x0e')  # 0x5ad250e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.visor.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'y\x92c\xf1')  # 0x799263f1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.force_render_unsorted))

        data.write(b'\xed:n\x87')  # 0xed3a6e87
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.takes_projected_shadow))

        data.write(b'\xf0y\x81\xe8')  # 0xf07981e8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xf07981e8))

        data.write(b'MU\xf7\xd4')  # 0x4d55f7d4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x4d55f7d4))

        data.write(b'\xe3\x15\xeer')  # 0xe315ee72
        data.write(b'\x00\x04')  # size
        self.actor_material_type.to_stream(data)

        data.write(b'X8\x95\xfa')  # 0x583895fa
        data.write(b'\x00\x04')  # size
        self.actor_collision_response.to_stream(data)

        data.write(b'\xc7\x12\x84|')  # 0xc712847c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_volume))

        data.write(b'p\x1ba\xb3')  # 0x701b61b3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_hostile))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            lighting=LightParameters.from_json(data['lighting']),
            scannable=ScannableParameters.from_json(data['scannable']),
            x_ray_model=data['x_ray_model'],
            x_ray_skin=data['x_ray_skin'],
            use_global_render_time=data['use_global_render_time'],
            fade_in_time=data['fade_in_time'],
            fade_out_time=data['fade_out_time'],
            visor=VisorParameters.from_json(data['visor']),
            force_render_unsorted=data['force_render_unsorted'],
            takes_projected_shadow=data['takes_projected_shadow'],
            unknown_0xf07981e8=data['unknown_0xf07981e8'],
            unknown_0x4d55f7d4=data['unknown_0x4d55f7d4'],
            actor_material_type=enums.ActorMaterialType.from_json(data['actor_material_type']),
            actor_collision_response=enums.ActorCollisionResponse.from_json(data['actor_collision_response']),
            max_volume=data['max_volume'],
            is_hostile=data['is_hostile'],
        )

    def to_json(self) -> dict:
        return {
            'lighting': self.lighting.to_json(),
            'scannable': self.scannable.to_json(),
            'x_ray_model': self.x_ray_model,
            'x_ray_skin': self.x_ray_skin,
            'use_global_render_time': self.use_global_render_time,
            'fade_in_time': self.fade_in_time,
            'fade_out_time': self.fade_out_time,
            'visor': self.visor.to_json(),
            'force_render_unsorted': self.force_render_unsorted,
            'takes_projected_shadow': self.takes_projected_shadow,
            'unknown_0xf07981e8': self.unknown_0xf07981e8,
            'unknown_0x4d55f7d4': self.unknown_0x4d55f7d4,
            'actor_material_type': self.actor_material_type.to_json(),
            'actor_collision_response': self.actor_collision_response.to_json(),
            'max_volume': self.max_volume,
            'is_hostile': self.is_hostile,
        }


def _decode_lighting(data: typing.BinaryIO, property_size: int):
    return LightParameters.from_stream(data, property_size)


def _decode_scannable(data: typing.BinaryIO, property_size: int):
    return ScannableParameters.from_stream(data, property_size)


def _decode_x_ray_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_x_ray_skin(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_use_global_render_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_visor(data: typing.BinaryIO, property_size: int):
    return VisorParameters.from_stream(data, property_size)


def _decode_force_render_unsorted(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_takes_projected_shadow(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xf07981e8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x4d55f7d4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_actor_material_type(data: typing.BinaryIO, property_size: int):
    return enums.ActorMaterialType.from_stream(data)


def _decode_actor_collision_response(data: typing.BinaryIO, property_size: int):
    return enums.ActorCollisionResponse.from_stream(data)


def _decode_max_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_is_hostile(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb028db0e: ('lighting', _decode_lighting),
    0x375bfd7c: ('scannable', _decode_scannable),
    0xbb52f0be: ('x_ray_model', _decode_x_ray_model),
    0xc647755b: ('x_ray_skin', _decode_x_ray_skin),
    0x1499803c: ('use_global_render_time', _decode_use_global_render_time),
    0x90aa341f: ('fade_in_time', _decode_fade_in_time),
    0x7c269ebc: ('fade_out_time', _decode_fade_out_time),
    0x5ad250e: ('visor', _decode_visor),
    0x799263f1: ('force_render_unsorted', _decode_force_render_unsorted),
    0xed3a6e87: ('takes_projected_shadow', _decode_takes_projected_shadow),
    0xf07981e8: ('unknown_0xf07981e8', _decode_unknown_0xf07981e8),
    0x4d55f7d4: ('unknown_0x4d55f7d4', _decode_unknown_0x4d55f7d4),
    0xe315ee72: ('actor_material_type', _decode_actor_material_type),
    0x583895fa: ('actor_collision_response', _decode_actor_collision_response),
    0xc712847c: ('max_volume', _decode_max_volume),
    0x701b61b3: ('is_hostile', _decode_is_hostile),
}
