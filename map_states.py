#!/usr/bin/env python3
import re
import csv

# Canonical US state names
US_STATE_LIST = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming",
    "District of Columbia",
    # Territories (map to their own name)
    "Puerto Rico", "Guam", "American Samoa", "Northern Mariana Islands",
    "Virgin Islands",
]

# State abbreviation -> canonical name
ABBREV = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
    "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska",
    "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NY": "New York", "NC": "North Carolina",
    "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon",
    "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
    "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming",
    "DC": "District of Columbia", "PR": "Puerto Rico", "GU": "Guam",
    "AS": "American Samoa", "VI": "Virgin Islands",
}

# US city -> state
CITY_TO_STATE = {
    # California cities
    "los angeles": "California", "san francisco": "California",
    "san diego": "California", "san jose": "California",
    "sacramento": "California", "fresno": "California",
    "long beach": "California", "oakland": "California",
    "bakersfield": "California", "anaheim": "California",
    "santa ana": "California", "riverside": "California",
    "stockton": "California", "irvine": "California",
    "chula vista": "California", "fremont": "California",
    "san bernardino": "California", "modesto": "California",
    "fontana": "California", "moreno valley": "California",
    "glendale": "California", "oxnard": "California",
    "huntington beach": "California", "garden grove": "California",
    "santa clarita": "California", "ocean side": "California",
    "oceanside": "California", "el monte": "California",
    "corona": "California", "chatsworth": "California",
    "rancho cucamonga": "California", "ontario": "California",
    "hayward": "California", "pomona": "California",
    "sunnyvale": "California", "escondido": "California",
    "torrance": "California", "pasadena": "California",
    "fullerton": "California", "orange": "California",
    "roseville": "California", "elk grove": "California",
    "concord": "California", "salinas": "California",
    "thousand oaks": "California", "visalia": "California",
    "simi valley": "California", "santa rosa": "California",
    "vallejo": "California", "palmdale": "California",
    "corona": "California", "sunnyvale": "California",
    "berkeley": "California", "palo alto": "California",
    "san mateo": "California", "santa cruz": "California",
    "redwood city": "California", "burlingame": "California",
    "whittier": "California", "costa mesa": "California",
    "chino": "California", "walnut creek": "California",
    "mountain view": "California", "beverly hills": "California",
    "santa barbara": "California", "napa": "California",
    "ventura": "California", "laguna": "California",
    "woodland hills": "California", "panorama city": "California",
    "fountain valley": "California", "gardena": "California",
    "milpitas": "California", "daly city": "California",
    "santa clara": "California", "cupertino": "California",
    "san ramon": "California", "pleasanton": "California",
    "livermore": "California", "antioch": "California",
    "richmond": "California", "compton": "California",
    "downey": "California", "inglewood": "California",
    "murrieta": "California", "temecula": "California",
    "el cajon": "California", "santee": "California",
    "carlsbad": "California", "vista": "California",
    "ramona": "California", "san joaquin": "California",
    "whittier": "California", "bellflower": "California",
    "bell gardens": "California", "colton": "California",
    "rialto": "California", "redondo beach": "California",
    "pacifica": "California", "san marcos": "California",
    "san luis": "California", "san lorenzo": "California",
    "escondido": "California", "glendora": "California",
    "palmdale": "California", "hemet": "California",
    "orange county": "California", "los angeles county": "California",
    "san francisco bay area": "California",
    "southern california": "California",
    "sebastopol": "California", "larkspur": "California",
    "belvedere-tiburon": "California", "tiburon": "California",
    "walnut": "California", "la jolla": "California",
    "san antonio": "California",  # note: there's also San Antonio TX; will handle below
    "alameda": "California", "alamo": "California",
    "campbell": "California", "los gatos": "California",
    "morgan hill": "California", "gilroy": "California",
    "watsonville": "California", "aptos": "California",
    "oakhurst": "California", "merced": "California",
    "turlock": "California", "clovis": "California",
    "tulare": "California", "porterville": "California",
    "delano": "California", "madera": "California",
    "hanford": "California", "lodi": "California",
    "manteca": "California", "tracy": "California",
    "petaluma": "California", "rohnert park": "California",
    "sebastopol": "California", "sonoma": "California",
    "ukiah": "California", "redding": "California",
    "chico": "California", "paradise": "California",
    "yuba city": "California", "marysville": "California",
    "glendale": "California", "burbank": "California",
    "alhambra": "California", "west covina": "California",
    "norwalk": "California", "torrance": "California",
    "bellflower": "California", "hawthorne": "California",
    "inglewood": "California", "culver city": "California",
    "el segundo": "California", "manhattan beach": "California",
    "redondo beach": "California", "hermosa beach": "California",
    "san pedro": "California", "wilmington": "California",
    "lomita": "California", "carson": "California",
    "lakewood": "California", "cerritos": "California",
    "artesia": "California", "hawaiian gardens": "California",
    "signal hill": "California", "seal beach": "California",
    "cypress": "California", "los alamitos": "California",
    "stanton": "California", "buena park": "California",
    "la habra": "California", "brea": "California",
    "yorba linda": "California", "placentia": "California",
    "villa park": "California", "tustin": "California",
    "el toro": "California", "laguna hills": "California",
    "laguna niguel": "California", "laguna beach": "California",
    "dana point": "California", "san clemente": "California",
    "mission viejo": "California", "lake forest": "California",
    "aliso viejo": "California", "rancho santa margarita": "California",
    "coto de caza": "California", "trabuco canyon": "California",
    "silverado": "California",
    # Texas cities
    "houston": "Texas", "dallas": "Texas", "san antonio": "Texas",
    "austin": "Texas", "fort worth": "Texas", "el paso": "Texas",
    "arlington": "Texas", "corpus christi": "Texas", "plano": "Texas",
    "laredo": "Texas", "lubbock": "Texas", "irving": "Texas",
    "garland": "Texas", "amarillo": "Texas", "grand prairie": "Texas",
    "mckinney": "Texas", "frisco": "Texas", "mesquite": "Texas",
    "killeen": "Texas", "mcallen": "Texas", "pasadena": "Texas",
    "midland": "Texas", "waco": "Texas", "denton": "Texas",
    "abilene": "Texas", "beaumont": "Texas", "round rock": "Texas",
    "odessa": "Texas", "tyler": "Texas", "richardson": "Texas",
    "lewisville": "Texas", "wichita falls": "Texas",
    "carrollton": "Texas", "college station": "Texas",
    "pearland": "Texas", "sugar land": "Texas", "sugarland": "Texas",
    "the woodlands texas": "Texas", "the woodlands": "Texas",
    "rockwall": "Texas", "conroe": "Texas", "new braunfels": "Texas",
    "cedar park": "Texas", "georgetown": "Texas",
    "allen": "Texas", "flower mound": "Texas",
    "san marcos": "Texas", "katy": "Texas",
    "weatherford": "Texas", "cleburne": "Texas",
    "longview": "Texas", "midland": "Texas",
    "fort worth": "Texas", "fort-worth": "Texas",
    "ft. worth": "Texas", "ft worth": "Texas",
    "texarkana": "Texas", "bullard": "Texas",
    "groesbeck": "Texas", "hewitt": "Texas",
    "kemah": "Texas", "huffman": "Texas",
    "antonio texas": "Texas",
    # New York cities
    "new york city": "New York", "nyc": "New York",
    "buffalo": "New York", "rochester": "New York",
    "yonkers": "New York", "syracuse": "New York",
    "albany": "New York", "new rochelle": "New York",
    "mount vernon": "New York", "schenectady": "New York",
    "utica": "New York", "white plains": "New York",
    "poughkeepsie": "New York", "troy": "New York",
    "tarrytown": "New York", "scarsdale": "New York",
    "larchmont": "New York", "bronxville": "New York",
    "rye": "New York", "port chester": "New York",
    "greenwich": "New York",  # may also be CT
    "valhalla": "New York", "mamaroneck": "New York",
    "tuckahoe": "New York", "pelham": "New York",
    "eastchester": "New York", "yonkers": "New York",
    "jersey city": "New Jersey",  # NJ not NY
    "brooklyn": "New York", "manhattan": "New York",
    "bronx": "New York", "queens": "New York",
    "staten island": "New York", "harlem": "New York",
    "long island": "New York", "flushing": "New York",
    "astoria": "New York", "jamaica": "New York",
    "syosset": "New York", "inwood": "New York",
    "hollis": "New York", "merrick": "New York",
    "lynbrook": "New York", "cedarhurst": "New York",
    "rockaway": "New York", "penfield": "New York",
    "northport": "New York", "north port": "New York",
    "rensselaer": "New York", "endicott": "New York",
    "northbridge": "New York", "ridgewood": "New York",
    "beachwood": "New York",  # could also be OH
    "islip": "New York",
    # Florida cities
    "miami": "Florida", "orlando": "Florida", "tampa": "Florida",
    "jacksonville": "Florida", "st. petersburg": "Florida",
    "hialeah": "Florida", "tallahassee": "Florida",
    "fort lauderdale": "Florida", "ft lauderdale": "Florida",
    "ft. lauderdale": "Florida", "port st. lucie": "Florida",
    "cape coral": "Florida", "pembroke pines": "Florida",
    "hollywood": "Florida", "gainesville": "Florida",
    "miramar": "Florida", "coral springs": "Florida",
    "clearwater": "Florida", "west palm beach": "Florida",
    "boca raton": "Florida", "pompano beach": "Florida",
    "daytona": "Florida", "lakeland": "Florida",
    "davie": "Florida", "miami-dade": "Florida",
    "miami dade": "Florida", "fort worth": "Florida",  # no
    "apopka": "Florida", "oldsmar": "Florida",
    "largo": "Florida", "palm beach": "Florida",
    "naples": "Florida", "sarasota": "Florida",
    "pensacola": "Florida", "melbourne": "Florida",
    "deland": "Florida", "cocoa": "Florida",
    "rockledge": "Florida", "brevard": "Florida",
    "fort lauderdale area": "Florida",
    "lauderdale": "Florida", "plantation": "Florida",
    "weston": "Florida", "davie": "Florida",
    "sunrise": "Florida", "deerfield": "Florida",
    "margate": "Florida", "coconut grove": "Florida",
    "homestead": "Florida", "key west": "Florida",
    "boynton beach": "Florida", "delray beach": "Florida",
    "lake worth": "Florida", "riviera beach": "Florida",
    "jupiter": "Florida", "palm beach gardens": "Florida",
    "tequesta": "Florida", "vero beach": "Florida",
    "sebastian": "Florida", "ferndale": "Florida",
    "fort pierce": "Florida", "port saint lucie": "Florida",
    "ocala": "Florida", "leesburg": "Florida",
    "eustis": "Florida", "tavares": "Florida",
    "clermont": "Florida", "kissimmee": "Florida",
    "sanford": "Florida", "deltona": "Florida",
    "daytona beach": "Florida", "new smyrna beach": "Florida",
    "titusville": "Florida", "cocoa beach": "Florida",
    "south miami": "Florida", "hialeah": "Florida",
    "miami springs": "Florida", "miami-gardens": "Florida",
    "north miami beach": "Florida", "aventura": "Florida",
    "sunny isles beach": "Florida", "bay harbor islands": "Florida",
    "opa-locka": "Florida", "miami-dade county": "Florida",
    "tallahassee": "Florida", "pensacola": "Florida",
    "panama city": "Florida", "fort walton beach": "Florida",
    "crestview": "Florida", "navarre": "Florida",
    "clearfield": "Florida",  # actually PA
    "auburndale": "Florida", "lakeland": "Florida",
    "tampa": "Florida", "brandon": "Florida",
    "riverview": "Florida", "plant city": "Florida",
    "winter haven": "Florida", "bartow": "Florida",
    "avon park": "Florida", "sebring": "Florida",
    "okeechobee": "Florida", "fort myers": "Florida",
    "cape coral": "Florida", "bonita springs": "Florida",
    "estero": "Florida", "marco island": "Florida",
    "naples": "Florida", "sarasota": "Florida",
    "bradenton": "Florida", "venice": "Florida",
    "englewood": "Florida", "port charlotte": "Florida",
    "punta gorda": "Florida", "charlotte harbor": "Florida",
    "starke": "Florida", "oldsmar": "Florida",
    "seminole": "Florida", "dade city": "Florida",
    "zephyrhills": "Florida", "new port richey": "Florida",
    "holiday": "Florida", "dunedin": "Florida",
    "palmetto": "Florida", "bradenton": "Florida",
    "st. croix": "Virgin Islands",
    "sarasota-bradenton": "Florida",
    "orange park": "Florida", "green cove springs": "Florida",
    "st. johns county": "Florida",
    "fort lauderdale": "Florida",
    "winter park": "Florida", "casselberry": "Florida",
    "oviedo": "Florida", "longwood": "Florida",
    "sanford": "Florida", "lake mary": "Florida",
    "debary": "Florida",
    # Illinois cities
    "chicago": "Illinois", "aurora": "Illinois",
    "rockford": "Illinois", "joliet": "Illinois",
    "naperville": "Illinois", "springfield": "Illinois",
    "peoria": "Illinois", "elgin": "Illinois",
    "waukegan": "Illinois", "champaign": "Illinois",
    "bloomington": "Illinois", "decatur": "Illinois",
    "evanston": "Illinois", "schaumburg": "Illinois",
    "bolingbrook": "Illinois", "palatine": "Illinois",
    "skokie": "Illinois", "des plaines": "Illinois",
    "orland park": "Illinois", "tinley park": "Illinois",
    "oak lawn": "Illinois", "berwyn": "Illinois",
    "mount prospect": "Illinois", "normal": "Illinois",
    "wheaton": "Illinois", "downers grove": "Illinois",
    "addison": "Illinois", "hoffman estates": "Illinois",
    "belleville": "Illinois", "urbana": "Illinois",
    "northbrook": "Illinois", "glenview": "Illinois",
    "hinsdale": "Illinois", "barrington": "Illinois",
    "winnetka": "Illinois", "itasca": "Illinois",
    "algonquin": "Illinois", "huntley": "Illinois",
    "woodridge": "Illinois", "bridgeview": "Illinois",
    "brookfield": "Illinois", "kankakee": "Illinois",
    "southgate": "Illinois", "westmont": "Illinois",
    "deerfield": "Illinois", "elmhurst": "Illinois",
    "oakton": "Illinois",
    "urbana-champaign": "Illinois", "chicagoland": "Illinois",
    "chicago-land": "Illinois", "chicago-north": "Illinois",
    "southern illinois": "Illinois",
    "mt. prospect": "Illinois",
    "gurnee": "Illinois", "lake county": "Illinois",
    "lake bluff": "Illinois", "libertyville": "Illinois",
    "waukegan": "Illinois", "north chicago": "Illinois",
    "winthrop harbor": "Illinois", "zion": "Illinois",
    "round lake beach": "Illinois", "grayslake": "Illinois",
    "lindenhurst": "Illinois", "antioch": "Illinois",
    "fox lake": "Illinois", "crystal lake": "Illinois",
    "mchenry": "Illinois", "woodstock": "Illinois",
    "marengo": "Illinois", "belvidere": "Illinois",
    "roscoe": "Illinois", "machesney park": "Illinois",
    "loves park": "Illinois", "cherry valley": "Illinois",
    "rockford": "Illinois", "freeport": "Illinois",
    "galena": "Illinois", "dixon": "Illinois",
    "dekalb": "Illinois", "sycamore": "Illinois",
    "batavia": "Illinois", "st. charles": "Illinois",
    "geneva": "Illinois", "wayne": "Illinois",
    "carol stream": "Illinois", "glendale heights": "Illinois",
    "west chicago": "Illinois", "winfield": "Illinois",
    "warrenville": "Illinois", "lisle": "Illinois",
    "butterfield": "Illinois", "oakbrook terrace": "Illinois",
    "oak brook": "Illinois", "villa park": "Illinois",
    "lombard": "Illinois", "glen ellyn": "Illinois",
    "wheaton": "Illinois", "carol stream": "Illinois",
    "bartlett": "Illinois", "streamwood": "Illinois",
    "elgin": "Illinois", "south elgin": "Illinois",
    "carpentersville": "Illinois", "dundee": "Illinois",
    "east dundee": "Illinois", "west dundee": "Illinois",
    "gilberts": "Illinois", "sleepy hollow": "Illinois",
    "hanover park": "Illinois", "bloomingdale": "Illinois",
    "glendale heights": "Illinois", "roselle": "Illinois",
    "medinah": "Illinois", "itasca": "Illinois",
    "wood dale": "Illinois", "bensenville": "Illinois",
    "franklin park": "Illinois", "melrose park": "Illinois",
    "bellwood": "Illinois", "hillside": "Illinois",
    "westchester": "Illinois", "la grange": "Illinois",
    "la grange park": "Illinois", "riverside": "Illinois",
    "north riverside": "Illinois", "berwyn": "Illinois",
    "cicero": "Illinois", "stickney": "Illinois",
    "forest park": "Illinois", "oak park": "Illinois",
    "river forest": "Illinois", "river grove": "Illinois",
    "elmwood park": "Illinois", "harwood heights": "Illinois",
    "norridge": "Illinois", "park ridge": "Illinois",
    "niles": "Illinois", "lincolnwood": "Illinois",
    "rosemont": "Illinois",
    # Pennsylvania cities
    "philadelphia": "Pennsylvania", "pittsburgh": "Pennsylvania",
    "allentown": "Pennsylvania", "erie": "Pennsylvania",
    "reading": "Pennsylvania", "scranton": "Pennsylvania",
    "bethlehem": "Pennsylvania", "lancaster": "Pennsylvania",
    "harrisburg": "Pennsylvania", "wilkes-barre": "Pennsylvania",
    "abington": "Pennsylvania", "upper darby": "Pennsylvania",
    "york": "Pennsylvania", "altoona": "Pennsylvania",
    "state college": "Pennsylvania", "gettysburg": "Pennsylvania",
    "westborough": "Pennsylvania",
    "paoli": "Pennsylvania", "chalfont": "Pennsylvania",
    "glenside": "Pennsylvania", "newtown": "Pennsylvania",
    "blue bell": "Pennsylvania", "fort washington": "Pennsylvania",
    "wayne": "Pennsylvania", "devon": "Pennsylvania",
    "exton": "Pennsylvania", "west chester": "Pennsylvania",
    "malvern": "Pennsylvania", "phoenixville": "Pennsylvania",
    "pottstown": "Pennsylvania", "norristown": "Pennsylvania",
    "conshohocken": "Pennsylvania", "king of prussia": "Pennsylvania",
    "ardmore": "Pennsylvania", "bryn mawr": "Pennsylvania",
    "haverford": "Pennsylvania", "swarthmore": "Pennsylvania",
    "springfield": "Pennsylvania", "media": "Pennsylvania",
    "chester": "Pennsylvania", "marcus hook": "Pennsylvania",
    "coatesville": "Pennsylvania", "kennett square": "Pennsylvania",
    "west grove": "Pennsylvania", "avondale": "Pennsylvania",
    "oxford": "Pennsylvania", "parkesburg": "Pennsylvania",
    "atglen": "Pennsylvania", "gap": "Pennsylvania",
    "ronks": "Pennsylvania", "strasburg": "Pennsylvania",
    "leola": "Pennsylvania", "lititz": "Pennsylvania",
    "manheim": "Pennsylvania", "elizabethtown": "Pennsylvania",
    "mount joy": "Pennsylvania", "columbia": "Pennsylvania",
    "marietta": "Pennsylvania",
    # Georgia cities
    "atlanta": "Georgia", "columbus": "Georgia",
    "savannah": "Georgia", "athens": "Georgia",
    "sandy springs": "Georgia", "roswell": "Georgia",
    "macon": "Georgia", "johns creek": "Georgia",
    "albany": "Georgia", "warner robins": "Georgia",
    "alpharetta": "Georgia", "marietta": "Georgia",
    "smyrna": "Georgia", "valdosta": "Georgia",
    "brookhaven": "Georgia", "dunwoody": "Georgia",
    "mcdonough": "Georgia", "stockbridge": "Georgia",
    "sandersville": "Georgia", "dalton": "Georgia",
    "gainesville": "Georgia",
    "cartersville": "Georgia", "canton": "Georgia",
    "rome": "Georgia", "griffin": "Georgia",
    "buford": "Georgia", "lawrenceville": "Georgia",
    "duluth": "Georgia", "norcross": "Georgia",
    "peachtree city": "Georgia", "newnan": "Georgia",
    "lagrange": "Georgia", "carrollton": "Georgia",
    "douglasville": "Georgia", "kennesaw": "Georgia",
    "woodstock": "Georgia", "acworth": "Georgia",
    "cumming": "Georgia",
    # Massachusetts cities
    "boston": "Massachusetts", "worcester": "Massachusetts",
    "springfield": "Massachusetts", "lowell": "Massachusetts",
    "cambridge": "Massachusetts", "new bedford": "Massachusetts",
    "brockton": "Massachusetts", "quincy": "Massachusetts",
    "lynn": "Massachusetts", "fall river": "Massachusetts",
    "newton": "Massachusetts", "somerville": "Massachusetts",
    "lawrence": "Massachusetts", "waltham": "Massachusetts",
    "haverhill": "Massachusetts", "malden": "Massachusetts",
    "medford": "Massachusetts", "westfield": "Massachusetts",
    "taunton": "Massachusetts", "chicopee": "Massachusetts",
    "weymouth": "Massachusetts", "revere": "Massachusetts",
    "peabody": "Massachusetts", "methuen": "Massachusetts",
    "barnstable": "Massachusetts", "pittsfield": "Massachusetts",
    "attleboro": "Massachusetts", "everett": "Massachusetts",
    "salem": "Massachusetts", "gloucester": "Massachusetts",
    "westborough": "Massachusetts", "lexington": "Massachusetts",
    "concord": "Massachusetts", "northborough": "Massachusetts",
    "marlborough": "Massachusetts", "wellesley": "Massachusetts",
    "brookline": "Massachusetts", "dedham": "Massachusetts",
    "norwood": "Massachusetts", "canton": "Massachusetts",
    "stoughton": "Massachusetts", "braintree": "Massachusetts",
    "randolph": "Massachusetts", "holbrook": "Massachusetts",
    "rockland": "Massachusetts", "abington": "Massachusetts",
    "whitman": "Massachusetts", "hanover": "Massachusetts",
    "marshfield": "Massachusetts", "duxbury": "Massachusetts",
    "plymouth": "Massachusetts", "kingston": "Massachusetts",
    "pembroke": "Massachusetts", "scituate": "Massachusetts",
    "cohasset": "Massachusetts", "hingham": "Massachusetts",
    "hull": "Massachusetts", "holbrook": "Massachusetts",
    "avon": "Massachusetts", "stoughton": "Massachusetts",
    "foxborough": "Massachusetts", "walpole": "Massachusetts",
    "sharon": "Massachusetts", "millis": "Massachusetts",
    "norfolk": "Massachusetts", "franklin": "Massachusetts",
    "medway": "Massachusetts", "holliston": "Massachusetts",
    "hopkinton": "Massachusetts", "ashland": "Massachusetts",
    "framingham": "Massachusetts", "natick": "Massachusetts",
    "sudbury": "Massachusetts", "wayland": "Massachusetts",
    "weston": "Massachusetts", "lincoln": "Massachusetts",
    "southborough": "Massachusetts", "northborough": "Massachusetts",
    "boylston": "Massachusetts", "clinton": "Massachusetts",
    "sterling": "Massachusetts", "holden": "Massachusetts",
    "paxton": "Massachusetts", "rutland": "Massachusetts",
    "barre": "Massachusetts", "templeton": "Massachusetts",
    "winchendon": "Massachusetts", "gardner": "Massachusetts",
    "fitchburg": "Massachusetts", "leominster": "Massachusetts",
    "lunenburg": "Massachusetts", "groton": "Massachusetts",
    "pepperell": "Massachusetts", "ashby": "Massachusetts",
    "shirley": "Massachusetts", "ayer": "Massachusetts",
    "littleton": "Massachusetts", "boxborough": "Massachusetts",
    "harvard": "Massachusetts", "stow": "Massachusetts",
    "hudson": "Massachusetts", "marlborough": "Massachusetts",
    "groveland": "Massachusetts", "brainerd": "Massachusetts",
    "foxboro": "Massachusetts", "chicopee": "Massachusetts",
    "westfield": "Massachusetts",
    # Ohio cities
    "columbus": "Ohio", "cleveland": "Ohio",
    "cincinnati": "Ohio", "toledo": "Ohio",
    "akron": "Ohio", "dayton": "Ohio",
    "parma": "Ohio", "canton": "Ohio",
    "youngstown": "Ohio", "lorain": "Ohio",
    "hamilton": "Ohio", "springfield": "Ohio",
    "kettering": "Ohio", "elyria": "Ohio",
    "lakewood": "Ohio", "cuyahoga": "Ohio",
    "westlake": "Ohio", "mentor": "Ohio",
    "strongsville": "Ohio", "fairfield": "Ohio",
    "beavercreek": "Ohio", "huber heights": "Ohio",
    "middletown": "Ohio", "coshocton": "Ohio",
    "wooster": "Ohio", "oberlin": "Ohio",
    "granville": "Ohio",
    # New Jersey cities
    "newark": "New Jersey", "jersey city": "New Jersey",
    "paterson": "New Jersey", "elizabeth": "New Jersey",
    "trenton": "New Jersey", "camden": "New Jersey",
    "clifton": "New Jersey", "passaic": "New Jersey",
    "east orange": "New Jersey", "union city": "New Jersey",
    "bayonne": "New Jersey", "irvington": "New Jersey",
    "hoboken": "New Jersey", "north bergen": "New Jersey",
    "vineland": "New Jersey", "new brunswick": "New Jersey",
    "perth amboy": "New Jersey", "woodbridge": "New Jersey",
    "atlantic city": "New Jersey", "parsippany": "New Jersey",
    "hackensack": "New Jersey", "cherry hill": "New Jersey",
    "princeton": "New Jersey", "morristown": "New Jersey",
    "marlton": "New Jersey", "freehold": "New Jersey",
    "flemington": "New Jersey", "ridgewood": "New Jersey",
    "rumson": "New Jersey", "short hills": "New Jersey",
    "saddle brook": "New Jersey", "sewell": "New Jersey",
    "carlstadt": "New Jersey", "totowa": "New Jersey",
    "darien": "New Jersey",  # could be CT
    "edgewater": "New Jersey",
    "marlboro": "New Jersey",
    # North Carolina cities
    "charlotte": "North Carolina", "raleigh": "North Carolina",
    "greensboro": "North Carolina", "durham": "North Carolina",
    "winston-salem": "North Carolina", "fayetteville": "North Carolina",
    "cary": "North Carolina", "wilmington": "North Carolina",
    "high point": "North Carolina", "greenville": "North Carolina",
    "asheville": "North Carolina", "concord": "North Carolina",
    "gastonia": "North Carolina", "jacksonville": "North Carolina",
    "chapel hill": "North Carolina", "rocky mount": "North Carolina",
    "huntersville": "North Carolina", "burlington": "North Carolina",
    "kannapolis": "North Carolina", "wilson": "North Carolina",
    "monroe": "North Carolina", "hickory": "North Carolina",
    "pinehurst": "North Carolina", "apex": "North Carolina",
    "morrisville": "North Carolina", "wake forest": "North Carolina",
    "albemarle": "North Carolina", "research triangle nc": "North Carolina",
    "research triangle north carolina": "North Carolina",
    "piedmont triad north carolina": "North Carolina",
    "piedmont-triad nc": "North Carolina",
    "piedmont-triad north carolina": "North Carolina",
    "ridge north carolina": "North Carolina",
    "summerville": "South Carolina",
    "clayton north carolina": "North Carolina",
    "monroe north carolina": "North Carolina",
    # Virginia cities
    "virginia beach": "Virginia", "norfolk": "Virginia",
    "chesapeake": "Virginia", "richmond": "Virginia",
    "newport news": "Virginia", "alexandria": "Virginia",
    "hampton": "Virginia", "roanoke": "Virginia",
    "portsmouth": "Virginia", "suffolk": "Virginia",
    "lynchburg": "Virginia", "harrisonburg": "Virginia",
    "charlottesville": "Virginia", "manassas": "Virginia",
    "fredericksburg": "Virginia", "herndon": "Virginia",
    "reston": "Virginia", "mclean": "Virginia",
    "ashburn": "Virginia", "centreville": "Virginia",
    "leesburg": "Virginia", "winchester": "Virginia",
    "arlington": "Virginia",
    "sterling": "Virginia", "chantilly": "Virginia",
    "fairfax": "Virginia", "falls church": "Virginia",
    "annandale": "Virginia", "springfield": "Virginia",
    "burke": "Virginia", "woodbridge": "Virginia",
    "dumfries": "Virginia", "stafford": "Virginia",
    "culpeper": "Virginia", "warrenton": "Virginia",
    "haymarket": "Virginia", "gainesville": "Virginia",
    "manassas park": "Virginia", "prince william": "Virginia",
    "dale city": "Virginia", "lake ridge": "Virginia",
    "woodbridge": "Virginia", "dumfries": "Virginia",
    "triangle": "Virginia", "quantico": "Virginia",
    "williamsburg": "Virginia", "hampton": "Virginia",
    "yorktown": "Virginia", "newport news": "Virginia",
    "waynesboro": "Virginia", "staunton": "Virginia",
    "lexington": "Virginia", "covington": "Virginia",
    "buena vista": "Virginia", "radford": "Virginia",
    "blacksburg": "Virginia", "christiansburg": "Virginia",
    "pulaski": "Virginia", "dublin": "Virginia",
    "wytheville": "Virginia", "marion": "Virginia",
    "bristol": "Virginia", "abingdon": "Virginia",
    "grundy": "Virginia", "big stone gap": "Virginia",
    "norton": "Virginia", "wise": "Virginia",
    "pennington gap": "Virginia", "jonesville": "Virginia",
    "gate city": "Virginia", "weber city": "Virginia",
    "damascus": "Virginia", "glade spring": "Virginia",
    "roanoke": "Virginia", "salem": "Virginia",
    "vinton": "Virginia", "rocky mount": "Virginia",
    "martinsville": "Virginia", "henry": "Virginia",
    "bassett": "Virginia", "collinsville": "Virginia",
    "eden": "Virginia",
    "powhatan": "Virginia", "waynesboro": "Virginia",
    "richmond": "Virginia", "colonial heights": "Virginia",
    "petersburg": "Virginia", "hopewell": "Virginia",
    "prince george": "Virginia",
    # Washington state cities
    "seattle": "Washington", "spokane": "Washington",
    "tacoma": "Washington", "vancouver": "Washington",
    "bellevue": "Washington", "kent": "Washington",
    "everett": "Washington", "renton": "Washington",
    "bellingham": "Washington", "yakima": "Washington",
    "kirkland": "Washington", "kennewick": "Washington",
    "redmond": "Washington", "marysville": "Washington",
    "pasco": "Washington", "federal way": "Washington",
    "shoreline": "Washington", "richland": "Washington",
    "kirkland": "Washington", "pullman": "Washington",
    "olympia": "Washington", "bremerton": "Washington",
    "battle ground": "Washington",
    "woodburn": "Oregon",  # Oregon city
    "beaverton": "Oregon", "hillsboro": "Oregon",
    "gresham": "Oregon", "medford": "Oregon",
    "springfield": "Oregon", "bend": "Oregon",
    "corvallis": "Oregon", "eugene": "Oregon",
    "portland": "Oregon", "lake oswego": "Oregon",
    "tigard": "Oregon", "tualatin": "Oregon",
    "wilsonville": "Oregon", "milwaukie": "Oregon",
    "happy valley": "Oregon", "clackamas": "Oregon",
    "troutdale": "Oregon",
    # Colorado cities
    "denver": "Colorado", "colorado springs": "Colorado",
    "aurora": "Colorado", "fort collins": "Colorado",
    "lakewood": "Colorado", "thornton": "Colorado",
    "arvada": "Colorado", "westminster": "Colorado",
    "pueblo": "Colorado", "boulder": "Colorado",
    "highlands ranch": "Colorado", "greeley": "Colorado",
    "longmont": "Colorado", "loveland": "Colorado",
    "centennial": "Colorado", "broomfield": "Colorado",
    "castle rock": "Colorado", "commerce city": "Colorado",
    "parker": "Colorado", "northglenn": "Colorado",
    "brighton": "Colorado", "littleton": "Colorado",
    "aspen": "Colorado", "vail": "Colorado",
    "breckenridge": "Colorado", "steamboat springs": "Colorado",
    "telluride": "Colorado", "durango": "Colorado",
    "cheyenne": "Colorado",  # actually WY
    "silverthorne": "Colorado", "salida": "Colorado",
    "evergreen": "Colorado", "montrose co": "Colorado",
    "edwards co": "Colorado",
    # Arizona cities
    "phoenix": "Arizona", "tucson": "Arizona",
    "mesa": "Arizona", "chandler": "Arizona",
    "scottsdale": "Arizona", "glendale": "Arizona",
    "gilbert": "Arizona", "tempe": "Arizona",
    "peoria": "Arizona", "surprise": "Arizona",
    "yuma": "Arizona", "avondale": "Arizona",
    "flagstaff": "Arizona", "goodyear": "Arizona",
    "lake havasu city": "Arizona", "casa grande": "Arizona",
    "prescott": "Arizona", "sedona": "Arizona",
    "oro valley": "Arizona", "maricopa": "Arizona",
    "globe": "Arizona",
    # Minnesota cities
    "minneapolis": "Minnesota", "saint paul": "Minnesota",
    "st. paul": "Minnesota", "rochester": "Minnesota",
    "duluth": "Minnesota", "bloomington": "Minnesota",
    "brooklyn park": "Minnesota", "plymouth": "Minnesota",
    "st. cloud": "Minnesota", "eagan": "Minnesota",
    "coon rapids": "Minnesota", "burnsville": "Minnesota",
    "eden prairie": "Minnesota", "maple grove": "Minnesota",
    "woodbury": "Minnesota", "minnetonka": "Minnesota",
    "apple valley": "Minnesota", "edina": "Minnesota",
    "st. louis park": "Minnesota", "moorhead": "Minnesota",
    "mankato": "Minnesota", "maplewood": "Minnesota",
    "shakopee": "Minnesota", "richfield": "Minnesota",
    "cottage grove": "Minnesota", "roseville": "Minnesota",
    "inver grove heights": "Minnesota", "andover": "Minnesota",
    "brooklyn center": "Minnesota", "lakeville": "Minnesota",
    "blaine": "Minnesota", "stillwater": "Minnesota",
    "anoka": "Minnesota", "brainerd": "Minnesota",
    "winona": "Minnesota", "north st. paul": "Minnesota",
    "white bear lake": "Minnesota", "arden hills": "Minnesota",
    "rosemount": "Minnesota",
    "st.paul-minneapolis": "Minnesota",
    # Tennessee cities
    "nashville": "Tennessee", "memphis": "Tennessee",
    "knoxville": "Tennessee", "chattanooga": "Tennessee",
    "clarksville": "Tennessee", "murfreesboro": "Tennessee",
    "franklin": "Tennessee", "jackson": "Tennessee",
    "johnson city": "Tennessee", "bartlett": "Tennessee",
    "hendersonville": "Tennessee", "kingsport": "Tennessee",
    "collierville": "Tennessee", "smyrna": "Tennessee",
    "germantown": "Tennessee", "brentwood": "Tennessee",
    "dickson": "Tennessee", "gallatin": "Tennessee",
    "la vergne": "Tennessee",
    # Maryland cities
    "baltimore": "Maryland", "columbia": "Maryland",
    "germantown": "Maryland", "silver spring": "Maryland",
    "waldorf": "Maryland", "glen burnie": "Maryland",
    "ellicott city": "Maryland", "dundalk": "Maryland",
    "rockville": "Maryland", "bowie": "Maryland",
    "gaithersburg": "Maryland", "hagerstown": "Maryland",
    "annapolis": "Maryland", "bethesda": "Maryland",
    "towson": "Maryland", "laurel": "Maryland",
    "hyattsville": "Maryland", "college park": "Maryland",
    "greenbelt": "Maryland", "bel air": "Maryland",
    "cumberland": "Maryland", "salisbury": "Maryland",
    "frederick": "Maryland", "westminster": "Maryland",
    "catonsville": "Maryland", "owings mills": "Maryland",
    "pikesville": "Maryland", "randallstown": "Maryland",
    "reisterstown": "Maryland", "cockeysville": "Maryland",
    "timonium": "Maryland", "lutherville": "Maryland",
    "parkville": "Maryland", "overlea": "Maryland",
    "rosedale": "Maryland", "middle river": "Maryland",
    "essex": "Maryland", "joppa": "Maryland",
    "aberdeen": "Maryland", "edgewood": "Maryland",
    "bel air": "Maryland", "fallston": "Maryland",
    "jarrettsville": "Maryland", "forest hill": "Maryland",
    "havre de grace": "Maryland", "perryville": "Maryland",
    "north east": "Maryland", "elkton": "Maryland",
    "rising sun": "Maryland",
    "greenbrier": "Maryland",
    "silver spring": "Maryland", "silverspring": "Maryland",
    "chevy chase": "Maryland", "potomac": "Maryland",
    "olney": "Maryland", "montgomery village": "Maryland",
    "gaithersburg": "Maryland", "germantown": "Maryland",
    "clarksburg": "Maryland", "damascus": "Maryland",
    "boyds": "Maryland", "laytonsville": "Maryland",
    "burtonsville": "Maryland", "spencerville": "Maryland",
    "aspen hill": "Maryland", "wheaton": "Maryland",
    "kensington": "Maryland", "takoma park": "Maryland",
    "langley park": "Maryland", "adelphi": "Maryland",
    "beltsville": "Maryland", "laurel": "Maryland",
    "berwyn heights": "Maryland", "college park": "Maryland",
    "riverdale": "Maryland", "new carrollton": "Maryland",
    "seat pleasant": "Maryland", "capitol heights": "Maryland",
    "district heights": "Maryland", "forestville": "Maryland",
    "suitland": "Maryland", "morningside": "Maryland",
    "camp springs": "Maryland", "clinton": "Maryland",
    "temple hills": "Maryland", "fort washington": "Maryland",
    "oxon hill": "Maryland", "national harbor": "Maryland",
    "accokeek": "Maryland", "bryans road": "Maryland",
    "waldorf": "Maryland", "white plains": "Maryland",
    "la plata": "Maryland", "prince frederick": "Maryland",
    "lexington park": "Maryland", "california": "Maryland",
    "leonardtown": "Maryland", "great mills": "Maryland",
    "st. mary's city": "Maryland",
    "annapolis": "Maryland", "severn": "Maryland",
    "pasadena": "Maryland", "arnold": "Maryland",
    "millersville": "Maryland", "crofton": "Maryland",
    "gambrills": "Maryland", "odenton": "Maryland",
    "davidsonville": "Maryland", "lothian": "Maryland",
    "harwood": "Maryland", "churchton": "Maryland",
    "deale": "Maryland", "shady side": "Maryland",
    "tracys landing": "Maryland", "mayo": "Maryland",
    "edgewater": "Maryland", "riva": "Maryland",
    "severna park": "Maryland", "linthicum": "Maryland",
    "hanover": "Maryland", "jessup": "Maryland",
    "mather": "Maryland", "latham": "Maryland",
    "joppa": "Maryland", "baltimore area": "Maryland",
    "baltimore metro": "Maryland",
    # Wisconsin cities
    "milwaukee": "Wisconsin", "madison": "Wisconsin",
    "green bay": "Wisconsin", "kenosha": "Wisconsin",
    "racine": "Wisconsin", "appleton": "Wisconsin",
    "waukesha": "Wisconsin", "oshkosh": "Wisconsin",
    "eau claire": "Wisconsin", "janesville": "Wisconsin",
    "west allis": "Wisconsin", "la crosse": "Wisconsin",
    "sheboygan": "Wisconsin", "wauwatosa": "Wisconsin",
    "fond du lac": "Wisconsin", "new berlin": "Wisconsin",
    "wausau": "Wisconsin", "brookfield": "Wisconsin",
    "beloit": "Wisconsin", "greenfield": "Wisconsin",
    "menomonie": "Wisconsin", "algonquin": "Wisconsin",
    "northfield": "Wisconsin",
    "milwaukee/waukesha": "Wisconsin",
    # Indiana cities
    "indianapolis": "Indiana", "fort wayne": "Indiana",
    "evansville": "Indiana", "south bend": "Indiana",
    "carmel": "Indiana", "fishers": "Indiana",
    "bloomington": "Indiana", "hammond": "Indiana",
    "gary": "Indiana", "muncie": "Indiana",
    "lafayette": "Indiana", "terre haute": "Indiana",
    "kokomo": "Indiana", "anderson": "Indiana",
    "noblesville": "Indiana", "greenwood": "Indiana",
    # Missouri cities
    "kansas city": "Missouri", "st. louis": "Missouri",
    "st louis": "Missouri", "springfield": "Missouri",
    "independence": "Missouri", "columbia": "Missouri",
    "lee's summit": "Missouri", "o'fallon": "Missouri",
    "st. joseph": "Missouri", "st. charles": "Missouri",
    "blue springs": "Missouri", "joplin": "Missouri",
    "florissant": "Missouri", "chesterfield": "Missouri",
    "st. peters": "Missouri", "ballwin": "Missouri",
    "liberty": "Missouri", "wentzville": "Missouri",
    "cape girardeau": "Missouri", "raymore": "Missouri",
    "belton": "Missouri", "st. ann": "Missouri",
    "hannibal": "Missouri",
    "ozark": "Missouri",
    # Kansas cities
    "wichita": "Kansas", "overland park": "Kansas",
    "kansas city": "Kansas", "topeka": "Kansas",
    "olathe": "Kansas", "lawrence": "Kansas",
    "shawnee": "Kansas", "manhattan": "Kansas",
    "salina": "Kansas", "hutchinson": "Kansas",
    "lenexa": "Kansas", "leavenworth": "Kansas",
    "leawood": "Kansas",
    # Iowa cities
    "des moines": "Iowa", "cedar rapids": "Iowa",
    "davenport": "Iowa", "sioux city": "Iowa",
    "iowa city": "Iowa", "waterloo": "Iowa",
    "council bluffs": "Iowa", "ames": "Iowa",
    "west des moines": "Iowa", "dubuque": "Iowa",
    "ankeny": "Iowa", "urbandale": "Iowa",
    "coralville": "Iowa", "mason city": "Iowa",
    "bettendorf": "Iowa", "ottumwa": "Iowa",
    "clinton": "Iowa", "marshalltown": "Iowa",
    "burlington": "Iowa", "fort dodge": "Iowa",
    # Michigan cities
    "detroit": "Michigan", "grand rapids": "Michigan",
    "warren": "Michigan", "sterling heights": "Michigan",
    "lansing": "Michigan", "ann arbor": "Michigan",
    "flint": "Michigan", "dearborn": "Michigan",
    "livonia": "Michigan", "troy": "Michigan",
    "westland": "Michigan", "clinton township": "Michigan",
    "canton": "Michigan", "southfield": "Michigan",
    "dearborn heights": "Michigan", "taylor": "Michigan",
    "royal oak": "Michigan", "pontiac": "Michigan",
    "saint clair shores": "Michigan", "novi": "Michigan",
    "kalamazoo": "Michigan", "saginaw": "Michigan",
    "kentwood": "Michigan", "wyoming": "Michigan",
    "inkster": "Michigan", "ferndale": "Michigan",
    "muskegon": "Michigan", "lapeer": "Michigan",
    "redford": "Michigan", "marquette": "Michigan",
    "ironwood": "Michigan", "cheboygan": "Michigan",
    "dearborn": "Michigan", "melville": "Michigan",
    "grand rapids grand rapids": "Michigan",
    # Connecticut cities
    "bridgeport": "Connecticut", "new haven": "Connecticut",
    "stamford": "Connecticut", "hartford": "Connecticut",
    "waterbury": "Connecticut", "norwalk": "Connecticut",
    "danbury": "Connecticut", "new britain": "Connecticut",
    "meriden": "Connecticut", "west hartford": "Connecticut",
    "bristol": "Connecticut", "middletown": "Connecticut",
    "milford": "Connecticut", "norwich": "Connecticut",
    "shelton": "Connecticut", "torrington": "Connecticut",
    "new london": "Connecticut", "ansonia": "Connecticut",
    "derby": "Connecticut", "groton": "Connecticut",
    "glastonbury": "Connecticut", "southington": "Connecticut",
    "cheshire": "Connecticut", "enfield": "Connecticut",
    "guilford": "Connecticut", "madison": "Connecticut",
    "old saybrook": "Connecticut", "essex": "Connecticut",
    "clinton": "Connecticut", "westbrook": "Connecticut",
    "old lyme": "Connecticut", "niantic": "Connecticut",
    "east lyme": "Connecticut", "waterford": "Connecticut",
    "new london": "Connecticut", "montville": "Connecticut",
    "norwich": "Connecticut", "sprague": "Connecticut",
    "voluntown": "Connecticut", "plainfield": "Connecticut",
    "killingly": "Connecticut", "danielson": "Connecticut",
    "putnam": "Connecticut", "woodstock": "Connecticut",
    "pomfret": "Connecticut", "brooklyn": "Connecticut",
    "thompson": "Connecticut", "northeast": "Connecticut",
    "conneticut": "Connecticut", "conn": "Connecticut",
    "wilton": "Connecticut", "darien": "Connecticut",
    "greenwich": "Connecticut",
    # South Carolina cities
    "columbia": "South Carolina", "charleston": "South Carolina",
    "north charleston": "South Carolina", "mount pleasant": "South Carolina",
    "rock hill": "South Carolina", "greenville": "South Carolina",
    "summerville": "South Carolina", "goose creek": "South Carolina",
    "hilton head island": "South Carolina", "sumter": "South Carolina",
    "florence": "South Carolina", "spartanburg": "South Carolina",
    "myrtle beach": "South Carolina", "aiken": "South Carolina",
    "anderson": "South Carolina", "greer": "South Carolina",
    "mauldin": "South Carolina", "blythewood": "South Carolina",
    "ridgeland": "South Carolina", "manning": "South Carolina",
    "newberry": "South Carolina",
    # Nevada cities
    "las vegas": "Nevada", "henderson": "Nevada",
    "reno": "Nevada", "north las vegas": "Nevada",
    "sparks": "Nevada", "carson city": "Nevada",
    "midvale": "Nevada",  # actually UT
    "elko": "Nevada", "mesquite": "Nevada",
    "boulder city": "Nevada",
    # Utah cities
    "salt lake city": "Utah", "west valley city": "Utah",
    "provo": "Utah", "west jordan": "Utah",
    "orem": "Utah", "sandy": "Utah",
    "ogden": "Utah", "st. george": "Utah",
    "layton": "Utah", "south jordan": "Utah",
    "taylorsville": "Utah", "millcreek": "Utah",
    "murray": "Utah", "herriman": "Utah",
    "riverton": "Utah", "draper": "Utah",
    "bountiful": "Utah", "lehi": "Utah",
    "holladay": "Utah", "cottonwood heights": "Utah",
    "midvale": "Utah", "kearns": "Utah",
    "magna": "Utah", "american fork": "Utah",
    "pleasant grove": "Utah", "lindon": "Utah",
    "cedar hills": "Utah", "highland": "Utah",
    "alpine": "Utah", "heber city": "Utah",
    "park city": "Utah", "breckenridge": "Utah",  # CO actually
    "moab": "Utah", "monticello": "Utah",
    "blanding": "Utah", "price": "Utah",
    "helper": "Utah", "wellington": "Utah",
    "spring city": "Utah", "manti": "Utah",
    "richfield": "Utah", "beaver": "Utah",
    "cedar city": "Utah", "hurricane": "Utah",
    "la verkin": "Utah", "washington": "Utah",
    "st. george": "Utah",
    "salt lake": "Utah",
    # Nebraska cities
    "omaha": "Nebraska", "lincoln": "Nebraska",
    "bellevue": "Nebraska", "grand island": "Nebraska",
    "kearney": "Nebraska", "fremont": "Nebraska",
    "hastings": "Nebraska", "north platte": "Nebraska",
    "norfolk": "Nebraska", "columbus": "Nebraska",
    # Oklahoma cities
    "oklahoma city": "Oklahoma", "tulsa": "Oklahoma",
    "norman": "Oklahoma", "broken arrow": "Oklahoma",
    "lawton": "Oklahoma", "edmond": "Oklahoma",
    "moore": "Oklahoma", "midwest city": "Oklahoma",
    "enid": "Oklahoma", "stillwater": "Oklahoma",
    "owasso": "Oklahoma", "bartlesville": "Oklahoma",
    # Louisiana cities
    "new orleans": "Louisiana", "baton rouge": "Louisiana",
    "shreveport": "Louisiana", "metairie": "Louisiana",
    "lafayette": "Louisiana", "lake charles": "Louisiana",
    "kenner": "Louisiana", "bossier city": "Louisiana",
    "monroe": "Louisiana", "alexandria": "Louisiana",
    "houma": "Louisiana", "new iberia": "Louisiana",
    # Alabama cities
    "birmingham": "Alabama", "montgomery": "Alabama",
    "huntsville": "Alabama", "mobile": "Alabama",
    "tuscaloosa": "Alabama", "hoover": "Alabama",
    "dothan": "Alabama", "auburn": "Alabama",
    "decatur": "Alabama", "madison": "Alabama",
    "gadsden": "Alabama", "prichard": "Alabama",
    "phenix city": "Alabama", "florence": "Alabama",
    "cullman": "Alabama", "anniston": "Alabama",
    "theodore": "Alabama", "biloxi": "Alabama",  # MS actually
    # Kentucky cities
    "louisville": "Kentucky", "lexington": "Kentucky",
    "bowling green": "Kentucky", "owensboro": "Kentucky",
    "covington": "Kentucky", "richmond": "Kentucky",
    "hopkinsville": "Kentucky", "florence": "Kentucky",
    "elizabethtown": "Kentucky", "paducah": "Kentucky",
    "nicholasville": "Kentucky", "frankfort": "Kentucky",
    # Arkansas cities
    "little rock": "Arkansas", "fort smith": "Arkansas",
    "fayetteville": "Arkansas", "springdale": "Arkansas",
    "jonesboro": "Arkansas", "north little rock": "Arkansas",
    "conway": "Arkansas", "rogers": "Arkansas",
    "bentonville": "Arkansas", "pine bluff": "Arkansas",
    "hot springs": "Arkansas", "benton": "Arkansas",
    # Mississippi cities
    "jackson": "Mississippi", "gulfport": "Mississippi",
    "southaven": "Mississippi", "hattiesburg": "Mississippi",
    "biloxi": "Mississippi", "meridian": "Mississippi",
    "tupelo": "Mississippi", "olive branch": "Mississippi",
    "horn lake": "Mississippi", "columbus": "Mississippi",
    "corinth": "Mississippi", "vicksburg": "Mississippi",
    "pascagoula": "Mississippi", "oxford": "Mississippi",
    "ridgeland": "Mississippi", "madison": "Mississippi",
    # New Hampshire cities
    "manchester": "New Hampshire", "nashua": "New Hampshire",
    "concord": "New Hampshire", "derry": "New Hampshire",
    "dover": "New Hampshire", "rochester": "New Hampshire",
    "salem": "New Hampshire", "merrimack": "New Hampshire",
    "hudson": "New Hampshire", "londonderry": "New Hampshire",
    "keene": "New Hampshire", "portsmouth": "New Hampshire",
    # Rhode Island cities
    "providence": "Rhode Island", "cranston": "Rhode Island",
    "warwick": "Rhode Island", "pawtucket": "Rhode Island",
    "east providence": "Rhode Island", "woonsocket": "Rhode Island",
    "coventry": "Rhode Island", "cumberland": "Rhode Island",
    "north providence": "Rhode Island", "south kingstown": "Rhode Island",
    "west warwick": "Rhode Island", "north kingstown": "Rhode Island",
    "bristol": "Rhode Island", "tiverton": "Rhode Island",
    "middletown": "Rhode Island", "portsmouth": "Rhode Island",
    "newport": "Rhode Island", "johnston": "Rhode Island",
    "barrington": "Rhode Island",
    # Delaware cities
    "wilmington": "Delaware", "dover": "Delaware",
    "newark": "Delaware", "middletown": "Delaware",
    "smyrna": "Delaware", "milford": "Delaware",
    "seaford": "Delaware", "georgetown": "Delaware",
    "elsmere": "Delaware", "new castle": "Delaware",
    "bear": "Delaware", "newark": "Delaware",
    "hockessin": "Delaware", "claymont": "Delaware",
    "christiana": "Delaware", "greenville": "Delaware",
    "lewes": "Delaware", "rehoboth beach": "Delaware",
    "millsboro": "Delaware",
    # DC area
    "washington": "District of Columbia",
    "washington d.c.": "District of Columbia",
    "washington dc": "District of Columbia",
    "washington d.c": "District of Columbia",
    "washington d. c.": "District of Columbia",
    # Hawaii cities
    "honolulu": "Hawaii", "hilo": "Hawaii",
    "kailua": "Hawaii", "pearl city": "Hawaii",
    "waipahu": "Hawaii", "kaneohe": "Hawaii",
    "mililani": "Hawaii", "waimalu": "Hawaii",
    "kihei": "Hawaii", "lahaina": "Hawaii",
    "wailuku": "Hawaii", "kula": "Hawaii",
    "makawao": "Hawaii", "pukalani": "Hawaii",
    "paia": "Hawaii", "haiku": "Hawaii",
    "kahului": "Hawaii", "waikiki": "Hawaii",
    "holualoa": "Hawaii", "kauai": "Hawaii",
    # Maine cities
    "portland": "Maine", "lewiston": "Maine",
    "bangor": "Maine", "south portland": "Maine",
    "auburn": "Maine", "brunswick": "Maine",
    "biddeford": "Maine", "sanford": "Maine",
    "augusta": "Maine", "saco": "Maine",
    "westbrook": "Maine", "waterville": "Maine",
    "caribou": "Maine", "ellsworth": "Maine",
    # Montana cities
    "billings": "Montana", "missoula": "Montana",
    "great falls": "Montana", "bozeman": "Montana",
    "butte": "Montana", "helena": "Montana",
    "kalispell": "Montana", "havre": "Montana",
    "anaconda": "Montana", "miles city": "Montana",
    # Wyoming cities
    "cheyenne": "Wyoming", "casper": "Wyoming",
    "laramie": "Wyoming", "gillette": "Wyoming",
    "rock springs": "Wyoming", "sheridan": "Wyoming",
    "green river": "Wyoming", "evanston": "Wyoming",
    "riverton": "Wyoming", "jackson": "Wyoming",
    "cody": "Wyoming", "lander": "Wyoming",
    # West Virginia cities
    "charleston": "West Virginia", "huntington": "West Virginia",
    "parkersburg": "West Virginia", "morgantown": "West Virginia",
    "wheeling": "West Virginia", "weirton": "West Virginia",
    "fairmont": "West Virginia", "martinsburg": "West Virginia",
    "beckley": "West Virginia", "clarksburg": "West Virginia",
    # Vermont cities
    "burlington": "Vermont", "essex": "Vermont",
    "rutland": "Vermont", "south burlington": "Vermont",
    "barre": "Vermont", "montpelier": "Vermont",
    # Idaho cities
    "boise": "Idaho", "nampa": "Idaho",
    "meridian": "Idaho", "idaho falls": "Idaho",
    "pocatello": "Idaho", "caldwell": "Idaho",
    "coeur d'alene": "Idaho", "twin falls": "Idaho",
    "lewiston": "Idaho", "ketchum": "Idaho",
    # New Mexico cities
    "albuquerque": "New Mexico", "las cruces": "New Mexico",
    "rio rancho": "New Mexico", "santa fe": "New Mexico",
    "roswell": "New Mexico", "farmington": "New Mexico",
    "clovis": "New Mexico", "portales": "New Mexico",
    "carlsbad": "New Mexico", "alamogordo": "New Mexico",
    "gallup": "New Mexico", "hobbs": "New Mexico",
    "artesia": "New Mexico", "espanola": "New Mexico",
    # Alaska cities
    "anchorage": "Alaska", "fairbanks": "Alaska",
    "juneau": "Alaska", "sitka": "Alaska",
    "ketchikan": "Alaska", "wasilla": "Alaska",
    "kenai": "Alaska", "kodiak": "Alaska",
    "bethel": "Alaska", "palmer": "Alaska",
    "soldotna": "Alaska", "homer": "Alaska",
    "dillingham": "Alaska", "skagway": "Alaska",
    # South Dakota cities
    "sioux falls": "South Dakota", "rapid city": "South Dakota",
    "aberdeen": "South Dakota", "brookings": "South Dakota",
    "watertown": "South Dakota", "mitchell": "South Dakota",
    "yankton": "South Dakota",
    # North Dakota cities
    "fargo": "North Dakota", "bismarck": "North Dakota",
    "grand forks": "North Dakota", "minot": "North Dakota",
    "west fargo": "North Dakota", "williston": "North Dakota",
    "dickinson": "North Dakota", "mandan": "North Dakota",
    "jamestown": "North Dakota", "valley city": "North Dakota",
    # Puerto Rico cities
    "san juan": "Puerto Rico", "bayamon": "Puerto Rico",
    "carolina": "Puerto Rico", "ponce": "Puerto Rico",
    "caguas": "Puerto Rico", "guaynabo": "Puerto Rico",
    "arecibo": "Puerto Rico", "mayaguez": "Puerto Rico",
    "aguadilla": "Puerto Rico", "humacao": "Puerto Rico",
    "toa baja": "Puerto Rico", "toa alta": "Puerto Rico",
    "vieques": "Puerto Rico", "culebra": "Puerto Rico",
    "fajardo": "Puerto Rico", "hatillo": "Puerto Rico",
    "lajas": "Puerto Rico", "lares": "Puerto Rico",
    "luquillo": "Puerto Rico", "moca": "Puerto Rico",
    "naguabo": "Puerto Rico", "orocovis": "Puerto Rico",
    "rincon": "Puerto Rico", "sabana grande": "Puerto Rico",
    "san german": "Puerto Rico", "san lorenzo": "Puerto Rico",
    "santurce": "Puerto Rico", "trujillo alto": "Puerto Rico",
    "trujillo alto": "Puerto Rico", "vega alta": "Puerto Rico",
    "yabucoa": "Puerto Rico", "yauco": "Puerto Rico",
    "dorado": "Puerto Rico", "cayey": "Puerto Rico",
    "ciales": "Puerto Rico", "coamo": "Puerto Rico",
    "corozal": "Puerto Rico", "guayama": "Puerto Rico",
    "jayuya": "Puerto Rico", "juncos": "Puerto Rico",
    "manati": "Puerto Rico", "maunabo": "Puerto Rico",
    "mayagez": "Puerto Rico",
    "plaza san juan": "Puerto Rico",
    "old san juan": "Puerto Rico",
    "bayamn": "Puerto Rico", "cidra": "Puerto Rico",
    "anasco": "Puerto Rico", "aguadilla": "Puerto Rico",
    "aguas buenas": "Puerto Rico", "aibonito": "Puerto Rico",
    "barceloneta": "Puerto Rico", "barranquitas": "Puerto Rico",
    "camuy": "Puerto Rico", "canóvanas": "Puerto Rico",
    "ceiba": "Puerto Rico",
    "guanica": "Puerto Rico",
    "isabela": "Puerto Rico",
    "patillas": "Puerto Rico",
    "penuelas": "Puerto Rico", "quebradillas": "Puerto Rico",
    "salinas": "Puerto Rico", "santa isabel": "Puerto Rico",
    "utuado": "Puerto Rico", "villalba": "Puerto Rico",
    "adjuntas": "Puerto Rico",
    "christiansted": "Virgin Islands",
    "kingshill": "Virgin Islands",
    # Guam
    "dededo": "Guam",
    # American Samoa
    "pago": "American Samoa",
    # Northern Mariana Islands
    "saipan": "Northern Mariana Islands",
}

