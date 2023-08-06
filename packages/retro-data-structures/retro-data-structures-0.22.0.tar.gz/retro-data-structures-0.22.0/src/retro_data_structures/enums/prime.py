"""
Generated file.
"""
import enum
import typing
import struct


class State(enum.IntEnum):
    Active = 0x0
    Arrived = 0x1
    Closed = 0x2
    Entered = 0x3
    Exited = 0x4
    Inactive = 0x5
    Inside = 0x6
    MaxReached = 0x7
    Open = 0x8
    Zero = 0x9
    Attack = 0xA
    UnknownState1 = 0xB
    Retreat = 0xC
    Patrol = 0xD
    Dead = 0xE
    CameraPath = 0xF
    CameraTarget = 0x10
    UnknownState2 = 0x11
    Play = 0x12
    UnknownState3 = 0x13
    DeathRattle = 0x14
    UnknownState4 = 0x15
    Damage = 0x16
    UnknownState5 = 0x17
    UnknownState6 = 0x18
    Modify = 0x19
    ScanDone = 0x1C
    DFST = 0x1E
    ReflectedDamage = 0x1F
    InheritBounds = 0x20

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class Message(enum.IntEnum):
    Activate = 0x1
    UnknownMessage1 = 0x2
    Close = 0x3
    Deactivate = 0x4
    Decrement = 0x5
    Follow = 0x6
    Increment = 0x7
    Next = 0x8
    Open = 0x9
    Reset = 0xA
    ResetAndStart = 0xB
    SetToMax = 0xC
    SetToZero = 0xD
    Start = 0xE
    Stop = 0xF
    StopAndReset = 0x10
    ToggleActive = 0x11
    UnknownMessage2 = 0x12
    Action = 0x13
    Play = 0x14
    Alert = 0x15

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class TriggerFlags(enum.IntFlag):
    DetectPlayer = 1
    DetectAI = 2
    DetectProjectiles = 1024
    DetectBombs = 64
    Unknown1 = 128
    KillOnEntered = 2048
    DetectMorphedPlayer = 4096
    ApplyForce = 8192
    DetectPlayerIfCompletelyInside = 16384
    Unknown2 = 32768
    DetectUnmorphedPlayer = 65536
    BlockEnvironmentalEffects = 131072

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class MemoType(enum.IntEnum):
    StatusMessage = 0
    MessageBox = 1

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class RenderSide(enum.IntEnum):
    _None = 0
    North = 1
    South = 2
    West = 4
    East = 8
    Top = 16
    Bottom = 32

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class Flags(enum.IntFlag):
    PendingAmbush = 1
    CeilingAmbush = 2
    NonAggressive = 4
    Melee = 8
    NoShuffleCloseCheck = 16
    OnlyAttackInRange = 32
    Unknown = 64
    NoKnockbackImpulseReset = 128
    NoMeleeAttack = 512
    BreakAttack = 1024
    Seated = 4096
    ShadowPirate = 8192
    AlertBeforeCloak = 16384
    NoBreakDamage = 32768
    FloatingCorpse = 65536
    RagdollNoAiCollision = 131072
    Trooper = 262144

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class Function(enum.IntEnum):
    Function0 = 0
    PlayerFollowLocator = 1
    SpinnerController = 2
    ObjectFollowLocator = 3
    Function4 = 4
    InventoryActivator = 5
    MapStation = 6
    SaveStation = 7
    IntroBossRingController = 8
    ViewFrustumTesterUnused = 9
    ShotSpinnerController = 10
    EscapeSequence = 11
    BossEnergyBar = 12
    EndGame = 13
    HUDFadeIn = 14
    CinematicSkip = 15
    ScriptLayerController = 16
    RainSimulator = 17
    AreaDamage = 18
    ObjectFollowObjectUnused = 19
    RedundantHintSystem = 20
    DropBomb = 21
    Function22 = 22
    MissileStation = 23
    Billboard = 24
    PlayerInAreaRelay = 25
    HUDTarget = 26
    FogFader = 27
    EnterLogbookScreen = 28
    PowerBombStation = 29
    Ending = 30
    FusionRelay = 31
    WeaponSwitchPALonly = 32

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class EnvironmentalEffect(enum.IntEnum):
    _None = 0
    Snow = 1
    Rain = 2
    Bubbles = 3

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class PhazonType(enum.IntEnum):
    _None = 0
    Blue = 1
    Orange = 2

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class ControllerMapping(enum.IntEnum):
    _None = 0
    LeftStickUp = 1
    LeftStickDown = 2
    LeftStickLeft = 3
    LeftStickRight = 4
    RightStickUp = 5
    RightStickDown = 6
    RightStickLeft = 7
    RightStickRight = 8
    LeftTrigger = 9
    RightTrigger = 10
    DPadUp = 11
    DPadDown = 12
    DPadLeft = 13
    DPadRight = 14
    AButton = 15
    BButton = 16
    XButton = 17
    YButton = 18
    ZButton = 19
    LeftTriggerPress = 20
    RightTriggerPress = 21
    Start = 22

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class HelmetVisMode(enum.IntEnum):
    ReducedUpdate = 0
    NotVisible = 1
    Deco = 2
    HelmetDeco = 3
    GlowHelmetDeco = 4
    HelmetOnly = 5

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class HudVisMode(enum.IntEnum):
    One = 0
    Two = 1
    Three = 2
    Four = 3

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class WorldLightingOptions(enum.IntEnum):
    Unknown1 = 0
    NormalWorldLighting = 1
    Unknown2 = 2
    DisableWorldLighting = 3
    Unknown3 = 4
    Unknown4 = 5

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class LightRecalculationOptions(enum.IntEnum):
    Never = 0
    _8Frames = 1
    _4Frames = 2
    EveryFrame = 3

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class LogbookCategory(enum.IntEnum):
    _None = 0
    SpacePirateData = 1
    ChozoLore = 2
    Creatures = 3
    Research = 4
    Artifacts = 5

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class PlayerAction(enum.IntEnum):
    Forward = 0
    Backward = 1
    TurnLeft = 2
    TurnRight = 3
    StrafeLeft = 4
    StrafeRight = 5
    LookLeft = 6
    LookRight = 7
    LookUp = 8
    LookDown = 9
    JumpBoost = 10
    FireBomb = 11
    MissilePowerBomb = 12
    Morph = 13
    AimUp = 14
    AimDown = 15
    CycleBeamUp = 16
    CycleBeamDown = 17
    CycleItem = 18
    PowerBeam = 19
    IceBeam = 20
    WaveBeam = 21
    PlasmaBeam = 22
    ToggleHolster = 23
    OrbitClose = 24
    OrbitFar = 25
    OrbitObject = 26
    OrbitSelect = 27
    OrbitConfirm = 28
    OrbitLeft = 29
    OrbitRight = 30
    OrbitUp = 31
    OrbitDown = 32
    LookHold1 = 33
    LookHold2 = 34
    LookZoomIn = 35
    LookZoomOut = 36
    AimHold = 37
    MapCircleUp = 38
    MapCircleDown = 39
    MapCircleLeft = 40
    MapCircleRight = 41
    MapMoveForward = 42
    MapMoveBack = 43
    MapMoveLeft = 44
    MapMoveRight = 45
    MapZoomIn = 46
    MapZoomOut = 47
    SpiderBall = 48
    ChaseCamera = 49
    XRayVisor = 50
    ThermoVisor = 51
    EnviroVisor = 52
    NoVisor = 53
    VisorMenu = 54
    VisorUp = 55
    VisorDown = 56
    UNKNOWN = 66
    UseShield = 59
    ScanItem = 60

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

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
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class ScanImagePane(enum.IntEnum):
    Pane0 = 0
    Pane1 = 1
    Pane2 = 2
    Pane3 = 3
    Pane01 = 4
    Pane12 = 5
    Pane23 = 6
    Pane012 = 7
    Pane123 = 8
    Pane0123 = 9
    Pane4 = 10
    Pane5 = 11
    Pane6 = 12
    Pane7 = 13
    Pane45 = 14
    Pane56 = 15
    Pane67 = 16
    Pane456 = 17
    Pane567 = 18
    Pane4567 = 19
    _None = 4294967295

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class ScanSpeed(enum.IntEnum):
    Normal = 0
    Slow = 1

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

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
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class VulnerabilityType(enum.IntEnum):
    DoubleDamage = 0
    Normal = 1
    Reflect = 2
    Immune = 3
    PassThrough = 4
    DirectDouble = 5
    DirectNormal = 6
    DirectImmune = 7

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class WeaponType(enum.IntEnum):
    Power = 0
    Ice = 1
    Wave = 2
    Plasma = 3
    Bomb = 4
    PowerBomb = 5
    Missile = 6
    BoostBall = 7
    Phazon = 8
    AI = 9
    PoisonWater = 10
    Lava = 11
    Hot = 12
    UnusedWeapon1 = 13
    UnusedWeapon2 = 14

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value
