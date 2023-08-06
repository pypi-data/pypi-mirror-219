import copy
import unittest

import pandas as pd
from leximpact_aggregates.aggregate import AggregateManager
from decouple import config


tc = unittest.TestCase()

# Import des années
annee_erfs = config("YEAR_ERFS")
annee_pote = config("YEAR_POTE")
annee_de_calcul = config("YEAR_COMPUTATION")
aggregates_path = config("AGREGATS_PATH")

dico_var = {
    "entity_list": {"individu", "menage", "famille", "foyer_fiscal"},
    "individu": {
        "weight": "weight_individus",
        "id": "index",
        "filter_by_name": "menage_ordinaire_individus",
        "plural": "individus",
    },
    "famille": {
        "weight": "weight_familles",
        "id": "famille_id",
        "filter_by_name": "menage_ordinaire",
        "plural": "familles",
    },
    "menage": {
        "weight": "weight_menages",
        "id": "menage_id",
        "filter_by_name": "menage_ordinaire_familles",
        "plural": "menages",
    },
    "foyer_fiscal": {
        "weight": "weight_foyers",
        "id": "foyer_fiscal_id",
        "filter_by_name": "menage_ordinaire_foyers_fiscaux",
        "plural": "foyers_fiscaux",
    },
}


def individus_to_entity(
    tax_benefit_system, sample_individus, entity, specific_wprms=None
):
    """
    Regroupe un échantillon par individus en échantillon par entité de groupe
    """
    assert entity != "individu"

    id_entity = dico_var[entity]["id"]
    wprm = dico_var[entity]["weight"]

    print(
        "On a une base initiale de ",
        len(sample_individus),
        " individus pour ",
        sample_individus[id_entity].nunique(),
        entity,
        "s",
    )

    # Cas d'une base normale (i.e. PAS en cours de calibration)
    if specific_wprms is None:
        assert (
            sample_individus["weight_individus"] == sample_individus["weight_familles"]
        ).all()
        assert (
            sample_individus["weight_familles"] == sample_individus["weight_foyers"]
        ).all()
        all_wprms = [
            "weight_individus",
            "weight_familles",
            "weight_foyers",
            # "weight_menages", #Non car on ne les traite pas
        ]
        wprm_list = [w for w in all_wprms if w in sample_individus.keys()]
    else:
        wprm_list = specific_wprms

    wprm_list.append(id_entity)
    print("On regroupe la base selon ", wprm_list)

    for variable in sample_individus.columns.to_list():
        if variable not in tax_benefit_system.variables:
            continue
        column = tax_benefit_system.variables[variable]
        var_entity = column.entity.key
        # Supprimer les variables ménages
        if var_entity == "menage":
            print(f"Effacement de {variable}")
            sample_individus.drop([variable], axis=1, inplace=True)
        # Mettre à 0 les variables foyers, hors déclarant principal et hors poids
        elif (
            var_entity == "foyer_fiscal"
            and "quifoy" in sample_individus.columns.to_list()
            and variable != "weight_foyers"
        ):
            # sample_individus.iloc["quifoy"==0, variable] = 0
            print(f"Mise à 0 de {variable}")
            sample_individus.loc[sample_individus["quifoy"] == 0, variable] = 0

    # On regroupe les individus de sample_pop_individus en foyers fiscaux par leur idfoy (et leurs 'wprm' pour ne pas sommer les poids)
    if entity == "foyer_fiscal":
        wprm_list = [
            "weight_foyers",
            "foyer_fiscal_id",
        ]
    print(f"{wprm_list=}")
    sample_entity = sample_individus.groupby(wprm_list, as_index=False).sum()
    print("On a ", len(sample_entity), entity + " apres le groupby")

    if entity == "famille" or entity == "foyer_fiscal":
        print("On supprime les colonnes qui n'ont plus de sens au niveau foyer")
        cols = [
            "famille_role",
            "famille_position",
            "foyer_fiscal_role",
            "foyer_fiscal_position",
            "age",
            "categorie_salarie",
            "contrat_de_travail",
            "statut_marital",
        ]
        for col in cols:
            if col in sample_entity.columns:
                sample_entity.drop(col, axis=1, inplace=True)
        # On valide la colonne de poids
        sample_entity["wprm"] = sample_entity[wprm].copy()
        if entity == "foyer_fiscal":
            if "idfoy" in sample_entity.columns:
                if (
                    sample_entity["idfoy"].nunique()
                    != sample_entity["foyer_fiscal_id"].nunique()
                ):
                    print(
                        f"WARNING individus_to_entity : {sample_entity['idfoy'].nunique()} idfoy uniques mais {sample_entity['foyer_fiscal_id'].nunique()} foyer_fiscal_id unique !"
                    )
                else:
                    print(
                        f"DEBUG : individus_to_entity : Tout va bien, il y a {sample_entity['idfoy'].nunique()} idfoy uniques et {sample_entity['foyer_fiscal_id'].nunique()} foyer_fiscal_id unique !"
                    )
            sample_entity["idfoy"] = sample_entity["foyer_fiscal_id"].copy()
        # On vérifie que l'on a bien le même nombre de foyers fiscaux distincts avant et après
        tc.assertEqual(
            sample_individus[id_entity].nunique(), sample_entity[id_entity].nunique()
        )
        tc.assertEqual(len(sample_entity), sample_individus[id_entity].nunique())

    elif entity == "menage":
        print(
            "Attention, on ne peut pas remonter des individus aux ménages, car les poids n'auraient plus de sens économique"
        )
        sample_entity = pd.DataFrame()
    else:
        print(entity, " n'est pas une entité OpenFisca")
        sample_entity = pd.DataFrame()

    return sample_entity


