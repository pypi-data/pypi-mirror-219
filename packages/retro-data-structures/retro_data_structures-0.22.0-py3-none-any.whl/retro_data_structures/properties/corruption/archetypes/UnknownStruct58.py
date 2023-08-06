# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.PlasmaBeamInfo import PlasmaBeamInfo
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct58(BaseProperty):
    unknown_0x90aefee1: bool = dataclasses.field(default=True)
    char: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    swarm_bot_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    part_0xb64ed093: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_0xc7dc6d3e: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0x41481f90: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    giant_form_electric_effect: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    part_0x3b5b99a8: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    giant_electric_ball_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0x2975be8d: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0x3dcf98a5: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0xdc17fb84: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0xc35db9ce: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0xa70e1bbb: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0x7cc1b298: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0x7be868ce: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    ring_idle_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0x4d9ed8e1: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    ring_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    ring_explosion_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    wheel_portal_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    wheel_tumble_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0xe3c3de5e: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    shock_not_solid: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    elsc: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    part_0x3b6cdadb: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0xa6e942ed: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    plasma_beam_info: PlasmaBeamInfo = dataclasses.field(default_factory=PlasmaBeamInfo)
    part_0x82ee63c8: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0xab0a66da: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    txtr: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    unknown_0x4f6e81a8: float = dataclasses.field(default=100.0)
    interface_delayed_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    scan_sphere_form: AssetId = dataclasses.field(metadata={'asset_types': ['SCAN']}, default=default_asset_id)
    scan_tornado_form: AssetId = dataclasses.field(metadata={'asset_types': ['SCAN']}, default=default_asset_id)
    scan_wheel_form: AssetId = dataclasses.field(metadata={'asset_types': ['SCAN']}, default=default_asset_id)
    scan_ring_form: AssetId = dataclasses.field(metadata={'asset_types': ['SCAN']}, default=default_asset_id)
    scan_giant_form: AssetId = dataclasses.field(metadata={'asset_types': ['SCAN']}, default=default_asset_id)
    scan: AssetId = dataclasses.field(metadata={'asset_types': ['SCAN']}, default=default_asset_id)
    caud_0x9a469187: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud_0xa959b017: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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
        data.write(b'\x00)')  # 41 properties

        data.write(b'\x90\xae\xfe\xe1')  # 0x90aefee1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x90aefee1))

        data.write(b'Ld\xd3\xa6')  # 0x4c64d3a6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.char.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x00\xdd\x06\xcc')  # 0xdd06cc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.swarm_bot_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb6N\xd0\x93')  # 0xb64ed093
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0xb64ed093))

        data.write(b'\xc7\xdcm>')  # 0xc7dc6d3e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xc7dc6d3e))

        data.write(b'AH\x1f\x90')  # 0x41481f90
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x41481f90))

        data.write(b'\xc5\x01*8')  # 0xc5012a38
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.giant_form_electric_effect))

        data.write(b';[\x99\xa8')  # 0x3b5b99a8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0x3b5b99a8))

        data.write(b'j\xe0\xca\xe6')  # 0x6ae0cae6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.giant_electric_ball_effect))

        data.write(b')u\xbe\x8d')  # 0x2975be8d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0x2975be8d))

        data.write(b'=\xcf\x98\xa5')  # 0x3dcf98a5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0x3dcf98a5))

        data.write(b'\xdc\x17\xfb\x84')  # 0xdc17fb84
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0xdc17fb84))

        data.write(b'\xc3]\xb9\xce')  # 0xc35db9ce
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0xc35db9ce))

        data.write(b'\xa7\x0e\x1b\xbb')  # 0xa70e1bbb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0xa70e1bbb))

        data.write(b'|\xc1\xb2\x98')  # 0x7cc1b298
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0x7cc1b298))

        data.write(b'{\xe8h\xce')  # 0x7be868ce
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0x7be868ce))

        data.write(b'\xc9\x0c\xda\x8c')  # 0xc90cda8c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.ring_idle_effect))

        data.write(b'M\x9e\xd8\xe1')  # 0x4d9ed8e1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0x4d9ed8e1))

        data.write(b'!\xdcL5')  # 0x21dc4c35
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.ring_projectile))

        data.write(b'\xcbg=\xa3')  # 0xcb673da3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.ring_explosion_effect))

        data.write(b'\xc1\xbb\xbe\xd8')  # 0xc1bbbed8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.wheel_portal_effect))

        data.write(b'\xf48lB')  # 0xf4386c42
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.wheel_tumble_effect))

        data.write(b'\xe3\xc3\xde^')  # 0xe3c3de5e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0xe3c3de5e))

        data.write(b'\x18\x99\xc89')  # 0x1899c839
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.shock_not_solid))

        data.write(b'kf\x06\xb8')  # 0x6b6606b8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.elsc))

        data.write(b';l\xda\xdb')  # 0x3b6cdadb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0x3b6cdadb))

        data.write(b'\xa6\xe9B\xed')  # 0xa6e942ed
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0xa6e942ed))

        data.write(b'!\xec=!')  # 0x21ec3d21
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.plasma_beam_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x82\xeec\xc8')  # 0x82ee63c8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0x82ee63c8))

        data.write(b'\xab\nf\xda')  # 0xab0a66da
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0xab0a66da))

        data.write(b'[g\xa4\xe7')  # 0x5b67a4e7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.txtr))

        data.write(b'On\x81\xa8')  # 0x4f6e81a8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4f6e81a8))

        data.write(b'\xadn\xcc\x7f')  # 0xad6ecc7f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.interface_delayed_effect))

        data.write(b'\x91\xd5\xf3\x17')  # 0x91d5f317
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.scan_sphere_form))

        data.write(b'\x1d\xdf\xd4Z')  # 0x1ddfd45a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.scan_tornado_form))

        data.write(b'\x01\xfb\xa7H')  # 0x1fba748
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.scan_wheel_form))

        data.write(b'\xcd/=\x00')  # 0xcd2f3d00
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.scan_ring_form))

        data.write(b'\xae\x81?\x86')  # 0xae813f86
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.scan_giant_form))

        data.write(b'\xd2~\x87\x86')  # 0xd27e8786
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.scan))

        data.write(b'\x9aF\x91\x87')  # 0x9a469187
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x9a469187))

        data.write(b'\xa9Y\xb0\x17')  # 0xa959b017
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0xa959b017))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x90aefee1=data['unknown_0x90aefee1'],
            char=AnimationParameters.from_json(data['char']),
            swarm_bot_vulnerability=DamageVulnerability.from_json(data['swarm_bot_vulnerability']),
            part_0xb64ed093=data['part_0xb64ed093'],
            unknown_0xc7dc6d3e=data['unknown_0xc7dc6d3e'],
            unknown_0x41481f90=data['unknown_0x41481f90'],
            giant_form_electric_effect=data['giant_form_electric_effect'],
            part_0x3b5b99a8=data['part_0x3b5b99a8'],
            giant_electric_ball_effect=data['giant_electric_ball_effect'],
            part_0x2975be8d=data['part_0x2975be8d'],
            part_0x3dcf98a5=data['part_0x3dcf98a5'],
            part_0xdc17fb84=data['part_0xdc17fb84'],
            part_0xc35db9ce=data['part_0xc35db9ce'],
            part_0xa70e1bbb=data['part_0xa70e1bbb'],
            part_0x7cc1b298=data['part_0x7cc1b298'],
            part_0x7be868ce=data['part_0x7be868ce'],
            ring_idle_effect=data['ring_idle_effect'],
            part_0x4d9ed8e1=data['part_0x4d9ed8e1'],
            ring_projectile=data['ring_projectile'],
            ring_explosion_effect=data['ring_explosion_effect'],
            wheel_portal_effect=data['wheel_portal_effect'],
            wheel_tumble_effect=data['wheel_tumble_effect'],
            part_0xe3c3de5e=data['part_0xe3c3de5e'],
            shock_not_solid=data['shock_not_solid'],
            elsc=data['elsc'],
            part_0x3b6cdadb=data['part_0x3b6cdadb'],
            part_0xa6e942ed=data['part_0xa6e942ed'],
            plasma_beam_info=PlasmaBeamInfo.from_json(data['plasma_beam_info']),
            part_0x82ee63c8=data['part_0x82ee63c8'],
            part_0xab0a66da=data['part_0xab0a66da'],
            txtr=data['txtr'],
            unknown_0x4f6e81a8=data['unknown_0x4f6e81a8'],
            interface_delayed_effect=data['interface_delayed_effect'],
            scan_sphere_form=data['scan_sphere_form'],
            scan_tornado_form=data['scan_tornado_form'],
            scan_wheel_form=data['scan_wheel_form'],
            scan_ring_form=data['scan_ring_form'],
            scan_giant_form=data['scan_giant_form'],
            scan=data['scan'],
            caud_0x9a469187=data['caud_0x9a469187'],
            caud_0xa959b017=data['caud_0xa959b017'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x90aefee1': self.unknown_0x90aefee1,
            'char': self.char.to_json(),
            'swarm_bot_vulnerability': self.swarm_bot_vulnerability.to_json(),
            'part_0xb64ed093': self.part_0xb64ed093,
            'unknown_0xc7dc6d3e': self.unknown_0xc7dc6d3e,
            'unknown_0x41481f90': self.unknown_0x41481f90,
            'giant_form_electric_effect': self.giant_form_electric_effect,
            'part_0x3b5b99a8': self.part_0x3b5b99a8,
            'giant_electric_ball_effect': self.giant_electric_ball_effect,
            'part_0x2975be8d': self.part_0x2975be8d,
            'part_0x3dcf98a5': self.part_0x3dcf98a5,
            'part_0xdc17fb84': self.part_0xdc17fb84,
            'part_0xc35db9ce': self.part_0xc35db9ce,
            'part_0xa70e1bbb': self.part_0xa70e1bbb,
            'part_0x7cc1b298': self.part_0x7cc1b298,
            'part_0x7be868ce': self.part_0x7be868ce,
            'ring_idle_effect': self.ring_idle_effect,
            'part_0x4d9ed8e1': self.part_0x4d9ed8e1,
            'ring_projectile': self.ring_projectile,
            'ring_explosion_effect': self.ring_explosion_effect,
            'wheel_portal_effect': self.wheel_portal_effect,
            'wheel_tumble_effect': self.wheel_tumble_effect,
            'part_0xe3c3de5e': self.part_0xe3c3de5e,
            'shock_not_solid': self.shock_not_solid,
            'elsc': self.elsc,
            'part_0x3b6cdadb': self.part_0x3b6cdadb,
            'part_0xa6e942ed': self.part_0xa6e942ed,
            'plasma_beam_info': self.plasma_beam_info.to_json(),
            'part_0x82ee63c8': self.part_0x82ee63c8,
            'part_0xab0a66da': self.part_0xab0a66da,
            'txtr': self.txtr,
            'unknown_0x4f6e81a8': self.unknown_0x4f6e81a8,
            'interface_delayed_effect': self.interface_delayed_effect,
            'scan_sphere_form': self.scan_sphere_form,
            'scan_tornado_form': self.scan_tornado_form,
            'scan_wheel_form': self.scan_wheel_form,
            'scan_ring_form': self.scan_ring_form,
            'scan_giant_form': self.scan_giant_form,
            'scan': self.scan,
            'caud_0x9a469187': self.caud_0x9a469187,
            'caud_0xa959b017': self.caud_0xa959b017,
        }


