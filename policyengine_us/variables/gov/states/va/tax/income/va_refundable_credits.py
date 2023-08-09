from policyengine_us.model_api import *


class va_refundable_credits(Variable):
    value_type = float
    entity = TaxUnit
    label = "Virginia refundable credits"
    unit = USD
    definition_period = YEAR
    defined_for = StateCode.VA

    adds = "gov.states.va.tax.income.credits.refundable"