"""
Utilisation de la librairie d'agrégats initialisée vers le path du projet
"""


def agg_lib():
    aggm_c = AggregateManager(aggregates_path=aggregates_path)
    return aggm_c


def get_copules(year, new_var, nb_copules, copules_var=None):
    data_structure = "copulas_" + nb_copules
    agg = agg_lib()
    agg.load_aggregate(
        "POTE",
        new_var,
        year=str(year),
        data_structure=data_structure,
        copules_var=copules_var,
    )
    return agg.aggregate.data[-1].values


def get_quantiles_casd(variable):
    agg = agg_lib()
    try:
        agg.load_aggregate(
            "POTE", variable, year=str(annee_pote), data_structure="distribution_100"
        )
        quantiles = agg.aggregate.data[-1].values
    except FileNotFoundError:
        print(
            "ATTENTION : Il n'y a pas d'extraction de POTE correspondant à la variable ",
            variable,
        )

    return quantiles


POTE_List = [
    "frf",
    "revenus_capitaux_prelevement_forfaitaire_unique_ir",
    "z5kc",
    "revenu_categoriel_foncier",
    "mnrvi2",
    "f4bb",
    "mnrvr3",
    "retraites",
    "f7cd",
    "z5nd",
    "rbg",
    "f7ap",
    "z1bp",
    "f7qs",
    "f7db",
    "impotnet",
    "z1gb",
    "z1ba",
    "z5ko",
    "z8ut",
    "z5rc",
    "z1cp",
    "f7qr",
    "rnirdu",
    "z1aa",
    "rimp",
    "z1hb",
    "z8sw",
    "rente_viagere_titre_onereux_net",
    "z5qc",
    "f2dh",
    "z5hc",
    "mnrvk",
    "revenus_capitaux_prelevement_liberatoire",
    "f1dw",
    "f8uy",
    "f4bc",
    "z3wh",
    "f3ua",
    "f6gu",
    "z1ap",
    "f2tr",
    "chomage_et_indemnites",
    "f1cw",
    "salaire_imposable",
    "z1cj",
    "f7uf",
    "rnirai",
    "z1az",
    "f2bh",
    "z5tb",
    "assiette_csg_plus_values",
    "z5xb",
    "z1ag",
    "z1ak",
    "z1bj",
    "f4be",
    "txmoy",
    "irpp_economique",
    "f2ch",
    "f4ba",
    "rfr",
    "z1ao",
    "assiette_csg_revenus_capital",
    "z1bs",
    "z1aj",
    "impot",
    "z1bk",
    "f3vg",
    "f4bd",
    "z8sx",
    "f3vz",
    "f7av",
    "f2dc",
    "revenus_capitaux_prelevement_bareme",
    "rnirp8",
    "z1as",
    "f8tk",
    "mnrvni",
    "rnimeh",
    "f7ga",
    "z3wg",
    "z1ha",
    "z5hq",
    "z5kp",
    "z1bz",
    "z1af",
    "z8sc",
    "mnimqg",
    "f6de",
    "retraite_imposable",
    "rnsgbd",
    "rnsgld",
    "cics",
    "mnipeg",
]

