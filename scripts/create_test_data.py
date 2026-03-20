"""
Script de teste: cria 5 Leads e 5 Opportunities no Salesforce simultaneamente.
Lê as credenciais de src/main/resources/config.properties.
"""

import concurrent.futures
import os
import time
from datetime import date, timedelta
from pathlib import Path
import uuid

from simple_salesforce import Salesforce

# ── Leitura das credenciais ──────────────────────────────────────────────────
def load_config() -> dict:
    config_path = Path(__file__).parent.parent / "src" / "main" / "resources" / "config.properties"
    props = {}
    with open(config_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                props[k.strip()] = v.strip()
    return props

# ── Dados de teste ────────────────────────────────────────────────────────────
# Sufixo único por execução para evitar regra de duplicidade
_RUN_ID = str(int(time.time()))[-6:]

LEADS = [
    {"FirstName": "Alice",   "LastName": "Souza",    "Email": f"alice.souza.{_RUN_ID}@testcdc.io",    "Company": "TestCo 1", "Status": "Open - Not Contacted", "LeadSource": "Web"},
    {"FirstName": "Bruno",   "LastName": "Lima",     "Email": f"bruno.lima.{_RUN_ID}@testcdc.io",     "Company": "TestCo 2", "Status": "Open - Not Contacted", "LeadSource": "Phone Inquiry"},
    {"FirstName": "Carla",   "LastName": "Mendes",   "Email": f"carla.mendes.{_RUN_ID}@testcdc.io",   "Company": "TestCo 3", "Status": "Working - Contacted",  "LeadSource": "Partner Referral"},
    {"FirstName": "Diego",   "LastName": "Santos",   "Email": f"diego.santos.{_RUN_ID}@testcdc.io",   "Company": "TestCo 4", "Status": "Open - Not Contacted", "LeadSource": "Web"},
    {"FirstName": "Elaine",  "LastName": "Ferreira", "Email": f"elaine.ferreira.{_RUN_ID}@testcdc.io","Company": "TestCo 5", "Status": "Working - Contacted",  "LeadSource": "Internal"},
]

close_date = (date.today() + timedelta(days=30)).isoformat()  # ex: 2026-04-18

OPPORTUNITIES = [
    {"Name": "Opp CDC Test 1", "StageName": "Prospecting",    "CloseDate": close_date, "Amount": 10000.00, "Type": "New Business"},
    {"Name": "Opp CDC Test 2", "StageName": "Qualification",  "CloseDate": close_date, "Amount": 25000.00, "Type": "New Business"},
    {"Name": "Opp CDC Test 3", "StageName": "Needs Analysis", "CloseDate": close_date, "Amount": 50000.00, "Type": "Existing Business - Upgrade"},
    {"Name": "Opp CDC Test 4", "StageName": "Proposal/Price Quote", "CloseDate": close_date, "Amount": 75000.00, "Type": "New Business"},
    {"Name": "Opp CDC Test 5", "StageName": "Value Proposition","CloseDate": close_date, "Amount": 120000.00,"Type": "Existing Business - Renewal"},
]

# ── Funções de criação ────────────────────────────────────────────────────────
def create_lead(sf: Salesforce, lead: dict) -> dict:
    result = sf.Lead.create(lead)
    return {"type": "Lead", "name": f"{lead['FirstName']} {lead['LastName']}", "id": result["id"], "success": result["success"]}

def create_opportunity(sf: Salesforce, opp: dict) -> dict:
    result = sf.Opportunity.create(opp)
    return {"type": "Opportunity", "name": opp["Name"], "id": result["id"], "success": result["success"]}

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    config = load_config()

    username  = config["SF_USERNAME"]
    password  = config["SF_PASSWORD"]
    token     = config["SF_SECURITY_TOKEN"]
    auth_url  = config["SF_AUTHORIZATION_URL"]

    # Extrai o instance URL (ex: https://orgfarm-....my.salesforce.com)
    instance_url = auth_url.split("/services/")[0]

    print(f"Conectando ao Salesforce: {instance_url}")
    print(f"Usuário: {username}\n")

    sf = Salesforce(username=username, password=password, security_token=token,
                    instance_url=instance_url)

    tasks = (
        [(create_lead, lead) for lead in LEADS] +
        [(create_opportunity, opp)  for opp in OPPORTUNITIES]
    )

    print(f"Criando {len(LEADS)} Leads e {len(OPPORTUNITIES)} Opportunities simultaneamente...\n")
    start = time.time()

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fn, sf, data): (fn, data) for fn, data in tasks}
        for future in concurrent.futures.as_completed(futures):
            try:
                results.append(future.result())
            except Exception as exc:
                fn, data = futures[future]
                results.append({"type": fn.__name__, "error": str(exc), "success": False})

    elapsed = time.time() - start

    # Ordenar para exibição: Leads primeiro, depois Opportunities
    results.sort(key=lambda r: (r.get("type", ""), r.get("name", "")))

    leads_ok  = [r for r in results if r.get("type") == "Lead"        and r.get("success")]
    opps_ok   = [r for r in results if r.get("type") == "Opportunity" and r.get("success")]
    errors    = [r for r in results if not r.get("success")]

    print("=" * 60)
    print(f"RESULTADO  ({elapsed:.2f}s)")
    print("=" * 60)

    print(f"\n[OK] Leads criados ({len(leads_ok)}/5):")
    for r in leads_ok:
        print(f"  - {r['name']:25s}  id={r['id']}")

    print(f"\n[OK] Opportunities criadas ({len(opps_ok)}/5):")
    for r in opps_ok:
        print(f"  - {r['name']:25s}  id={r['id']}")

    if errors:
        print(f"\n[ERRO] Erros ({len(errors)}):")
        for r in errors:
            print(f"  - {r}")

    print("\nVerifique os eventos CDC no log do Mule e nas tabelas SQLite.")

if __name__ == "__main__":
    main()
