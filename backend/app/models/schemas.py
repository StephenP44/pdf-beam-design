from __future__ import annotations

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class MemberType(str, Enum):
    LVL_BEAM = "LVL_beam"
    TIMBER_JOIST = "timber_joist"
    TIMBER_BEARER = "timber_bearer"
    TIMBER_RAFTER = "timber_rafter"
    TIMBER_LINTEL = "timber_lintel"
    SMARTJOIST = "smartjoist"
    STEEL = "steel"


class PointLoad(BaseModel):
    position_m: float
    value_kn: float


class LoadSet(BaseModel):
    udl_kn_per_m: float = 0.0
    point_loads: List[PointLoad] = Field(default_factory=list)


class ZoneType(str, Enum):
    FLOOR = "floor"
    ROOF = "roof"


class Zone(BaseModel):
    id: str
    type: ZoneType
    polygon: List[List[float]]
    dead_udl_kn_per_m2: float = 0.0
    live_udl_kn_per_m2: float = 0.0


class Member(BaseModel):
    id: str
    type: MemberType
    material: str = ""
    nominated_size_schedule: Optional[str] = None
    nominated_size_plan: Optional[str] = None
    final_nominated_size: Optional[str] = None
    span_m: float = 0.0
    cantilever_m: float = 0.0
    supports: List[List[float]] = Field(default_factory=list)
    zone_id: Optional[str] = None
    loads: LoadSet = Field(default_factory=LoadSet)
    check_result: Optional[str] = None
    governing_limit: Optional[str] = None
    computed_deflection_mm: Optional[float] = None
    suggested_size: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)


class ProjectState(BaseModel):
    project_name: str = "Untitled"
    input_pdf_hash: str
    scale_input: str = "1:100"
    scale_detected: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)
    members: List[Member] = Field(default_factory=list)
    zones: List[Zone] = Field(default_factory=list)


class RunCheckRequest(BaseModel):
    project: ProjectState


class RunCheckResponse(BaseModel):
    project: ProjectState
    report_path: str
    annotated_pdf_path: str
