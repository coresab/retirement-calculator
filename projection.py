"""
Retirement projection engine.
Projects portfolio growth over time with multiple scenarios.
"""

from typing import List, Dict
from calculator import calculate_401k_limits, calculate_employer_match, calculate_hsa_limit, calculate_roth_ira_limit
from constants import *


def project_retirement(
    current_age: int,
    retirement_age: int,
    current_salary: float,
    annual_raise_pct: float,
    existing_401k: float,
    existing_ira: float,
    existing_hsa: float,
    match_percent: float,
    match_cap_percent: float,
    match_dollar_cap: float,
    plan_allows_mega: bool,
    hsa_coverage: str,
    total_hsa: float,
    inflation_rate: float = DEFAULT_INFLATION_RATE,
    magi: float = 0,
    filing_status: str = "single",
    backdoor_roth: float = 0
) -> Dict:
    """
    Project retirement savings year by year.

    Returns projections for 3 scenarios: conservative (5%), moderate (7%), aggressive (10%).
    """
    years = retirement_age - current_age
    if years <= 0:
        return {"error": "Retirement age must be greater than current age"}

    scenarios = {
        "conservative": {"rate": DEFAULT_RETURN_CONSERVATIVE, "data": []},
        "moderate": {"rate": DEFAULT_RETURN_MODERATE, "data": []},
        "aggressive": {"rate": DEFAULT_RETURN_AGGRESSIVE, "data": []}
    }

    # Initialize balances for each scenario
    for scenario in scenarios.values():
        scenario["balance_401k"] = existing_401k
        scenario["balance_ira"] = existing_ira
        scenario["balance_hsa"] = existing_hsa

    current_year = 2026  # Starting year
    salary = current_salary
    age = current_age

    for year_offset in range(years + 1):
        year = current_year + year_offset

        # Calculate limits based on current age
        k401_limits = calculate_401k_limits(age)

        # IRA limit - check if income exceeds Roth limit (use backdoor if so)
        ira_info = calculate_roth_ira_limit(age, magi, filing_status)
        if ira_info["suggest_backdoor"]:
            ira_limit = min(backdoor_roth, ira_info["max_limit"])
        else:
            ira_limit = ira_info["allowed_contribution"]

        # HSA contribution (use provided total, capped by limits)
        hsa_info = calculate_hsa_limit(age, hsa_coverage, total_hsa)
        hsa_contribution = hsa_info["total_contribution"]

        # Employee deferral (capped by salary)
        employee_deferral = min(k401_limits["max_deferral"], salary)

        # Employer match
        employer_match = calculate_employer_match(
            salary, match_percent, match_cap_percent, match_dollar_cap
        )

        # Mega backdoor room
        if plan_allows_mega:
            total_limit = min(k401_limits["total_415c"], salary)
            mega_room = max(0, total_limit - employee_deferral - employer_match)
        else:
            mega_room = 0

        # Total annual contribution
        annual_401k = employee_deferral + employer_match + mega_room

        for name, scenario in scenarios.items():
            rate = scenario["rate"]

            if year_offset == 0:
                # First year - just starting balances
                total = scenario["balance_401k"] + scenario["balance_ira"] + scenario["balance_hsa"]
            else:
                # Add contributions and apply growth
                scenario["balance_401k"] = (scenario["balance_401k"] + annual_401k) * (1 + rate)
                scenario["balance_ira"] = (scenario["balance_ira"] + ira_limit) * (1 + rate)
                scenario["balance_hsa"] = (scenario["balance_hsa"] + hsa_contribution) * (1 + rate)
                total = scenario["balance_401k"] + scenario["balance_ira"] + scenario["balance_hsa"]

            # Inflation-adjusted value
            inflation_factor = (1 + inflation_rate) ** year_offset
            real_value = total / inflation_factor

            scenario["data"].append({
                "year": year,
                "age": age,
                "nominal": round(total, 0),
                "real": round(real_value, 0),
                "balance_401k": round(scenario["balance_401k"], 0),
                "balance_ira": round(scenario["balance_ira"], 0),
                "balance_hsa": round(scenario["balance_hsa"], 0),
                "annual_contribution": round(annual_401k + ira_limit + hsa_contribution, 0),
                "salary": round(salary, 0)
            })

        # Next year: age increases, salary grows
        age += 1
        salary *= (1 + annual_raise_pct)

    # Final results
    final_conservative = scenarios["conservative"]["data"][-1]
    final_moderate = scenarios["moderate"]["data"][-1]
    final_aggressive = scenarios["aggressive"]["data"][-1]

    return {
        "years_to_retirement": years,
        "retirement_year": current_year + years,
        "scenarios": {
            "conservative": scenarios["conservative"]["data"],
            "moderate": scenarios["moderate"]["data"],
            "aggressive": scenarios["aggressive"]["data"]
        },
        "final_balances": {
            "conservative": {
                "nominal": final_conservative["nominal"],
                "real": final_conservative["real"]
            },
            "moderate": {
                "nominal": final_moderate["nominal"],
                "real": final_moderate["real"]
            },
            "aggressive": {
                "nominal": final_aggressive["nominal"],
                "real": final_aggressive["real"]
            }
        },
        "headline": {
            "low_nominal": final_conservative["nominal"],
            "high_nominal": final_aggressive["nominal"],
            "low_real": final_conservative["real"],
            "high_real": final_aggressive["real"],
            "retirement_year": current_year + years
        }
    }


def format_currency(amount: float) -> str:
    """Format number as currency string."""
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"${amount / 1_000:.0f}K"
    else:
        return f"${amount:,.0f}"


def generate_headline(projection: Dict) -> str:
    """Generate the headline projection statement."""
    h = projection["headline"]
    year = h["retirement_year"]
    low = format_currency(h["low_nominal"])
    high = format_currency(h["high_nominal"])
    low_real = format_currency(h["low_real"])
    high_real = format_currency(h["high_real"])

    return {
        "main": f"By {year}, you could have between {low} and {high}",
        "subtitle": f"(~{low_real} to {high_real} in today's dollars)"
    }