CCSS_List = [
    "csg_salaire_prive",
    "csg_chomage",
    "csg_salaire_public",
    "csg_retraite",
    "csg_indemnite_journaliere",
    "csg_salaire",
]


class DF_quantiles:
    """DataFrame qui contient la distribution des données en buckets"""

    def __init__(self, frontiers):
        self.columns = ["seuil_inf", "seuil_max", "middle", "nb_ff", "sum", "mean"]
        self.index = [str(i) for i in range(0, len(frontiers) - 1)]
        self.df = pd.DataFrame(columns=self.columns, index=self.index)
        self.bucket_list = {key: None for key in self.index}

    def update_quantile(self, i, bucket):
        self.df["seuil_inf"][i] = bucket.seuil_inf
        self.df["seuil_max"][i] = bucket.seuil_max
        self.df["middle"][i] = bucket.middle
        self.df["nb_ff"][i] = bucket.nb_ff
        self.df["sum"][i] = bucket.sum_
        self.df["mean"][i] = bucket.mean_
        # On sauvegarde l'ensemble des buckets
        self.bucket_list[str(i)] = bucket

        return self


class Bucket_Base:
    """Objet qui contient toutes les informations d'un bucket"""

    def __init__(self, i, frontiers, erfs_ff, var_name):
        self.nb = i
        self.seuil_inf = frontiers[self.nb]
        self.seuil_max = frontiers[self.nb + 1]
        self.middle = self.seuil_inf + (self.seuil_max - self.seuil_inf) / 2
        # Echantillon du bucket
        self.sample = erfs_ff.loc[
            (erfs_ff[var_name] >= self.seuil_inf) & (erfs_ff[var_name] < self.seuil_max)
        ].copy(deep=True)
        self.sample_pondere = (
            self.sample[var_name] * self.sample["weight_foyers"]
        ).copy(deep=True)
        # Infos
        self.nb_ff = round(self.sample["weight_foyers"].sum())
        self.sum_ = self.sample_pondere.sum()
        self.mean_ = self.sample_pondere.mean()


class Bucket_Pote:
    def __init__(self, i, frontiers, calib):
        self.nb = i
        self.seuil_inf = frontiers[self.nb]
        self.seuil_max = frontiers[self.nb + 1]
        self.middle = self.seuil_inf + (self.seuil_max - self.seuil_inf) / 2
        # Infos
        self.nb_ff = calib[self.nb]["bucket_count"]
        self.sum_ = calib[self.nb]["bucket_sum"]
        self.mean_ = calib[self.nb]["bucket_mean"]


""" Génère la distribution en buckets de la base ERFS (en foyers fiscaux!), calée sur POTE """


