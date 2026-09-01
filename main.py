import math
from datetime import datetime, timezone
import flet as ft

# --- Variable globale pour la page ---
current_page = None

# --- CATALOGUE DES ÉTOILES (GHA Aries corrigé + Déclinaison) ---
STARS_CATALOG = {
    "Acamar": {"gha_aries_corr": 315.15, "dec": -40.15},
    "Achernar": {"gha_aries_corr": 335.24, "dec": -57.14},
    "Acrux": {"gha_aries_corr": 173.05, "dec": -63.11},
    "Adhara": {"gha_aries_corr": 255.09, "dec": -28.59},
    "Aldebaran": {"gha_aries_corr": 290.44, "dec": 16.32},
    "Alioth": {"gha_aries_corr": 166.17, "dec": 55.51},
    "Alkaid": {"gha_aries_corr": 152.96, "dec": 49.13},
    "Al Nair": {"gha_aries_corr": 27.38, "dec": -46.52},
    "Alnilam": {"gha_aries_corr": 275.43, "dec": -1.12},
    "Alphard": {"gha_aries_corr": 217.52, "dec": -8.44},
    "Alphecca": {"gha_aries_corr": 126.07, "dec": 26.39},
    "Alpheratz": {"gha_aries_corr": 357.77, "dec": 29.11},
    "Altair": {"gha_aries_corr": 62.01, "dec": 8.53},
    "Ankaa": {"gha_aries_corr": 353.10, "dec": -42.12},
    "Antares": {"gha_aries_corr": 112.21, "dec": -26.28},
    "Arcturus": {"gha_aries_corr": 145.91, "dec": 19.05},
    "Atria": {"gha_aries_corr": 107.21, "dec": -69.03},
    "Avior": {"gha_aries_corr": 234.17, "dec": -59.34},
    "Bellatrix": {"gha_aries_corr": 278.28, "dec": 6.22},
    "Betelgeuse": {"gha_aries_corr": 270.97, "dec": 7.24},
    "Canopus": {"gha_aries_corr": 263.92, "dec": -52.42},
    "Capella": {"gha_aries_corr": 280.64, "dec": 46.01},
    "Deneb": {"gha_aries_corr": 49.29, "dec": 45.21},
    "Denebola": {"gha_aries_corr": 182.29, "dec": 14.28},
    "Diphda": {"gha_aries_corr": 349.12, "dec": -17.53},
    "Dubhe": {"gha_aries_corr": 193.87, "dec": 61.39},
    "Elnath": {"gha_aries_corr": 278.08, "dec": 28.37},
    "Eltanin": {"gha_aries_corr": 90.44, "dec": 51.29},
    "Enif": {"gha_aries_corr": 33.43, "dec": 9.58},
    "Fomalhaut": {"gha_aries_corr": 15.58, "dec": -29.31},
    "Gacrux": {"gha_aries_corr": 171.97, "dec": -57.12},
    "Gienah": {"gha_aries_corr": 175.85, "dec": -17.38},
    "Hadar": {"gha_aries_corr": 148.74, "dec": -60.27},
    "Hamal": {"gha_aries_corr": 327.93, "dec": 23.33},
    "Kaus Australis": {"gha_aries_corr": 83.71, "dec": -34.23},
    "Kochab": {"gha_aries_corr": 137.20, "dec": 74.05},
    "Markab": {"gha_aries_corr": 13.34, "dec": 15.18},
    "Menkar": {"gha_aries_corr": 314.11, "dec": 4.09},
    "Menkent": {"gha_aries_corr": 148.04, "dec": -36.27},
    "Miaplacidus": {"gha_aries_corr": 221.41, "dec": -69.47},
    "Mirfak": {"gha_aries_corr": 308.79, "dec": 49.55},
    "Nunki": {"gha_aries_corr": 75.94, "dec": -26.16},
    "Peacock": {"gha_aries_corr": 53.11, "dec": -56.40},
    "Polaris": {"gha_aries_corr": 316.02, "dec": 89.21},
    "Pollux": {"gha_aries_corr": 243.52, "dec": 28.01},
    "Procyon": {"gha_aries_corr": 244.95, "dec": 5.10},
    "Rasalhague": {"gha_aries_corr": 96.03, "dec": 12.33},
    "Regulus": {"gha_aries_corr": 207.39, "dec": 11.52},
    "Rigel": {"gha_aries_corr": 281.08, "dec": -8.11},
    "Rigil Kentaurus": {"gha_aries_corr": 139.87, "dec": -60.54},
    "Sabik": {"gha_aries_corr": 102.10, "dec": -15.44},
    "Shaula": {"gha_aries_corr": 96.18, "dec": -37.07},
    "Sirius": {"gha_aries_corr": 258.30, "dec": -16.44},
    "Spica": {"gha_aries_corr": 158.27, "dec": -11.15},
    "Suhail": {"gha_aries_corr": 222.89, "dec": -43.30},
    "Vega": {"gha_aries_corr": 80.36, "dec": 38.48},
    "Zubenelgenubi": {"gha_aries_corr": 137.01, "dec": -16.07},
}

