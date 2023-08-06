# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.TIcon.Configurations import Configurations
from retro_data_structures.properties.echoes.archetypes.TweakTargeting.Charge.Gauge import Gauge
from retro_data_structures.properties.echoes.archetypes.TweakTargeting.LockDagger import LockDagger
from retro_data_structures.properties.echoes.archetypes.TweakTargeting.LockFire import LockFire
from retro_data_structures.properties.echoes.archetypes.TweakTargeting.OuterBeamIcon import OuterBeamIcon
from retro_data_structures.properties.echoes.archetypes.TweakTargeting.Scan import Scan
from retro_data_structures.properties.echoes.archetypes.TweakTargeting.VulnerabilityIndicator import VulnerabilityIndicator
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class TweakTargeting(BaseObjectType):
    instance_name: str = dataclasses.field(default='')
    unknown_0x5173932f: OuterBeamIcon = dataclasses.field(default_factory=OuterBeamIcon)
    unknown_0x23ff4be4: Configurations = dataclasses.field(default_factory=Configurations)
    unknown_0x92e98613: Configurations = dataclasses.field(default_factory=Configurations)
    unknown_0x64833842: Configurations = dataclasses.field(default_factory=Configurations)
    unknown_0x8dfd6e3c: Configurations = dataclasses.field(default_factory=Configurations)
    charge_gauge: Gauge = dataclasses.field(default_factory=Gauge)
    lock_fire: LockFire = dataclasses.field(default_factory=LockFire)
    lock_dagger: LockDagger = dataclasses.field(default_factory=LockDagger)
    scan: Scan = dataclasses.field(default_factory=Scan)
    unknown_0xc3410560: int = dataclasses.field(default=1)
    unknown_0x3eb13041: float = dataclasses.field(default=0.15000000596046448)
    unknown_0x5e67cab0: float = dataclasses.field(default=0.30000001192092896)
    unknown_0xe0ca98ac: float = dataclasses.field(default=0.15000000596046448)
    lock_on_confirm_reticle_scale: float = dataclasses.field(default=1.0)
    unknown_0x9f8d62c1: float = dataclasses.field(default=0.4000000059604645)
    unknown_0xff5eeeb9: float = dataclasses.field(default=0.4000000059604645)
    unknown_0x0d0b660d: float = dataclasses.field(default=0.20000000298023224)
    seeker_target_reticle_scale: float = dataclasses.field(default=0.5)
    unknown_0x03efc783: float = dataclasses.field(default=-120.0)
    unknown_0xdcbd7bf8: float = dataclasses.field(default=120.0)
    unknown_0x2acd6b4b: float = dataclasses.field(default=0.9599999785423279)
    unknown_0xb4c6c331: float = dataclasses.field(default=0.46000000834465027)
    unknown_0x27d02089: float = dataclasses.field(default=0.17000000178813934)
    unknown_0xae89310e: float = dataclasses.field(default=1.0)
    unknown_0xb27644df: float = dataclasses.field(default=1.0)
    unknown_0x21e2d1cc: float = dataclasses.field(default=1.0)
    orbit_point_occluded_opacity: float = dataclasses.field(default=0.0)
    unknown_0x5c489cb5: float = dataclasses.field(default=0.0)
    orbit_point_z_offset: float = dataclasses.field(default=-0.4000000059604645)
    unknown_0x61a6a38e: float = dataclasses.field(default=0.10000000149011612)
    unknown_0xfbdf31f9: float = dataclasses.field(default=0.30000001192092896)
    unknown_0xf76f7d0b: float = dataclasses.field(default=0.30000001192092896)
    unknown_0x810b3a08: float = dataclasses.field(default=0.0)
    unknown_0x73fe1553: float = dataclasses.field(default=1.0)
    unknown_0xc8aef6f2: float = dataclasses.field(default=0.0)
    unknown_0x69b1e76c: float = dataclasses.field(default=1.0)
    unknown_0x8a0dfd23: float = dataclasses.field(default=1.0)
    unknown_0x8299e96e: float = dataclasses.field(default=1.0)
    unknown_0xa18a3f25: float = dataclasses.field(default=1.0)
    unknown_0x23be9bb2: float = dataclasses.field(default=1.0)
    unknown_0x8d512b82: float = dataclasses.field(default=0.0)
    unknown_0x39f1698d: float = dataclasses.field(default=1.0)
    unknown_0xc768c1e9: float = dataclasses.field(default=1.0)
    unknown_0x55c47b0e: float = dataclasses.field(default=1.0)
    unknown_0xa009aea2: float = dataclasses.field(default=0.4000000059604645)
    unknown_0x38080bbf: float = dataclasses.field(default=0.699999988079071)
    unknown_0x71017dbe: float = dataclasses.field(default=0.800000011920929)
    unknown_0x4a996997: float = dataclasses.field(default=0.4000000059604645)
    unknown_0x9f9fa6f3: float = dataclasses.field(default=0.30000001192092896)
    unknown_0x932fea01: float = dataclasses.field(default=0.30000001192092896)
    unknown_0x165f0fa8: float = dataclasses.field(default=2.0)
    unknown_0x6bd6b11f: float = dataclasses.field(default=0.0)
    unknown_0x42420f6e: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    flower_reticle_scale: float = dataclasses.field(default=1.0)
    flower_reticle_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xb090e147: float = dataclasses.field(default=0.5)
    unknown_0x4c73a43d: float = dataclasses.field(default=1.0)
    unknown_0x6543d31b: float = dataclasses.field(default=0.8999999761581421)
    unknown_0x8cd2d1ce: float = dataclasses.field(default=0.15000000596046448)
    missile_bracket_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x45910e5d: float = dataclasses.field(default=0.5)
    unknown_0x07b30fa0: float = dataclasses.field(default=1.0)
    unknown_0x13ce8500: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x9829f256: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x77a613b9: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xdfa81287: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    lock_on_confirm_reticle_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    seeker_reticle_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x618d150a: float = dataclasses.field(default=160.0)
    unknown_0x209a2a8c: float = dataclasses.field(default=240.0)
    unknown_0xacb3f8f7: float = dataclasses.field(default=160.0)
    unknown_0xeda4c771: float = dataclasses.field(default=240.0)
    unknown_0xd3427574: float = dataclasses.field(default=160.0)
    unknown_0x92554af2: float = dataclasses.field(default=240.0)
    unknown_0x1e134e75: float = dataclasses.field(default=160.0)
    unknown_0x5f0471f3: float = dataclasses.field(default=240.0)
    unknown_0xe90548ac: float = dataclasses.field(default=160.0)
    unknown_0xa812772a: float = dataclasses.field(default=240.0)
    unknown_0x2d75c7be: float = dataclasses.field(default=160.0)
    unknown_0x6c62f838: float = dataclasses.field(default=240.0)
    unknown_0xf98e6242: float = dataclasses.field(default=160.0)
    unknown_0xb8995dc4: float = dataclasses.field(default=240.0)
    unknown_0x5009c614: float = dataclasses.field(default=160.0)
    unknown_0x111ef992: float = dataclasses.field(default=240.0)
    grapple_icon_scale: float = dataclasses.field(default=1.0)
    grapple_icon_scale_inactive: float = dataclasses.field(default=0.5)
    unknown_0x498d794a: float = dataclasses.field(default=80.0)
    unknown_0x089a46cc: float = dataclasses.field(default=240.0)
    grapple_icon_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    grapple_icon_color_inactive: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x083b1cc8: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x966982b1: float = dataclasses.field(default=0.5)
    unknown_0xf9799f5f: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x9b980788: float = dataclasses.field(default=0.5)
    orbit_point_model_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    crosshairs_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x2ff52290: float = dataclasses.field(default=0.30000001192092896)
    unknown_0x8a548cc9: bool = dataclasses.field(default=True)
    unknown_0x65d449e1: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x42c7fbe4: float = dataclasses.field(default=0.800000011920929)
    unknown_0x13820c03: float = dataclasses.field(default=80.0)
    unknown_0x52953385: float = dataclasses.field(default=80.0)
    x_ray_seeker_reticle_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xdd8cf478: float = dataclasses.field(default=1.0)
    unknown_0xcbac6d52: float = dataclasses.field(default=32.0)
    unknown_0x980a75b6: float = dataclasses.field(default=120.0)
    unknown_0xcd1e0e91: float = dataclasses.field(default=18.0)
    unknown_0xce9cf241: float = dataclasses.field(default=1.399999976158142)
    unknown_0xb6531e99: float = dataclasses.field(default=0.5)
    unknown_0x77e5c6b5: float = dataclasses.field(default=2.0)
    unknown_0xfef5668b: float = dataclasses.field(default=8.0)
    health_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    power_vulnerability_indicator: VulnerabilityIndicator = dataclasses.field(default_factory=VulnerabilityIndicator)
    light_vulnerability_indicator: VulnerabilityIndicator = dataclasses.field(default_factory=VulnerabilityIndicator)
    dark_vulnerability_indicator: VulnerabilityIndicator = dataclasses.field(default_factory=VulnerabilityIndicator)
    annihilator_vulnerability_indicator: VulnerabilityIndicator = dataclasses.field(default_factory=VulnerabilityIndicator)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return None

    def set_name(self, name: str) -> None:
        raise RuntimeError(f"{self.__class__.__name__} does not have name")

    @classmethod
    def object_type(cls) -> str:
        return 'TWTG'

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

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

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00u')  # 117 properties

        data.write(b'\x7f\xda\x14f')  # 0x7fda1466
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.instance_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Qs\x93/')  # 0x5173932f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x5173932f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'#\xffK\xe4')  # 0x23ff4be4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x23ff4be4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x92\xe9\x86\x13')  # 0x92e98613
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x92e98613.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'd\x838B')  # 0x64833842
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x64833842.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8d\xfdn<')  # 0x8dfd6e3c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x8dfd6e3c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbcZA\xb2')  # 0xbc5a41b2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.charge_gauge.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x00\x185\x89')  # 0x183589
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.lock_fire.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd2\x0e\xcc\x07')  # 0xd20ecc07
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.lock_dagger.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'e\xef\x9f*')  # 0x65ef9f2a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scan.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc3A\x05`')  # 0xc3410560
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xc3410560))

        data.write(b'>\xb10A')  # 0x3eb13041
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3eb13041))

        data.write(b'^g\xca\xb0')  # 0x5e67cab0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5e67cab0))

        data.write(b'\xe0\xca\x98\xac')  # 0xe0ca98ac
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe0ca98ac))

        data.write(b'\xc1\xe3Z\xbb')  # 0xc1e35abb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lock_on_confirm_reticle_scale))

        data.write(b'\x9f\x8db\xc1')  # 0x9f8d62c1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9f8d62c1))

        data.write(b'\xff^\xee\xb9')  # 0xff5eeeb9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xff5eeeb9))

        data.write(b'\r\x0bf\r')  # 0xd0b660d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0d0b660d))

        data.write(b'\x13-\xd0\x9e')  # 0x132dd09e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.seeker_target_reticle_scale))

        data.write(b'\x03\xef\xc7\x83')  # 0x3efc783
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x03efc783))

        data.write(b'\xdc\xbd{\xf8')  # 0xdcbd7bf8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xdcbd7bf8))

        data.write(b'*\xcdkK')  # 0x2acd6b4b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2acd6b4b))

        data.write(b'\xb4\xc6\xc31')  # 0xb4c6c331
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb4c6c331))

        data.write(b"'\xd0 \x89")  # 0x27d02089
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x27d02089))

        data.write(b'\xae\x891\x0e')  # 0xae89310e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xae89310e))

        data.write(b'\xb2vD\xdf')  # 0xb27644df
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb27644df))

        data.write(b'!\xe2\xd1\xcc')  # 0x21e2d1cc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x21e2d1cc))

        data.write(b'\x8e:\xfe\xf8')  # 0x8e3afef8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.orbit_point_occluded_opacity))

        data.write(b'\\H\x9c\xb5')  # 0x5c489cb5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5c489cb5))

        data.write(b'\xef,\x84.')  # 0xef2c842e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.orbit_point_z_offset))

        data.write(b'a\xa6\xa3\x8e')  # 0x61a6a38e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x61a6a38e))

        data.write(b'\xfb\xdf1\xf9')  # 0xfbdf31f9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfbdf31f9))

        data.write(b'\xf7o}\x0b')  # 0xf76f7d0b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf76f7d0b))

        data.write(b'\x81\x0b:\x08')  # 0x810b3a08
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x810b3a08))

        data.write(b's\xfe\x15S')  # 0x73fe1553
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x73fe1553))

        data.write(b'\xc8\xae\xf6\xf2')  # 0xc8aef6f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc8aef6f2))

        data.write(b'i\xb1\xe7l')  # 0x69b1e76c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x69b1e76c))

        data.write(b'\x8a\r\xfd#')  # 0x8a0dfd23
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8a0dfd23))

        data.write(b'\x82\x99\xe9n')  # 0x8299e96e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8299e96e))

        data.write(b'\xa1\x8a?%')  # 0xa18a3f25
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa18a3f25))

        data.write(b'#\xbe\x9b\xb2')  # 0x23be9bb2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x23be9bb2))

        data.write(b'\x8dQ+\x82')  # 0x8d512b82
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8d512b82))

        data.write(b'9\xf1i\x8d')  # 0x39f1698d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x39f1698d))

        data.write(b'\xc7h\xc1\xe9')  # 0xc768c1e9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc768c1e9))

        data.write(b'U\xc4{\x0e')  # 0x55c47b0e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x55c47b0e))

        data.write(b'\xa0\t\xae\xa2')  # 0xa009aea2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa009aea2))

        data.write(b'8\x08\x0b\xbf')  # 0x38080bbf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x38080bbf))

        data.write(b'q\x01}\xbe')  # 0x71017dbe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x71017dbe))

        data.write(b'J\x99i\x97')  # 0x4a996997
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4a996997))

        data.write(b'\x9f\x9f\xa6\xf3')  # 0x9f9fa6f3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9f9fa6f3))

        data.write(b'\x93/\xea\x01')  # 0x932fea01
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x932fea01))

        data.write(b'\x16_\x0f\xa8')  # 0x165f0fa8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x165f0fa8))

        data.write(b'k\xd6\xb1\x1f')  # 0x6bd6b11f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6bd6b11f))

        data.write(b'BB\x0fn')  # 0x42420f6e
        data.write(b'\x00\x10')  # size
        self.unknown_0x42420f6e.to_stream(data)

        data.write(b'\xa62)\xf1')  # 0xa63229f1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flower_reticle_scale))

        data.write(b'\xbd\xa4_\x1a')  # 0xbda45f1a
        data.write(b'\x00\x10')  # size
        self.flower_reticle_color.to_stream(data)

        data.write(b'\xb0\x90\xe1G')  # 0xb090e147
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb090e147))

        data.write(b'Ls\xa4=')  # 0x4c73a43d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4c73a43d))

        data.write(b'eC\xd3\x1b')  # 0x6543d31b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6543d31b))

        data.write(b'\x8c\xd2\xd1\xce')  # 0x8cd2d1ce
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8cd2d1ce))

        data.write(b'\xe4/k\xe0')  # 0xe42f6be0
        data.write(b'\x00\x10')  # size
        self.missile_bracket_color.to_stream(data)

        data.write(b'E\x91\x0e]')  # 0x45910e5d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x45910e5d))

        data.write(b'\x07\xb3\x0f\xa0')  # 0x7b30fa0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x07b30fa0))

        data.write(b'\x13\xce\x85\x00')  # 0x13ce8500
        data.write(b'\x00\x10')  # size
        self.unknown_0x13ce8500.to_stream(data)

        data.write(b'\x98)\xf2V')  # 0x9829f256
        data.write(b'\x00\x10')  # size
        self.unknown_0x9829f256.to_stream(data)

        data.write(b'w\xa6\x13\xb9')  # 0x77a613b9
        data.write(b'\x00\x10')  # size
        self.unknown_0x77a613b9.to_stream(data)

        data.write(b'\xdf\xa8\x12\x87')  # 0xdfa81287
        data.write(b'\x00\x10')  # size
        self.unknown_0xdfa81287.to_stream(data)

        data.write(b'\xdau,P')  # 0xda752c50
        data.write(b'\x00\x10')  # size
        self.lock_on_confirm_reticle_color.to_stream(data)

        data.write(b'{TN\x14')  # 0x7b544e14
        data.write(b'\x00\x10')  # size
        self.seeker_reticle_color.to_stream(data)

        data.write(b'a\x8d\x15\n')  # 0x618d150a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x618d150a))

        data.write(b' \x9a*\x8c')  # 0x209a2a8c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x209a2a8c))

        data.write(b'\xac\xb3\xf8\xf7')  # 0xacb3f8f7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xacb3f8f7))

        data.write(b'\xed\xa4\xc7q')  # 0xeda4c771
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xeda4c771))

        data.write(b'\xd3But')  # 0xd3427574
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd3427574))

        data.write(b'\x92UJ\xf2')  # 0x92554af2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x92554af2))

        data.write(b'\x1e\x13Nu')  # 0x1e134e75
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1e134e75))

        data.write(b'_\x04q\xf3')  # 0x5f0471f3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5f0471f3))

        data.write(b'\xe9\x05H\xac')  # 0xe90548ac
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe90548ac))

        data.write(b'\xa8\x12w*')  # 0xa812772a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa812772a))

        data.write(b'-u\xc7\xbe')  # 0x2d75c7be
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2d75c7be))

        data.write(b'lb\xf88')  # 0x6c62f838
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6c62f838))

        data.write(b'\xf9\x8ebB')  # 0xf98e6242
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf98e6242))

        data.write(b'\xb8\x99]\xc4')  # 0xb8995dc4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb8995dc4))

        data.write(b'P\t\xc6\x14')  # 0x5009c614
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5009c614))

        data.write(b'\x11\x1e\xf9\x92')  # 0x111ef992
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x111ef992))

        data.write(b'\xec\x0f\xf8\x88')  # 0xec0ff888
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_icon_scale))

        data.write(b'\xf2)\xe0^')  # 0xf229e05e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_icon_scale_inactive))

        data.write(b'I\x8dyJ')  # 0x498d794a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x498d794a))

        data.write(b'\x08\x9aF\xcc')  # 0x89a46cc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x089a46cc))

        data.write(b'\xf7\x99\x8ec')  # 0xf7998e63
        data.write(b'\x00\x10')  # size
        self.grapple_icon_color.to_stream(data)

        data.write(b'<\xe8S\xe3')  # 0x3ce853e3
        data.write(b'\x00\x10')  # size
        self.grapple_icon_color_inactive.to_stream(data)

        data.write(b'\x08;\x1c\xc8')  # 0x83b1cc8
        data.write(b'\x00\x10')  # size
        self.unknown_0x083b1cc8.to_stream(data)

        data.write(b'\x96i\x82\xb1')  # 0x966982b1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x966982b1))

        data.write(b'\xf9y\x9f_')  # 0xf9799f5f
        data.write(b'\x00\x10')  # size
        self.unknown_0xf9799f5f.to_stream(data)

        data.write(b'\x9b\x98\x07\x88')  # 0x9b980788
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9b980788))

        data.write(b'5#\xa4\x7f')  # 0x3523a47f
        data.write(b'\x00\x10')  # size
        self.orbit_point_model_color.to_stream(data)

        data.write(b"'5\x8bM")  # 0x27358b4d
        data.write(b'\x00\x10')  # size
        self.crosshairs_color.to_stream(data)

        data.write(b'/\xf5"\x90')  # 0x2ff52290
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2ff52290))

        data.write(b'\x8aT\x8c\xc9')  # 0x8a548cc9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x8a548cc9))

        data.write(b'e\xd4I\xe1')  # 0x65d449e1
        data.write(b'\x00\x10')  # size
        self.unknown_0x65d449e1.to_stream(data)

        data.write(b'B\xc7\xfb\xe4')  # 0x42c7fbe4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x42c7fbe4))

        data.write(b'\x13\x82\x0c\x03')  # 0x13820c03
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x13820c03))

        data.write(b'R\x953\x85')  # 0x52953385
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x52953385))

        data.write(b'\x0c\xd8\xfe]')  # 0xcd8fe5d
        data.write(b'\x00\x10')  # size
        self.x_ray_seeker_reticle_color.to_stream(data)

        data.write(b'\xdd\x8c\xf4x')  # 0xdd8cf478
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xdd8cf478))

        data.write(b'\xcb\xacmR')  # 0xcbac6d52
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcbac6d52))

        data.write(b'\x98\nu\xb6')  # 0x980a75b6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x980a75b6))

        data.write(b'\xcd\x1e\x0e\x91')  # 0xcd1e0e91
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcd1e0e91))

        data.write(b'\xce\x9c\xf2A')  # 0xce9cf241
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xce9cf241))

        data.write(b'\xb6S\x1e\x99')  # 0xb6531e99
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb6531e99))

        data.write(b'w\xe5\xc6\xb5')  # 0x77e5c6b5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x77e5c6b5))

        data.write(b'\xfe\xf5f\x8b')  # 0xfef5668b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfef5668b))

        data.write(b'\\\xe2\xa1o')  # 0x5ce2a16f
        data.write(b'\x00\x10')  # size
        self.health_color.to_stream(data)

        data.write(b'\x1e\x17\x96\x03')  # 0x1e179603
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.power_vulnerability_indicator.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'+p\xce\xf8')  # 0x2b70cef8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.light_vulnerability_indicator.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x94l\xef\xde')  # 0x946cefde
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.dark_vulnerability_indicator.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x92\x1c\x86\xe1')  # 0x921c86e1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.annihilator_vulnerability_indicator.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            instance_name=data['instance_name'],
            unknown_0x5173932f=OuterBeamIcon.from_json(data['unknown_0x5173932f']),
            unknown_0x23ff4be4=Configurations.from_json(data['unknown_0x23ff4be4']),
            unknown_0x92e98613=Configurations.from_json(data['unknown_0x92e98613']),
            unknown_0x64833842=Configurations.from_json(data['unknown_0x64833842']),
            unknown_0x8dfd6e3c=Configurations.from_json(data['unknown_0x8dfd6e3c']),
            charge_gauge=Gauge.from_json(data['charge_gauge']),
            lock_fire=LockFire.from_json(data['lock_fire']),
            lock_dagger=LockDagger.from_json(data['lock_dagger']),
            scan=Scan.from_json(data['scan']),
            unknown_0xc3410560=data['unknown_0xc3410560'],
            unknown_0x3eb13041=data['unknown_0x3eb13041'],
            unknown_0x5e67cab0=data['unknown_0x5e67cab0'],
            unknown_0xe0ca98ac=data['unknown_0xe0ca98ac'],
            lock_on_confirm_reticle_scale=data['lock_on_confirm_reticle_scale'],
            unknown_0x9f8d62c1=data['unknown_0x9f8d62c1'],
            unknown_0xff5eeeb9=data['unknown_0xff5eeeb9'],
            unknown_0x0d0b660d=data['unknown_0x0d0b660d'],
            seeker_target_reticle_scale=data['seeker_target_reticle_scale'],
            unknown_0x03efc783=data['unknown_0x03efc783'],
            unknown_0xdcbd7bf8=data['unknown_0xdcbd7bf8'],
            unknown_0x2acd6b4b=data['unknown_0x2acd6b4b'],
            unknown_0xb4c6c331=data['unknown_0xb4c6c331'],
            unknown_0x27d02089=data['unknown_0x27d02089'],
            unknown_0xae89310e=data['unknown_0xae89310e'],
            unknown_0xb27644df=data['unknown_0xb27644df'],
            unknown_0x21e2d1cc=data['unknown_0x21e2d1cc'],
            orbit_point_occluded_opacity=data['orbit_point_occluded_opacity'],
            unknown_0x5c489cb5=data['unknown_0x5c489cb5'],
            orbit_point_z_offset=data['orbit_point_z_offset'],
            unknown_0x61a6a38e=data['unknown_0x61a6a38e'],
            unknown_0xfbdf31f9=data['unknown_0xfbdf31f9'],
            unknown_0xf76f7d0b=data['unknown_0xf76f7d0b'],
            unknown_0x810b3a08=data['unknown_0x810b3a08'],
            unknown_0x73fe1553=data['unknown_0x73fe1553'],
            unknown_0xc8aef6f2=data['unknown_0xc8aef6f2'],
            unknown_0x69b1e76c=data['unknown_0x69b1e76c'],
            unknown_0x8a0dfd23=data['unknown_0x8a0dfd23'],
            unknown_0x8299e96e=data['unknown_0x8299e96e'],
            unknown_0xa18a3f25=data['unknown_0xa18a3f25'],
            unknown_0x23be9bb2=data['unknown_0x23be9bb2'],
            unknown_0x8d512b82=data['unknown_0x8d512b82'],
            unknown_0x39f1698d=data['unknown_0x39f1698d'],
            unknown_0xc768c1e9=data['unknown_0xc768c1e9'],
            unknown_0x55c47b0e=data['unknown_0x55c47b0e'],
            unknown_0xa009aea2=data['unknown_0xa009aea2'],
            unknown_0x38080bbf=data['unknown_0x38080bbf'],
            unknown_0x71017dbe=data['unknown_0x71017dbe'],
            unknown_0x4a996997=data['unknown_0x4a996997'],
            unknown_0x9f9fa6f3=data['unknown_0x9f9fa6f3'],
            unknown_0x932fea01=data['unknown_0x932fea01'],
            unknown_0x165f0fa8=data['unknown_0x165f0fa8'],
            unknown_0x6bd6b11f=data['unknown_0x6bd6b11f'],
            unknown_0x42420f6e=Color.from_json(data['unknown_0x42420f6e']),
            flower_reticle_scale=data['flower_reticle_scale'],
            flower_reticle_color=Color.from_json(data['flower_reticle_color']),
            unknown_0xb090e147=data['unknown_0xb090e147'],
            unknown_0x4c73a43d=data['unknown_0x4c73a43d'],
            unknown_0x6543d31b=data['unknown_0x6543d31b'],
            unknown_0x8cd2d1ce=data['unknown_0x8cd2d1ce'],
            missile_bracket_color=Color.from_json(data['missile_bracket_color']),
            unknown_0x45910e5d=data['unknown_0x45910e5d'],
            unknown_0x07b30fa0=data['unknown_0x07b30fa0'],
            unknown_0x13ce8500=Color.from_json(data['unknown_0x13ce8500']),
            unknown_0x9829f256=Color.from_json(data['unknown_0x9829f256']),
            unknown_0x77a613b9=Color.from_json(data['unknown_0x77a613b9']),
            unknown_0xdfa81287=Color.from_json(data['unknown_0xdfa81287']),
            lock_on_confirm_reticle_color=Color.from_json(data['lock_on_confirm_reticle_color']),
            seeker_reticle_color=Color.from_json(data['seeker_reticle_color']),
            unknown_0x618d150a=data['unknown_0x618d150a'],
            unknown_0x209a2a8c=data['unknown_0x209a2a8c'],
            unknown_0xacb3f8f7=data['unknown_0xacb3f8f7'],
            unknown_0xeda4c771=data['unknown_0xeda4c771'],
            unknown_0xd3427574=data['unknown_0xd3427574'],
            unknown_0x92554af2=data['unknown_0x92554af2'],
            unknown_0x1e134e75=data['unknown_0x1e134e75'],
            unknown_0x5f0471f3=data['unknown_0x5f0471f3'],
            unknown_0xe90548ac=data['unknown_0xe90548ac'],
            unknown_0xa812772a=data['unknown_0xa812772a'],
            unknown_0x2d75c7be=data['unknown_0x2d75c7be'],
            unknown_0x6c62f838=data['unknown_0x6c62f838'],
            unknown_0xf98e6242=data['unknown_0xf98e6242'],
            unknown_0xb8995dc4=data['unknown_0xb8995dc4'],
            unknown_0x5009c614=data['unknown_0x5009c614'],
            unknown_0x111ef992=data['unknown_0x111ef992'],
            grapple_icon_scale=data['grapple_icon_scale'],
            grapple_icon_scale_inactive=data['grapple_icon_scale_inactive'],
            unknown_0x498d794a=data['unknown_0x498d794a'],
            unknown_0x089a46cc=data['unknown_0x089a46cc'],
            grapple_icon_color=Color.from_json(data['grapple_icon_color']),
            grapple_icon_color_inactive=Color.from_json(data['grapple_icon_color_inactive']),
            unknown_0x083b1cc8=Color.from_json(data['unknown_0x083b1cc8']),
            unknown_0x966982b1=data['unknown_0x966982b1'],
            unknown_0xf9799f5f=Color.from_json(data['unknown_0xf9799f5f']),
            unknown_0x9b980788=data['unknown_0x9b980788'],
            orbit_point_model_color=Color.from_json(data['orbit_point_model_color']),
            crosshairs_color=Color.from_json(data['crosshairs_color']),
            unknown_0x2ff52290=data['unknown_0x2ff52290'],
            unknown_0x8a548cc9=data['unknown_0x8a548cc9'],
            unknown_0x65d449e1=Color.from_json(data['unknown_0x65d449e1']),
            unknown_0x42c7fbe4=data['unknown_0x42c7fbe4'],
            unknown_0x13820c03=data['unknown_0x13820c03'],
            unknown_0x52953385=data['unknown_0x52953385'],
            x_ray_seeker_reticle_color=Color.from_json(data['x_ray_seeker_reticle_color']),
            unknown_0xdd8cf478=data['unknown_0xdd8cf478'],
            unknown_0xcbac6d52=data['unknown_0xcbac6d52'],
            unknown_0x980a75b6=data['unknown_0x980a75b6'],
            unknown_0xcd1e0e91=data['unknown_0xcd1e0e91'],
            unknown_0xce9cf241=data['unknown_0xce9cf241'],
            unknown_0xb6531e99=data['unknown_0xb6531e99'],
            unknown_0x77e5c6b5=data['unknown_0x77e5c6b5'],
            unknown_0xfef5668b=data['unknown_0xfef5668b'],
            health_color=Color.from_json(data['health_color']),
            power_vulnerability_indicator=VulnerabilityIndicator.from_json(data['power_vulnerability_indicator']),
            light_vulnerability_indicator=VulnerabilityIndicator.from_json(data['light_vulnerability_indicator']),
            dark_vulnerability_indicator=VulnerabilityIndicator.from_json(data['dark_vulnerability_indicator']),
            annihilator_vulnerability_indicator=VulnerabilityIndicator.from_json(data['annihilator_vulnerability_indicator']),
        )

    def to_json(self) -> dict:
        return {
            'instance_name': self.instance_name,
            'unknown_0x5173932f': self.unknown_0x5173932f.to_json(),
            'unknown_0x23ff4be4': self.unknown_0x23ff4be4.to_json(),
            'unknown_0x92e98613': self.unknown_0x92e98613.to_json(),
            'unknown_0x64833842': self.unknown_0x64833842.to_json(),
            'unknown_0x8dfd6e3c': self.unknown_0x8dfd6e3c.to_json(),
            'charge_gauge': self.charge_gauge.to_json(),
            'lock_fire': self.lock_fire.to_json(),
            'lock_dagger': self.lock_dagger.to_json(),
            'scan': self.scan.to_json(),
            'unknown_0xc3410560': self.unknown_0xc3410560,
            'unknown_0x3eb13041': self.unknown_0x3eb13041,
            'unknown_0x5e67cab0': self.unknown_0x5e67cab0,
            'unknown_0xe0ca98ac': self.unknown_0xe0ca98ac,
            'lock_on_confirm_reticle_scale': self.lock_on_confirm_reticle_scale,
            'unknown_0x9f8d62c1': self.unknown_0x9f8d62c1,
            'unknown_0xff5eeeb9': self.unknown_0xff5eeeb9,
            'unknown_0x0d0b660d': self.unknown_0x0d0b660d,
            'seeker_target_reticle_scale': self.seeker_target_reticle_scale,
            'unknown_0x03efc783': self.unknown_0x03efc783,
            'unknown_0xdcbd7bf8': self.unknown_0xdcbd7bf8,
            'unknown_0x2acd6b4b': self.unknown_0x2acd6b4b,
            'unknown_0xb4c6c331': self.unknown_0xb4c6c331,
            'unknown_0x27d02089': self.unknown_0x27d02089,
            'unknown_0xae89310e': self.unknown_0xae89310e,
            'unknown_0xb27644df': self.unknown_0xb27644df,
            'unknown_0x21e2d1cc': self.unknown_0x21e2d1cc,
            'orbit_point_occluded_opacity': self.orbit_point_occluded_opacity,
            'unknown_0x5c489cb5': self.unknown_0x5c489cb5,
            'orbit_point_z_offset': self.orbit_point_z_offset,
            'unknown_0x61a6a38e': self.unknown_0x61a6a38e,
            'unknown_0xfbdf31f9': self.unknown_0xfbdf31f9,
            'unknown_0xf76f7d0b': self.unknown_0xf76f7d0b,
            'unknown_0x810b3a08': self.unknown_0x810b3a08,
            'unknown_0x73fe1553': self.unknown_0x73fe1553,
            'unknown_0xc8aef6f2': self.unknown_0xc8aef6f2,
            'unknown_0x69b1e76c': self.unknown_0x69b1e76c,
            'unknown_0x8a0dfd23': self.unknown_0x8a0dfd23,
            'unknown_0x8299e96e': self.unknown_0x8299e96e,
            'unknown_0xa18a3f25': self.unknown_0xa18a3f25,
            'unknown_0x23be9bb2': self.unknown_0x23be9bb2,
            'unknown_0x8d512b82': self.unknown_0x8d512b82,
            'unknown_0x39f1698d': self.unknown_0x39f1698d,
            'unknown_0xc768c1e9': self.unknown_0xc768c1e9,
            'unknown_0x55c47b0e': self.unknown_0x55c47b0e,
            'unknown_0xa009aea2': self.unknown_0xa009aea2,
            'unknown_0x38080bbf': self.unknown_0x38080bbf,
            'unknown_0x71017dbe': self.unknown_0x71017dbe,
            'unknown_0x4a996997': self.unknown_0x4a996997,
            'unknown_0x9f9fa6f3': self.unknown_0x9f9fa6f3,
            'unknown_0x932fea01': self.unknown_0x932fea01,
            'unknown_0x165f0fa8': self.unknown_0x165f0fa8,
            'unknown_0x6bd6b11f': self.unknown_0x6bd6b11f,
            'unknown_0x42420f6e': self.unknown_0x42420f6e.to_json(),
            'flower_reticle_scale': self.flower_reticle_scale,
            'flower_reticle_color': self.flower_reticle_color.to_json(),
            'unknown_0xb090e147': self.unknown_0xb090e147,
            'unknown_0x4c73a43d': self.unknown_0x4c73a43d,
            'unknown_0x6543d31b': self.unknown_0x6543d31b,
            'unknown_0x8cd2d1ce': self.unknown_0x8cd2d1ce,
            'missile_bracket_color': self.missile_bracket_color.to_json(),
            'unknown_0x45910e5d': self.unknown_0x45910e5d,
            'unknown_0x07b30fa0': self.unknown_0x07b30fa0,
            'unknown_0x13ce8500': self.unknown_0x13ce8500.to_json(),
            'unknown_0x9829f256': self.unknown_0x9829f256.to_json(),
            'unknown_0x77a613b9': self.unknown_0x77a613b9.to_json(),
            'unknown_0xdfa81287': self.unknown_0xdfa81287.to_json(),
            'lock_on_confirm_reticle_color': self.lock_on_confirm_reticle_color.to_json(),
            'seeker_reticle_color': self.seeker_reticle_color.to_json(),
            'unknown_0x618d150a': self.unknown_0x618d150a,
            'unknown_0x209a2a8c': self.unknown_0x209a2a8c,
            'unknown_0xacb3f8f7': self.unknown_0xacb3f8f7,
            'unknown_0xeda4c771': self.unknown_0xeda4c771,
            'unknown_0xd3427574': self.unknown_0xd3427574,
            'unknown_0x92554af2': self.unknown_0x92554af2,
            'unknown_0x1e134e75': self.unknown_0x1e134e75,
            'unknown_0x5f0471f3': self.unknown_0x5f0471f3,
            'unknown_0xe90548ac': self.unknown_0xe90548ac,
            'unknown_0xa812772a': self.unknown_0xa812772a,
            'unknown_0x2d75c7be': self.unknown_0x2d75c7be,
            'unknown_0x6c62f838': self.unknown_0x6c62f838,
            'unknown_0xf98e6242': self.unknown_0xf98e6242,
            'unknown_0xb8995dc4': self.unknown_0xb8995dc4,
            'unknown_0x5009c614': self.unknown_0x5009c614,
            'unknown_0x111ef992': self.unknown_0x111ef992,
            'grapple_icon_scale': self.grapple_icon_scale,
            'grapple_icon_scale_inactive': self.grapple_icon_scale_inactive,
            'unknown_0x498d794a': self.unknown_0x498d794a,
            'unknown_0x089a46cc': self.unknown_0x089a46cc,
            'grapple_icon_color': self.grapple_icon_color.to_json(),
            'grapple_icon_color_inactive': self.grapple_icon_color_inactive.to_json(),
            'unknown_0x083b1cc8': self.unknown_0x083b1cc8.to_json(),
            'unknown_0x966982b1': self.unknown_0x966982b1,
            'unknown_0xf9799f5f': self.unknown_0xf9799f5f.to_json(),
            'unknown_0x9b980788': self.unknown_0x9b980788,
            'orbit_point_model_color': self.orbit_point_model_color.to_json(),
            'crosshairs_color': self.crosshairs_color.to_json(),
            'unknown_0x2ff52290': self.unknown_0x2ff52290,
            'unknown_0x8a548cc9': self.unknown_0x8a548cc9,
            'unknown_0x65d449e1': self.unknown_0x65d449e1.to_json(),
            'unknown_0x42c7fbe4': self.unknown_0x42c7fbe4,
            'unknown_0x13820c03': self.unknown_0x13820c03,
            'unknown_0x52953385': self.unknown_0x52953385,
            'x_ray_seeker_reticle_color': self.x_ray_seeker_reticle_color.to_json(),
            'unknown_0xdd8cf478': self.unknown_0xdd8cf478,
            'unknown_0xcbac6d52': self.unknown_0xcbac6d52,
            'unknown_0x980a75b6': self.unknown_0x980a75b6,
            'unknown_0xcd1e0e91': self.unknown_0xcd1e0e91,
            'unknown_0xce9cf241': self.unknown_0xce9cf241,
            'unknown_0xb6531e99': self.unknown_0xb6531e99,
            'unknown_0x77e5c6b5': self.unknown_0x77e5c6b5,
            'unknown_0xfef5668b': self.unknown_0xfef5668b,
            'health_color': self.health_color.to_json(),
            'power_vulnerability_indicator': self.power_vulnerability_indicator.to_json(),
            'light_vulnerability_indicator': self.light_vulnerability_indicator.to_json(),
            'dark_vulnerability_indicator': self.dark_vulnerability_indicator.to_json(),
            'annihilator_vulnerability_indicator': self.annihilator_vulnerability_indicator.to_json(),
        }

    def _dependencies_for_unknown_0x5173932f(self, asset_manager):
        yield from self.unknown_0x5173932f.dependencies_for(asset_manager)

    def _dependencies_for_unknown_0x23ff4be4(self, asset_manager):
        yield from self.unknown_0x23ff4be4.dependencies_for(asset_manager)

    def _dependencies_for_unknown_0x92e98613(self, asset_manager):
        yield from self.unknown_0x92e98613.dependencies_for(asset_manager)

    def _dependencies_for_unknown_0x64833842(self, asset_manager):
        yield from self.unknown_0x64833842.dependencies_for(asset_manager)

    def _dependencies_for_unknown_0x8dfd6e3c(self, asset_manager):
        yield from self.unknown_0x8dfd6e3c.dependencies_for(asset_manager)

    def _dependencies_for_charge_gauge(self, asset_manager):
        yield from self.charge_gauge.dependencies_for(asset_manager)

    def _dependencies_for_lock_fire(self, asset_manager):
        yield from self.lock_fire.dependencies_for(asset_manager)

    def _dependencies_for_lock_dagger(self, asset_manager):
        yield from self.lock_dagger.dependencies_for(asset_manager)

    def _dependencies_for_scan(self, asset_manager):
        yield from self.scan.dependencies_for(asset_manager)

    def _dependencies_for_power_vulnerability_indicator(self, asset_manager):
        yield from self.power_vulnerability_indicator.dependencies_for(asset_manager)

    def _dependencies_for_light_vulnerability_indicator(self, asset_manager):
        yield from self.light_vulnerability_indicator.dependencies_for(asset_manager)

    def _dependencies_for_dark_vulnerability_indicator(self, asset_manager):
        yield from self.dark_vulnerability_indicator.dependencies_for(asset_manager)

    def _dependencies_for_annihilator_vulnerability_indicator(self, asset_manager):
        yield from self.annihilator_vulnerability_indicator.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unknown_0x5173932f, "unknown_0x5173932f", "OuterBeamIcon"),
            (self._dependencies_for_unknown_0x23ff4be4, "unknown_0x23ff4be4", "Configurations"),
            (self._dependencies_for_unknown_0x92e98613, "unknown_0x92e98613", "Configurations"),
            (self._dependencies_for_unknown_0x64833842, "unknown_0x64833842", "Configurations"),
            (self._dependencies_for_unknown_0x8dfd6e3c, "unknown_0x8dfd6e3c", "Configurations"),
            (self._dependencies_for_charge_gauge, "charge_gauge", "Gauge"),
            (self._dependencies_for_lock_fire, "lock_fire", "LockFire"),
            (self._dependencies_for_lock_dagger, "lock_dagger", "LockDagger"),
            (self._dependencies_for_scan, "scan", "Scan"),
            (self._dependencies_for_power_vulnerability_indicator, "power_vulnerability_indicator", "VulnerabilityIndicator"),
            (self._dependencies_for_light_vulnerability_indicator, "light_vulnerability_indicator", "VulnerabilityIndicator"),
            (self._dependencies_for_dark_vulnerability_indicator, "dark_vulnerability_indicator", "VulnerabilityIndicator"),
            (self._dependencies_for_annihilator_vulnerability_indicator, "annihilator_vulnerability_indicator", "VulnerabilityIndicator"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for TweakTargeting.{field_name} ({field_type}): {e}"
                )


