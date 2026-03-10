#!/usr/bin/env python3
"""Post-process state_mapping.csv to resolve ambiguous/unknown entries."""
import csv

# Manual overrides for ambiguous entries
OVERRIDES = {
    # US cities
    "Cruz": "California",           # Santa Cruz area
    "L.A.": "California",
    "Berkley": "California",
    "Bell": "California",
    "Hercules": "California",
    "Atwater": "California",
    "Banning": "California",
    "Angeles": "California",
    "Angeles C": "California",
    "Jose C": "California",
    "Silverado": "California",
    "Leandro C": "California",
    "Bernardino C": "California",
    "Bay Area": "California",
    "Rosa C": "California",
    "Diego C": "California",
    "Diego C.": "California",
    "Sonoma County": "California",
    "San Francisco Bay Area": "California",
    "Colchester Co": "California",

    "Bryan": "Texas",
    "Bellaire": "Texas",
    "Wharton": "Texas",
    "Harris": "Texas",
    "Graham": "Texas",
    "Fairview": "Texas",
    "Brownwood": "Texas",
    "Uvalde": "Texas",
    "Kaufman": "Texas",
    "Universal City Texs": "Texas",
    "Galveston": "Texas",
    "Bc Texas": "Texas",
    "Antonio Texas": "Texas",
    "Falls Co": "Texas",

    "Stuart": "Florida",
    "Summerfield": "Florida",
    "Lauderhill": "Florida",
    "Pines": "Florida",            # Pembroke Pines FL
    "South Miami": "Florida",

    "Jersey": "New Jersey",
    "N.J.": "New Jersey",
    "Belmar": "New Jersey",
    "Rutherford": "New Jersey",
    "Pleasantville": "New Jersey",
    "Wenonah": "New Jersey",
    "Bedminster": "New Jersey",
    "Sewell": "New Jersey",
    "Roslyn": "New York",

    "Attica": "New York",
    "Sullivan": "New York",
    "Bellerose": "New York",
    "Bellaire": "Texas",

    "Powell": "Ohio",
    "Coshocton": "Ohio",

    "Davidson": "Tennessee",       # Davidson County TN (Nashville)
    "Gallatin": "Tennessee",

    "Lenoir": "North Carolina",
    "/ Wake County": "North Carolina",
    "Pinehurst": "North Carolina",
    "Boone": "North Carolina",

    "Spotsylvania": "Virginia",
    "Warrenton": "Virginia",
    "Powhatan": "Virginia",

    "Logan": "Utah",
    "Pendleton": "Oregon",
    "Russellville": "Arkansas",
    "Bryant": "Arkansas",
    "Baxter": "Arkansas",          # Baxter County AR

    "N.H.": "New Hampshire",
    "Seabrook": "New Hampshire",

    "Cloud": "Minnesota",          # St. Cloud MN
    "Zimmerman": "Minnesota",

    "Holland": "Michigan",
    "Freeland": "Michigan",
    "Kalkaska": "Michigan",

    "Superior": "Wisconsin",
    "Menomonie": "Wisconsin",

    "Celina": "Ohio",
    "Irwin": "Pennsylvania",
    "Enola": "Pennsylvania",
    "Butler": "Pennsylvania",

    "Townsend": "Montana",

    "Fenton": "Michigan",
    "Berea": "Kentucky",

    "Nouveau-Mexique": "New Mexico",

    "Western Mass": "Massachusetts",
    "Western Massachusetts": "Massachusetts",

    "Bellaire": "Texas",

    "Pendleton": "Oregon",

    # Ambiguous generics -> unknown/invalid
    "City": "unknown/invalid",
    "Harbor": "unknown/invalid",
    "Springs": "unknown/invalid",
    "Headquarters": "unknown/invalid",
    "Western": "unknown/invalid",
    "Heights": "unknown/invalid",
    "West Coast": "unknown/invalid",
    "Northwest": "unknown/invalid",
    "Address": "unknown/invalid",
    "Beach": "unknown/invalid",
    "Southeast": "unknown/invalid",
    "Region": "unknown/invalid",
    "Dora": "unknown/invalid",
    "Holly": "unknown/invalid",
    "Smithfield": "unknown/invalid",
    "Jasper": "unknown/invalid",
    "State": "unknown/invalid",
    "Roads": "unknown/invalid",
    "Central": "unknown/invalid",
    "East": "unknown/invalid",
    "West": "unknown/invalid",
    "Rock": "unknown/invalid",
    "Bridge": "unknown/invalid",
    "Creek": "unknown/invalid",
    "Islands": "unknown/invalid",
    "Centro": "unknown/invalid",
    "Southeastern": "unknown/invalid",
    "Clark": "unknown/invalid",
    "Jefferson": "unknown/invalid",
    "Fayette": "unknown/invalid",
    "States": "unknown/invalid",
    "John": "unknown/invalid",
    "Wells": "unknown/invalid",
    "Bedford": "unknown/invalid",
    "Underwood": "unknown/invalid",
    "United States": "unknown/invalid",
    "University-Wide": "unknown/invalid",
    "Usa": "unknown/invalid",
    "Usa +---": "unknown/invalid",
    "Usa / Colorado": "Colorado",
    "America": "unknown/invalid",
    "Airports": "unknown/invalid",
    "Avenue": "unknown/invalid",
    "Aviation": "unknown/invalid",
    "Amelia": "unknown/invalid",
    "WcX Lr": "unknown/invalid",
    "Ub Lx": "unknown/invalid",
    "Ub Sl": "unknown/invalid",
    "Jpssm": "unknown/invalid",
    "Tw": "unknown/invalid",
    "Tw Bb": "unknown/invalid",
    "Tw Bx": "unknown/invalid",
    "Tw Dh": "unknown/invalid",
    "Tw Eb": "unknown/invalid",
    "Tw Ht": "unknown/invalid",
    "Tw Ss": "unknown/invalid",
    "Atwood": "unknown/invalid",
    "West Coast Region": "unknown/invalid",
    "Western Region": "unknown/invalid",
    "Westlands": "unknown/invalid",
    "Bailey": "unknown/invalid",
    "Vernon": "unknown/invalid",
    "tat-Unis": "unknown/invalid",

    # Non-USA
    "Kong": "not-usa",           # Hong Kong
    "Qubec": "not-usa",          # Quebec, Canada
    "Zuid Holland": "not-usa",
    "South Holland": "not-usa",  # Netherlands
    "Nouveau-Mexique": "New Mexico",  # French for New Mexico
    "Lisboa": "not-usa",         # Lisbon
    "Tunis": "not-usa",
    "Distrito Capital": "not-usa",  # Venezuela
    "Western Province": "not-usa",
    "Mxico": "not-usa",
    "Nottingham": "not-usa",      # UK city
    "Fife": "not-usa",            # Scotland
    "Hants": "not-usa",           # Hampshire UK
    "Isle Of Wight": "not-usa",
    "Zrich": "not-usa",           # Zurich
    "Twickenham": "not-usa",
    "Veszprem": "not-usa",        # Hungary
    "Upper Hutt": "not-usa",      # NZ
    "Bay Of Plenty": "not-usa",   # NZ
    "Ulster": "not-usa",          # Northern Ireland
    "Usvi": "Virgin Islands",
    "Ben Arous": "not-usa",       # Tunisia
    "Venezia": "not-usa",
    "Bamber Bridge": "not-usa",   # UK
    "Baleares": "not-usa",        # Spain
    "Balkesir": "not-usa",        # Turkey
    "Ballymena County Antrim": "not-usa",
    "Basildon": "not-usa",        # UK
    "Vung Tau": "not-usa",        # Vietnam
    "Vlaams-Brabant": "not-usa",
    "Babil": "not-usa",           # Iraq
    "Bacau": "not-usa",           # Romania
    "Badajoz": "not-usa",         # Spain
    "Baden Wrttemberg": "not-usa",
    "Baden-Wrttemberg": "not-usa",
    "West Indies": "not-usa",
    "Attiki": "not-usa",          # Greece
    "Aydn": "not-usa",            # Turkey
    "Ayutthaya": "not-usa",       # Thailand
    "Zaragoza": "not-usa",
    "Zh Zuid Holland": "not-usa",
    "Zhangjiagang City": "not-usa",
    "ita Prefecture": "not-usa",  # Japan
    "Zhuzhou": "not-usa",
    "Ziud-Holland": "not-usa",
    "Zamboanga Sibugay": "not-usa",
    "Zuid Holland Noord": "not-usa",
    "Amritsar": "not-usa",
    "Kalmar County": "not-usa",   # Sweden
    "Kampong Speu": "not-usa",
    "Kayes": "not-usa",           # Mali
    "Jambi": "not-usa",
    "Aires": "not-usa",           # Buenos Aires
    "Binh Dinh": "not-usa",
    "Bom Jardim": "not-usa",
    "Bondi Junction": "not-usa",
    "Bologna": "not-usa",
    "Blagoevgrad": "not-usa",     # Bulgaria
    "Bogot D.C.": "not-usa",
    "Bishop": "California",
    "Bklyn": "New York",          # Brooklyn
    "Bluemont": "Virginia",
    "Blandon": "Pennsylvania",
    "Banning": "California",
    "Bayern": "not-usa",          # Germany
    "Bp": "unknown/invalid",
}


def main():
    rows = []
    with open('/home/harshit.p/agent/state_mapping.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    changed = 0
    for row in rows:
        if row['mapped_state'] == 'ambiguous/unknown':
            orig = row['original_entry']
            if orig in OVERRIDES:
                row['mapped_state'] = OVERRIDES[orig]
                changed += 1

    with open('/home/harshit.p/agent/state_mapping.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['original_entry', 'mapped_state', 'count'])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Fixed {changed} entries.")

    # Count remaining ambiguous
    remaining = [r['original_entry'] for r in rows if r['mapped_state'] == 'ambiguous/unknown']
    print(f"Still ambiguous: {len(remaining)}")


if __name__ == '__main__':
    main()
