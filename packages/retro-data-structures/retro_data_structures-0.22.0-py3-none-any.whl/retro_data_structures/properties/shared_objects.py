# Generated File
import typing

import retro_data_structures.properties.corruption.objects as _corruption_objects
import retro_data_structures.properties.dkc_returns.objects as _dkc_returns_objects
import retro_data_structures.properties.echoes.objects as _echoes_objects
import retro_data_structures.properties.prime.objects as _prime_objects
import retro_data_structures.properties.prime_remastered.objects as _prime_remastered_objects

AIHint = typing.Union[
    _echoes_objects.AIHint,
    _corruption_objects.AIHint,
    _dkc_returns_objects.AIHint
]
AIJumpPoint = typing.Union[
    _prime_objects.AIJumpPoint,
    _echoes_objects.AIJumpPoint
]
AIKeyframe = typing.Union[
    _prime_objects.AIKeyframe,
    _echoes_objects.AIKeyframe,
    _corruption_objects.AIKeyframe,
    _dkc_returns_objects.AIKeyframe
]
AIWaypoint = typing.Union[
    _echoes_objects.AIWaypoint,
    _corruption_objects.AIWaypoint,
    _dkc_returns_objects.AIWaypoint
]
AVIS = typing.Union[
    _corruption_objects.AVIS,
    _dkc_returns_objects.AVIS
]
Actor = typing.Union[
    _prime_objects.Actor,
    _echoes_objects.Actor,
    _corruption_objects.Actor,
    _dkc_returns_objects.Actor
]
ActorKeyframe = typing.Union[
    _prime_objects.ActorKeyframe,
    _echoes_objects.ActorKeyframe,
    _corruption_objects.ActorKeyframe,
    _dkc_returns_objects.ActorKeyframe,
    _prime_remastered_objects.ActorKeyframe
]
ActorRotate = typing.Union[
    _prime_objects.ActorRotate,
    _echoes_objects.ActorRotate
]
ActorTransform = typing.Union[
    _corruption_objects.ActorTransform,
    _dkc_returns_objects.ActorTransform
]
AmbientAI = typing.Union[
    _prime_objects.AmbientAI,
    _echoes_objects.AmbientAI,
    _corruption_objects.AmbientAI
]
AreaAttributes = typing.Union[
    _prime_objects.AreaAttributes,
    _echoes_objects.AreaAttributes,
    _corruption_objects.AreaAttributes,
    _dkc_returns_objects.AreaAttributes
]
AreaDamage = typing.Union[
    _echoes_objects.AreaDamage,
    _corruption_objects.AreaDamage,
    _dkc_returns_objects.AreaDamage
]
AreaStreamedAudioState = typing.Union[
    _corruption_objects.AreaStreamedAudioState,
    _dkc_returns_objects.AreaStreamedAudioState
]
AtomicAlpha = typing.Union[
    _prime_objects.AtomicAlpha,
    _echoes_objects.AtomicAlpha,
    _corruption_objects.AtomicAlpha
]
AtomicBeta = typing.Union[
    _prime_objects.AtomicBeta,
    _echoes_objects.AtomicBeta
]
AudioOccluder = typing.Union[
    _corruption_objects.AudioOccluder,
    _dkc_returns_objects.AudioOccluder
]
BallTrigger = typing.Union[
    _prime_objects.BallTrigger,
    _echoes_objects.BallTrigger,
    _corruption_objects.BallTrigger
]
Beam = typing.Union[
    _corruption_objects.Beam,
    _prime_remastered_objects.Beam
]
BloomEffect = typing.Union[
    _dkc_returns_objects.BloomEffect,
    _prime_remastered_objects.BloomEffect
]
Cable = typing.Union[
    _corruption_objects.Cable,
    _dkc_returns_objects.Cable
]
Camera = typing.Union[
    _prime_objects.Camera,
    _echoes_objects.Camera
]
CameraBlurKeyframe = typing.Union[
    _prime_objects.CameraBlurKeyframe,
    _echoes_objects.CameraBlurKeyframe,
    _corruption_objects.CameraBlurKeyframe,
    _dkc_returns_objects.CameraBlurKeyframe
]
CameraFilterKeyframe = typing.Union[
    _prime_objects.CameraFilterKeyframe,
    _echoes_objects.CameraFilterKeyframe,
    _corruption_objects.CameraFilterKeyframe,
    _dkc_returns_objects.CameraFilterKeyframe
]
CameraHint = typing.Union[
    _prime_objects.CameraHint,
    _echoes_objects.CameraHint,
    _corruption_objects.CameraHint,
    _dkc_returns_objects.CameraHint,
    _prime_remastered_objects.CameraHint
]
CameraManager = typing.Union[
    _dkc_returns_objects.CameraManager,
    _prime_remastered_objects.CameraManager
]
CameraPitch = typing.Union[
    _echoes_objects.CameraPitch,
    _corruption_objects.CameraPitch
]
CameraShaker = typing.Union[
    _prime_objects.CameraShaker,
    _echoes_objects.CameraShaker,
    _corruption_objects.CameraShaker,
    _dkc_returns_objects.CameraShaker,
    _prime_remastered_objects.CameraShaker
]
CameraWaypoint = typing.Union[
    _prime_objects.CameraWaypoint,
    _echoes_objects.CameraWaypoint
]
CannonBall = typing.Union[
    _echoes_objects.CannonBall,
    _corruption_objects.CannonBall
]
Checkpoint = typing.Union[
    _dkc_returns_objects.Checkpoint,
    _prime_remastered_objects.Checkpoint
]
ChozoGhost = typing.Union[
    _prime_objects.ChozoGhost,
    _echoes_objects.ChozoGhost
]
CinematicCamera = typing.Union[
    _corruption_objects.CinematicCamera,
    _dkc_returns_objects.CinematicCamera
]
ColorModulate = typing.Union[
    _prime_objects.ColorModulate,
    _echoes_objects.ColorModulate,
    _corruption_objects.ColorModulate,
    _dkc_returns_objects.ColorModulate
]
ConditionalRelay = typing.Union[
    _echoes_objects.ConditionalRelay,
    _corruption_objects.ConditionalRelay,
    _dkc_returns_objects.ConditionalRelay
]
ControlHint = typing.Union[
    _echoes_objects.ControlHint,
    _corruption_objects.ControlHint
]
ControllerAction = typing.Union[
    _prime_objects.ControllerAction,
    _echoes_objects.ControllerAction,
    _corruption_objects.ControllerAction,
    _dkc_returns_objects.ControllerAction,
    _prime_remastered_objects.ControllerAction
]
Counter = typing.Union[
    _prime_objects.Counter,
    _echoes_objects.Counter,
    _corruption_objects.Counter,
    _dkc_returns_objects.Counter,
    _prime_remastered_objects.Counter
]
CoverPoint = typing.Union[
    _prime_objects.CoverPoint,
    _echoes_objects.CoverPoint,
    _corruption_objects.CoverPoint,
    _prime_remastered_objects.CoverPoint
]
CustomInterpolation = typing.Union[
    _dkc_returns_objects.CustomInterpolation,
    _prime_remastered_objects.CustomInterpolation
]
DamageActor = typing.Union[
    _echoes_objects.DamageActor,
    _corruption_objects.DamageActor
]
DamageableTrigger = typing.Union[
    _prime_objects.DamageableTrigger,
    _echoes_objects.DamageableTrigger,
    _corruption_objects.DamageableTrigger,
    _dkc_returns_objects.DamageableTrigger
]
DamageableTriggerOrientated = typing.Union[
    _echoes_objects.DamageableTriggerOrientated,
    _corruption_objects.DamageableTriggerOrientated,
    _dkc_returns_objects.DamageableTriggerOrientated
]
DarkSamus = typing.Union[
    _echoes_objects.DarkSamus,
    _corruption_objects.DarkSamus
]
Debris = typing.Union[
    _prime_objects.Debris,
    _echoes_objects.Debris,
    _corruption_objects.Debris,
    _dkc_returns_objects.Debris
]
DebrisExtended = typing.Union[
    _prime_objects.DebrisExtended,
    _echoes_objects.DebrisExtended
]
DistanceFog = typing.Union[
    _prime_objects.DistanceFog,
    _echoes_objects.DistanceFog,
    _corruption_objects.DistanceFog,
    _dkc_returns_objects.DistanceFog
]
Dock = typing.Union[
    _prime_objects.Dock,
    _echoes_objects.Dock,
    _corruption_objects.Dock,
    _prime_remastered_objects.Dock
]
Door = typing.Union[
    _prime_objects.Door,
    _echoes_objects.Door,
    _corruption_objects.Door
]
DynamicLight = typing.Union[
    _echoes_objects.DynamicLight,
    _corruption_objects.DynamicLight,
    _dkc_returns_objects.DynamicLight
]
Effect = typing.Union[
    _prime_objects.Effect,
    _echoes_objects.Effect,
    _corruption_objects.Effect,
    _dkc_returns_objects.Effect,
    _prime_remastered_objects.Effect
]
ElectroMagneticPulse = typing.Union[
    _prime_objects.ElectroMagneticPulse,
    _corruption_objects.ElectroMagneticPulse
]
ElitePirate = typing.Union[
    _prime_objects.ElitePirate,
    _echoes_objects.ElitePirate
]
EnvFxDensityController = typing.Union[
    _prime_objects.EnvFxDensityController,
    _echoes_objects.EnvFxDensityController,
    _corruption_objects.EnvFxDensityController,
    _dkc_returns_objects.EnvFxDensityController
]
FalsePerspective = typing.Union[
    _corruption_objects.FalsePerspective,
    _dkc_returns_objects.FalsePerspective
]
FishCloud = typing.Union[
    _prime_objects.FishCloud,
    _echoes_objects.FishCloud,
    _corruption_objects.FishCloud
]
FishCloudModifier = typing.Union[
    _prime_objects.FishCloudModifier,
    _echoes_objects.FishCloudModifier,
    _corruption_objects.FishCloudModifier
]
FlyerSwarm = typing.Union[
    _echoes_objects.FlyerSwarm,
    _corruption_objects.FlyerSwarm
]
FlyingPirate = typing.Union[
    _prime_objects.FlyingPirate,
    _echoes_objects.FlyingPirate,
    _corruption_objects.FlyingPirate
]
FogOverlay = typing.Union[
    _echoes_objects.FogOverlay,
    _corruption_objects.FogOverlay,
    _dkc_returns_objects.FogOverlay
]
FogVolume = typing.Union[
    _prime_objects.FogVolume,
    _echoes_objects.FogVolume,
    _corruption_objects.FogVolume,
    _dkc_returns_objects.FogVolume,
    _prime_remastered_objects.FogVolume
]
GeneratedObjectDeleter = typing.Union[
    _corruption_objects.GeneratedObjectDeleter,
    _dkc_returns_objects.GeneratedObjectDeleter
]
Generator = typing.Union[
    _prime_objects.Generator,
    _echoes_objects.Generator,
    _corruption_objects.Generator,
    _dkc_returns_objects.Generator,
    _prime_remastered_objects.Generator
]
GrapplePoint = typing.Union[
    _prime_objects.GrapplePoint,
    _echoes_objects.GrapplePoint,
    _corruption_objects.GrapplePoint
]
GuiMenu = typing.Union[
    _echoes_objects.GuiMenu,
    _corruption_objects.GuiMenu,
    _dkc_returns_objects.GuiMenu
]
GuiScreen = typing.Union[
    _echoes_objects.GuiScreen,
    _corruption_objects.GuiScreen
]
GuiSlider = typing.Union[
    _echoes_objects.GuiSlider,
    _corruption_objects.GuiSlider,
    _dkc_returns_objects.GuiSlider
]
GuiWidget = typing.Union[
    _echoes_objects.GuiWidget,
    _corruption_objects.GuiWidget,
    _dkc_returns_objects.GuiWidget
]
GunTurretBase = typing.Union[
    _echoes_objects.GunTurretBase,
    _corruption_objects.GunTurretBase
]
GunTurretTop = typing.Union[
    _echoes_objects.GunTurretTop,
    _corruption_objects.GunTurretTop
]
HUDHint = typing.Union[
    _echoes_objects.HUDHint,
    _corruption_objects.HUDHint
]
HUDMemo = typing.Union[
    _prime_objects.HUDMemo,
    _echoes_objects.HUDMemo,
    _corruption_objects.HUDMemo
]
LODController = typing.Union[
    _corruption_objects.LODController,
    _dkc_returns_objects.LODController
]
LevelDarkener = typing.Union[
    _dkc_returns_objects.LevelDarkener,
    _prime_remastered_objects.LevelDarkener
]
LightVolume = typing.Union[
    _corruption_objects.LightVolume,
    _dkc_returns_objects.LightVolume
]
MemoryRelay = typing.Union[
    _prime_objects.MemoryRelay,
    _echoes_objects.MemoryRelay,
    _corruption_objects.MemoryRelay,
    _dkc_returns_objects.MemoryRelay
]
Metaree = typing.Union[
    _echoes_objects.Metaree,
    _corruption_objects.Metaree
]
MetroidAlpha = typing.Union[
    _prime_objects.MetroidAlpha,
    _echoes_objects.MetroidAlpha
]
Midi = typing.Union[
    _prime_objects.Midi,
    _echoes_objects.Midi
]
MinorIng = typing.Union[
    _echoes_objects.MinorIng,
    _corruption_objects.MinorIng
]
MultiModelActor = typing.Union[
    _corruption_objects.MultiModelActor,
    _dkc_returns_objects.MultiModelActor
]
MysteryFlyer = typing.Union[
    _echoes_objects.MysteryFlyer,
    _corruption_objects.MysteryFlyer
]
OptionalAreaAsset = typing.Union[
    _corruption_objects.OptionalAreaAsset,
    _dkc_returns_objects.OptionalAreaAsset
]
Parasite = typing.Union[
    _prime_objects.Parasite,
    _echoes_objects.Parasite,
    _corruption_objects.Parasite
]
PathCamera = typing.Union[
    _prime_objects.PathCamera,
    _echoes_objects.PathCamera
]
PathControl = typing.Union[
    _corruption_objects.PathControl,
    _dkc_returns_objects.PathControl,
    _prime_remastered_objects.PathControl
]
PathMeshCtrl = typing.Union[
    _echoes_objects.PathMeshCtrl,
    _corruption_objects.PathMeshCtrl
]
Pickup = typing.Union[
    _prime_objects.Pickup,
    _echoes_objects.Pickup,
    _corruption_objects.Pickup,
    _dkc_returns_objects.Pickup,
    _prime_remastered_objects.Pickup
]
PickupGenerator = typing.Union[
    _prime_objects.PickupGenerator,
    _echoes_objects.PickupGenerator
]
PillBug = typing.Union[
    _echoes_objects.PillBug,
    _corruption_objects.PillBug
]
PlantScarabSwarm = typing.Union[
    _echoes_objects.PlantScarabSwarm,
    _corruption_objects.PlantScarabSwarm
]
Platform = typing.Union[
    _prime_objects.Platform,
    _echoes_objects.Platform,
    _corruption_objects.Platform,
    _dkc_returns_objects.Platform
]
PlayerActor = typing.Union[
    _prime_objects.PlayerActor,
    _echoes_objects.PlayerActor,
    _corruption_objects.PlayerActor,
    _dkc_returns_objects.PlayerActor,
    _prime_remastered_objects.PlayerActor
]
PlayerHint = typing.Union[
    _prime_objects.PlayerHint,
    _echoes_objects.PlayerHint,
    _corruption_objects.PlayerHint
]
PlayerRespawn = typing.Union[
    _dkc_returns_objects.PlayerRespawn,
    _prime_remastered_objects.PlayerRespawn
]
PlayerStateChange = typing.Union[
    _prime_objects.PlayerStateChange,
    _echoes_objects.PlayerStateChange
]
PoiObject = typing.Union[
    _dkc_returns_objects.PoiObject,
    _prime_remastered_objects.PoiObject
]
PointOfInterest = typing.Union[
    _prime_objects.PointOfInterest,
    _echoes_objects.PointOfInterest,
    _corruption_objects.PointOfInterest,
    _prime_remastered_objects.PointOfInterest
]
PositionRelay = typing.Union[
    _corruption_objects.PositionRelay,
    _dkc_returns_objects.PositionRelay
]
Projectile = typing.Union[
    _dkc_returns_objects.Projectile,
    _prime_remastered_objects.Projectile
]
PuddleSpore = typing.Union[
    _prime_objects.PuddleSpore,
    _echoes_objects.PuddleSpore
]
Puffer = typing.Union[
    _prime_objects.Puffer,
    _echoes_objects.Puffer,
    _corruption_objects.Puffer
]
RadialDamage = typing.Union[
    _prime_objects.RadialDamage,
    _echoes_objects.RadialDamage,
    _corruption_objects.RadialDamage,
    _dkc_returns_objects.RadialDamage
]
RandomRelay = typing.Union[
    _prime_objects.RandomRelay,
    _echoes_objects.RandomRelay,
    _corruption_objects.RandomRelay
]
Relay = typing.Union[
    _prime_objects.Relay,
    _echoes_objects.Relay,
    _corruption_objects.Relay,
    _dkc_returns_objects.Relay,
    _prime_remastered_objects.Relay
]
RelayRandom = typing.Union[
    _dkc_returns_objects.RelayRandom,
    _prime_remastered_objects.RelayRandom
]
Repulsor = typing.Union[
    _prime_objects.Repulsor,
    _echoes_objects.Repulsor,
    _corruption_objects.Repulsor
]
Retronome = typing.Union[
    _dkc_returns_objects.Retronome,
    _prime_remastered_objects.Retronome
]
Ripper = typing.Union[
    _prime_objects.Ripper,
    _echoes_objects.Ripper
]
Ripple = typing.Union[
    _prime_objects.Ripple,
    _echoes_objects.Ripple,
    _corruption_objects.Ripple
]
RoomAcoustics = typing.Union[
    _prime_objects.RoomAcoustics,
    _echoes_objects.RoomAcoustics,
    _corruption_objects.RoomAcoustics
]
RumbleEffect = typing.Union[
    _prime_objects.RumbleEffect,
    _echoes_objects.RumbleEffect,
    _corruption_objects.RumbleEffect,
    _dkc_returns_objects.RumbleEffect
]
ScriptLayerController = typing.Union[
    _echoes_objects.ScriptLayerController,
    _corruption_objects.ScriptLayerController,
    _dkc_returns_objects.ScriptLayerController
]
SequenceTimer = typing.Union[
    _echoes_objects.SequenceTimer,
    _corruption_objects.SequenceTimer,
    _dkc_returns_objects.SequenceTimer
]
ShadowProjector = typing.Union[
    _prime_objects.ShadowProjector,
    _echoes_objects.ShadowProjector,
    _corruption_objects.ShadowProjector,
    _dkc_returns_objects.ShadowProjector
]
SkyRipple = typing.Union[
    _echoes_objects.SkyRipple,
    _corruption_objects.SkyRipple
]
SkyboxModInca = typing.Union[
    _corruption_objects.SkyboxModInca,
    _dkc_returns_objects.SkyboxModInca
]
SnakeWeedSwarm = typing.Union[
    _prime_objects.SnakeWeedSwarm,
    _echoes_objects.SnakeWeedSwarm
]
Sound = typing.Union[
    _prime_objects.Sound,
    _echoes_objects.Sound,
    _corruption_objects.Sound,
    _dkc_returns_objects.Sound,
    _prime_remastered_objects.Sound
]
SoundModifier = typing.Union[
    _echoes_objects.SoundModifier,
    _corruption_objects.SoundModifier,
    _dkc_returns_objects.SoundModifier
]
SpacePirate = typing.Union[
    _prime_objects.SpacePirate,
    _echoes_objects.SpacePirate,
    _corruption_objects.SpacePirate
]
SpankWeed = typing.Union[
    _prime_objects.SpankWeed,
    _echoes_objects.SpankWeed
]
SpawnPoint = typing.Union[
    _prime_objects.SpawnPoint,
    _echoes_objects.SpawnPoint,
    _corruption_objects.SpawnPoint,
    _dkc_returns_objects.SpawnPoint,
    _prime_remastered_objects.SpawnPoint
]
SpecialFunction = typing.Union[
    _prime_objects.SpecialFunction,
    _echoes_objects.SpecialFunction,
    _corruption_objects.SpecialFunction,
    _dkc_returns_objects.SpecialFunction
]
SpiderBallAttractionSurface = typing.Union[
    _prime_objects.SpiderBallAttractionSurface,
    _echoes_objects.SpiderBallAttractionSurface,
    _corruption_objects.SpiderBallAttractionSurface
]
SpiderBallWaypoint = typing.Union[
    _prime_objects.SpiderBallWaypoint,
    _echoes_objects.SpiderBallWaypoint,
    _corruption_objects.SpiderBallWaypoint
]
SpindleCamera = typing.Union[
    _prime_objects.SpindleCamera,
    _echoes_objects.SpindleCamera
]
Spinner = typing.Union[
    _echoes_objects.Spinner,
    _corruption_objects.Spinner,
    _dkc_returns_objects.Spinner
]
Steam = typing.Union[
    _prime_objects.Steam,
    _echoes_objects.Steam,
    _corruption_objects.Steam
]
StreamedAudio = typing.Union[
    _prime_objects.StreamedAudio,
    _echoes_objects.StreamedAudio,
    _corruption_objects.StreamedAudio,
    _dkc_returns_objects.StreamedAudio
]
StreamedMovie = typing.Union[
    _echoes_objects.StreamedMovie,
    _corruption_objects.StreamedMovie,
    _dkc_returns_objects.StreamedMovie,
    _prime_remastered_objects.StreamedMovie
]
Subtitles = typing.Union[
    _corruption_objects.Subtitles,
    _dkc_returns_objects.Subtitles
]
SurfaceControl = typing.Union[
    _corruption_objects.SurfaceControl,
    _dkc_returns_objects.SurfaceControl,
    _prime_remastered_objects.SurfaceControl
]
Switch = typing.Union[
    _prime_objects.Switch,
    _echoes_objects.Switch,
    _corruption_objects.Switch,
    _dkc_returns_objects.Switch
]
TargetingPoint = typing.Union[
    _prime_objects.TargetingPoint,
    _echoes_objects.TargetingPoint,
    _corruption_objects.TargetingPoint
]
TeamAI = typing.Union[
    _echoes_objects.TeamAI,
    _corruption_objects.TeamAI
]
TextPane = typing.Union[
    _echoes_objects.TextPane,
    _corruption_objects.TextPane,
    _dkc_returns_objects.TextPane,
    _prime_remastered_objects.TextPane
]
TimeKeyframe = typing.Union[
    _echoes_objects.TimeKeyframe,
    _corruption_objects.TimeKeyframe,
    _dkc_returns_objects.TimeKeyframe,
    _prime_remastered_objects.TimeKeyframe
]
Timer = typing.Union[
    _prime_objects.Timer,
    _echoes_objects.Timer,
    _corruption_objects.Timer,
    _dkc_returns_objects.Timer,
    _prime_remastered_objects.Timer
]
Trigger = typing.Union[
    _prime_objects.Trigger,
    _echoes_objects.Trigger,
    _corruption_objects.Trigger,
    _dkc_returns_objects.Trigger
]
Tryclops = typing.Union[
    _prime_objects.Tryclops,
    _echoes_objects.Tryclops
]
VisorFlare = typing.Union[
    _prime_objects.VisorFlare,
    _echoes_objects.VisorFlare,
    _corruption_objects.VisorFlare
]
VisorGoo = typing.Union[
    _prime_objects.VisorGoo,
    _echoes_objects.VisorGoo,
    _corruption_objects.VisorGoo
]
WallCrawlerSwarm = typing.Union[
    _prime_objects.WallCrawlerSwarm,
    _corruption_objects.WallCrawlerSwarm
]
Water = typing.Union[
    _prime_objects.Water,
    _echoes_objects.Water,
    _corruption_objects.Water
]
Waypoint = typing.Union[
    _prime_objects.Waypoint,
    _echoes_objects.Waypoint,
    _corruption_objects.Waypoint,
    _dkc_returns_objects.Waypoint,
    _prime_remastered_objects.Waypoint
]
WorldAttributes = typing.Union[
    _corruption_objects.WorldAttributes,
    _dkc_returns_objects.WorldAttributes
]
WorldLightFader = typing.Union[
    _prime_objects.WorldLightFader,
    _echoes_objects.WorldLightFader,
    _corruption_objects.WorldLightFader,
    _dkc_returns_objects.WorldLightFader
]
WorldTeleporter = typing.Union[
    _prime_objects.WorldTeleporter,
    _echoes_objects.WorldTeleporter,
    _corruption_objects.WorldTeleporter
]
