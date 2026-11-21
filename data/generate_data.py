"""Generates the synthetic CRM dataset for the Salesforce + Power BI + Excel sales pipeline project.
All names are fictional and all emails use example.com. No real people or companies.
Patterns (lead-source conversion, deal size, sales cycle, seasonality, rep performance) are built in
deliberately so the dashboards have something realistic to show. State this in the README."""
import csv, random, math, datetime as dt
random.seed(2026)
TODAY = dt.date(2026, 11, 5)
START = dt.date(2025, 1, 1)

CITY_REGION = {"Hamburg":"Nord","Hannover":"Nord","Bremen":"Nord","Berlin":"Ost","Leipzig":"Ost","Dresden":"Ost",
               "Cologne":"West","Düsseldorf":"West","Essen":"West","Munich":"Süd","Stuttgart":"Süd","Nuremberg":"Süd"}
CITIES = list(CITY_REGION)
INDUSTRIES = ["Manufacturing","Retail","Healthcare","Technology","Transportation","Finance","Energy","Education","Hospitality","Construction"]
IND_W = [18,14,10,16,10,9,6,5,6,6]
PREFIX = ["Nord","Süd","West","Ost","Alpha","Beta","Delta","Nova","Prima","Terra","Vita","Optima","Rhein","Elbe","Spree","Main","Zenit","Orion","Linea","Atlas","Aurum","Brevo","Corvus","Helio"]
SUFFIX = ["Systems","Solutions","Logistik","Werke","Handel","Technik","Consulting","Services","Digital","Group"]
FIRST = ["Anna","Ben","Clara","David","Elena","Felix","Greta","Hans","Ines","Jonas","Katrin","Lukas","Mara","Nico","Olga","Paul","Rita","Sven","Tina","Uwe","Vera","Willi","Yara","Zoe"]
LAST = ["Muster","Beispiel","Probe","Demo","Modell","Vorlage","Schmidt","Weber","Fischer","Meyer","Wagner","Becker","Hoffmann","Koch","Richter","Klein","Wolf","Neumann"]
TITLES = ["Purchasing Manager","IT Manager","Head of Sales","CFO","Operations Lead","Marketing Manager","CEO","Data Lead"]

SOURCES = ["Web","Partner Referral","LinkedIn","Trade Show","Email Campaign","Phone Inquiry"]
SRC_W = [28,10,22,12,18,10]
LEAD_TO_OPP = {"Web":0.08,"Partner Referral":0.30,"LinkedIn":0.16,"Trade Show":0.14,"Email Campaign":0.06,"Phone Inquiry":0.12}
WIN_BASE = {"Partner Referral":0.55,"LinkedIn":0.38,"Trade Show":0.34,"Phone Inquiry":0.36,"Web":0.28,"Email Campaign":0.24,"Existing Customer":0.62}
CYCLE = {"Partner Referral":38,"LinkedIn":55,"Trade Show":62,"Phone Inquiry":50,"Web":70,"Email Campaign":78,"Existing Customer":30}
REPS = {"Anna Keller":1.10,"Markus Brandt":1.00,"Sofia Lehmann":1.15,"Jonas Richter":0.85,"Lea Hartmann":1.00,"Tim Vogel":0.90}
REP_REGION = {"Nord":["Markus Brandt","Lea Hartmann"],"Ost":["Anna Keller","Tim Vogel"],"West":["Sofia Lehmann","Jonas Richter"],"Süd":["Anna Keller","Jonas Richter","Tim Vogel"]}
PRODUCTS = {"Analytics Suite":45000,"Cloud Hosting":30000,"Support Plan":12000,"Training":6000}
PROD_W = [30,30,25,15]
OPEN_STAGES = ["Qualification","Needs Analysis","Value Proposition","Proposal/Price Quote","Negotiation/Review"]
STAGE_PROB = {"Qualification":0.10,"Needs Analysis":0.20,"Value Proposition":0.40,"Proposal/Price Quote":0.60,"Negotiation/Review":0.80}
# quarter-end months close more deals
MONTH_BOOST = {3:1.4,6:1.4,9:1.4,12:1.6,1:0.8,2:0.9,7:0.8,8:0.8}

