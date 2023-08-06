# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.RevolutionControl import RevolutionControl


@dataclasses.dataclass()
class PlayerMiscControls(BaseProperty):
    item_menu: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    use_item: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    combat_visor: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    scan_visor: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    x_ray_visor: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    command_visor: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x12a3619e: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x33e1a595: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    scan_to_combat_visor: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    orbit_lock: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    grapple_lock: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    grapple_pull: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    grapple_release: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    grapple_give: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    grapple_receive: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    summon_ship: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    ship_fire: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    scan_item: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    scan_item_exit: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0xf3a2fbdd: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x30d313eb: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x79dc49ca: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0xefd76f97: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0xe6366106: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    struggle: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)

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

        data.write(b'\xdd\xf8\x8c\x92')  # 0xddf88c92
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.item_menu.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8b\x0ed\xf6')  # 0x8b0e64f6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.use_item.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd4\x9e_\xcf')  # 0xd49e5fcf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.combat_visor.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9c\x18&\x89')  # 0x9c182689
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scan_visor.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x01\x1f\x01\x93')  # 0x11f0193
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.x_ray_visor.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbbV\n\xd3')  # 0xbb560ad3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.command_visor.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x12\xa3a\x9e')  # 0x12a3619e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x12a3619e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'3\xe1\xa5\x95')  # 0x33e1a595
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x33e1a595.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xab\xfa\xa1\xfa')  # 0xabfaa1fa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scan_to_combat_visor.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'#q{\x97')  # 0x23717b97
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.orbit_lock.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0eY\xd6"')  # 0xe59d622
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.grapple_lock.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'g\xd4^\xb2')  # 0x67d45eb2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.grapple_pull.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb4\xa6c5')  # 0xb4a66335
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.grapple_release.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe0sd[')  # 0xe073645b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.grapple_give.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcbm }')  # 0xcb6d207d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.grapple_receive.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'~\xe3\xac\xdf')  # 0x7ee3acdf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.summon_ship.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf6\xc8{\xf5')  # 0xf6c87bf5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ship_fire.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'J\x88\xa7o')  # 0x4a88a76f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scan_item.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb4;$w')  # 0xb43b2477
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scan_item_exit.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf3\xa2\xfb\xdd')  # 0xf3a2fbdd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xf3a2fbdd.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'0\xd3\x13\xeb')  # 0x30d313eb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x30d313eb.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'y\xdcI\xca')  # 0x79dc49ca
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x79dc49ca.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xef\xd7o\x97')  # 0xefd76f97
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xefd76f97.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe66a\x06')  # 0xe6366106
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xe6366106.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x98\xdam\x03')  # 0x98da6d03
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.struggle.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            item_menu=RevolutionControl.from_json(data['item_menu']),
            use_item=RevolutionControl.from_json(data['use_item']),
            combat_visor=RevolutionControl.from_json(data['combat_visor']),
            scan_visor=RevolutionControl.from_json(data['scan_visor']),
            x_ray_visor=RevolutionControl.from_json(data['x_ray_visor']),
            command_visor=RevolutionControl.from_json(data['command_visor']),
            unknown_0x12a3619e=RevolutionControl.from_json(data['unknown_0x12a3619e']),
            unknown_0x33e1a595=RevolutionControl.from_json(data['unknown_0x33e1a595']),
            scan_to_combat_visor=RevolutionControl.from_json(data['scan_to_combat_visor']),
            orbit_lock=RevolutionControl.from_json(data['orbit_lock']),
            grapple_lock=RevolutionControl.from_json(data['grapple_lock']),
            grapple_pull=RevolutionControl.from_json(data['grapple_pull']),
            grapple_release=RevolutionControl.from_json(data['grapple_release']),
            grapple_give=RevolutionControl.from_json(data['grapple_give']),
            grapple_receive=RevolutionControl.from_json(data['grapple_receive']),
            summon_ship=RevolutionControl.from_json(data['summon_ship']),
            ship_fire=RevolutionControl.from_json(data['ship_fire']),
            scan_item=RevolutionControl.from_json(data['scan_item']),
            scan_item_exit=RevolutionControl.from_json(data['scan_item_exit']),
            unknown_0xf3a2fbdd=RevolutionControl.from_json(data['unknown_0xf3a2fbdd']),
            unknown_0x30d313eb=RevolutionControl.from_json(data['unknown_0x30d313eb']),
            unknown_0x79dc49ca=RevolutionControl.from_json(data['unknown_0x79dc49ca']),
            unknown_0xefd76f97=RevolutionControl.from_json(data['unknown_0xefd76f97']),
            unknown_0xe6366106=RevolutionControl.from_json(data['unknown_0xe6366106']),
            struggle=RevolutionControl.from_json(data['struggle']),
        )

    def to_json(self) -> dict:
        return {
            'item_menu': self.item_menu.to_json(),
            'use_item': self.use_item.to_json(),
            'combat_visor': self.combat_visor.to_json(),
            'scan_visor': self.scan_visor.to_json(),
            'x_ray_visor': self.x_ray_visor.to_json(),
            'command_visor': self.command_visor.to_json(),
            'unknown_0x12a3619e': self.unknown_0x12a3619e.to_json(),
            'unknown_0x33e1a595': self.unknown_0x33e1a595.to_json(),
            'scan_to_combat_visor': self.scan_to_combat_visor.to_json(),
            'orbit_lock': self.orbit_lock.to_json(),
            'grapple_lock': self.grapple_lock.to_json(),
            'grapple_pull': self.grapple_pull.to_json(),
            'grapple_release': self.grapple_release.to_json(),
            'grapple_give': self.grapple_give.to_json(),
            'grapple_receive': self.grapple_receive.to_json(),
            'summon_ship': self.summon_ship.to_json(),
            'ship_fire': self.ship_fire.to_json(),
            'scan_item': self.scan_item.to_json(),
            'scan_item_exit': self.scan_item_exit.to_json(),
            'unknown_0xf3a2fbdd': self.unknown_0xf3a2fbdd.to_json(),
            'unknown_0x30d313eb': self.unknown_0x30d313eb.to_json(),
            'unknown_0x79dc49ca': self.unknown_0x79dc49ca.to_json(),
            'unknown_0xefd76f97': self.unknown_0xefd76f97.to_json(),
            'unknown_0xe6366106': self.unknown_0xe6366106.to_json(),
            'struggle': self.struggle.to_json(),
        }