# --- PARAMÈTRES POUR LES PLANÈTES (VSOP87 simplifié) ---
PLANETS_VSOP = {
    "Vénus": {"L0": [4.898950, 0.01113429, 0.0], "B": [0.0, 0.0, 0.0], "R": [0.723332, 0.00000028], "sd": 0.5},
    "Mars": {"L0": [1.408554, 0.01555197, 0.0], "B": [0.0, 0.0, 0.0], "R": [1.523679, 0.00000093], "sd": 0.1},
    "Jupiter": {"L0": [5.584815, 0.00299618, 0.0], "B": [0.0, 0.0, 0.0], "R": [5.202603, -0.00000152], "sd": 0.5},
    "Saturne": {"L0": [6.161520, 0.00120055, 0.0], "B": [0.0, 0.0, 0.0], "R": [9.554909, -0.00000208], "sd": 0.4},
}

# --- PARAMÈTRES POUR LA LUNE (ELP/MPP02 simplifié) ---
MOON_PARAMS = {
    "L0": [4.719967, 0.22997150, 0.00000011],
    "B": [0.0, 0.00010313, 0.0],
    "D": [1.0 / 384400, 0.0],
    "sd": 15.0,
}

ASTRES_LIST = ["Soleil", "Lune", "Vénus", "Mars", "Jupiter", "Saturne"] + sorted(list(STARS_CATALOG.keys()))

# --- CACHE POUR LES ÉPHÉMÉRIDES ---
ephemerides_cache = {}

# --- FONCTIONS UTILITAIRES ---
def deg_min_to_decimal(deg, min_val):
    return float(deg) + float(min_val) / 60.0

def decimal_to_deg_min(decimal):
    deg = int(decimal)
    min_val = (decimal - deg) * 60.0
    return deg, min_val

def time_to_hms(time_str):
    h, m, s = map(int, time_str.split(":"))
    return h, m, s

def hms_to_time(h, m, s):
    return f"{h:02d}:{m:02d}:{s:02d}"

# --- FONCTIONS DE CALCUL DES ÉPHÉMÉRIDES ---
def get_julian_date(dt):
    Y, M, D_j = dt.year, dt.month, dt.day
    if M <= 2:
        Y -= 1
        M += 12
    A = int(Y / 100)
    B = 2 - A + int(A / 4)
    jd = int(365.25 * (Y + 4716)) + int(30.6001 * (M + 1)) + D_j + B - 1524.5
    jd += (dt.hour + dt.minute / 60.0 + dt.second / 3600.0) / 24.0
    return jd

def get_gha_aries(jd):
    T = (jd - 2451545.0) / 36525.0
    gha_aries = (280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.0003879 * T * T) % 360.0
    return gha_aries

