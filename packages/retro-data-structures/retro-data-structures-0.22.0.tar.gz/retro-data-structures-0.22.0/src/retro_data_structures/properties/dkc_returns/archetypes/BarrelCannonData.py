# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums


@dataclasses.dataclass()
class BarrelCannonData(BaseProperty):
    grab_radius: float = dataclasses.field(default=1.5)
    release_radius: float = dataclasses.field(default=3.0)
    ignore_gravity_radius: float = dataclasses.field(default=1.0)
    unknown_0x49d8e65a: bool = dataclasses.field(default=False)
    launch_behavior: int = dataclasses.field(default=0)  # Choice
    launch_timer: float = dataclasses.field(default=0.15000000596046448)
    launch_direction: int = dataclasses.field(default=0)  # Choice
    launch_speed: float = dataclasses.field(default=21.0)
    unknown_0xc440842b: float = dataclasses.field(default=0.0)
    unknown_0x9bb1543f: float = dataclasses.field(default=1.0499999523162842)
    target_reorientation_time: float = dataclasses.field(default=0.20000000298023224)
    render_texture_set: int = dataclasses.field(default=0)
    unknown_0x97ad5bee: bool = dataclasses.field(default=True)
    unknown_0x094b5ad6: bool = dataclasses.field(default=True)
    unknown_0x25967162: bool = dataclasses.field(default=True)
    unknown_0x26b5fcdf: bool = dataclasses.field(default=True)
    allow_air_control: bool = dataclasses.field(default=False)
    unknown_0x36051905: bool = dataclasses.field(default=True)
    unknown_0xfc4118dd: bool = dataclasses.field(default=True)
    unknown_0x06d1b8c7: bool = dataclasses.field(default=False)
    unknown_0x341f63f8: bool = dataclasses.field(default=False)
    unknown_0x4d6847e5: bool = dataclasses.field(default=False)
    unknown_0x2255a13d: bool = dataclasses.field(default=False)
    barrel_cannon_enum_0x98501823: enums.BarrelCannonEnum = dataclasses.field(default=enums.BarrelCannonEnum.Unknown2)
    barrel_cannon_enum_0x098ecab6: enums.BarrelCannonEnum = dataclasses.field(default=enums.BarrelCannonEnum.Unknown4)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

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

        data.write(b'\x89fG#')  # 0x89664723
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grab_radius))

        data.write(b'+/E\x19')  # 0x2b2f4519
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.release_radius))

        data.write(b'\xfb5\xa9Z')  # 0xfb35a95a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ignore_gravity_radius))

        data.write(b'I\xd8\xe6Z')  # 0x49d8e65a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x49d8e65a))

        data.write(b'-*J\xd6')  # 0x2d2a4ad6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.launch_behavior))

        data.write(b'\xd5\xed\x0fw')  # 0xd5ed0f77
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.launch_timer))

        data.write(b'\x89\xd7y\x1e')  # 0x89d7791e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.launch_direction))

        data.write(b'18\x1a\x17')  # 0x31381a17
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.launch_speed))

        data.write(b'\xc4@\x84+')  # 0xc440842b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc440842b))

        data.write(b'\x9b\xb1T?')  # 0x9bb1543f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9bb1543f))

        data.write(b'\x06\x13!\xae')  # 0x61321ae
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.target_reorientation_time))

        data.write(b'2\xfa\xb9~')  # 0x32fab97e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.render_texture_set))

        data.write(b'\x97\xad[\xee')  # 0x97ad5bee
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x97ad5bee))

        data.write(b'\tKZ\xd6')  # 0x94b5ad6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x094b5ad6))

        data.write(b'%\x96qb')  # 0x25967162
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x25967162))

        data.write(b'&\xb5\xfc\xdf')  # 0x26b5fcdf
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x26b5fcdf))

        data.write(b'l*\xd8\xb4')  # 0x6c2ad8b4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_air_control))

        data.write(b'6\x05\x19\x05')  # 0x36051905
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x36051905))

        data.write(b'\xfcA\x18\xdd')  # 0xfc4118dd
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xfc4118dd))

        data.write(b'\x06\xd1\xb8\xc7')  # 0x6d1b8c7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x06d1b8c7))

        data.write(b'4\x1fc\xf8')  # 0x341f63f8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x341f63f8))

        data.write(b'MhG\xe5')  # 0x4d6847e5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x4d6847e5))

        data.write(b'"U\xa1=')  # 0x2255a13d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x2255a13d))

        data.write(b'\x98P\x18#')  # 0x98501823
        data.write(b'\x00\x04')  # size
        self.barrel_cannon_enum_0x98501823.to_stream(data)

        data.write(b'\t\x8e\xca\xb6')  # 0x98ecab6
        data.write(b'\x00\x04')  # size
        self.barrel_cannon_enum_0x098ecab6.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            grab_radius=data['grab_radius'],
            release_radius=data['release_radius'],
            ignore_gravity_radius=data['ignore_gravity_radius'],
            unknown_0x49d8e65a=data['unknown_0x49d8e65a'],
            launch_behavior=data['launch_behavior'],
            launch_timer=data['launch_timer'],
            launch_direction=data['launch_direction'],
            launch_speed=data['launch_speed'],
            unknown_0xc440842b=data['unknown_0xc440842b'],
            unknown_0x9bb1543f=data['unknown_0x9bb1543f'],
            target_reorientation_time=data['target_reorientation_time'],
            render_texture_set=data['render_texture_set'],
            unknown_0x97ad5bee=data['unknown_0x97ad5bee'],
            unknown_0x094b5ad6=data['unknown_0x094b5ad6'],
            unknown_0x25967162=data['unknown_0x25967162'],
            unknown_0x26b5fcdf=data['unknown_0x26b5fcdf'],
            allow_air_control=data['allow_air_control'],
            unknown_0x36051905=data['unknown_0x36051905'],
            unknown_0xfc4118dd=data['unknown_0xfc4118dd'],
            unknown_0x06d1b8c7=data['unknown_0x06d1b8c7'],
            unknown_0x341f63f8=data['unknown_0x341f63f8'],
            unknown_0x4d6847e5=data['unknown_0x4d6847e5'],
            unknown_0x2255a13d=data['unknown_0x2255a13d'],
            barrel_cannon_enum_0x98501823=enums.BarrelCannonEnum.from_json(data['barrel_cannon_enum_0x98501823']),
            barrel_cannon_enum_0x098ecab6=enums.BarrelCannonEnum.from_json(data['barrel_cannon_enum_0x098ecab6']),
        )

    def to_json(self) -> dict:
        return {
            'grab_radius': self.grab_radius,
            'release_radius': self.release_radius,
            'ignore_gravity_radius': self.ignore_gravity_radius,
            'unknown_0x49d8e65a': self.unknown_0x49d8e65a,
            'launch_behavior': self.launch_behavior,
            'launch_timer': self.launch_timer,
            'launch_direction': self.launch_direction,
            'launch_speed': self.launch_speed,
            'unknown_0xc440842b': self.unknown_0xc440842b,
            'unknown_0x9bb1543f': self.unknown_0x9bb1543f,
            'target_reorientation_time': self.target_reorientation_time,
            'render_texture_set': self.render_texture_set,
            'unknown_0x97ad5bee': self.unknown_0x97ad5bee,
            'unknown_0x094b5ad6': self.unknown_0x094b5ad6,
            'unknown_0x25967162': self.unknown_0x25967162,
            'unknown_0x26b5fcdf': self.unknown_0x26b5fcdf,
            'allow_air_control': self.allow_air_control,
            'unknown_0x36051905': self.unknown_0x36051905,
            'unknown_0xfc4118dd': self.unknown_0xfc4118dd,
            'unknown_0x06d1b8c7': self.unknown_0x06d1b8c7,
            'unknown_0x341f63f8': self.unknown_0x341f63f8,
            'unknown_0x4d6847e5': self.unknown_0x4d6847e5,
            'unknown_0x2255a13d': self.unknown_0x2255a13d,
            'barrel_cannon_enum_0x98501823': self.barrel_cannon_enum_0x98501823.to_json(),
            'barrel_cannon_enum_0x098ecab6': self.barrel_cannon_enum_0x098ecab6.to_json(),
        }


