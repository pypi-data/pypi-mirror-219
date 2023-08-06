# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.prime as enums
from retro_data_structures.properties.prime.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class Trigger(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unnamed: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    force: Vector = dataclasses.field(default_factory=Vector)
    trigger_flags: enums.TriggerFlags = dataclasses.field(default=enums.TriggerFlags(0))
    active: bool = dataclasses.field(default=False)
    deactivate_on_entered: bool = dataclasses.field(default=False)
    deactivate_on_exited: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x4

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        unnamed = DamageInfo.from_stream(data, property_size)
        force = Vector.from_stream(data)
        trigger_flags = enums.TriggerFlags.from_stream(data)
        active = struct.unpack('>?', data.read(1))[0]
        deactivate_on_entered = struct.unpack('>?', data.read(1))[0]
        deactivate_on_exited = struct.unpack('>?', data.read(1))[0]
        return cls(name, position, scale, unnamed, force, trigger_flags, active, deactivate_on_entered, deactivate_on_exited)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\t')  # 9 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.scale.to_stream(data)
        self.unnamed.to_stream(data)
        self.force.to_stream(data)
        self.trigger_flags.to_stream(data)
        data.write(struct.pack('>?', self.active))
        data.write(struct.pack('>?', self.deactivate_on_entered))
        data.write(struct.pack('>?', self.deactivate_on_exited))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            scale=Vector.from_json(data['scale']),
            unnamed=DamageInfo.from_json(data['unnamed']),
            force=Vector.from_json(data['force']),
            trigger_flags=enums.TriggerFlags.from_json(data['trigger_flags']),
            active=data['active'],
            deactivate_on_entered=data['deactivate_on_entered'],
            deactivate_on_exited=data['deactivate_on_exited'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'scale': self.scale.to_json(),
            'unnamed': self.unnamed.to_json(),
            'force': self.force.to_json(),
            'trigger_flags': self.trigger_flags.to_json(),
            'active': self.active,
            'deactivate_on_entered': self.deactivate_on_entered,
            'deactivate_on_exited': self.deactivate_on_exited,
        }

    def _dependencies_for_unnamed(self, asset_manager):
        yield from self.unnamed.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed, "unnamed", "DamageInfo"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Trigger.{field_name} ({field_type}): {e}"
                )