def get_sun_ephemerides(jd):
    T = (jd - 2451545.0) / 36525.0
    L0 = (280.46646 + 36000.76983 * T + 0.0003032 * T * T) % 360.0
    M = (357.52911 + 35999.05029 * T - 0.0001537 * T * T) % 360.0
    lambda_sun = L0 + (1.914602 - 0.004817 * T) * math.sin(math.radians(M)) + (0.019993 - 0.000101 * T) * math.sin(math.radians(2 * M))
    epsilon = 23.439291 - 0.0130042 * T - 0.00000016 * T * T
    dec = math.degrees(math.asin(math.sin(math.radians(epsilon)) * math.sin(math.radians(lambda_sun))))
    alpha = math.degrees(math.atan2(
        math.cos(math.radians(epsilon)) * math.sin(math.radians(lambda_sun)),
        math.cos(math.radians(lambda_sun))
    ))
    EqT = 4 * (L0 - alpha)
    if EqT > 20:
        EqT -= 1440
    if EqT < -20:
        EqT += 1440
    gha_aries = get_gha_aries(jd)
    gha_sun = (gha_aries - alpha) % 360.0
    sd = 16.0 / 60.0
    return gha_sun, dec, sd, EqT

def get_moon_ephemerides(jd):
    T = (jd - 2451545.0) / 36525.0
    days_since_j2000 = jd - 2451545.0
    L0 = (MOON_PARAMS["L0"][0] + MOON_PARAMS["L0"][1] * days_since_j2000 + MOON_PARAMS["L0"][2] * days_since_j2000 * days_since_j2000) % (2 * math.pi)
    B = MOON_PARAMS["B"][0] + MOON_PARAMS["B"][1] * days_since_j2000
    D = MOON_PARAMS["D"][0] + MOON_PARAMS["D"][1] * days_since_j2000
    lambda_moon = math.degrees(L0)
    beta_moon = math.degrees(B)
    gha_aries = get_gha_aries(jd)
    gha_moon = (gha_aries + 180.0 - lambda_moon) % 360.0
    dec = math.degrees(math.asin(
        math.sin(math.radians(beta_moon)) * math.cos(math.radians(23.439)) +
        math.cos(math.radians(beta_moon)) * math.sin(math.radians(23.439)) * math.sin(math.radians(lambda_moon))
    ))
    sd = MOON_PARAMS["sd"] / 60.0
    return gha_moon, dec, sd, 0.0

def get_planet_ephemerides(planet, jd):
    T = (jd - 2451545.0) / 36525.0
    params = PLANETS_VSOP[planet]
    L0 = params["L0"][0] + params["L0"][1] * T + params["L0"][2] * T * T
    B = params["B"][0] + params["B"][1] * T + params["B"][2] * T * T
    R = params["R"][0] + params["R"][1] * T
    lambda_planet = math.degrees(L0)
    beta_planet = math.degrees(B)
    gha_aries = get_gha_aries(jd)
    gha_planet = (gha_aries + lambda_planet - 180.0) % 360.0
    epsilon = 23.439291 - 0.0130042 * T
    dec = math.degrees(math.asin(
        math.sin(math.radians(beta_planet)) * math.cos(math.radians(epsilon)) +
        math.cos(math.radians(beta_planet)) * math.sin(math.radians(epsilon)) * math.sin(math.radians(lambda_planet))
    ))
    sd = params["sd"] / 60.0
    return gha_planet, dec, sd, 0.0

def get_coordonnees_ephemerides(astre, jd):
    cache_key = (astre, round(jd, 6))
    if cache_key in ephemerides_cache:
        return ephemerides_cache[cache_key]
    if astre in STARS_CATALOG:
        gha_aries = get_gha_aries(jd)
        gha = (gha_aries + STARS_CATALOG[astre]["gha_aries_corr"]) % 360.0
        dec = STARS_CATALOG[astre]["dec"]
        result = (gha, dec, 0.0, 0.0)
    elif astre == "Soleil":
        result = get_sun_ephemerides(jd)
    elif astre == "Lune":
        result = get_moon_ephemerides(jd)
    elif astre in PLANETS_VSOP:
        result = get_planet_ephemerides(astre, jd)
    else:
        result = (0.0, 0.0, 0.0, 0.0)
    ephemerides_cache[cache_key] = result
    return result

def get_refraction(h_accessible, temperature=10.0, pressure=1010.0):
    if h_accessible < -0.575:
        return 0.0
    h_rad = math.radians(h_accessible)
    refraction = (1.02 * (pressure / 1010.0) * (283.0 / (273.0 + temperature))) / math.tan(h_rad + 10.3 / (h_accessible + 5.11))
    return refraction / 3600.0

