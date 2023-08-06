import numpy as np
from sklearn.linear_model import LinearRegression

from .inflator import (
    taux_croissance_pib_nominal_par_tete,
    smpt_growth_by_year,
    total_annuel_salaires,
    revalorisation_retraite,
    reval_chomage,
    nb_foyers_par_annee,
    population_france_metropolitaine,
    population_france_totale,
    variation_annuelle_irl,
)


# Regression linéaire pour estimer les salaires des années futures
def projection_salaires(yearf):
    yearf = int(yearf)
    salaires_annuels = total_annuel_salaires.copy()

    last_known = int(list(total_annuel_salaires.keys())[-1])
    print(
        "Attention, les années au-dessus de ",
        last_known,
        " sont estimées par régression linéaire",
    )

    # Linear Regression
    # X = np.array([int(i) for i in range(len(inflation_sal.values()))]).reshape(-1, 1)
    X = np.array([int(i) for i in total_annuel_salaires.keys()]).reshape(-1, 1)
    Y = np.array([float(i) for i in total_annuel_salaires.values()]).reshape(-1, 1)

    model = LinearRegression().fit(X, Y)
    for year in range(last_known + 1, yearf + 1):
        to_predict = np.array(year).reshape(-1, 1)

        prediction = model.predict(to_predict)[0][0]
        salaires_annuels[str(year)] = prediction

    return salaires_annuels


# INFLATION SALARIALE
def inflator_salarial(startp, endp):
    startp = int(startp)
    endp = int(endp)
    adjrate_sal = 1
    total_annuel_salaires_proj = projection_salaires(endp)
    # Calcul du taux d'inflation
    annees_connues = list(total_annuel_salaires_proj.keys())
    annees_connues.remove(annees_connues[0])  # On supprime l'année 1
    inflation_sal_proj = {}
    for year in annees_connues:
        inflation_sal_proj[year] = (
            total_annuel_salaires_proj[year]
            / total_annuel_salaires_proj[str(int(year) - 1)]
        )
    # Calcul du taux d'ajustement
    for year in range(startp + 1, endp + 1):
        adjrate_sal = adjrate_sal * inflation_sal_proj[str(year)]

    return adjrate_sal


# INFLATION SMPT
def inflator_smpt(startp, endp):
    startp = int(startp)
    endp = int(endp)
    # Calcul du taux d'inflation economique sur plusieurs années
    adjrate_smpt = 1
    for year in range(startp, endp):
        rateinfla = smpt_growth_by_year[str(year)]
        adjrate_smpt = adjrate_smpt * (1 + rateinfla / 100)  # Car on a les données en %
    # print("Taux d'ajustement economique : ", adjrate_eco)

    return adjrate_smpt


# INFLATION ECONOMIQUE
def inflator_economique(startp, endp):
    startp = int(startp)
    endp = int(endp)
    # Calcul du taux d'inflation economique sur plusieurs années
    adjrate_eco = 1
    for year in range(startp, endp):
        rateinfla = taux_croissance_pib_nominal_par_tete[str(year)]
        adjrate_eco = adjrate_eco * (1 + rateinfla / 100)  # Car on a les données en %
    # print("Taux d'ajustement economique : ", adjrate_eco)

    return adjrate_eco


# REVALORISATION DES RETRAITES
def inflator_retraite(startp, endp):
    startp = int(startp)
    endp = int(endp)
    # Calcul du taux d'inflation des retraites sur plusieurs années
    adjrate_ret = 1
    for year in range(startp, endp):
        print(year)
        rateinfla = revalorisation_retraite[str(year)]
        adjrate_ret = adjrate_ret * (1 + rateinfla / 100)  # Car on a les données en %
    # print("Taux d'ajustement de revalorisation des retraites: ", adjrate_ret)

    return adjrate_ret


# REVALORISATION DU CHOMAGE
def inflator_chomage(startp, endp):
    startp = int(startp)
    endp = int(endp)
    # Calcul du taux d'inflation du chomage sur plusieurs années
    adjrate_chom = 1
    for year in range(startp, endp):
        rateinfla = reval_chomage[str(year)]
        adjrate_chom = adjrate_chom * (1 + rateinfla / 100)  # Car on a les données en %
    # print("Taux d'ajustement de revalorisation du chômage: ", adjrate_chom)

    return adjrate_chom


# REVALORISATION LOYERS
def inflator_irl(startp, endp):
    startp = int(startp)
    endp = int(endp)
    # Calcul du taux d'inflation du chomage sur plusieurs années
    adjrate_irl = 1
    for year in range(startp, endp):
        rateinfla = variation_annuelle_irl[str(year)]
        adjrate_irl = adjrate_irl * (1 + rateinfla / 100)  # Car on a les données en %
    # print("Taux d'ajustement de revalorisation du chômage: ", adjrate_chom)

    return adjrate_irl


