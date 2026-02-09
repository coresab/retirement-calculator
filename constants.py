"""
2026 IRS Contribution Limits
Source: IRS Notice 2025-67
"""

# 401(k) / 403(b) / 457(b) Limits
LIMIT_401K_DEFERRAL = 24_500              # Employee elective deferral
LIMIT_401K_CATCHUP_STANDARD = 8_000       # Catch-up (age 50-59, 64+)
LIMIT_401K_CATCHUP_SUPER = 11_250         # Super catch-up (age 60-63, SECURE 2.0)
LIMIT_401K_TOTAL_ADDITIONS = 72_000       # Section 415(c) limit (employee + employer + after-tax)
LIMIT_401K_TOTAL_WITH_CATCHUP = 80_000    # With standard catch-up
LIMIT_401K_TOTAL_WITH_SUPER = 83_250      # With super catch-up (age 60-63)

# SECURE 2.0 Roth Catch-Up Rule
ROTH_CATCHUP_FICA_THRESHOLD = 150_000     # Prior-year FICA wages threshold

# IRA Limits
LIMIT_IRA_CONTRIBUTION = 7_500
LIMIT_IRA_CATCHUP = 1_100                 # Age 50+
LIMIT_IRA_TOTAL_WITH_CATCHUP = 8_600

# Roth IRA Income Phase-Outs (2026)
ROTH_PHASEOUT = {
    "single": {"start": 153_000, "end": 168_000},
    "mfj": {"start": 242_000, "end": 252_000},
    "mfs": {"start": 0, "end": 10_000},
    "hoh": {"start": 153_000, "end": 168_000},  # Same as single
}

# Traditional IRA Deduction Phase-Outs (if covered by workplace plan)
TRAD_IRA_PHASEOUT = {
    "single": {"start": 81_000, "end": 91_000},
    "mfj_has_plan": {"start": 129_000, "end": 149_000},
    "mfj_spouse_has_plan": {"start": 242_000, "end": 252_000},
}

# HSA Limits
LIMIT_HSA_SELF = 4_400
LIMIT_HSA_FAMILY = 8_750
LIMIT_HSA_CATCHUP = 1_000                 # Age 55+ (not enrolled in Medicare)

# HDHP Requirements (to be HSA-eligible)
HDHP_MIN_DEDUCTIBLE_SELF = 1_700
HDHP_MIN_DEDUCTIBLE_FAMILY = 3_400
HDHP_MAX_OOP_SELF = 8_500
HDHP_MAX_OOP_FAMILY = 17_000

# Projection defaults
DEFAULT_ANNUAL_RAISE = 0.03               # 3%
DEFAULT_INFLATION_RATE = 0.025            # 2.5%
DEFAULT_RETURN_CONSERVATIVE = 0.05        # 5%
DEFAULT_RETURN_MODERATE = 0.07            # 7%
DEFAULT_RETURN_AGGRESSIVE = 0.10          # 10%

# Pay periods
PAY_PERIODS_BIWEEKLY = 26
PAY_PERIODS_SEMIMONTHLY = 24

# Filing status options
FILING_STATUSES = [
    {"value": "single", "label": "Single"},
    {"value": "mfj", "label": "Married Filing Jointly"},
    {"value": "mfs", "label": "Married Filing Separately"},
    {"value": "hoh", "label": "Head of Household"},
]

# HSA coverage options
HSA_COVERAGE_OPTIONS = [
    {"value": "none", "label": "Not enrolled in HDHP"},
    {"value": "self", "label": "Self-only coverage"},
    {"value": "family", "label": "Family coverage"},
]