def get_hauteur_vraie():
    hi_deg_val = float(hi_deg.value or 0)
    hi_min_val = float(hi_min.value or 0)
    hi_decimale_val = float(hi_decimale.value or 0)
    hi_decimal = deg_min_to_decimal(hi_deg_val, hi_min_val) + hi_decimale_val / 60.0
    colli_min = float(collimation.value or 0)
    colli_decimal = colli_min / 60.0
    oeil = float(hauteur_oeil.value or 0)
    depression = (1.76 * math.sqrt(oeil)) / 60.0
    h_accessible = hi_decimal - colli_decimal - depression
    temperature = float(temperature_input.value or 10.0)
    pressure = float(pressure_input.value or 1010.0)
    refraction = get_refraction(h_accessible, temperature, pressure)
    return h_accessible - refraction

def get_longitude_estee():
    lon_deg_val = float(lon_deg.value or 0)
    lon_min_val = float(lon_min.value or 0)
    lon_decimal = deg_min_to_decimal(lon_deg_val, lon_min_val)
    return -lon_decimal if lon_card.value == "W" else lon_decimal

def pre_regler_sextant(e):
    try:
        astre = astre_spinner.value
        lat_deg_val = float(lat_deg.value or 0)
        lat_min_val = float(lat_min.value or 0)
        lat = deg_min_to_decimal(lat_deg_val, lat_min_val)
        if lat_card.value == "S":
            lat = -lat

        lon_est = get_longitude_estee()
        dt = datetime.strptime(f"{date_input.value} {time_input.value}", "%Y-%m-%d %H:%M:%S")
        jd = get_julian_date(dt)

        gha, dec, sd, _ = get_coordonnees_ephemerides(astre, jd)
        ahl = (gha + lon_est) % 360.0
        lat_rad, dec_rad, ahl_rad = map(math.radians, [lat, dec, ahl])

        sin_hc = (math.sin(lat_rad) * math.sin(dec_rad)) + (math.cos(lat_rad) * math.cos(dec_rad) * math.cos(ahl_rad))
        hc = math.degrees(math.asin(max(-1.0, min(1.0, sin_hc))))

        cos_z = (math.sin(dec_rad) - (math.sin(lat_rad) * math.sin(math.radians(hc)))) / (math.cos(lat_rad) * math.cos(math.radians(hc)))
        z_deg = math.degrees(math.acos(max(-1.0, min(1.0, cos_z))))
        azimut = 360 - z_deg if math.sin(ahl_rad) > 0 else z_deg

        hc_deg, hc_min = decimal_to_deg_min(hc)
        azimut_deg, azimut_min = decimal_to_deg_min(azimut)

        texte = (
            f"--- PRÉRÉGLAGE DU SEXTANT POUR {astre} ---\n"
            f"Position: Lat {lat_deg_val}° {lat_min_val}' {lat_card.value}, "
            f"Lon {float(lon_deg.value or 0)}° {float(lon_min.value or 0)}' {lon_card.value}\n"
            f"Date/Heure: {date_input.value} {time_input.value} UTC\n\n"
            f"Hauteur théorique (Hc): {hc_deg}° {hc_min:.1f}'\n"
            f"Azimut (Z): {azimut_deg}° {azimut_min:.1f}'\n\n"
            f"👉 Réglez votre sextant sur une hauteur proche de {hc_deg}° {hc_min:.1f}' et "
            f"viser dans la direction {azimut_deg}° {azimut_min:.1f}'."
        )

        result_text.value = texte
        current_page.update()
    except Exception as ex:
        result_text.value = f"Erreur : {str(ex)}"
        current_page.update()

def effacer_tout(e):
    global droites_calculees, ephemerides_cache
    droites_calculees = []
    ephemerides_cache = {}
    lat_deg.value = ""
    lat_min.value = ""
    hi_decimale.value = ""
    lat_card.value = "N"
    lon_deg.value = ""
    lon_min.value = ""
    lon_card.value = "W"
    date_input.value = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    time_input.value = datetime.now(timezone.utc).strftime("%H:%M:%S")
    astre_spinner.value = "Soleil"
    hi_deg.value = ""
    hi_min.value = ""
    collimation.value = "0.0"
    hauteur_oeil.value = "2.5"
    bord_spinner.value = "Inférieur"
    cap_suivi.value = "0"
    dist_parcourue.value = "0.0"
    temperature_input.value = "10.0"
    pressure_input.value = "1010.0"
    result_text.value = "Tous les champs ont été réinitialisés."
    current_page.update()

