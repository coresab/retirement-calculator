# 2026 Retirement & HSA Contribution Calculator — Build Plan

## Overview

A clean, interactive web app that helps people understand exactly how much they can contribute to their retirement accounts and HSA in the 2026 tax year. Users input their age, salary, filing status, and employer match — the calculator shows their maximum contributions across all accounts, including the Mega Backdoor Roth strategy, with a visual breakdown.

**Goal:** Make complex IRS rules simple and actionable. Most people don't know they're leaving money on the table.

---

## 2026 IRS Limits (Verified from IRS Notice 2025-67)

### 401(k) / 403(b) / 457(b)

| Limit | Amount |
|-------|--------|
| Employee elective deferral (pre-tax or Roth) | $24,500 |
| Catch-up contribution (age 50-59, 64+) | $8,000 |
| "Super" catch-up (age 60-63 only, SECURE 2.0) | $11,250 (replaces the $8,000) |
| Total annual additions limit (Section 415(c)) — employee + employer + after-tax | $72,000 |
| Total with standard catch-up (age 50-59, 64+) | $80,000 |
| Total with super catch-up (age 60-63) | $83,250 |

**SECURE 2.0 Roth Catch-Up Rule (NEW for 2026):**
If your prior-year FICA wages (2025 Box 3 on W-2) exceed $150,000, catch-up contributions **must** be made as Roth (after-tax). Pre-tax catch-up is no longer allowed for high earners.

### Mega Backdoor Roth (After-Tax 401(k) Contributions)

| Component | Calculation |
|-----------|-------------|
| After-tax contribution room | $72,000 − employee deferrals − employer contributions |
| With catch-up (50-59, 64+) | $80,000 − employee deferrals − employer contributions − catch-up |
| With super catch-up (60-63) | $83,250 − employee deferrals − employer contributions − super catch-up |

**Requirements:** Plan must allow (1) after-tax contributions AND (2) in-service distributions or in-plan Roth conversions. Not all plans support this.

### IRA (Traditional & Roth)

| Limit | Amount |
|-------|--------|
| Annual contribution limit | $7,500 |
| Catch-up (age 50+) | $1,100 |
| Total with catch-up | $8,600 |

**Roth IRA Income Phase-Outs (2026):**

| Filing Status | Full Contribution | Phase-Out Range | No Contribution |
|---------------|-------------------|-----------------|-----------------|
| Single / Head of Household | MAGI < $153,000 | $153,000 - $168,000 | MAGI ≥ $168,000 |
| Married Filing Jointly | MAGI < $242,000 | $242,000 - $252,000 | MAGI ≥ $252,000 |
| Married Filing Separately | — | $0 - $10,000 | MAGI ≥ $10,000 |

**Traditional IRA Deduction Phase-Outs (if covered by workplace plan):**

| Filing Status | Phase-Out Range |
|---------------|-----------------|
| Single | $81,000 - $91,000 |
| Married Filing Jointly (contributor has plan) | $129,000 - $149,000 |
| Married Filing Jointly (contributor has NO plan, spouse does) | $242,000 - $252,000 |

**Backdoor Roth IRA:** If income exceeds Roth limits, contribute $7,500 to Traditional IRA (non-deductible) → convert to Roth. Separate from Mega Backdoor Roth.

### HSA (Health Savings Account)

| Limit | Self-Only | Family |
|-------|-----------|--------|
| Annual contribution limit | $4,400 | $8,750 |
| Catch-up (age 55+, not enrolled in Medicare) | +$1,000 | +$1,000 |
| Total with catch-up | $5,400 | $9,750 |

**HDHP Requirements (must be enrolled to contribute to HSA):**

| Requirement | Self-Only | Family |
|-------------|-----------|--------|
| Minimum annual deductible | $1,700 | $3,400 |
| Maximum out-of-pocket | $8,500 | $17,000 |

**Note:** Employer HSA contributions count toward the annual limit. If your employer contributes $1,000, your personal limit is reduced by $1,000.

**NEW for 2026 (One Big Beautiful Bill Act):**
- Bronze and catastrophic plans from an Exchange are now HSA-compatible regardless of whether they meet the standard HDHP definition.
- Direct Primary Care (DPC) arrangement fees can be paid from HSA tax-free.
- Telehealth coverage before meeting deductible no longer disqualifies HSA eligibility (made permanent).