def _decode_item_menu(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_use_item(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_combat_visor(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_scan_visor(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_x_ray_visor(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_command_visor(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x12a3619e(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x33e1a595(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_scan_to_combat_visor(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_orbit_lock(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_grapple_lock(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_grapple_pull(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_grapple_release(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_grapple_give(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_grapple_receive(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_summon_ship(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_ship_fire(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_scan_item(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_scan_item_exit(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0xf3a2fbdd(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x30d313eb(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x79dc49ca(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0xefd76f97(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0xe6366106(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_struggle(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xddf88c92: ('item_menu', _decode_item_menu),
    0x8b0e64f6: ('use_item', _decode_use_item),
    0xd49e5fcf: ('combat_visor', _decode_combat_visor),
    0x9c182689: ('scan_visor', _decode_scan_visor),
    0x11f0193: ('x_ray_visor', _decode_x_ray_visor),
    0xbb560ad3: ('command_visor', _decode_command_visor),
    0x12a3619e: ('unknown_0x12a3619e', _decode_unknown_0x12a3619e),
    0x33e1a595: ('unknown_0x33e1a595', _decode_unknown_0x33e1a595),
    0xabfaa1fa: ('scan_to_combat_visor', _decode_scan_to_combat_visor),
    0x23717b97: ('orbit_lock', _decode_orbit_lock),
    0xe59d622: ('grapple_lock', _decode_grapple_lock),
    0x67d45eb2: ('grapple_pull', _decode_grapple_pull),
    0xb4a66335: ('grapple_release', _decode_grapple_release),
    0xe073645b: ('grapple_give', _decode_grapple_give),
    0xcb6d207d: ('grapple_receive', _decode_grapple_receive),
    0x7ee3acdf: ('summon_ship', _decode_summon_ship),
    0xf6c87bf5: ('ship_fire', _decode_ship_fire),
    0x4a88a76f: ('scan_item', _decode_scan_item),
    0xb43b2477: ('scan_item_exit', _decode_scan_item_exit),
    0xf3a2fbdd: ('unknown_0xf3a2fbdd', _decode_unknown_0xf3a2fbdd),
    0x30d313eb: ('unknown_0x30d313eb', _decode_unknown_0x30d313eb),
    0x79dc49ca: ('unknown_0x79dc49ca', _decode_unknown_0x79dc49ca),
    0xefd76f97: ('unknown_0xefd76f97', _decode_unknown_0xefd76f97),
    0xe6366106: ('unknown_0xe6366106', _decode_unknown_0xe6366106),
    0x98da6d03: ('struggle', _decode_struggle),
}
