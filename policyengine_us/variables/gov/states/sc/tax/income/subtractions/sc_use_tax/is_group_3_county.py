class is_group3_county(Variable):
    value_type = bool
    entity = TaxUnit
    label = "In a South Carolina use tax region 3 county"
    definition_period = YEAR
    defined_for = StateCode.SC
    reference = (
        "https://dor.sc.gov/resources-site/lawandpolicy/Documents/SC%20Sales%20Tax%20Manual.pdf"
    )

    def formula(household, period, parameters):
        county = household("county_str", period)
        group_3_counties = parameters(period).gov.states.sc.tax.income.use_tax.rate.county_group_3
        return np.isin(county, group_3_counties)
