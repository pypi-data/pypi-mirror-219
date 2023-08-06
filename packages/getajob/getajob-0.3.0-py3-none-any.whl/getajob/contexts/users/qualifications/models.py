import typing as t
from enum import Enum

from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel


class MostRecentWork(BaseModel):
    job_title: str
    company_name: str


class LevelOfEducationEnum(str, Enum):
    HIGH_SCHOOL = "High School"
    ASSOCIATES = "Associates"
    BACHELORS = "Bachelors"
    MASTERS = "Masters"
    PHD = "PhD"
    OTHER = "Other"


class FieldOfStudy(str, Enum):
    COMPUTER_SCIENCE = "Computer Science"
    ENGINEERING = "Engineering"
    BUSINESS = "Business"
    ARTS = "Arts"
    OTHER = "Other"


class SkillEnum(str, Enum):
    PYTHON = "Python"
    JAVASCRIPT = "JavaScript"
    HTML = "HTML"
    CSS = "CSS"
    SQL = "SQL"
    C = "C"
    C_PLUS_PLUS = "C++"
    C_SHARP = "C#"
    JAVA = "Java"
    RUBY = "Ruby"
    PHP = "PHP"
    GO = "Go"
    SWIFT = "Swift"
    KOTLIN = "Kotlin"
    RUST = "Rust"
    TYPESCRIPT = "TypeScript"
    BASH = "Bash"
    OTHER = "Other"


class Education(BaseModel):
    level_of_education: LevelOfEducationEnum
    field_of_study: FieldOfStudy


class Skill(BaseModel):
    skill: SkillEnum
    years_of_experience: int


class LicenseEnum(str, Enum):
    DRIVERS_LICENSE = "Driver's License"
    CDL = "Commercial Driver's License"
    OTHER = "Other"


class License(BaseModel):
    license_name: LicenseEnum
    expiration_date_month: int | None = None
    expiration_date_year: str | None = None
    does_not_expire: bool


class CertificationEnum(str, Enum):
    CPH = "CPH - Certified Professional in Healthcare"


class Certification(BaseModel):
    certification_name: CertificationEnum
    expiration_date_month: int | None = None
    expiration_date_year: str | None = None
    does_not_expire: bool


class LanguageEnum(str, Enum):
    ENGLISH = "English"
    SPANISH = "Spanish"
    FRENCH = "French"
    GERMAN = "German"
    MANDARIN = "Mandarin"
    JAPANESE = "Japanese"
    KOREAN = "Korean"
    ARABIC = "Arabic"


class LanguageProficiencyEnum(str, Enum):
    BASIC = "Basic"
    CONVERSATIONAL = "Conversational"
    FLUENT = "Fluent"
    NATIVE = "Native"


class Langauge(BaseModel):
    language: LanguageEnum
    language_proficiency: LanguageProficiencyEnum


class Qualifications(BaseModel):
    most_recent_job: MostRecentWork | None = None
    education: t.List[Education] | None = None
    skills: t.List[Skill] | None = None
    licenses: t.List[License] | None = None
    certifications: t.List[Certification] | None = None
    language_proficiencies: t.List[Langauge] | None = None


class UserQualifications(Qualifications, BaseDataModel):
    ...
