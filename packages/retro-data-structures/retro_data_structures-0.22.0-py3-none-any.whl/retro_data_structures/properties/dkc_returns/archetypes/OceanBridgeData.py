# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.OceanBridgeStructA import OceanBridgeStructA
from retro_data_structures.properties.dkc_returns.archetypes.OceanBridgeStructB import OceanBridgeStructB
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class OceanBridgeData(BaseProperty):
    unknown_0xe993145f: int = dataclasses.field(default=0)
    cmdl_0x69a2b08e: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0xa2fe632b: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    alt_model2: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    unknown_0xef36c220: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0xf233f298: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    z_motion: Spline = dataclasses.field(default_factory=Spline)
    y_rotation: Spline = dataclasses.field(default_factory=Spline)
    impulse_time_min: float = dataclasses.field(default=-0.10000000149011612)
    impulse_time_max: float = dataclasses.field(default=0.25)
    impulse_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    collision_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    unknown_0x6045bb7b: int = dataclasses.field(default=4)
    unknown_0xfe69d67a: float = dataclasses.field(default=0.05000000074505806)
    unknown_0x847759ba: float = dataclasses.field(default=12.0)
    rise_min: float = dataclasses.field(default=0.75)
    rise_max: float = dataclasses.field(default=2.5)
    rise_step: float = dataclasses.field(default=0.5)
    target_height: float = dataclasses.field(default=7.0)
    unknown_0x75ce0c79: float = dataclasses.field(default=7.0)
    unknown_0xe5d866f1: bool = dataclasses.field(default=False)
    unknown_0xb0946259: bool = dataclasses.field(default=True)
    unknown_0x812afc85: bool = dataclasses.field(default=True)
    unknown_0x66ad2b98: float = dataclasses.field(default=0.10000000149011612)
    unknown_0x1d2d962d: float = dataclasses.field(default=10.0)
    center_plank: int = dataclasses.field(default=2)
    rotate_plank0: bool = dataclasses.field(default=False)
    rotate_plank1: bool = dataclasses.field(default=False)
    rotate_plank2: bool = dataclasses.field(default=False)
    rotate_plank3: bool = dataclasses.field(default=False)
    rotate_plank4: bool = dataclasses.field(default=False)
    rotate_plank5: bool = dataclasses.field(default=False)
    rotate_plank6: bool = dataclasses.field(default=False)
    rotate_plank7: bool = dataclasses.field(default=False)
    rotate_plank8: bool = dataclasses.field(default=False)
    rotate_plank9: bool = dataclasses.field(default=False)
    unknown_0xe6b1d780: bool = dataclasses.field(default=False)
    unknown_0xdbd1fe30: bool = dataclasses.field(default=False)
    unknown_0x9c7184e0: bool = dataclasses.field(default=False)
    unknown_0xa111ad50: bool = dataclasses.field(default=False)
    unknown_0x13317140: bool = dataclasses.field(default=False)
    unknown_0x2e5158f0: bool = dataclasses.field(default=False)
    unknown_0x69f12220: bool = dataclasses.field(default=False)
    unknown_0x54910b90: bool = dataclasses.field(default=False)
    unknown_0xd6c19c41: bool = dataclasses.field(default=False)
    unknown_0xeba1b5f1: bool = dataclasses.field(default=False)
    ocean_bridge_struct_a_0x66a86577: OceanBridgeStructA = dataclasses.field(default_factory=OceanBridgeStructA)
    ocean_bridge_struct_a_0xfddb8fa3: OceanBridgeStructA = dataclasses.field(default_factory=OceanBridgeStructA)
    ocean_bridge_struct_a_0x8b3eb69e: OceanBridgeStructA = dataclasses.field(default_factory=OceanBridgeStructA)
    ocean_bridge_struct_a_0x104d5c4a: OceanBridgeStructA = dataclasses.field(default_factory=OceanBridgeStructA)
    ocean_bridge_struct_a_0x66f4c4e4: OceanBridgeStructA = dataclasses.field(default_factory=OceanBridgeStructA)
    ocean_bridge_struct_a_0xfd872e30: OceanBridgeStructA = dataclasses.field(default_factory=OceanBridgeStructA)
    ocean_bridge_struct_a_0x8b62170d: OceanBridgeStructA = dataclasses.field(default_factory=OceanBridgeStructA)
    ocean_bridge_struct_a_0x1011fdd9: OceanBridgeStructA = dataclasses.field(default_factory=OceanBridgeStructA)
    ocean_bridge_struct_a_0x66112651: OceanBridgeStructA = dataclasses.field(default_factory=OceanBridgeStructA)
    ocean_bridge_struct_a_0xfd62cc85: OceanBridgeStructA = dataclasses.field(default_factory=OceanBridgeStructA)
    ocean_bridge_struct_a_0x17a09d5f: OceanBridgeStructA = dataclasses.field(default_factory=OceanBridgeStructA)
    ocean_bridge_struct_a_0x8cd3778b: OceanBridgeStructA = dataclasses.field(default_factory=OceanBridgeStructA)
    ocean_bridge_struct_a_0xfa364eb6: OceanBridgeStructA = dataclasses.field(default_factory=OceanBridgeStructA)
    ocean_bridge_struct_a_0x6145a462: OceanBridgeStructA = dataclasses.field(default_factory=OceanBridgeStructA)
    ocean_bridge_struct_a_0x17fc3ccc: OceanBridgeStructA = dataclasses.field(default_factory=OceanBridgeStructA)
    ocean_bridge_struct_a_0x8c8fd618: OceanBridgeStructA = dataclasses.field(default_factory=OceanBridgeStructA)
    ocean_bridge_struct_a_0xfa6aef25: OceanBridgeStructA = dataclasses.field(default_factory=OceanBridgeStructA)
    ocean_bridge_struct_a_0x611905f1: OceanBridgeStructA = dataclasses.field(default_factory=OceanBridgeStructA)
    ocean_bridge_struct_a_0x1719de79: OceanBridgeStructA = dataclasses.field(default_factory=OceanBridgeStructA)
    ocean_bridge_struct_a_0x8c6a34ad: OceanBridgeStructA = dataclasses.field(default_factory=OceanBridgeStructA)
    ocean_bridge_struct_b_0xdafe5d7a: OceanBridgeStructB = dataclasses.field(default_factory=OceanBridgeStructB)
    ocean_bridge_struct_b_0x418db7ae: OceanBridgeStructB = dataclasses.field(default_factory=OceanBridgeStructB)
    ocean_bridge_struct_b_0x37688e93: OceanBridgeStructB = dataclasses.field(default_factory=OceanBridgeStructB)
    ocean_bridge_struct_b_0xac1b6447: OceanBridgeStructB = dataclasses.field(default_factory=OceanBridgeStructB)
    ocean_bridge_struct_b_0xdaa2fce9: OceanBridgeStructB = dataclasses.field(default_factory=OceanBridgeStructB)
    ocean_bridge_struct_b_0x41d1163d: OceanBridgeStructB = dataclasses.field(default_factory=OceanBridgeStructB)
    ocean_bridge_struct_b_0x37342f00: OceanBridgeStructB = dataclasses.field(default_factory=OceanBridgeStructB)
    ocean_bridge_struct_b_0xac47c5d4: OceanBridgeStructB = dataclasses.field(default_factory=OceanBridgeStructB)
    ocean_bridge_struct_b_0xda471e5c: OceanBridgeStructB = dataclasses.field(default_factory=OceanBridgeStructB)
    ocean_bridge_struct_b_0x4134f488: OceanBridgeStructB = dataclasses.field(default_factory=OceanBridgeStructB)
    ocean_bridge_struct_b_0x3ce60d48: OceanBridgeStructB = dataclasses.field(default_factory=OceanBridgeStructB)
    ocean_bridge_struct_b_0xa795e79c: OceanBridgeStructB = dataclasses.field(default_factory=OceanBridgeStructB)
    ocean_bridge_struct_b_0xd170dea1: OceanBridgeStructB = dataclasses.field(default_factory=OceanBridgeStructB)
    ocean_bridge_struct_b_0x4a033475: OceanBridgeStructB = dataclasses.field(default_factory=OceanBridgeStructB)
    ocean_bridge_struct_b_0x3cbaacdb: OceanBridgeStructB = dataclasses.field(default_factory=OceanBridgeStructB)
    ocean_bridge_struct_b_0xa7c9460f: OceanBridgeStructB = dataclasses.field(default_factory=OceanBridgeStructB)
    ocean_bridge_struct_b_0xd12c7f32: OceanBridgeStructB = dataclasses.field(default_factory=OceanBridgeStructB)
    ocean_bridge_struct_b_0x4a5f95e6: OceanBridgeStructB = dataclasses.field(default_factory=OceanBridgeStructB)
    ocean_bridge_struct_b_0x3c5f4e6e: OceanBridgeStructB = dataclasses.field(default_factory=OceanBridgeStructB)
    ocean_bridge_struct_b_0xa72ca4ba: OceanBridgeStructB = dataclasses.field(default_factory=OceanBridgeStructB)
    sfx_volume: float = dataclasses.field(default=1.0)
    caud_0xe7ca6050: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud_0x5d4fbc07: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0x0ed5e783: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    caud_0xa3bac487: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud_0x4fe79727: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0x1c7dcca3: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    caud_0x51ed297f: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud_0xeaeffc4b: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0xb975a7cf: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    caud_0xb6f08fe8: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud_0x89e8256f: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0xda727eeb: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    caud_0x6e33f4ce: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud_0x7b8e2cd2: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0x28147756: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0x0093800d: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0xccbb7330: Spline = dataclasses.field(default_factory=Spline)
    unknown_0xaa62345f: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x1852af24: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x0ba9a91c: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x6fcc7dd4: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x77c88cc7: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x7b066bac: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x64fadea2: Spline = dataclasses.field(default_factory=Spline)
    caud_0x751bfe84: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    acceptable_vascular: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud_0x3dba2f5c: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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
        data.write(b'\x00r')  # 114 properties

        data.write(b'\xe9\x93\x14_')  # 0xe993145f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xe993145f))

        data.write(b'i\xa2\xb0\x8e')  # 0x69a2b08e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0x69a2b08e))

        data.write(b'\xa2\xfec+')  # 0xa2fe632b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0xa2fe632b))

        data.write(b'$j\x11\x85')  # 0x246a1185
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.alt_model2))

        data.write(b'\xef6\xc2 ')  # 0xef36c220
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xef36c220))

        data.write(b'\xf23\xf2\x98')  # 0xf233f298
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xf233f298))

        data.write(b'\xf7\xaa_2')  # 0xf7aa5f32
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.z_motion.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd0#\x9f\x95')  # 0xd0239f95
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.y_rotation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'V\x88h;')  # 0x5688683b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.impulse_time_min))

        data.write(b'\xb0\xe8\xc7\xda')  # 0xb0e8c7da
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.impulse_time_max))

        data.write(b'##\xba\x82')  # 0x2323ba82
        data.write(b'\x00\x0c')  # size
        self.impulse_offset.to_stream(data)

        data.write(b'.hl*')  # 0x2e686c2a
        data.write(b'\x00\x0c')  # size
        self.collision_offset.to_stream(data)

        data.write(b'`E\xbb{')  # 0x6045bb7b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x6045bb7b))

        data.write(b'\xfei\xd6z')  # 0xfe69d67a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfe69d67a))

        data.write(b'\x84wY\xba')  # 0x847759ba
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x847759ba))

        data.write(b'\xe5\xb6\xb6f')  # 0xe5b6b666
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rise_min))

        data.write(b'\x03\xd6\x19\x87')  # 0x3d61987
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rise_max))

        data.write(b'\xc2F\xb3\xca')  # 0xc246b3ca
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rise_step))

        data.write(b'\xbd\xba\x19\x1e')  # 0xbdba191e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.target_height))

        data.write(b'u\xce\x0cy')  # 0x75ce0c79
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x75ce0c79))

        data.write(b'\xe5\xd8f\xf1')  # 0xe5d866f1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xe5d866f1))

        data.write(b'\xb0\x94bY')  # 0xb0946259
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xb0946259))

        data.write(b'\x81*\xfc\x85')  # 0x812afc85
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x812afc85))

        data.write(b'f\xad+\x98')  # 0x66ad2b98
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x66ad2b98))

        data.write(b'\x1d-\x96-')  # 0x1d2d962d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1d2d962d))

        data.write(b'\x9d\xee4z')  # 0x9dee347a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.center_plank))

        data.write(b'\x1f>\xadS')  # 0x1f3ead53
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.rotate_plank0))

        data.write(b'"^\x84\xe3')  # 0x225e84e3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.rotate_plank1))

        data.write(b'e\xfe\xfe3')  # 0x65fefe33
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.rotate_plank2))

        data.write(b'X\x9e\xd7\x83')  # 0x589ed783
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.rotate_plank3))

        data.write(b'\xea\xbe\x0b\x93')  # 0xeabe0b93
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.rotate_plank4))

        data.write(b'\xd7\xde"#')  # 0xd7de2223
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.rotate_plank5))

        data.write(b'\x90~X\xf3')  # 0x907e58f3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.rotate_plank6))

        data.write(b'\xad\x1eqC')  # 0xad1e7143
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.rotate_plank7))

        data.write(b'/N\xe6\x92')  # 0x2f4ee692
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.rotate_plank8))

        data.write(b'\x12.\xcf"')  # 0x122ecf22
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.rotate_plank9))

        data.write(b'\xe6\xb1\xd7\x80')  # 0xe6b1d780
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xe6b1d780))

        data.write(b'\xdb\xd1\xfe0')  # 0xdbd1fe30
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xdbd1fe30))

        data.write(b'\x9cq\x84\xe0')  # 0x9c7184e0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x9c7184e0))

        data.write(b'\xa1\x11\xadP')  # 0xa111ad50
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xa111ad50))

        data.write(b'\x131q@')  # 0x13317140
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x13317140))

        data.write(b'.QX\xf0')  # 0x2e5158f0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x2e5158f0))

        data.write(b'i\xf1" ')  # 0x69f12220
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x69f12220))

        data.write(b'T\x91\x0b\x90')  # 0x54910b90
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x54910b90))

        data.write(b'\xd6\xc1\x9cA')  # 0xd6c19c41
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xd6c19c41))

        data.write(b'\xeb\xa1\xb5\xf1')  # 0xeba1b5f1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xeba1b5f1))

        data.write(b'f\xa8ew')  # 0x66a86577
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_a_0x66a86577.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfd\xdb\x8f\xa3')  # 0xfddb8fa3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_a_0xfddb8fa3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8b>\xb6\x9e')  # 0x8b3eb69e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_a_0x8b3eb69e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x10M\\J')  # 0x104d5c4a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_a_0x104d5c4a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'f\xf4\xc4\xe4')  # 0x66f4c4e4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_a_0x66f4c4e4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfd\x87.0')  # 0xfd872e30
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_a_0xfd872e30.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8bb\x17\r')  # 0x8b62170d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_a_0x8b62170d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x10\x11\xfd\xd9')  # 0x1011fdd9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_a_0x1011fdd9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'f\x11&Q')  # 0x66112651
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_a_0x66112651.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfdb\xcc\x85')  # 0xfd62cc85
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_a_0xfd62cc85.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x17\xa0\x9d_')  # 0x17a09d5f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_a_0x17a09d5f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8c\xd3w\x8b')  # 0x8cd3778b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_a_0x8cd3778b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfa6N\xb6')  # 0xfa364eb6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_a_0xfa364eb6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'aE\xa4b')  # 0x6145a462
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_a_0x6145a462.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x17\xfc<\xcc')  # 0x17fc3ccc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_a_0x17fc3ccc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8c\x8f\xd6\x18')  # 0x8c8fd618
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_a_0x8c8fd618.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfaj\xef%')  # 0xfa6aef25
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_a_0xfa6aef25.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'a\x19\x05\xf1')  # 0x611905f1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_a_0x611905f1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x17\x19\xdey')  # 0x1719de79
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_a_0x1719de79.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8cj4\xad')  # 0x8c6a34ad
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_a_0x8c6a34ad.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xda\xfe]z')  # 0xdafe5d7a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_b_0xdafe5d7a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'A\x8d\xb7\xae')  # 0x418db7ae
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_b_0x418db7ae.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'7h\x8e\x93')  # 0x37688e93
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_b_0x37688e93.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xac\x1bdG')  # 0xac1b6447
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_b_0xac1b6447.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xda\xa2\xfc\xe9')  # 0xdaa2fce9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_b_0xdaa2fce9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'A\xd1\x16=')  # 0x41d1163d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_b_0x41d1163d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'74/\x00')  # 0x37342f00
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_b_0x37342f00.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xacG\xc5\xd4')  # 0xac47c5d4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_b_0xac47c5d4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdaG\x1e\\')  # 0xda471e5c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_b_0xda471e5c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'A4\xf4\x88')  # 0x4134f488
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_b_0x4134f488.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'<\xe6\rH')  # 0x3ce60d48
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_b_0x3ce60d48.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa7\x95\xe7\x9c')  # 0xa795e79c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_b_0xa795e79c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd1p\xde\xa1')  # 0xd170dea1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_b_0xd170dea1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'J\x034u')  # 0x4a033475
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_b_0x4a033475.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'<\xba\xac\xdb')  # 0x3cbaacdb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_b_0x3cbaacdb.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa7\xc9F\x0f')  # 0xa7c9460f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_b_0xa7c9460f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd1,\x7f2')  # 0xd12c7f32
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_b_0xd12c7f32.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'J_\x95\xe6')  # 0x4a5f95e6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_b_0x4a5f95e6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'<_Nn')  # 0x3c5f4e6e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_b_0x3c5f4e6e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa7,\xa4\xba')  # 0xa72ca4ba
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ocean_bridge_struct_b_0xa72ca4ba.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaa\xa1%m')  # 0xaaa1256d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.sfx_volume))

        data.write(b'\xe7\xca`P')  # 0xe7ca6050
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0xe7ca6050))

        data.write(b']O\xbc\x07')  # 0x5d4fbc07
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x5d4fbc07))

        data.write(b'\x0e\xd5\xe7\x83')  # 0xed5e783
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x0ed5e783))

        data.write(b'\xa3\xba\xc4\x87')  # 0xa3bac487
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0xa3bac487))

        data.write(b"O\xe7\x97'")  # 0x4fe79727
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x4fe79727))

        data.write(b'\x1c}\xcc\xa3')  # 0x1c7dcca3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x1c7dcca3))

        data.write(b'Q\xed)\x7f')  # 0x51ed297f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x51ed297f))

        data.write(b'\xea\xef\xfcK')  # 0xeaeffc4b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0xeaeffc4b))

        data.write(b'\xb9u\xa7\xcf')  # 0xb975a7cf
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xb975a7cf))

        data.write(b'\xb6\xf0\x8f\xe8')  # 0xb6f08fe8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0xb6f08fe8))

        data.write(b'\x89\xe8%o')  # 0x89e8256f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x89e8256f))

        data.write(b'\xdar~\xeb')  # 0xda727eeb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xda727eeb))

        data.write(b'n3\xf4\xce')  # 0x6e33f4ce
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x6e33f4ce))

        data.write(b'{\x8e,\xd2')  # 0x7b8e2cd2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x7b8e2cd2))

        data.write(b'(\x14wV')  # 0x28147756
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x28147756))

        data.write(b'\x00\x93\x80\r')  # 0x93800d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x0093800d))

        data.write(b'\xcc\xbbs0')  # 0xccbb7330
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xccbb7330.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaab4_')  # 0xaa62345f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xaa62345f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x18R\xaf$')  # 0x1852af24
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x1852af24.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0b\xa9\xa9\x1c')  # 0xba9a91c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x0ba9a91c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'o\xcc}\xd4')  # 0x6fcc7dd4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x6fcc7dd4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'w\xc8\x8c\xc7')  # 0x77c88cc7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x77c88cc7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'{\x06k\xac')  # 0x7b066bac
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x7b066bac.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'd\xfa\xde\xa2')  # 0x64fadea2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x64fadea2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'u\x1b\xfe\x84')  # 0x751bfe84
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x751bfe84))

        data.write(b'^\xb1\x13\xbf')  # 0x5eb113bf
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.acceptable_vascular))

        data.write(b'=\xba/\\')  # 0x3dba2f5c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x3dba2f5c))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xe993145f=data['unknown_0xe993145f'],
            cmdl_0x69a2b08e=data['cmdl_0x69a2b08e'],
            cmdl_0xa2fe632b=data['cmdl_0xa2fe632b'],
            alt_model2=data['alt_model2'],
            unknown_0xef36c220=data['unknown_0xef36c220'],
            unknown_0xf233f298=data['unknown_0xf233f298'],
            z_motion=Spline.from_json(data['z_motion']),
            y_rotation=Spline.from_json(data['y_rotation']),
            impulse_time_min=data['impulse_time_min'],
            impulse_time_max=data['impulse_time_max'],
            impulse_offset=Vector.from_json(data['impulse_offset']),
            collision_offset=Vector.from_json(data['collision_offset']),
            unknown_0x6045bb7b=data['unknown_0x6045bb7b'],
            unknown_0xfe69d67a=data['unknown_0xfe69d67a'],
            unknown_0x847759ba=data['unknown_0x847759ba'],
            rise_min=data['rise_min'],
            rise_max=data['rise_max'],
            rise_step=data['rise_step'],
            target_height=data['target_height'],
            unknown_0x75ce0c79=data['unknown_0x75ce0c79'],
            unknown_0xe5d866f1=data['unknown_0xe5d866f1'],
            unknown_0xb0946259=data['unknown_0xb0946259'],
            unknown_0x812afc85=data['unknown_0x812afc85'],
            unknown_0x66ad2b98=data['unknown_0x66ad2b98'],
            unknown_0x1d2d962d=data['unknown_0x1d2d962d'],
            center_plank=data['center_plank'],
            rotate_plank0=data['rotate_plank0'],
            rotate_plank1=data['rotate_plank1'],
            rotate_plank2=data['rotate_plank2'],
            rotate_plank3=data['rotate_plank3'],
            rotate_plank4=data['rotate_plank4'],
            rotate_plank5=data['rotate_plank5'],
            rotate_plank6=data['rotate_plank6'],
            rotate_plank7=data['rotate_plank7'],
            rotate_plank8=data['rotate_plank8'],
            rotate_plank9=data['rotate_plank9'],
            unknown_0xe6b1d780=data['unknown_0xe6b1d780'],
            unknown_0xdbd1fe30=data['unknown_0xdbd1fe30'],
            unknown_0x9c7184e0=data['unknown_0x9c7184e0'],
            unknown_0xa111ad50=data['unknown_0xa111ad50'],
            unknown_0x13317140=data['unknown_0x13317140'],
            unknown_0x2e5158f0=data['unknown_0x2e5158f0'],
            unknown_0x69f12220=data['unknown_0x69f12220'],
            unknown_0x54910b90=data['unknown_0x54910b90'],
            unknown_0xd6c19c41=data['unknown_0xd6c19c41'],
            unknown_0xeba1b5f1=data['unknown_0xeba1b5f1'],
            ocean_bridge_struct_a_0x66a86577=OceanBridgeStructA.from_json(data['ocean_bridge_struct_a_0x66a86577']),
            ocean_bridge_struct_a_0xfddb8fa3=OceanBridgeStructA.from_json(data['ocean_bridge_struct_a_0xfddb8fa3']),
            ocean_bridge_struct_a_0x8b3eb69e=OceanBridgeStructA.from_json(data['ocean_bridge_struct_a_0x8b3eb69e']),
            ocean_bridge_struct_a_0x104d5c4a=OceanBridgeStructA.from_json(data['ocean_bridge_struct_a_0x104d5c4a']),
            ocean_bridge_struct_a_0x66f4c4e4=OceanBridgeStructA.from_json(data['ocean_bridge_struct_a_0x66f4c4e4']),
            ocean_bridge_struct_a_0xfd872e30=OceanBridgeStructA.from_json(data['ocean_bridge_struct_a_0xfd872e30']),
            ocean_bridge_struct_a_0x8b62170d=OceanBridgeStructA.from_json(data['ocean_bridge_struct_a_0x8b62170d']),
            ocean_bridge_struct_a_0x1011fdd9=OceanBridgeStructA.from_json(data['ocean_bridge_struct_a_0x1011fdd9']),
            ocean_bridge_struct_a_0x66112651=OceanBridgeStructA.from_json(data['ocean_bridge_struct_a_0x66112651']),
            ocean_bridge_struct_a_0xfd62cc85=OceanBridgeStructA.from_json(data['ocean_bridge_struct_a_0xfd62cc85']),
            ocean_bridge_struct_a_0x17a09d5f=OceanBridgeStructA.from_json(data['ocean_bridge_struct_a_0x17a09d5f']),
            ocean_bridge_struct_a_0x8cd3778b=OceanBridgeStructA.from_json(data['ocean_bridge_struct_a_0x8cd3778b']),
            ocean_bridge_struct_a_0xfa364eb6=OceanBridgeStructA.from_json(data['ocean_bridge_struct_a_0xfa364eb6']),
            ocean_bridge_struct_a_0x6145a462=OceanBridgeStructA.from_json(data['ocean_bridge_struct_a_0x6145a462']),
            ocean_bridge_struct_a_0x17fc3ccc=OceanBridgeStructA.from_json(data['ocean_bridge_struct_a_0x17fc3ccc']),
            ocean_bridge_struct_a_0x8c8fd618=OceanBridgeStructA.from_json(data['ocean_bridge_struct_a_0x8c8fd618']),
            ocean_bridge_struct_a_0xfa6aef25=OceanBridgeStructA.from_json(data['ocean_bridge_struct_a_0xfa6aef25']),
            ocean_bridge_struct_a_0x611905f1=OceanBridgeStructA.from_json(data['ocean_bridge_struct_a_0x611905f1']),
            ocean_bridge_struct_a_0x1719de79=OceanBridgeStructA.from_json(data['ocean_bridge_struct_a_0x1719de79']),
            ocean_bridge_struct_a_0x8c6a34ad=OceanBridgeStructA.from_json(data['ocean_bridge_struct_a_0x8c6a34ad']),
            ocean_bridge_struct_b_0xdafe5d7a=OceanBridgeStructB.from_json(data['ocean_bridge_struct_b_0xdafe5d7a']),
            ocean_bridge_struct_b_0x418db7ae=OceanBridgeStructB.from_json(data['ocean_bridge_struct_b_0x418db7ae']),
            ocean_bridge_struct_b_0x37688e93=OceanBridgeStructB.from_json(data['ocean_bridge_struct_b_0x37688e93']),
            ocean_bridge_struct_b_0xac1b6447=OceanBridgeStructB.from_json(data['ocean_bridge_struct_b_0xac1b6447']),
            ocean_bridge_struct_b_0xdaa2fce9=OceanBridgeStructB.from_json(data['ocean_bridge_struct_b_0xdaa2fce9']),
            ocean_bridge_struct_b_0x41d1163d=OceanBridgeStructB.from_json(data['ocean_bridge_struct_b_0x41d1163d']),
            ocean_bridge_struct_b_0x37342f00=OceanBridgeStructB.from_json(data['ocean_bridge_struct_b_0x37342f00']),
            ocean_bridge_struct_b_0xac47c5d4=OceanBridgeStructB.from_json(data['ocean_bridge_struct_b_0xac47c5d4']),
            ocean_bridge_struct_b_0xda471e5c=OceanBridgeStructB.from_json(data['ocean_bridge_struct_b_0xda471e5c']),
            ocean_bridge_struct_b_0x4134f488=OceanBridgeStructB.from_json(data['ocean_bridge_struct_b_0x4134f488']),
            ocean_bridge_struct_b_0x3ce60d48=OceanBridgeStructB.from_json(data['ocean_bridge_struct_b_0x3ce60d48']),
            ocean_bridge_struct_b_0xa795e79c=OceanBridgeStructB.from_json(data['ocean_bridge_struct_b_0xa795e79c']),
            ocean_bridge_struct_b_0xd170dea1=OceanBridgeStructB.from_json(data['ocean_bridge_struct_b_0xd170dea1']),
            ocean_bridge_struct_b_0x4a033475=OceanBridgeStructB.from_json(data['ocean_bridge_struct_b_0x4a033475']),
            ocean_bridge_struct_b_0x3cbaacdb=OceanBridgeStructB.from_json(data['ocean_bridge_struct_b_0x3cbaacdb']),
            ocean_bridge_struct_b_0xa7c9460f=OceanBridgeStructB.from_json(data['ocean_bridge_struct_b_0xa7c9460f']),
            ocean_bridge_struct_b_0xd12c7f32=OceanBridgeStructB.from_json(data['ocean_bridge_struct_b_0xd12c7f32']),
            ocean_bridge_struct_b_0x4a5f95e6=OceanBridgeStructB.from_json(data['ocean_bridge_struct_b_0x4a5f95e6']),
            ocean_bridge_struct_b_0x3c5f4e6e=OceanBridgeStructB.from_json(data['ocean_bridge_struct_b_0x3c5f4e6e']),
            ocean_bridge_struct_b_0xa72ca4ba=OceanBridgeStructB.from_json(data['ocean_bridge_struct_b_0xa72ca4ba']),
            sfx_volume=data['sfx_volume'],
            caud_0xe7ca6050=data['caud_0xe7ca6050'],
            caud_0x5d4fbc07=data['caud_0x5d4fbc07'],
            unknown_0x0ed5e783=data['unknown_0x0ed5e783'],
            caud_0xa3bac487=data['caud_0xa3bac487'],
            caud_0x4fe79727=data['caud_0x4fe79727'],
            unknown_0x1c7dcca3=data['unknown_0x1c7dcca3'],
            caud_0x51ed297f=data['caud_0x51ed297f'],
            caud_0xeaeffc4b=data['caud_0xeaeffc4b'],
            unknown_0xb975a7cf=data['unknown_0xb975a7cf'],
            caud_0xb6f08fe8=data['caud_0xb6f08fe8'],
            caud_0x89e8256f=data['caud_0x89e8256f'],
            unknown_0xda727eeb=data['unknown_0xda727eeb'],
            caud_0x6e33f4ce=data['caud_0x6e33f4ce'],
            caud_0x7b8e2cd2=data['caud_0x7b8e2cd2'],
            unknown_0x28147756=data['unknown_0x28147756'],
            unknown_0x0093800d=data['unknown_0x0093800d'],
            unknown_0xccbb7330=Spline.from_json(data['unknown_0xccbb7330']),
            unknown_0xaa62345f=Spline.from_json(data['unknown_0xaa62345f']),
            unknown_0x1852af24=Spline.from_json(data['unknown_0x1852af24']),
            unknown_0x0ba9a91c=Spline.from_json(data['unknown_0x0ba9a91c']),
            unknown_0x6fcc7dd4=Spline.from_json(data['unknown_0x6fcc7dd4']),
            unknown_0x77c88cc7=Spline.from_json(data['unknown_0x77c88cc7']),
            unknown_0x7b066bac=Spline.from_json(data['unknown_0x7b066bac']),
            unknown_0x64fadea2=Spline.from_json(data['unknown_0x64fadea2']),
            caud_0x751bfe84=data['caud_0x751bfe84'],
            acceptable_vascular=data['acceptable_vascular'],
            caud_0x3dba2f5c=data['caud_0x3dba2f5c'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xe993145f': self.unknown_0xe993145f,
            'cmdl_0x69a2b08e': self.cmdl_0x69a2b08e,
            'cmdl_0xa2fe632b': self.cmdl_0xa2fe632b,
            'alt_model2': self.alt_model2,
            'unknown_0xef36c220': self.unknown_0xef36c220,
            'unknown_0xf233f298': self.unknown_0xf233f298,
            'z_motion': self.z_motion.to_json(),
            'y_rotation': self.y_rotation.to_json(),
            'impulse_time_min': self.impulse_time_min,
            'impulse_time_max': self.impulse_time_max,
            'impulse_offset': self.impulse_offset.to_json(),
            'collision_offset': self.collision_offset.to_json(),
            'unknown_0x6045bb7b': self.unknown_0x6045bb7b,
            'unknown_0xfe69d67a': self.unknown_0xfe69d67a,
            'unknown_0x847759ba': self.unknown_0x847759ba,
            'rise_min': self.rise_min,
            'rise_max': self.rise_max,
            'rise_step': self.rise_step,
            'target_height': self.target_height,
            'unknown_0x75ce0c79': self.unknown_0x75ce0c79,
            'unknown_0xe5d866f1': self.unknown_0xe5d866f1,
            'unknown_0xb0946259': self.unknown_0xb0946259,
            'unknown_0x812afc85': self.unknown_0x812afc85,
            'unknown_0x66ad2b98': self.unknown_0x66ad2b98,
            'unknown_0x1d2d962d': self.unknown_0x1d2d962d,
            'center_plank': self.center_plank,
            'rotate_plank0': self.rotate_plank0,
            'rotate_plank1': self.rotate_plank1,
            'rotate_plank2': self.rotate_plank2,
            'rotate_plank3': self.rotate_plank3,
            'rotate_plank4': self.rotate_plank4,
            'rotate_plank5': self.rotate_plank5,
            'rotate_plank6': self.rotate_plank6,
            'rotate_plank7': self.rotate_plank7,
            'rotate_plank8': self.rotate_plank8,
            'rotate_plank9': self.rotate_plank9,
            'unknown_0xe6b1d780': self.unknown_0xe6b1d780,
            'unknown_0xdbd1fe30': self.unknown_0xdbd1fe30,
            'unknown_0x9c7184e0': self.unknown_0x9c7184e0,
            'unknown_0xa111ad50': self.unknown_0xa111ad50,
            'unknown_0x13317140': self.unknown_0x13317140,
            'unknown_0x2e5158f0': self.unknown_0x2e5158f0,
            'unknown_0x69f12220': self.unknown_0x69f12220,
            'unknown_0x54910b90': self.unknown_0x54910b90,
            'unknown_0xd6c19c41': self.unknown_0xd6c19c41,
            'unknown_0xeba1b5f1': self.unknown_0xeba1b5f1,
            'ocean_bridge_struct_a_0x66a86577': self.ocean_bridge_struct_a_0x66a86577.to_json(),
            'ocean_bridge_struct_a_0xfddb8fa3': self.ocean_bridge_struct_a_0xfddb8fa3.to_json(),
            'ocean_bridge_struct_a_0x8b3eb69e': self.ocean_bridge_struct_a_0x8b3eb69e.to_json(),
            'ocean_bridge_struct_a_0x104d5c4a': self.ocean_bridge_struct_a_0x104d5c4a.to_json(),
            'ocean_bridge_struct_a_0x66f4c4e4': self.ocean_bridge_struct_a_0x66f4c4e4.to_json(),
            'ocean_bridge_struct_a_0xfd872e30': self.ocean_bridge_struct_a_0xfd872e30.to_json(),
            'ocean_bridge_struct_a_0x8b62170d': self.ocean_bridge_struct_a_0x8b62170d.to_json(),
            'ocean_bridge_struct_a_0x1011fdd9': self.ocean_bridge_struct_a_0x1011fdd9.to_json(),
            'ocean_bridge_struct_a_0x66112651': self.ocean_bridge_struct_a_0x66112651.to_json(),
            'ocean_bridge_struct_a_0xfd62cc85': self.ocean_bridge_struct_a_0xfd62cc85.to_json(),
            'ocean_bridge_struct_a_0x17a09d5f': self.ocean_bridge_struct_a_0x17a09d5f.to_json(),
            'ocean_bridge_struct_a_0x8cd3778b': self.ocean_bridge_struct_a_0x8cd3778b.to_json(),
            'ocean_bridge_struct_a_0xfa364eb6': self.ocean_bridge_struct_a_0xfa364eb6.to_json(),
            'ocean_bridge_struct_a_0x6145a462': self.ocean_bridge_struct_a_0x6145a462.to_json(),
            'ocean_bridge_struct_a_0x17fc3ccc': self.ocean_bridge_struct_a_0x17fc3ccc.to_json(),
            'ocean_bridge_struct_a_0x8c8fd618': self.ocean_bridge_struct_a_0x8c8fd618.to_json(),
            'ocean_bridge_struct_a_0xfa6aef25': self.ocean_bridge_struct_a_0xfa6aef25.to_json(),
            'ocean_bridge_struct_a_0x611905f1': self.ocean_bridge_struct_a_0x611905f1.to_json(),
            'ocean_bridge_struct_a_0x1719de79': self.ocean_bridge_struct_a_0x1719de79.to_json(),
            'ocean_bridge_struct_a_0x8c6a34ad': self.ocean_bridge_struct_a_0x8c6a34ad.to_json(),
            'ocean_bridge_struct_b_0xdafe5d7a': self.ocean_bridge_struct_b_0xdafe5d7a.to_json(),
            'ocean_bridge_struct_b_0x418db7ae': self.ocean_bridge_struct_b_0x418db7ae.to_json(),
            'ocean_bridge_struct_b_0x37688e93': self.ocean_bridge_struct_b_0x37688e93.to_json(),
            'ocean_bridge_struct_b_0xac1b6447': self.ocean_bridge_struct_b_0xac1b6447.to_json(),
            'ocean_bridge_struct_b_0xdaa2fce9': self.ocean_bridge_struct_b_0xdaa2fce9.to_json(),
            'ocean_bridge_struct_b_0x41d1163d': self.ocean_bridge_struct_b_0x41d1163d.to_json(),
            'ocean_bridge_struct_b_0x37342f00': self.ocean_bridge_struct_b_0x37342f00.to_json(),
            'ocean_bridge_struct_b_0xac47c5d4': self.ocean_bridge_struct_b_0xac47c5d4.to_json(),
            'ocean_bridge_struct_b_0xda471e5c': self.ocean_bridge_struct_b_0xda471e5c.to_json(),
            'ocean_bridge_struct_b_0x4134f488': self.ocean_bridge_struct_b_0x4134f488.to_json(),
            'ocean_bridge_struct_b_0x3ce60d48': self.ocean_bridge_struct_b_0x3ce60d48.to_json(),
            'ocean_bridge_struct_b_0xa795e79c': self.ocean_bridge_struct_b_0xa795e79c.to_json(),
            'ocean_bridge_struct_b_0xd170dea1': self.ocean_bridge_struct_b_0xd170dea1.to_json(),
            'ocean_bridge_struct_b_0x4a033475': self.ocean_bridge_struct_b_0x4a033475.to_json(),
            'ocean_bridge_struct_b_0x3cbaacdb': self.ocean_bridge_struct_b_0x3cbaacdb.to_json(),
            'ocean_bridge_struct_b_0xa7c9460f': self.ocean_bridge_struct_b_0xa7c9460f.to_json(),
            'ocean_bridge_struct_b_0xd12c7f32': self.ocean_bridge_struct_b_0xd12c7f32.to_json(),
            'ocean_bridge_struct_b_0x4a5f95e6': self.ocean_bridge_struct_b_0x4a5f95e6.to_json(),
            'ocean_bridge_struct_b_0x3c5f4e6e': self.ocean_bridge_struct_b_0x3c5f4e6e.to_json(),
            'ocean_bridge_struct_b_0xa72ca4ba': self.ocean_bridge_struct_b_0xa72ca4ba.to_json(),
            'sfx_volume': self.sfx_volume,
            'caud_0xe7ca6050': self.caud_0xe7ca6050,
            'caud_0x5d4fbc07': self.caud_0x5d4fbc07,
            'unknown_0x0ed5e783': self.unknown_0x0ed5e783,
            'caud_0xa3bac487': self.caud_0xa3bac487,
            'caud_0x4fe79727': self.caud_0x4fe79727,
            'unknown_0x1c7dcca3': self.unknown_0x1c7dcca3,
            'caud_0x51ed297f': self.caud_0x51ed297f,
            'caud_0xeaeffc4b': self.caud_0xeaeffc4b,
            'unknown_0xb975a7cf': self.unknown_0xb975a7cf,
            'caud_0xb6f08fe8': self.caud_0xb6f08fe8,
            'caud_0x89e8256f': self.caud_0x89e8256f,
            'unknown_0xda727eeb': self.unknown_0xda727eeb,
            'caud_0x6e33f4ce': self.caud_0x6e33f4ce,
            'caud_0x7b8e2cd2': self.caud_0x7b8e2cd2,
            'unknown_0x28147756': self.unknown_0x28147756,
            'unknown_0x0093800d': self.unknown_0x0093800d,
            'unknown_0xccbb7330': self.unknown_0xccbb7330.to_json(),
            'unknown_0xaa62345f': self.unknown_0xaa62345f.to_json(),
            'unknown_0x1852af24': self.unknown_0x1852af24.to_json(),
            'unknown_0x0ba9a91c': self.unknown_0x0ba9a91c.to_json(),
            'unknown_0x6fcc7dd4': self.unknown_0x6fcc7dd4.to_json(),
            'unknown_0x77c88cc7': self.unknown_0x77c88cc7.to_json(),
            'unknown_0x7b066bac': self.unknown_0x7b066bac.to_json(),
            'unknown_0x64fadea2': self.unknown_0x64fadea2.to_json(),
            'caud_0x751bfe84': self.caud_0x751bfe84,
            'acceptable_vascular': self.acceptable_vascular,
            'caud_0x3dba2f5c': self.caud_0x3dba2f5c,
        }


