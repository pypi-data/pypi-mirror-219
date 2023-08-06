# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class SpawnPoint(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    power_beam: int = dataclasses.field(default=0)
    ice_beam: int = dataclasses.field(default=0)
    wave_beam: int = dataclasses.field(default=0)
    plasma_beam: int = dataclasses.field(default=0)
    missiles: int = dataclasses.field(default=0)
    scan_visor: int = dataclasses.field(default=0)
    morph_ball_bomb: int = dataclasses.field(default=0)
    power_bombs: int = dataclasses.field(default=0)
    flamethrower: int = dataclasses.field(default=0)
    thermal_visor: int = dataclasses.field(default=0)
    charge_beam: int = dataclasses.field(default=0)
    super_missile: int = dataclasses.field(default=0)
    grapple_beam: int = dataclasses.field(default=0)
    x_ray_visor: int = dataclasses.field(default=0)
    ice_spreader: int = dataclasses.field(default=0)
    space_jump_boots: int = dataclasses.field(default=0)
    morph_ball: int = dataclasses.field(default=0)
    combat_visor: int = dataclasses.field(default=0)
    boost_ball: int = dataclasses.field(default=0)
    spider_ball: int = dataclasses.field(default=0)
    power_suit: int = dataclasses.field(default=0)
    gravity_suit: int = dataclasses.field(default=0)
    varia_suit: int = dataclasses.field(default=0)
    phazon_suit: int = dataclasses.field(default=0)
    energy_tanks: int = dataclasses.field(default=0)
    unknown_item_1: int = dataclasses.field(default=0)
    health_refill: int = dataclasses.field(default=0)
    unknown_item_2: int = dataclasses.field(default=0)
    wavebuster: int = dataclasses.field(default=0)
    default_spawn: bool = dataclasses.field(default=False)
    active: bool = dataclasses.field(default=False)
    morphed: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0xF

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        power_beam = struct.unpack('>l', data.read(4))[0]
        ice_beam = struct.unpack('>l', data.read(4))[0]
        wave_beam = struct.unpack('>l', data.read(4))[0]
        plasma_beam = struct.unpack('>l', data.read(4))[0]
        missiles = struct.unpack('>l', data.read(4))[0]
        scan_visor = struct.unpack('>l', data.read(4))[0]
        morph_ball_bomb = struct.unpack('>l', data.read(4))[0]
        power_bombs = struct.unpack('>l', data.read(4))[0]
        flamethrower = struct.unpack('>l', data.read(4))[0]
        thermal_visor = struct.unpack('>l', data.read(4))[0]
        charge_beam = struct.unpack('>l', data.read(4))[0]
        super_missile = struct.unpack('>l', data.read(4))[0]
        grapple_beam = struct.unpack('>l', data.read(4))[0]
        x_ray_visor = struct.unpack('>l', data.read(4))[0]
        ice_spreader = struct.unpack('>l', data.read(4))[0]
        space_jump_boots = struct.unpack('>l', data.read(4))[0]
        morph_ball = struct.unpack('>l', data.read(4))[0]
        combat_visor = struct.unpack('>l', data.read(4))[0]
        boost_ball = struct.unpack('>l', data.read(4))[0]
        spider_ball = struct.unpack('>l', data.read(4))[0]
        power_suit = struct.unpack('>l', data.read(4))[0]
        gravity_suit = struct.unpack('>l', data.read(4))[0]
        varia_suit = struct.unpack('>l', data.read(4))[0]
        phazon_suit = struct.unpack('>l', data.read(4))[0]
        energy_tanks = struct.unpack('>l', data.read(4))[0]
        unknown_item_1 = struct.unpack('>l', data.read(4))[0]
        health_refill = struct.unpack('>l', data.read(4))[0]
        unknown_item_2 = struct.unpack('>l', data.read(4))[0]
        wavebuster = struct.unpack('>l', data.read(4))[0]
        default_spawn = struct.unpack('>?', data.read(1))[0]
        active = struct.unpack('>?', data.read(1))[0]
        morphed = struct.unpack('>?', data.read(1))[0]
        return cls(name, position, rotation, power_beam, ice_beam, wave_beam, plasma_beam, missiles, scan_visor, morph_ball_bomb, power_bombs, flamethrower, thermal_visor, charge_beam, super_missile, grapple_beam, x_ray_visor, ice_spreader, space_jump_boots, morph_ball, combat_visor, boost_ball, spider_ball, power_suit, gravity_suit, varia_suit, phazon_suit, energy_tanks, unknown_item_1, health_refill, unknown_item_2, wavebuster, default_spawn, active, morphed)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00#')  # 35 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        data.write(struct.pack('>l', self.power_beam))
        data.write(struct.pack('>l', self.ice_beam))
        data.write(struct.pack('>l', self.wave_beam))
        data.write(struct.pack('>l', self.plasma_beam))
        data.write(struct.pack('>l', self.missiles))
        data.write(struct.pack('>l', self.scan_visor))
        data.write(struct.pack('>l', self.morph_ball_bomb))
        data.write(struct.pack('>l', self.power_bombs))
        data.write(struct.pack('>l', self.flamethrower))
        data.write(struct.pack('>l', self.thermal_visor))
        data.write(struct.pack('>l', self.charge_beam))
        data.write(struct.pack('>l', self.super_missile))
        data.write(struct.pack('>l', self.grapple_beam))
        data.write(struct.pack('>l', self.x_ray_visor))
        data.write(struct.pack('>l', self.ice_spreader))
        data.write(struct.pack('>l', self.space_jump_boots))
        data.write(struct.pack('>l', self.morph_ball))
        data.write(struct.pack('>l', self.combat_visor))
        data.write(struct.pack('>l', self.boost_ball))
        data.write(struct.pack('>l', self.spider_ball))
        data.write(struct.pack('>l', self.power_suit))
        data.write(struct.pack('>l', self.gravity_suit))
        data.write(struct.pack('>l', self.varia_suit))
        data.write(struct.pack('>l', self.phazon_suit))
        data.write(struct.pack('>l', self.energy_tanks))
        data.write(struct.pack('>l', self.unknown_item_1))
        data.write(struct.pack('>l', self.health_refill))
        data.write(struct.pack('>l', self.unknown_item_2))
        data.write(struct.pack('>l', self.wavebuster))
        data.write(struct.pack('>?', self.default_spawn))
        data.write(struct.pack('>?', self.active))
        data.write(struct.pack('>?', self.morphed))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            power_beam=data['power_beam'],
            ice_beam=data['ice_beam'],
            wave_beam=data['wave_beam'],
            plasma_beam=data['plasma_beam'],
            missiles=data['missiles'],
            scan_visor=data['scan_visor'],
            morph_ball_bomb=data['morph_ball_bomb'],
            power_bombs=data['power_bombs'],
            flamethrower=data['flamethrower'],
            thermal_visor=data['thermal_visor'],
            charge_beam=data['charge_beam'],
            super_missile=data['super_missile'],
            grapple_beam=data['grapple_beam'],
            x_ray_visor=data['x_ray_visor'],
            ice_spreader=data['ice_spreader'],
            space_jump_boots=data['space_jump_boots'],
            morph_ball=data['morph_ball'],
            combat_visor=data['combat_visor'],
            boost_ball=data['boost_ball'],
            spider_ball=data['spider_ball'],
            power_suit=data['power_suit'],
            gravity_suit=data['gravity_suit'],
            varia_suit=data['varia_suit'],
            phazon_suit=data['phazon_suit'],
            energy_tanks=data['energy_tanks'],
            unknown_item_1=data['unknown_item_1'],
            health_refill=data['health_refill'],
            unknown_item_2=data['unknown_item_2'],
            wavebuster=data['wavebuster'],
            default_spawn=data['default_spawn'],
            active=data['active'],
            morphed=data['morphed'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'power_beam': self.power_beam,
            'ice_beam': self.ice_beam,
            'wave_beam': self.wave_beam,
            'plasma_beam': self.plasma_beam,
            'missiles': self.missiles,
            'scan_visor': self.scan_visor,
            'morph_ball_bomb': self.morph_ball_bomb,
            'power_bombs': self.power_bombs,
            'flamethrower': self.flamethrower,
            'thermal_visor': self.thermal_visor,
            'charge_beam': self.charge_beam,
            'super_missile': self.super_missile,
            'grapple_beam': self.grapple_beam,
            'x_ray_visor': self.x_ray_visor,
            'ice_spreader': self.ice_spreader,
            'space_jump_boots': self.space_jump_boots,
            'morph_ball': self.morph_ball,
            'combat_visor': self.combat_visor,
            'boost_ball': self.boost_ball,
            'spider_ball': self.spider_ball,
            'power_suit': self.power_suit,
            'gravity_suit': self.gravity_suit,
            'varia_suit': self.varia_suit,
            'phazon_suit': self.phazon_suit,
            'energy_tanks': self.energy_tanks,
            'unknown_item_1': self.unknown_item_1,
            'health_refill': self.health_refill,
            'unknown_item_2': self.unknown_item_2,
            'wavebuster': self.wavebuster,
            'default_spawn': self.default_spawn,
            'active': self.active,
            'morphed': self.morphed,
        }

    def dependencies_for(self, asset_manager):
        yield from []
