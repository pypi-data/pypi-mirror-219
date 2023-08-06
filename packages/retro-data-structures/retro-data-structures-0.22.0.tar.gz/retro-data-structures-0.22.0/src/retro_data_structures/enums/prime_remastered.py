"""
Generated file.
"""
import enum
import typing
import struct


class MemoType(enum.IntEnum):
    StatusMessage = 0
    MessageBox = 1

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack("<L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack("<L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class PlayerItem(enum.IntEnum):
    PowerBeam = 0
    IceBeam = 1
    WaveBeam = 2
    PlasmaBeam = 3
    Missile = 4
    ScanVisor = 5
    MorphBallBomb = 6
    PowerBomb = 7
    Flamethrower = 8
    ThermalVisor = 9
    ChargeBeam = 10
    SuperMissile = 11
    GrappleBeam = 12
    XRayVisor = 13
    IceSpreader = 14
    SpaceJumpBoots = 15
    MorphBall = 16
    CombatVisor = 17
    BoostBall = 18
    SpiderBall = 19
    PowerSuit = 20
    GravitySuit = 21
    VariaSuit = 22
    PhazonSuit = 23
    EnergyTank = 24
    UnknownItem1 = 25
    HealthRefill = 26
    UnknownItem2 = 27
    Wavebuster = 28
    ArtifactofTruth = 29
    ArtifactofStrength = 30
    ArtifactofElder = 31
    ArtifactofWild = 32
    ArtifactofLifegiver = 33
    ArtifactofWarrior = 34
    ArtifactofChozo = 35
    ArtifactofNature = 36
    ArtifactofSun = 37
    ArtifactofWorld = 38
    ArtifactofSpirit = 39
    ArtifactofNewborn = 40

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack("<L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack("<L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class VisorFlags(enum.IntFlag):
    Combat = 1
    Scan = 2
    Thermal = 4
    XRay = 8

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack("<L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack("<L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value
