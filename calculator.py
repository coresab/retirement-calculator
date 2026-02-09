"""
Core calculation logic for retirement contributions.
"""

from constants import *


def calculate_401k_limits(age: int) -> dict:
    """
    Calculate 401(k) contribution limits based on age.
    Returns deferral limit and total 415(c) limit.
    """
    if age < 50:
        deferral = LIMIT_401K_DEFERRAL
        total = LIMIT_401K_TOTAL_ADDITIONS
        catchup = 0
        catchup_type = None
    elif 50 <= age <= 59:
        deferral = LIMIT_401K_DEFERRAL + LIMIT_401K_CATCHUP_STANDARD
        total = LIMIT_401K_TOTAL_WITH_CATCHUP
        catchup = LIMIT_401K_CATCHUP_STANDARD
        catchup_type = "standard"
    elif 60 <= age <= 63:
        deferral = LIMIT_401K_DEFERRAL + LIMIT_401K_CATCHUP_SUPER
        total = LIMIT_401K_TOTAL_WITH_SUPER
        catchup = LIMIT_401K_CATCHUP_SUPER
        catchup_type = "super"
    else:  # 64+
        deferral = LIMIT_401K_DEFERRAL + LIMIT_401K_CATCHUP_STANDARD
        total = LIMIT_401K_TOTAL_WITH_CATCHUP
        catchup = LIMIT_401K_CATCHUP_STANDARD
        catchup_type = "standard"

    return {
        "base_deferral": LIMIT_401K_DEFERRAL,
        "catchup": catchup,
        "catchup_type": catchup_type,
        "max_deferral": deferral,
        "total_415c": total
    }


def calculate_employer_match(
    salary: float,
    match_percent: float,
    match_cap_percent: float,
    dollar_cap: float = None
) -> float:
    """
    Calculate employer 401(k) match.

    Args:
        salary: Annual salary
        match_percent: Match rate (e.g., 1.0 for 100% match)
        match_cap_percent: Cap as % of salary (e.g., 0.06 for 6%)
        dollar_cap: Optional absolute dollar cap
    """
    # Employee contributes up to cap, employer matches that
    employee_contribution_for_match = salary * match_cap_percent
    match_amount = employee_contribution_for_match * match_percent

    if dollar_cap:
        match_amount = min(match_amount, dollar_cap)

    return match_amount


def calculate_mega_backdoor_room(
    age: int,
    salary: float,
    employee_deferral: float,
    employer_match: float,
    plan_allows_aftertax: bool,
    plan_allows_conversion: bool
) -> dict:
    """
    Calculate Mega Backdoor Roth contribution room.
    """
    limits = calculate_401k_limits(age)
    total_limit = min(limits["total_415c"], salary)  # Can't exceed 100% of comp

    # Room for after-tax = total limit - deferrals - match
    after_tax_room = total_limit - employee_deferral - employer_match
    after_tax_room = max(0, after_tax_room)

    available = plan_allows_aftertax and plan_allows_conversion

    return {
        "room": after_tax_room if available else 0,
        "available": available,
        "plan_allows_aftertax": plan_allows_aftertax,
        "plan_allows_conversion": plan_allows_conversion,
        "total_415c_limit": total_limit
    }


def calculate_roth_ira_limit(
    age: int,
    magi: float,
    filing_status: str
) -> dict:
    """
    Calculate Roth IRA contribution limit with phase-out.
    """
    base_limit = LIMIT_IRA_CONTRIBUTION
    catchup = LIMIT_IRA_CATCHUP if age >= 50 else 0
    full_limit = base_limit + catchup

    phaseout = ROTH_PHASEOUT.get(filing_status, ROTH_PHASEOUT["single"])
    start = phaseout["start"]
    end = phaseout["end"]

    if magi < start:
        # Full contribution allowed
        limit = full_limit
        eligible = True
        suggest_backdoor = False
    elif magi >= end:
        # No direct Roth contribution
        limit = 0
        eligible = False
        suggest_backdoor = True
    else:
        # Partial contribution (linear phase-out)
        reduction = full_limit * (magi - start) / (end - start)
        limit = full_limit - reduction
        # Round up to nearest $10 per IRS rules
        limit = max(0, round(limit / 10) * 10)
        eligible = True
        suggest_backdoor = False

    return {
        "base_limit": base_limit,
        "catchup": catchup,
        "max_limit": full_limit,
        "allowed_contribution": limit,
        "eligible": eligible,
        "suggest_backdoor": suggest_backdoor,
        "phaseout_start": start,
        "phaseout_end": end
    }