def preparer_meridienne(e):
    try:
        dt_date = datetime.strptime(date_input.value, "%Y-%m-%d")
        jd_midi = get_julian_date(dt_date.replace(hour=12, minute=0, second=0))
        _, _, _, eq_temps = get_coordonnees_ephemerides("Soleil", jd_midi)
        lon_est = get_longitude_estee()
        heure_passage_dec = 12.0 - (eq_temps / 60.0) - (lon_est / 15.0)
        heures = int(heure_passage_dec)
        minutes = int((heure_passage_dec - heures) * 60)
        secondes = int((((heure_passage_dec - heures) * 60) - minutes) * 60)
        heure_str = hms_to_time(heures, minutes, secondes)
        time_input.value = heure_str
        result_text.value = (
            f"--- PRÉPARATION MÉRIDIENNE ---\n"
            f"Heure du passage au Méridien : {heure_str} UTC\n"
            f"Copiée dans le champ Heure."
        )
        current_page.update()
    except Exception as ex:
        result_text.value = f"Erreur : {str(ex)}"
        current_page.update()

def calculer_latitude_meridienne(e):
    try:
        ho = get_hauteur_vraie()
        dt = datetime.strptime(f"{date_input.value} {time_input.value}", "%Y-%m-%d %H:%M:%S")
        _, dec_soleil, sd_soleil, _ = get_coordonnees_ephemerides("Soleil", get_julian_date(dt))
        if bord_spinner.value == "Inférieur":
            ho += sd_soleil
        elif bord_spinner.value == "Supérieur":
            ho -= sd_soleil
        z_zenith = 90.0 - ho
        lat_calculee = z_zenith + dec_soleil
        card = "N" if lat_calculee >= 0 else "S"
        lat_abs = abs(lat_calculee)
        lat_deg, lat_min = decimal_to_deg_min(lat_abs)
        result_text.value = (
            f"--- MÉRIDIENNE ---\n"
            f"Ho : {ho:.4f}° | Dec : {dec_soleil:.4f}°\n"
            f"👉 LATITUDE MÉRIDIENNE : {lat_deg}° {lat_min:.1f}' {card}"
        )
        lat_deg.value = str(lat_deg)
        lat_min.value = f"{lat_min:.1f}"
        lat_card.value = card
        current_page.update()
    except Exception as ex:
        result_text.value = f"Erreur : {str(ex)}"
        current_page.update()

def calculer_droite(e):
    try:
        astre = astre_spinner.value
        lat_deg_val = float(lat_deg.value or 0)
        lat_min_val = float(lat_min.value or 0)
        lat = deg_min_to_decimal(lat_deg_val, lat_min_val)
        if lat_card.value == "S":
            lat = -lat
        lon_est = get_longitude_estee()
        ho = get_hauteur_vraie()
        dt = datetime.strptime(f"{date_input.value} {time_input.value}", "%Y-%m-%d %H:%M:%S")
        res = get_coordonnees_ephemerides(astre, get_julian_date(dt))
        ghag, dec_astre, sd_astre, _ = res
        if bord_spinner.value == "Inférieur":
            ho += sd_astre
        elif bord_spinner.value == "Supérieur":
            ho -= sd_astre
        ahl = ghag + lon_est
        lat_rad, dec_rad, ahl_rad = map(math.radians, [lat, dec_astre, ahl])
        sin_hc = (math.sin(lat_rad) * math.sin(dec_rad)) + (math.cos(lat_rad) * math.cos(dec_rad) * math.cos(ahl_rad))
        hc = math.degrees(math.asin(max(-1.0, min(1.0, sin_hc))))
        cos_z = (math.sin(dec_rad) - (math.sin(lat_rad) * math.sin(math.radians(hc)))) / (math.cos(lat_rad) * math.cos(math.radians(hc)))
        z_deg = math.degrees(math.acos(max(-1.0, min(1.0, cos_z))))
        azimut = 360 - z_deg if math.sin(ahl_rad) > 0 else z_deg
        intercept = (ho - hc) * 60.0
        azimut_deg, azimut_min = decimal_to_deg_min(azimut)
        droites_calculees.append({
            "astre": astre,
            "intercept": intercept,
            "azimut_deg": azimut_deg,
            "azimut_min": azimut_min,
            "lat_deg": lat_deg_val,
            "lat_min": lat_min_val,
            "lat_card": lat_card.value,
            "lon_deg": float(lon_deg.value or 0),
            "lon_min": float(lon_min.value or 0),
            "lon_card": lon_card.value,
            "timestamp": dt.strftime("%H:%M:%S"),
        })
        rafraichir_affichage()
    except Exception as ex:
        result_text.value = f"Erreur : {str(ex)}"
        current_page.update()

