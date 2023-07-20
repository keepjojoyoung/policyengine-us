from policyengine_us.model_api import *


class nm_property_tax_rebate_eligible(Variable):
    value_type = float
    entity = TaxUnit
    label = "Eligible for the New Mexico property tax rebate"
    unit = USD
    definition_period = YEAR
    reference = "https://klvg4oyd4j.execute-api.us-west-2.amazonaws.com/prod/PublicFiles/34821a9573ca43e7b06dfad20f5183fd/1afc56af-ea90-4d48-82e5-1f9aeb43255a/PITbook2022.pdf"
    defined_for = StateCode.NM

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.states.nm.tax.income.rebates.property_tax
        # Head or spoue eligible if 65 or over
        age_head = tax_unit("age_head", period)
        age_spouse = tax_unit("age_spouse", period)
        age_eligible = (age_head | age_spouse) >= p.age_eligibility
        # Person eligible if income below $16,000
        agi = tax_unit("nm_agi", period)
        agi_eligible = agi <= p.income_threshold
        return age_eligible & agi_eligible
