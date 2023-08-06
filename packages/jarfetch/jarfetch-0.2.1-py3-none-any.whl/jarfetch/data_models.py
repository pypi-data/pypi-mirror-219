from typing import MutableMapping, Literal, Union
from dataclasses import dataclass, fields, asdict
from datetime import datetime
import json


# known api jar types as of 2023-06-16T15:01:22Z
JarType = Literal['bedrock', 'modded', 'proxies', 'servers', 'vanilla']

# known api jar categories as of 2023-06-16T15:01:22Z
JarCat = Literal['pocketmine', 'mohist', 'fabric', 'forge', 'catserver', 'waterfall', 'bungeecord', 'velocity', 'paper',
                 'purpur', 'sponge', 'vanilla', 'snapshot']

# known api type-category combinations as of 2023-06-16T15:01:22Z
allowed: dict[JarType, list[JarCat]] = {'bedrock': ['pocketmine'],
                                        'modded': ['mohist', 'fabric', 'forge', 'catserver'],
                                        'proxies': ['waterfall', 'bungeecord', 'velocity'],
                                        'servers': ['paper', 'purpur', 'sponge'],
                                        'vanilla': ['vanilla', 'snapshot']}

# known api endpoints as of 2023-06-16T15:01:22Z
Endpoints = Literal['fetchJar', 'fetchLatest', 'fetchAll', 'fetchTypes', 'fetchDetails']


class FlexTimeStamp(datetime):
    @classmethod
    def from_js_iso(cls, v: int) -> 'FlexTimeStamp':
        return cls.fromtimestamp(v / 1000)

    def __int__(self):
        return int(self.timestamp() * 1000)

    def __str__(self):
        return self.strftime('%Y-%m-%dT%H%MZ')

    def __repr__(self):
        return str(self)


class DynamoJSONEncoder(json.JSONEncoder):
    """
    Expanded capabilities for handling custom nested dataclasses
    """
    def default(self, o):
        if isinstance(o, FlexTimeStamp):
            return int(o)
        elif isinstance(o, JarSize):
            return o.revert()
        elif isinstance(o, Adaptive):
            return asdict(o)
        else:
            return super().default(o)


class Fluid:
    def to_json(self) -> str:
        """Revert the data back to its JSON format"""
        return DynamoJSONEncoder().encode(self)

    def to_dict(self) -> dict:
        """Provide the data as a standard Python dict"""
        return json.loads(self.to_json())


@dataclass
class Adaptive(Fluid):

    @classmethod
    def from_attrs(cls, kvs: MutableMapping):

        cls_attrs = {field.name for field in fields(cls)}

        matched, unmatched = {}, {}
        for k, v in kvs.items():
            if k in cls_attrs:
                matched[k] = v
            else:
                unmatched[k] = v

        built = cls(**matched)

        for k, v in unmatched.items():
            setattr(built, k, v)

        return built


@dataclass
class JarSize(Adaptive):
    """
    Attributes
    ----------
    bytes : int
        number of bytes
    MB : float
        jar file display size
    """

    @classmethod
    def via_conversion(cls, kvs):
        converted = {
            'bytes': kvs['bytes'],
            'MB': float(kvs['display'].split(' ')[0])
        }
        return cls(**converted)

    bytes: int
    MB: float

    def revert(self):
        return {'bytes': self.bytes, 'display': f'{self.MB} MB'}


@dataclass
class JarDetails(Adaptive):
    file: str
    md5: str
    size: Union[JarSize, dict]
    stability: Literal['stable', 'experimental']
    version: str
    built: Union[FlexTimeStamp, int]

    def __post_init__(self):
        if self.built is not None:
            self.built = FlexTimeStamp.from_js_iso(self.built)
        if self.size is not None:
            self.size = JarSize.via_conversion(self.size)


@dataclass
class FullJarDetails(JarDetails):
    jar_type: JarType
    jar_category: JarCat
    version: str
    latest: bool
    href: str


class LocalJarFile:
    file_path: str
    category: JarCat
    fetch_ts: datetime
    size: int
    version: str
    built: int
    md5: str
