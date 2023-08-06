# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class SeedBoss1HandData(BaseProperty):
    health: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    character_animation_set: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    state_machine: AssetId = dataclasses.field(metadata={'asset_types': ['FSM2']}, default=default_asset_id)
    hand_actor_parameters: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    explosion: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    explosion_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    stop_homing_range: float = dataclasses.field(default=20.0)

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\xcf\x90\xd1^')  # 0xcf90d15e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.health.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'{q\xae\x90')  # 0x7b71ae90
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'q\xa5\xa1\x98')  # 0x71a5a198
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_animation_set.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'UtA`')  # 0x55744160
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.state_machine))

        data.write(b'\xa3\x0e\xe9\x99')  # 0xa30ee999
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hand_actor_parameters.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd8\xc6\xd1\\')  # 0xd8c6d15c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.explosion))

        data.write(b'\x9a\tH\x14')  # 0x9a094814
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.explosion_sound))

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x05:\xe4\xa7')  # 0x53ae4a7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stop_homing_range))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            health=HealthInfo.from_json(data['health']),
            vulnerability=DamageVulnerability.from_json(data['vulnerability']),
            character_animation_set=AnimationParameters.from_json(data['character_animation_set']),
            state_machine=data['state_machine'],
            hand_actor_parameters=ActorParameters.from_json(data['hand_actor_parameters']),
            explosion=data['explosion'],
            explosion_sound=data['explosion_sound'],
            damage=DamageInfo.from_json(data['damage']),
            stop_homing_range=data['stop_homing_range'],
        )

    def to_json(self) -> dict:
        return {
            'health': self.health.to_json(),
            'vulnerability': self.vulnerability.to_json(),
            'character_animation_set': self.character_animation_set.to_json(),
            'state_machine': self.state_machine,
            'hand_actor_parameters': self.hand_actor_parameters.to_json(),
            'explosion': self.explosion,
            'explosion_sound': self.explosion_sound,
            'damage': self.damage.to_json(),
            'stop_homing_range': self.stop_homing_range,
        }


def _decode_health(data: typing.BinaryIO, property_size: int):
    return HealthInfo.from_stream(data, property_size)


def _decode_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_character_animation_set(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_state_machine(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_hand_actor_parameters(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_explosion(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_explosion_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_stop_homing_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xcf90d15e: ('health', _decode_health),
    0x7b71ae90: ('vulnerability', _decode_vulnerability),
    0x71a5a198: ('character_animation_set', _decode_character_animation_set),
    0x55744160: ('state_machine', _decode_state_machine),
    0xa30ee999: ('hand_actor_parameters', _decode_hand_actor_parameters),
    0xd8c6d15c: ('explosion', _decode_explosion),
    0x9a094814: ('explosion_sound', _decode_explosion_sound),
    0x337f9524: ('damage', _decode_damage),
    0x53ae4a7: ('stop_homing_range', _decode_stop_homing_range),
}
