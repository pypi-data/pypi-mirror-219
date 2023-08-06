from enum import Enum
from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel


class NumEmployeesEnum(str, Enum):
    one_to_ten = "1-10"
    eleven_to_fifty = "11-50"
    fiftyone_to_twohundred = "51-200"
    twohundredone_to_fivehundred = "201-500"
    fivehundredone_to_onethousand = "501-1000"
    morethan_onethousand = "1001+"


class CreateCompanyDetails(BaseModel):
    num_employees: NumEmployeesEnum | None = None
    owner_first_and_last_name: str | None = None
    owner_phone_number: str | None = None
    company_description: str | None = None


class CompanyDetails(BaseDataModel, CreateCompanyDetails):
    ...
