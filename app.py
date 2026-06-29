import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(page_title="Forge — Men's Jewellery Command Dashboard", page_icon="◆", layout="wide")

# ── Theme colours ──
GOLD = "#C8A55B"
POS = "#3FB68B"
NEG = "#E5645E"
STEEL = "#5B8DEF"
AMBER = "#E0A33E"
VIOLET = "#9B7FE0"
MUTED = "#8A94A3"
FAINT = "#5B6573"
INK = "#0E1116"
SURFACE = "#161B22"
SURFACE2 = "#1C232C"
LINE = "#262E38"

# ── Custom CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');
.stApp { background: #0E1116; color: #E6E9EE; }
[data-testid="stSidebar"] { background: #161B22; border-right: 1px solid #262E38; }
[data-testid="stSidebar"] .stRadio label { color: #8A94A3; font-size: 13px; }
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; }
.kpi-card { background: #161B22; border: 1px solid #262E38; border-radius: 14px; padding: 16px; position: relative; overflow: hidden; }
.kpi-card .label { font-size: 10.5px; letter-spacing: 1px; text-transform: uppercase; color: #5B6573; }
.kpi-card .value { font-size: 24px; font-weight: 700; margin-top: 7px; font-family: 'JetBrains Mono', monospace; }
.kpi-card .delta { font-size: 11.5px; margin-top: 5px; }
.up { color: #3FB68B; } .down { color: #E5645E; }
.card { background: #161B22; border: 1px solid #262E38; border-radius: 14px; padding: 18px; margin-bottom: 16px; }
.tag { font-size: 10px; letter-spacing: .6px; text-transform: uppercase; padding: 3px 8px; border-radius: 20px; font-weight: 600; }
.tag-pos { background: rgba(63,182,139,.14); color: #3FB68B; }
.tag-neg { background: rgba(229,100,94,.14); color: #E5645E; }
.tag-warn { background: rgba(224,163,62,.14); color: #E0A33E; }
.tag-gold { background: rgba(200,165,91,.14); color: #C8A55B; }
.alert { display: flex; gap: 12px; align-items: flex-start; padding: 13px 14px; border-radius: 11px; border: 1px solid #262E38; background: #1C232C; margin-bottom: 10px; }
.alert .dot { width: 9px; height: 9px; border-radius: 50%; margin-top: 5px; flex: none; }
.alert.crit { border-color: rgba(229,100,94,.4); }
.alert.crit .dot { background: #E5645E; box-shadow: 0 0 10px #E5645E; }
.alert.warn { border-color: rgba(224,163,62,.35); }
.alert.warn .dot { background: #E0A33E; }
.alert.good { border-color: rgba(63,182,139,.35); }
.alert.good .dot { background: #3FB68B; }
.alert .t { font-weight: 600; font-size: 13px; margin-bottom: 2px; color: #E6E9EE; }
.alert .d { font-size: 12px; color: #8A94A3; }
.alert .fix { font-size: 11.5px; color: #C8A55B; margin-top: 4px; }
.mini-card { background: #1C232C; border: 1px solid #262E38; border-radius: 11px; padding: 13px; }
.mini-card .l { font-size: 10.5px; letter-spacing: .8px; text-transform: uppercase; color: #5B6573; }
.mini-card .v { font-size: 19px; font-weight: 700; font-family: 'JetBrains Mono', monospace; margin-top: 6px; color: #E6E9EE; }
.mini-card .s { font-size: 11px; color: #8A94A3; margin-top: 3px; }
.pill { font-size: 10.5px; padding: 2px 8px; border-radius: 20px; font-weight: 600; }
.pill-win { background: rgba(63,182,139,.15); color: #3FB68B; }
.pill-ok { background: rgba(91,141,239,.15); color: #5B8DEF; }
.pill-dead { background: rgba(229,100,94,.15); color: #E5645E; }
.pill-watch { background: rgba(224,163,62,.15); color: #E0A33E; }
.pl-line { display: grid; grid-template-columns: 1fr auto auto; gap: 10px; align-items: center; padding: 11px 0; border-bottom: 1px solid #262E38; color: #E6E9EE; }
.pl-line:last-child { border-bottom: 0; }
.pl-line .nm { font-size: 13px; }
.pl-line .nm small { display: block; color: #5B6573; font-size: 11px; }
.pl-line .amt { font-family: 'JetBrains Mono', monospace; font-size: 13.5px; text-align: right; }
.pl-line .pct { font-family: 'JetBrains Mono', monospace; font-size: 11.5px; color: #8A94A3; text-align: right; min-width: 54px; }
.pl-line.head { font-weight: 600; }
.pl-line.total { border-top: 2px solid #262E38; background: rgba(200,165,91,.04); margin-top: 4px; padding: 13px 8px; border-radius: 8px; }
.pl-cost .amt { color: #E5645E; }
.pl-rev .amt { color: #3FB68B; }
.note { font-size: 11.5px; color: #5B6573; margin-top: 14px; line-height: 1.6; }
.hero-card { border: 1px solid #262E38; border-radius: 14px; padding: 18px; background: #161B22; position: relative; overflow: hidden; }
.leak-card { display: grid; grid-template-columns: 38px 1fr auto; gap: 16px; align-items: start; padding: 16px 18px; border: 1px solid #262E38; border-radius: 13px; background: #161B22; margin-bottom: 11px; color: #E6E9EE; }
.leak-card .rk { font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 700; color: #5B6573; text-align: center; padding-top: 2px; }
.leak-card .nm { font-weight: 600; font-size: 14.5px; margin-bottom: 5px; }
.leak-card .cause { font-size: 12.5px; color: #8A94A3; line-height: 1.5; }
.leak-card .fix { font-size: 12px; color: #C8A55B; margin-top: 8px; }
.leak-card .amt { font-family: 'JetBrains Mono', monospace; font-size: 21px; font-weight: 700; text-align: right; }
.leak-card .per { font-size: 10.5px; color: #5B6573; margin-top: 2px; text-align: right; }
.scenario { border: 1px solid #262E38; border-radius: 12px; padding: 16px; background: #1C232C; color: #E6E9EE; }
.scenario .s-name { font-family: 'Space Grotesk', sans-serif; font-weight: 600; font-size: 13px; letter-spacing: .6px; margin-top: 4px; text-transform: uppercase; }
.scenario .s-pct { font-size: 34px; font-weight: 700; line-height: 1.1; margin-top: 6px; font-family: 'JetBrains Mono', monospace; color: #E6E9EE; }
.plan-line { display: flex; justify-content: space-between; align-items: center; padding: 9px 2px; border-bottom: 1px solid #262E38; font-size: 13px; color: #E6E9EE; }
.plan-line span { color: #8A94A3; }
.plan-line b { font-family: 'JetBrains Mono', monospace; }
.plan-line.hl { background: rgba(200,165,91,.06); margin: 4px -8px; padding: 11px 8px; border-radius: 7px; border-bottom: 0; }
div[data-testid="stMetric"] { background: #161B22; border: 1px solid #262E38; border-radius: 14px; padding: 12px 16px; }
.stTabs [data-baseweb="tab-list"] { gap: 2px; }
.stTabs [data-baseweb="tab"] { background: #161B22; border-radius: 8px; color: #8A94A3; }
.stTabs [aria-selected="true"] { background: #1C232C !important; color: #C8A55B !important; }
table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
thead th { text-align: left; color: #5B6573; font-size: 10.5px; letter-spacing: .8px; text-transform: uppercase; font-weight: 600; padding: 9px 10px; border-bottom: 1px solid #262E38; }
tbody td { padding: 10px; border-bottom: 1px solid #262E38; color: #E6E9EE; }
tbody tr:last-child td { border-bottom: 0; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# DATA — same as the HTML dashboard
# ══════════════════════════════════════════════════════════════════════════
D = {
    "currency": "£",
    "month": "June 2026",
    "grossRevenue": 248500,
    "refunds": 14910,
    "orders": 3420,
    "newCustomers": 2050,
    "returningCustomers": 1370,
    "cogs": 51390,
    "shippingOut": 21204,
    "packaging": 3762,
    "paymentFees": 5606,
    "pickPackLabour": 8037,
    "metaSpend": 38000, "googleSpend": 22000, "tiktokSpend": 15000,
    "emailPlatform": 900, "influencer": 6000,
    "salariesOther": 34000, "rent": 4500, "software": 2200, "utilities": 1800, "insurance": 600,
    "channels": [
        {"name": "Meta", "rev": 92000, "spend": 38000, "orders": 1260, "ctr": 1.8, "cvr": 2.6, "newCust": 980, "colour": STEEL},
        {"name": "Google", "rev": 58000, "spend": 22000, "orders": 760, "ctr": 4.1, "cvr": 3.4, "newCust": 520, "colour": POS},
        {"name": "TikTok", "rev": 28000, "spend": 15000, "orders": 430, "ctr": 1.1, "cvr": 1.4, "newCust": 340, "colour": VIOLET},
        {"name": "Email", "rev": 41000, "spend": 900, "orders": 600, "ctr": 3.2, "cvr": 4.8, "newCust": 90, "colour": GOLD},
        {"name": "Organic", "rev": 29500, "spend": 0, "orders": 370, "ctr": 0, "cvr": 3.1, "newCust": 120, "colour": MUTED},
    ],
    "repeatRate": 28.4, "avgOrdersLifetime": 1.9, "ltv": 84.9, "blendedCAC": 36.6,
    "cohorts": [
        {"m": "Jan", "d": [100, 18, 26, 31, 35, 38]},
        {"m": "Feb", "d": [100, 19, 27, 33, 37, None]},
        {"m": "Mar", "d": [100, 21, 29, 34, None, None]},
        {"m": "Apr", "d": [100, 22, 31, None, None, None]},
        {"m": "May", "d": [100, 24, None, None, None, None]},
        {"m": "Jun", "d": [100, None, None, None, None, None]},
    ],
    "email": [
        {"name": "Welcome flow", "rev": 9800, "type": "flow"},
        {"name": "Abandoned checkout", "rev": 7600, "type": "flow"},
        {"name": "Browse abandon", "rev": 3100, "type": "flow"},
        {"name": "Post-purchase", "rev": 4200, "type": "flow"},
        {"name": "Win-back", "rev": 2300, "type": "flow"},
        {"name": "Campaigns (broadcasts)", "rev": 14000, "type": "campaign"},
    ],
    "organicTrend": [21000, 23500, 24800, 26200, 28100, 29500],
    "winners": [
        {"name": "Onyx Signet Ring", "rev": 21400, "spend": 6100, "margin": 64, "units": 298},
        {"name": "Cuban Link Chain 5mm", "rev": 18900, "spend": 5400, "margin": 58, "units": 214},
        {"name": "Matte Steel Bracelet", "rev": 12600, "spend": 3200, "margin": 67, "units": 340},
    ],
    "wasted": [
        {"name": "Engraved Dog Tag", "rev": 2100, "spend": 2950, "margin": 41, "roas": 0.71},
        {"name": "Leather Wrap Bracelet", "rev": 1600, "spend": 2100, "margin": 38, "roas": 0.76},
        {"name": "Gold Hoop (single)", "rev": 1900, "spend": 2200, "margin": 44, "roas": 0.86},
    ],
    "prodMargin": [
        {"name": "Onyx Signet", "m": 64}, {"name": "Cuban Link", "m": 58}, {"name": "Steel Bracelet", "m": 67},
        {"name": "Beaded Set", "m": 52}, {"name": "Pendant", "m": 55}, {"name": "Dog Tag", "m": 41}, {"name": "Hoop", "m": 44},
    ],
    "launches": [
        {"name": "Obsidian Collection", "date": "02 Jun", "rev": 16800, "sellthru": 72, "margin": 61, "status": "win"},
        {"name": "Minimalist Studs", "date": "09 Jun", "rev": 6400, "sellthru": 48, "margin": 57, "status": "ok"},
        {"name": "Festival Layered Set", "date": "14 Jun", "rev": 2900, "sellthru": 31, "margin": 49, "status": "watch"},
    ],
    "stockValue": 184600, "skuCount": 142, "deadStockValue": 14280,
    "invStatus": [{"l": "Best sellers", "v": 92000, "c": POS}, {"l": "Steady", "v": 58320, "c": STEEL}, {"l": "Slow", "v": 20000, "c": AMBER}, {"l": "Dead", "v": 14280, "c": NEG}],
    "inv": [
        {"sku": "Onyx Signet Ring", "units": 412, "value": 9080, "sellthru": 88, "days": 11, "status": "win"},
        {"sku": "Cuban Link 5mm", "units": 308, "value": 7300, "sellthru": 81, "days": 14, "status": "win"},
        {"sku": "Steel Bracelet", "units": 520, "value": 6240, "sellthru": 76, "days": 18, "status": "ok"},
        {"sku": "Beaded Set", "units": 290, "value": 5800, "sellthru": 43, "days": 62, "status": "watch"},
        {"sku": "Engraved Dog Tag", "units": 610, "value": 6710, "sellthru": 19, "days": 148, "status": "dead"},
        {"sku": "Leather Wrap", "units": 430, "value": 4730, "sellthru": 22, "days": 131, "status": "dead"},
    ],
    "dead": [
        {"sku": "Engraved Dog Tag", "units": 610, "value": 6710, "age": 148, "plan": "Bundle + 40% markdown"},
        {"sku": "Leather Wrap", "units": 430, "value": 4730, "age": 131, "plan": "Clearance email to lapsed list"},
        {"sku": "Gold Hoop single", "units": 180, "value": 1980, "age": 96, "plan": "Pair as set, push on TikTok"},
        {"sku": "Festival Set", "units": 74, "value": 860, "age": 38, "plan": "Watch 14 days then mark down"},
    ],
    "staff": [
        {"name": "Marcus T.", "role": "Paid social buyer", "type": "rev", "driven": 118000, "cost": 3400, "target": 110000, "errors": None, "packed": None},
        {"name": "Priya R.", "role": "Email & retention", "type": "rev", "driven": 41000, "cost": 2900, "target": 38000, "errors": None, "packed": None},
        {"name": "Dan W.", "role": "CS / upsell", "type": "rev", "driven": 14200, "cost": 2400, "target": 18000, "errors": None, "packed": None},
        {"name": "Liam H.", "role": "Picker / packer", "type": "ops", "driven": None, "cost": 2200, "target": None, "errors": 0.6, "packed": 1480},
        {"name": "Sofia K.", "role": "Picker / packer", "type": "ops", "driven": None, "cost": 2150, "target": None, "errors": 2.9, "packed": 1120},
        {"name": "Jon M.", "role": "Picker / packer", "type": "ops", "driven": None, "cost": 2100, "target": None, "errors": 4.7, "packed": 820},
    ],
    "ppCostTrend": [3.92, 3.81, 3.74, 3.68, 3.55, 3.45],
    "perfectOrderRate": 94.2,
    "dispatchSLA": [
        {"window": "Same-day (before 2pm)", "target": 95, "actual": 91},
        {"window": "Next-day", "target": 98, "actual": 96},
        {"window": "48-hour (peak)", "target": 99, "actual": 97},
    ],
    "returns": [
        {"reason": "Wrong item sent (mis-pick)", "orders": 38, "cost": 1120},
        {"reason": "Damaged in transit", "orders": 24, "cost": 890},
        {"reason": "Not as expected", "orders": 61, "cost": 1640},
        {"reason": "Sizing", "orders": 47, "cost": 980},
    ],
    "reinvest": {
        "presets": {"conservative": 30, "neutral": 60, "aggressive": 100},
        "marginalFactor": 0.80,
        "allocation": [
            {"name": "Google", "weight": 42},
            {"name": "Meta", "weight": 40},
            {"name": "Email", "weight": 13, "marginalRoas": 4.0},
            {"name": "TikTok", "weight": 5},
        ],
    },
    "breakeven": {
        "globalMargin": 61.5,
        "targetNetMargin": 15,
        "platformMargin": {"Meta": 61.5, "Google": 61.5, "TikTok": 54.0, "Email": 64.0, "Organic": 61.5},
    },
    "lostSalesRevenue": 4200,
    "benchmarks": {"fulfilmentCpo": 10.50},
    "retail": {
        "revenue": 62000, "cogs": 31000, "distribution": 2400, "tradeMarketing": 3200,
        "commission": 5800, "salesRep": 4500, "overheadAllocation": 6000,
        "trend": [38000, 42000, 45000, 49000, 54000, 62000],
    },
    "quarterly": {
        "monthly": [
            {"m": "Jan", "v": 212}, {"m": "Feb", "v": 268}, {"m": "Mar", "v": 246}, {"m": "Apr", "v": 252},
            {"m": "May", "v": 274}, {"m": "Jun", "v": 311}, {"m": "Jul", "v": 216}, {"m": "Aug", "v": 207},
            {"m": "Sep", "v": 261}, {"m": "Oct", "v": 303}, {"m": "Nov", "v": 412}, {"m": "Dec", "v": 444},
        ],
        "quarters": [
            {"q": "Q1", "months": "Jan–Mar", "dtcRev": 620000, "retailRev": 106000, "adSpend": 212000, "newCust": 5400, "topProduct": "Cuban Link Chain", "topReason": "Valentine's gifting", "topRev": 84000},
            {"q": "Q2", "months": "Apr–Jun", "dtcRev": 712000, "retailRev": 125000, "adSpend": 225000, "newCust": 5900, "topProduct": "Onyx Signet Ring", "topReason": "Father's Day", "topRev": 96000},
            {"q": "Q3", "months": "Jul–Sep", "dtcRev": 580000, "retailRev": 104000, "adSpend": 201000, "newCust": 4800, "topProduct": "Matte Steel Bracelet", "topReason": "Summer everyday", "topRev": 71000},
            {"q": "Q4", "months": "Oct–Dec", "dtcRev": 980000, "retailRev": 179000, "adSpend": 291000, "newCust": 8200, "topProduct": "Obsidian Gift Set", "topReason": "Christmas peak", "topRev": 148000},
        ],
    },
    "marketplaces": {
        "fulfilPerUnit": 7.30,
        "cogsRate": 0.24,
        "dtcFeePct": 2.4,
        "overheadAllocation": 4500,
        "trend": [28000, 30500, 32000, 34800, 36500, 38200],
        "channels": [
            {"name": "Etsy", "feePct": 9.0, "fixedFee": 0.20, "rev": 18400, "units": 240, "topProduct": "Matte Steel Bracelet"},
            {"name": "NOTHS", "feePct": 27, "fixedFee": 0, "rev": 11200, "units": 132, "topProduct": "Onyx Signet Ring"},
            {"name": "Debenhams", "feePct": 22, "fixedFee": 0, "rev": 8600, "units": 96, "topProduct": "Cuban Link Chain"},
        ],
        "catalogue": [
            {"name": "Onyx Signet Ring", "cost": 24, "prices": {"DTC": 79, "Etsy": 82, "NOTHS": 85, "Debenhams": 84}},
            {"name": "Cuban Link Chain", "cost": 31, "prices": {"DTC": 89, "Etsy": 92, "NOTHS": 95, "Debenhams": 94}},
            {"name": "Matte Steel Bracelet", "cost": 12, "prices": {"DTC": 38, "Etsy": 39, "NOTHS": 42, "Debenhams": 41}},
            {"name": "Beaded Bracelet", "cost": 11, "prices": {"DTC": 28, "Etsy": 29, "NOTHS": 30, "Debenhams": 29}},
            {"name": "Stud Earrings", "cost": 7, "prices": {"DTC": 18, "Etsy": 19, "NOTHS": 16, "Debenhams": 20}},
            {"name": "Enamel Pin", "cost": 6, "prices": {"DTC": 14, "Etsy": 14, "NOTHS": 14, "Debenhams": 15}},
        ],
    },
    "adPlaybook": {
        "months": [
            {"m": "Jan", "spend": 60, "roas": 1.5, "note": "Post-Christmas slump", "action": "cut"},
            {"m": "Feb", "spend": 80, "roas": 3.3, "note": "Valentine's gifting", "action": "scale"},
            {"m": "Mar", "spend": 66, "roas": 2.4, "note": "Cooldown", "action": "hold"},
            {"m": "Apr", "spend": 64, "roas": 2.6, "note": "Steady", "action": "hold"},
            {"m": "May", "spend": 72, "roas": 2.9, "note": "Build to Father's Day", "action": "scale"},
            {"m": "Jun", "spend": 84, "roas": 3.3, "note": "Father's Day peak", "action": "scale"},
            {"m": "Jul", "spend": 58, "roas": 1.5, "note": "Post-event + summer lull", "action": "cut"},
            {"m": "Aug", "spend": 55, "roas": 1.8, "note": "Summer lull", "action": "hold"},
            {"m": "Sep", "spend": 64, "roas": 2.5, "note": "Autumn pick-up", "action": "hold"},
            {"m": "Oct", "spend": 74, "roas": 2.8, "note": "Pre-Christmas build", "action": "scale"},
            {"m": "Nov", "spend": 96, "roas": 3.6, "note": "Black Friday", "action": "scale"},
            {"m": "Dec", "spend": 104, "roas": 3.3, "note": "Christmas peak", "action": "scale"},
        ],
        "weakestChannel": "TikTok",
        "strongestChannel": "Email",
    },
    "customers": {
        "total": 18400,
        "segments": [
            {"name": "Champions", "cust": 8, "rev": 31, "desc": "Recent, frequent, high spend — your VIPs", "c": GOLD},
            {"name": "Loyal", "cust": 14, "rev": 24, "desc": "Buy regularly with a solid AOV", "c": POS},
            {"name": "Promising / new", "cust": 22, "rev": 14, "desc": "First or second order — nurture into loyalty", "c": STEEL},
            {"name": "At risk", "cust": 16, "rev": 12, "desc": "Haven't bought in a while — win them back", "c": AMBER},
            {"name": "One-time", "cust": 40, "rev": 19, "desc": "Single purchase, never returned", "c": MUTED},
        ],
        "age": [{"b": "18–24", "p": 14}, {"b": "25–34", "p": 38}, {"b": "35–44", "p": 27}, {"b": "45–54", "p": 14}, {"b": "55+", "p": 7}],
        "buyer": [{"g": "Self-purchase (men)", "p": 58, "c": STEEL}, {"g": "Gifting (mostly women)", "p": 42, "c": VIOLET}],
        "locations": [{"c": "London", "p": 24}, {"c": "Manchester", "p": 9}, {"c": "Birmingham", "p": 7}, {"c": "Glasgow", "p": 6}, {"c": "Leeds", "p": 5}, {"c": "Rest of UK", "p": 49}],
        "motivation": [
            {"r": "Self-treat / personal style", "p": 46, "c": GOLD},
            {"r": "Gift for a partner", "p": 28, "c": VIOLET},
            {"r": "Gift — Father's Day / birthday", "p": 18, "c": STEEL},
            {"r": "Special occasion", "p": 8, "c": AMBER},
        ],
        "personas": [
            {"name": "The Self-Expressor", "share": "~40% of customers", "who": "25–34, urban, style-led, lives on TikTok & Instagram", "why": "Buys to express identity — layers chains and rings, follows trends. Repeats if you keep newness and quality coming.", "channel": "Meta · TikTok", "aov": "£68"},
            {"name": "The Gift-Giver", "share": "~30%", "who": "Partners & family, spikes around events", "why": "Buying for the men in their life at Valentine's, Father's Day and birthdays. Wants easy returns, gift packaging and a safe bet.", "channel": "Google · Meta", "aov": "£82"},
            {"name": "The Collector", "share": "~15%", "who": "35–44, higher income, considered buyer", "why": "Buys signet & heirloom pieces — fewer orders, higher AOV, low price sensitivity. Your most loyal, best-LTV customer.", "channel": "Email · Organic", "aov": "£110"},
        ],
    },
    "amazonKpis": {
        "ccc": {"dso": 2, "dpo": 30},
        "newCAC": 39.5,
        "scorecard": [
            {"group": "Financial & growth", "rows": [
                {"m": "Marketing efficiency ratio (MER)", "v": "3.03x", "t": "≥ 3.0x", "s": "good"},
                {"m": "Contribution margin (CM2)", "v": "26.4%", "t": "≥ 25%", "s": "good"},
                {"m": "CAC payback", "v": "0.9 orders", "t": "≤ 2 orders", "s": "good"},
                {"m": "Cash conversion cycle", "v": "83 days", "t": "≤ 60 days", "s": "warn"},
                {"m": "Month-on-month growth", "v": "+12.4%", "t": "≥ 10%", "s": "good"},
            ]},
            {"group": "Customer", "rows": [
                {"m": "Repeat-purchase rate", "v": "28.4%", "t": "≥ 30%", "s": "warn"},
                {"m": "Net Promoter Score", "v": "62", "t": "≥ 50", "s": "good"},
                {"m": "Average review rating", "v": "4.7 / 5", "t": "≥ 4.5", "s": "good"},
                {"m": "Contacts per order (CS load)", "v": "9.1%", "t": "≤ 8%", "s": "warn"},
                {"m": "New vs returning revenue", "v": "63 / 37", "t": "balance", "s": "neutral"},
            ]},
            {"group": "Demand & inventory", "rows": [
                {"m": "In-stock / availability rate", "v": "96.4%", "t": "≥ 98%", "s": "warn"},
                {"m": "Lost sales from stockouts", "v": "£4,200", "t": "£0", "s": "warn"},
                {"m": "GMROI (margin per £ of stock)", "v": "9.3", "t": "≥ 3.0", "s": "good"},
                {"m": "Inventory turns (annualised)", "v": "3.3x", "t": "≥ 4.0x", "s": "warn"},
                {"m": "Demand forecast accuracy", "v": "82%", "t": "≥ 85%", "s": "warn"},
            ]},
            {"group": "Fulfilment & quality", "rows": [
                {"m": "Perfect-order rate", "v": "94.2%", "t": "≥ 97%", "s": "warn"},
                {"m": "Order defect rate (ODR)", "v": "1.8%", "t": "≤ 1%", "s": "bad"},
                {"m": "On-time dispatch", "v": "94.7%", "t": "≥ 98%", "s": "warn"},
                {"m": "Units per hour (packing)", "v": "42", "t": "≥ 50", "s": "warn"},
                {"m": "Fulfilment cost / order", "v": "£11.29", "t": "≤ £10.50", "s": "warn"},
                {"m": "Return rate", "v": "5.0%", "t": "≤ 4%", "s": "warn"},
                {"m": "Damage rate", "v": "0.7%", "t": "≤ 0.5%", "s": "warn"},
            ]},
        ],
    },
}

# ── Derived totals ──
def f0(n): return f"£{round(n):,}"
def f1(n): return f"£{n:,.1f}"
def pct(n): return f"{n:.1f}%"

netRev = D["grossRevenue"] - D["refunds"]
cogsTotal = D["cogs"] + D["shippingOut"] + D["packaging"] + D["paymentFees"] + D["pickPackLabour"]
grossProfit = netRev - cogsTotal
marketing = D["metaSpend"] + D["googleSpend"] + D["tiktokSpend"] + D["emailPlatform"] + D["influencer"]
contribution = grossProfit - marketing
overheads = D["salariesOther"] + D["rent"] + D["software"] + D["utilities"] + D["insurance"]
netProfit = contribution - overheads
aov = D["grossRevenue"] / D["orders"]
grossMarginPct = grossProfit / netRev * 100
netMarginPct = netProfit / netRev * 100
contributionPerOrder = contribution / D["orders"]
ltvCac = D["ltv"] / D["blendedCAC"]
invTurns = (D["cogs"] * 12) / D["stockValue"]

# ── Plotly layout defaults ──
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", size=11, color=MUTED),
    margin=dict(l=40, r=20, t=30, b=40),
    xaxis=dict(gridcolor=LINE, zerolinecolor=LINE),
    yaxis=dict(gridcolor=LINE, zerolinecolor=LINE),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
)

def styled_plotly(fig, height=320):
    fig.update_layout(**PLOT_LAYOUT, height=height)
    return fig

def mini_cards(items):
    cols = st.columns(len(items))
    for col, m in zip(cols, items):
        col.markdown(f"""<div class="mini-card"><div class="l">{m[0]}</div><div class="v">{m[1]}</div><div class="s">{m[2]}</div></div>""", unsafe_allow_html=True)

def pill(status, label):
    cls = {"win": "pill-win", "ok": "pill-ok", "dead": "pill-dead", "watch": "pill-watch"}.get(status, "pill-ok")
    return f'<span class="pill {cls}">{label}</span>'

def mp_aggregate():
    MP = D["marketplaces"]
    fulfil = MP["fulfilPerUnit"]
    rev = units = fees = 0
    for c in MP["channels"]:
        rev += c["rev"]; units += c["units"]
        fees += c["rev"] * c["feePct"] / 100 + c["units"] * c["fixedFee"]
    cogs = rev * MP["cogsRate"]
    ful = units * fulfil
    gross = rev - cogs - ful - fees
    overhead = MP["overheadAllocation"]
    net = gross - overhead
    return {"rev": rev, "units": units, "cogs": cogs, "ful": ful, "fees": fees, "gross": gross, "overhead": overhead, "net": net}

# ══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""<div style="display:flex;align-items:center;gap:11px;padding:0 6px 22px;border-bottom:1px solid #262E38;margin-bottom:16px">
        <div style="width:34px;height:34px;border-radius:9px;background:linear-gradient(140deg,#C8A55B,#7a5f2a);display:grid;place-items:center;font-family:'Space Grotesk';font-weight:700;color:#1a1408;font-size:18px">F</div>
        <div><b style="font-family:'Space Grotesk';font-weight:600;letter-spacing:.5px;font-size:16px;color:#E6E9EE">FORGE</b><br><small style="color:#5B6573;font-size:10.5px;letter-spacing:1.5px;text-transform:uppercase">Command Centre</small></div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='font-size:10px;letter-spacing:1.4px;text-transform:uppercase;color:#5B6573;padding:8px 0 4px'>Money</div>", unsafe_allow_html=True)
    page = st.radio("", [
        "◆ Command Overview",
        "↯ Where we're leaking",
        "⤴ Reinvestment Planner",
        "£ Online (DTC) P&L",
        "◰ Marketplace P&L",
        "∑ Combined P&L",
        "▲ Acquisition",
        "⚖ Break-even ROAS",
        "∞ CAC & LTV",
        "↻ Retention",
        "☺ Customers",
        "◈ Products & Launches",
        "◰ Marketplaces",
        "▦ Inventory",
        "☖ Staff & Targets",
        "⚙ Pick · Pack · Dispatch",
        "◷ Quarterly trends",
        "⎈ Ad spend playbook",
        "★ Amazon-grade KPIs",
    ], label_visibility="collapsed")

    st.markdown("""<div style="margin-top:20px;padding:12px;border:1px solid #262E38;border-radius:11px;background:#161B22;font-size:11px;color:#8A94A3">
        Numbers shown are sample figures for a scaling DTC brand. Edit the <b style="color:#C8A55B">DATA</b> block to plug in your real numbers.</div>""", unsafe_allow_html=True)

# ── KPI Ribbon (always shown) ──
kpi_items = [
    ("Net revenue", f0(netRev), "▲ +12.4% vs May", True, GOLD),
    ("Net profit", f0(netProfit), f"▲ {pct(netMarginPct)} margin", True, POS),
    ("Gross margin", pct(grossMarginPct), "after all COGS", True, STEEL),
    ("Contribution / order", f1(contributionPerOrder), "after ads", True, VIOLET),
    ("Blended ROAS", f"{D['grossRevenue']/marketing:.2f}x", f"{f0(marketing)} spent", False, AMBER),
    ("LTV : CAC", f"{ltvCac:.1f}x", "target 3.0x+", False, POS if ltvCac >= 3 else AMBER),
]

cols = st.columns(6)
for col, (label, value, delta, is_up, color) in zip(cols, kpi_items):
    delta_cls = "up" if is_up else "down"
    col.markdown(f"""<div class="kpi-card" style="border-top: 2px solid {color}">
        <div class="label">{label}</div><div class="value">{value}</div>
        <div class="delta {delta_cls}">{delta}</div></div>""", unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════
# SECTIONS
# ══════════════════════════════════════════════════════════════════════════

if page == "◆ Command Overview":
    st.title("Command Overview")
    st.caption(f"The single screen where you see every penny in and out — {D['month']}")

    c1, c2 = st.columns([1.6, 1])
    with c1:
        st.subheader("Profit waterfall — where the money goes")
        st.caption("Gross revenue stepped down through every cost to net profit")
        steps = [
            ("Net revenue", netRev, "start"), ("Product cost", -D["cogs"], ""),
            ("Shipping", -D["shippingOut"], ""), ("Pick & pack", -D["pickPackLabour"], ""),
            ("Pack + fees", -(D["packaging"]+D["paymentFees"]), ""), ("Marketing", -marketing, ""),
            ("Overheads", -overheads, ""), ("Net profit", netProfit, "end"),
        ]
        labels = [s[0] for s in steps]
        measures = []
        values = []
        for s in steps:
            if s[2] == "start":
                measures.append("absolute"); values.append(s[1])
            elif s[2] == "end":
                measures.append("total"); values.append(0)
            else:
                measures.append("relative"); values.append(s[1])
        fig = go.Figure(go.Waterfall(
            x=labels, y=values, measure=measures,
            increasing=dict(marker_color=POS), decreasing=dict(marker_color=NEG),
            totals=dict(marker_color=GOLD),
            connector=dict(line=dict(color=LINE, width=1)),
            textposition="outside",
            text=[f"£{abs(v):,.0f}" for v in [netRev, D["cogs"], D["shippingOut"], D["pickPackLabour"], D["packaging"]+D["paymentFees"], marketing, overheads, netProfit]],
            textfont=dict(size=9, color=MUTED),
        ))
        st.plotly_chart(styled_plotly(fig, 350), use_container_width=True)
        st.markdown(f'<div class="note">Read left→right: each red step is money leaving the business. The two tallest red steps are your biggest leaks — fix those first.</div>', unsafe_allow_html=True)

    with c2:
        st.subheader("Money-leak alerts")
        st.caption("Auto-flagged the moment a metric breaches target")
        tt = next(c for c in D["channels"] if c["name"] == "TikTok")
        tr = tt["rev"] / tt["spend"]
        ttM = D["breakeven"]["platformMargin"].get("TikTok", grossMarginPct) / 100
        ttBE = 1 / ttM
        ttProfit = tt["rev"] * ttM - tt["spend"]
        worst_staff = max((s for s in D["staff"] if s["type"] == "ops"), key=lambda s: s["errors"])

        alerts = []
        if tr < ttBE * 1.3:
            alerts.append(("crit" if ttProfit <= 0 else "warn", f"TikTok at {tr:.2f}x vs {ttBE:.2f}x break-even",
                f"At its {ttM*100:.0f}% product margin, {f0(tt['spend'])} of spend returned only {'+'if ttProfit>=0 else '−'}{f0(abs(ttProfit))} profit.",
                "Fix → pause the bottom ad sets, test UGC hooks, or shift budget to Google."))
        if ltvCac < 3:
            alerts.append(("warn", f"LTV:CAC at {ltvCac:.1f}x — under the 3.0x safety line",
                "Growth is profitable but thin. A small CAC rise could tip acquisition into a loss.",
                "Fix → lift repeat rate via email flows; raise AOV with bundles."))
        if worst_staff["errors"] > 3:
            alerts.append(("crit", f"{worst_staff['name']}: {worst_staff['errors']}% packing error rate",
                "Mis-sends drive returns & re-ships. Each mis-pick costs ~£29.",
                "Fix → scan-to-pack verification + retraining before peak."))
        alerts.append(("warn", f"{f0(D['deadStockValue'])} frozen in dead stock",
            "Cash tied up in poor sellers can't buy winners or fund ads.",
            "Fix → see liquidation plan in Inventory."))
        email_ch = next(c for c in D["channels"] if c["name"] == "Email")
        alerts.append(("good", f"Email driving {f0(email_ch['rev'])} at 45x ROAS",
            "Your cheapest, highest-margin channel is compounding. Protect and scale it.", ""))

        alert_details = {
            0: {"impact": f"TikTok spent {f0(tt['spend'])} and earned {f0(tt['rev'])}. At {ttM*100:.0f}% product margin, that's only {f0(tt['rev']*ttM)} gross profit — barely covering the ad spend.",
                "breakdown": [("TikTok spend", f0(tt['spend'])), ("TikTok revenue", f0(tt['rev'])), ("Gross profit from TikTok", f0(tt['rev']*ttM)), ("Net after ad cost", f"{'+'if ttProfit>=0 else '−'}{f0(abs(ttProfit))}"), ("Break-even ROAS needed", f"{ttBE:.2f}x"), ("Actual ROAS", f"{tr:.2f}x")],
                "actions": ["Pause ad sets with ROAS below 1.5x", "Test 3 new UGC-style creatives", "Shift 50% of TikTok budget to Google (3.4% CVR vs 1.4%)", "Set a 14-day review window before scaling back up"]},
            1: {"impact": f"Your LTV of {f1(D['ltv'])} divided by CAC of {f1(D['blendedCAC'])} gives {ltvCac:.1f}x. The danger zone starts below 2.0x.",
                "breakdown": [("Customer LTV", f1(D['ltv'])), ("Blended CAC", f1(D['blendedCAC'])), ("LTV:CAC ratio", f"{ltvCac:.1f}x"), ("Repeat rate", f"{D['repeatRate']}%"), ("Avg orders/lifetime", f"{D['avgOrdersLifetime']:.1f}")],
                "actions": ["Add a post-purchase upsell flow (target: +£12 AOV)", "Launch a win-back email to the 16% at-risk segment", "Test bundle offers to lift repeat rate from 28% → 32%"]},
            2: {"impact": f"{worst_staff['name']} packed {worst_staff['packed']} orders with a {worst_staff['errors']}% error rate. That's ~{round(worst_staff['packed']*worst_staff['errors']/100)} mis-sends at ~£29 each = {f0(round(worst_staff['packed']*worst_staff['errors']/100*29))} in re-ship costs.",
                "breakdown": [("Orders packed", f"{worst_staff['packed']}"), ("Error rate", f"{worst_staff['errors']}%"), ("Estimated mis-sends", f"{round(worst_staff['packed']*worst_staff['errors']/100)}"), ("Cost per mis-send", "~£29"), ("Monthly cost of errors", f"~{f0(round(worst_staff['packed']*worst_staff['errors']/100*29))}")],
                "actions": ["Implement scan-to-pack barcode verification", "Pair with Liam H. (0.6% error rate) for buddy training", "Set a 2-week target: reduce to <2% or reassign"]},
            3: {"impact": f"£{D['deadStockValue']:,} is locked in {len(D['dead'])} SKUs that aren't selling. That's cash that could buy best-sellers or fund ads.",
                "breakdown": [(d["sku"], f"{f0(d['value'])} · {d['units']} units · {d['age']}d old") for d in D["dead"]],
                "actions": [f"{d['sku']}: {d['plan']}" for d in D["dead"]]},
            4: {"impact": f"Email generated {f0(email_ch['rev'])} from just {f0(email_ch['spend'])} platform cost. That's a {email_ch['rev']/email_ch['spend']:.0f}x return — your most efficient channel by far.",
                "breakdown": [(e["name"], f"{f0(e['rev'])} ({e['type']})") for e in D["email"]],
                "actions": ["Increase send frequency on the welcome flow", "A/B test subject lines on campaigns", "Add a VIP early-access flow for Champions segment"]},
        }

        for idx, (lv, t, d, fix) in enumerate(alerts):
            icon = {"crit": "🔴", "warn": "🟡", "good": "🟢"}.get(lv, "⚪")
            with st.expander(f"{icon} {t}", expanded=False):
                st.markdown(f"**Summary:** {d}")
                if fix:
                    st.markdown(f"**Quick fix:** {fix}")
                det = alert_details.get(idx, {})
                if det.get("impact"):
                    st.markdown(f"**Full impact analysis:**")
                    st.info(det["impact"])
                if det.get("breakdown"):
                    st.markdown("**Detailed breakdown:**")
                    bk_df = pd.DataFrame(det["breakdown"], columns=["Metric", "Value"])
                    st.dataframe(bk_df, hide_index=True, use_container_width=True)
                if det.get("actions"):
                    st.markdown("**Action plan:**")
                    for ai, action in enumerate(det["actions"], 1):
                        st.markdown(f"{ai}. {action}")

    st.markdown("#### Revenue engine")
    c1, c2 = st.columns([1.6, 1])
    with c1:
        st.subheader("What's driving revenue")
        fig = go.Figure(go.Bar(
            x=[c["name"] for c in D["channels"]], y=[c["rev"] for c in D["channels"]],
            marker_color=[c["colour"] for c in D["channels"]], text=[f"£{c['rev']/1000:.0f}k" for c in D["channels"]],
            textposition="outside", textfont=dict(size=10, color=MUTED),
        ))
        fig.update_layout(showlegend=False)
        st.plotly_chart(styled_plotly(fig, 300), use_container_width=True)
    with c2:
        st.subheader("Channel efficiency")
        df = pd.DataFrame([{
            "Channel": c["name"], "Revenue": f0(c["rev"]),
            "ROAS": f"{c['rev']/c['spend']:.2f}x" if c["spend"] else "∞",
            "Share": f"{c['rev']/D['grossRevenue']*100:.0f}%"
        } for c in D["channels"]])
        st.dataframe(df, hide_index=True, use_container_width=True)

    st.markdown("#### Channel deep-dive")
    selected_ch = st.selectbox("Select a channel to explore", [c["name"] for c in D["channels"]], key="overview_channel")
    ch = next(c for c in D["channels"] if c["name"] == selected_ch)
    ch_roas = ch["rev"] / ch["spend"] if ch["spend"] else float("inf")
    ch_cac = ch["spend"] / ch["newCust"] if ch["spend"] and ch["newCust"] else 0
    ch_aov = ch["rev"] / ch["orders"]
    ch_margin = D["breakeven"]["platformMargin"].get(ch["name"], grossMarginPct) / 100
    ch_profit = ch["rev"] * ch_margin - ch["spend"]

    cc1, cc2, cc3, cc4 = st.columns(4)
    cc1.metric("Revenue", f0(ch["rev"]))
    cc2.metric("Spend", f0(ch["spend"]) if ch["spend"] else "£0")
    cc3.metric("ROAS", f"{ch_roas:.2f}x" if ch["spend"] else "∞")
    cc4.metric("Profit after ads", f"{'+'if ch_profit>=0 else '−'}{f0(abs(ch_profit))}" if ch["spend"] else f"+{f0(ch['rev']*ch_margin)}")

    cc1, cc2 = st.columns(2)
    with cc1:
        st.markdown(f"""
        | Metric | Value |
        |--------|-------|
        | Orders | {ch['orders']:,} |
        | New customers | {ch['newCust']:,} |
        | AOV | {f1(ch_aov)} |
        | CTR | {ch['ctr']}% |
        | CVR | {ch['cvr']}% |
        | CAC | {f1(ch_cac) if ch_cac else 'N/A (free)'} |
        | Share of revenue | {ch['rev']/D['grossRevenue']*100:.1f}% |
        """)
    with cc2:
        fig = go.Figure(go.Pie(
            labels=["This channel", "Rest"],
            values=[ch["rev"], D["grossRevenue"] - ch["rev"]],
            marker=dict(colors=[ch["colour"], LINE]), hole=.65,
            textinfo="percent", textfont=dict(size=12),
        ))
        fig.update_layout(title=f"{ch['name']}'s share of total revenue", showlegend=False)
        st.plotly_chart(styled_plotly(fig, 220), use_container_width=True)

    st.markdown("#### Health at a glance")
    mini_cards([
        ("AOV", f1(aov), "avg order value"),
        ("Contribution / order", f1(contributionPerOrder), "after ad spend"),
        ("Perfect-order rate", f"{D['perfectOrderRate']}%", "on-time, accurate, kept"),
        ("Inventory turns", f"{invTurns:.1f}x", "annualised"),
    ])

elif page == "↯ Where we're leaking":
    st.title("Where we're leaking")
    st.caption("Every money leak ranked by what it costs you — with the fix and the £ to recover")

    gm = grossMarginPct / 100
    leaks = []
    adWaste = sum(p["spend"] - p["rev"] * (p["margin"] / 100) for p in D["wasted"])
    leaks.append({"type": "bleed", "name": "Wasted ad spend on losing products", "amount": adWaste,
        "cause": f"{len(D['wasted'])} products spending more than their margin returns.",
        "fix": "Pause or rework these ad sets — the saving drops straight onto net profit."})
    tt = next(c for c in D["channels"] if c["name"] == "TikTok")
    ttM = D["breakeven"]["platformMargin"].get("TikTok", grossMarginPct) / 100
    ttProfit = tt["rev"] * ttM - tt["spend"]
    g = next(c for c in D["channels"] if c["name"] == "Google")
    gRoas = g["rev"] / g["spend"]; gM = D["breakeven"]["platformMargin"].get("Google", grossMarginPct) / 100
    reallocProfit = tt["spend"] * gRoas * gM - tt["spend"]
    leaks.append({"type": "table", "name": "TikTok spend barely clearing cost", "amount": reallocProfit - ttProfit,
        "cause": f"{f0(tt['spend'])} on TikTok made just {f0(ttProfit)} at its {ttM*100:.0f}% margin.",
        "fix": "Fix TikTok creative & targeting, or move the budget to Google."})
    stockoutProfit = D["lostSalesRevenue"] * gm
    leaks.append({"type": "bleed", "name": "Lost sales from stockouts", "amount": stockoutProfit,
        "cause": f"{f0(D['lostSalesRevenue'])} of demand for winners you couldn't fulfil.",
        "fix": "Tighten reorder points on best-sellers."})
    varFulfil = D["shippingOut"] + D["pickPackLabour"] + D["packaging"] + D["paymentFees"]
    cpo = varFulfil / D["orders"]; tgtCpo = D["benchmarks"]["fulfilmentCpo"]
    fulfilOver = max(0, (cpo - tgtCpo) * D["orders"])
    leaks.append({"type": "bleed", "name": "Fulfilment cost above benchmark", "amount": fulfilOver,
        "cause": f"{f1(cpo)}/order to fulfil vs a {f1(tgtCpo)} target.",
        "fix": "Renegotiate courier rates, trim packaging cost."})
    mispick = next((r for r in D["returns"] if "mis-pick" in r["reason"].lower()), None)
    if mispick:
        leaks.append({"type": "bleed", "name": "Preventable mis-sends", "amount": mispick["cost"],
            "cause": f"{mispick['orders']} wrong items shipped.", "fix": "Scan-to-pack verification."})
    leaks.sort(key=lambda l: -l["amount"])

    bleed = sum(l["amount"] for l in leaks if l["type"] == "bleed")
    onTable = sum(l["amount"] for l in leaks if l["type"] == "table")
    trapped = D["deadStockValue"]
    potential = netProfit + bleed + onTable

    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="hero-card" style="border-top:2px solid {NEG}"><div style="font-size:11px;letter-spacing:.7px;text-transform:uppercase;color:{FAINT}">Active monthly bleed</div><div style="font-size:30px;font-weight:700;font-family:JetBrains Mono;color:{NEG};margin-top:8px">{f0(bleed)}</div><div style="font-size:11.5px;color:{MUTED};margin-top:4px">cash you lose or never earn, every month</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="hero-card" style="border-top:2px solid {AMBER}"><div style="font-size:11px;letter-spacing:.7px;text-transform:uppercase;color:{FAINT}">Profit left on the table</div><div style="font-size:30px;font-weight:700;font-family:JetBrains Mono;color:{AMBER};margin-top:8px">{f0(onTable)}</div><div style="font-size:11.5px;color:{MUTED};margin-top:4px">underperforming spend you can redeploy</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="hero-card" style="border-top:2px solid {STEEL}"><div style="font-size:11px;letter-spacing:.7px;text-transform:uppercase;color:{FAINT}">Trapped capital</div><div style="font-size:30px;font-weight:700;font-family:JetBrains Mono;color:{STEEL};margin-top:8px">{f0(trapped)}</div><div style="font-size:11.5px;color:{MUTED};margin-top:4px">cash frozen in dead stock to release</div></div>', unsafe_allow_html=True)

    st.markdown(f"Plug these and net profit could climb from **{f0(netProfit)}** to **~{f0(potential)}** a month.")

    st.markdown("#### Ranked by what it's costing you")
    for i, l in enumerate(leaks):
        lc = NEG if l["type"] == "bleed" else AMBER
        tag_txt = "🔴 Cash bleed" if l["type"] == "bleed" else "🟡 Left on table"
        with st.expander(f"**#{i+1}** {l['name']} — **{f0(l['amount'])}/mo** {tag_txt}", expanded=False):
            st.markdown(f"**What's happening:** {l['cause']}")
            st.markdown(f"**Fix:** {l['fix']}")
            st.markdown(f"**Monthly impact:** {f0(l['amount'])}")
            pct_of_profit = l['amount'] / netProfit * 100 if netProfit else 0
            st.progress(min(pct_of_profit / 100, 1.0), text=f"{pct_of_profit:.0f}% of current net profit")
            if "ad spend" in l["name"].lower() or "wasted" in l["name"].lower():
                st.markdown("**Products losing money on ads:**")
                wdf = pd.DataFrame([{"Product": p["name"], "Revenue": f0(p["rev"]), "Spend": f0(p["spend"]), "ROAS": f"{p['roas']}x", "Margin": f"{p['margin']}%", "Net loss": f"−{f0(p['spend'] - p['rev'] * p['margin']/100)}"} for p in D["wasted"]])
                st.dataframe(wdf, hide_index=True, use_container_width=True)
            elif "tiktok" in l["name"].lower():
                st.markdown("**TikTok vs other channels:**")
                comp = [c for c in D["channels"] if c["spend"] > 0]
                cdf = pd.DataFrame([{"Channel": c["name"], "Spend": f0(c["spend"]), "Revenue": f0(c["rev"]), "ROAS": f"{c['rev']/c['spend']:.2f}x", "CVR": f"{c['cvr']}%"} for c in comp])
                st.dataframe(cdf, hide_index=True, use_container_width=True)
            elif "stockout" in l["name"].lower():
                st.markdown("**Best-sellers at risk of stockout:**")
                risky = [i for i in D["inv"] if i["days"] < 20 and i["status"] == "win"]
                if risky:
                    rdf = pd.DataFrame([{"SKU": r["sku"], "Units left": r["units"], "Days cover": f"{r['days']}d", "Sell-through": f"{r['sellthru']}%"} for r in risky])
                    st.dataframe(rdf, hide_index=True, use_container_width=True)
            elif "fulfilment" in l["name"].lower():
                st.markdown("**Cost per order breakdown:**")
                cpo_items = [("Outbound shipping", D["shippingOut"]/D["orders"]), ("Pick & pack", D["pickPackLabour"]/D["orders"]), ("Packaging", D["packaging"]/D["orders"]), ("Payment fees", D["paymentFees"]/D["orders"])]
                fdf = pd.DataFrame([{"Component": c[0], "Per order": f1(c[1])} for c in cpo_items])
                st.dataframe(fdf, hide_index=True, use_container_width=True)
            elif "mis-send" in l["name"].lower():
                st.markdown("**All return reasons:**")
                rdf = pd.DataFrame([{"Reason": r["reason"], "Orders": r["orders"], "Cost": f0(r["cost"])} for r in D["returns"]])
                st.dataframe(rdf, hide_index=True, use_container_width=True)

    st.markdown("#### Leak ranking")
    fig = go.Figure(go.Bar(
        y=[l["name"] for l in leaks], x=[l["amount"] for l in leaks], orientation="h",
        marker_color=[NEG if l["type"] == "bleed" else AMBER for l in leaks],
        text=[f"£{l['amount']:,.0f}/mo" for l in leaks], textposition="outside",
    ))
    fig.update_layout(showlegend=False)
    st.plotly_chart(styled_plotly(fig, 300), use_container_width=True)

    st.markdown("#### What plugging them does to net profit")
    fig = go.Figure(go.Bar(
        x=["Net profit today", "Bleed plugged", "+ spend redeployed", "Potential"],
        y=[netProfit, netProfit + bleed, potential, potential],
        marker_color=[GOLD, "#cf8f5a", POS, POS],
        text=[f0(v) for v in [netProfit, netProfit + bleed, potential, potential]],
        textposition="outside",
    ))
    fig.update_layout(showlegend=False)
    st.plotly_chart(styled_plotly(fig, 300), use_container_width=True)

elif page == "⤴ Reinvestment Planner":
    st.title("Reinvestment Planner")
    st.caption(f"You made **{f0(netProfit)}** in net profit. Here's exactly what to reinvest.")

    cfg = D["reinvest"]
    mf = cfg["marginalFactor"]
    gm = grossMarginPct / 100
    breakeven_roas = 1 / gm

    def roas_of(name):
        c = next((ch for ch in D["channels"] if ch["name"] == name), None)
        return c["rev"] / c["spend"] if c and c["spend"] else 0

    def project(pct_val):
        reinvestAmt = netProfit * (pct_val / 100)
        incRev = 0; rows = []
        for a in cfg["allocation"]:
            spend = reinvestAmt * (a["weight"] / 100)
            eff = a.get("marginalRoas", roas_of(a["name"]) * mf)
            rev = spend * eff; incRev += rev
            rows.append({"name": a["name"], "weight": a["weight"], "spend": spend, "eff": eff, "rev": rev})
        incGP = incRev * gm
        reinvestProfit = incGP - reinvestAmt
        banked = netProfit - reinvestAmt
        newBudget = marketing + reinvestAmt
        eff_total = incRev / reinvestAmt if reinvestAmt else 0
        return {"pct": pct_val, "reinvestAmt": reinvestAmt, "incRev": incRev, "incGP": incGP,
                "reinvestProfit": reinvestProfit, "banked": banked, "newBudget": newBudget, "rows": rows, "eff": eff_total}

    stances = [
        ("Conservative", 30, "Protect cash. Bank most of the profit.", STEEL),
        ("Neutral", 60, "Balanced. Grow while keeping a cushion.", GOLD),
        ("Aggressive", 100, "All profit back into growth.", POS),
    ]
    cols = st.columns(3)
    for col, (name, pct_val, desc, color) in zip(cols, stances):
        p = project(pct_val)
        col.markdown(f"""<div class="scenario" style="border-top: 3px solid {color}">
            <div class="s-name" style="color:{color}">{name}</div>
            <div class="s-pct">{pct_val}%</div>
            <div style="font-size:11px;color:{FAINT};margin-bottom:12px">of profit reinvested</div>
            <div class="plan-line"><span>Spend on ads</span><b>{f0(p['reinvestAmt'])}</b></div>
            <div class="plan-line"><span>Bank / retain</span><b>{f0(max(0, p['banked']))}</b></div>
            <div class="plan-line"><span>New ad budget</span><b>{f0(p['newBudget'])}</b></div>
            <div class="plan-line"><span>Expected new revenue</span><b style="color:{POS}">{f0(p['incRev'])}</b></div>
            <div class="plan-line"><span>Profit it throws off</span><b style="color:{POS if p['reinvestProfit']>=0 else NEG}">{'+'if p['reinvestProfit']>=0 else '−'}{f0(abs(p['reinvestProfit']))}</b></div>
            <div style="font-size:11.5px;color:{MUTED};margin-top:11px">{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("#### Build your own plan")
    slider_pct = st.slider("Reinvest % of profit", 0, 150, 60, key="reinvest_slider")
    p = project(slider_pct)
    st.markdown(f"**{slider_pct}%** — {f0(p['reinvestAmt'])} of {f0(netProfit)}")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="plan-line"><span>Reinvest into ads</span><b>{f0(p['reinvestAmt'])}</b></div>
        <div class="plan-line"><span>{'Drawn from reserves' if slider_pct > 100 else 'Banked as retained profit'}</span><b>{f0(abs(p['banked']))}</b></div>
        <div class="plan-line"><span>New total ad budget</span><b>{f0(p['newBudget'])}</b></div>
        <div class="plan-line"><span>Effective ROAS on new spend</span><b style="color:{POS if p['eff']>=breakeven_roas else AMBER}">{p['eff']:.2f}x</b></div>
        <div class="plan-line hl"><span>Expected new revenue</span><b style="color:{POS}">{f0(p['incRev'])}</b></div>
        <div class="plan-line hl"><span>Net profit the reinvestment adds</span><b style="color:{POS if p['reinvestProfit']>=0 else NEG}">{'+'if p['reinvestProfit']>=0 else '−'}{f0(abs(p['reinvestProfit']))}</b></div>
        """, unsafe_allow_html=True)
    with c2:
        st.subheader("Where every reinvested £ goes")
        df = pd.DataFrame([{
            "Channel": r["name"], "Split": f"{r['weight']}%", "Spend": f0(r["spend"]),
            "Eff. ROAS": f"{r['eff']:.2f}x", "Expected rev": f0(r["rev"])
        } for r in p["rows"]])
        st.dataframe(df, hide_index=True, use_container_width=True)

elif page == "£ Online (DTC) P&L":
    st.title(f"Online (DTC) P&L — {D['month']}")
    st.caption("Your Shopify store, every line to the penny")

    c1, c2 = st.columns([1.6, 1])
    with c1:
        st.markdown(f'<span class="tag tag-gold">Net {f0(netProfit)}</span>', unsafe_allow_html=True)
        lines = [
            ("Gross revenue", D["grossRevenue"], "pl-rev head"),
            ("Less: returns & refunds", -D["refunds"], "pl-cost"),
            ("Net revenue", netRev, "total"),
            ("Product cost (COGS)", -D["cogs"], "pl-cost"),
            ("Outbound shipping", -D["shippingOut"], "pl-cost"),
            ("Pick & pack labour", -D["pickPackLabour"], "pl-cost"),
            ("Packaging", -D["packaging"], "pl-cost"),
            ("Payment fees", -D["paymentFees"], "pl-cost"),
            ("Gross profit", grossProfit, "total"),
            ("Meta ads", -D["metaSpend"], "pl-cost"),
            ("Google ads", -D["googleSpend"], "pl-cost"),
            ("TikTok ads", -D["tiktokSpend"], "pl-cost"),
            ("Influencer / UGC", -D["influencer"], "pl-cost"),
            ("Email platform", -D["emailPlatform"], "pl-cost"),
            ("Contribution margin", contribution, "total"),
            ("Salaries (non-fulfilment)", -D["salariesOther"], "pl-cost"),
            ("Rent & warehouse", -D["rent"], "pl-cost"),
            ("Software & apps", -D["software"], "pl-cost"),
            ("Utilities & misc", -D["utilities"], "pl-cost"),
            ("Insurance", -D["insurance"], "pl-cost"),
            ("NET PROFIT", netProfit, "total"),
        ]
        html = ""
        for nm, amt, cls in lines:
            p_val = f"{abs(amt)/netRev*100:.1f}%"
            amt_str = f"−{f0(-amt)}" if amt < 0 else f0(amt)
            html += f'<div class="pl-line {cls}"><div class="nm">{nm}</div><div class="amt">{amt_str}</div><div class="pct">{p_val}</div></div>'
        st.markdown(html, unsafe_allow_html=True)

    with c2:
        st.subheader("Margin ladder")
        ladder = [
            ("Net revenue", 100, GOLD), ("Gross margin", grossMarginPct, STEEL),
            ("Contribution margin", contribution/netRev*100, VIOLET), ("Net margin", netMarginPct, POS),
        ]
        for l, v, c in ladder:
            st.markdown(f"""<div style="margin:10px 0"><div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:5px;color:#E6E9EE"><span>{l}</span><span style="color:{c};font-family:JetBrains Mono">{v:.1f}%</span></div>
            <div style="height:8px;background:#1C232C;border-radius:5px;overflow:hidden"><div style="width:{v}%;height:100%;background:{c}"></div></div></div>""", unsafe_allow_html=True)

        st.subheader("Net profit trend")
        fig = go.Figure(go.Scatter(
            x=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            y=[9200, 11400, 12800, 14100, 16500, netProfit],
            mode="lines+markers", line=dict(color=POS, width=2), fill="tozeroy",
            fillcolor="rgba(63,182,139,.12)", marker=dict(size=6, color=POS),
        ))
        st.plotly_chart(styled_plotly(fig, 220), use_container_width=True)

    st.markdown("#### Cost structure")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Cost breakdown")
        cd = [("Product cost", D["cogs"], GOLD), ("Marketing", marketing, STEEL), ("Salaries", D["salariesOther"], VIOLET),
              ("Shipping", D["shippingOut"], AMBER), ("Pick&pack", D["pickPackLabour"], POS),
              ("Other", D["packaging"]+D["paymentFees"]+D["rent"]+D["software"]+D["utilities"]+D["insurance"], MUTED)]
        fig = go.Figure(go.Pie(labels=[x[0] for x in cd], values=[x[1] for x in cd],
            marker=dict(colors=[x[2] for x in cd]), hole=.62, textinfo="label+percent", textfont=dict(size=10)))
        st.plotly_chart(styled_plotly(fig, 300), use_container_width=True)
    with c2:
        st.subheader("Cost per order to fulfil")
        cpo_items = [
            ("Product cost", D["cogs"]/D["orders"]), ("Outbound shipping", D["shippingOut"]/D["orders"]),
            ("Pick & pack labour", D["pickPackLabour"]/D["orders"]), ("Packaging", D["packaging"]/D["orders"]),
            ("Payment fees", D["paymentFees"]/D["orders"]),
        ]
        cpoTotal = sum(c[1] for c in cpo_items)
        df = pd.DataFrame([{"Component": c[0], "Per order": f1(c[1]), "% of AOV": f"{c[1]/aov*100:.1f}%"} for c in cpo_items] +
            [{"Component": "Total to fulfil", "Per order": f1(cpoTotal), "% of AOV": f"{cpoTotal/aov*100:.0f}%"}])
        st.dataframe(df, hide_index=True, use_container_width=True)

elif page == "◰ Marketplace P&L":
    st.title(f"Marketplace P&L — {D['month']}")
    m = mp_aggregate()
    grossPct = m["gross"] / m["rev"] * 100
    netPct = m["net"] / m["rev"] * 100
    st.markdown(f'<span class="tag tag-gold">Net {f0(m["net"])}</span>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.6, 1])
    with c1:
        lines = [
            ("Marketplace revenue", m["rev"], "pl-rev head"),
            ("Product cost (COGS)", -m["cogs"], "pl-cost"),
            ("Fulfilment (ship & pack)", -m["ful"], "pl-cost"),
            ("Platform & commission fees", -m["fees"], "pl-cost"),
            ("Gross profit / contribution", m["gross"], "total"),
            ("Allocated overheads", -m["overhead"], "pl-cost"),
            ("MARKETPLACE NET PROFIT", m["net"], "total"),
        ]
        html = ""
        for nm, amt, cls in lines:
            p_val = f"{abs(amt)/m['rev']*100:.1f}%"
            amt_str = f"−{f0(-amt)}" if amt < 0 else f0(amt)
            html += f'<div class="pl-line {cls}"><div class="nm">{nm}</div><div class="amt">{amt_str}</div><div class="pct">{p_val}</div></div>'
        st.markdown(html, unsafe_allow_html=True)
    with c2:
        st.subheader("Margin shape")
        for l, v, c in [("Revenue", 100, GOLD), ("Gross / contribution", grossPct, VIOLET), ("Net margin", netPct, POS)]:
            st.markdown(f'<div style="margin:11px 0"><div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:5px;color:#E6E9EE"><span>{l}</span><span style="color:{c};font-family:JetBrains Mono">{v:.1f}%</span></div><div style="height:8px;background:#1C232C;border-radius:5px;overflow:hidden"><div style="width:{v}%;height:100%;background:{c}"></div></div></div>', unsafe_allow_html=True)
        st.subheader("Marketplace revenue trend")
        fig = go.Figure(go.Scatter(x=["Jan","Feb","Mar","Apr","May","Jun"], y=D["marketplaces"]["trend"],
            mode="lines+markers", line=dict(color=GOLD, width=2), fill="tozeroy", fillcolor="rgba(200,165,91,.12)", marker=dict(size=6, color=GOLD)))
        st.plotly_chart(styled_plotly(fig, 220), use_container_width=True)

elif page == "∑ Combined P&L":
    st.title(f"Combined P&L — Online + Marketplaces — {D['month']}")
    m = mp_aggregate()
    combNet = netProfit + m["net"]
    combNetRev = netRev + m["rev"]
    st.markdown(f'<span class="tag tag-gold">Net {f0(combNet)}</span>', unsafe_allow_html=True)

    onlineFulfilOnly = D["shippingOut"] + D["pickPackLabour"] + D["packaging"]
    rows = [
        ("Net revenue", netRev, m["rev"], True), ("Product cost (COGS)", -D["cogs"], -m["cogs"], False),
        ("Fulfilment", -onlineFulfilOnly, -m["ful"], False), ("Platform & payment fees", -D["paymentFees"], -m["fees"], False),
        ("Gross profit", grossProfit, m["gross"], True), ("Marketing & ads", -marketing, 0, False),
        ("Contribution", contribution, m["gross"], True), ("Overheads", -overheads, -m["overhead"], False),
        ("NET PROFIT", netProfit, m["net"], True),
    ]
    df = pd.DataFrame([{
        "Line": l, "Online (DTC)": f0(o) if o >= 0 else f"−{f0(-o)}",
        "Marketplaces": f0(r) if r >= 0 else (f"−{f0(-r)}" if r != 0 else "—"),
        "Combined": f0(o+r) if o+r >= 0 else f"−{f0(-(o+r))}",
        "% of rev": f"{abs(o+r)/combNetRev*100:.1f}%"
    } for l, o, r, tot in rows])
    st.dataframe(df, hide_index=True, use_container_width=True)

    combMargin = combNet / combNetRev * 100
    mini_cards([
        ("Combined net revenue", f0(combNetRev), "online + marketplaces"),
        ("Combined net profit", f0(combNet), f"{combMargin:.1f}% margin"),
        ("Marketplace share of profit", f"{m['net']/combNet*100:.0f}%", f"from {m['rev']/combNetRev*100:.0f}% of revenue"),
    ])

    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure(go.Pie(labels=["Online", "Marketplaces"], values=[netRev, m["rev"]], marker=dict(colors=[STEEL, GOLD]), hole=.62))
        fig.update_layout(title="Revenue split")
        st.plotly_chart(styled_plotly(fig, 280), use_container_width=True)
    with c2:
        fig = go.Figure(go.Pie(labels=["Online", "Marketplaces"], values=[netProfit, m["net"]], marker=dict(colors=[STEEL, GOLD]), hole=.62))
        fig.update_layout(title="Net profit split")
        st.plotly_chart(styled_plotly(fig, 280), use_container_width=True)

elif page == "▲ Acquisition":
    st.title("Acquisition")
    paid = [c for c in D["channels"] if c["spend"] > 0]
    totalSpend = sum(c["spend"] for c in paid)
    totalNew = sum(c["newCust"] for c in D["channels"])
    mini_cards([
        ("Total ad spend", f0(marketing), "all paid + influencer"),
        ("New customers", f"{totalNew:,}", "first-time buyers"),
        ("Blended CAC", f1(totalSpend / totalNew), "spend ÷ new custs"),
        ("Blended ROAS", f"{D['grossRevenue']/marketing:.2f}x", "rev ÷ spend"),
    ])

    c1, c2 = st.columns([1.6, 1])
    with c1:
        st.subheader("Spend vs revenue vs ROAS")
        fig = go.Figure()
        fig.add_bar(x=[c["name"] for c in D["channels"]], y=[c["rev"] for c in D["channels"]], name="Revenue", marker_color="rgba(200,165,91,.85)")
        fig.add_bar(x=[c["name"] for c in D["channels"]], y=[c["spend"] for c in D["channels"]], name="Spend", marker_color="rgba(91,141,239,.85)")
        roas_vals = [c["rev"]/c["spend"] if c["spend"] else None for c in D["channels"]]
        fig.add_scatter(x=[c["name"] for c in D["channels"]], y=roas_vals, name="ROAS", yaxis="y2", mode="lines+markers", line=dict(color=POS, width=2), marker=dict(size=6))
        fig.update_layout(yaxis2=dict(overlaying="y", side="right", title="ROAS", gridcolor="rgba(0,0,0,0)"), barmode="group")
        st.plotly_chart(styled_plotly(fig, 320), use_container_width=True)
    with c2:
        st.subheader("Funnel by channel")
        df = pd.DataFrame([{
            "Channel": c["name"], "CTR": f"{c['ctr']}%" if c["ctr"] else "—",
            "CVR": f"{c['cvr']}%" if c["cvr"] else "—", "AOV": f1(c["rev"]/c["orders"])
        } for c in D["channels"]])
        st.dataframe(df, hide_index=True, use_container_width=True)

    st.subheader("Full channel ledger")
    data = []
    for c in D["channels"]:
        roas = c["rev"]/c["spend"] if c["spend"] else float("inf")
        cac = c["spend"]/c["newCust"] if c["spend"] and c["newCust"] else 0
        if not c["spend"]: verdict = "Free"
        elif roas >= 3: verdict = "Scale"
        elif roas < 2: verdict = "Losing money"
        else: verdict = "Hold"
        data.append({"Channel": c["name"], "Spend": f0(c["spend"]) if c["spend"] else "—",
            "Revenue": f0(c["rev"]), "ROAS": f"{roas:.2f}x" if c["spend"] else "∞",
            "Orders": c["orders"], "New custs": c["newCust"],
            "CAC": f1(cac) if cac else "—", "Verdict": verdict})
    st.dataframe(pd.DataFrame(data), hide_index=True, use_container_width=True)

elif page == "⚖ Break-even ROAS":
    st.title("Break-even ROAS")
    cfg = D["breakeven"]
    paid = [c for c in D["channels"] if c["spend"] > 0]

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Your margin model")
        margin_val = st.slider("Contribution margin (%)", 30.0, 80.0, cfg["globalMargin"], 0.5)
        target_net = st.slider("Net margin target (%)", 0, 40, cfg["targetNetMargin"])
        be = 1 / (margin_val / 100)
        adShare = (margin_val - target_net) / 100
        tgt = 1 / adShare if adShare > 0 else float("inf")
        st.markdown(f"""<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px">
            <div class="mini-card" style="text-align:center"><div class="l">Break-even ROAS</div><div class="v" style="color:{AMBER}">{be:.2f}x</div><div class="s">never drop below this</div></div>
            <div class="mini-card" style="text-align:center"><div class="l">Target ROAS</div><div class="v" style="color:{POS}">{tgt:.2f}x</div><div class="s">to hit your profit goal</div></div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.subheader("Plan a campaign")
        calc_spend = st.number_input("Planned spend (£)", value=5000, step=100)
        calc_rev = st.number_input("Revenue expected back (£)", value=12000, step=100)
        roas = calc_rev / calc_spend if calc_spend else 0
        contrib_calc = calc_rev * margin_val / 100
        profit_calc = contrib_calc - calc_spend
        clears = roas >= be
        st.markdown(f"""
        <div class="plan-line"><span>ROAS this implies</span><b style="color:{POS if clears else NEG}">{roas:.2f}x</b></div>
        <div class="plan-line"><span>Break-even ROAS</span><b>{be:.2f}x</b></div>
        <div class="plan-line"><span>Contribution this earns</span><b>{f0(contrib_calc)}</b></div>
        <div class="plan-line hl"><span>{'Profit' if profit_calc>=0 else 'Loss'} after ad spend</span><b style="color:{POS if profit_calc>=0 else NEG}">{'+'if profit_calc>=0 else '−'}{f0(abs(profit_calc))}</b></div>
        """, unsafe_allow_html=True)

    st.subheader("Per-platform — what each one cost vs what came back")
    data = []
    for c in paid:
        pm = cfg["platformMargin"].get(c["name"], margin_val) / 100
        roas = c["rev"] / c["spend"]; pbe = 1 / pm
        contrib_ch = c["rev"] * pm; profit_ch = contrib_ch - c["spend"]
        verdict = "Losing" if profit_ch <= 0 else ("Profitable" if roas >= pbe * 1.3 else "Thin")
        data.append({"Platform": c["name"], "Margin": f"{pm*100:.0f}%", "Spend": f0(c["spend"]),
            "Revenue": f0(c["rev"]), "Actual": f"{roas:.2f}x", "Break-even": f"{pbe:.2f}x",
            "Profit after ads": f"{'+'if profit_ch>=0 else '−'}{f0(abs(profit_ch))}", "Verdict": verdict})
    st.dataframe(pd.DataFrame(data), hide_index=True, use_container_width=True)

    fig = go.Figure()
    fig.add_bar(x=[c["name"] for c in paid], y=[c["rev"]/c["spend"] for c in paid], name="Actual ROAS",
        marker_color=[POS if c["rev"]/c["spend"] >= 1/(cfg["platformMargin"].get(c["name"], margin_val)/100) else NEG for c in paid])
    beArr = [1/(cfg["platformMargin"].get(c["name"], margin_val)/100) for c in paid]
    fig.add_scatter(x=[c["name"] for c in paid], y=beArr, name="Break-even", mode="lines+markers",
        line=dict(color=AMBER, dash="dash"), marker=dict(size=5, color=AMBER))
    st.plotly_chart(styled_plotly(fig, 300), use_container_width=True)

elif page == "∞ CAC & LTV":
    st.title("CAC & LTV")
    st.caption("How acquisition cost, repurchase rate and time-to-reorder set your real ad ceiling")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Your customer in plain numbers")
        fov = st.number_input("First order value (£)", value=72.66, step=1.0)
        rov = st.number_input("Average repeat order value (£)", value=78.0, step=1.0)
        cac = st.number_input("Cost to acquire one customer (£)", value=39.50, step=1.0)
        margin_cl = st.slider("Profit margin on each order (%)", 30, 80, 61) / 100
        repeat_pct = st.slider("% of customers who buy again", 0, 80, 28) / 100
        freq = st.slider("Re-orders per year (returning customers)", 0.25, 6.0, 2.0, 0.25)
        years = st.slider("How long they stay (years)", 0.25, 5.0, 1.5, 0.25)
    with c2:
        returnerRepeats = freq * years
        blendedRepeats = repeat_pct * returnerRepeats
        N = 1 + blendedRepeats
        ltv = margin_cl * (fov + blendedRepeats * rov)
        ratio = ltv / cac if cac else 0
        maxCac3 = ltv / 3
        firstProfit = margin_cl * fov - cac
        perCust = ltv - cac

        gcol = POS if ratio >= 3 else (AMBER if ratio >= 2 else NEG)
        st.subheader("What a customer is worth")
        fig = go.Figure(go.Indicator(mode="gauge+number", value=ratio,
            number=dict(suffix="x", font=dict(size=40, color=gcol)),
            gauge=dict(axis=dict(range=[0, 4], tickcolor=MUTED), bar=dict(color=gcol),
                bgcolor=SURFACE2, bordercolor=LINE, steps=[
                    dict(range=[0, 2], color="rgba(229,100,94,.15)"),
                    dict(range=[2, 3], color="rgba(224,163,62,.15)"),
                    dict(range=[3, 4], color="rgba(63,182,139,.15)"),
                ], threshold=dict(line=dict(color=GOLD, width=2), thickness=0.75, value=3))))
        fig.update_layout(title="LTV : CAC ratio (target 3.0x)")
        st.plotly_chart(styled_plotly(fig, 250), use_container_width=True)

        st.markdown(f"""
        <div class="plan-line"><span>Customer LTV (lifetime, gross margin)</span><b style="color:{GOLD}">{f1(ltv)}</b></div>
        <div class="plan-line"><span>Avg orders per customer (blended)</span><b>{N:.2f}</b></div>
        <div class="plan-line hl"><span>Lifetime profit per customer (LTV − CAC)</span><b style="color:{POS if perCust>=0 else NEG}">{'+'if perCust>=0 else '−'}{f1(abs(perCust))}</b></div>
        <div class="plan-line"><span>Max CAC for 3:1</span><b>{f1(maxCac3)}</b></div>
        """, unsafe_allow_html=True)

    st.markdown("#### Payback curve")
    maxOrders = max(3, int(np.ceil(1 + returnerRepeats)) + 1)
    cum = [margin_cl * (fov + (k - 1) * rov) for k in range(1, maxOrders + 1)]
    fig = go.Figure()
    fig.add_scatter(x=[f"Order {k}" for k in range(1, maxOrders+1)], y=cum, name="Cumulative profit", fill="tozeroy",
        line=dict(color=POS), fillcolor="rgba(63,182,139,.12)")
    fig.add_scatter(x=[f"Order {k}" for k in range(1, maxOrders+1)], y=[cac]*maxOrders, name="CAC",
        line=dict(color=NEG, dash="dash"))
    st.plotly_chart(styled_plotly(fig, 280), use_container_width=True)

    st.markdown("#### Sensitivity: LTV vs repeat rate")
    reps = [10, 20, 30, 40, 50, 60, 70]
    ltvR = [margin_cl * (fov + (rp/100) * returnerRepeats * rov) for rp in reps]
    curRep = round(repeat_pct * 100)
    fig = go.Figure(go.Bar(x=[f"{r}%" for r in reps], y=ltvR,
        marker_color=[GOLD if abs(r - curRep) < 6 else "rgba(91,141,239,.6)" for r in reps]))
    fig.update_layout(xaxis_title="% of customers who buy again", yaxis_title="Customer LTV")
    st.plotly_chart(styled_plotly(fig, 300), use_container_width=True)

elif page == "↻ Retention":
    st.title("Retention")
    mini_cards([
        ("Repeat-purchase rate", f"{D['repeatRate']}%", "buy more than once"),
        ("Customer LTV", f1(D["ltv"]), "gross-margin lifetime"),
        ("Avg orders / customer", f"{D['avgOrdersLifetime']:.1f}", "lifetime"),
        ("LTV : CAC", f"{ltvCac:.1f}x", "target 3.0x+"),
    ])

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("LTV : CAC gauge")
        fig = go.Figure(go.Indicator(mode="gauge+number", value=ltvCac,
            number=dict(suffix="x", font=dict(size=36, color=AMBER)),
            gauge=dict(axis=dict(range=[0, 4]), bar=dict(color=AMBER), bgcolor=SURFACE2, bordercolor=LINE)))
        st.plotly_chart(styled_plotly(fig, 250), use_container_width=True)
    with c2:
        st.subheader("Repeat-purchase cohorts")
        fig = go.Figure()
        labels_x = ["Order 1", "+1mo", "+2mo", "+3mo", "+4mo", "+5mo"]
        colors = [GOLD, STEEL, VIOLET, POS]
        for i, c in enumerate(D["cohorts"][:4]):
            fig.add_scatter(x=labels_x, y=c["d"], name=c["m"], line=dict(color=colors[i]), mode="lines+markers", connectgaps=True)
        st.plotly_chart(styled_plotly(fig, 300), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Email flows vs campaigns")
        emailTotal = sum(e["rev"] for e in D["email"])
        email_details = {
            "Welcome flow": "Triggered when a new subscriber signs up. First impression — sets the tone and drives first purchase.",
            "Abandoned checkout": "Sent when a customer adds to cart but doesn't complete. Recovers ~10-15% of abandoned carts.",
            "Browse abandon": "Triggered after browsing without adding to cart. Gentle nudge with personalized product recommendations.",
            "Post-purchase": "Sent after delivery. Builds loyalty, drives reviews, and suggests complementary products.",
            "Win-back": "Targets lapsed customers (60-90 days inactive). Re-engages with special offers or new arrivals.",
            "Campaigns (broadcasts)": "Scheduled email blasts — new launches, promotions, seasonal events. Drives bulk revenue.",
        }
        for e in D["email"]:
            share = e["rev"] / emailTotal * 100
            with st.expander(f"**{e['name']}** — {f0(e['rev'])} ({share:.0f}% of email revenue)", expanded=False):
                st.metric("Revenue", f0(e["rev"]))
                st.markdown(f"**Type:** {e['type'].title()}")
                st.markdown(f"**What it does:** {email_details.get(e['name'], '')}")
                st.progress(share / 100, text=f"{share:.0f}% of email revenue")
    with c2:
        st.subheader("Organic & direct revenue")
        fig = go.Figure(go.Bar(x=["Jan","Feb","Mar","Apr","May","Jun"], y=D["organicTrend"],
            marker_color="rgba(138,148,163,.7)", text=[f"£{v/1000:.1f}k" for v in D["organicTrend"]], textposition="outside"))
        st.plotly_chart(styled_plotly(fig, 280), use_container_width=True)
        growth = (D["organicTrend"][-1] - D["organicTrend"][0]) / D["organicTrend"][0] * 100
        st.info(f"Organic revenue grew {growth:.0f}% over 6 months — from {f0(D['organicTrend'][0])} to {f0(D['organicTrend'][-1])}.")

elif page == "☺ Customers":
    st.title("Customers")
    C = D["customers"]
    champ = max(C["segments"], key=lambda s: s["rev"])
    giftShare = sum(m["p"] for m in C["motivation"] if "gift" in m["r"].lower() or "occasion" in m["r"].lower())
    mini_cards([
        ("Customers in total", f"{C['total']:,}", "all-time"),
        ("Repeat-purchase rate", f"{D['repeatRate']}%", "buy more than once"),
        ("Top segment", champ["name"], f"{champ['rev']}% of revenue from {champ['cust']}% of customers"),
        ("Gifting share", f"{giftShare}%", "bought as a gift"),
    ])

    c1, c2 = st.columns([1.6, 1])
    with c1:
        st.subheader("Customer segments")
        fig = go.Figure()
        fig.add_bar(x=[s["name"] for s in C["segments"]], y=[s["cust"] for s in C["segments"]], name="% of customers", marker_color="rgba(91,141,239,.6)")
        fig.add_bar(x=[s["name"] for s in C["segments"]], y=[s["rev"] for s in C["segments"]], name="% of revenue", marker_color=GOLD)
        fig.update_layout(barmode="group")
        st.plotly_chart(styled_plotly(fig, 300), use_container_width=True)
    with c2:
        st.subheader("The 80/20, ranked")
        df = pd.DataFrame([{"Segment": s["name"], "Customers": f"{s['cust']}%", "Revenue": f"{s['rev']}%", "Who": s["desc"]} for s in C["segments"]])
        st.dataframe(df, hide_index=True, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Age")
        fig = go.Figure(go.Bar(x=[a["b"] for a in C["age"]], y=[a["p"] for a in C["age"]],
            marker_color=[GOLD if a["p"] == max(x["p"] for x in C["age"]) else "rgba(91,141,239,.6)" for a in C["age"]]))
        st.plotly_chart(styled_plotly(fig, 250), use_container_width=True)
    with c2:
        st.subheader("Self-wear vs gifting")
        fig = go.Figure(go.Pie(labels=[b["g"] for b in C["buyer"]], values=[b["p"] for b in C["buyer"]],
            marker=dict(colors=[b["c"] for b in C["buyer"]]), hole=.6))
        st.plotly_chart(styled_plotly(fig, 250), use_container_width=True)
    with c3:
        st.subheader("Top locations")
        fig = go.Figure(go.Bar(y=[l["c"] for l in C["locations"]], x=[l["p"] for l in C["locations"]],
            orientation="h", marker_color="rgba(200,165,91,.7)"))
        st.plotly_chart(styled_plotly(fig, 250), use_container_width=True)

    st.subheader("Purchase motivation")
    fig = go.Figure(go.Bar(y=[m["r"] for m in C["motivation"]], x=[m["p"] for m in C["motivation"]],
        orientation="h", marker_color=[m["c"] for m in C["motivation"]]))
    st.plotly_chart(styled_plotly(fig, 250), use_container_width=True)

    st.markdown("#### Your three core customers")
    for p in C["personas"]:
        with st.expander(f"**{p['name']}** — {p['share']} · AOV {p['aov']}", expanded=False):
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"**Who they are:** {p['who']}")
                st.markdown(f"**Why they buy:** {p['why']}")
                st.markdown(f"""
                | Attribute | Detail |
                |-----------|--------|
                | Share of customers | {p['share']} |
                | Best channels | {p['channel']} |
                | Typical AOV | {p['aov']} |
                """)
            with c2:
                channels = p["channel"].split(" · ")
                ch_data = [next((c for c in D["channels"] if c["name"] == ch), None) for ch in channels]
                ch_data = [c for c in ch_data if c]
                if ch_data:
                    fig = go.Figure(go.Bar(
                        x=[c["name"] for c in ch_data],
                        y=[c["rev"] for c in ch_data],
                        marker_color=[c["colour"] for c in ch_data],
                        text=[f0(c["rev"]) for c in ch_data], textposition="outside"))
                    fig.update_layout(showlegend=False, title="Channel revenue")
                    st.plotly_chart(styled_plotly(fig, 200), use_container_width=True)
            if "Self-Expressor" in p["name"]:
                st.info("**Growth strategy:** Keep newness flowing. Launch monthly drops, use Instagram Reels and TikTok UGC. Reward repeat purchases with early access.")
            elif "Gift-Giver" in p["name"]:
                st.info("**Growth strategy:** Make gifting frictionless. Add gift wrapping, gift cards, and easy returns. Target spikes around Valentine's, Father's Day, and Christmas with Google Shopping.")
            elif "Collector" in p["name"]:
                st.info("**Growth strategy:** Build exclusivity. Limited editions, VIP early access, and personalized email. Highest LTV segment — protect at all costs.")

elif page == "◈ Products & Launches":
    st.title("Products & Launches")

    prod_tab1, prod_tab2, prod_tab3, prod_tab4 = st.tabs(["🏆 Winners", "💸 Wasted spend", "📊 Margins", "🚀 Launches"])

    with prod_tab1:
        st.subheader("Winning products on ads")
        for p in D["winners"]:
            profit = p["rev"] * p["margin"] / 100 - p["spend"]
            roas = p["rev"] / p["spend"]
            with st.expander(f"**{p['name']}** — {f0(p['rev'])} revenue · {roas:.1f}x ROAS", expanded=False):
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Revenue", f0(p["rev"]))
                m2.metric("Ad spend", f0(p["spend"]))
                m3.metric("ROAS", f"{roas:.1f}x")
                m4.metric("Profit after ads", f"+{f0(profit)}")
                st.markdown(f"""
                | Metric | Value |
                |--------|-------|
                | Units sold | {p['units']:,} |
                | Product margin | {p['margin']}% |
                | Revenue per unit | {f1(p['rev']/p['units'])} |
                | Ad cost per unit | {f1(p['spend']/p['units'])} |
                | Profit per unit | {f1(profit/p['units'])} |
                """)
                st.success(f"This product generates {f0(profit)} net profit from ads. Consider scaling spend by 20% and monitoring ROAS.")

    with prod_tab2:
        st.subheader("Wasted ad spend — products losing money")
        wasteTotal = sum(p["spend"] - p["rev"] * p["margin"] / 100 for p in D["wasted"])
        st.error(f"Total wasted: {f0(wasteTotal)}/mo — pausing these drops straight to net profit.")
        for p in D["wasted"]:
            loss = p["spend"] - p["rev"] * p["margin"] / 100
            with st.expander(f"**{p['name']}** — ROAS {p['roas']}x · losing ~{f0(loss)}/mo", expanded=False):
                m1, m2, m3 = st.columns(3)
                m1.metric("Revenue", f0(p["rev"]))
                m2.metric("Ad spend", f0(p["spend"]))
                m3.metric("ROAS", f"{p['roas']}x", delta=f"{p['roas']-1.63:.2f}x vs break-even", delta_color="inverse")
                st.markdown(f"""
                | Metric | Value |
                |--------|-------|
                | Product margin | {p['margin']}% |
                | Gross profit | {f0(p['rev'] * p['margin'] / 100)} |
                | Ad spend | {f0(p['spend'])} |
                | **Net loss** | **−{f0(loss)}** |
                | Break-even revenue needed | {f0(p['spend'] / (p['margin']/100))} |
                """)
                st.warning("**Recommended action:** Pause ads immediately. Test organic promotion or bundle with a winner.")

    with prod_tab3:
        st.subheader("Margin by product")
        fig = go.Figure(go.Bar(y=[p["name"] for p in D["prodMargin"]], x=[p["m"] for p in D["prodMargin"]], orientation="h",
            marker_color=[POS if p["m"] >= 55 else (AMBER if p["m"] >= 45 else NEG) for p in D["prodMargin"]],
            text=[f"{p['m']}%" for p in D["prodMargin"]], textposition="outside"))
        st.plotly_chart(styled_plotly(fig, 300), use_container_width=True)
        avg_margin = sum(p["m"] for p in D["prodMargin"]) / len(D["prodMargin"])
        below = [p for p in D["prodMargin"] if p["m"] < 50]
        st.info(f"Average margin: {avg_margin:.0f}%. {len(below)} product(s) below 50% — consider price increases or cost renegotiation.")

    with prod_tab4:
        st.subheader("Launch tracker")
        for l in D["launches"]:
            status_icon = {"win": "🟢", "ok": "🔵", "watch": "🟡"}[l["status"]]
            grade = {"win": "Winner", "ok": "Solid", "watch": "At risk"}[l["status"]]
            with st.expander(f"{status_icon} **{l['name']}** — {l['date']} · {f0(l['rev'])} · {grade}", expanded=False):
                m1, m2, m3 = st.columns(3)
                m1.metric("Revenue", f0(l["rev"]))
                m2.metric("Sell-through", f"{l['sellthru']}%")
                m3.metric("Margin", f"{l['margin']}%")
                st.markdown(f"""
                | Metric | Value |
                |--------|-------|
                | Launch date | {l['date']} |
                | Revenue to date | {f0(l['rev'])} |
                | Sell-through rate | {l['sellthru']}% |
                | Product margin | {l['margin']}% |
                | Gross profit | {f0(l['rev'] * l['margin'] / 100)} |
                | Grade | {grade} |
                """)
                if l["status"] == "win":
                    st.success("Strong launch — consider reordering and scaling ad spend.")
                elif l["status"] == "ok":
                    st.info("Performing steady — monitor sell-through over next 2 weeks.")
                else:
                    st.warning("Below expectations — review pricing, creative, and targeting. Set a 14-day review deadline.")

elif page == "▦ Inventory":
    st.title("Inventory")
    mini_cards([
        ("Stock on hand", f0(D["stockValue"]), "cash tied up"),
        ("Active SKUs", str(D["skuCount"]), "lines carried"),
        ("Inventory turns", f"{invTurns:.1f}x", "annualised"),
        ("Dead stock", f0(D["deadStockValue"]), "to liquidate"),
    ])

    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.subheader("Stock status mix")
        fig = go.Figure(go.Pie(labels=[s["l"] for s in D["invStatus"]], values=[s["v"] for s in D["invStatus"]],
            marker=dict(colors=[s["c"] for s in D["invStatus"]]), hole=.6))
        st.plotly_chart(styled_plotly(fig, 280), use_container_width=True)
    with c2:
        st.subheader("SKU-level inventory")
        status_labels = {"win": "Winner", "ok": "Healthy", "watch": "Slow", "dead": "Dead"}
        status_icons = {"win": "🟢", "ok": "🔵", "watch": "🟡", "dead": "🔴"}
        for inv_item in D["inv"]:
            icon = status_icons[inv_item["status"]]
            label = status_labels[inv_item["status"]]
            unit_val = inv_item["value"] / inv_item["units"]
            with st.expander(f"{icon} **{inv_item['sku']}** — {inv_item['units']} units · {inv_item['days']}d cover · {label}", expanded=False):
                m1, m2, m3 = st.columns(3)
                m1.metric("Units on hand", f"{inv_item['units']}")
                m2.metric("Stock value", f0(inv_item["value"]))
                m3.metric("Days of cover", f"{inv_item['days']}d")
                st.markdown(f"""
                | Metric | Value |
                |--------|-------|
                | Sell-through rate | {inv_item['sellthru']}% |
                | Unit cost | {f1(unit_val)} |
                | Daily sell rate | ~{inv_item['units']/max(inv_item['days'],1):.0f} units |
                | Reorder point (14d cover) | {round(inv_item['units']/max(inv_item['days'],1)*14)} units |
                """)
                if inv_item["status"] == "win":
                    st.success(f"Only {inv_item['days']}d of cover left — reorder now to avoid stockout.")
                elif inv_item["status"] == "dead":
                    st.error(f"Slow mover at {inv_item['sellthru']}% sell-through. Consider markdown or bundling.")

    st.subheader("Dead-stock liquidation plan")
    st.error(f"Total frozen capital: {f0(D['deadStockValue'])} across {len(D['dead'])} SKUs")
    for d in D["dead"]:
        urgency = "🔴" if d["age"] > 120 else ("🟡" if d["age"] > 60 else "🟢")
        with st.expander(f"{urgency} **{d['sku']}** — {f0(d['value'])} frozen · {d['age']}d old", expanded=False):
            m1, m2, m3 = st.columns(3)
            m1.metric("Units stuck", f"{d['units']}")
            m2.metric("Cash frozen", f0(d["value"]))
            m3.metric("Days since last sale", f"{d['age']}d")
            unit_cost = d["value"] / d["units"]
            st.markdown(f"""
            | Metric | Value |
            |--------|-------|
            | Unit cost | {f1(unit_cost)} |
            | Units remaining | {d['units']} |
            | Total frozen value | {f0(d['value'])} |
            | Age (days) | {d['age']}d |
            | Recovery at 40% markdown | ~{f0(d['value'] * 0.6)} |
            | Recovery at 60% markdown | ~{f0(d['value'] * 0.4)} |
            """)
            st.info(f"**Liquidation plan:** {d['plan']}")
            if d["age"] > 120:
                st.error("Urgent: over 120 days old. Markdown aggressively or bundle with best-sellers.")
            elif d["age"] > 60:
                st.warning("Monitor closely. If no improvement in 14 days, begin clearance.")

elif page == "☖ Staff & Targets":
    st.title("Staff & Targets")
    rev_staff = [s for s in D["staff"] if s["type"] == "rev"]
    ops_staff = [s for s in D["staff"] if s["type"] == "ops"]
    totalDriven = sum(s["driven"] for s in rev_staff)
    avgErr = sum(s["errors"] for s in ops_staff) / len(ops_staff)
    mini_cards([
        ("Revenue-driving heads", str(len(rev_staff)), "sales / marketing / CS"),
        ("Fulfilment heads", str(len(ops_staff)), "pick & pack"),
        ("Revenue per rev-head", f0(totalDriven / len(rev_staff)), "attributed"),
        ("Avg packing error rate", f"{avgErr:.1f}%", "target <1.5%"),
    ])

    st.subheader("Staff scorecard")
    staff_tab1, staff_tab2 = st.tabs(["💰 Revenue team", "📦 Fulfilment team"])
    with staff_tab1:
        for s in [s for s in D["staff"] if s["type"] == "rev"]:
            grossFromThem = s["driven"] * (grossMarginPct / 100)
            impact = grossFromThem - s["cost"]
            hit = s["driven"] / s["target"] * 100
            verdict_icon = "🟢" if s["driven"] >= s["target"] else "🟡"
            with st.expander(f"{verdict_icon} **{s['name']}** — {s['role']} · {f0(s['driven'])} driven · {hit:.0f}% of target", expanded=False):
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Revenue driven", f0(s["driven"]))
                m2.metric("Target", f0(s["target"]))
                m3.metric("Target hit", f"{hit:.0f}%")
                m4.metric("Profit impact", f"{'+'if impact>0 else '−'}{f0(abs(impact))}")
                st.progress(min(hit / 100, 1.0), text=f"{hit:.0f}% of {f0(s['target'])} target")
                st.markdown(f"""
                | Metric | Value |
                |--------|-------|
                | Loaded cost (salary + benefits) | {f0(s['cost'])} |
                | Revenue attributed | {f0(s['driven'])} |
                | Gross profit generated | {f0(grossFromThem)} |
                | ROI on salary | {grossFromThem/s['cost']:.1f}x |
                | Net impact (profit − cost) | {'+'if impact>0 else '−'}{f0(abs(impact))} |
                """)
                if s["driven"] >= s["target"]:
                    st.success(f"Hitting target. Generating {f0(impact)} net impact. Consider performance bonus.")
                else:
                    st.warning(f"Below target by {f0(s['target'] - s['driven'])}. Review pipeline and support needed.")
    with staff_tab2:
        for s in [s for s in D["staff"] if s["type"] == "ops"]:
            cpo = s["cost"] / s["packed"]
            verdict_icon = "🟢" if s["errors"] < 1.5 else ("🟡" if s["errors"] < 3 else "🔴")
            missends = round(s["packed"] * s["errors"] / 100)
            missend_cost = missends * 29
            with st.expander(f"{verdict_icon} **{s['name']}** — {s['role']} · {s['packed']} packed · {s['errors']}% errors", expanded=False):
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Orders packed", f"{s['packed']}")
                m2.metric("Error rate", f"{s['errors']}%")
                m3.metric("Cost/order", f1(cpo))
                m4.metric("Est. mis-send cost", f"−{f0(missend_cost)}")
                st.markdown(f"""
                | Metric | Value |
                |--------|-------|
                | Monthly salary | {f0(s['cost'])} |
                | Orders packed | {s['packed']} |
                | Cost per order | {f1(cpo)} |
                | Error rate | {s['errors']}% |
                | Estimated mis-sends | {missends} |
                | Mis-send cost (~£29 each) | {f0(missend_cost)} |
                | True cost (salary + errors) | {f0(s['cost'] + missend_cost)} |
                """)
                if s["errors"] < 1.5:
                    st.success("Excellent accuracy. Consider as mentor for other packers.")
                elif s["errors"] < 3:
                    st.info("Acceptable but room to improve. Monitor weekly.")
                else:
                    st.error(f"High error rate costing ~{f0(missend_cost)}/mo in re-ships. Needs scan-to-pack and retraining.")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Revenue roles — target attainment")
        fig = go.Figure()
        fig.add_bar(x=[s["name"] for s in rev_staff], y=[s["target"] for s in rev_staff], name="Target", marker_color="rgba(91,141,239,.35)")
        fig.add_bar(x=[s["name"] for s in rev_staff], y=[s["driven"] for s in rev_staff], name="Actual", marker_color=GOLD)
        fig.update_layout(barmode="group")
        st.plotly_chart(styled_plotly(fig, 300), use_container_width=True)
    with c2:
        st.subheader("Fulfilment — packing rate vs error rate")
        fig = go.Figure(go.Scatter(
            x=[s["packed"] for s in ops_staff], y=[s["errors"] for s in ops_staff],
            mode="markers+text", text=[s["name"] for s in ops_staff], textposition="top center",
            marker=dict(size=14, color=[POS if s["errors"] < 1.5 else (AMBER if s["errors"] < 3 else NEG) for s in ops_staff]),
            textfont=dict(size=10, color=MUTED),
        ))
        fig.update_layout(xaxis_title="Orders packed / month", yaxis_title="Error rate %")
        st.plotly_chart(styled_plotly(fig, 300), use_container_width=True)

elif page == "⚙ Pick · Pack · Dispatch":
    st.title("Pick · Pack · Dispatch")
    totReturns = sum(r["orders"] for r in D["returns"])
    returnCost = sum(r["cost"] for r in D["returns"])
    mini_cards([
        ("Pick & pack / order", f1(D["ppCostTrend"][-1]), "labour + packaging"),
        ("Perfect-order rate", f"{D['perfectOrderRate']}%", "target 97%"),
        ("Return rate", f"{totReturns/D['orders']*100:.1f}%", f"{totReturns} orders"),
        ("Cost of returns", f0(returnCost), "this month"),
    ])

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Cost to pick & pack one order")
        fig = go.Figure(go.Scatter(x=["Jan","Feb","Mar","Apr","May","Jun"], y=D["ppCostTrend"],
            mode="lines+markers", line=dict(color=GOLD, width=2), fill="tozeroy", fillcolor="rgba(200,165,91,.12)"))
        st.plotly_chart(styled_plotly(fig, 280), use_container_width=True)
    with c2:
        st.subheader("Perfect-order rate")
        fig = go.Figure(go.Indicator(mode="gauge+number", value=D["perfectOrderRate"],
            number=dict(suffix="%", font=dict(size=36, color=POS)),
            gauge=dict(axis=dict(range=[0, 100]), bar=dict(color=POS), bgcolor=SURFACE2, bordercolor=LINE,
                threshold=dict(line=dict(color=AMBER, width=2), thickness=0.75, value=97))))
        fig.update_layout(title="Target: 97%")
        st.plotly_chart(styled_plotly(fig, 250), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Dispatch SLA")
        for s in D["dispatchSLA"]:
            met = s["actual"] >= s["target"]
            icon = "🟢" if met else "🔴"
            gap = s["actual"] - s["target"]
            with st.expander(f"{icon} **{s['window']}** — {s['actual']}% vs {s['target']}% target", expanded=False):
                st.metric("Actual performance", f"{s['actual']}%", delta=f"{gap:+d}pp vs target")
                st.progress(s["actual"] / 100, text=f"{s['actual']}% dispatched on time")
                if not met:
                    st.warning(f"Missing target by {abs(gap)}pp. Review bottlenecks in this dispatch window.")
                else:
                    st.success("Meeting target. Maintain current performance.")
    with c2:
        st.subheader("Returns & the cost of getting it wrong")
        for r in D["returns"]:
            share = r["orders"] / totReturns * 100
            preventable = "mis-pick" in r["reason"].lower() or "damaged" in r["reason"].lower()
            icon = "🔴" if preventable else "🟡"
            with st.expander(f"{icon} **{r['reason']}** — {r['orders']} orders · {f0(r['cost'])} cost", expanded=False):
                m1, m2 = st.columns(2)
                m1.metric("Orders affected", f"{r['orders']}")
                m2.metric("Total cost", f0(r["cost"]))
                st.markdown(f"**Share of all returns:** {share:.0f}%")
                cost_per = r["cost"] / r["orders"]
                st.markdown(f"**Cost per return:** {f1(cost_per)}")
                if preventable:
                    st.error("This is a preventable return. Fix the root cause to eliminate these costs entirely.")
                else:
                    st.info("Customer-driven return. Improve product descriptions, sizing guides, or photos to reduce.")

elif page == "◰ Marketplaces":
    st.title("Marketplaces")
    MP = D["marketplaces"]
    fulfil = MP["fulfilPerUnit"]
    fees_map = {"DTC": {"f": MP["dtcFeePct"], "fixed": 0}}
    for c in MP["channels"]:
        fees_map[c["name"]] = {"f": c["feePct"], "fixed": c["fixedFee"]}

    totRev = sum(c["rev"] for c in MP["channels"])
    cardData = []
    for c in MP["channels"]:
        feesPaid = c["rev"] * c["feePct"] / 100 + c["units"] * c["fixedFee"]
        cogs = c["rev"] * MP["cogsRate"]; ful = c["units"] * fulfil
        profit = c["rev"] - feesPaid - cogs - ful; margin = profit / c["rev"] * 100
        cardData.append({**c, "feesPaid": feesPaid, "profit": profit, "margin": margin})
    totProfit = sum(c["profit"] for c in cardData)
    best = max(cardData, key=lambda c: c["margin"])

    mini_cards([
        ("Marketplace revenue", f0(totRev), "Etsy + NOTHS + Debenhams"),
        ("Marketplace contribution", f0(totProfit), f"{totProfit/totRev*100:.1f}% before overhead"),
        ("Avg take rate", f"{sum(c['feePct'] for c in MP['channels'])/len(MP['channels']):.0f}%", "fees before your costs"),
        ("Best margin", best["name"], f"{best['margin']:.0f}% net"),
    ])

    st.markdown("#### Profit per marketplace")
    for c in cardData:
        margin_icon = "🟢" if c["margin"] > 30 else ("🟡" if c["margin"] > 15 else "🔴")
        cogs_mp = c["rev"] * MP["cogsRate"]
        ful_mp = c["units"] * fulfil
        with st.expander(f"{margin_icon} **{c['name']}** — {f0(c['rev'])} revenue · {c['margin']:.0f}% margin · {c['units']} orders", expanded=False):
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Revenue", f0(c["rev"]))
            m2.metric("Platform fees", f"−{f0(c['feesPaid'])}")
            m3.metric("Contribution", f0(c["profit"]))
            m4.metric("Net margin", f"{c['margin']:.1f}%")
            st.markdown(f"""
            | Line item | Amount | % of revenue |
            |-----------|--------|-------------|
            | Revenue | {f0(c['rev'])} | 100% |
            | Product cost (COGS) | −{f0(cogs_mp)} | {cogs_mp/c['rev']*100:.1f}% |
            | Fulfilment | −{f0(ful_mp)} | {ful_mp/c['rev']*100:.1f}% |
            | Platform fees ({c['feePct']}%) | −{f0(c['feesPaid'])} | {c['feesPaid']/c['rev']*100:.1f}% |
            | **Contribution** | **{f0(c['profit'])}** | **{c['margin']:.1f}%** |
            """)
            st.markdown(f"**Top seller:** {c['topProduct']}")
            rev_per_order = c["rev"] / c["units"]
            profit_per_order = c["profit"] / c["units"]
            st.markdown(f"**Revenue per order:** {f1(rev_per_order)} · **Profit per order:** {f1(profit_per_order)}")

    st.markdown("#### Product margins by marketplace")
    def net_unit(price, cost, ch):
        fe = fees_map[ch]; return price * (1 - fe["f"] / 100) - fe["fixed"] - cost - fulfil
    mpOrder = ["Etsy", "NOTHS", "Debenhams"]
    data = []
    for p in MP["catalogue"]:
        row = {"Product": p["name"], "Cost": f1(p["cost"])}
        for ch in mpOrder:
            n = net_unit(p["prices"][ch], p["cost"], ch)
            m = n / p["prices"][ch] * 100
            row[f"{ch} £/unit"] = f"{'+'if n>=0 else '−'}{abs(n):.2f} ({m:.0f}%)"
        data.append(row)
    st.dataframe(pd.DataFrame(data), hide_index=True, use_container_width=True)

    st.markdown("#### Margin guard — cost-increase calculator")
    c1, c2 = st.columns(2)
    with c1:
        product_idx = st.selectbox("Product", range(len(MP["catalogue"])), format_func=lambda i: MP["catalogue"][i]["name"])
        channel = st.selectbox("Channel", ["DTC", "Etsy", "NOTHS", "Debenhams"])
        sel_prod = MP["catalogue"][product_idx]
        curr_cost = st.number_input("Current unit cost (£)", value=float(sel_prod["cost"]), step=0.5)
        new_cost = st.number_input("New unit cost (£)", value=float(sel_prod["cost"]), step=0.5)
        price = st.number_input("Selling price (£)", value=float(sel_prod["prices"][channel]), step=0.5)
        target_margin = st.slider("Minimum net margin (%)", 0, 50, 20)

        nowNet = net_unit(price, curr_cost, channel)
        newNet = net_unit(price, new_cost, channel)
        nowM = nowNet / price * 100 if price else 0
        newM = newNet / price * 100 if price else 0

        def min_price(cost, ch, tPct):
            fe = fees_map[ch]; d = (1 - fe["f"]/100) - tPct/100
            return (fe["fixed"] + cost + fulfil) / d if d > 0 else float("inf")

        floor = min_price(new_cost, channel, target_margin)
        be = min_price(new_cost, channel, 0)

        st.markdown(f"""
        <div class="plan-line"><span>Now — net at {f1(curr_cost)} cost</span><b style="color:{POS if nowNet>0 else NEG}">{'+'if nowNet>=0 else '−'}{f1(abs(nowNet))} ({nowM:.0f}%)</b></div>
        <div class="plan-line hl"><span>After — net at {f1(new_cost)} cost</span><b style="color:{POS if newNet>0 else NEG}">{'+'if newNet>=0 else '−'}{f1(abs(newNet))} ({newM:.0f}%)</b></div>
        <div class="plan-line"><span>Price floor for {target_margin}% margin</span><b style="color:{GOLD}">{f1(floor) if floor < 9999 else '—'}</b></div>
        <div class="plan-line"><span>Break-even price</span><b>{f1(be)}</b></div>
        """, unsafe_allow_html=True)
    with c2:
        st.subheader("Price floor by channel")
        chOrder = ["DTC", "Etsy", "NOTHS", "Debenhams"]
        data = []
        for ch in chOrder:
            fl = min_price(new_cost, ch, target_margin)
            pr = sel_prod["prices"][ch]
            ok = pr >= fl
            data.append({"Channel": ch, "Fee": f"{fees_map[ch]['f']}%", "Your price": f1(pr),
                f"Floor @ {target_margin}%": f1(fl) if fl < 9999 else "—", "Status": "OK" if ok else "Underwater"})
        st.dataframe(pd.DataFrame(data), hide_index=True, use_container_width=True)

elif page == "◷ Quarterly trends":
    st.title("Quarterly trends")
    Q = D["quarterly"]
    months = Q["monthly"]
    peakM = max(months, key=lambda m: m["v"])
    avg = sum(m["v"] for m in months) / 12

    st.subheader("When the money comes in")
    fig = go.Figure(go.Bar(x=[m["m"] for m in months], y=[m["v"] for m in months],
        marker_color=[GOLD if m["v"]==peakM["v"] else (POS if m["v"]>avg else "rgba(91,141,239,.55)") for m in months],
        text=[f"£{m['v']}k" for m in months], textposition="outside"))
    st.plotly_chart(styled_plotly(fig, 320), use_container_width=True)

    st.markdown("#### Quarter by quarter")
    for q in Q["quarters"]:
        tot = q["dtcRev"] + q["retailRev"]; roas = q["dtcRev"] / q["adSpend"]
        peak_label = " ⭐ Peak" if q['q'] == 'Q4' else ""
        with st.expander(f"**{q['q']}** ({q['months']}) — Total: {f0(tot)} · ROAS: {roas:.2f}x{peak_label}", expanded=False):
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total revenue", f0(tot))
            m2.metric("Ad spend", f0(q["adSpend"]))
            m3.metric("ROAS", f"{roas:.2f}x")
            m4.metric("New customers", f"{q['newCust']:,}")
            st.markdown("---")
            d1, d2 = st.columns(2)
            with d1:
                st.markdown(f"""
                | Metric | Value |
                |--------|-------|
                | DTC revenue | {f0(q['dtcRev'])} |
                | Retail revenue | {f0(q['retailRev'])} |
                | DTC share | {q['dtcRev']/tot*100:.0f}% |
                | Retail share | {q['retailRev']/tot*100:.0f}% |
                | Cost per new customer | {f1(q['adSpend']/q['newCust'])} |
                | Revenue per new customer | {f1(q['dtcRev']/q['newCust'])} |
                """)
            with d2:
                st.markdown(f"**Hero product:** {q['topProduct']}")
                st.markdown(f"**Reason:** {q['topReason']}")
                st.markdown(f"**Hero revenue:** {f0(q['topRev'])}")
                st.markdown(f"**Hero as % of DTC:** {q['topRev']/q['dtcRev']*100:.1f}%")
                fig = go.Figure(go.Pie(labels=["Hero product", "Other products"], values=[q["topRev"], q["dtcRev"]-q["topRev"]],
                    marker=dict(colors=[GOLD, LINE]), hole=.6, textinfo="percent"))
                fig.update_layout(showlegend=False, title="Hero product share")
                st.plotly_chart(styled_plotly(fig, 180), use_container_width=True)

    st.subheader("Ad spend & efficiency by quarter")
    fig = go.Figure()
    fig.add_bar(x=[q["q"] for q in Q["quarters"]], y=[q["dtcRev"]+q["retailRev"] for q in Q["quarters"]], name="Revenue", marker_color="rgba(200,165,91,.85)")
    fig.add_bar(x=[q["q"] for q in Q["quarters"]], y=[q["adSpend"] for q in Q["quarters"]], name="Ad spend", marker_color="rgba(91,141,239,.85)")
    fig.add_scatter(x=[q["q"] for q in Q["quarters"]], y=[q["dtcRev"]/q["adSpend"] for q in Q["quarters"]], name="ROAS",
        yaxis="y2", mode="lines+markers", line=dict(color=POS, width=2))
    fig.update_layout(barmode="group", yaxis2=dict(overlaying="y", side="right", title="ROAS", gridcolor="rgba(0,0,0,0)"))
    st.plotly_chart(styled_plotly(fig, 320), use_container_width=True)

elif page == "⎈ Ad spend playbook":
    st.title("Ad spend playbook")
    P = D["adPlaybook"]; M = P["months"]
    margin = grossMarginPct / 100; be = 1 / margin
    profitOf = lambda m: m["spend"] * 1000 * (m["roas"] * margin - 1)
    cuts = [m for m in M if m["action"] == "cut"]
    scales = [m for m in M if m["action"] == "scale"]
    lostLastYear = sum(min(0, profitOf(m)) for m in cuts)
    peak = max(scales, key=lambda m: m["roas"])

    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="hero-card" style="border-top:2px solid {NEG}"><div style="font-size:11px;text-transform:uppercase;color:{FAINT}">Lost in post-event slumps</div><div style="font-size:30px;font-weight:700;font-family:JetBrains Mono;color:{NEG};margin-top:8px">−{f0(abs(lostLastYear))}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="hero-card" style="border-top:2px solid {AMBER}"><div style="font-size:11px;text-transform:uppercase;color:{FAINT}">Break-even ROAS</div><div style="font-size:30px;font-weight:700;font-family:JetBrains Mono;color:{AMBER};margin-top:8px">{be:.2f}x</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="hero-card" style="border-top:2px solid {POS}"><div style="font-size:11px;text-transform:uppercase;color:{FAINT}">Best window to scale</div><div style="font-size:30px;font-weight:700;font-family:JetBrains Mono;color:{POS};margin-top:8px">{peak["m"]}</div><div style="font-size:11.5px;color:{MUTED};margin-top:4px">{peak["roas"]:.1f}x ROAS · {peak["note"]}</div></div>', unsafe_allow_html=True)

    st.subheader("ROAS by month vs break-even")
    colA = {"scale": "rgba(63,182,139,.85)", "hold": "rgba(224,163,62,.8)", "cut": "rgba(229,100,94,.85)"}
    fig = go.Figure()
    fig.add_bar(x=[m["m"] for m in M], y=[m["roas"] for m in M], name="ROAS",
        marker_color=[colA[m["action"]] for m in M])
    fig.add_scatter(x=[m["m"] for m in M], y=[be]*12, name="Break-even",
        line=dict(color=NEG, dash="dash"), mode="lines")
    st.plotly_chart(styled_plotly(fig, 320), use_container_width=True)

    st.subheader("Recommended budget schedule")
    mult = {"cut": 0.45, "hold": 1.0, "scale": 1.2}
    rec = [round(m["spend"] * mult[m["action"]]) for m in M]
    fig = go.Figure()
    fig.add_bar(x=[m["m"] for m in M], y=[m["spend"] for m in M], name="Last year", marker_color="rgba(91,141,239,.45)")
    fig.add_bar(x=[m["m"] for m in M], y=rec, name="Recommended", marker_color=[colA[m["action"]] for m in M])
    fig.update_layout(barmode="group")
    st.plotly_chart(styled_plotly(fig, 320), use_container_width=True)

    ad_tab1, ad_tab2, ad_tab3 = st.tabs(["📈 Scale months", "📉 Cut months", "📋 Full calendar"])
    with ad_tab1:
        st.subheader("↑ Scale up here")
        for m in scales:
            profit = profitOf(m)
            with st.expander(f"**{m['m']}** — {m['roas']:.1f}x ROAS · +{f0(profit)} profit · {m['note']}", expanded=False):
                m1, m2, m3 = st.columns(3)
                m1.metric("ROAS", f"{m['roas']:.1f}x")
                m2.metric("Spend (£k)", f"£{m['spend']}k")
                m3.metric("Profit from spend", f"+{f0(profit)}")
                recommended = round(m["spend"] * 1.2)
                st.markdown(f"""
                | Metric | Value |
                |--------|-------|
                | Last year spend | £{m['spend']}k |
                | Recommended spend | £{recommended}k (+20%) |
                | Expected revenue at {m['roas']:.1f}x | {f0(recommended * 1000 * m['roas'])} |
                | Context | {m['note']} |
                """)
                st.success(f"This is a scaling window. Budget should be {recommended}k+ to capitalize on {m['note'].lower()}.")
    with ad_tab2:
        st.subheader("↓ Pull spend back here")
        for m in cuts:
            loss = abs(profitOf(m))
            with st.expander(f"**{m['m']}** — {m['roas']:.1f}x ROAS · −{f0(loss)} lost · {m['note']}", expanded=False):
                m1, m2, m3 = st.columns(3)
                m1.metric("ROAS", f"{m['roas']:.1f}x", delta=f"{m['roas']-be:.2f}x vs break-even", delta_color="normal")
                m2.metric("Spend (£k)", f"£{m['spend']}k")
                m3.metric("Money lost", f"−{f0(loss)}")
                recommended = round(m["spend"] * 0.45)
                st.markdown(f"""
                | Metric | Value |
                |--------|-------|
                | Last year spend | £{m['spend']}k |
                | Recommended spend | £{recommended}k (−55%) |
                | Context | {m['note']} |
                | Savings vs last year | {f0((m['spend'] - recommended) * 1000)} |
                """)
                st.warning(f"Pull back significantly. Shift budget to email and retention during {m['note'].lower()}.")
    with ad_tab3:
        st.subheader("Full 12-month calendar")
        action_icon = {"scale": "📈", "hold": "⏸️", "cut": "📉"}
        for m in M:
            profit = profitOf(m)
            icon = action_icon[m["action"]]
            color = "green" if m["action"] == "scale" else ("orange" if m["action"] == "hold" else "red")
            st.markdown(f"{icon} **{m['m']}** — £{m['spend']}k spend · {m['roas']:.1f}x ROAS · {m['note']} · :{color}[{m['action'].upper()}]")

elif page == "★ Amazon-grade KPIs":
    st.title("Amazon-grade KPIs")
    K = D["amazonKpis"]
    gm = grossMarginPct / 100
    varFulfil = D["shippingOut"] + D["pickPackLabour"] + D["packaging"] + D["paymentFees"]
    cm1 = netRev - D["cogs"] - varFulfil
    cm2 = cm1 - marketing
    cm3 = cm2 - overheads
    dio = round(365 / invTurns)
    ccc = dio + K["ccc"]["dso"] - K["ccc"]["dpo"]
    firstOrderMargin = aov * gm
    paybackOrders = K["newCAC"] / firstOrderMargin

    mini_cards([
        ("MER", f"{D['grossRevenue']/marketing:.2f}x", "marketing efficiency"),
        ("CAC payback", f"{paybackOrders:.1f} orders", "time to recoup"),
        ("Cash conversion", f"{ccc} days", "cash locked up"),
        ("GMROI", "9.3", "margin per £ stock"),
        ("Order defect rate", "1.8%", "target ≤1%"),
        ("In-stock rate", "96.4%", "availability"),
    ])

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Contribution ladder — CM1 → CM2 → CM3")
        tiers = [("CM1", "after product & fulfilment", cm1, STEEL), ("CM2", "after marketing", cm2, VIOLET), ("CM3", "after fixed overheads", cm3, POS)]
        for l, sub, v, c in tiers:
            m = v / netRev * 100; per = v / D["orders"]
            st.markdown(f"""<div style="margin:14px 0">
            <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px;color:#E6E9EE">
            <span><b style="font-family:Space Grotesk;color:{c}">{l}</b> <small style="color:{FAINT}">{sub}</small></span>
            <span style="font-family:JetBrains Mono;font-size:12px">{f1(per)}/order · <span style="color:{c}">{m:.1f}%</span></span></div>
            <div style="height:9px;background:#1C232C;border-radius:5px;overflow:hidden"><div style="width:{m}%;height:100%;background:{c}"></div></div></div>""", unsafe_allow_html=True)
    with c2:
        st.subheader("Cash conversion cycle")
        cccParts = [("Days inventory held (DIO)", dio, "+", NEG), ("Days to collect cash (DSO)", K["ccc"]["dso"], "+", AMBER), ("Days to pay suppliers (DPO)", K["ccc"]["dpo"], "−", POS)]
        maxd = max(dio, K["ccc"]["dpo"], 30)
        for l, v, sign, c in cccParts:
            st.markdown(f"""<div style="margin:13px 0">
            <div style="display:flex;justify-content:space-between;font-size:12.5px;margin-bottom:5px;color:#E6E9EE"><span>{'less: ' if sign=='−' else ''}{l}</span><span style="color:{c};font-family:JetBrains Mono">{sign}{v}d</span></div>
            <div style="height:7px;background:#1C232C;border-radius:5px;overflow:hidden"><div style="width:{v/maxd*100}%;height:100%;background:{c}"></div></div></div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="plan-line hl"><span>Cash conversion cycle</span><b style="font-size:18px;color:{AMBER};font-family:JetBrains Mono">{ccc} days</b></div>""", unsafe_allow_html=True)

    st.subheader("CAC payback curve")
    orders = [1, 2, 3, 4, 5]
    cumMargin = [firstOrderMargin * n for n in orders]
    fig = go.Figure()
    fig.add_scatter(x=[f"Order {n}" for n in orders], y=cumMargin, name="Cumulative gross margin", fill="tozeroy",
        line=dict(color=POS), fillcolor="rgba(63,182,139,.12)")
    fig.add_scatter(x=[f"Order {n}" for n in orders], y=[K["newCAC"]]*5, name="CAC", line=dict(color=NEG, dash="dash"))
    st.plotly_chart(styled_plotly(fig, 280), use_container_width=True)

    st.subheader("Operational health scorecard")
    labFor = {"good": "On target", "warn": "Watch", "bad": "Fix now", "neutral": "Monitor"}
    iconFor = {"good": "🟢", "warn": "🟡", "bad": "🔴", "neutral": "🔵"}
    kpi_explanations = {
        "Marketing efficiency ratio (MER)": "Total revenue divided by total marketing spend. Shows how efficiently your entire marketing engine converts spend into revenue.",
        "Contribution margin (CM2)": "What's left after product costs, fulfilment, AND marketing. The money available to cover fixed costs and profit.",
        "CAC payback": "How many orders it takes to recoup the cost of acquiring a customer. Under 2 orders means fast payback.",
        "Cash conversion cycle": "Days between paying for inventory and collecting cash from customers. Lower is better — cash stays liquid.",
        "Month-on-month growth": "Revenue growth rate vs the previous month. Sustained 10%+ indicates healthy scaling.",
        "Repeat-purchase rate": "Percentage of customers who buy more than once. Higher repeat rate = lower reliance on paid acquisition.",
        "Net Promoter Score": "Would customers recommend you? 50+ is excellent. Drives organic growth through word-of-mouth.",
        "Average review rating": "Product quality signal. Below 4.5 causes conversion rate drops, especially on marketplaces.",
        "Contacts per order (CS load)": "How many customer service tickets per order. High ratio = product/shipping quality issues.",
        "New vs returning revenue": "Balance between acquisition and retention revenue. Heavy new-customer dependence is risky.",
        "In-stock / availability rate": "Percentage of SKUs available to buy. Stockouts = lost revenue and damaged ad efficiency.",
        "Lost sales from stockouts": "Revenue you couldn't capture because products were out of stock.",
        "GMROI (margin per £ of stock)": "Gross margin return on inventory investment. How hard your stock is working for you.",
        "Inventory turns (annualised)": "How many times you sell through your entire inventory per year. Higher = less cash tied up.",
        "Demand forecast accuracy": "How well you predict what will sell. Poor forecasts cause stockouts AND dead stock.",
        "Perfect-order rate": "Orders delivered on time, complete, undamaged, with correct invoice. The gold standard of fulfilment.",
        "Order defect rate (ODR)": "Percentage of orders with a defect (return, complaint, chargeback). Amazon suspends at 1%.",
        "On-time dispatch": "Orders shipped within the promised window. Late dispatch = poor reviews and repeat-purchase drops.",
        "Units per hour (packing)": "Warehouse productivity metric. Below 50 UPH means process inefficiency or training gaps.",
        "Fulfilment cost / order": "Total cost to pick, pack, and ship one order. Keep below £10.50 for healthy margins.",
        "Return rate": "Percentage of orders returned. Above 4% signals product quality or listing accuracy issues.",
        "Damage rate": "Orders damaged in transit. Above 0.5% = packaging or courier problems.",
    }
    for g in K["scorecard"]:
        with st.expander(f"**{g['group']}** — {sum(1 for r in g['rows'] if r['s']=='good')}/{len(g['rows'])} on target", expanded=False):
            for r in g["rows"]:
                icon = iconFor[r["s"]]
                status = labFor[r["s"]]
                st.markdown(f"{icon} **{r['m']}**: {r['v']} (target: {r['t']}) — *{status}*")
                explanation = kpi_explanations.get(r["m"], "")
                if explanation:
                    st.caption(explanation)
                if r["s"] == "bad":
                    st.error(f"Below target. Immediate action required to bring {r['m']} to {r['t']}.")
                elif r["s"] == "warn":
                    st.warning(f"Approaching risk zone. Monitor weekly and plan corrective action.")
                st.markdown("---")
