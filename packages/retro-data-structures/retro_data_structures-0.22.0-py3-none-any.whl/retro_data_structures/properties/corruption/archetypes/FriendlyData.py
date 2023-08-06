# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.RagDollData import RagDollData
from retro_data_structures.properties.corruption.archetypes.StaticGeometryTest import StaticGeometryTest
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class FriendlyData(BaseProperty):
    flotsam: bool = dataclasses.field(default=False)
    rag_doll_properties: RagDollData = dataclasses.field(default_factory=RagDollData)
    unknown_0xbf443451: bool = dataclasses.field(default=False)
    invulnerable: bool = dataclasses.field(default=False)
    unknown_0x41baf88d: bool = dataclasses.field(default=True)
    unknown_0xef5671d6: bool = dataclasses.field(default=False)
    unknown_0xa4ae2178: bool = dataclasses.field(default=False)
    avoidance_range: float = dataclasses.field(default=10.0)
    unknown_0x02ac6274: bool = dataclasses.field(default=False)
    unknown_0xaed1fba2: float = dataclasses.field(default=30.0)
    unknown_0xb9a462fd: float = dataclasses.field(default=2.0)
    unknown_0x9888c19c: float = dataclasses.field(default=2.0)
    unknown_0x7f1279e1: float = dataclasses.field(default=1.0)
    can_interrupt_fidget: bool = dataclasses.field(default=False)
    shot_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    sound_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    shot_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    static_geometry_test_0x785c41f5: StaticGeometryTest = dataclasses.field(default_factory=StaticGeometryTest)
    static_geometry_test_0xfc5a0a21: StaticGeometryTest = dataclasses.field(default_factory=StaticGeometryTest)
    burst_fire: AssetId = dataclasses.field(metadata={'asset_types': ['BFRC']}, default=default_asset_id)
    gun_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    use_head_tracking: bool = dataclasses.field(default=True)
    unknown_0x330619ca: float = dataclasses.field(default=10.0)
    unknown_0xa7be5edf: float = dataclasses.field(default=1000.0)
    unknown_0x679e2937: bool = dataclasses.field(default=False)
    unknown_0xf484e0ae: bool = dataclasses.field(default=False)
    unknown_0xec3fde21: float = dataclasses.field(default=60.0)
    unknown_0x24d18b0a: float = dataclasses.field(default=90.0)
    unknown_0x3ea5a256: bool = dataclasses.field(default=True)
    is_grabbable: bool = dataclasses.field(default=False)
    is_a_target: bool = dataclasses.field(default=True)

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
        data.write(b'\x00\x1f')  # 31 properties

        data.write(b'\xc1\xd1\xe4e')  # 0xc1d1e465
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.flotsam))

        data.write(b'\xa1Ip\x1e')  # 0xa149701e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rag_doll_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbfD4Q')  # 0xbf443451
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xbf443451))

        data.write(b'fR\xbd\xd7')  # 0x6652bdd7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.invulnerable))

        data.write(b'A\xba\xf8\x8d')  # 0x41baf88d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x41baf88d))

        data.write(b'\xefVq\xd6')  # 0xef5671d6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xef5671d6))

        data.write(b'\xa4\xae!x')  # 0xa4ae2178
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xa4ae2178))

        data.write(b'P\xa9\xbd\r')  # 0x50a9bd0d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.avoidance_range))

        data.write(b'\x02\xacbt')  # 0x2ac6274
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x02ac6274))

        data.write(b'\xae\xd1\xfb\xa2')  # 0xaed1fba2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xaed1fba2))

        data.write(b'\xb9\xa4b\xfd')  # 0xb9a462fd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb9a462fd))

        data.write(b'\x98\x88\xc1\x9c')  # 0x9888c19c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9888c19c))

        data.write(b'\x7f\x12y\xe1')  # 0x7f1279e1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7f1279e1))

        data.write(b'f-\\\xc9')  # 0x662d5cc9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_interrupt_fidget))

        data.write(b'Q%;\xa3')  # 0x51253ba3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.shot_projectile))

        data.write(b'\x10\xe3\xef\xdd')  # 0x10e3efdd
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_projectile))

        data.write(b'\xce\xa3\x018')  # 0xcea30138
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shot_damage.to_stream(data, default_override={'di_damage': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'x\\A\xf5')  # 0x785c41f5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.static_geometry_test_0x785c41f5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfcZ\n!')  # 0xfc5a0a21
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.static_geometry_test_0xfc5a0a21.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfc4G?')  # 0xfc34473f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.burst_fire))

        data.write(b'P4\x08R')  # 0x50340852
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.gun_model))

        data.write(b'.\xa0\x13\xa6')  # 0x2ea013a6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_head_tracking))

        data.write(b'3\x06\x19\xca')  # 0x330619ca
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x330619ca))

        data.write(b'\xa7\xbe^\xdf')  # 0xa7be5edf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa7be5edf))

        data.write(b'g\x9e)7')  # 0x679e2937
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x679e2937))

        data.write(b'\xf4\x84\xe0\xae')  # 0xf484e0ae
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xf484e0ae))

        data.write(b'\xec?\xde!')  # 0xec3fde21
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xec3fde21))

        data.write(b'$\xd1\x8b\n')  # 0x24d18b0a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x24d18b0a))

        data.write(b'>\xa5\xa2V')  # 0x3ea5a256
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x3ea5a256))

        data.write(b'f\xb0\x99\xe0')  # 0x66b099e0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_grabbable))

        data.write(b'\xf5\xac\xd1.')  # 0xf5acd12e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_a_target))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            flotsam=data['flotsam'],
            rag_doll_properties=RagDollData.from_json(data['rag_doll_properties']),
            unknown_0xbf443451=data['unknown_0xbf443451'],
            invulnerable=data['invulnerable'],
            unknown_0x41baf88d=data['unknown_0x41baf88d'],
            unknown_0xef5671d6=data['unknown_0xef5671d6'],
            unknown_0xa4ae2178=data['unknown_0xa4ae2178'],
            avoidance_range=data['avoidance_range'],
            unknown_0x02ac6274=data['unknown_0x02ac6274'],
            unknown_0xaed1fba2=data['unknown_0xaed1fba2'],
            unknown_0xb9a462fd=data['unknown_0xb9a462fd'],
            unknown_0x9888c19c=data['unknown_0x9888c19c'],
            unknown_0x7f1279e1=data['unknown_0x7f1279e1'],
            can_interrupt_fidget=data['can_interrupt_fidget'],
            shot_projectile=data['shot_projectile'],
            sound_projectile=data['sound_projectile'],
            shot_damage=DamageInfo.from_json(data['shot_damage']),
            static_geometry_test_0x785c41f5=StaticGeometryTest.from_json(data['static_geometry_test_0x785c41f5']),
            static_geometry_test_0xfc5a0a21=StaticGeometryTest.from_json(data['static_geometry_test_0xfc5a0a21']),
            burst_fire=data['burst_fire'],
            gun_model=data['gun_model'],
            use_head_tracking=data['use_head_tracking'],
            unknown_0x330619ca=data['unknown_0x330619ca'],
            unknown_0xa7be5edf=data['unknown_0xa7be5edf'],
            unknown_0x679e2937=data['unknown_0x679e2937'],
            unknown_0xf484e0ae=data['unknown_0xf484e0ae'],
            unknown_0xec3fde21=data['unknown_0xec3fde21'],
            unknown_0x24d18b0a=data['unknown_0x24d18b0a'],
            unknown_0x3ea5a256=data['unknown_0x3ea5a256'],
            is_grabbable=data['is_grabbable'],
            is_a_target=data['is_a_target'],
        )

    def to_json(self) -> dict:
        return {
            'flotsam': self.flotsam,
            'rag_doll_properties': self.rag_doll_properties.to_json(),
            'unknown_0xbf443451': self.unknown_0xbf443451,
            'invulnerable': self.invulnerable,
            'unknown_0x41baf88d': self.unknown_0x41baf88d,
            'unknown_0xef5671d6': self.unknown_0xef5671d6,
            'unknown_0xa4ae2178': self.unknown_0xa4ae2178,
            'avoidance_range': self.avoidance_range,
            'unknown_0x02ac6274': self.unknown_0x02ac6274,
            'unknown_0xaed1fba2': self.unknown_0xaed1fba2,
            'unknown_0xb9a462fd': self.unknown_0xb9a462fd,
            'unknown_0x9888c19c': self.unknown_0x9888c19c,
            'unknown_0x7f1279e1': self.unknown_0x7f1279e1,
            'can_interrupt_fidget': self.can_interrupt_fidget,
            'shot_projectile': self.shot_projectile,
            'sound_projectile': self.sound_projectile,
            'shot_damage': self.shot_damage.to_json(),
            'static_geometry_test_0x785c41f5': self.static_geometry_test_0x785c41f5.to_json(),
            'static_geometry_test_0xfc5a0a21': self.static_geometry_test_0xfc5a0a21.to_json(),
            'burst_fire': self.burst_fire,
            'gun_model': self.gun_model,
            'use_head_tracking': self.use_head_tracking,
            'unknown_0x330619ca': self.unknown_0x330619ca,
            'unknown_0xa7be5edf': self.unknown_0xa7be5edf,
            'unknown_0x679e2937': self.unknown_0x679e2937,
            'unknown_0xf484e0ae': self.unknown_0xf484e0ae,
            'unknown_0xec3fde21': self.unknown_0xec3fde21,
            'unknown_0x24d18b0a': self.unknown_0x24d18b0a,
            'unknown_0x3ea5a256': self.unknown_0x3ea5a256,
            'is_grabbable': self.is_grabbable,
            'is_a_target': self.is_a_target,
        }