def _decode_unknown_0x90aefee1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_char(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_swarm_bot_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_part_0xb64ed093(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xc7dc6d3e(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x41481f90(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_giant_form_electric_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0x3b5b99a8(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_giant_electric_ball_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0x2975be8d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0x3dcf98a5(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0xdc17fb84(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0xc35db9ce(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0xa70e1bbb(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0x7cc1b298(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0x7be868ce(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_ring_idle_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0x4d9ed8e1(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_ring_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_ring_explosion_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_wheel_portal_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_wheel_tumble_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0xe3c3de5e(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_shock_not_solid(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_elsc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0x3b6cdadb(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0xa6e942ed(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_plasma_beam_info(data: typing.BinaryIO, property_size: int):
    return PlasmaBeamInfo.from_stream(data, property_size)


def _decode_part_0x82ee63c8(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0xab0a66da(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_txtr(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x4f6e81a8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_interface_delayed_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_scan_sphere_form(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_scan_tornado_form(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_scan_wheel_form(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_scan_ring_form(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_scan_giant_form(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_scan(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x9a469187(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0xa959b017(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x90aefee1: ('unknown_0x90aefee1', _decode_unknown_0x90aefee1),
    0x4c64d3a6: ('char', _decode_char),
    0xdd06cc: ('swarm_bot_vulnerability', _decode_swarm_bot_vulnerability),
    0xb64ed093: ('part_0xb64ed093', _decode_part_0xb64ed093),
    0xc7dc6d3e: ('unknown_0xc7dc6d3e', _decode_unknown_0xc7dc6d3e),
    0x41481f90: ('unknown_0x41481f90', _decode_unknown_0x41481f90),
    0xc5012a38: ('giant_form_electric_effect', _decode_giant_form_electric_effect),
    0x3b5b99a8: ('part_0x3b5b99a8', _decode_part_0x3b5b99a8),
    0x6ae0cae6: ('giant_electric_ball_effect', _decode_giant_electric_ball_effect),
    0x2975be8d: ('part_0x2975be8d', _decode_part_0x2975be8d),
    0x3dcf98a5: ('part_0x3dcf98a5', _decode_part_0x3dcf98a5),
    0xdc17fb84: ('part_0xdc17fb84', _decode_part_0xdc17fb84),
    0xc35db9ce: ('part_0xc35db9ce', _decode_part_0xc35db9ce),
    0xa70e1bbb: ('part_0xa70e1bbb', _decode_part_0xa70e1bbb),
    0x7cc1b298: ('part_0x7cc1b298', _decode_part_0x7cc1b298),
    0x7be868ce: ('part_0x7be868ce', _decode_part_0x7be868ce),
    0xc90cda8c: ('ring_idle_effect', _decode_ring_idle_effect),
    0x4d9ed8e1: ('part_0x4d9ed8e1', _decode_part_0x4d9ed8e1),
    0x21dc4c35: ('ring_projectile', _decode_ring_projectile),
    0xcb673da3: ('ring_explosion_effect', _decode_ring_explosion_effect),
    0xc1bbbed8: ('wheel_portal_effect', _decode_wheel_portal_effect),
    0xf4386c42: ('wheel_tumble_effect', _decode_wheel_tumble_effect),
    0xe3c3de5e: ('part_0xe3c3de5e', _decode_part_0xe3c3de5e),
    0x1899c839: ('shock_not_solid', _decode_shock_not_solid),
    0x6b6606b8: ('elsc', _decode_elsc),
    0x3b6cdadb: ('part_0x3b6cdadb', _decode_part_0x3b6cdadb),
    0xa6e942ed: ('part_0xa6e942ed', _decode_part_0xa6e942ed),
    0x21ec3d21: ('plasma_beam_info', _decode_plasma_beam_info),
    0x82ee63c8: ('part_0x82ee63c8', _decode_part_0x82ee63c8),
    0xab0a66da: ('part_0xab0a66da', _decode_part_0xab0a66da),
    0x5b67a4e7: ('txtr', _decode_txtr),
    0x4f6e81a8: ('unknown_0x4f6e81a8', _decode_unknown_0x4f6e81a8),
    0xad6ecc7f: ('interface_delayed_effect', _decode_interface_delayed_effect),
    0x91d5f317: ('scan_sphere_form', _decode_scan_sphere_form),
    0x1ddfd45a: ('scan_tornado_form', _decode_scan_tornado_form),
    0x1fba748: ('scan_wheel_form', _decode_scan_wheel_form),
    0xcd2f3d00: ('scan_ring_form', _decode_scan_ring_form),
    0xae813f86: ('scan_giant_form', _decode_scan_giant_form),
    0xd27e8786: ('scan', _decode_scan),
    0x9a469187: ('caud_0x9a469187', _decode_caud_0x9a469187),
    0xa959b017: ('caud_0xa959b017', _decode_caud_0xa959b017),
}
