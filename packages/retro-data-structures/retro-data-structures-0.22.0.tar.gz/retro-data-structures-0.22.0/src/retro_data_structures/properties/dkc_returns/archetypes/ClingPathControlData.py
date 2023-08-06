# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.MaterialType import MaterialType


@dataclasses.dataclass()
class ClingPathControlData(BaseProperty):
    cling_path_control_struct: MaterialType = dataclasses.field(default_factory=MaterialType)
    can_player_walk_off_cling: bool = dataclasses.field(default=False)
    lock_distance_override: float = dataclasses.field(default=0.0)
    use_fixed_lateral_jump: enums.UseFixedLateralJump = dataclasses.field(default=enums.UseFixedLateralJump.Unknown1)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xfa\x16h\x86')  # 0xfa166886
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.cling_path_control_struct.to_stream(data, default_override={'material_type': 4042527608})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf7\x0b\xef\xc0')  # 0xf70befc0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_player_walk_off_cling))

        data.write(b'\xd7\xd2\xb3\xde')  # 0xd7d2b3de
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lock_distance_override))

        data.write(b"\x8c\x99'\xc2")  # 0x8c9927c2
        data.write(b'\x00\x04')  # size
        self.use_fixed_lateral_jump.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            cling_path_control_struct=MaterialType.from_json(data['cling_path_control_struct']),
            can_player_walk_off_cling=data['can_player_walk_off_cling'],
            lock_distance_override=data['lock_distance_override'],
            use_fixed_lateral_jump=enums.UseFixedLateralJump.from_json(data['use_fixed_lateral_jump']),
        )

    def to_json(self) -> dict:
        return {
            'cling_path_control_struct': self.cling_path_control_struct.to_json(),
            'can_player_walk_off_cling': self.can_player_walk_off_cling,
            'lock_distance_override': self.lock_distance_override,
            'use_fixed_lateral_jump': self.use_fixed_lateral_jump.to_json(),
        }


def _decode_cling_path_control_struct(data: typing.BinaryIO, property_size: int):
    return MaterialType.from_stream(data, property_size, default_override={'material_type': 4042527608})


def _decode_can_player_walk_off_cling(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_lock_distance_override(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_use_fixed_lateral_jump(data: typing.BinaryIO, property_size: int):
    return enums.UseFixedLateralJump.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xfa166886: ('cling_path_control_struct', _decode_cling_path_control_struct),
    0xf70befc0: ('can_player_walk_off_cling', _decode_can_player_walk_off_cling),
    0xd7d2b3de: ('lock_distance_override', _decode_lock_distance_override),
    0x8c9927c2: ('use_fixed_lateral_jump', _decode_use_fixed_lateral_jump),
}
