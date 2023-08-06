# copier coller depuis taxipp, à checker et sourcer
## Sources : calculée à partir des données de population et de PIB nominal de l'INSEE
taux_croissance_pib_nominal_par_tete = {
    "2023": 5.3,  # temp copy
    "2022": 5.3,  # prévision fondée sur la prévision de croissance du PIB nominal du RESF 2022
    "2021": 6.3,  # prévision fondée sur la prévision de croissance du PIB nominal du RESF 2022
    "2020": -5.3,
    "2019": 2.9,
    "2018": 2.3,
    "2017": 2.6,
    "2016": 1.0,
    "2015": 1.7,
    "2014": 0.7,
    "2013": 0.9,
    "2012": 0.9,
    "2011": 2.6,
    "2010": 2.6,
}

# copier coller depuis taxipp, à checker et sourcer
# Source: INSEE (observé) et RESF (prévision)
# evolution en moyenne annuelle du SMPT nominal pour le secteur marchand non agricole
smpt_growth_by_year = {
    "2023": 3.8,  # temp à changer dans le RESF
    "2022": 5.7,  # note de conjoncture mars 2023
    "2021": 5.6,  # note de conjoncture mars 2023
    "2020": -4.4,  # note de conjoncture mars 2023
    "2019": 2.3,  # note de conjoncture mars 2023
    "2018": 1.7,  # note de conjoncture décembre 2019
    "2017": 1.7,
    "2016": 1.2,
    "2015": 1.6,
    "2014": 0.6,
    "2013": 1.3,
    "2012": 1.8,
    "2011": 2.6,
    "2010": 2.4,
}

total_annuel_salaires = {
    "2003": 505_413_219_971,
    "2004": 521_074_208_677,
    "2005": 535_224_289_868,
    "2006": 555_718_533_592,
    "2007": 576_696_329_635,
    "2008": 598_350_414_779,
    "2009": 603_748_075_702,
    "2010": 621_113_771_549,
    "2011": 638_494_009_748,
    "2012": 651_235_711_284,
    "2013": 664_720_821_400,
    "2014": 674_188_954_200,
    "2015": 683_665_874_000,
    "2016": 695_665_787_000,
    "2017": 713_523_524_000,
    "2018": 738_077_177_000,
    "2019": 743_500_200_000,  # Sur le nouveau site
    "2020": 758_741_700_000,  # Sur le nouveau site
    "2021": 758_741_700_000 * 1.023,
    "2022": 758_741_700_000 * 1.023 * 1.031,
    "2023": 758_741_700_000 * 1.023 * 1.031 * 1.033,
}

# Création de la liste des taux d'inflation (en %)
# Données issues du PLF - 'Chiffres clés' (=inflation hors tabac = prix à la consommation)
inflation_idc = {
    "2017": 1.0,
    "2018": 1.6,
    "2019": 0.9,
    "2020": 0.2,
    "2021": 1.5,
    "2022": 5.2,
    "2023": 4.3,  # à changer
}

# Pour info, pas utilisé dans ce code:
# Création de la liste des taux d'inflation (en %)
# Source: https://www.insee.fr/fr/statistiques/2122401#tableau-figure1
inflation_insee = {
    "2009": 0.1,
    "2010": 1.5,
    "2011": 2.0,
    "2012": 2.0,
    "2013": 0.9,
    "2014": 0.5,
    "2015": 0.0,
    "2016": 0.2,
    "2017": 1.0,
    "2018": 1.8,
    "2019": 1.1,
    "2020": 0.5,
    "2021": 1.6,
    "2022": 5.9,  # https://www.insee.fr/fr/statistiques?debut=0&theme=30&conjoncture=43
    "2023": 5.9,  # temp copy
}

# Création de la liste des taux d'inflation (en %)
# Source : https://www.ipp.eu/baremes-ipp/regimes-de-retraites/0/0/revalorisation_pension/
# On ne traite que le cas du régime général privé
revalorisation_retraite = {
    "2015": 0.1,  # legislation cnav
    "2016": 0.0,  # legislation cnav
    "2017": 0.8,  # legislation cnav
    "2018": 0.0,  # legislation cnav
    "2019": 0.3,  # legislation cnav
    "2020": 0.3,  # legislation cnav
    "2021": 0.4,  # legislation cnav
    "2022": 1.1 + 4,  # legislation cnav
    "2023": 0.8,  # legislation cnav
}

# Création de la liste des taux d'inflation (en %)
# Source : https://www.ipp.eu/baremes-ipp/chomage/allocations_assurance_chomage/sr_alloc/
reval_chomage = {
    "2017": 0.65,
    "2018": 0.7,
    "2019": 0.7,
    "2020": 0.4,
    "2021": 0.6,  # https://www.service-public.fr/particuliers/actualites/A15021
    "2022": 2.9,  # https://www.service-public.fr/particuliers/actualites/A15787
    "2023": 1.9,  # https://www.service-public.fr/particuliers/actualites/A16503
}

nb_foyers_par_annee = {
    "2011": 36_389_256,
    "2012": 36_720_036,
    "2013": 37_119_219,
    "2014": 37_429_459,
    "2015": 37_683_595,
    "2016": 37_889_181,
    "2017": 38_332_977,
    "2018": 38_549_926,
    "2019": 39_331_689,  # 39_167_000 selon un autre document sur le meme site...
    "2020": 39_887_586,  # Source : national.xls # 39_714_000 selon un autre document sur le meme site...
}

population_france_metropolitaine = {
    "2023": 65_834_837,
    "2022": 65_646_837,
    "2021": 65_450_219,
    "2020": 65_269_154,
    "2019": 65_096_768,
    "2018": 64_844_037,
    "2017": 64_844_037,  # temp copy
}

population_france_totale = {
    "2023": 68_042_591,
    "2022": 67_842_591,
    "2021": 67_635_124,
    "2020": 67_441_850,
    "2019": 67_257_982,
    "2018": 66_992_159,
    "2017": 66_992_159,  # temp copy
}

# Sources : INSEE, Variation annuelle de l'Indice de Référence des Loyers (IRL)
# La variation annuelle T2 (sur laquelle sont indexés les paramètres du barèmes des APL depuis 2014)
variation_annuelle_irl = {
    "2023": 3.5,  # temp copy
    "2022": 3.5,  # Source INSEE le 4/07/2023
    "2021": 0.42,  # Source INSEE le 27/10/2021
    "2020": 0.66,
    "2019": 1.53,
    "2018": 1.25,
    "2017": 0.75,
    "2016": 0.00,
    "2015": 0.08,
    "2014": 0.57,
    "2013": 1.20,
    "2012": 2.20,
    "2011": 1.73,
    "2010": 0.57,
}
