# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.PlasmaBeamInfo import PlasmaBeamInfo
from retro_data_structures.properties.echoes.archetypes.SandBossStructB import SandBossStructB
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class UnknownStruct41(BaseProperty):
    sand_boss_struct_b_0xb9784f0e: SandBossStructB = dataclasses.field(default_factory=SandBossStructB)
    sand_boss_struct_b_0xb8ae1bdc: SandBossStructB = dataclasses.field(default_factory=SandBossStructB)
    charge_beam_info: PlasmaBeamInfo = dataclasses.field(default_factory=PlasmaBeamInfo)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xb9xO\x0e')  # 0xb9784f0e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sand_boss_struct_b_0xb9784f0e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb8\xae\x1b\xdc')  # 0xb8ae1bdc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sand_boss_struct_b_0xb8ae1bdc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x94\xdad5')  # 0x94da6435
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.charge_beam_info.to_stream(data, default_override={'length': 500.0, 'radius': 1.0, 'expansion_speed': 4.0, 'life_time': 1.0, 'pulse_speed': 20.0, 'shutdown_time': 0.25, 'pulse_effect_scale': 2.0, 'inner_color': Color(r=0.49803900718688965, g=0.49803900718688965, b=0.49803900718688965, a=0.49803900718688965), 'outer_color': Color(r=0.6000000238418579, g=0.6000000238418579, b=0.0, a=0.49803900718688965)})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            sand_boss_struct_b_0xb9784f0e=SandBossStructB.from_json(data['sand_boss_struct_b_0xb9784f0e']),
            sand_boss_struct_b_0xb8ae1bdc=SandBossStructB.from_json(data['sand_boss_struct_b_0xb8ae1bdc']),
            charge_beam_info=PlasmaBeamInfo.from_json(data['charge_beam_info']),
        )

    def to_json(self) -> dict:
        return {
            'sand_boss_struct_b_0xb9784f0e': self.sand_boss_struct_b_0xb9784f0e.to_json(),
            'sand_boss_struct_b_0xb8ae1bdc': self.sand_boss_struct_b_0xb8ae1bdc.to_json(),
            'charge_beam_info': self.charge_beam_info.to_json(),
        }

    def _dependencies_for_sand_boss_struct_b_0xb9784f0e(self, asset_manager):
        yield from self.sand_boss_struct_b_0xb9784f0e.dependencies_for(asset_manager)

    def _dependencies_for_sand_boss_struct_b_0xb8ae1bdc(self, asset_manager):
        yield from self.sand_boss_struct_b_0xb8ae1bdc.dependencies_for(asset_manager)

    def _dependencies_for_charge_beam_info(self, asset_manager):
        yield from self.charge_beam_info.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_sand_boss_struct_b_0xb9784f0e, "sand_boss_struct_b_0xb9784f0e", "SandBossStructB"),
            (self._dependencies_for_sand_boss_struct_b_0xb8ae1bdc, "sand_boss_struct_b_0xb8ae1bdc", "SandBossStructB"),
            (self._dependencies_for_charge_beam_info, "charge_beam_info", "PlasmaBeamInfo"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for UnknownStruct41.{field_name} ({field_type}): {e}"
                )


def _decode_sand_boss_struct_b_0xb9784f0e(data: typing.BinaryIO, property_size: int):
    return SandBossStructB.from_stream(data, property_size)


def _decode_sand_boss_struct_b_0xb8ae1bdc(data: typing.BinaryIO, property_size: int):
    return SandBossStructB.from_stream(data, property_size)


def _decode_charge_beam_info(data: typing.BinaryIO, property_size: int):
    return PlasmaBeamInfo.from_stream(data, property_size, default_override={'length': 500.0, 'radius': 1.0, 'expansion_speed': 4.0, 'life_time': 1.0, 'pulse_speed': 20.0, 'shutdown_time': 0.25, 'pulse_effect_scale': 2.0, 'inner_color': Color(r=0.49803900718688965, g=0.49803900718688965, b=0.49803900718688965, a=0.49803900718688965), 'outer_color': Color(r=0.6000000238418579, g=0.6000000238418579, b=0.0, a=0.49803900718688965)})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb9784f0e: ('sand_boss_struct_b_0xb9784f0e', _decode_sand_boss_struct_b_0xb9784f0e),
    0xb8ae1bdc: ('sand_boss_struct_b_0xb8ae1bdc', _decode_sand_boss_struct_b_0xb8ae1bdc),
    0x94da6435: ('charge_beam_info', _decode_charge_beam_info),
}