def _decode_flotsam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_rag_doll_properties(data: typing.BinaryIO, property_size: int):
    return RagDollData.from_stream(data, property_size)


def _decode_unknown_0xbf443451(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_invulnerable(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x41baf88d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xef5671d6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xa4ae2178(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_avoidance_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x02ac6274(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xaed1fba2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb9a462fd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9888c19c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7f1279e1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_can_interrupt_fidget(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_shot_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_shot_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_damage': 5.0})


def _decode_static_geometry_test_0x785c41f5(data: typing.BinaryIO, property_size: int):
    return StaticGeometryTest.from_stream(data, property_size)


def _decode_static_geometry_test_0xfc5a0a21(data: typing.BinaryIO, property_size: int):
    return StaticGeometryTest.from_stream(data, property_size)


def _decode_burst_fire(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_gun_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_use_head_tracking(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x330619ca(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa7be5edf(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x679e2937(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xf484e0ae(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xec3fde21(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x24d18b0a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3ea5a256(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_grabbable(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_a_target(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc1d1e465: ('flotsam', _decode_flotsam),
    0xa149701e: ('rag_doll_properties', _decode_rag_doll_properties),
    0xbf443451: ('unknown_0xbf443451', _decode_unknown_0xbf443451),
    0x6652bdd7: ('invulnerable', _decode_invulnerable),
    0x41baf88d: ('unknown_0x41baf88d', _decode_unknown_0x41baf88d),
    0xef5671d6: ('unknown_0xef5671d6', _decode_unknown_0xef5671d6),
    0xa4ae2178: ('unknown_0xa4ae2178', _decode_unknown_0xa4ae2178),
    0x50a9bd0d: ('avoidance_range', _decode_avoidance_range),
    0x2ac6274: ('unknown_0x02ac6274', _decode_unknown_0x02ac6274),
    0xaed1fba2: ('unknown_0xaed1fba2', _decode_unknown_0xaed1fba2),
    0xb9a462fd: ('unknown_0xb9a462fd', _decode_unknown_0xb9a462fd),
    0x9888c19c: ('unknown_0x9888c19c', _decode_unknown_0x9888c19c),
    0x7f1279e1: ('unknown_0x7f1279e1', _decode_unknown_0x7f1279e1),
    0x662d5cc9: ('can_interrupt_fidget', _decode_can_interrupt_fidget),
    0x51253ba3: ('shot_projectile', _decode_shot_projectile),
    0x10e3efdd: ('sound_projectile', _decode_sound_projectile),
    0xcea30138: ('shot_damage', _decode_shot_damage),
    0x785c41f5: ('static_geometry_test_0x785c41f5', _decode_static_geometry_test_0x785c41f5),
    0xfc5a0a21: ('static_geometry_test_0xfc5a0a21', _decode_static_geometry_test_0xfc5a0a21),
    0xfc34473f: ('burst_fire', _decode_burst_fire),
    0x50340852: ('gun_model', _decode_gun_model),
    0x2ea013a6: ('use_head_tracking', _decode_use_head_tracking),
    0x330619ca: ('unknown_0x330619ca', _decode_unknown_0x330619ca),
    0xa7be5edf: ('unknown_0xa7be5edf', _decode_unknown_0xa7be5edf),
    0x679e2937: ('unknown_0x679e2937', _decode_unknown_0x679e2937),
    0xf484e0ae: ('unknown_0xf484e0ae', _decode_unknown_0xf484e0ae),
    0xec3fde21: ('unknown_0xec3fde21', _decode_unknown_0xec3fde21),
    0x24d18b0a: ('unknown_0x24d18b0a', _decode_unknown_0x24d18b0a),
    0x3ea5a256: ('unknown_0x3ea5a256', _decode_unknown_0x3ea5a256),
    0x66b099e0: ('is_grabbable', _decode_is_grabbable),
    0xf5acd12e: ('is_a_target', _decode_is_a_target),
}