# Known non-US locations (countries, regions, cities)
NON_USA_KEYWORDS = {
    # Countries
    "canada", "ontario", "british columbia", "alberta", "quebec", "manitoba",
    "saskatchewan", "nova scotia", "new brunswick", "prince edward island",
    "newfoundland", "nunavut", "yukon",
    "uk", "england", "scotland", "wales", "northern ireland", "ireland",
    "london", "manchester", "birmingham", "bristol", "leeds", "sheffield",
    "liverpool", "newcastle", "cardiff", "edinburgh", "glasgow", "belfast",
    "essex", "surrey", "kent", "hampshire", "berkshire", "oxfordshire",
    "hertfordshire", "cambridgeshire", "buckinghamshire", "bedfordshire",
    "northamptonshire", "leicestershire", "warwickshire", "staffordshire",
    "shropshire", "herefordshire", "worcestershire", "gloucestershire",
    "wiltshire", "somerset", "dorset", "devon", "cornwall",
    "west midlands", "west yorkshire", "south yorkshire", "east yorkshire",
    "north yorkshire", "lincolnshire", "nottinghamshire", "derbyshire",
    "cheshire", "lancashire", "cumbria", "durham", "northumberland",
    "tyne and wear", "merseyside", "west sussex", "east sussex",
    "oxon", "herts", "bucks", "berks", "lancs", "notts",
    "suffolk", "norfolk", "middlesex",
    # India
    "india", "maharashtra", "karnataka", "delhi", "punjab", "gujarat",
    "uttar pradesh", "tamil nadu", "west bengal", "rajasthan",
    "haryana", "kerala", "telangana", "andhra pradesh", "bihar",
    "madhya pradesh", "assam", "odisha", "himachal pradesh",
    "chandigarh", "noida", "gurgaon", "bengaluru", "bangalore",
    "hyderabad", "chennai", "mumbai", "kolkata", "pune", "ahmedabad",
    "new delhi", "ludhiana", "gwalior", "meerut", "agra", "varanasi",
    "nagpur", "coimbatore", "surat", "patna", "bhopal", "indore",
    "nagaland",
    # Pakistan
    "pakistan", "karachi", "lahore", "islamabad", "sindh",
    "punjab", "khyber pakhtunkhwa", "gilgit", "gilgit-baltistan",
    "balochistan", "faisalabad", "rawalpindi", "multan", "hyderabad",
    "sialkot",
    # Bangladesh
    "bangladesh", "dhaka", "chittagong", "sylhet", "rajshahi",
    "khulna", "rangpur", "mymensingh", "barisal", "comilla",
    "narail", "netrakona", "lalmonirhat", "gaibandha",
    # China
    "china", "beijing", "shanghai", "guangdong", "zhejiang", "jiangsu",
    "shandong", "fujian", "hubei", "hunan", "sichuan", "guangxi",
    "liaoning", "hebei", "henan", "yunnan", "jiangxi", "chongqing",
    "tianjin", "shenzhen", "nanjing", "suzhou", "wuhan", "hangzhou",
    "foshan", "chengdu", "zhengzhou", "changsha", "jinan",
    "shijiazhuang", "weifang", "sihui", "fuzhou",
    # Australia
    "australia", "new south wales", "victoria", "queensland",
    "western australia", "south australia", "tasmania",
    "australian capital territory",
    "sydney", "melbourne", "brisbane", "perth", "adelaide",
    "canberra", "darwin", "hobart", "cairns", "gold coast",
    "newcastle", "wollongong",
    # New Zealand
    "new zealand", "auckland", "wellington", "christchurch",
    "hamilton", "tauranga", "dunedin", "palmerston north",
    "new south wales nsw", "waikato",
    # South Africa
    "south africa", "gauteng", "western cape", "kwazulu natal",
    "kwazulu-natal", "eastern cape", "limpopo", "mpumalanga",
    "free state", "north west", "northern cape",
    "johannesburg", "cape town", "durban", "pretoria",
    "soweto", "port elizabeth", "bloemfontein", "roodepoort",
    "pietermaritzburg", "randburg",
    # Africa (other)
    "nigeria", "kenya", "ghana", "ethiopia", "uganda", "tanzania",
    "senegal", "cameroon", "mali", "rwanda", "abuja", "lagos",
    "nairobi", "accra", "addis ababa", "kampala", "kigali",
    "dar es salaam", "mombasa", "nakuru", "dakar", "harare",
    "durban kzn", "federal capital territory", "akwa ibom",
    "cross river", "cross river state", "osun state",
    "rivers", "olancho", "borno", "abidjan",
    # Middle East
    "dubai", "abu dhabi", "sharjah", "ajman", "muscat",
    "riyadh", "jeddah", "makkah", "amman", "tehran",
    "baghdad", "jerusalem", "ankara", "istanbul", "izmir",
    "doha", "kuwait", "oman", "qatar", "bahrain", "saudi arabia",
    "uae", "jordan", "egypt", "cairo", "gaza",
    "iran", "iraq", "turkey", "esfahan", "isfahan", "semnan",
    "mazandaran", "belarus", "ukraine", "kyiv",
    # Europe
    "germany", "france", "spain", "italy", "netherlands",
    "belgium", "switzerland", "sweden", "norway", "denmark",
    "finland", "poland", "portugal", "austria", "czech republic",
    "hungary", "romania", "bulgaria", "croatia", "serbia",
    "berlin", "munich", "frankfurt", "hamburg", "cologne",
    "paris", "lyon", "marseille", "madrid", "barcelona",
    "rome", "milan", "naples", "turin", "florence",
    "amsterdam", "rotterdam", "the hague", "eindhoven",
    "brussels", "antwerp", "zurich", "geneva", "lausanne",
    "stockholm", "oslo", "copenhagen", "helsinki",
    "warsaw", "krakow", "lisbon", "porto", "vienna",
    "budapest", "prague", "bucharest", "sofia", "zagreb",
    "vilnius", "riga", "tallinn",
    "ile de france", "ile-de-france", "normandie", "bretagne",
    "nord-pas-de-calais", "provence", "languedoc",
    "cataluna", "andalusia", "galicia", "navarre", "aragua",
    "gelderland", "zeeland", "groningen", "friesland",
    "limburg", "overijssel", "utrecht", "drenthe", "flevoland",
    "noord-holland", "noord holland", "zuid-holland", "noord-brabant",
    "hessen", "sachsen", "rheinland-pfalz", "badenwrttemberg",
    "schleswig-holstein", "rheinland pfalz",
    "west midlands", "west java", "jawa barat", "jawa tengah",
    "antwerp", "antwerpen", "west-vlaanderen", "vlaams brabant",
    # Latin America
    "mexico", "brazil", "argentina", "colombia", "chile", "peru",
    "venezuela", "ecuador", "bolivia", "paraguay", "uruguay",
    "guatemala", "costa rica", "panama", "honduras", "nicaragua",
    "el salvador", "mexico city", "cdmx", "guadalajara", "monterrey",
    "sao paulo", "rio de janeiro", "belo horizonte",
    "buenos aires", "bogota", "lima", "santiago", "quito",
    "medellin", "cali", "cartagena",
    "jalisco", "baja california", "sonora", "chihuahua",
    "tamaulipas", "nuevo leon", "puebla", "oaxaca",
    "veracruz", "tabasco", "chiapas", "yucatan",
    "aguascalientes", "guanajuato", "queretaro", "hidalgo",
    "zacatecas", "san luis potosi", "nayarit", "colima",
    "morelos", "tlaxcala", "quintana roo", "campeche",
    "sinaloa", "guerrero", "michoacan",
    "distrito federal", "santa catarina", "minas gerais",
    "rio grande do sul", "parana", "bahia", "ceara", "alagoas",
    "pernambuco", "paraiba",
    "cundinamarca", "antioquia", "valle", "atlantico",
    "risaralda", "cordoba", "santander",
    "lima", "arequipa", "cusco", "chiclayo", "trujillo",
    "guayaquil", "quito", "cuenca", "manabi",
    "pichincha", "guayas", "cotopaxi", "azuay",
    "rio de janeiro", "sao paulo", "goias", "mato grosso",
    "rondnia", "acre", "amazonas", "para", "tocantins",
    "maranhao", "piaui", "pernambuco", "paraiba", "alagoas",
    "sergipe", "espirito santo",
    # Southeast Asia
    "singapore", "malaysia", "indonesia", "thailand", "vietnam",
    "philippines", "cambodia", "myanmar", "laos",
    "selangor", "kuala lumpur", "penang", "johor",
    "jakarta", "bali", "surabaya", "bandung", "medan",
    "bangkok", "chiang mai", "pattaya", "phuket",
    "ho chi minh city", "hanoi", "ha noi", "hcm",
    "manila", "cebu", "davao",
    "phnom penh", "yangon", "naypyidaw",
    "west java", "jawa barat", "jawa tengah", "sulawesi tengah",
    "banten", "lampung", "sumatera selatan", "sumatera utara",
    "west indonesia", "kalimantan tengah",
    "dki jakarta", "jakarta raya", "jakarta barat",
    # East Asia
    "japan", "south korea", "taiwan", "hong kong",
    "tokyo", "osaka", "kyoto", "yokohama", "nagoya",
    "seoul", "busan", "incheon", "daegu",
    "taipei", "taichung", "kaohsiung",
    "hong kong", "kowloon", "kongkong", "guangzhou",
    "gyeonggi-do", "gyeonggi",
    "hokkaido", "fukushima", "gifu prefecture",
    "kanagawa-ken", "mishima city",
    # South Korea
    "korea",
    # Others
    "russia", "moscow", "yekaterinburg",
    "ukraine", "kyiv",
    "iraq", "afghanistan", "kabul",
    "nepal", "kathmandu",
    "sri lanka",
    "mongolia", "ulaanbaatar",
    "europe", "africa", "asia",
}


