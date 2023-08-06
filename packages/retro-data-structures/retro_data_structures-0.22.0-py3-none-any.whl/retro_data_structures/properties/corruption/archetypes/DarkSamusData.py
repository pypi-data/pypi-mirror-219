# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.ShockWaveInfo import ShockWaveInfo


@dataclasses.dataclass()
class DarkSamusData(BaseProperty):
    unknown_0xfbc0f458: float = dataclasses.field(default=0.0)
    unknown_0x7d5486f6: float = dataclasses.field(default=625.0)
    unknown_0xb6085553: float = dataclasses.field(default=625.0)
    unknown_0xab0d65eb: float = dataclasses.field(default=510.0)
    unknown_0x6051b64e: float = dataclasses.field(default=400.0)
    unknown_0xfd5398eb: float = dataclasses.field(default=-1.0)
    unknown_0x7bc7ea45: float = dataclasses.field(default=-1.0)
    unknown_0xb09b39e0: float = dataclasses.field(default=-1.0)
    unknown_0xad9e0958: float = dataclasses.field(default=-1.0)
    unknown_0x66c2dafd: float = dataclasses.field(default=-1.0)
    unknown_0xf3dba20b: float = dataclasses.field(default=11.0)
    unknown_0x754fd0a5: float = dataclasses.field(default=11.0)
    unknown_0xbe130300: float = dataclasses.field(default=10.0)
    unknown_0xa31633b8: float = dataclasses.field(default=10.0)
    unknown_0x684ae01d: float = dataclasses.field(default=9.0)
    unknown_0xa3ad3caf: int = dataclasses.field(default=0)
    unknown_0xb1189341: int = dataclasses.field(default=2)
    unknown_0x09a4f424: int = dataclasses.field(default=2)
    unknown_0x9473cc9d: int = dataclasses.field(default=2)
    unknown_0x4bf5e22c: float = dataclasses.field(default=0.0)
    unknown_0xcd619082: float = dataclasses.field(default=0.0)
    unknown_0x063d4327: float = dataclasses.field(default=100.0)
    unknown_0x1b38739f: float = dataclasses.field(default=100.0)
    unknown_0xd064a03a: float = dataclasses.field(default=100.0)
    unknown_0x63cd8fea: float = dataclasses.field(default=0.10000000149011612)
    unknown_0xe559fd44: float = dataclasses.field(default=0.20000000298023224)
    unknown_0x2e052ee1: float = dataclasses.field(default=0.30000001192092896)
    unknown_0x33001e59: float = dataclasses.field(default=0.30000001192092896)
    unknown_0xf85ccdfc: float = dataclasses.field(default=0.30000001192092896)
    unknown_0x35c8d201: float = dataclasses.field(default=4.0)
    unknown_0xb35ca0af: float = dataclasses.field(default=3.0)
    unknown_0x7800730a: float = dataclasses.field(default=1.2999999523162842)
    unknown_0x650543b2: float = dataclasses.field(default=0.699999988079071)
    unknown_0xae599017: float = dataclasses.field(default=0.30000001192092896)
    unknown_0x781cc1e9: float = dataclasses.field(default=750.0)
    unknown_0xc377b3c1: float = dataclasses.field(default=375.0)
    unknown_0x0df4b149: float = dataclasses.field(default=21.0)
    melee_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    mega_blaster_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    mega_boost_trail_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    damage_info_0x429c17bd: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    damage_info_0x995aa633: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    shock_wave_info: ShockWaveInfo = dataclasses.field(default_factory=ShockWaveInfo)
    homing_missile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    echo_health: float = dataclasses.field(default=360.0)
    energy_wave_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    echo_blast_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    super_loop_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    damage_info_0xcaa6ecee: DamageInfo = dataclasses.field(default_factory=DamageInfo)

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
        data.write(b'\x001')  # 49 properties

        data.write(b'\xfb\xc0\xf4X')  # 0xfbc0f458
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfbc0f458))

        data.write(b'}T\x86\xf6')  # 0x7d5486f6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7d5486f6))

        data.write(b'\xb6\x08US')  # 0xb6085553
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb6085553))

        data.write(b'\xab\re\xeb')  # 0xab0d65eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xab0d65eb))

        data.write(b'`Q\xb6N')  # 0x6051b64e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6051b64e))

        data.write(b'\xfdS\x98\xeb')  # 0xfd5398eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfd5398eb))

        data.write(b'{\xc7\xeaE')  # 0x7bc7ea45
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7bc7ea45))

        data.write(b'\xb0\x9b9\xe0')  # 0xb09b39e0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb09b39e0))

        data.write(b'\xad\x9e\tX')  # 0xad9e0958
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xad9e0958))

        data.write(b'f\xc2\xda\xfd')  # 0x66c2dafd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x66c2dafd))

        data.write(b'\xf3\xdb\xa2\x0b')  # 0xf3dba20b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf3dba20b))

        data.write(b'uO\xd0\xa5')  # 0x754fd0a5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x754fd0a5))

        data.write(b'\xbe\x13\x03\x00')  # 0xbe130300
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbe130300))

        data.write(b'\xa3\x163\xb8')  # 0xa31633b8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa31633b8))

        data.write(b'hJ\xe0\x1d')  # 0x684ae01d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x684ae01d))

        data.write(b'\xa3\xad<\xaf')  # 0xa3ad3caf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xa3ad3caf))

        data.write(b'\xb1\x18\x93A')  # 0xb1189341
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xb1189341))

        data.write(b'\t\xa4\xf4$')  # 0x9a4f424
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x09a4f424))

        data.write(b'\x94s\xcc\x9d')  # 0x9473cc9d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x9473cc9d))

        data.write(b'K\xf5\xe2,')  # 0x4bf5e22c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4bf5e22c))

        data.write(b'\xcda\x90\x82')  # 0xcd619082
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcd619082))

        data.write(b"\x06=C'")  # 0x63d4327
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x063d4327))

        data.write(b'\x1b8s\x9f')  # 0x1b38739f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1b38739f))

        data.write(b'\xd0d\xa0:')  # 0xd064a03a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd064a03a))

        data.write(b'c\xcd\x8f\xea')  # 0x63cd8fea
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x63cd8fea))

        data.write(b'\xe5Y\xfdD')  # 0xe559fd44
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe559fd44))

        data.write(b'.\x05.\xe1')  # 0x2e052ee1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2e052ee1))

        data.write(b'3\x00\x1eY')  # 0x33001e59
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x33001e59))

        data.write(b'\xf8\\\xcd\xfc')  # 0xf85ccdfc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf85ccdfc))

        data.write(b'5\xc8\xd2\x01')  # 0x35c8d201
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x35c8d201))

        data.write(b'\xb3\\\xa0\xaf')  # 0xb35ca0af
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb35ca0af))

        data.write(b'x\x00s\n')  # 0x7800730a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7800730a))

        data.write(b'e\x05C\xb2')  # 0x650543b2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x650543b2))

        data.write(b'\xaeY\x90\x17')  # 0xae599017
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xae599017))

        data.write(b'x\x1c\xc1\xe9')  # 0x781cc1e9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x781cc1e9))

        data.write(b'\xc3w\xb3\xc1')  # 0xc377b3c1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc377b3c1))

        data.write(b'\r\xf4\xb1I')  # 0xdf4b149
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0df4b149))

        data.write(b'\xc9A`4')  # 0xc9416034
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.melee_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'A@F\xa8')  # 0x414046a8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mega_blaster_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa0\xe0\xd7\xf8')  # 0xa0e0d7f8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mega_boost_trail_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'B\x9c\x17\xbd')  # 0x429c17bd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0x429c17bd.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x99Z\xa63')  # 0x995aa633
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0x995aa633.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'UW\x11\x99')  # 0x55571199
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shock_wave_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Y\x8c\x00\x05')  # 0x598c0005
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.homing_missile_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'K\xc4\xae\\')  # 0x4bc4ae5c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.echo_health))

        data.write(b'\x93\xec\xf9E')  # 0x93ecf945
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.energy_wave_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xae\xf2\xf8W')  # 0xaef2f857
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.echo_blast_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd7O\xc7l')  # 0xd74fc76c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.super_loop_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xca\xa6\xec\xee')  # 0xcaa6ecee
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0xcaa6ecee.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xfbc0f458=data['unknown_0xfbc0f458'],
            unknown_0x7d5486f6=data['unknown_0x7d5486f6'],
            unknown_0xb6085553=data['unknown_0xb6085553'],
            unknown_0xab0d65eb=data['unknown_0xab0d65eb'],
            unknown_0x6051b64e=data['unknown_0x6051b64e'],
            unknown_0xfd5398eb=data['unknown_0xfd5398eb'],
            unknown_0x7bc7ea45=data['unknown_0x7bc7ea45'],
            unknown_0xb09b39e0=data['unknown_0xb09b39e0'],
            unknown_0xad9e0958=data['unknown_0xad9e0958'],
            unknown_0x66c2dafd=data['unknown_0x66c2dafd'],
            unknown_0xf3dba20b=data['unknown_0xf3dba20b'],
            unknown_0x754fd0a5=data['unknown_0x754fd0a5'],
            unknown_0xbe130300=data['unknown_0xbe130300'],
            unknown_0xa31633b8=data['unknown_0xa31633b8'],
            unknown_0x684ae01d=data['unknown_0x684ae01d'],
            unknown_0xa3ad3caf=data['unknown_0xa3ad3caf'],
            unknown_0xb1189341=data['unknown_0xb1189341'],
            unknown_0x09a4f424=data['unknown_0x09a4f424'],
            unknown_0x9473cc9d=data['unknown_0x9473cc9d'],
            unknown_0x4bf5e22c=data['unknown_0x4bf5e22c'],
            unknown_0xcd619082=data['unknown_0xcd619082'],
            unknown_0x063d4327=data['unknown_0x063d4327'],
            unknown_0x1b38739f=data['unknown_0x1b38739f'],
            unknown_0xd064a03a=data['unknown_0xd064a03a'],
            unknown_0x63cd8fea=data['unknown_0x63cd8fea'],
            unknown_0xe559fd44=data['unknown_0xe559fd44'],
            unknown_0x2e052ee1=data['unknown_0x2e052ee1'],
            unknown_0x33001e59=data['unknown_0x33001e59'],
            unknown_0xf85ccdfc=data['unknown_0xf85ccdfc'],
            unknown_0x35c8d201=data['unknown_0x35c8d201'],
            unknown_0xb35ca0af=data['unknown_0xb35ca0af'],
            unknown_0x7800730a=data['unknown_0x7800730a'],
            unknown_0x650543b2=data['unknown_0x650543b2'],
            unknown_0xae599017=data['unknown_0xae599017'],
            unknown_0x781cc1e9=data['unknown_0x781cc1e9'],
            unknown_0xc377b3c1=data['unknown_0xc377b3c1'],
            unknown_0x0df4b149=data['unknown_0x0df4b149'],
            melee_damage=DamageInfo.from_json(data['melee_damage']),
            mega_blaster_damage=DamageInfo.from_json(data['mega_blaster_damage']),
            mega_boost_trail_damage=DamageInfo.from_json(data['mega_boost_trail_damage']),
            damage_info_0x429c17bd=DamageInfo.from_json(data['damage_info_0x429c17bd']),
            damage_info_0x995aa633=DamageInfo.from_json(data['damage_info_0x995aa633']),
            shock_wave_info=ShockWaveInfo.from_json(data['shock_wave_info']),
            homing_missile_damage=DamageInfo.from_json(data['homing_missile_damage']),
            echo_health=data['echo_health'],
            energy_wave_damage=DamageInfo.from_json(data['energy_wave_damage']),
            echo_blast_damage=DamageInfo.from_json(data['echo_blast_damage']),
            super_loop_damage=DamageInfo.from_json(data['super_loop_damage']),
            damage_info_0xcaa6ecee=DamageInfo.from_json(data['damage_info_0xcaa6ecee']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xfbc0f458': self.unknown_0xfbc0f458,
            'unknown_0x7d5486f6': self.unknown_0x7d5486f6,
            'unknown_0xb6085553': self.unknown_0xb6085553,
            'unknown_0xab0d65eb': self.unknown_0xab0d65eb,
            'unknown_0x6051b64e': self.unknown_0x6051b64e,
            'unknown_0xfd5398eb': self.unknown_0xfd5398eb,
            'unknown_0x7bc7ea45': self.unknown_0x7bc7ea45,
            'unknown_0xb09b39e0': self.unknown_0xb09b39e0,
            'unknown_0xad9e0958': self.unknown_0xad9e0958,
            'unknown_0x66c2dafd': self.unknown_0x66c2dafd,
            'unknown_0xf3dba20b': self.unknown_0xf3dba20b,
            'unknown_0x754fd0a5': self.unknown_0x754fd0a5,
            'unknown_0xbe130300': self.unknown_0xbe130300,
            'unknown_0xa31633b8': self.unknown_0xa31633b8,
            'unknown_0x684ae01d': self.unknown_0x684ae01d,
            'unknown_0xa3ad3caf': self.unknown_0xa3ad3caf,
            'unknown_0xb1189341': self.unknown_0xb1189341,
            'unknown_0x09a4f424': self.unknown_0x09a4f424,
            'unknown_0x9473cc9d': self.unknown_0x9473cc9d,
            'unknown_0x4bf5e22c': self.unknown_0x4bf5e22c,
            'unknown_0xcd619082': self.unknown_0xcd619082,
            'unknown_0x063d4327': self.unknown_0x063d4327,
            'unknown_0x1b38739f': self.unknown_0x1b38739f,
            'unknown_0xd064a03a': self.unknown_0xd064a03a,
            'unknown_0x63cd8fea': self.unknown_0x63cd8fea,
            'unknown_0xe559fd44': self.unknown_0xe559fd44,
            'unknown_0x2e052ee1': self.unknown_0x2e052ee1,
            'unknown_0x33001e59': self.unknown_0x33001e59,
            'unknown_0xf85ccdfc': self.unknown_0xf85ccdfc,
            'unknown_0x35c8d201': self.unknown_0x35c8d201,
            'unknown_0xb35ca0af': self.unknown_0xb35ca0af,
            'unknown_0x7800730a': self.unknown_0x7800730a,
            'unknown_0x650543b2': self.unknown_0x650543b2,
            'unknown_0xae599017': self.unknown_0xae599017,
            'unknown_0x781cc1e9': self.unknown_0x781cc1e9,
            'unknown_0xc377b3c1': self.unknown_0xc377b3c1,
            'unknown_0x0df4b149': self.unknown_0x0df4b149,
            'melee_damage': self.melee_damage.to_json(),
            'mega_blaster_damage': self.mega_blaster_damage.to_json(),
            'mega_boost_trail_damage': self.mega_boost_trail_damage.to_json(),
            'damage_info_0x429c17bd': self.damage_info_0x429c17bd.to_json(),
            'damage_info_0x995aa633': self.damage_info_0x995aa633.to_json(),
            'shock_wave_info': self.shock_wave_info.to_json(),
            'homing_missile_damage': self.homing_missile_damage.to_json(),
            'echo_health': self.echo_health,
            'energy_wave_damage': self.energy_wave_damage.to_json(),
            'echo_blast_damage': self.echo_blast_damage.to_json(),
            'super_loop_damage': self.super_loop_damage.to_json(),
            'damage_info_0xcaa6ecee': self.damage_info_0xcaa6ecee.to_json(),
        }