def distrib_to_quantiles(base_erfs, var_name, quantiles):
    # On vérifie qu'on est en base de foyers
    assert len(base_erfs) < 80_000

    # I - Nombre de foyers à zéro
    nb_zero_erfs, nb_zero_pote = nb_zero(base_erfs, var_name, quantiles)

    # II - Obtention des frontières de distribution
    quantiles, frontieres_var = get_minimal_frontiers(quantiles, base_erfs, var_name)
    print(
        "Dans POTE, on a ",
        quantiles[0]["bucket_count"],
        " foyers de ",
        var_name,
        " == 0",
    )

    # III - On passe à zéro tous les gens du 1er quantile
    sample_zero = base_erfs[base_erfs[var_name] == 0]
    print(
        "Dans l'ERFS, on a ",
        sample_zero["weight_foyers"].sum(),
        " foyers de ",
        var_name,
        " == 0",
    )
    # print(frontieres_var)

    # III - Création d'objets pour enregistrer les quantiles
    Distrib_BASE = DF_quantiles(frontieres_var)
    Distrib_POTE = DF_quantiles(frontieres_var)

    # IV - Création des quantiles
    for i in range(0, len(frontieres_var) - 1):
        # Distribution de l'ERFS
        bucket_erfs = Bucket_Base(i, frontieres_var, base_erfs, var_name)
        Distrib_BASE = Distrib_BASE.update_quantile(i, bucket_erfs)
        # Distribution de POTE
        bucket_pote = Bucket_Pote(i, frontieres_var, quantiles)
        Distrib_POTE = Distrib_POTE.update_quantile(i, bucket_pote)

    # IV - Tests
    df_erfs = Distrib_BASE.df
    df_pote = Distrib_POTE.df
    # Vérification des frontières
    tc.assertAlmostEqual(df_erfs["seuil_inf"].sum(), df_pote["seuil_inf"].sum())
    tc.assertAlmostEqual(df_erfs["seuil_max"].sum(), df_pote["seuil_max"].sum())
    # Vérification que les frontières de buckets sont bien distinctes
    tc.assertAlmostEqual(df_erfs["seuil_inf"].nunique(), len(df_erfs["seuil_inf"]))
    # Vérification du nombre total de foyers fiscaux
    tc.assertAlmostEqual(
        df_erfs["nb_ff"].sum() / base_erfs["weight_foyers"].sum(), 1, places=0
    )
    # Vérification de la somme totale
    tc.assertAlmostEqual(
        df_erfs["sum"].sum() / (base_erfs[var_name] * base_erfs["weight_foyers"]).sum(),
        1,
        places=3,
    )  # Pour avoir plus de marge à cause des arrondis de poids

    return Distrib_BASE, Distrib_POTE, quantiles


""" Calcule le nombre de gens à zéro dans POTE et dans l'ERFS avant calibration """


def nb_zero(base_erfs, var_name, quantiles):
    nb_zero_erfs = base_erfs[base_erfs[var_name] < quantiles[1]["lower_bound"]][
        "weight_foyers"
    ].sum()
    nb_zero_pote = quantiles[0]["bucket_count"]

    print(
        "Nombre de foyers de ",
        var_name,
        "à zéro, dans l'ERFS : ",
        nb_zero_erfs,
        "et dans POTE : ",
        nb_zero_pote,
        "soit un écart de : ",
        100 * (nb_zero_erfs - nb_zero_pote) / nb_zero_pote,
        "%",
    )

    return nb_zero_erfs, nb_zero_pote


