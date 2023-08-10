from policyengine_us.model_api import *


class co_collegeinvest_amount(Variable):
    value_type = float
    entity = TaxUnit
    label = "Colorado collegeinvest amount"
    unit = USD
    definition_period = YEAR
    defined_for = StateCode.CO