def wchoice(items, weights): return random.choices(items, weights=weights)[0]
def write(name, rows):
    with open(name, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
def rand_date(a, b): return a + dt.timedelta(days=random.randint(0, (b - a).days))

# ---------- Accounts ----------
accounts, used = [], set()
while len(accounts) < 70:
    n = f"{random.choice(PREFIX)} {random.choice(SUFFIX)} GmbH"
    if n in used: continue
    used.add(n)
    city = random.choice(CITIES); emp = int(random.choice([20,50,100,250,500,1000,2000]) * random.uniform(0.8,1.2))
    accounts.append({"Account_Code":f"ACC-{len(accounts)+1:03d}","Name":n,"Industry":wchoice(INDUSTRIES,IND_W),
        "BillingCity":city,"BillingCountry":"Germany","Region__c":CITY_REGION[city],
        "NumberOfEmployees":emp,"AnnualRevenue":int(emp*random.uniform(90000,160000)//1000*1000),
        "Type":wchoice(["Prospect","Customer - Direct","Channel Partner / Reseller"],[40,50,10])})
write("accounts.csv", accounts)

# ---------- Contacts ----------
contacts = []
for i in range(140):
    a = random.choice(accounts); fn, ln = random.choice(FIRST), random.choice(LAST)
    contacts.append({"FirstName":fn,"LastName":ln,"Account Name":a["Name"],"Title":random.choice(TITLES),
        "Email":f"{fn.lower()}.{ln.lower()}.{i}@example.com","MailingCity":a["BillingCity"]})
write("contacts.csv", contacts)

# ---------- Leads (800, Jan 2025 - Oct 2026, growing trend) ----------
months = []
d = START
while d <= dt.date(2026, 10, 31):
    months.append(d); d = (d.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
mw = [1 + 0.03*i for i in range(len(months))]
leads = []
for i in range(800):
    m = wchoice(months, mw)
    created = m + dt.timedelta(days=random.randint(0, 27))
    if created > dt.date(2026, 10, 31): created = dt.date(2026, 10, 31)
    src = wchoice(SOURCES, SRC_W); age = (TODAY - created).days
    if age < 30: status = wchoice(["Open - Not Contacted","Working - Contacted"],[55,45])
    elif age < 120: status = wchoice(["Open - Not Contacted","Working - Contacted","Closed - Not Converted"],[20,50,30])
    else: status = wchoice(["Open - Not Contacted","Working - Contacted","Closed - Not Converted"],[10,30,60])
    fn, ln = random.choice(FIRST), random.choice(LAST); city = random.choice(CITIES)
    leads.append({"FirstName":fn,"LastName":ln,"Company":f"{random.choice(PREFIX)} {random.choice(SUFFIX)} (Lead {i+1:03d})",
        "Email":f"{fn.lower()}.{ln.lower()}.lead{i}@example.com","LeadSource":src,"Status":status,
        "Industry":wchoice(INDUSTRIES,IND_W),"Rating":wchoice(["Hot","Warm","Cold"],[20,40,40]),
        "City":city,"Country":"Germany","Lead_Created_Date__c":created.isoformat()})
write("leads.csv", leads)

# ---------- Opportunities ----------
def make_opp(acct, src, opp_created, opp_type):
    prod = wchoice(list(PRODUCTS), PROD_W)
    size = 0.6 + min(acct["NumberOfEmployees"], 2000)/2000*1.2
    amount = int(max(2000, random.lognormvariate(math.log(PRODUCTS[prod]*size), 0.35)) // 100 * 100)
    cycle = max(7, int(random.gauss(CYCLE[src], 14)))
    close = opp_created + dt.timedelta(days=cycle)
    rep = random.choice(REP_REGION[acct["Region__c"]])
    return prod, amount, close, rep

opps = []
def finalize(acct, src, created, otype, n):
    if created > TODAY: return
    prod, amount, close, rep = make_opp(acct, src, created, otype)
    # shift some closes into quarter-end months
    if random.random() < 0.35:
        qm = [m for m in (3,6,9,12) if m >= close.month]
        if qm:
            m = qm[0]; day = random.randint(15, 28); close = close.replace(month=m, day=day)
    if close <= TODAY:
        p = WIN_BASE[src] * REPS[rep] * (0.8 if amount > 60000 else 1.0) * MONTH_BOOST.get(close.month,1.0)**0.5
        stage = "Closed Won" if random.random() < min(p, 0.85) else "Closed Lost"
    else:
        stage = wchoice(OPEN_STAGES, [15,25,25,20,15])
    opps.append({"Name":f"{acct['Name']} - {prod} ({n:03d})","AccountName":acct["Name"],"StageName":stage,"Amount":amount,
        "CloseDate":close.isoformat(),"LeadSource":src,"Type":otype,"Sales_Rep__c":rep,"Product_Line__c":prod,
        "Opp_Created_Date__c":created.isoformat()})

n = 0
for L in leads:   # opportunities that come from leads
    if random.random() < LEAD_TO_OPP[L["LeadSource"]]:
        n += 1
        created = dt.date.fromisoformat(L["Lead_Created_Date__c"]) + dt.timedelta(days=random.randint(5, 40))
        finalize(random.choice(accounts), L["LeadSource"], created, "New Customer", n)
for i in range(90):   # upsell / renewal opportunities from existing customers (not from leads)
    n += 1
    finalize(random.choice([a for a in accounts if a["Type"]!="Prospect"]), "Existing Customer", rand_date(START, TODAY), "Existing Customer - Upgrade", n)

for i in range(35):   # additional open pipeline created in the last ~2 months
    n += 1
    acct = random.choice(accounts)
    src = wchoice(SOURCES + ["Existing Customer"], SRC_W + [20])
    otype = "Existing Customer - Upgrade" if src == "Existing Customer" else "New Customer"
    created = rand_date(TODAY - dt.timedelta(days=60), TODAY - dt.timedelta(days=3))
    prod = wchoice(list(PRODUCTS), PROD_W)
    size = 0.6 + min(acct["NumberOfEmployees"], 2000)/2000*1.2
    amount = int(max(2000, random.lognormvariate(math.log(PRODUCTS[prod]*size), 0.35)) // 100 * 100)
    close = TODAY + dt.timedelta(days=random.randint(10, 120))
    opps.append({"Name":f"{acct['Name']} - {prod} ({n:03d})","AccountName":acct["Name"],"StageName":wchoice(OPEN_STAGES,[15,25,25,20,15]),
        "Amount":amount,"CloseDate":close.isoformat(),"LeadSource":src,"Type":otype,"Sales_Rep__c":random.choice(REP_REGION[acct["Region__c"]]),
        "Product_Line__c":prod,"Opp_Created_Date__c":created.isoformat()})
opps.sort(key=lambda r: r["Opp_Created_Date__c"])
write("opportunities.csv", opps)

# ---------- Reference totals for reconciliation ----------
won = [o for o in opps if o["StageName"]=="Closed Won"]; lost = [o for o in opps if o["StageName"]=="Closed Lost"]
open_ = [o for o in opps if not o["StageName"].startswith("Closed")]
ref = [("accounts",len(accounts)),("contacts",len(contacts)),("leads",len(leads)),("opportunities",len(opps)),
       ("closed_won_count",len(won)),("closed_lost_count",len(lost)),("open_count",len(open_)),
       ("closed_won_amount",sum(int(o["Amount"]) for o in won)),("open_pipeline_amount",sum(int(o["Amount"]) for o in open_)),
       ("win_rate_pct",round(100*len(won)/(len(won)+len(lost)),1))]
with open("reference_totals.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["metric","value"]); w.writerows(ref)
for k,v in ref: print(k,v)
