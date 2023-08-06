# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.LightParameters import LightParameters
from retro_data_structures.properties.echoes.archetypes.ScannableParameters import ScannableParameters
from retro_data_structures.properties.echoes.archetypes.VisorParameters import VisorParameters
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ActorParameters(BaseProperty):
    lighting: LightParameters = dataclasses.field(default_factory=LightParameters)
    scannable: ScannableParameters = dataclasses.field(default_factory=ScannableParameters)
    dark_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    dark_skin: AssetId = dataclasses.field(metadata={'asset_types': ['CSKR']}, default=default_asset_id)
    echo_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    echo_skin: AssetId = dataclasses.field(metadata={'asset_types': ['CSKR']}, default=default_asset_id)
    use_global_render_time: bool = dataclasses.field(default=True)
    fade_in_time: float = dataclasses.field(default=1.0)
    fade_out_time: float = dataclasses.field(default=1.0)
    visor: VisorParameters = dataclasses.field(default_factory=VisorParameters)
    unknown_0xcd4c81a1: bool = dataclasses.field(default=False)
    force_render_unsorted: bool = dataclasses.field(default=False)
    takes_projected_shadow: bool = dataclasses.field(default=True)
    unknown_0xf07981e8: bool = dataclasses.field(default=False)
    unknown_0x6df33845: bool = dataclasses.field(default=False)
    max_volume: int = dataclasses.field(default=127)
    max_echo_volume: int = dataclasses.field(default=127)

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
        data.write(b'\x00\x11')  # 17 properties

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

        data.write(b'\xc0\xba\x9e\x18')  # 0xc0ba9e18
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.dark_model))

        data.write(b'\x9f\x02}\x91')  # 0x9f027d91
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.dark_skin))

        data.write(b'k\x1f\xbc:')  # 0x6b1fbc3a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.echo_model))

        data.write(b'\xeb\x1d\x06\xbe')  # 0xeb1d06be
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.echo_skin))

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

        data.write(b'\xcdL\x81\xa1')  # 0xcd4c81a1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xcd4c81a1))

        data.write(b'y\x92c\xf1')  # 0x799263f1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.force_render_unsorted))

        data.write(b'\xed:n\x87')  # 0xed3a6e87
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.takes_projected_shadow))

        data.write(b'\xf0y\x81\xe8')  # 0xf07981e8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xf07981e8))

        data.write(b'm\xf38E')  # 0x6df33845
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x6df33845))

        data.write(b'\xc7\x12\x84|')  # 0xc712847c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_volume))

        data.write(b'\xba&\x00\xd7')  # 0xba2600d7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_echo_volume))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            lighting=LightParameters.from_json(data['lighting']),
            scannable=ScannableParameters.from_json(data['scannable']),
            dark_model=data['dark_model'],
            dark_skin=data['dark_skin'],
            echo_model=data['echo_model'],
            echo_skin=data['echo_skin'],
            use_global_render_time=data['use_global_render_time'],
            fade_in_time=data['fade_in_time'],
            fade_out_time=data['fade_out_time'],
            visor=VisorParameters.from_json(data['visor']),
            unknown_0xcd4c81a1=data['unknown_0xcd4c81a1'],
            force_render_unsorted=data['force_render_unsorted'],
            takes_projected_shadow=data['takes_projected_shadow'],
            unknown_0xf07981e8=data['unknown_0xf07981e8'],
            unknown_0x6df33845=data['unknown_0x6df33845'],
            max_volume=data['max_volume'],
            max_echo_volume=data['max_echo_volume'],
        )

    def to_json(self) -> dict:
        return {
            'lighting': self.lighting.to_json(),
            'scannable': self.scannable.to_json(),
            'dark_model': self.dark_model,
            'dark_skin': self.dark_skin,
            'echo_model': self.echo_model,
            'echo_skin': self.echo_skin,
            'use_global_render_time': self.use_global_render_time,
            'fade_in_time': self.fade_in_time,
            'fade_out_time': self.fade_out_time,
            'visor': self.visor.to_json(),
            'unknown_0xcd4c81a1': self.unknown_0xcd4c81a1,
            'force_render_unsorted': self.force_render_unsorted,
            'takes_projected_shadow': self.takes_projected_shadow,
            'unknown_0xf07981e8': self.unknown_0xf07981e8,
            'unknown_0x6df33845': self.unknown_0x6df33845,
            'max_volume': self.max_volume,
            'max_echo_volume': self.max_echo_volume,
        }

    def _dependencies_for_lighting(self, asset_manager):
        yield from self.lighting.dependencies_for(asset_manager)

    def _dependencies_for_scannable(self, asset_manager):
        yield from self.scannable.dependencies_for(asset_manager)

    def _dependencies_for_dark_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.dark_model)

    def _dependencies_for_dark_skin(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.dark_skin)

    def _dependencies_for_echo_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.echo_model)

    def _dependencies_for_echo_skin(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.echo_skin)

    def _dependencies_for_visor(self, asset_manager):
        yield from self.visor.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_lighting, "lighting", "LightParameters"),
            (self._dependencies_for_scannable, "scannable", "ScannableParameters"),
            (self._dependencies_for_dark_model, "dark_model", "AssetId"),
            (self._dependencies_for_dark_skin, "dark_skin", "AssetId"),
            (self._dependencies_for_echo_model, "echo_model", "AssetId"),
            (self._dependencies_for_echo_skin, "echo_skin", "AssetId"),
            (self._dependencies_for_visor, "visor", "VisorParameters"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for ActorParameters.{field_name} ({field_type}): {e}"
                )


def _decode_lighting(data: typing.BinaryIO, property_size: int):
    return LightParameters.from_stream(data, property_size)


def _decode_scannable(data: typing.BinaryIO, property_size: int):
    return ScannableParameters.from_stream(data, property_size)


def _decode_dark_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_dark_skin(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_echo_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_echo_skin(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_use_global_render_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_visor(data: typing.BinaryIO, property_size: int):
    return VisorParameters.from_stream(data, property_size)


def _decode_unknown_0xcd4c81a1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_force_render_unsorted(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_takes_projected_shadow(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xf07981e8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x6df33845(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_max_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_max_echo_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb028db0e: ('lighting', _decode_lighting),
    0x375bfd7c: ('scannable', _decode_scannable),
    0xc0ba9e18: ('dark_model', _decode_dark_model),
    0x9f027d91: ('dark_skin', _decode_dark_skin),
    0x6b1fbc3a: ('echo_model', _decode_echo_model),
    0xeb1d06be: ('echo_skin', _decode_echo_skin),
    0x1499803c: ('use_global_render_time', _decode_use_global_render_time),
    0x90aa341f: ('fade_in_time', _decode_fade_in_time),
    0x7c269ebc: ('fade_out_time', _decode_fade_out_time),
    0x5ad250e: ('visor', _decode_visor),
    0xcd4c81a1: ('unknown_0xcd4c81a1', _decode_unknown_0xcd4c81a1),
    0x799263f1: ('force_render_unsorted', _decode_force_render_unsorted),
    0xed3a6e87: ('takes_projected_shadow', _decode_takes_projected_shadow),
    0xf07981e8: ('unknown_0xf07981e8', _decode_unknown_0xf07981e8),
    0x6df33845: ('unknown_0x6df33845', _decode_unknown_0x6df33845),
    0xc712847c: ('max_volume', _decode_max_volume),
    0xba2600d7: ('max_echo_volume', _decode_max_echo_volume),
}
