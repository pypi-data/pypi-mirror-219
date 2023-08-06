# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.SeedBoss1Action import SeedBoss1Action


@dataclasses.dataclass()
class SeedBoss1Stage(BaseProperty):
    anim_playback_rate: float = dataclasses.field(default=1.0)
    min_health_percentage: float = dataclasses.field(default=0.0)
    unknown_0x95e7a2c2: float = dataclasses.field(default=0.0)
    unknown_0x76ba1c18: float = dataclasses.field(default=0.0)
    unknown_0xcd4edca2: float = dataclasses.field(default=0.0)
    unknown_0xf9b082b0: float = dataclasses.field(default=0.0)
    time_before_orb_grab: float = dataclasses.field(default=5.0)
    unknown_0x905063f4: bool = dataclasses.field(default=False)
    unknown_0xbae5eabb: bool = dataclasses.field(default=False)
    can_energize: bool = dataclasses.field(default=False)
    unknown_0x40c60cfc: float = dataclasses.field(default=5.0)
    unknown_0x69b8f1e4: float = dataclasses.field(default=15.0)
    unknown_0xae7dd037: float = dataclasses.field(default=1.0)
    unknown_0x90c818bf: float = dataclasses.field(default=1.0)
    unknown_0xc31d15ee: float = dataclasses.field(default=0.25)
    reverse_direction_chance: float = dataclasses.field(default=0.25)
    hand_projectile: SeedBoss1Action = dataclasses.field(default_factory=SeedBoss1Action)
    seed_boss1_action_0xbaf37baa: SeedBoss1Action = dataclasses.field(default_factory=SeedBoss1Action)
    unknown_0xaf8c9223: float = dataclasses.field(default=0.05999999865889549)
    seed_boss1_action_0xd83d4564: SeedBoss1Action = dataclasses.field(default_factory=SeedBoss1Action)
    seed_boss1_action_0x95b6d3b7: SeedBoss1Action = dataclasses.field(default_factory=SeedBoss1Action)
    charge_player: SeedBoss1Action = dataclasses.field(default_factory=SeedBoss1Action)
    unknown_0x4432c4fe: int = dataclasses.field(default=1)
    unknown_0x2ac6aa4b: float = dataclasses.field(default=3.0)
    unknown_0xdbf10d5e: float = dataclasses.field(default=1.0)

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
        data.write(b'\x00\x19')  # 25 properties

        data.write(b'\x1b\x0eu\xb3')  # 0x1b0e75b3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.anim_playback_rate))

        data.write(b'\xdf\xeaF\xb3')  # 0xdfea46b3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_health_percentage))

        data.write(b'\x95\xe7\xa2\xc2')  # 0x95e7a2c2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x95e7a2c2))

        data.write(b'v\xba\x1c\x18')  # 0x76ba1c18
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x76ba1c18))

        data.write(b'\xcdN\xdc\xa2')  # 0xcd4edca2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcd4edca2))

        data.write(b'\xf9\xb0\x82\xb0')  # 0xf9b082b0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf9b082b0))

        data.write(b'#b\xc4\xe2')  # 0x2362c4e2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.time_before_orb_grab))

        data.write(b'\x90Pc\xf4')  # 0x905063f4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x905063f4))

        data.write(b'\xba\xe5\xea\xbb')  # 0xbae5eabb
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xbae5eabb))

        data.write(b'\x1e:\x93\x94')  # 0x1e3a9394
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_energize))

        data.write(b'@\xc6\x0c\xfc')  # 0x40c60cfc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x40c60cfc))

        data.write(b'i\xb8\xf1\xe4')  # 0x69b8f1e4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x69b8f1e4))

        data.write(b'\xae}\xd07')  # 0xae7dd037
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xae7dd037))

        data.write(b'\x90\xc8\x18\xbf')  # 0x90c818bf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x90c818bf))

        data.write(b'\xc3\x1d\x15\xee')  # 0xc31d15ee
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc31d15ee))

        data.write(b'\xa0Y\xd7_')  # 0xa059d75f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reverse_direction_chance))

        data.write(b'\x1e\x85t9')  # 0x1e857439
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hand_projectile.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xba\xf3{\xaa')  # 0xbaf37baa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.seed_boss1_action_0xbaf37baa.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaf\x8c\x92#')  # 0xaf8c9223
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xaf8c9223))

        data.write(b'\xd8=Ed')  # 0xd83d4564
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.seed_boss1_action_0xd83d4564.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95\xb6\xd3\xb7')  # 0x95b6d3b7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.seed_boss1_action_0x95b6d3b7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'F\xaa\x80\x16')  # 0x46aa8016
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.charge_player.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'D2\xc4\xfe')  # 0x4432c4fe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x4432c4fe))

        data.write(b'*\xc6\xaaK')  # 0x2ac6aa4b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2ac6aa4b))

        data.write(b'\xdb\xf1\r^')  # 0xdbf10d5e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xdbf10d5e))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            anim_playback_rate=data['anim_playback_rate'],
            min_health_percentage=data['min_health_percentage'],
            unknown_0x95e7a2c2=data['unknown_0x95e7a2c2'],
            unknown_0x76ba1c18=data['unknown_0x76ba1c18'],
            unknown_0xcd4edca2=data['unknown_0xcd4edca2'],
            unknown_0xf9b082b0=data['unknown_0xf9b082b0'],
            time_before_orb_grab=data['time_before_orb_grab'],
            unknown_0x905063f4=data['unknown_0x905063f4'],
            unknown_0xbae5eabb=data['unknown_0xbae5eabb'],
            can_energize=data['can_energize'],
            unknown_0x40c60cfc=data['unknown_0x40c60cfc'],
            unknown_0x69b8f1e4=data['unknown_0x69b8f1e4'],
            unknown_0xae7dd037=data['unknown_0xae7dd037'],
            unknown_0x90c818bf=data['unknown_0x90c818bf'],
            unknown_0xc31d15ee=data['unknown_0xc31d15ee'],
            reverse_direction_chance=data['reverse_direction_chance'],
            hand_projectile=SeedBoss1Action.from_json(data['hand_projectile']),
            seed_boss1_action_0xbaf37baa=SeedBoss1Action.from_json(data['seed_boss1_action_0xbaf37baa']),
            unknown_0xaf8c9223=data['unknown_0xaf8c9223'],
            seed_boss1_action_0xd83d4564=SeedBoss1Action.from_json(data['seed_boss1_action_0xd83d4564']),
            seed_boss1_action_0x95b6d3b7=SeedBoss1Action.from_json(data['seed_boss1_action_0x95b6d3b7']),
            charge_player=SeedBoss1Action.from_json(data['charge_player']),
            unknown_0x4432c4fe=data['unknown_0x4432c4fe'],
            unknown_0x2ac6aa4b=data['unknown_0x2ac6aa4b'],
            unknown_0xdbf10d5e=data['unknown_0xdbf10d5e'],
        )

    def to_json(self) -> dict:
        return {
            'anim_playback_rate': self.anim_playback_rate,
            'min_health_percentage': self.min_health_percentage,
            'unknown_0x95e7a2c2': self.unknown_0x95e7a2c2,
            'unknown_0x76ba1c18': self.unknown_0x76ba1c18,
            'unknown_0xcd4edca2': self.unknown_0xcd4edca2,
            'unknown_0xf9b082b0': self.unknown_0xf9b082b0,
            'time_before_orb_grab': self.time_before_orb_grab,
            'unknown_0x905063f4': self.unknown_0x905063f4,
            'unknown_0xbae5eabb': self.unknown_0xbae5eabb,
            'can_energize': self.can_energize,
            'unknown_0x40c60cfc': self.unknown_0x40c60cfc,
            'unknown_0x69b8f1e4': self.unknown_0x69b8f1e4,
            'unknown_0xae7dd037': self.unknown_0xae7dd037,
            'unknown_0x90c818bf': self.unknown_0x90c818bf,
            'unknown_0xc31d15ee': self.unknown_0xc31d15ee,
            'reverse_direction_chance': self.reverse_direction_chance,
            'hand_projectile': self.hand_projectile.to_json(),
            'seed_boss1_action_0xbaf37baa': self.seed_boss1_action_0xbaf37baa.to_json(),
            'unknown_0xaf8c9223': self.unknown_0xaf8c9223,
            'seed_boss1_action_0xd83d4564': self.seed_boss1_action_0xd83d4564.to_json(),
            'seed_boss1_action_0x95b6d3b7': self.seed_boss1_action_0x95b6d3b7.to_json(),
            'charge_player': self.charge_player.to_json(),
            'unknown_0x4432c4fe': self.unknown_0x4432c4fe,
            'unknown_0x2ac6aa4b': self.unknown_0x2ac6aa4b,
            'unknown_0xdbf10d5e': self.unknown_0xdbf10d5e,
        }