_FAST_FORMAT = None
_FAST_IDS = (0x89664723, 0x2b2f4519, 0xfb35a95a, 0x49d8e65a, 0x2d2a4ad6, 0xd5ed0f77, 0x89d7791e, 0x31381a17, 0xc440842b, 0x9bb1543f, 0x61321ae, 0x32fab97e, 0x97ad5bee, 0x94b5ad6, 0x25967162, 0x26b5fcdf, 0x6c2ad8b4, 0x36051905, 0xfc4118dd, 0x6d1b8c7, 0x341f63f8, 0x4d6847e5, 0x2255a13d, 0x98501823, 0x98ecab6)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[BarrelCannonData]:
    if property_count != 25:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLH?LHLLHfLHLLHfLHfLHfLHfLHlLH?LH?LH?LH?LH?LH?LH?LH?LH?LH?LH?LHLLHL')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(214))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33], dec[36], dec[39], dec[42], dec[45], dec[48], dec[51], dec[54], dec[57], dec[60], dec[63], dec[66], dec[69], dec[72]) != _FAST_IDS:
        data.seek(before)
        return None

    return BarrelCannonData(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
        dec[26],
        dec[29],
        dec[32],
        dec[35],
        dec[38],
        dec[41],
        dec[44],
        dec[47],
        dec[50],
        dec[53],
        dec[56],
        dec[59],
        dec[62],
        dec[65],
        dec[68],
        enums.BarrelCannonEnum(dec[71]),
        enums.BarrelCannonEnum(dec[74]),
    )