def clean(name):
    """Lowercase and strip."""
    return name.lower().strip()


def normalize_entry(raw):
    """Strip extra whitespace, normalize internal spaces."""
    return re.sub(r'\s+', ' ', raw.strip())


def map_entry(raw):
    name = normalize_entry(raw)
    name_lower = name.lower()
    name_lower_strip = re.sub(r'\s+', ' ', name_lower).strip()

    # --- Direct match to US state list ---
    for state in US_STATE_LIST:
        if name_lower_strip == state.lower():
            return state

    # --- DC variants ---
    dc_patterns = [
        r'^d\.?c\.?$', r'^district\s+of\s+columbia',
        r'^distric\s+of\s+columbia', r'^distrito\s+de\s+columbia',
        r'^dc\s', r'washington.*d\.?c', r'washington dc',
        r'^d\.\s*c\.', r'^d\.\s*f\.',
    ]
    for p in dc_patterns:
        if re.search(p, name_lower_strip):
            return "District of Columbia"

    # --- Washington alone -> ambiguous, but usually Washington state (it's in state list) ---
    # Already handled by direct match above

    # --- State abbreviation patterns: "TX Texas", "Ca California" etc ---
    # Pattern: 2-letter abbrev followed by state name
    m = re.match(r'^([a-z]{2})\s+(.+)$', name_lower_strip)
    if m:
        abbrev_part = m.group(1).upper()
        rest = m.group(2).strip()
        if abbrev_part in ABBREV:
            # Check if rest matches or is close to the state name
            expected = ABBREV[abbrev_part].lower()
            if rest.startswith(expected[:4]) or expected.startswith(rest[:4]):
                return ABBREV[abbrev_part]
            # Also handle "Tx Tx" -> Texas
            if rest == abbrev_part.lower() or rest.upper() == abbrev_part:
                return ABBREV[abbrev_part]
            # e.g., "Tx Dallas" - still Texas
            if abbrev_part in ABBREV:
                return ABBREV[abbrev_part]

    # Pattern: state name followed by abbreviation or state name
    # e.g., "Texas Tx", "North Carolina Nc", "California California"
    for state in US_STATE_LIST:
        sl = state.lower()
        if name_lower_strip.startswith(sl):
            return state

    # Pattern: abbreviation alone or with junk
    m = re.match(r'^([a-z]{2})\s*[\-\./\|]?\s*(.*)$', name_lower_strip)
    if m:
        abbrev_part = m.group(1).upper()
        if abbrev_part in ABBREV:
            return ABBREV[abbrev_part]

    # Pattern: "Md Maryland", "Ma Massachusetts" etc (abbrev + state)
    m = re.match(r'^([a-z]{2})-([a-z].+)$', name_lower_strip)
    if m:
        abbrev_part = m.group(1).upper()
        if abbrev_part in ABBREV:
            return ABBREV[abbrev_part]

    # --- City lookup ---
    if name_lower_strip in CITY_TO_STATE:
        return CITY_TO_STATE[name_lower_strip]

    # Try partial city match (city name is a prefix of entry)
    for city, state in CITY_TO_STATE.items():
        if name_lower_strip == city:
            return state
        # e.g., "San Francisco Bay Area" -> California
        if name_lower_strip.startswith(city + ' '):
            return state
        if name_lower_strip.endswith(' ' + city):
            return state

    # --- Non-USA keyword match ---
    for kw in NON_USA_KEYWORDS:
        if kw in name_lower_strip:
            return "not-usa"

    # --- Additional non-US patterns ---
    non_usa_extra = [
        r'\buk\b', r'\bengland\b', r'\bscotland\b', r'\bwales\b',
        r'\bireland\b', r'\baustralia\b', r'\bnew zealand\b',
        r'\bcanada\b', r'\bindian?\b', r'\bpakistan\b',
        r'\bbangladesh\b', r'\bchina\b', r'\bjapan\b',
        r'\bkorea\b', r'\bsingapore\b', r'\bmalaysia\b',
        r'\bnigeria\b', r'\bkenya\b', r'\bghana\b',
        r'\bsouth africa\b', r'\bezypt\b',
        r'\bmexico\b', r'\bbrazil\b', r'\bargentina\b',
        r'\bcolumbia\b',  # Colombia country - note: also South Carolina city
        r'\beuropean?\b', r'\bafrican?\b',
    ]
    for p in non_usa_extra:
        if re.search(p, name_lower_strip):
            # Avoid false positives
            if 'south carolina' in name_lower_strip or 'district of columbia' in name_lower_strip:
                continue
            return "not-usa"

    # --- UK county patterns ---
    uk_counties = ['shire', 'eshire', 'ashire', 'yorkshire', 'fordshire',
                   'lancashire', 'midlands', 'wales', 'sussex', 'somerset']
    for uc in uk_counties:
        if name_lower_strip.endswith(uc) or uc in name_lower_strip:
            return "not-usa"

    # Try known non-US cities explicitly
    non_us_cities = {
        'london', 'paris', 'berlin', 'madrid', 'rome', 'amsterdam',
        'brussels', 'zurich', 'geneva', 'stockholm', 'oslo', 'copenhagen',
        'helsinki', 'warsaw', 'prague', 'budapest', 'bucharest', 'sofia',
        'zagreb', 'belgrade', 'athens', 'istanbul', 'ankara', 'cairo',
        'nairobi', 'lagos', 'accra', 'johannesburg', 'cape town', 'durban',
        'tokyo', 'osaka', 'seoul', 'beijing', 'shanghai', 'hong kong',
        'taipei', 'singapore', 'kuala lumpur', 'jakarta', 'bangkok',
        'manila', 'ho chi minh city', 'hanoi', 'yangon', 'phnom penh',
        'mumbai', 'delhi', 'bangalore', 'hyderabad', 'chennai', 'kolkata',
        'karachi', 'islamabad', 'lahore', 'dhaka', 'kathmandu',
        'sydney', 'melbourne', 'brisbane', 'perth', 'auckland',
        'toronto', 'montreal', 'vancouver', 'calgary', 'ottawa',
        'mexico city', 'sao paulo', 'rio de janeiro', 'buenos aires',
        'bogota', 'lima', 'santiago', 'quito', 'caracas',
        'dubai', 'abu dhabi', 'riyadh', 'doha', 'amman', 'beirut',
        'tehran', 'baghdad', 'kabul', 'moscow', 'kyiv',
        'vilnius', 'riga', 'tallinn',
    }
    if name_lower_strip in non_us_cities:
        return "not-usa"

    # --- NaN / Null / junk ---
    junk_patterns = [
        r'^nan$', r'^null$', r'^n/a$', r'^none$', r'^-+$',
        r'^_+$', r'^\*+$', r'^\.+$', r'^\(\)\s*-$',
        r'^remote', r'^virtual', r'^nationwide',
        r'^nation-wide', r'^worldwide', r'^anywhere',
        r'^available', r'^unknown', r'^various', r'^other',
        r'^global', r'^distributed', r'^anywhere',
        r'^remote-first', r'^remote-based',
        r'^http', r'^https',
        r'@',
        r'^startupland', r'^ghostland', r'^wonderland',
        r'^venueland', r'^meta-verse', r'^decentraland',
        r'^podcastland', r'^awesometown', r'^odyssey',
        r'^opportunity', r'^cosmos', r'^universe',
        r'^moon', r'^outer-rim',
    ]
    for p in junk_patterns:
        if re.search(p, name_lower_strip):
            return "unknown/invalid"

    # --- Misspellings of common states ---
    misspellings = {
        # California
        'californie': 'California', 'califrnia': 'California',
        'califorina': 'California', 'californi': 'California',
        'californien': 'California', 'calfornia': 'California',
        'californai': 'California', 'callifornia': 'California',
        'califormia': 'California', 'calif': 'California',
        'cali': 'California', 'kaliforniya': 'California',
        'kalifornien': 'California', 'kalifornia': 'California',
        # Florida
        'flrida': 'Florida', 'floride': 'Florida',
        'fl florida': 'Florida', 'flrida .': 'Florida',
        'flordia': 'Florida', 'florda': 'Florida',
        'florid': 'Florida', 'fla.': 'Florida',
        'fl. florida': 'Florida', 'floryda': 'Florida',
        'florida sunshine state': 'Florida',
        # Texas
        'tx texas': 'Texas', 'teksas': 'Texas',
        'texa': 'Texas', 'texs': 'Texas', 'texsas': 'Texas',
        'tex.': 'Texas', 'texas.': 'Texas',
        # Pennsylvania
        'pennsylvanie': 'Pennsylvania', 'pensilvnia': 'Pennsylvania',
        'pensilvania': 'Pennsylvania', 'pennsylvannia': 'Pennsylvania',
        'pennsylvania pa': 'Pennsylvania',
        # Massachusetts
        'massachussetts': 'Massachusetts', 'massachusets': 'Massachusetts',
        'masachusetts': 'Massachusetts', 'massachussetts': 'Massachusetts',
        'mass': 'Massachusetts', 'mass.': 'Massachusetts',
        'massachusets': 'Massachusetts',
        # Georgia
        'gergia': 'Georgia', 'georga': 'Georgia',
        'geogria': 'Georgia', 'georgie': 'Georgia',
        # Virginia
        'virgina': 'Virginia', 'virgnia': 'Virginia',
        'virgini': 'Virginia', 'virigina': 'Virginia',
        'viriginia': 'Virginia', 'vrginia': 'Virginia',
        'viginia': 'Virginia', 'virjinya': 'Virginia',
        'virginie': 'Virginia',
        # Tennessee
        'tennesee': 'Tennessee', 'tenessee': 'Tennessee',
        'tennesse': 'Tennessee', 'tenessee': 'Tennessee',
        'tenesse': 'Tennessee', 'tenn': 'Tennessee',
        'tenn.': 'Tennessee',
        # Minnesota
        'minesota': 'Minnesota', 'minesotta': 'Minnesota',
        'minn': 'Minnesota', 'minn.': 'Minnesota',
        'minnsota': 'Minnesota',
        # Oregon
        'oregn': 'Oregon', 'oregan': 'Oregon',
        'orgeon': 'Oregon', 'ore.': 'Oregon',
        # New York
        'newyork': 'New York', 'nueva york': 'New York',
        'nowy jork': 'New York', 'new-york': 'New York',
        'n.y.': 'New York', 'ny': 'New York',
        'n. y.': 'New York', 'new york state': 'New York',
        'nueva york': 'New York',
        # North Carolina
        'nc north carolina': 'North Carolina',
        'north carolina nc': 'North Carolina',
        'n. carolina': 'North Carolina',
        'n. c.': 'North Carolina',
        'n.c.': 'North Carolina',
        'nc': 'North Carolina',
        'nort carolina': 'North Carolina',
        'north-carolina': 'North Carolina',
        'carolina del norte': 'North Carolina',
        'caroline du nord': 'North Carolina',
        'carolina del nord': 'North Carolina',
        'kuzey karolina': 'North Carolina',
        'carolina do norte': 'North Carolina',
        'n carolina': 'North Carolina',
        'nc nc': 'North Carolina',
        # South Carolina
        'sc south carolina': 'South Carolina',
        'south carolina sc': 'South Carolina',
        's.c.': 'South Carolina',
        's. carolina': 'South Carolina',
        's. c.': 'South Carolina',
        'carolina del sur': 'South Carolina',
        'caroline du sud': 'South Carolina',
        'south caroline': 'South Carolina',
        'carolina del sud': 'South Carolina',
        # Indiana
        'indianna': 'Indiana',
        # Delaware
        'deleware': 'Delaware', 'delware': 'Delaware',
        'dalware': 'Delaware', 'dalaware': 'Delaware',
        'delawre': 'Delaware', 'dalaware': 'Delaware',
        # Nevada
        'navada': 'Nevada',
        # Louisiana
        'louisiane': 'Louisiana', 'louisian': 'Louisiana',
        'luisiana': 'Louisiana', 'lousiana': 'Louisiana',
        # Ohio
        'ohiio': 'Ohio', 'oh ohio': 'Ohio',
        # Kansas
        'ks': 'Kansas',
        # Missouri
        'misouri': 'Missouri', 'missuri': 'Missouri',
        'missour': 'Missouri', 'misuri': 'Missouri',
        'missori': 'Missouri',
        # West Virginia
        'w.va.': 'West Virginia', 'w.v.': 'West Virginia',
        'wv': 'West Virginia',
        # Connecticut
        'conneticut': 'Connecticut',
        'conn': 'Connecticut',
        # Rhode Island
        'r.i.': 'Rhode Island',
        # New Jersey
        'nueva jersey': 'New Jersey',
        'n.j.': 'New Jersey',
        'new-jersey': 'New Jersey',
        'newjersey': 'New Jersey',
        # New Mexico
        'nuevo mexico': 'New Mexico', 'nuevo mxico': 'New Mexico',
        'nm new mexico': 'New Mexico',
        # Idaho
        'idoha': 'Idaho',
        # Alaska
        'ak alaska': 'Alaska',
        # Maryland
        'mrayland': 'Maryland', 'marryland': 'Maryland',
        'md': 'Maryland',
        # District of Columbia
        'd.c.': 'District of Columbia',
        'd. c.': 'District of Columbia',
        'dc': 'District of Columbia',
        # York -> Pennsylvania
        'york': 'Pennsylvania',
        # Southern California region
        'southern california': 'California',
        'so paulo': 'not-usa', 'sao paulo': 'not-usa',
    }
    if name_lower_strip in misspellings:
        return misspellings[name_lower_strip]

    # --- Compound state mentions ---
    # If entry contains a US state keyword clearly
    for state in US_STATE_LIST:
        sl = state.lower()
        # Handle "River South Carolina", "State Of Oregon", etc.
        if sl in name_lower_strip:
            return state

    return "ambiguous/unknown"