def bucket_merge_with_above(calib_in, id_rm: int):
    """
    This method merge two bucket together.
    ::calib:: The buckets list
    ::id_rm:: The index of the bucket to merge with the bucket above
    """

    new_calib = copy.deepcopy(calib_in)
    # On supprime le bucket id_rm
    buck_removed = new_calib.pop(id_rm)

    # On remplace les valeurs de celui qui est devenu le suivant
    new_calib[id_rm]["lower_bound"] = buck_removed["lower_bound"]
    # new_calib[id_rm]["upper_bound"] ne change pas
    new_calib[id_rm]["bucket_count"] = (
        buck_removed["bucket_count"] + new_calib[id_rm]["bucket_count"]
    )

    new_calib[id_rm]["bucket_sum"] = (
        buck_removed["bucket_sum"] + new_calib[id_rm]["bucket_sum"]
    )

    # new_calib[id_rm]["count_above_upper_bound"] Ne change pas
    new_calib[id_rm]["bucket_mean"] = (
        new_calib[id_rm]["bucket_sum"] / new_calib[id_rm]["bucket_count"]
    )
    new_calib[id_rm]["bucket_stdev"] = 0

    # On verifie qu'on ne perd personne en cours de route
    tot_av = 0
    tot_ap = 0
    for i in range(len(calib_in)):
        tot_av += calib_in[i]["bucket_count"]
    for j in range(len(new_calib)):
        tot_av
        tot_ap += new_calib[j]["bucket_count"]

    tc.assertEqual(tot_av, tot_ap)

    return new_calib


""" Obtention des frontières minimales (non jointives) de la distribution issue de POTE """


def get_minimal_frontiers(quantiles, erfs, var_name):
    # 0 - On cherche la premiere frontiere au-dessus de zéro et on fusionne les buckets nuls
    for i in range(len(quantiles)):
        if quantiles[i]["upper_bound"] > 0:
            frontiere_supp_initiale = quantiles[i]["upper_bound"]
            break

    # 1 - On fusionne les buckets qui ont les mêmes frontières
    last = False
    while last is False:
        buckets = quantiles
        for idx, bucket in enumerate(buckets):
            # On s'arrête 2 buckets avant la fin
            if idx + 2 == len(buckets):
                last = True
                break
            # Si les buckets contiennent les mêmes frontières
            elif bucket["lower_bound"] == quantiles[idx + 1]["lower_bound"]:
                quantiles = bucket_merge_with_above(quantiles, idx)
                break

    # 2 - On initialise le 1er bucket de gens nuls (pour réparer le fichier quantiles)
    frontieres_var = [0, frontiere_supp_initiale]
    quantiles[0]["upper_bound"] = frontiere_supp_initiale
    quantiles[1]["lower_bound"] = frontiere_supp_initiale

    # 3 - On recupere toutes les frontieres
    for i in range(1, len(quantiles) - 1):
        frontieres_var.append(quantiles[i]["upper_bound"])

    # 4 - On augmente la hauteur du seuil max (cas où max(ERFS) > max(POTE))
    big_max = (
        max(erfs[var_name].max(), quantiles[-1]["upper_bound"]) + 1
    )  # Pour garder la valeur max dans le bucket
    frontieres_var.append(big_max)

    print(frontieres_var)
    tc.assertEqual(len(frontieres_var) - 1, len(quantiles))
    tc.assertEqual(len(frontieres_var), len(set(frontieres_var)))

    print(
        "On étudie la distribution en ",
        len(frontieres_var) - 1,
        " buckets, avec un min de ",
        frontieres_var[0],
        " et un max de ",
        frontieres_var[-1],
        "€ de",
        var_name,
    )

    return quantiles, frontieres_var


def generate_title(
    var_name, annee_erfs, annee_pote, title_suffix, log=False, cal=False
):
    """Génère un titre adapté pour les différents plots issus de la calibration"""
    # Avec ou sans calibration
    if cal is False:
        title = (
            "Comparaison des distributions de "
            + var_name
            + "\n ERFS "
            + annee_erfs
            + " (en rouge) et  POTE  "
            + annee_pote
            + " (en bleu) "
        )
    else:
        title = (
            "Calibration de la distribution de "
            + var_name
            + "\n ERFS "
            + annee_erfs
            + " (en rouge), calibration (en vert) et  POTE  "
            + annee_pote
            + " (en bleu) "
        )

    # Details
    title = title + title_suffix

    return title