def _decode_grab_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_release_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ignore_gravity_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x49d8e65a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_launch_behavior(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_launch_timer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_launch_direction(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_launch_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc440842b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9bb1543f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_target_reorientation_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_render_texture_set(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x97ad5bee(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x094b5ad6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x25967162(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x26b5fcdf(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_air_control(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x36051905(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xfc4118dd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x06d1b8c7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x341f63f8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x4d6847e5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x2255a13d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_barrel_cannon_enum_0x98501823(data: typing.BinaryIO, property_size: int):
    return enums.BarrelCannonEnum.from_stream(data)


def _decode_barrel_cannon_enum_0x098ecab6(data: typing.BinaryIO, property_size: int):
    return enums.BarrelCannonEnum.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x89664723: ('grab_radius', _decode_grab_radius),
    0x2b2f4519: ('release_radius', _decode_release_radius),
    0xfb35a95a: ('ignore_gravity_radius', _decode_ignore_gravity_radius),
    0x49d8e65a: ('unknown_0x49d8e65a', _decode_unknown_0x49d8e65a),
    0x2d2a4ad6: ('launch_behavior', _decode_launch_behavior),
    0xd5ed0f77: ('launch_timer', _decode_launch_timer),
    0x89d7791e: ('launch_direction', _decode_launch_direction),
    0x31381a17: ('launch_speed', _decode_launch_speed),
    0xc440842b: ('unknown_0xc440842b', _decode_unknown_0xc440842b),
    0x9bb1543f: ('unknown_0x9bb1543f', _decode_unknown_0x9bb1543f),
    0x61321ae: ('target_reorientation_time', _decode_target_reorientation_time),
    0x32fab97e: ('render_texture_set', _decode_render_texture_set),
    0x97ad5bee: ('unknown_0x97ad5bee', _decode_unknown_0x97ad5bee),
    0x94b5ad6: ('unknown_0x094b5ad6', _decode_unknown_0x094b5ad6),
    0x25967162: ('unknown_0x25967162', _decode_unknown_0x25967162),
    0x26b5fcdf: ('unknown_0x26b5fcdf', _decode_unknown_0x26b5fcdf),
    0x6c2ad8b4: ('allow_air_control', _decode_allow_air_control),
    0x36051905: ('unknown_0x36051905', _decode_unknown_0x36051905),
    0xfc4118dd: ('unknown_0xfc4118dd', _decode_unknown_0xfc4118dd),
    0x6d1b8c7: ('unknown_0x06d1b8c7', _decode_unknown_0x06d1b8c7),
    0x341f63f8: ('unknown_0x341f63f8', _decode_unknown_0x341f63f8),
    0x4d6847e5: ('unknown_0x4d6847e5', _decode_unknown_0x4d6847e5),
    0x2255a13d: ('unknown_0x2255a13d', _decode_unknown_0x2255a13d),
    0x98501823: ('barrel_cannon_enum_0x98501823', _decode_barrel_cannon_enum_0x98501823),
    0x98ecab6: ('barrel_cannon_enum_0x098ecab6', _decode_barrel_cannon_enum_0x098ecab6),
}
