"""
2026 Retirement & HSA Contribution Calculator
Built with Dash + Plotly
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from calculator import calculate_all
from projection import project_retirement, generate_headline, format_currency
from constants import *

# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True,
    title="2026 Retirement Calculator"
)

server = app.server

# Custom CSS for Helvetica and dropdown fixes
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            * {
                font-family: Helvetica, Arial, sans-serif !important;
            }
            .contribution-bar {
                height: 30px;
                border-radius: 4px;
                margin-bottom: 8px;
            }
            /* Fix dropdown text visibility in dark theme */
            .Select-value-label, .Select-value {
                color: white !important;
            }
            .Select-control {
                background-color: #375a7f !important;
            }
            .Select-menu-outer {
                background-color: #2c3034 !important;
            }
            .Select-option {
                background-color: #2c3034 !important;
                color: white !important;
            }
            .Select-option:hover, .Select-option.is-focused {
                background-color: #375a7f !important;
            }
            /* Dash dropdown specific fixes */
            .dash-dropdown .Select-value-label {
                color: white !important;
            }
            .dash-dropdown .Select-single-value {
                color: white !important;
            }
            .VirtualizedSelectOption {
                color: white !important;
            }
            .VirtualizedSelectFocusedOption {
                background-color: #375a7f !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Color scheme for contribution buckets
COLORS = {
    "deferral": "#3B82F6",      # Blue - 401(k) deferral
    "match": "#10B981",          # Green - Employer match
    "mega": "#8B5CF6",           # Purple - Mega Backdoor
    "ira": "#F59E0B",            # Orange - IRA
    "hsa": "#14B8A6",            # Teal - HSA
    "conservative": "#3B82F6",   # Blue
    "moderate": "#10B981",       # Green
    "aggressive": "#F59E0B",     # Orange
    "background": "#1a1d21",
    "card": "#2c3034"
}

# Navbar
navbar = dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand("2026 Retirement Calculator", className="ms-2 fs-4 fw-bold"),
    ], fluid=True),
    color="dark",
    dark=True,
    className="mb-4"
)

# Input form
input_form = dbc.Card([
    dbc.CardHeader(html.H5("Your Information", className="mb-0")),
    dbc.CardBody([
        # Personal Info Section
        html.H6("Personal Details", className="text-muted mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Label("Current Age"),
                dbc.Input(id="input-age", type="number", value=35, min=18, max=80)
            ], md=6),
            dbc.Col([
                dbc.Label("Retirement Age"),
                dbc.Input(id="input-retirement-age", type="number", value=65, min=50, max=80)
            ], md=6),
        ], className="mb-3"),

        dbc.Row([
            dbc.Col([
                dbc.Label("Annual Salary"),
                dbc.InputGroup([
                    dbc.InputGroupText("$"),
                    dbc.Input(id="input-salary", type="number", value=150000, min=0, step=1000)
                ])
            ], md=6),
            dbc.Col([
                dbc.Label("Filing Status"),
                dbc.Select(
                    id="input-filing-status",
                    options=[{"label": s["label"], "value": s["value"]} for s in FILING_STATUSES],
                    value="single"
                )
            ], md=6),
        ], className="mb-3"),

        dbc.Row([
            dbc.Col([
                dbc.Label("Prior-Year FICA Wages", id="fica-label"),
                dbc.InputGroup([
                    dbc.InputGroupText("$"),
                    dbc.Input(id="input-fica-wages", type="number", value=150000, min=0, step=1000)
                ]),
                dbc.Tooltip(
                    "Your 2025 W-2 Box 3. If over $150K, catch-up must be Roth (SECURE 2.0).",
                    target="fica-label"
                )
            ], md=6),
            dbc.Col([
                dbc.Label("Expected Annual Raise"),
                dbc.InputGroup([
                    dbc.Input(id="input-raise", type="number", value=3.0, min=0, max=20, step=0.5),
                    dbc.InputGroupText("%")
                ])
            ], md=6),
        ], className="mb-3"),

        dbc.Row([
            dbc.Col([
                dbc.Label("Expected Inflation"),
                dbc.InputGroup([
                    dbc.Input(id="input-inflation", type="number", value=2.5, min=0, max=10, step=0.5),
                    dbc.InputGroupText("%")
                ])
            ], md=6),
        ], className="mb-4"),

        html.Hr(),

        # 401(k) Section
        html.H6("401(k) Plan Details", className="text-muted mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Label("Employer Match"),
                dbc.InputGroup([
                    dbc.Input(id="input-match-pct", type="number", value=100, min=0, max=200, step=25),
                    dbc.InputGroupText("%")
                ]),
                dbc.FormText("e.g., 100 = 100% match")
            ], md=6),
            dbc.Col([
                dbc.Label("Match Cap (% of salary)"),
                dbc.InputGroup([
                    dbc.Input(id="input-match-cap", type="number", value=6, min=0, max=100, step=1),
                    dbc.InputGroupText("%")
                ]),
                dbc.FormText("e.g., 6 = up to 6% of salary")
            ], md=6),
        ], className="mb-3"),

        dbc.Row([
            dbc.Col([
                dbc.Label("Match Dollar Cap", id="match-cap-label"),
                dbc.InputGroup([
                    dbc.InputGroupText("$"),
                    dbc.Input(id="input-match-dollar-cap", type="number", value=0, min=0, step=500)
                ]),
                dbc.Tooltip("Leave 0 if no dollar cap", target="match-cap-label")
            ], md=6),
        ], className="mb-3"),

        dbc.Row([
            dbc.Col([
                dbc.Label("Plan allows after-tax contributions?", id="aftertax-label"),
                dbc.Select(
                    id="input-allows-aftertax",
                    options=[
                        {"label": "Yes", "value": "yes"},
                        {"label": "No", "value": "no"},
                        {"label": "Not sure", "value": "notsure"},
                    ],
                    value="yes"
                ),
                dbc.Tooltip("Required for Mega Backdoor Roth", target="aftertax-label")
            ], md=6),
            dbc.Col([
                dbc.Label("Plan allows in-plan Roth conversion?", id="conversion-label"),
                dbc.Select(
                    id="input-allows-conversion",
                    options=[
                        {"label": "Yes", "value": "yes"},
                        {"label": "No", "value": "no"},
                        {"label": "Not sure", "value": "notsure"},
                    ],
                    value="yes"
                ),
                dbc.Tooltip("Required for Mega Backdoor Roth", target="conversion-label")
            ], md=6),
        ], className="mb-4"),

        html.Hr(),

        # HSA Section
        html.H6("HSA Details", className="text-muted mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Label("HSA Coverage Type"),
                dbc.Select(
                    id="input-hsa-coverage",
                    options=[{"label": o["label"], "value": o["value"]} for o in HSA_COVERAGE_OPTIONS],
                    value="self"
                )
            ], md=6),
            dbc.Col([
                dbc.Label("Total HSA Contribution (Employer + Yourself)", id="hsa-total-label"),
                dbc.InputGroup([
                    dbc.InputGroupText("$"),
                    dbc.Input(id="input-total-hsa", type="number", value=4400, min=0, step=100)
                ]),
                dbc.Tooltip("2026 max: $4,400 (self) or $8,750 (family). Add $1,000 if 55+.", target="hsa-total-label")
            ], md=6),
        ], className="mb-4"),

        html.Hr(),

        # IRA Section
        html.H6("IRA Details", className="text-muted mb-3"),
        html.Div(id="backdoor-roth-section", children=[
            dbc.Row([
                dbc.Col([
                    dbc.Label("Backdoor Roth IRA Contribution", id="backdoor-label"),
                    dbc.InputGroup([
                        dbc.InputGroupText("$"),
                        dbc.Input(id="input-backdoor-roth", type="number", value=0, min=0, max=8600, step=100)
                    ]),
                    dbc.FormText("Only applies if your income exceeds Roth IRA limits. Max: $7,500 (+$1,100 if 50+).", className="text-muted")
                ], md=6),
            ], className="mb-4"),
        ]),

        html.Hr(),

        # Existing Balances
        html.H6("Existing Balances (for projection)", className="text-muted mb-3"),
        html.P("These balances grow at the same rate as your projection (5%/7%/10% per year).", className="small text-muted mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Label("Current 401(k) Balance"),
                dbc.InputGroup([
                    dbc.InputGroupText("$"),
                    dbc.Input(id="input-balance-401k", type="number", value=100000, min=0, step=5000)
                ])
            ], md=6),
            dbc.Col([
                dbc.Label("Current IRA Balance"),
                dbc.InputGroup([
                    dbc.InputGroupText("$"),
                    dbc.Input(id="input-balance-ira", type="number", value=25000, min=0, step=1000)
                ])
            ], md=6),
        ], className="mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Label("Current HSA Balance"),
                dbc.InputGroup([
                    dbc.InputGroupText("$"),
                    dbc.Input(id="input-balance-hsa", type="number", value=10000, min=0, step=1000)
                ])
            ], md=6),
        ], className="mb-3"),

        dbc.Button("Calculate", id="btn-calculate", color="success", size="lg", className="mt-3 w-100")
    ])
], className="mb-4")

# Results area
results_area = html.Div(id="results-container")

# App layout
app.layout = html.Div([
    navbar,
    dbc.Container([
        dbc.Row([
            dbc.Col([input_form], lg=5),
            dbc.Col([results_area], lg=7),
        ])
    ], fluid=True, className="px-4"),

    # Disclaimer
    dbc.Container([
        html.Hr(className="mt-5"),
        html.P(
            "This calculator is for educational purposes only. It does not constitute tax, legal, or financial advice. "
            "Consult a qualified tax professional or financial advisor for advice specific to your situation. "
            "IRS limits and rules are subject to change.",
            className="text-muted small text-center"
        )
    ], fluid=True, className="px-4 pb-4")
])


def create_contribution_bar_chart(results: dict) -> go.Figure:
    """Create stacked bar chart showing contribution breakdown."""
    totals = results["totals"]["breakdown"]

    fig = go.Figure()

    # Add each contribution type
    categories = ["Your 401(k)", "Employer Match", "Mega Backdoor", "IRA", "HSA"]
    values = [
        totals["401k_deferral"],
        totals["employer_match"],
        totals["mega_backdoor"],
        totals["ira"],
        totals["hsa"]
    ]
    colors = [COLORS["deferral"], COLORS["match"], COLORS["mega"], COLORS["ira"], COLORS["hsa"]]

    fig.add_trace(go.Bar(
        x=values,
        y=["Contributions"],
        orientation="h",
        marker_color=colors[0],
        name="401(k) Deferral",
        text=f"${values[0]:,.0f}",
        textposition="inside",
        hovertemplate="401(k) Deferral: $%{x:,.0f}<extra></extra>"
    ))

    cumulative = values[0]
    for i, (cat, val, color) in enumerate(zip(categories[1:], values[1:], colors[1:]), 1):
        if val > 0:
            fig.add_trace(go.Bar(
                x=[val],
                y=["Contributions"],
                orientation="h",
                marker_color=color,
                name=cat,
                text=f"${val:,.0f}" if val > 2000 else "",
                textposition="inside",
                hovertemplate=f"{cat}: $%{{x:,.0f}}<extra></extra>"
            ))

    fig.update_layout(
        barmode="stack",
        height=100,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        font=dict(color="white")
    )

    return fig


def create_projection_chart(projection: dict, show_real: bool = False) -> go.Figure:
    """Create retirement projection line chart."""
    fig = go.Figure()

    value_key = "real" if show_real else "nominal"

    # Get data for each scenario
    conservative = projection["scenarios"]["conservative"]
    moderate = projection["scenarios"]["moderate"]
    aggressive = projection["scenarios"]["aggressive"]

    years = [d["year"] for d in moderate]
    cons_values = [d[value_key] for d in conservative]
    mod_values = [d[value_key] for d in moderate]
    agg_values = [d[value_key] for d in aggressive]

    # Shaded area between conservative and aggressive
    fig.add_trace(go.Scatter(
        x=years + years[::-1],
        y=agg_values + cons_values[::-1],
        fill="toself",
        fillcolor="rgba(16, 185, 129, 0.1)",
        line=dict(color="rgba(0,0,0,0)"),
        name="Range",
        showlegend=False,
        hoverinfo="skip"
    ))

    # Conservative line
    fig.add_trace(go.Scatter(
        x=years, y=cons_values,
        mode="lines",
        name="Conservative (5%)",
        line=dict(color=COLORS["conservative"], width=2, dash="dot"),
        hovertemplate="Year: %{x}<br>Balance: $%{y:,.0f}<extra>Conservative</extra>"
    ))

    # Moderate line (highlighted)
    fig.add_trace(go.Scatter(
        x=years, y=mod_values,
        mode="lines",
        name="Moderate (7%)",
        line=dict(color=COLORS["moderate"], width=3),
        hovertemplate="Year: %{x}<br>Balance: $%{y:,.0f}<extra>Moderate</extra>"
    ))

    # Aggressive line
    fig.add_trace(go.Scatter(
        x=years, y=agg_values,
        mode="lines",
        name="Aggressive (10%)",
        line=dict(color=COLORS["aggressive"], width=2, dash="dot"),
        hovertemplate="Year: %{x}<br>Balance: $%{y:,.0f}<extra>Aggressive</extra>"
    ))

    value_label = "Today's Dollars" if show_real else "Nominal Dollars"

    fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=dict(text=f"Projected Portfolio Value ({value_label})", font=dict(size=16)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.1)",
            title="Year"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.1)",
            title="Portfolio Value",
            tickformat="$,.0f"
        ),
        font=dict(color="white"),
        hovermode="x unified"
    )

    return fig


@callback(
    Output("results-container", "children"),
    Input("btn-calculate", "n_clicks"),
    [
        State("input-age", "value"),
        State("input-retirement-age", "value"),
        State("input-salary", "value"),
        State("input-filing-status", "value"),
        State("input-fica-wages", "value"),
        State("input-raise", "value"),
        State("input-inflation", "value"),
        State("input-match-pct", "value"),
        State("input-match-cap", "value"),
        State("input-match-dollar-cap", "value"),
        State("input-allows-aftertax", "value"),
        State("input-allows-conversion", "value"),
        State("input-hsa-coverage", "value"),
        State("input-total-hsa", "value"),
        State("input-backdoor-roth", "value"),
        State("input-balance-401k", "value"),
        State("input-balance-ira", "value"),
        State("input-balance-hsa", "value"),
    ],
    prevent_initial_call=True
)
def update_results(
    n_clicks, age, retirement_age, salary, filing_status, fica_wages,
    raise_pct, inflation_pct, match_pct, match_cap, match_dollar_cap,
    allows_aftertax, allows_conversion, hsa_coverage, total_hsa, backdoor_roth,
    balance_401k, balance_ira, balance_hsa
):
    if not n_clicks:
        return html.Div()

    # Convert string dropdown values to booleans
    aftertax_bool = allows_aftertax == "yes"
    conversion_bool = allows_conversion == "yes"

    # Calculate annual contributions
    results = calculate_all(
        age=age or 35,
        salary=salary or 150000,
        magi=salary or 150000,  # Using salary as MAGI approximation
        filing_status=filing_status or "single",
        match_percent=(match_pct or 100) / 100,
        match_cap_percent=(match_cap or 6) / 100,
        match_dollar_cap=match_dollar_cap if match_dollar_cap else None,
        plan_allows_aftertax=aftertax_bool,
        plan_allows_conversion=conversion_bool,
        hsa_coverage=hsa_coverage or "none",
        total_hsa=total_hsa or 0,
        prior_year_fica=fica_wages or 0,
        backdoor_roth=backdoor_roth or 0
    )

    # Calculate projection
    projection = project_retirement(
        current_age=age or 35,
        retirement_age=retirement_age or 65,
        current_salary=salary or 150000,
        annual_raise_pct=(raise_pct or 3) / 100,
        existing_401k=balance_401k or 0,
        existing_ira=balance_ira or 0,
        existing_hsa=balance_hsa or 0,
        match_percent=(match_pct or 100) / 100,
        match_cap_percent=(match_cap or 6) / 100,
        match_dollar_cap=match_dollar_cap if match_dollar_cap else None,
        plan_allows_mega=aftertax_bool and conversion_bool,
        hsa_coverage=hsa_coverage or "none",
        total_hsa=total_hsa or 0,
        inflation_rate=(inflation_pct or 2.5) / 100,
        magi=salary or 150000,
        filing_status=filing_status or "single",
        backdoor_roth=backdoor_roth or 0
    )

    headline = generate_headline(projection)

    # Build results cards
    return html.Div([
        # Headline projection
        dbc.Card([
            dbc.CardBody([
                html.H4(headline["main"], className="text-success text-center mb-1"),
                html.P(headline["subtitle"], className="text-muted text-center mb-0")
            ])
        ], className="mb-4", style={"backgroundColor": COLORS["card"]}),

        # Annual contribution summary
        dbc.Card([
            dbc.CardHeader(html.H5("2026 Tax-Advantaged Savings", className="mb-0")),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H2(f"${results['totals']['your_contributions']:,.0f}", className="text-success"),
                        html.P("Your Contributions", className="text-muted mb-0")
                    ], className="text-center"),
                    dbc.Col([
                        html.H2(f"${results['totals']['employer_match']:,.0f}", className="text-info"),
                        html.P("+ Employer Match", className="text-muted mb-0")
                    ], className="text-center"),
                    dbc.Col([
                        html.H2(f"${results['totals']['total_with_match']:,.0f}", className="text-warning"),
                        html.P("= Total", className="text-muted mb-0")
                    ], className="text-center"),
                ], className="mb-4"),

                # Contribution breakdown bar
                dcc.Graph(figure=create_contribution_bar_chart(results), config={"displayModeBar": False}),

                # Per paycheck
                dbc.Row([
                    dbc.Col([
                        html.H5(f"${results['per_paycheck_biweekly']:,.0f}", className="text-center"),
                        html.P("Per Paycheck (biweekly)", className="text-muted text-center small")
                    ]),
                    dbc.Col([
                        html.H5(f"${results['per_month']:,.0f}", className="text-center"),
                        html.P("Per Month", className="text-muted text-center small")
                    ]),
                ], className="mt-3")
            ])
        ], className="mb-4", style={"backgroundColor": COLORS["card"]}),

        # 401(k) details
        dbc.Card([
            dbc.CardHeader(html.H5("401(k) Breakdown", className="mb-0")),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Span("Base Deferral: ", className="text-muted"),
                            html.Span(f"${results['k401']['base_deferral']:,}")
                        ]),
                        html.Div([
                            html.Span("Catch-up: ", className="text-muted"),
                            html.Span(f"${results['k401']['catchup']:,}")
                        ]) if results['k401']['catchup'] > 0 else None,
                        html.Div([
                            html.Span("Your Max Deferral: ", className="text-muted"),
                            html.Span(f"${results['k401']['your_max_deferral']:,}", className="fw-bold")
                        ]),
                    ]),
                    dbc.Col([
                        html.Div([
                            html.Span("Employer Match: ", className="text-muted"),
                            html.Span(f"${results['k401']['employer_match']:,.0f}")
                        ]),
                        html.Div([
                            html.Span("415(c) Limit: ", className="text-muted"),
                            html.Span(f"${results['k401']['total_415c']:,}")
                        ]),
                    ]),
                ])
            ])
        ], className="mb-4", style={"backgroundColor": COLORS["card"]}),

        # Mega Backdoor Roth
        dbc.Card([
            dbc.CardHeader(html.H5("Mega Backdoor Roth", className="mb-0")),
            dbc.CardBody([
                html.H3(f"${results['mega_backdoor']['room']:,}", className="text-primary") if results['mega_backdoor']['available'] else None,
                html.P("Available after-tax contribution room", className="text-muted") if results['mega_backdoor']['available'] else None,
                dbc.Alert(
                    "Your plan supports Mega Backdoor Roth. You can contribute after-tax dollars and convert to Roth!",
                    color="success"
                ) if results['mega_backdoor']['available'] else dbc.Alert(
                    "Your plan doesn't support Mega Backdoor Roth. Ask your HR about adding after-tax contributions and in-plan Roth conversions.",
                    color="warning"
                )
            ])
        ], className="mb-4", style={"backgroundColor": COLORS["card"]}),

        # IRA
        dbc.Card([
            dbc.CardHeader(html.H5("IRA Contribution", className="mb-0")),
            dbc.CardBody([
                # If income exceeds Roth IRA limit
                html.Div([
                    html.H3(f"${backdoor_roth or 0:,}", className="text-warning"),
                    html.P("Backdoor Roth IRA contribution", className="text-muted"),
                    dbc.Alert(
                        f"You're contributing ${backdoor_roth or 0:,} via Backdoor Roth IRA. "
                        "This involves contributing to a Traditional IRA (non-deductible) and converting to Roth.",
                        color="success"
                    ) if (backdoor_roth or 0) > 0 else dbc.Alert(
                        "The IRS does not allow you to make direct Roth IRA contributions as your income exceeds the limit. "
                        "However, you can research the Backdoor Roth IRA conversion opportunity.",
                        color="warning"
                    )
                ]) if results['ira']['suggest_backdoor'] else html.Div([
                    # If eligible for direct Roth IRA
                    html.H3(f"${results['ira']['allowed_contribution']:,}", className="text-warning"),
                    html.P("Maximum Roth IRA contribution", className="text-muted"),
                    html.P(
                        "You're eligible for direct Roth IRA contributions based on your income.",
                        className="small text-success"
                    )
                ])
            ])
        ], className="mb-4", style={"backgroundColor": COLORS["card"]}),

        # HSA
        dbc.Card([
            dbc.CardHeader(html.H5("HSA Contribution", className="mb-0")),
            dbc.CardBody([
                html.H3(f"${results['hsa']['total_contribution']:,}", className="text-info") if results['hsa']['eligible'] else html.H3("$0"),
                html.P(f"Total HSA contribution (max: ${results['hsa']['max_limit']:,})", className="text-muted") if results['hsa']['eligible'] else None,
                html.P(
                    "Triple tax advantage: tax-deductible contributions, tax-free growth, tax-free qualified withdrawals!",
                    className="small text-muted"
                ) if results['hsa']['eligible'] else html.P(
                    "You must be enrolled in an HDHP to contribute to an HSA.",
                    className="text-warning"
                )
            ])
        ], className="mb-4", style={"backgroundColor": COLORS["card"]}),

        # Projection chart
        dbc.Card([
            dbc.CardHeader([
                dbc.Row([
                    dbc.Col(html.H5("Retirement Projection", className="mb-0")),
                    dbc.Col([
                        dbc.RadioItems(
                            id="projection-toggle",
                            options=[
                                {"label": "Nominal $", "value": "nominal"},
                                {"label": "Today's $", "value": "real"},
                            ],
                            value="nominal",
                            inline=True,
                            className="float-end"
                        )
                    ], className="text-end")
                ])
            ]),
            dbc.CardBody([
                dcc.Graph(
                    id="projection-chart",
                    figure=create_projection_chart(projection, show_real=False),
                    config={"displayModeBar": False}
                ),
                dcc.Store(id="projection-data", data=projection)
            ])
        ], className="mb-4", style={"backgroundColor": COLORS["card"]}),
    ])


@callback(
    Output("projection-chart", "figure"),
    Input("projection-toggle", "value"),
    State("projection-data", "data")
)
def update_projection_view(toggle_value, projection_data):
    if not projection_data:
        return go.Figure()
    show_real = toggle_value == "real"
    return create_projection_chart(projection_data, show_real=show_real)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8051)