def _decode_unknown_0xe993145f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_cmdl_0x69a2b08e(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0xa2fe632b(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_alt_model2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xef36c220(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xf233f298(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_z_motion(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_y_rotation(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_impulse_time_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_impulse_time_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_impulse_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_collision_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_0x6045bb7b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xfe69d67a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x847759ba(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rise_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rise_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rise_step(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_target_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x75ce0c79(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe5d866f1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xb0946259(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x812afc85(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x66ad2b98(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1d2d962d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_center_plank(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_rotate_plank0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_rotate_plank1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_rotate_plank2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_rotate_plank3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_rotate_plank4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_rotate_plank5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_rotate_plank6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_rotate_plank7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_rotate_plank8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_rotate_plank9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xe6b1d780(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xdbd1fe30(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x9c7184e0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xa111ad50(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x13317140(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x2e5158f0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x69f12220(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x54910b90(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xd6c19c41(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xeba1b5f1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ocean_bridge_struct_a_0x66a86577(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructA.from_stream(data, property_size)


def _decode_ocean_bridge_struct_a_0xfddb8fa3(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructA.from_stream(data, property_size)


def _decode_ocean_bridge_struct_a_0x8b3eb69e(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructA.from_stream(data, property_size)


def _decode_ocean_bridge_struct_a_0x104d5c4a(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructA.from_stream(data, property_size)


def _decode_ocean_bridge_struct_a_0x66f4c4e4(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructA.from_stream(data, property_size)


def _decode_ocean_bridge_struct_a_0xfd872e30(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructA.from_stream(data, property_size)


def _decode_ocean_bridge_struct_a_0x8b62170d(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructA.from_stream(data, property_size)


def _decode_ocean_bridge_struct_a_0x1011fdd9(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructA.from_stream(data, property_size)


def _decode_ocean_bridge_struct_a_0x66112651(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructA.from_stream(data, property_size)


def _decode_ocean_bridge_struct_a_0xfd62cc85(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructA.from_stream(data, property_size)


def _decode_ocean_bridge_struct_a_0x17a09d5f(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructA.from_stream(data, property_size)


def _decode_ocean_bridge_struct_a_0x8cd3778b(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructA.from_stream(data, property_size)


def _decode_ocean_bridge_struct_a_0xfa364eb6(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructA.from_stream(data, property_size)


def _decode_ocean_bridge_struct_a_0x6145a462(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructA.from_stream(data, property_size)


def _decode_ocean_bridge_struct_a_0x17fc3ccc(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructA.from_stream(data, property_size)


def _decode_ocean_bridge_struct_a_0x8c8fd618(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructA.from_stream(data, property_size)


def _decode_ocean_bridge_struct_a_0xfa6aef25(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructA.from_stream(data, property_size)


def _decode_ocean_bridge_struct_a_0x611905f1(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructA.from_stream(data, property_size)


def _decode_ocean_bridge_struct_a_0x1719de79(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructA.from_stream(data, property_size)


def _decode_ocean_bridge_struct_a_0x8c6a34ad(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructA.from_stream(data, property_size)


def _decode_ocean_bridge_struct_b_0xdafe5d7a(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructB.from_stream(data, property_size)


def _decode_ocean_bridge_struct_b_0x418db7ae(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructB.from_stream(data, property_size)


def _decode_ocean_bridge_struct_b_0x37688e93(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructB.from_stream(data, property_size)


def _decode_ocean_bridge_struct_b_0xac1b6447(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructB.from_stream(data, property_size)


def _decode_ocean_bridge_struct_b_0xdaa2fce9(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructB.from_stream(data, property_size)


def _decode_ocean_bridge_struct_b_0x41d1163d(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructB.from_stream(data, property_size)


def _decode_ocean_bridge_struct_b_0x37342f00(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructB.from_stream(data, property_size)


def _decode_ocean_bridge_struct_b_0xac47c5d4(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructB.from_stream(data, property_size)


def _decode_ocean_bridge_struct_b_0xda471e5c(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructB.from_stream(data, property_size)


def _decode_ocean_bridge_struct_b_0x4134f488(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructB.from_stream(data, property_size)


def _decode_ocean_bridge_struct_b_0x3ce60d48(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructB.from_stream(data, property_size)


def _decode_ocean_bridge_struct_b_0xa795e79c(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructB.from_stream(data, property_size)


def _decode_ocean_bridge_struct_b_0xd170dea1(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructB.from_stream(data, property_size)


def _decode_ocean_bridge_struct_b_0x4a033475(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructB.from_stream(data, property_size)


def _decode_ocean_bridge_struct_b_0x3cbaacdb(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructB.from_stream(data, property_size)


def _decode_ocean_bridge_struct_b_0xa7c9460f(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructB.from_stream(data, property_size)


def _decode_ocean_bridge_struct_b_0xd12c7f32(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructB.from_stream(data, property_size)


def _decode_ocean_bridge_struct_b_0x4a5f95e6(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructB.from_stream(data, property_size)


def _decode_ocean_bridge_struct_b_0x3c5f4e6e(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructB.from_stream(data, property_size)


def _decode_ocean_bridge_struct_b_0xa72ca4ba(data: typing.BinaryIO, property_size: int):
    return OceanBridgeStructB.from_stream(data, property_size)


def _decode_sfx_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_caud_0xe7ca6050(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x5d4fbc07(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x0ed5e783(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0xa3bac487(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x4fe79727(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x1c7dcca3(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x51ed297f(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0xeaeffc4b(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xb975a7cf(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0xb6f08fe8(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x89e8256f(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xda727eeb(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x6e33f4ce(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x7b8e2cd2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x28147756(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x0093800d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xccbb7330(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0xaa62345f(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x1852af24(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x0ba9a91c(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x6fcc7dd4(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x77c88cc7(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x7b066bac(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x64fadea2(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_caud_0x751bfe84(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_acceptable_vascular(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x3dba2f5c(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe993145f: ('unknown_0xe993145f', _decode_unknown_0xe993145f),
    0x69a2b08e: ('cmdl_0x69a2b08e', _decode_cmdl_0x69a2b08e),
    0xa2fe632b: ('cmdl_0xa2fe632b', _decode_cmdl_0xa2fe632b),
    0x246a1185: ('alt_model2', _decode_alt_model2),
    0xef36c220: ('unknown_0xef36c220', _decode_unknown_0xef36c220),
    0xf233f298: ('unknown_0xf233f298', _decode_unknown_0xf233f298),
    0xf7aa5f32: ('z_motion', _decode_z_motion),
    0xd0239f95: ('y_rotation', _decode_y_rotation),
    0x5688683b: ('impulse_time_min', _decode_impulse_time_min),
    0xb0e8c7da: ('impulse_time_max', _decode_impulse_time_max),
    0x2323ba82: ('impulse_offset', _decode_impulse_offset),
    0x2e686c2a: ('collision_offset', _decode_collision_offset),
    0x6045bb7b: ('unknown_0x6045bb7b', _decode_unknown_0x6045bb7b),
    0xfe69d67a: ('unknown_0xfe69d67a', _decode_unknown_0xfe69d67a),
    0x847759ba: ('unknown_0x847759ba', _decode_unknown_0x847759ba),
    0xe5b6b666: ('rise_min', _decode_rise_min),
    0x3d61987: ('rise_max', _decode_rise_max),
    0xc246b3ca: ('rise_step', _decode_rise_step),
    0xbdba191e: ('target_height', _decode_target_height),
    0x75ce0c79: ('unknown_0x75ce0c79', _decode_unknown_0x75ce0c79),
    0xe5d866f1: ('unknown_0xe5d866f1', _decode_unknown_0xe5d866f1),
    0xb0946259: ('unknown_0xb0946259', _decode_unknown_0xb0946259),
    0x812afc85: ('unknown_0x812afc85', _decode_unknown_0x812afc85),
    0x66ad2b98: ('unknown_0x66ad2b98', _decode_unknown_0x66ad2b98),
    0x1d2d962d: ('unknown_0x1d2d962d', _decode_unknown_0x1d2d962d),
    0x9dee347a: ('center_plank', _decode_center_plank),
    0x1f3ead53: ('rotate_plank0', _decode_rotate_plank0),
    0x225e84e3: ('rotate_plank1', _decode_rotate_plank1),
    0x65fefe33: ('rotate_plank2', _decode_rotate_plank2),
    0x589ed783: ('rotate_plank3', _decode_rotate_plank3),
    0xeabe0b93: ('rotate_plank4', _decode_rotate_plank4),
    0xd7de2223: ('rotate_plank5', _decode_rotate_plank5),
    0x907e58f3: ('rotate_plank6', _decode_rotate_plank6),
    0xad1e7143: ('rotate_plank7', _decode_rotate_plank7),
    0x2f4ee692: ('rotate_plank8', _decode_rotate_plank8),
    0x122ecf22: ('rotate_plank9', _decode_rotate_plank9),
    0xe6b1d780: ('unknown_0xe6b1d780', _decode_unknown_0xe6b1d780),
    0xdbd1fe30: ('unknown_0xdbd1fe30', _decode_unknown_0xdbd1fe30),
    0x9c7184e0: ('unknown_0x9c7184e0', _decode_unknown_0x9c7184e0),
    0xa111ad50: ('unknown_0xa111ad50', _decode_unknown_0xa111ad50),
    0x13317140: ('unknown_0x13317140', _decode_unknown_0x13317140),
    0x2e5158f0: ('unknown_0x2e5158f0', _decode_unknown_0x2e5158f0),
    0x69f12220: ('unknown_0x69f12220', _decode_unknown_0x69f12220),
    0x54910b90: ('unknown_0x54910b90', _decode_unknown_0x54910b90),
    0xd6c19c41: ('unknown_0xd6c19c41', _decode_unknown_0xd6c19c41),
    0xeba1b5f1: ('unknown_0xeba1b5f1', _decode_unknown_0xeba1b5f1),
    0x66a86577: ('ocean_bridge_struct_a_0x66a86577', _decode_ocean_bridge_struct_a_0x66a86577),
    0xfddb8fa3: ('ocean_bridge_struct_a_0xfddb8fa3', _decode_ocean_bridge_struct_a_0xfddb8fa3),
    0x8b3eb69e: ('ocean_bridge_struct_a_0x8b3eb69e', _decode_ocean_bridge_struct_a_0x8b3eb69e),
    0x104d5c4a: ('ocean_bridge_struct_a_0x104d5c4a', _decode_ocean_bridge_struct_a_0x104d5c4a),
    0x66f4c4e4: ('ocean_bridge_struct_a_0x66f4c4e4', _decode_ocean_bridge_struct_a_0x66f4c4e4),
    0xfd872e30: ('ocean_bridge_struct_a_0xfd872e30', _decode_ocean_bridge_struct_a_0xfd872e30),
    0x8b62170d: ('ocean_bridge_struct_a_0x8b62170d', _decode_ocean_bridge_struct_a_0x8b62170d),
    0x1011fdd9: ('ocean_bridge_struct_a_0x1011fdd9', _decode_ocean_bridge_struct_a_0x1011fdd9),
    0x66112651: ('ocean_bridge_struct_a_0x66112651', _decode_ocean_bridge_struct_a_0x66112651),
    0xfd62cc85: ('ocean_bridge_struct_a_0xfd62cc85', _decode_ocean_bridge_struct_a_0xfd62cc85),
    0x17a09d5f: ('ocean_bridge_struct_a_0x17a09d5f', _decode_ocean_bridge_struct_a_0x17a09d5f),
    0x8cd3778b: ('ocean_bridge_struct_a_0x8cd3778b', _decode_ocean_bridge_struct_a_0x8cd3778b),
    0xfa364eb6: ('ocean_bridge_struct_a_0xfa364eb6', _decode_ocean_bridge_struct_a_0xfa364eb6),
    0x6145a462: ('ocean_bridge_struct_a_0x6145a462', _decode_ocean_bridge_struct_a_0x6145a462),
    0x17fc3ccc: ('ocean_bridge_struct_a_0x17fc3ccc', _decode_ocean_bridge_struct_a_0x17fc3ccc),
    0x8c8fd618: ('ocean_bridge_struct_a_0x8c8fd618', _decode_ocean_bridge_struct_a_0x8c8fd618),
    0xfa6aef25: ('ocean_bridge_struct_a_0xfa6aef25', _decode_ocean_bridge_struct_a_0xfa6aef25),
    0x611905f1: ('ocean_bridge_struct_a_0x611905f1', _decode_ocean_bridge_struct_a_0x611905f1),
    0x1719de79: ('ocean_bridge_struct_a_0x1719de79', _decode_ocean_bridge_struct_a_0x1719de79),
    0x8c6a34ad: ('ocean_bridge_struct_a_0x8c6a34ad', _decode_ocean_bridge_struct_a_0x8c6a34ad),
    0xdafe5d7a: ('ocean_bridge_struct_b_0xdafe5d7a', _decode_ocean_bridge_struct_b_0xdafe5d7a),
    0x418db7ae: ('ocean_bridge_struct_b_0x418db7ae', _decode_ocean_bridge_struct_b_0x418db7ae),
    0x37688e93: ('ocean_bridge_struct_b_0x37688e93', _decode_ocean_bridge_struct_b_0x37688e93),
    0xac1b6447: ('ocean_bridge_struct_b_0xac1b6447', _decode_ocean_bridge_struct_b_0xac1b6447),
    0xdaa2fce9: ('ocean_bridge_struct_b_0xdaa2fce9', _decode_ocean_bridge_struct_b_0xdaa2fce9),
    0x41d1163d: ('ocean_bridge_struct_b_0x41d1163d', _decode_ocean_bridge_struct_b_0x41d1163d),
    0x37342f00: ('ocean_bridge_struct_b_0x37342f00', _decode_ocean_bridge_struct_b_0x37342f00),
    0xac47c5d4: ('ocean_bridge_struct_b_0xac47c5d4', _decode_ocean_bridge_struct_b_0xac47c5d4),
    0xda471e5c: ('ocean_bridge_struct_b_0xda471e5c', _decode_ocean_bridge_struct_b_0xda471e5c),
    0x4134f488: ('ocean_bridge_struct_b_0x4134f488', _decode_ocean_bridge_struct_b_0x4134f488),
    0x3ce60d48: ('ocean_bridge_struct_b_0x3ce60d48', _decode_ocean_bridge_struct_b_0x3ce60d48),
    0xa795e79c: ('ocean_bridge_struct_b_0xa795e79c', _decode_ocean_bridge_struct_b_0xa795e79c),
    0xd170dea1: ('ocean_bridge_struct_b_0xd170dea1', _decode_ocean_bridge_struct_b_0xd170dea1),
    0x4a033475: ('ocean_bridge_struct_b_0x4a033475', _decode_ocean_bridge_struct_b_0x4a033475),
    0x3cbaacdb: ('ocean_bridge_struct_b_0x3cbaacdb', _decode_ocean_bridge_struct_b_0x3cbaacdb),
    0xa7c9460f: ('ocean_bridge_struct_b_0xa7c9460f', _decode_ocean_bridge_struct_b_0xa7c9460f),
    0xd12c7f32: ('ocean_bridge_struct_b_0xd12c7f32', _decode_ocean_bridge_struct_b_0xd12c7f32),
    0x4a5f95e6: ('ocean_bridge_struct_b_0x4a5f95e6', _decode_ocean_bridge_struct_b_0x4a5f95e6),
    0x3c5f4e6e: ('ocean_bridge_struct_b_0x3c5f4e6e', _decode_ocean_bridge_struct_b_0x3c5f4e6e),
    0xa72ca4ba: ('ocean_bridge_struct_b_0xa72ca4ba', _decode_ocean_bridge_struct_b_0xa72ca4ba),
    0xaaa1256d: ('sfx_volume', _decode_sfx_volume),
    0xe7ca6050: ('caud_0xe7ca6050', _decode_caud_0xe7ca6050),
    0x5d4fbc07: ('caud_0x5d4fbc07', _decode_caud_0x5d4fbc07),
    0xed5e783: ('unknown_0x0ed5e783', _decode_unknown_0x0ed5e783),
    0xa3bac487: ('caud_0xa3bac487', _decode_caud_0xa3bac487),
    0x4fe79727: ('caud_0x4fe79727', _decode_caud_0x4fe79727),
    0x1c7dcca3: ('unknown_0x1c7dcca3', _decode_unknown_0x1c7dcca3),
    0x51ed297f: ('caud_0x51ed297f', _decode_caud_0x51ed297f),
    0xeaeffc4b: ('caud_0xeaeffc4b', _decode_caud_0xeaeffc4b),
    0xb975a7cf: ('unknown_0xb975a7cf', _decode_unknown_0xb975a7cf),
    0xb6f08fe8: ('caud_0xb6f08fe8', _decode_caud_0xb6f08fe8),
    0x89e8256f: ('caud_0x89e8256f', _decode_caud_0x89e8256f),
    0xda727eeb: ('unknown_0xda727eeb', _decode_unknown_0xda727eeb),
    0x6e33f4ce: ('caud_0x6e33f4ce', _decode_caud_0x6e33f4ce),
    0x7b8e2cd2: ('caud_0x7b8e2cd2', _decode_caud_0x7b8e2cd2),
    0x28147756: ('unknown_0x28147756', _decode_unknown_0x28147756),
    0x93800d: ('unknown_0x0093800d', _decode_unknown_0x0093800d),
    0xccbb7330: ('unknown_0xccbb7330', _decode_unknown_0xccbb7330),
    0xaa62345f: ('unknown_0xaa62345f', _decode_unknown_0xaa62345f),
    0x1852af24: ('unknown_0x1852af24', _decode_unknown_0x1852af24),
    0xba9a91c: ('unknown_0x0ba9a91c', _decode_unknown_0x0ba9a91c),
    0x6fcc7dd4: ('unknown_0x6fcc7dd4', _decode_unknown_0x6fcc7dd4),
    0x77c88cc7: ('unknown_0x77c88cc7', _decode_unknown_0x77c88cc7),
    0x7b066bac: ('unknown_0x7b066bac', _decode_unknown_0x7b066bac),
    0x64fadea2: ('unknown_0x64fadea2', _decode_unknown_0x64fadea2),
    0x751bfe84: ('caud_0x751bfe84', _decode_caud_0x751bfe84),
    0x5eb113bf: ('acceptable_vascular', _decode_acceptable_vascular),
    0x3dba2f5c: ('caud_0x3dba2f5c', _decode_caud_0x3dba2f5c),
}