def _decode_anim_playback_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_health_percentage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x95e7a2c2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x76ba1c18(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcd4edca2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf9b082b0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_time_before_orb_grab(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x905063f4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xbae5eabb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_can_energize(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x40c60cfc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x69b8f1e4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xae7dd037(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x90c818bf(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc31d15ee(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reverse_direction_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hand_projectile(data: typing.BinaryIO, property_size: int):
    return SeedBoss1Action.from_stream(data, property_size)


def _decode_seed_boss1_action_0xbaf37baa(data: typing.BinaryIO, property_size: int):
    return SeedBoss1Action.from_stream(data, property_size)


def _decode_unknown_0xaf8c9223(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_seed_boss1_action_0xd83d4564(data: typing.BinaryIO, property_size: int):
    return SeedBoss1Action.from_stream(data, property_size)


def _decode_seed_boss1_action_0x95b6d3b7(data: typing.BinaryIO, property_size: int):
    return SeedBoss1Action.from_stream(data, property_size)


def _decode_charge_player(data: typing.BinaryIO, property_size: int):
    return SeedBoss1Action.from_stream(data, property_size)


def _decode_unknown_0x4432c4fe(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x2ac6aa4b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xdbf10d5e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1b0e75b3: ('anim_playback_rate', _decode_anim_playback_rate),
    0xdfea46b3: ('min_health_percentage', _decode_min_health_percentage),
    0x95e7a2c2: ('unknown_0x95e7a2c2', _decode_unknown_0x95e7a2c2),
    0x76ba1c18: ('unknown_0x76ba1c18', _decode_unknown_0x76ba1c18),
    0xcd4edca2: ('unknown_0xcd4edca2', _decode_unknown_0xcd4edca2),
    0xf9b082b0: ('unknown_0xf9b082b0', _decode_unknown_0xf9b082b0),
    0x2362c4e2: ('time_before_orb_grab', _decode_time_before_orb_grab),
    0x905063f4: ('unknown_0x905063f4', _decode_unknown_0x905063f4),
    0xbae5eabb: ('unknown_0xbae5eabb', _decode_unknown_0xbae5eabb),
    0x1e3a9394: ('can_energize', _decode_can_energize),
    0x40c60cfc: ('unknown_0x40c60cfc', _decode_unknown_0x40c60cfc),
    0x69b8f1e4: ('unknown_0x69b8f1e4', _decode_unknown_0x69b8f1e4),
    0xae7dd037: ('unknown_0xae7dd037', _decode_unknown_0xae7dd037),
    0x90c818bf: ('unknown_0x90c818bf', _decode_unknown_0x90c818bf),
    0xc31d15ee: ('unknown_0xc31d15ee', _decode_unknown_0xc31d15ee),
    0xa059d75f: ('reverse_direction_chance', _decode_reverse_direction_chance),
    0x1e857439: ('hand_projectile', _decode_hand_projectile),
    0xbaf37baa: ('seed_boss1_action_0xbaf37baa', _decode_seed_boss1_action_0xbaf37baa),
    0xaf8c9223: ('unknown_0xaf8c9223', _decode_unknown_0xaf8c9223),
    0xd83d4564: ('seed_boss1_action_0xd83d4564', _decode_seed_boss1_action_0xd83d4564),
    0x95b6d3b7: ('seed_boss1_action_0x95b6d3b7', _decode_seed_boss1_action_0x95b6d3b7),
    0x46aa8016: ('charge_player', _decode_charge_player),
    0x4432c4fe: ('unknown_0x4432c4fe', _decode_unknown_0x4432c4fe),
    0x2ac6aa4b: ('unknown_0x2ac6aa4b', _decode_unknown_0x2ac6aa4b),
    0xdbf10d5e: ('unknown_0xdbf10d5e', _decode_unknown_0xdbf10d5e),
}
