# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.TDamageInfo import TDamageInfo


@dataclasses.dataclass()
class CannonBall(BaseProperty):
    cannon_ball_damage: TDamageInfo = dataclasses.field(default_factory=TDamageInfo)

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
        data.write(b'\x00\x01')  # 1 properties

        data.write(b'\xd5\x1d\x8dq')  # 0xd51d8d71
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.cannon_ball_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            cannon_ball_damage=TDamageInfo.from_json(data['cannon_ball_damage']),
        )

    def to_json(self) -> dict:
        return {
            'cannon_ball_damage': self.cannon_ball_damage.to_json(),
        }

    def _dependencies_for_cannon_ball_damage(self, asset_manager):
        yield from self.cannon_ball_damage.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_cannon_ball_damage, "cannon_ball_damage", "TDamageInfo"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for CannonBall.{field_name} ({field_type}): {e}"
                )


def _decode_cannon_ball_damage(data: typing.BinaryIO, property_size: int):
    return TDamageInfo.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd51d8d71: ('cannon_ball_damage', _decode_cannon_ball_damage),
}
