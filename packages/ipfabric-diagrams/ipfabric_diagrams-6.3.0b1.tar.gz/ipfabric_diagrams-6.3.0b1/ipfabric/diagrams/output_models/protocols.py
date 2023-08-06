from typing import List, Union, Optional

from pydantic import BaseModel, Field

try:
    # TODO py37 & py38 required
    from typing import Annotated, Literal
except ImportError:
    from typing_extensions import Annotated, Literal


class Transport(BaseModel):
    src: Union[List[str], str]
    dst: Union[List[str], str]


class TCP(Transport, BaseModel):
    flags: List[str]
    type: Literal["tcp"]


class UDP(Transport, BaseModel):
    type: Literal["udp"]


class ICMP(BaseModel):
    icmpCode: int
    icmpType: int
    type: Literal["icmp"]


class MPLS(BaseModel):
    stack: List[str]
    type: Literal["mpls"]


class Ethernet(BaseModel):
    src: Optional[str] = None
    dst: Optional[str] = None
    etherType: str
    type: Literal["ethernet"]
    vlan: Optional[int] = None


class ESP(BaseModel):
    payload: str
    nextHeader: str
    type: Literal["esp"]


class IP(BaseModel):
    src: List[str]
    dst: List[str]
    fragmentOffset: int = Field(alias="fragment offset")
    protocol: str
    ttl: int
    type: Literal["ip"]


class VXLAN(BaseModel):
    type: Literal["vxlan"]
    vni: int


class CAPWAP(BaseModel):
    type: Literal["capwap"]


class GRE(BaseModel):
    type: Literal["gre"]


PROTOCOLS = Annotated[Union[ICMP, UDP, TCP, Ethernet, IP, MPLS, ESP, VXLAN, CAPWAP], Field(discriminator="type")]
