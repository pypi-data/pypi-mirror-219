# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct30(BaseProperty):
    state_machine: AssetId = dataclasses.field(metadata={'asset_types': ['AFSM', 'FSM2']}, default=default_asset_id)
    health: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    puddle_speed: float = dataclasses.field(default=20.0)
    blob_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0xe8a6e174: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0x1ab2b090: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    puddle_death: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sound_ing_spot_idle: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_ing_spot_move: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_0xb392943a: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_0x24ecc1e9: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_ing_spot_death: int = dataclasses.field(default=0, metadata={'sound': True})
    vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)

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
        data.write(b'\x00\r')  # 13 properties

        data.write(b'UtA`')  # 0x55744160
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.state_machine))

        data.write(b'\xcf\x90\xd1^')  # 0xcf90d15e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.health.to_stream(data, default_override={'hi_knock_back_resistance': 2.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"\xc6\xc1d'")  # 0xc6c16427
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.puddle_speed))

        data.write(b'#g\xf6\x89')  # 0x2367f689
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.blob_effect))

        data.write(b'\xe8\xa6\xe1t')  # 0xe8a6e174
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0xe8a6e174))

        data.write(b'\x1a\xb2\xb0\x90')  # 0x1ab2b090
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x1ab2b090))

        data.write(b'\x1c\xcf\xa4\xba')  # 0x1ccfa4ba
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.puddle_death))

        data.write(b'L\xab0\xa9')  # 0x4cab30a9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_ing_spot_idle))

        data.write(b'\x8f\x83\xbes')  # 0x8f83be73
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_ing_spot_move))

        data.write(b'\xb3\x92\x94:')  # 0xb392943a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_0xb392943a))

        data.write(b'$\xec\xc1\xe9')  # 0x24ecc1e9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_0x24ecc1e9))

        data.write(b'D\x89\x93^')  # 0x4489935e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_ing_spot_death))

        data.write(b'{q\xae\x90')  # 0x7b71ae90
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            state_machine=data['state_machine'],
            health=HealthInfo.from_json(data['health']),
            puddle_speed=data['puddle_speed'],
            blob_effect=data['blob_effect'],
            part_0xe8a6e174=data['part_0xe8a6e174'],
            part_0x1ab2b090=data['part_0x1ab2b090'],
            puddle_death=data['puddle_death'],
            sound_ing_spot_idle=data['sound_ing_spot_idle'],
            sound_ing_spot_move=data['sound_ing_spot_move'],
            sound_0xb392943a=data['sound_0xb392943a'],
            sound_0x24ecc1e9=data['sound_0x24ecc1e9'],
            sound_ing_spot_death=data['sound_ing_spot_death'],
            vulnerability=DamageVulnerability.from_json(data['vulnerability']),
        )

    def to_json(self) -> dict:
        return {
            'state_machine': self.state_machine,
            'health': self.health.to_json(),
            'puddle_speed': self.puddle_speed,
            'blob_effect': self.blob_effect,
            'part_0xe8a6e174': self.part_0xe8a6e174,
            'part_0x1ab2b090': self.part_0x1ab2b090,
            'puddle_death': self.puddle_death,
            'sound_ing_spot_idle': self.sound_ing_spot_idle,
            'sound_ing_spot_move': self.sound_ing_spot_move,
            'sound_0xb392943a': self.sound_0xb392943a,
            'sound_0x24ecc1e9': self.sound_0x24ecc1e9,
            'sound_ing_spot_death': self.sound_ing_spot_death,
            'vulnerability': self.vulnerability.to_json(),
        }

    def _dependencies_for_state_machine(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.state_machine)

    def _dependencies_for_health(self, asset_manager):
        yield from self.health.dependencies_for(asset_manager)

    def _dependencies_for_blob_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.blob_effect)

    def _dependencies_for_part_0xe8a6e174(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0xe8a6e174)

    def _dependencies_for_part_0x1ab2b090(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0x1ab2b090)

    def _dependencies_for_puddle_death(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.puddle_death)

    def _dependencies_for_sound_ing_spot_idle(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_ing_spot_idle)

    def _dependencies_for_sound_ing_spot_move(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_ing_spot_move)

    def _dependencies_for_sound_0xb392943a(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_0xb392943a)

    def _dependencies_for_sound_0x24ecc1e9(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_0x24ecc1e9)

    def _dependencies_for_sound_ing_spot_death(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_ing_spot_death)

    def _dependencies_for_vulnerability(self, asset_manager):
        yield from self.vulnerability.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_state_machine, "state_machine", "AssetId"),
            (self._dependencies_for_health, "health", "HealthInfo"),
            (self._dependencies_for_blob_effect, "blob_effect", "AssetId"),
            (self._dependencies_for_part_0xe8a6e174, "part_0xe8a6e174", "AssetId"),
            (self._dependencies_for_part_0x1ab2b090, "part_0x1ab2b090", "AssetId"),
            (self._dependencies_for_puddle_death, "puddle_death", "AssetId"),
            (self._dependencies_for_sound_ing_spot_idle, "sound_ing_spot_idle", "int"),
            (self._dependencies_for_sound_ing_spot_move, "sound_ing_spot_move", "int"),
            (self._dependencies_for_sound_0xb392943a, "sound_0xb392943a", "int"),
            (self._dependencies_for_sound_0x24ecc1e9, "sound_0x24ecc1e9", "int"),
            (self._dependencies_for_sound_ing_spot_death, "sound_ing_spot_death", "int"),
            (self._dependencies_for_vulnerability, "vulnerability", "DamageVulnerability"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for UnknownStruct30.{field_name} ({field_type}): {e}"
                )


def _decode_state_machine(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_health(data: typing.BinaryIO, property_size: int):
    return HealthInfo.from_stream(data, property_size, default_override={'hi_knock_back_resistance': 2.0})


def _decode_puddle_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_blob_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_part_0xe8a6e174(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_part_0x1ab2b090(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_puddle_death(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sound_ing_spot_idle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_ing_spot_move(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_0xb392943a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_0x24ecc1e9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_ing_spot_death(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x55744160: ('state_machine', _decode_state_machine),
    0xcf90d15e: ('health', _decode_health),
    0xc6c16427: ('puddle_speed', _decode_puddle_speed),
    0x2367f689: ('blob_effect', _decode_blob_effect),
    0xe8a6e174: ('part_0xe8a6e174', _decode_part_0xe8a6e174),
    0x1ab2b090: ('part_0x1ab2b090', _decode_part_0x1ab2b090),
    0x1ccfa4ba: ('puddle_death', _decode_puddle_death),
    0x4cab30a9: ('sound_ing_spot_idle', _decode_sound_ing_spot_idle),
    0x8f83be73: ('sound_ing_spot_move', _decode_sound_ing_spot_move),
    0xb392943a: ('sound_0xb392943a', _decode_sound_0xb392943a),
    0x24ecc1e9: ('sound_0x24ecc1e9', _decode_sound_0x24ecc1e9),
    0x4489935e: ('sound_ing_spot_death', _decode_sound_ing_spot_death),
    0x7b71ae90: ('vulnerability', _decode_vulnerability),
}
