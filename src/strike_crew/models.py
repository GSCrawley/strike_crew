# models.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class IOC(BaseModel):
    ip_addresses: List[str] = Field(default_factory=list)
    domains: List[str] = Field(default_factory=list)
    urls: List[str] = Field(default_factory=list)
    file_hashes: List[str] = Field(default_factory=list)
    email_addresses: List[str] = Field(default_factory=list)

class TTP(BaseModel):
    tactics: List[str] = Field(default_factory=list)
    techniques: List[str] = Field(default_factory=list)
    sub_techniques: List[str] = Field(default_factory=list)
    procedures: List[str] = Field(default_factory=list)

class ThreatActor(BaseModel):
    name: str
    aliases: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    motivation: Optional[str] = None
    country: Optional[str] = None
    
class CVE(BaseModel):
    id: str
    description: Optional[str] = None
    severity: Optional[str] = None
    published_date: Optional[datetime] = None

class Campaign(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class EmergingThreat(BaseModel):
    name: str
    description: str
    threat_type: str
    iocs: IOC = Field(default_factory=IOC)
    ttps: TTP = Field(default_factory=TTP)
    threat_actors: List[ThreatActor] = Field(default_factory=list)
    cves: List[CVE] = Field(default_factory=list)
    campaigns: List[Campaign] = Field(default_factory=list)
    targeted_sectors: List[str] = Field(default_factory=list)
    targeted_countries: List[str] = Field(default_factory=list)
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    confidence_score: float = 0.0
    data_sources: List[str] = Field(default_factory=list)
    mitigation_recommendations: List[str] = Field(default_factory=list)
    related_threats: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    references: List[str] = Field(default_factory=list)