def appliquer_translation(e):
    try:
        cap_compas = float(cap_suivi.value or 0)
        distance_parcourue_mn = float(dist_parcourue.value or 0)
        cap_radians = math.radians(cap_compas)

        for droite in droites_calculees[:-1]:
            latitude_actuelle_degres = deg_min_to_decimal(droite["lat_deg"], droite["lat_min"])
            if droite["lat_card"] == "S":
                latitude_actuelle_degres = -latitude_actuelle_degres

            longitude_actuelle_degres = deg_min_to_decimal(droite["lon_deg"], droite["lon_min"])
            if droite["lon_card"] == "W":
                longitude_actuelle_degres = -longitude_actuelle_degres

            variation_latitude_degres = (distance_parcourue_mn * math.cos(cap_radians)) / 60.0
            nouvelle_latitude_degres = latitude_actuelle_degres + variation_latitude_degres

            latitude_moyenne_radians = math.radians(nouvelle_latitude_degres - (variation_latitude_degres / 2.0))
            variation_longitude_degres = (distance_parcourue_mn * math.sin(cap_radians) / math.cos(latitude_moyenne_radians)) / 60.0
            nouvelle_longitude_degres = longitude_actuelle_degres + variation_longitude_degres

            nouvelle_latitude_deg, nouvelle_latitude_min = decimal_to_deg_min(abs(nouvelle_latitude_degres))
            nouvelle_latitude_card = "S" if nouvelle_latitude_degres < 0 else "N"

            nouvelle_longitude_deg, nouvelle_longitude_min = decimal_to_deg_min(abs(nouvelle_longitude_degres))
            nouvelle_longitude_card = "W" if nouvelle_longitude_degres < 0 else "E"

            droite["lat_deg"] = nouvelle_latitude_deg
            droite["lat_min"] = nouvelle_latitude_min
            droite["lat_card"] = nouvelle_latitude_card
            droite["lon_deg"] = nouvelle_longitude_deg
            droite["lon_min"] = nouvelle_longitude_min
            droite["lon_card"] = nouvelle_longitude_card

        rafraichir_affichage(trans=True)
    except Exception as ex:
        result_text.value = f"Erreur lors de la translation : {str(ex)}"
        current_page.update()

def rafraichir_affichage(trans=False):
    texte = "--- DROITES SUR LA TABLE ---\n"
    if trans:
        texte += "[INFO] Droites translatées !\n\n"
    if not droites_calculees:
        texte += "Aucune droite calculée pour l'instant."
    else:
        for idx, d in enumerate(droites_calculees):
            sens = "Vers" if d["intercept"] >= 0 else "Loin"
            texte += (
                f"Série {idx+1} [{d['timestamp']}] - {d['astre']}:\n"
                f"  Z : {d['azimut_deg']}° {d['azimut_min']:.1f}' | "
                f"Intercept : {abs(d['intercept']):.1f} MN ({sens})\n"
                f"  Ref: Lat {d['lat_deg']}° {d['lat_min']:.1f}' {d['lat_card']}, "
                f"Lon {d['lon_deg']}° {d['lon_min']:.1f}' {d['lon_card']}\n"
            )
    result_text.value = texte
    current_page.update()

