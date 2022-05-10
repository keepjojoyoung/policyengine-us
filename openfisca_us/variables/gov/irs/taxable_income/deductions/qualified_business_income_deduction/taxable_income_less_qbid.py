from openfisca_us.model_api import *


class taxable_income_less_qbid(Variable):
    value_type = float
    entity = TaxUnit
    label = "Taxable income (not considering QBID)"
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        agi = tax_unit("adjusted_gross_income", period)
        deductions = parameters(period).irs.deductions
        ded_if_itemizing = [
            deduction
            for deduction in deductions.deductions_if_itemizing
            if deduction != "qualified_business_income_deduction"
        ]
        ded_if_not_itemizing = [
            deduction
            for deduction in deductions.deductions_if_not_itemizing
            if deduction != "qualified_business_income_deduction"
        ]
        ded_value_if_itemizing = add(tax_unit, period, ded_if_itemizing)
        ded_value_if_not_itemizing = add(
            tax_unit, period, ded_if_not_itemizing
        )
        itemizes = ded_value_if_itemizing > ded_value_if_not_itemizing
        return max_(
            0,
            agi
            - where(
                itemizes, ded_value_if_itemizing, ded_value_if_not_itemizing
            ),
        )