def _decode_instance_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0x5173932f(data: typing.BinaryIO, property_size: int):
    return OuterBeamIcon.from_stream(data, property_size)


def _decode_unknown_0x23ff4be4(data: typing.BinaryIO, property_size: int):
    return Configurations.from_stream(data, property_size)


def _decode_unknown_0x92e98613(data: typing.BinaryIO, property_size: int):
    return Configurations.from_stream(data, property_size)


def _decode_unknown_0x64833842(data: typing.BinaryIO, property_size: int):
    return Configurations.from_stream(data, property_size)


def _decode_unknown_0x8dfd6e3c(data: typing.BinaryIO, property_size: int):
    return Configurations.from_stream(data, property_size)


def _decode_charge_gauge(data: typing.BinaryIO, property_size: int):
    return Gauge.from_stream(data, property_size)


def _decode_lock_fire(data: typing.BinaryIO, property_size: int):
    return LockFire.from_stream(data, property_size)


def _decode_lock_dagger(data: typing.BinaryIO, property_size: int):
    return LockDagger.from_stream(data, property_size)


def _decode_scan(data: typing.BinaryIO, property_size: int):
    return Scan.from_stream(data, property_size)


def _decode_unknown_0xc3410560(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x3eb13041(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5e67cab0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe0ca98ac(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lock_on_confirm_reticle_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9f8d62c1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xff5eeeb9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0d0b660d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_seeker_target_reticle_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x03efc783(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xdcbd7bf8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2acd6b4b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb4c6c331(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x27d02089(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xae89310e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb27644df(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x21e2d1cc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_orbit_point_occluded_opacity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5c489cb5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_orbit_point_z_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x61a6a38e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xfbdf31f9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf76f7d0b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x810b3a08(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x73fe1553(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc8aef6f2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x69b1e76c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8a0dfd23(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8299e96e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa18a3f25(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x23be9bb2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8d512b82(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x39f1698d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc768c1e9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x55c47b0e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa009aea2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x38080bbf(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x71017dbe(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4a996997(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9f9fa6f3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x932fea01(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x165f0fa8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6bd6b11f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x42420f6e(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_flower_reticle_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flower_reticle_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xb090e147(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4c73a43d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6543d31b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8cd2d1ce(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_missile_bracket_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x45910e5d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x07b30fa0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x13ce8500(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x9829f256(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x77a613b9(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xdfa81287(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_lock_on_confirm_reticle_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_seeker_reticle_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x618d150a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x209a2a8c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xacb3f8f7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xeda4c771(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd3427574(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x92554af2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1e134e75(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5f0471f3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe90548ac(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa812772a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2d75c7be(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6c62f838(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf98e6242(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb8995dc4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5009c614(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x111ef992(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_icon_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_icon_scale_inactive(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x498d794a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x089a46cc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_icon_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_grapple_icon_color_inactive(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x083b1cc8(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x966982b1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf9799f5f(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x9b980788(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_orbit_point_model_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_crosshairs_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x2ff52290(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8a548cc9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x65d449e1(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x42c7fbe4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x13820c03(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x52953385(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_x_ray_seeker_reticle_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xdd8cf478(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcbac6d52(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x980a75b6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcd1e0e91(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xce9cf241(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb6531e99(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x77e5c6b5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xfef5668b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_health_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_power_vulnerability_indicator(data: typing.BinaryIO, property_size: int):
    return VulnerabilityIndicator.from_stream(data, property_size)


def _decode_light_vulnerability_indicator(data: typing.BinaryIO, property_size: int):
    return VulnerabilityIndicator.from_stream(data, property_size)


def _decode_dark_vulnerability_indicator(data: typing.BinaryIO, property_size: int):
    return VulnerabilityIndicator.from_stream(data, property_size)


def _decode_annihilator_vulnerability_indicator(data: typing.BinaryIO, property_size: int):
    return VulnerabilityIndicator.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7fda1466: ('instance_name', _decode_instance_name),
    0x5173932f: ('unknown_0x5173932f', _decode_unknown_0x5173932f),
    0x23ff4be4: ('unknown_0x23ff4be4', _decode_unknown_0x23ff4be4),
    0x92e98613: ('unknown_0x92e98613', _decode_unknown_0x92e98613),
    0x64833842: ('unknown_0x64833842', _decode_unknown_0x64833842),
    0x8dfd6e3c: ('unknown_0x8dfd6e3c', _decode_unknown_0x8dfd6e3c),
    0xbc5a41b2: ('charge_gauge', _decode_charge_gauge),
    0x183589: ('lock_fire', _decode_lock_fire),
    0xd20ecc07: ('lock_dagger', _decode_lock_dagger),
    0x65ef9f2a: ('scan', _decode_scan),
    0xc3410560: ('unknown_0xc3410560', _decode_unknown_0xc3410560),
    0x3eb13041: ('unknown_0x3eb13041', _decode_unknown_0x3eb13041),
    0x5e67cab0: ('unknown_0x5e67cab0', _decode_unknown_0x5e67cab0),
    0xe0ca98ac: ('unknown_0xe0ca98ac', _decode_unknown_0xe0ca98ac),
    0xc1e35abb: ('lock_on_confirm_reticle_scale', _decode_lock_on_confirm_reticle_scale),
    0x9f8d62c1: ('unknown_0x9f8d62c1', _decode_unknown_0x9f8d62c1),
    0xff5eeeb9: ('unknown_0xff5eeeb9', _decode_unknown_0xff5eeeb9),
    0xd0b660d: ('unknown_0x0d0b660d', _decode_unknown_0x0d0b660d),
    0x132dd09e: ('seeker_target_reticle_scale', _decode_seeker_target_reticle_scale),
    0x3efc783: ('unknown_0x03efc783', _decode_unknown_0x03efc783),
    0xdcbd7bf8: ('unknown_0xdcbd7bf8', _decode_unknown_0xdcbd7bf8),
    0x2acd6b4b: ('unknown_0x2acd6b4b', _decode_unknown_0x2acd6b4b),
    0xb4c6c331: ('unknown_0xb4c6c331', _decode_unknown_0xb4c6c331),
    0x27d02089: ('unknown_0x27d02089', _decode_unknown_0x27d02089),
    0xae89310e: ('unknown_0xae89310e', _decode_unknown_0xae89310e),
    0xb27644df: ('unknown_0xb27644df', _decode_unknown_0xb27644df),
    0x21e2d1cc: ('unknown_0x21e2d1cc', _decode_unknown_0x21e2d1cc),
    0x8e3afef8: ('orbit_point_occluded_opacity', _decode_orbit_point_occluded_opacity),
    0x5c489cb5: ('unknown_0x5c489cb5', _decode_unknown_0x5c489cb5),
    0xef2c842e: ('orbit_point_z_offset', _decode_orbit_point_z_offset),
    0x61a6a38e: ('unknown_0x61a6a38e', _decode_unknown_0x61a6a38e),
    0xfbdf31f9: ('unknown_0xfbdf31f9', _decode_unknown_0xfbdf31f9),
    0xf76f7d0b: ('unknown_0xf76f7d0b', _decode_unknown_0xf76f7d0b),
    0x810b3a08: ('unknown_0x810b3a08', _decode_unknown_0x810b3a08),
    0x73fe1553: ('unknown_0x73fe1553', _decode_unknown_0x73fe1553),
    0xc8aef6f2: ('unknown_0xc8aef6f2', _decode_unknown_0xc8aef6f2),
    0x69b1e76c: ('unknown_0x69b1e76c', _decode_unknown_0x69b1e76c),
    0x8a0dfd23: ('unknown_0x8a0dfd23', _decode_unknown_0x8a0dfd23),
    0x8299e96e: ('unknown_0x8299e96e', _decode_unknown_0x8299e96e),
    0xa18a3f25: ('unknown_0xa18a3f25', _decode_unknown_0xa18a3f25),
    0x23be9bb2: ('unknown_0x23be9bb2', _decode_unknown_0x23be9bb2),
    0x8d512b82: ('unknown_0x8d512b82', _decode_unknown_0x8d512b82),
    0x39f1698d: ('unknown_0x39f1698d', _decode_unknown_0x39f1698d),
    0xc768c1e9: ('unknown_0xc768c1e9', _decode_unknown_0xc768c1e9),
    0x55c47b0e: ('unknown_0x55c47b0e', _decode_unknown_0x55c47b0e),
    0xa009aea2: ('unknown_0xa009aea2', _decode_unknown_0xa009aea2),
    0x38080bbf: ('unknown_0x38080bbf', _decode_unknown_0x38080bbf),
    0x71017dbe: ('unknown_0x71017dbe', _decode_unknown_0x71017dbe),
    0x4a996997: ('unknown_0x4a996997', _decode_unknown_0x4a996997),
    0x9f9fa6f3: ('unknown_0x9f9fa6f3', _decode_unknown_0x9f9fa6f3),
    0x932fea01: ('unknown_0x932fea01', _decode_unknown_0x932fea01),
    0x165f0fa8: ('unknown_0x165f0fa8', _decode_unknown_0x165f0fa8),
    0x6bd6b11f: ('unknown_0x6bd6b11f', _decode_unknown_0x6bd6b11f),
    0x42420f6e: ('unknown_0x42420f6e', _decode_unknown_0x42420f6e),
    0xa63229f1: ('flower_reticle_scale', _decode_flower_reticle_scale),
    0xbda45f1a: ('flower_reticle_color', _decode_flower_reticle_color),
    0xb090e147: ('unknown_0xb090e147', _decode_unknown_0xb090e147),
    0x4c73a43d: ('unknown_0x4c73a43d', _decode_unknown_0x4c73a43d),
    0x6543d31b: ('unknown_0x6543d31b', _decode_unknown_0x6543d31b),
    0x8cd2d1ce: ('unknown_0x8cd2d1ce', _decode_unknown_0x8cd2d1ce),
    0xe42f6be0: ('missile_bracket_color', _decode_missile_bracket_color),
    0x45910e5d: ('unknown_0x45910e5d', _decode_unknown_0x45910e5d),
    0x7b30fa0: ('unknown_0x07b30fa0', _decode_unknown_0x07b30fa0),
    0x13ce8500: ('unknown_0x13ce8500', _decode_unknown_0x13ce8500),
    0x9829f256: ('unknown_0x9829f256', _decode_unknown_0x9829f256),
    0x77a613b9: ('unknown_0x77a613b9', _decode_unknown_0x77a613b9),
    0xdfa81287: ('unknown_0xdfa81287', _decode_unknown_0xdfa81287),
    0xda752c50: ('lock_on_confirm_reticle_color', _decode_lock_on_confirm_reticle_color),
    0x7b544e14: ('seeker_reticle_color', _decode_seeker_reticle_color),
    0x618d150a: ('unknown_0x618d150a', _decode_unknown_0x618d150a),
    0x209a2a8c: ('unknown_0x209a2a8c', _decode_unknown_0x209a2a8c),
    0xacb3f8f7: ('unknown_0xacb3f8f7', _decode_unknown_0xacb3f8f7),
    0xeda4c771: ('unknown_0xeda4c771', _decode_unknown_0xeda4c771),
    0xd3427574: ('unknown_0xd3427574', _decode_unknown_0xd3427574),
    0x92554af2: ('unknown_0x92554af2', _decode_unknown_0x92554af2),
    0x1e134e75: ('unknown_0x1e134e75', _decode_unknown_0x1e134e75),
    0x5f0471f3: ('unknown_0x5f0471f3', _decode_unknown_0x5f0471f3),
    0xe90548ac: ('unknown_0xe90548ac', _decode_unknown_0xe90548ac),
    0xa812772a: ('unknown_0xa812772a', _decode_unknown_0xa812772a),
    0x2d75c7be: ('unknown_0x2d75c7be', _decode_unknown_0x2d75c7be),
    0x6c62f838: ('unknown_0x6c62f838', _decode_unknown_0x6c62f838),
    0xf98e6242: ('unknown_0xf98e6242', _decode_unknown_0xf98e6242),
    0xb8995dc4: ('unknown_0xb8995dc4', _decode_unknown_0xb8995dc4),
    0x5009c614: ('unknown_0x5009c614', _decode_unknown_0x5009c614),
    0x111ef992: ('unknown_0x111ef992', _decode_unknown_0x111ef992),
    0xec0ff888: ('grapple_icon_scale', _decode_grapple_icon_scale),
    0xf229e05e: ('grapple_icon_scale_inactive', _decode_grapple_icon_scale_inactive),
    0x498d794a: ('unknown_0x498d794a', _decode_unknown_0x498d794a),
    0x89a46cc: ('unknown_0x089a46cc', _decode_unknown_0x089a46cc),
    0xf7998e63: ('grapple_icon_color', _decode_grapple_icon_color),
    0x3ce853e3: ('grapple_icon_color_inactive', _decode_grapple_icon_color_inactive),
    0x83b1cc8: ('unknown_0x083b1cc8', _decode_unknown_0x083b1cc8),
    0x966982b1: ('unknown_0x966982b1', _decode_unknown_0x966982b1),
    0xf9799f5f: ('unknown_0xf9799f5f', _decode_unknown_0xf9799f5f),
    0x9b980788: ('unknown_0x9b980788', _decode_unknown_0x9b980788),
    0x3523a47f: ('orbit_point_model_color', _decode_orbit_point_model_color),
    0x27358b4d: ('crosshairs_color', _decode_crosshairs_color),
    0x2ff52290: ('unknown_0x2ff52290', _decode_unknown_0x2ff52290),
    0x8a548cc9: ('unknown_0x8a548cc9', _decode_unknown_0x8a548cc9),
    0x65d449e1: ('unknown_0x65d449e1', _decode_unknown_0x65d449e1),
    0x42c7fbe4: ('unknown_0x42c7fbe4', _decode_unknown_0x42c7fbe4),
    0x13820c03: ('unknown_0x13820c03', _decode_unknown_0x13820c03),
    0x52953385: ('unknown_0x52953385', _decode_unknown_0x52953385),
    0xcd8fe5d: ('x_ray_seeker_reticle_color', _decode_x_ray_seeker_reticle_color),
    0xdd8cf478: ('unknown_0xdd8cf478', _decode_unknown_0xdd8cf478),
    0xcbac6d52: ('unknown_0xcbac6d52', _decode_unknown_0xcbac6d52),
    0x980a75b6: ('unknown_0x980a75b6', _decode_unknown_0x980a75b6),
    0xcd1e0e91: ('unknown_0xcd1e0e91', _decode_unknown_0xcd1e0e91),
    0xce9cf241: ('unknown_0xce9cf241', _decode_unknown_0xce9cf241),
    0xb6531e99: ('unknown_0xb6531e99', _decode_unknown_0xb6531e99),
    0x77e5c6b5: ('unknown_0x77e5c6b5', _decode_unknown_0x77e5c6b5),
    0xfef5668b: ('unknown_0xfef5668b', _decode_unknown_0xfef5668b),
    0x5ce2a16f: ('health_color', _decode_health_color),
    0x1e179603: ('power_vulnerability_indicator', _decode_power_vulnerability_indicator),
    0x2b70cef8: ('light_vulnerability_indicator', _decode_light_vulnerability_indicator),
    0x946cefde: ('dark_vulnerability_indicator', _decode_dark_vulnerability_indicator),
    0x921c86e1: ('annihilator_vulnerability_indicator', _decode_annihilator_vulnerability_indicator),
}