def inflation_foyers_fiscaux(year_end):
    # FOYERS FISCAUX, DATA ET PROJECTION
    nb_foyers = nb_foyers_par_annee.copy()
    last_known = int(list(nb_foyers.keys())[-1])

    # Regression linéaire pour estimer le nombre de foyers des années futures
    if last_known < year_end:
        print(
            "Attention, les années au-dessus de ",
            last_known,
            " sont estimées par régression linéaire",
        )

        # Linear Regression
        X = np.array([int(i) for i in nb_foyers_par_annee.keys()]).reshape(-1, 1)
        Y = np.array([float(i) for i in nb_foyers_par_annee.values()]).reshape(-1, 1)

        model = LinearRegression().fit(X, Y)
        for year in range(last_known + 1, year_end + 1):
            to_predict = np.array(year).reshape(-1, 1)
            prediction = round(model.predict(to_predict)[0][0], 0)
            nb_foyers[str(year)] = prediction

    print("Objectif de ", nb_foyers[str(year_end)], "foyers fiscaux en ", year_end)

    return nb_foyers[str(year_end)]


def get_total_population(year):
    print("On calibre sur le total de foyers")

    return inflation_foyers_fiscaux(year)


def inflation_population(startp, endp, only_metropole=True):
    if only_metropole:
        taux = (
            population_france_metropolitaine[endp]
            / population_france_metropolitaine[startp]
        )
    else:
        taux = population_france_totale[endp] / population_france_totale[startp]
    return taux


def inflation_coefs(variables, startp, endp, ajustement_pop=True):
    inverse = False
    if startp > endp:
        temp = startp
        startp = endp
        endp = temp
        inverse = True

    inflator_by_variable = {}

    cols_type_pop = [
        "weight_familles",
        "weight_foyers",
        "weight_individus",
        "weight_menages",
        "wprm",
    ]
    adjrate_pop = inflation_population(startp, endp)

    # Variables indexées sur l'inflation salariale
    cols_type_salarial = [
        "salaire_de_base",
        "traitement_indiciaire_brut",
        "primes_fonction_publique",
        "revenus_capitaux_prelevement_liberatoire",
        "revenus_capitaux_prelevement_bareme",
        "revenus_capitaux_prelevement_forfaitaire_unique_ir",
        "rente_viagere_titre_onereux_net",
        "revenu_categoriel_foncier",
        "assiette_csg_plus_values",
        "reductions",
        "credits_impot",
    ]
    adjrate_sal = inflator_smpt(startp, endp)

    # Variables indexées sur l'indice des prix à la consommation
    cols_type_idc = [
        "revenus_capitaux_prelevement_liberatoire",
        "revenus_capitaux_prelevement_bareme",
        "revenus_capitaux_prelevement_forfaitaire_unique_ir",
        "rente_viagere_titre_onereux_net",
        "revenu_categoriel_foncier",
        "assiette_csg_plus_values",
        "reductions",
        "credits_impot",
        "pensions_alimentaires_percues",
        "pension_invalidite",
        "rpns_imposables",
    ]
    adjrate_eco = inflator_economique(startp, endp)

    # Variables indexées sur la revalorisation des retraites
    cols_retraite = ["retraite_brute", "pre_retraite"]
    adjrate_ret = inflator_retraite(startp, endp)

    # Variables indexées sur la revalorisation des indemnisations de chômage
    cols_chomage = ["chomage_brut"]
    adjrate_chom = inflator_chomage(startp, endp)

    cols_loyers = ["loyer"]
    adjrate_loyer = inflator_irl(startp, endp)

    if inverse:
        adjrate_pop = 1 / adjrate_pop
        adjrate_sal = 1 / adjrate_sal
        adjrate_eco = 1 / adjrate_eco
        adjrate_ret = 1 / adjrate_ret
        adjrate_chom = 1 / adjrate_chom
        adjrate_loyer = 1 / adjrate_loyer

    if ajustement_pop:
        taux_pop = adjrate_pop
    else:
        taux_pop = 1

    # ON INFLATE
    for col in variables:
        # Type population
        if col in cols_type_pop:
            inflator_by_variable.update({col: adjrate_pop})
        # Type 'salarial'
        elif col in cols_type_salarial:
            inflator_by_variable.update({col: adjrate_sal / taux_pop})
        # Type IDC
        elif col in cols_type_idc:
            inflator_by_variable.update({col: adjrate_eco / taux_pop})
        # Type retraite
        elif col in cols_retraite:
            inflator_by_variable.update({col: adjrate_ret / taux_pop})
        # Type chomage
        elif col in cols_chomage:
            inflator_by_variable.update({col: adjrate_chom / taux_pop})
        # Type irl
        elif col in cols_loyers:
            inflator_by_variable.update({col: adjrate_loyer})

    return inflator_by_variable