def _decode_unknown_0xfbc0f458(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7d5486f6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb6085553(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xab0d65eb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6051b64e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xfd5398eb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7bc7ea45(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb09b39e0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xad9e0958(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x66c2dafd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf3dba20b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x754fd0a5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbe130300(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa31633b8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x684ae01d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa3ad3caf(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xb1189341(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x09a4f424(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x9473cc9d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x4bf5e22c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcd619082(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x063d4327(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1b38739f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd064a03a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x63cd8fea(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe559fd44(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2e052ee1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x33001e59(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf85ccdfc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x35c8d201(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb35ca0af(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7800730a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x650543b2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xae599017(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x781cc1e9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc377b3c1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0df4b149(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_melee_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_mega_blaster_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_mega_boost_trail_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_damage_info_0x429c17bd(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_damage_info_0x995aa633(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_shock_wave_info(data: typing.BinaryIO, property_size: int):
    return ShockWaveInfo.from_stream(data, property_size)


def _decode_homing_missile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_echo_health(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_energy_wave_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_echo_blast_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_super_loop_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_damage_info_0xcaa6ecee(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xfbc0f458: ('unknown_0xfbc0f458', _decode_unknown_0xfbc0f458),
    0x7d5486f6: ('unknown_0x7d5486f6', _decode_unknown_0x7d5486f6),
    0xb6085553: ('unknown_0xb6085553', _decode_unknown_0xb6085553),
    0xab0d65eb: ('unknown_0xab0d65eb', _decode_unknown_0xab0d65eb),
    0x6051b64e: ('unknown_0x6051b64e', _decode_unknown_0x6051b64e),
    0xfd5398eb: ('unknown_0xfd5398eb', _decode_unknown_0xfd5398eb),
    0x7bc7ea45: ('unknown_0x7bc7ea45', _decode_unknown_0x7bc7ea45),
    0xb09b39e0: ('unknown_0xb09b39e0', _decode_unknown_0xb09b39e0),
    0xad9e0958: ('unknown_0xad9e0958', _decode_unknown_0xad9e0958),
    0x66c2dafd: ('unknown_0x66c2dafd', _decode_unknown_0x66c2dafd),
    0xf3dba20b: ('unknown_0xf3dba20b', _decode_unknown_0xf3dba20b),
    0x754fd0a5: ('unknown_0x754fd0a5', _decode_unknown_0x754fd0a5),
    0xbe130300: ('unknown_0xbe130300', _decode_unknown_0xbe130300),
    0xa31633b8: ('unknown_0xa31633b8', _decode_unknown_0xa31633b8),
    0x684ae01d: ('unknown_0x684ae01d', _decode_unknown_0x684ae01d),
    0xa3ad3caf: ('unknown_0xa3ad3caf', _decode_unknown_0xa3ad3caf),
    0xb1189341: ('unknown_0xb1189341', _decode_unknown_0xb1189341),
    0x9a4f424: ('unknown_0x09a4f424', _decode_unknown_0x09a4f424),
    0x9473cc9d: ('unknown_0x9473cc9d', _decode_unknown_0x9473cc9d),
    0x4bf5e22c: ('unknown_0x4bf5e22c', _decode_unknown_0x4bf5e22c),
    0xcd619082: ('unknown_0xcd619082', _decode_unknown_0xcd619082),
    0x63d4327: ('unknown_0x063d4327', _decode_unknown_0x063d4327),
    0x1b38739f: ('unknown_0x1b38739f', _decode_unknown_0x1b38739f),
    0xd064a03a: ('unknown_0xd064a03a', _decode_unknown_0xd064a03a),
    0x63cd8fea: ('unknown_0x63cd8fea', _decode_unknown_0x63cd8fea),
    0xe559fd44: ('unknown_0xe559fd44', _decode_unknown_0xe559fd44),
    0x2e052ee1: ('unknown_0x2e052ee1', _decode_unknown_0x2e052ee1),
    0x33001e59: ('unknown_0x33001e59', _decode_unknown_0x33001e59),
    0xf85ccdfc: ('unknown_0xf85ccdfc', _decode_unknown_0xf85ccdfc),
    0x35c8d201: ('unknown_0x35c8d201', _decode_unknown_0x35c8d201),
    0xb35ca0af: ('unknown_0xb35ca0af', _decode_unknown_0xb35ca0af),
    0x7800730a: ('unknown_0x7800730a', _decode_unknown_0x7800730a),
    0x650543b2: ('unknown_0x650543b2', _decode_unknown_0x650543b2),
    0xae599017: ('unknown_0xae599017', _decode_unknown_0xae599017),
    0x781cc1e9: ('unknown_0x781cc1e9', _decode_unknown_0x781cc1e9),
    0xc377b3c1: ('unknown_0xc377b3c1', _decode_unknown_0xc377b3c1),
    0xdf4b149: ('unknown_0x0df4b149', _decode_unknown_0x0df4b149),
    0xc9416034: ('melee_damage', _decode_melee_damage),
    0x414046a8: ('mega_blaster_damage', _decode_mega_blaster_damage),
    0xa0e0d7f8: ('mega_boost_trail_damage', _decode_mega_boost_trail_damage),
    0x429c17bd: ('damage_info_0x429c17bd', _decode_damage_info_0x429c17bd),
    0x995aa633: ('damage_info_0x995aa633', _decode_damage_info_0x995aa633),
    0x55571199: ('shock_wave_info', _decode_shock_wave_info),
    0x598c0005: ('homing_missile_damage', _decode_homing_missile_damage),
    0x4bc4ae5c: ('echo_health', _decode_echo_health),
    0x93ecf945: ('energy_wave_damage', _decode_energy_wave_damage),
    0xaef2f857: ('echo_blast_damage', _decode_echo_blast_damage),
    0xd74fc76c: ('super_loop_damage', _decode_super_loop_damage),
    0xcaa6ecee: ('damage_info_0xcaa6ecee', _decode_damage_info_0xcaa6ecee),
}
