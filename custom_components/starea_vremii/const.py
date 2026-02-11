"""Constants for the Starea Vremii integration."""

from datetime import timedelta

DOMAIN = "starea_vremii"
NAME = "Starea Vremii"
API_URL = "https://www.meteoromania.ro/wp-json/meteoapi/v2/starea-vremii"
CONF_MODE = "mode"
CONF_COUNTY = "county"
CONF_STATION = "station"
UPDATE_INTERVAL = timedelta(minutes=15)

MODE_COUNTY = "county"
MODE_STATION = "station"

COUNTY_STATION_MAP = {
    "Alba": "ALBA IULIA",
    "Arad": "ARAD",
    "Argeș": "PITESTI",
    "Bacău": "BACAU",
    "Bihor": "ORADEA",
    "Bistrița-Năsăud": "BISTRITA",
    "Botoșani": "BOTOSANI",
    "Brăila": "BRAILA",
    "Brașov": "BRASOV GHIMBAV",
    "București": "BUCURESTI BANEASA",
    "Buzău": "BUZAU",
    "Călărași": "CALARASI",
    "Caraș-Severin": "RESITA",
    "Cluj": "CLUJ-NAPOCA",
    "Constanța": "CONSTANTA",
    "Covasna": "SFANTU GHEORGHE (MUNTE)",
    "Dâmbovița": "TARGOVISTE",
    "Dolj": "CRAIOVA",
    "Galați": "GALATI",
    "Giurgiu": "GIURGIU",
    "Gorj": "TARGU JIU",
    "Harghita": "MIERCUREA CIUC",
    "Hunedoara": "DEVA",
    "Ialomița": "SLOBOZIA",
    "Iași": "IASI",
    "Ilfov": "BUCURESTI AFUMATI",
    "Maramureș": "BAIA MARE",
    "Mehedinți": "DROBETA TURNU SEVERIN",
    "Mureș": "TARGU MURES",
    "Neamț": "PIATRA NEAMT",
    "Olt": "SLATINA",
    "Prahova": "PLOIESTI",
    "Sălaj": "ZALAU",
    "Satu Mare": "SATU MARE",
    "Sibiu": "SIBIU",
    "Suceava": "SUCEAVA",
    "Teleorman": "ALEXANDRIA",
    "Timiș": "TIMISOARA",
    "Tulcea": "TULCEA",
    "Vâlcea": "RAMNICU VALCEA",
    "Vaslui": "VASLUI",
    "Vrancea": "FOCSANI"
}

COUNTIES = list(COUNTY_STATION_MAP.keys())
