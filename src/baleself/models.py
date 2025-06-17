from dataclasses import dataclass
from typing import Callable, Dict, Any, List, Pattern
from enum import Enum

class EventType(Enum):
    COMMAND = "command"
    REGEX = "regex"

@dataclass
class Message:
    text: str
    data_sid: str
    direction: str
    timestamp: str
    is_gift: bool
    channel_id: str | bool
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        return cls(
            text=data.get('text', ''),
            data_sid=data.get('data_sid', ''),
            direction=data.get('direction', 'ltr'),
            timestamp=data.get('timestamp', ''),
            is_gift=data.get('is_gift', False),
            channel_id=data.get('channel_id', False)
        )

@dataclass
class User:
    name: str | bool
    username: str | bool
    avatar: str | bool
    bio: str | bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        return cls(
            name=data.get('name', False),
            username=data.get('username', False),
            avatar=data.get('avatar', False),
            bio=data.get('bio', False)
        )
        
@dataclass
class Group:
    name: str | bool
    description: str | bool
    group_id: str | bool
    avatar: str | bool
    total_members: int | bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Group':
        return cls(
            name=data.get('name', False),
            description=data.get('description', False),
            group_id=data.get('group_id', False),
            avatar=data.get('avatar', False),
            total_members=data.get('total_members', False),
        )
        
@dataclass
class Channel:
    name: str | bool
    subscribers: int | bool
    channel_id: str | bool
    avatar: str | bool
    description: str | bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Channel':
        return cls(
            name=data.get('name', False),
            subscribers=data.get('subscribers', False), 
            channel_id=data.get('channel_id', False),
            avatar=data.get('avatar', False),
            description=data.get('description', False)
        )

        
@dataclass
class Event:
    type: EventType
    pattern: Pattern = None
    