---

## Core Features

### 1. Input Form
User provides:

**Personal Info:**
- **Current age** (or date of birth)
- **Target retirement age** — or target year (toggleable, auto-calculates the other)
- **Annual salary / gross income**
- **Assumed annual raise %** — default 3%, adjustable
- **Filing status** — Single, Married Filing Jointly, Married Filing Separately, Head of Household
- **Prior-year FICA wages** — to determine if Roth catch-up rule applies (over $150,000)

**401(k) Plan Details:**
- **Employer match** — percentage and cap (e.g., "100% match up to 6% of salary")
- **Does your plan allow after-tax contributions?** (Yes/No/Not sure) — for Mega Backdoor Roth
- **Does your plan allow in-plan Roth conversions or in-service distributions?** (Yes/No/Not sure)

**HSA:**
- **HSA coverage type** — Self-only, Family, or Not enrolled in HDHP
- **Employer HSA contribution** — if any

**Existing Balances (for projection):**
- **Current 401(k) balance** — default $0
- **Current IRA balance** — default $0
- **Current HSA balance** — default $0

**Projection Settings:**
- **Assumed inflation rate** — default 2.5%, adjustable

### 2. Results Dashboard
Clearly shows:

**401(k) Section:**
- Your max employee deferral: $24,500 (+ catch-up if eligible)
- Your employer match amount (calculated from salary and match formula)
- Total employer + employee: $X
- Remaining room for Mega Backdoor Roth after-tax contributions: $Y
- Total possible into 401(k): $Z
- Visual bar showing how each bucket fills up toward the $72,000 cap

**Mega Backdoor Roth Explanation:**
- If plan allows it: "You can contribute an additional $X in after-tax dollars and convert to Roth"
- If plan doesn't allow it: "Your plan doesn't support this strategy. Here's what to ask your HR about."
- If not sure: "Check with your plan administrator — here's a template email you can send"

**IRA Section:**
- Roth IRA eligibility based on income
- If eligible: max contribution amount
- If income too high: explain Backdoor Roth strategy
- Traditional IRA deductibility based on income + workplace plan coverage

**HSA Section:**
- Max contribution based on coverage type
- Minus employer contribution
- Your personal max contribution
- Catch-up if 55+
- Explain the triple tax advantage (tax-deductible, tax-free growth, tax-free qualified withdrawals)

**Total Tax-Advantaged Savings Summary:**
- Grand total across all accounts
- Per paycheck breakdown (assuming 26 or 24 pay periods)
- Monthly breakdown
- Visual comparison: "You could save up to $X per year tax-advantaged"

**Retirement Projection (headline):**
- "By [year], you could have between **$X** and **$Y**"
- Subtitle: "(~$A to $B in today's dollars)"
- Interactive chart with 3 growth scenarios
- Toggle: nominal vs. inflation-adjusted
- Hover any year to see balances

### 3. Retirement Projection Engine

**Additional Inputs:**
- **Current age** — used with target retirement age to calculate investment horizon
- **Target retirement** — toggleable between a specific year (e.g., 2051) or years from now (e.g., 25 years). Switching one auto-calculates the other.
- **Existing balances** — current 401(k) balance, IRA balance, HSA balance. These are the starting point for compound growth.
- **Assumed annual raise %** — user-configurable (default 3%). As salary grows each year, employer match and contribution capacity increase.
- **Assumed inflation rate** — default 2.5%, used for inflation-adjusted view

**3 Growth Scenarios:**
| Scenario | Annual Return | Description |
|----------|---------------|-------------|
| Conservative | 5% | Bonds-heavy, lower risk |
| Moderate | 7% | Balanced portfolio (default/highlighted) |
| Aggressive | 10% | Equity-heavy, higher risk |

