from __future__ import annotations

from datetime import date
from enum import Enum
from typing import List
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class DefaultDates(BaseModel):
    ActivationDate: date
    DeactivationDate: date


class Department(DefaultDates):
    DepartmentIdentifier: str
    DepartmentLevelIdentifier: str
    DepartmentName: Optional[str]
    DepartmentUUIDIdentifier: Optional[UUID]


class EmploymentStatus(DefaultDates):
    # TODO: add constraint
    EmploymentStatusCode: str


class Employment(BaseModel):
    # TODO: add missing fields
    EmploymentIdentifier: str
    EmploymentDate: date
    AnniversaryDate: date
    EmploymentStatus: EmploymentStatus


class Person(BaseModel):
    """
    An SD (GetEmployment) person... can maybe be generalized
    """

    # TODO: add constraint
    PersonCivilRegistrationIdentifier: str
    Employment: List[Employment]


class GetDepartmentResponse(BaseModel):
    """
    Response model for SDs GetDepartment20111201
    """

    # TODO: add missing fields
    RegionIdentifier: str
    RegionUUIDIdentifier: Optional[UUID]
    InstitutionIdentifier: str
    InstitutionUUIDIdentifier: Optional[UUID]
    Department: List[Department]


class GetEmploymentResponse(BaseModel):
    """
    Response model for SDs GetDepartment20111201
    """

    Person: List[Person]


class DepartmentLevelIdentifierEnum(str, Enum):
    afdelings_niveau = "Afdelings-niveau"
    ny0_niveau = "NY0-niveau"
    ny1_niveau = "NY1-niveau"
    ny2_niveau = "NY2-niveau"
    ny3_niveau = "NY3-niveau"
    ny4_niveau = "NY4-niveau"
    ny5_niveau = "NY5-niveau"
    ny6_niveau = "NY6-niveau"
    ny7_niveau = "NY7-niveau"
    ny8_niveau = "NY8-niveau"


class DepartmentLevelReference(BaseModel):
    DepartmentLevelIdentifier: DepartmentLevelIdentifierEnum | None = None
    DepartmentLevelReference: DepartmentLevelReference | None = None
    # TODO: add validator?


class DepartmentReference(BaseModel):
    DepartmentIdentifier: str
    DepartmentUUIDIdentifier: UUID | None = None
    DepartmentLevelIdentifier: DepartmentLevelIdentifierEnum
    DepartmentReference: list[DepartmentReference] = []


class OrganizationModel(DefaultDates):
    DepartmentReference: list[DepartmentReference] = []


class GetOrganizationResponse(BaseModel):
    """
    Response model for SDs GetOrganisation20111201
    """

    RegionIdentifier: str
    RegionUUIDIdentifier: UUID | None = None
    InstitutionIdentifier: str
    InstitutionUUIDIdentifier: UUID | None = None
    DepartmentStructureName: str

    OrganizationStructure: DepartmentLevelReference
    Organization: list[OrganizationModel] = []