def calculate_hsa_limit(
    age: int,
    coverage_type: str,
    total_contribution: float = 0
) -> dict:
    """
    Calculate HSA contribution limit.
    total_contribution is the combined employer + personal contribution.
    """
    if coverage_type == "none":
        return {
            "base_limit": 0,
            "catchup": 0,
            "max_limit": 0,
            "total_contribution": 0,
            "eligible": False
        }

    if coverage_type == "self":
        base_limit = LIMIT_HSA_SELF
    else:  # family
        base_limit = LIMIT_HSA_FAMILY

    catchup = LIMIT_HSA_CATCHUP if age >= 55 else 0
    max_limit = base_limit + catchup

    # Cap at max limit
    actual_contribution = min(total_contribution, max_limit)

    return {
        "base_limit": base_limit,
        "catchup": catchup,
        "max_limit": max_limit,
        "total_contribution": actual_contribution,
        "eligible": True
    }


def calculate_roth_catchup_requirement(
    age: int,
    prior_year_fica_wages: float
) -> dict:
    """
    Determine if SECURE 2.0 Roth catch-up rule applies.
    If prior-year FICA wages exceed $150,000, catch-up must be Roth.
    """
    if age < 50:
        return {
            "applies": False,
            "reason": "Under age 50, no catch-up contributions"
        }

    if prior_year_fica_wages > ROTH_CATCHUP_FICA_THRESHOLD:
        return {
            "applies": True,
            "must_be_roth": True,
            "reason": f"Prior-year FICA wages (${prior_year_fica_wages:,.0f}) exceed ${ROTH_CATCHUP_FICA_THRESHOLD:,}. Catch-up contributions must be Roth."
        }
    else:
        return {
            "applies": True,
            "must_be_roth": False,
            "reason": "You can make catch-up contributions as pre-tax or Roth."
        }


def calculate_total_tax_advantaged(
    employee_deferral: float,
    employer_match: float,
    mega_backdoor: float,
    ira: float,
    hsa: float
) -> dict:
    """
    Calculate grand total tax-advantaged savings.
    """
    total = employee_deferral + mega_backdoor + ira + hsa
    total_with_match = total + employer_match

    return {
        "your_contributions": total,
        "employer_match": employer_match,
        "total_with_match": total_with_match,
        "breakdown": {
            "401k_deferral": employee_deferral,
            "employer_match": employer_match,
            "mega_backdoor": mega_backdoor,
            "ira": ira,
            "hsa": hsa
        }
    }


def calculate_per_paycheck(
    annual_amount: float,
    pay_periods: int = PAY_PERIODS_BIWEEKLY
) -> float:
    """Calculate per-paycheck contribution amount."""
    return annual_amount / pay_periods


def calculate_all(
    age: int,
    salary: float,
    magi: float,
    filing_status: str,
    match_percent: float,
    match_cap_percent: float,
    match_dollar_cap: float,
    plan_allows_aftertax: bool,
    plan_allows_conversion: bool,
    hsa_coverage: str,
    total_hsa: float,
    prior_year_fica: float,
    backdoor_roth: float = 0
) -> dict:
    """
    Master calculation function - calculates everything.
    """
    # 401(k) limits
    k401_limits = calculate_401k_limits(age)
    max_deferral = min(k401_limits["max_deferral"], salary)

    # Employer match
    employer_match = calculate_employer_match(
        salary, match_percent, match_cap_percent, match_dollar_cap
    )

    # Mega Backdoor
    mega = calculate_mega_backdoor_room(
        age, salary, max_deferral, employer_match,
        plan_allows_aftertax, plan_allows_conversion
    )

    # IRA
    ira = calculate_roth_ira_limit(age, magi, filing_status)

    # HSA
    hsa = calculate_hsa_limit(age, hsa_coverage, total_hsa)

    # Roth catch-up rule
    roth_catchup = calculate_roth_catchup_requirement(age, prior_year_fica)

    # Determine IRA contribution: use backdoor if income too high, otherwise use direct Roth
    if ira["suggest_backdoor"]:
        ira_contribution = min(backdoor_roth, ira["max_limit"])  # Cap at IRA limit
    else:
        ira_contribution = ira["allowed_contribution"]

    # Totals
    totals = calculate_total_tax_advantaged(
        max_deferral,
        employer_match,
        mega["room"],
        ira_contribution,
        hsa["total_contribution"]
    )

    # Per paycheck
    per_paycheck = calculate_per_paycheck(totals["your_contributions"])

    return {
        "age": age,
        "salary": salary,
        "k401": {
            **k401_limits,
            "your_max_deferral": max_deferral,
            "employer_match": employer_match,
            "total_401k_savings": max_deferral + employer_match + mega["room"]
        },
        "mega_backdoor": mega,
        "ira": ira,
        "hsa": hsa,
        "roth_catchup_rule": roth_catchup,
        "totals": totals,
        "per_paycheck_biweekly": per_paycheck,
        "per_paycheck_semimonthly": calculate_per_paycheck(
            totals["your_contributions"], PAY_PERIODS_SEMIMONTHLY
        ),
        "per_month": totals["your_contributions"] / 12
    }