**Projection Chart (the showstopper visual):**
- X-axis: years (2026 → target retirement year)
- Y-axis: total portfolio value
- 3 lines: conservative (blue), moderate (green), aggressive (orange)
- Shaded area between conservative and aggressive showing the "range of outcomes"
- Hover/tap any year to see projected balance for all 3 scenarios
- Toggle between **nominal dollars** and **inflation-adjusted (today's dollars)**
- Each account type (401k, IRA, HSA) contributes to the total — optionally show stacked breakdown

**Headline Result:**
> "By 2051, you could have between **$1.8M** and **$3.2M** (~$980K to $1.7M in today's dollars)"

**Year-over-Year Logic:**
```
For each year from current_year to retirement_year:
  1. Increase salary by annual_raise_percent
  2. Recalculate employer match based on new salary
  3. Recalculate contribution limits (apply age-based catch-up thresholds as user ages)
  4. Add annual contributions (employee + employer + mega backdoor + IRA + HSA)
  5. Apply investment return to existing balance + new contributions
  6. Store balance for each year for the chart

Note: As the user ages into catch-up eligibility (50, 60-63, 64+),
contribution limits automatically adjust year by year.
```

**Inflation-Adjusted Calculation:**
```
real_value = nominal_value / (1 + inflation_rate) ^ years_from_now
```

### 4. Paycheck Impact Calculator
Show how contributions affect take-home pay:
- Input: current contribution % or $ amount
- Output: estimated per-paycheck impact (accounting for pre-tax savings reducing taxable income)
- "If you max everything out, your paycheck decreases by approximately $X"

### 5. Comparison View
Show side by side:
- "What you're doing now" vs. "What you could be doing"
- Visual bars for current vs. maximum contributions
- Links to the projection chart showing the difference over time

### 6. Education Tooltips
Throughout the app, provide clear explanations:
- What is a Mega Backdoor Roth?
- What does "catch-up contribution" mean?
- What is the SECURE 2.0 Roth catch-up rule?
- Why is an HSA the best retirement account? (triple tax advantage)
- What is a Backdoor Roth IRA vs. Mega Backdoor Roth?
- What's the difference between nominal and inflation-adjusted dollars?
- Why does your annual raise matter for retirement savings?

---

## Tech Stack

| Layer | Tech | Why |
|-------|------|-----|
| Framework | Next.js (React) + App Router | Consistent with your other projects |
| Styling | Tailwind CSS | Fast, clean |
| Charts/Visuals | Recharts | Bar charts for contribution breakdowns, line charts for projections |
| State Management | React useState/useReducer | Simple enough, no Redux needed |
| Hosting | Vercel | Free tier, instant deploy |
| Data | Hardcoded 2026 limits (no API needed) | IRS limits are static for the year |

**No backend needed** — this is a purely client-side calculator. All logic runs in the browser. No user data is stored or transmitted.

---

## Calculation Logic

### 401(k) Employee Deferral
```
if age < 50:
  max_deferral = $24,500
elif age >= 50 and age <= 59:
  max_deferral = $24,500 + $8,000 = $32,500
elif age >= 60 and age <= 63:
  max_deferral = $24,500 + $11,250 = $35,750  (super catch-up)
elif age >= 64:
  max_deferral = $24,500 + $8,000 = $32,500

# Cannot exceed annual salary
max_deferral = min(max_deferral, annual_salary)
```

### Roth Catch-Up Requirement (SECURE 2.0)
```
if prior_year_fica_wages > $150,000 and age >= 50:
  catch_up_must_be_roth = true
  # If plan has no Roth option, catch-up contributions are blocked entirely
```

### Employer Match
```
# Example: 100% match up to 6% of salary
employer_match = min(salary × match_percentage, salary × match_cap_percentage)

# Some plans have a dollar cap
employer_match = min(employer_match, dollar_cap) if dollar_cap exists
```

### Section 415(c) Total Limit
```
if age < 50:
  total_limit = $72,000
elif age >= 50 and age <= 59:
  total_limit = $80,000
elif age >= 60 and age <= 63:
  total_limit = $83,250
elif age >= 64:
  total_limit = $80,000

# Cannot exceed 100% of compensation
total_limit = min(total_limit, annual_salary)
```

### Mega Backdoor Roth Room
```
after_tax_room = total_limit - employee_deferral - employer_match

# Only available if plan allows after-tax + conversions
if plan_allows_after_tax and plan_allows_conversions:
  mega_backdoor_available = after_tax_room
else:
  mega_backdoor_available = 0
```

### Roth IRA Contribution (with phase-out)
```
if filing_status == "single":
  if magi < $153,000:
    roth_ira_limit = $7,500 (+ $1,100 catch-up if 50+)
  elif magi >= $153,000 and magi < $168,000:
    # Partial contribution (linear phase-out)
    reduction = ($7,500) × (magi - $153,000) / ($168,000 - $153,000)
    roth_ira_limit = $7,500 - reduction (rounded up to nearest $10)
  else:
    roth_ira_limit = $0  # Suggest Backdoor Roth

# Similar logic for MFJ with $242,000-$252,000 range
```

### HSA Contribution
```
if not enrolled_in_hdhp:
  hsa_limit = $0
elif coverage == "self_only":
  hsa_limit = $4,400
elif coverage == "family":
  hsa_limit = $8,750

if age >= 55 and not_enrolled_in_medicare:
  hsa_limit += $1,000

# Subtract employer contribution
personal_hsa_limit = hsa_limit - employer_hsa_contribution
```

### Grand Total Tax-Advantaged Savings
```
total = employee_deferral + mega_backdoor_roth + roth_ira (or backdoor) + hsa
# Show this as the headline number
```

### Retirement Projection (Year-by-Year)
```
# Initialize
balance_401k = existing_401k_balance
balance_ira = existing_ira_balance
balance_hsa = existing_hsa_balance
current_salary = annual_salary
current_age = age

for year in range(current_year, retirement_year):

  # 1. Determine age-based limits for this year
  if current_age < 50:
    deferral_limit = 24500
    total_415c = 72000
  elif current_age >= 50 and current_age <= 59:
    deferral_limit = 24500 + 8000
    total_415c = 80000
  elif current_age >= 60 and current_age <= 63:
    deferral_limit = 24500 + 11250
    total_415c = 83250
  elif current_age >= 64:
    deferral_limit = 24500 + 8000
    total_415c = 80000

  ira_limit = 7500 + (1100 if current_age >= 50 else 0)
  hsa_limit = (hsa_base - employer_hsa) + (1000 if current_age >= 55 else 0)

  # 2. Calculate employer match based on current salary
  employer_match = min(current_salary * match_pct, current_salary * match_cap_pct)

  # 3. Calculate mega backdoor room
  mega_room = total_415c - deferral_limit - employer_match
  mega_room = max(mega_room, 0)  # Can't be negative
  if not plan_allows_mega: mega_room = 0

  # 4. Add annual contributions to each bucket
  balance_401k += deferral_limit + employer_match + mega_room
  balance_ira += ira_limit
  balance_hsa += hsa_limit

  # 5. Apply investment return (for each scenario)
  for rate in [0.05, 0.07, 0.10]:
    balance_401k_scenario *= (1 + rate)
    balance_ira_scenario *= (1 + rate)
    balance_hsa_scenario *= (1 + rate)

  # 6. Apply salary raise for next year
  current_salary *= (1 + annual_raise_pct)
  current_age += 1

  # 7. Store year snapshot for chart
  snapshots.append({year, total_balance_by_scenario})

# Inflation adjustment for display
years_out = retirement_year - current_year
real_value = nominal_value / (1 + inflation_rate) ^ years_out
```

**Note on IRS limit increases:** For simplicity, the calculator assumes 2026 limits stay flat for all future years. In reality, IRS limits increase annually with inflation. An optional enhancement would be to assume limits grow at the same inflation rate, but for MVP, flat limits are fine and avoids over-promising.

---

## MVP Scope (Week 1)

### Must Have
- [ ] Input form with all fields (age, salary, filing status, employer match, plan features, HSA)
- [ ] Target retirement input — toggleable between year and years-from-now
- [ ] Existing balances input (401k, IRA, HSA)
- [ ] Annual raise % input (default 3%)
- [ ] 401(k) contribution calculator with catch-up logic (including SECURE 2.0 super catch-up)
- [ ] Employer match calculator
- [ ] Mega Backdoor Roth room calculator
- [ ] Roth IRA eligibility and phase-out calculator
- [ ] Backdoor Roth IRA suggestion when income too high
- [ ] HSA contribution calculator with employer contribution offset
- [ ] Total tax-advantaged savings summary
- [ ] Per-paycheck breakdown
- [ ] Visual bar charts showing how each bucket fills up
- [ ] Retirement projection chart with 3 scenarios (5%, 7%, 10%)
- [ ] Shaded range between conservative and aggressive on chart
- [ ] Hover/tap any year to see projected balances
- [ ] Toggle between nominal and inflation-adjusted dollars (default 2.5% inflation)
- [ ] Headline result: "By [year], you could have between $X and $Y"
- [ ] Year-by-year logic that adjusts catch-up limits as user ages into 50, 60-63, 64+
- [ ] Year-by-year salary increases affecting employer match and contributions
- [ ] Educational tooltips explaining each concept
- [ ] Mobile responsive
- [ ] Disclaimer: "This is for educational purposes only. Consult a tax professional."

### Nice to Have (Week 2+)
- [ ] Comparison view (current contributions vs. max)
- [ ] Paycheck take-home impact calculator
- [ ] Shareable results (URL with encoded params)
- [ ] Dark mode
- [ ] Print/PDF export of your contribution plan
- [ ] "Email your HR" template for asking about after-tax contributions
- [ ] Support for multiple 401(k) plans (job changers mid-year)
- [ ] 2025 vs. 2026 comparison
- [ ] Account-level stacked breakdown in projection chart (401k vs IRA vs HSA)
- [ ] Assume IRS limits grow with inflation (optional toggle for more realistic projection)

---

## Project Structure

```
retirement-calculator/
├── src/
│   ├── app/
│   │   ├── page.tsx                  # Main calculator page
│   │   ├── layout.tsx                # App layout + metadata
│   │   └── globals.css               # Tailwind imports
│   ├── components/
│   │   ├── InputForm.tsx             # User input form (all sections)
│   │   ├── ResultsSummary.tsx        # Grand total + per-paycheck
│   │   ├── Section401k.tsx           # 401(k) breakdown
│   │   ├── SectionMegaBackdoor.tsx   # Mega Backdoor Roth section
│   │   ├── SectionIRA.tsx            # IRA eligibility + contribution
│   │   ├── SectionHSA.tsx            # HSA contribution
│   │   ├── ContributionBar.tsx       # Visual bar chart component
│   │   ├── ProjectionChart.tsx       # Retirement growth projection (Recharts)
│   │   ├── ProjectionHeadline.tsx    # "By 2051, you could have..." headline
│   │   ├── ScenarioToggle.tsx        # Nominal vs. inflation-adjusted toggle
│   │   ├── RetirementTargetInput.tsx # Year vs. years-from-now toggle input
│   │   ├── Tooltip.tsx               # Educational tooltip component
│   │   └── Disclaimer.tsx            # Legal disclaimer
│   ├── lib/
│   │   ├── constants.ts              # All 2026 IRS limits in one place
│   │   ├── calculator.ts             # Core contribution calculation logic
│   │   ├── projection.ts             # Year-by-year projection engine
│   │   ├── formatters.ts             # Currency/number formatting helpers
│   │   └── types.ts                  # TypeScript interfaces
│   └── data/
│       └── tooltips.ts               # Educational content for tooltips
├── package.json
├── tailwind.config.js
├── tsconfig.json
└── next.config.js
```

---

## Claude Code Kickoff Prompt

```
I want to build a 2026 Retirement & HSA Contribution Calculator — a clean, interactive
web app that helps people understand how much they can contribute to their 401(k),
IRA, Mega Backdoor Roth, and HSA based on the latest 2026 IRS limits. It also projects
how much they could retire with based on 3 growth scenarios.

## Key Details

This is a client-side only calculator. No backend, no database, no API calls.
All IRS limits are hardcoded constants.

**2026 IRS Limits to encode:**
- 401(k) employee deferral: $24,500
- 401(k) catch-up (age 50-59, 64+): $8,000
- 401(k) super catch-up (age 60-63, SECURE 2.0): $11,250
- Total 401(k) annual additions (415c): $72,000 (no catch-up), $80,000 (standard), $83,250 (super)
- IRA contribution: $7,500
- IRA catch-up (50+): $1,100
- Roth IRA phase-out (single): $153,000-$168,000
- Roth IRA phase-out (MFJ): $242,000-$252,000
- HSA self-only: $4,400 / HSA family: $8,750
- HSA catch-up (55+): $1,000
- HDHP min deductible: $1,700 self / $3,400 family
- HDHP max OOP: $8,500 self / $17,000 family
- SECURE 2.0 Roth catch-up wage threshold: $150,000 (prior year FICA wages)

**User inputs:**
- Current age
- Target retirement (toggleable: specific year OR years-from-now, auto-calc the other)
- Annual salary
- Assumed annual raise % (default 3%)
- Filing status (Single, MFJ, MFS, HOH)
- Employer match (% and cap)
- Does plan allow after-tax contributions? (Yes/No/Not sure)
- Does plan allow in-plan Roth conversions? (Yes/No/Not sure)
- HSA coverage type (Self-only, Family, Not enrolled)
- Employer HSA contribution
- Prior-year FICA wages (for SECURE 2.0 Roth catch-up rule)
- Existing balances: current 401(k), IRA, and HSA balances
- Assumed inflation rate (default 2.5%)

**What the app calculates and displays:**

Part 1 — Annual Contribution Breakdown:
1. 401(k) max employee deferral (with catch-up if eligible)
2. Employer match amount
3. Mega Backdoor Roth room (after-tax contribution space)
4. IRA contribution (with Roth eligibility check and Backdoor Roth suggestion)
5. HSA max contribution (minus employer contribution)
6. Grand total tax-advantaged savings
7. Per-paycheck breakdown (26 or 24 pay periods)
8. Visual bar charts showing how each bucket fills toward the $72K cap
9. Educational tooltips explaining each concept

Part 2 — Retirement Projection:
1. Year-by-year compound growth starting from existing balances
2. Each year: increase salary by raise %, recalculate match, adjust catch-up as user ages
3. 3 growth scenarios: conservative (5%), moderate (7%), aggressive (10%)
4. Interactive line chart: X=years, Y=portfolio value, 3 lines + shaded range
5. Toggle between nominal dollars and inflation-adjusted (today's dollars)
6. Hover any year to see projected balance for all 3 scenarios
7. Headline: "By [year], you could have between $X and $Y (~$A-$B in today's dollars)"

**Tech stack:**
- Next.js with App Router + TypeScript
- Tailwind CSS
- Recharts for all charts (bar charts for contribution breakdown, line/area chart for projection)
- No backend — purely client-side

**Design:**
- Clean, modern, professional — feels like a premium fintech tool
- Mobile responsive
- Color-coded contribution buckets:
  - 401(k) deferral: Blue
  - Employer match: Green
  - Mega Backdoor Roth: Purple
  - IRA: Orange
  - HSA: Teal
- The projection chart is the hero visual — prominent placement
- 3 scenario lines with shaded range between conservative and aggressive
- Sections for: 401(k), Mega Backdoor Roth, IRA, HSA, Grand Total, Projection

**Important UX details:**
- When Mega Backdoor Roth isn't available, explain what it is + suggest asking HR
- When income too high for Roth IRA, explain Backdoor Roth strategy
- As user ages through the projection, catch-up limits auto-adjust (hitting 50, 60, 64)
- Salary grows each year → employer match grows → more total savings
- Include disclaimer: "For educational purposes only. Consult a tax professional."

Let's build this step by step. Start with:
1. constants.ts — all 2026 IRS limits
2. calculator.ts — annual contribution calculation logic
3. projection.ts — year-by-year projection engine
4. InputForm component
5. Results + charts
```

---

## Design Notes

- **Color scheme suggestion:** Use distinct colors for each bucket:
  - 401(k) employee deferral: Blue
  - Employer match: Green
  - Mega Backdoor Roth (after-tax): Purple
  - IRA: Orange
  - HSA: Teal
- **Two hero visuals:**
  1. The **bar chart** showing how $72,000 gets filled (deferral → match → after-tax room). Makes Mega Backdoor Roth click instantly.
  2. The **projection chart** showing 3 growth lines fanning out over time with shaded range. This is the emotional payoff — seeing $2M+ makes people act.
- **Headline hierarchy:**
  - First: "You can save up to **$XX,XXX** tax-advantaged in 2026"
  - Second: "By **[year]**, you could have between **$X.XM** and **$X.XM**"
  - Subtitle: "(~$X.XM to $X.XM in today's dollars)"
- **Progressive disclosure:** Start simple (totals + projection headline), let users expand each section for details
- **The nominal/inflation toggle** should be right above the projection chart, clearly labeled so people understand what they're looking at

---

## Important Disclaimers to Include

- This calculator is for educational and informational purposes only.
- It does not constitute tax, legal, or financial advice.
- Consult a qualified tax professional or financial advisor for advice specific to your situation.
- IRS limits and rules are subject to change.
- Mega Backdoor Roth availability depends on your specific employer plan.
- State tax treatment of Roth conversions may vary.
- All calculations are estimates and may not reflect your exact situation.
