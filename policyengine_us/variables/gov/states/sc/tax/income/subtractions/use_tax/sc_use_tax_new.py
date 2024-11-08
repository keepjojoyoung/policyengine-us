from policyengine_us.model_api import *

class sc_use_tax(Variable):
    value_type = float
    entity = TaxUnit
    label = "South Carolina Use Tax"
    unit = USD
    definition_period = YEAR
    reference = "https://dor.sc.gov/resources-site/lawandpolicy/Documents/SC%20Sales%20Tax%20Manual.pdf"
    defined_for = StateCode.SC

    def formula(tax_unit, period, parameters):
        out_of_state_purchases = tax_unit(
            "out_of_state_purchase_value", period
        )

        county = tax_unit.household("county_str", period)
        
        county_group = tax_unit.household("sc_use_tax_county_group", period)
        
        p = parameters(period).gov.states.sc.tax.income.use_tax

        additional_rate = select(
            [
                county_group == ScUseTaxCountyGroup.GROUP1,
                county_group == ScUseTaxCountyGroup.GROUP2,
                county_group == ScUseTaxCountyGroup.GROUP3,
            ],
            [
                p.group_one,  
                p.group_two,  
                p.group_three,  
            ],
            default=0,  
        )

        total_rate = p.main + additional_rate

        return out_of_state_purchases * total_rate
