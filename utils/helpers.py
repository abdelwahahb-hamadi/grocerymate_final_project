from datetime import date
from dateutil.relativedelta import relativedelta

def dob_for_age_years(age_years: int) -> str:
    """
    Returns DOB string in DD-MM-YYYY that makes user exactly `age_years` today.
    """
    d = date.today() - relativedelta(years=age_years)
    return d.strftime("%d-%m-%Y")