from policyengine_us.model_api import *


class sc_use_tax_in_group_two_county(Variable):
    value_type = bool
    entity = Household
    label = "In a South Carolina use tax group two county"
    definition_period = YEAR
    defined_for = StateCode.SC
    reference = "https://dor.sc.gov/resources-site/lawandpolicy/Documents/SC%20Sales%20Tax%20Manual.pdf"

    def formula(household, period, parameters):
        county = household("county_str", period)
        group_two_counties = parameters(
            period
        ).gov.states.sc.tax.income.use_tax.county_group.two
        return np.isin(county, group_two_counties)
