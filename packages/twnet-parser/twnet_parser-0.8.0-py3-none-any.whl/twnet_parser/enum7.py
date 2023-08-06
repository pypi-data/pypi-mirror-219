# pylint: disable=duplicate-code
from enum import Enum

class Pickup(Enum):
    HEALTH: int = 0
    ARMOR: int = 1
    GRENADE: int = 2
    SHOTGUN: int = 3
    LASER: int = 4
    NINJA: int = 5
    GUN: int = 6
    HAMMER: int = 7

class Emote(Enum):
    NORMAL: int = 0
    PAIN: int = 1
    HAPPY: int = 2
    SURPRISE: int = 3
    ANGRY: int = 4
    BLINK: int = 5

class Emoticon(Enum):
    OOP: int = 0
    EXCLAMATION: int = 1
    HEARTS: int = 2
    DROP: int = 3
    DOTDOT: int = 4
    MUSIC: int = 5
    SORRY: int = 6
    GHOST: int = 7
    SUSHI: int = 8
    SPLATTEE: int = 9
    DEVILTEE: int = 10
    ZOMG: int = 11
    ZZZ: int = 12
    WTF: int = 13
    EYES: int = 14
    QUESTION: int = 15

class Vote(Enum):
    UNKNOWN: int = 0
    START_OP: int = 1
    START_KICK: int = 2
    START_SPEC: int = 3
    END_ABORT: int = 4
    END_PASS: int = 5
    END_FAIL: int = 6

class Chat(Enum):
    NONE: int = 0
    ALL: int = 1
    TEAM: int = 2
    WHISPER: int = 3

class Gamemsg(Enum):
    TEAM_SWAP: int = 0
    SPEC_INVALIDID: int = 1
    TEAM_SHUFFLE: int = 2
    TEAM_BALANCE: int = 3
    CTF_DROP: int = 4
    CTF_RETURN: int = 5
    TEAM_ALL: int = 6
    TEAM_BALANCE_VICTIM: int = 7
    CTF_GRAB: int = 8
    CTF_CAPTURE: int = 9
    GAME_PAUSED: int = 10

class Weapon(Enum):
    HAMMER: int = 0
    PISTOL: int = 1
    SHOTGUN: int = 2
    GRENADE: int = 3
    RIFLE: int = 4
    NINJA: int = 5

class Team(Enum):
    SPECTATORS: int = -1
    RED: int = 0
    BLUE: int = 1

class Sound(Enum):
    GUN_FIRE: int = 0
    SHOTGUN_FIRE: int = 1
    GRENADE_FIRE: int = 2
    HAMMER_FIRE: int = 3
    HAMMER_HIT: int = 4
    NINJA_FIRE: int = 5
    GRENADE_EXPLODE: int = 6
    NINJA_HIT: int = 7
    RIFLE_FIRE: int = 8
    RIFLE_BOUNCE: int = 9
    WEAPON_SWITCH: int = 10
    PLAYER_PAIN_SHORT: int = 11
    PLAYER_PAIN_LONG: int = 12
    BODY_LAND: int = 13
    PLAYER_AIRJUMP: int = 14
    PLAYER_JUMP: int = 15
    PLAYER_DIE: int = 16
    PLAYER_SPAWN: int = 17
    PLAYER_SKID: int = 18
    TEE_CRY: int = 19
    HOOK_LOOP: int = 20
    HOOK_ATTACH_GROUND: int = 21
    HOOK_ATTACH_PLAYER: int = 22
    HOOK_NOATTACH: int = 23
    PICKUP_HEALTH: int = 24
    PICKUP_ARMOR: int = 25
    PICKUP_GRENADE: int = 26
    PICKUP_SHOTGUN: int = 27
    PICKUP_NINJA: int = 28
    WEAPON_SPAWN: int = 29
    WEAPON_NOAMMO: int = 30
    HIT: int = 31
    CHAT_SERVER: int = 32
    CHAT_CLIENT: int = 33
    CHAT_HIGHLIGHT: int = 34
    CTF_DROP: int = 35
    CTF_RETURN: int = 36
    CTF_GRAB_PL: int = 37
    CTF_GRAB_EN: int = 38
    CTF_CAPTURE: int = 39
    MENU: int = 40

class Spec(Enum):
    FREEVIEW: int = 0
    PLAYER: int = 1
    FLAGRED: int = 2
    FLAGBLUE: int = 3

class Skinpart(Enum):
    BODY: int = 0
    MARKING: int = 1
    DECORATION: int = 2
    HANDS: int = 3
    FEET: int = 4
    EYES: int = 5