def main(page: ft.Page):
    global lat_deg, lat_min, hi_decimale, lat_card, lon_deg, lon_min, lon_card
    global date_input, time_input, astre_spinner, hi_deg, hi_min
    global collimation, hauteur_oeil, bord_spinner, cap_suivi, dist_parcourue
    global result_text, droites_calculees, temperature_input, pressure_input, current_page

    current_page = page
    page.title = "AstroNav"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0  # Pas de padding global pour utiliser tout l'espace
    page.safe_area = ft.SafeArea(all=True)  # Respecte les zones sûres (barre d'état, etc.)
    page.scroll = "auto"
    page.fonts = {
        "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap"
    }
    page.theme = ft.Theme(
        font_family="Roboto",
        page_transitions=ft.PageTransitionsTheme(
            android=ft.PageTransitionTheme.NONE,
            ios=ft.PageTransitionTheme.NONE,
        )
    )

    # --- Barre d'information en haut ---
    info_bar = ft.AppBar(
        title=ft.Text("AstroNav - Navigation Astronique", size=16, weight="bold"),
        center_title=True,
        bgcolor=ft.Colors.BLUE_GREY_900,
        actions=[
            ft.IconButton(
                icon=ft.icons.REFRESH,
                on_click=lambda e: effacer_tout(e),
                tooltip="Réinitialiser",
            ),
        ],
    )

    droites_calculees = []
    ephemerides_cache = {}

    # --- Style pour les champs ---
    text_field_style = {
        "width": 110,
        "height": 45,
        "text_size": 14,
        "border_color": ft.Colors.BLUE_GREY_700,
        "focused_border_color": ft.Colors.BLUE_400,
        "content_padding": ft.padding.only(left=10, right=10),
    }

    dropdown_style = {
        "width": 110,
        "height": 45,
        "text_size": 14,
    }

    button_style = {
        "height": 45,
        "bgcolor": ft.Colors.BLUE_GREY_800,
        "color": ft.Colors.WHITE,
        "shape": ft.RoundedRectangleBorder(radius=8),
        "expand": True,
    }

    # --- CHAMPS D'ENTRÉE : Position estimée ---
    lat_deg = ft.TextField(label="Lat Deg", **text_field_style)
    lat_min = ft.TextField(label="Lat Min", **text_field_style)
    lat_card = ft.Dropdown(label="N/S", options=[ft.dropdown.Option("N"), ft.dropdown.Option("S")], value="N", **dropdown_style)

    lon_deg = ft.TextField(label="Lon Deg", **text_field_style)
    lon_min = ft.TextField(label="Lon Min", **text_field_style)
    lon_card = ft.Dropdown(label="E/W", options=[ft.dropdown.Option("E"), ft.dropdown.Option("W")], value="W", **dropdown_style)

    current_time = datetime.now(timezone.utc)
    date_input = ft.TextField(label="Date", value=current_time.strftime("%Y-%m-%d"), **text_field_style)
    time_input = ft.TextField(label="Heure UTC", value=current_time.strftime("%H:%M:%S"), **text_field_style)

    # --- CHAMPS D'ENTRÉE : Sélection de l'astre et hauteur ---
    astre_spinner = ft.Dropdown(
        label="Astre",
        options=[ft.dropdown.Option(a) for a in ASTRES_LIST],
        value="Soleil",
        width=200,
        height=45,
        text_size=14,
    )

    hi_deg = ft.TextField(label="Hi Deg", **text_field_style)
    hi_min = ft.TextField(label="Hi Min", **text_field_style)
    hi_decimale = ft.TextField(label="Hi Dec", width=90, height=45, text_size=14, content_padding=ft.padding.only(left=10, right=10))

    # --- CHAMPS D'ENTRÉE : Corrections et paramètres ---
    collimation = ft.TextField(label="Collimation", value="0.0", **text_field_style)
    hauteur_oeil = ft.TextField(label="Hauteur Œil", value="2.5", **text_field_style)
    bord_spinner = ft.Dropdown(
        label="Bord visé",
        options=[
            ft.dropdown.Option("Inférieur"),
            ft.dropdown.Option("Supérieur"),
            ft.dropdown.Option("Milieu/Centre"),
        ],
        value="Inférieur",
        **dropdown_style,
    )

    temperature_input = ft.TextField(label="Température", value="10.0", **text_field_style)
    pressure_input = ft.TextField(label="Pression", value="1010.0", **text_field_style)

    # --- CHAMPS D'ENTRÉE : Estime (mouvement du navire) ---
    cap_suivi = ft.TextField(label="Cap", value="0", **text_field_style)
    dist_parcourue = ft.TextField(label="Distance", value="0.0", **text_field_style)

    # --- AFFICHAGE DES RÉSULTATS ---
    result_text = ft.Text(
        value="En attente de calcul...",
        size=14,
        color=ft.Colors.BLUE_GREY_300,
        selectable=True,
    )

    # --- MISE EN PAGE DE L'INTERFACE ---
    page.add(
        info_bar,  # Barre d'information en haut

        # --- Section : Position estimée ---
        ft.Container(
            content=ft.Column([
                ft.Text("📍 POSITION ESTIMÉE", weight="bold", color=ft.Colors.BLUE_200, size=16),
                ft.Row([lat_deg, lat_min, lat_card], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([lon_deg, lon_min, lon_card], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([date_input, time_input], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
            ], spacing=5),
            padding=10,
        ),

        ft.Divider(height=5, color=ft.Colors.BLUE_GREY_800),

        # --- Section : Préréglage du sextant ---
        ft.Container(
            content=ft.Column([
                ft.Text("🔭 PRÉRÉGLAGE DU SEXTANT", weight="bold", color=ft.Colors.YELLOW_200, size=16),
                ft.Row([astre_spinner], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    ft.Button(
                        "Calculer Hauteur/Azimut",
                        on_click=pre_regler_sextant,
                        height=45,
                        bgcolor=ft.Colors.YELLOW_700,
                        color=ft.Colors.BLACK,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        expand=True,
                    )
                ]),
            ], spacing=5),
            padding=10,
        ),

        ft.Divider(height=5, color=ft.Colors.BLUE_GREY_800),

        # --- Section : Méridienne (Soleil) ---
        ft.Container(
            content=ft.Column([
                ft.Text("☀️ MÉRIDIENNE", weight="bold", color=ft.Colors.ORANGE_200, size=16),
                ft.Row([
                    ft.Button(
                        "Calculer Heure",
                        on_click=preparer_meridienne,
                        **button_style,
                    ),
                    ft.Button(
                        "Calculer Latitude",
                        on_click=calculer_latitude_meridienne,
                        bgcolor=ft.Colors.GREEN_700,
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        height=45,
                        expand=True,
                    ),
                ], spacing=5),
            ], spacing=5),
            padding=10,
        ),

        ft.Divider(height=5, color=ft.Colors.BLUE_GREY_800),

        # --- Section : Droites successives ---
        ft.Container(
            content=ft.Column([
                ft.Text("📏 DROITES DE HAUTEUR", weight="bold", color=ft.Colors.GREEN_200, size=16),
                ft.Text("Hauteur instrumentale (Hi):", size=14, color=ft.Colors.BLUE_GREY_300),
                ft.Row([hi_deg, hi_min, hi_decimale], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([collimation, hauteur_oeil, bord_spinner], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([temperature_input, pressure_input], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
            ], spacing=5),
            padding=10,
        ),

        ft.Divider(height=5, color=ft.Colors.BLUE_GREY_800),

        # --- Section : Estime / Log ---
        ft.Container(
            content=ft.Column([
                ft.Text("⛵ ESTIME / LOG", weight="bold", color=ft.Colors.PURPLE_200, size=16),
                ft.Row([cap_suivi, dist_parcourue], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    ft.Button("Calculer Droite", on_click=calculer_droite, **button_style),
                ]),
                ft.Row([
                    ft.Button("Translater", on_click=appliquer_translation, **button_style),
                    ft.Button("Effacer tout", on_click=effacer_tout, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=8), height=45, expand=True),
                ], spacing=5),
            ], spacing=5),
            padding=10,
        ),

        ft.Divider(height=5, color=ft.Colors.BLUE_GREY_800),

        # --- Affichage des résultats ---
        ft.Container(
            content=result_text,
            padding=15,
            bgcolor=ft.Colors.BLUE_GREY_900,
            border_radius=8,
            margin=ft.margin.only(bottom=10),
            expand=True,
        ),
    )

ft.app(target=main, view=ft.AppView.FLET_APP)  # Utilise FLET_APP pour une meilleure intégration mobile