def parse_line(line):
    """Parse a line from the states file.
    Format: name (padded) count pct%
    Returns (name, count) or None.
    """
    line = line.rstrip('\n')
    # Skip header lines
    if line.startswith('Top') or line.startswith(' ' * 30 + 'count') or line.startswith('state'):
        return None
    # Strip leading number+tab if present
    line = re.sub(r'^\s*\d+\s*→', '', line)
    # Now parse: "Name                     count   pct"
    # The name takes up most of the line, count is at the end
    m = re.match(r'^(.+?)\s{2,}(\d+)\s+[\d.]+\s*$', line)
    if not m:
        return None
    name = m.group(1).strip()
    count = int(m.group(2))
    return name, count


def main():
    results = []
    with open('/home/harshit.p/agent/states', 'r', encoding='utf-8') as f:
        for line in f:
            parsed = parse_line(line)
            if parsed is None:
                continue
            name, count = parsed
            mapped = map_entry(name)
            results.append((name, mapped, count))

    with open('/home/harshit.p/agent/state_mapping.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['original_entry', 'mapped_state', 'count'])
        for name, mapped, count in results:
            writer.writerow([name, mapped, count])

    print(f"Wrote {len(results)} rows to state_mapping.csv")

    # Summary
    from collections import Counter
    summary = Counter()
    for _, mapped, count in results:
        summary[mapped] += count
    print("\nTop mapped states by total count:")
    for state, cnt in summary.most_common(20):
        print(f"  {state}: {cnt:,}")


if __name__ == '__main__':
    main()
