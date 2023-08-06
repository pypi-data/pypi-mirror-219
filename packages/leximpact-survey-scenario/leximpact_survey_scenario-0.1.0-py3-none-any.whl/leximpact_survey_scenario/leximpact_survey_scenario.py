import logging
import unittest
from typing import Any, Optional

import numpy as np
import pandas as pd

from openfisca_core.taxbenefitsystems import TaxBenefitSystem
from openfisca_france_data.erfs_fpr.scenario import ErfsFprSurveyScenario

from openfisca_survey_manager.survey_collections import SurveyCollection
from openfisca_survey_manager import default_config_files_directory

from leximpact_survey_scenario.scenario_tools.inflation_calibration_values import (
    inflation_coefs,
)
from leximpact_survey_scenario.leximpact_tax_and_benefit_system import leximpact_tbs


tc = unittest.TestCase()
pd.set_option("display.max_columns", None)
log = logging.getLogger(__name__)


# Liste des variables qui sont injectées par Monte-Carlo et ajoutée en input variable du survey_scenario
## sous liste en fonction de la variable primaire par laquelle on impute
variables_by_revenu_individuels_100 = [
    "revenu_categoriel_foncier",
    "rente_viagere_titre_onereux_net",
    "revenus_capitaux_prelevement_bareme",
    "revenus_capitaux_prelevement_forfaitaire_unique_ir",
    "revenus_capitaux_prelevement_liberatoire",
]
variables_by_revenus_individuels_20 = [
    "assiette_csg_plus_values",
]

variables_by_revkire_par_part = [
    "reductions",
    "credits_impot",
]
future_monte_carlo_variables = (
    variables_by_revenu_individuels_100
    + variables_by_revenus_individuels_20
    + variables_by_revkire_par_part
)


class LeximpactErfsSurveyScenario(ErfsFprSurveyScenario):
    """Survey scenario spécialisé pour l'ERFS-FPR utilisée par Leximpact."""

    def __init__(
        self,
        config_dirpath: str = default_config_files_directory,
        annee_erfs: int = 2019,
        final_year: int = 2023,
        rebuild_input_data: bool = False,
        # rebuild_input_data est un paramètre hérité de survey_manager.
        init_from_data: bool = True,
        baseline_tax_benefit_system: Optional[TaxBenefitSystem] = None,
        tax_benefit_system_plf: Optional[TaxBenefitSystem] = None,
        data: Any = None,
        collection: str = "leximpact",
        survey_name: str = None,
    ):
        """Crée un `LeximpactErfsSurveyScenario`.

        :param annee_erfs:                  L'année des données de l'enquête.
        :param rebuild_input_data:          Si l'on doit formatter les données (raw) ou pas.
        :param init_from_data:              Si on veut suspendre l'initialisation automatique par les données
        :param tax_benefit_system:          Le `TaxBenefitSystem` déjà réformé.
        :param baseline_tax_benefit_system: Le `TaxBenefitSystem` au droit courant.
        :param data:                        Les données de l'enquête.
        :param reform:                      Reform OpenFisca.
        :param collection:                  Collection à lire.
        :param survey_name:                 Nom de l'enquête.
        """

        super().__init__(annee_erfs)
        self.collection = collection
        self.annee_erfs = int(annee_erfs)
        self.final_year = int(final_year)
        self.config_dirpath = config_dirpath
        self.config_files_directory = config_dirpath

        self._set_used_as_input_variables()
        # non_neutralizable_variables hérite d'une liste de variables d'ErfsFprSurveyScenario
        self.non_neutralizable_variables += self.used_as_input_variables

        # ## Initialisation des Baseline/ Non baseline TaxBenefitSystems
        if baseline_tax_benefit_system is None:
            baseline_tax_benefit_system = leximpact_tbs

        if tax_benefit_system_plf is None:
            tax_benefit_system_plf = leximpact_tbs

        self.set_tax_benefit_systems(
            tax_benefit_system=tax_benefit_system_plf,
            baseline_tax_benefit_system=baseline_tax_benefit_system,
        )

        if survey_name is None:
            survey_name = f"{collection}_{annee_erfs}"

        # ## Création de la base de données sur les périodes voulues
        # S'il n'y a pas de données, on sait où les trouver.
        if data is None:
            # List of years available
            years_available = []
            print(
                f"LeximpactErfsSurveyScenario : Using {config_dirpath} as config_dirpath"
            )
            survey_collection = SurveyCollection.load(
                collection=collection, config_files_directory=config_dirpath
            )
            survey = survey_collection.get_survey(survey_name)
            for table_name, _ in survey.tables.items():
                if table_name[-4:].isnumeric():
                    years_available.append(int(table_name[-4:]))
            years_available = list(set(years_available))

            # List of years to create
            years = [year for year in range(self.annee_erfs, self.final_year + 1)]

            print(f"{years_available=} vs {years=}")

            data = {"input_data_table_by_entity_by_period": {}, "survey": survey_name}
            current_year = None

            for year in years:
                if data["input_data_table_by_entity_by_period"].get(year) is None:
                    data["input_data_table_by_entity_by_period"][year] = {}
                if year in years_available:
                    data_year = year
                else:
                    data_year = self.annee_erfs
                    print(f"WARNING: no data for {year}, will took {data_year}")
                for table_name, _ in survey.tables.items():
                    current_year = table_name[-4:]
                    if current_year.isnumeric():
                        current_year = int(current_year)
                        entity = table_name[:-5]
                        if current_year == data_year:
                            # print(f"Using {table_name} for {entity} for {year}")
                            data["input_data_table_by_entity_by_period"][year][
                                entity
                            ] = table_name
                    else:
                        print(
                            f"WARNING {table_name} will be ignored because it has no year !!!"
                        )

        print("Données du scénario : \n", data)
        self.input_data = data
        self.rebuild_input_data = rebuild_input_data

        if init_from_data:
            self.input_from_data()

    def custom_initialize(self, simulation):
        inflator_by_variable = {}
        for inflation_year in [
            self.final_year - 2,
            self.final_year - 1,
            self.final_year,
        ]:
            inflator_by_variable.update(
                {
                    inflation_year: inflation_coefs(
                        self.used_as_input_variables,
                        str(self.annee_erfs),
                        str(inflation_year),
                    )
                }
            )
        for var in self.used_as_input_variables:
            if var in simulation.tax_benefit_system.variables:
                array_var = self.calculate_variable(
                    var, period=self.annee_erfs, use_baseline=True
                )
                for inflation_year in [
                    self.final_year - 2,
                    self.final_year - 1,
                    self.final_year,
                ]:
                    if var in inflator_by_variable[inflation_year].keys():
                        inflated_array = (
                            array_var.copy() * inflator_by_variable[inflation_year][var]
                        )
                    elif (var in ["date_naissance"]) & (
                        self.final_year > self.annee_erfs
                    ):
                        inflated_array = [
                            np.datetime64(
                                (
                                    np.datetime64(date, "Y")
                                    + (self.final_year - self.annee_erfs)
                                ),
                                "D",
                            )
                            for date in array_var
                        ]
                    else:
                        inflated_array = array_var.copy()
                    try:
                        simulation.set_input(var, inflation_year, inflated_array)
                    except ValueError:
                        simulation.delete_arrays(var, inflation_year)
                        simulation.set_input(var, inflation_year, inflated_array)

    # Initialisation custom
    def input_from_data(self, var_list=None):
        # On défini nos variables d'interet sont définies dans self.used_as_input_variables

        # Initialisation du scenario avec les données
        self.init_from_data(
            data=self.input_data,
            rebuild_input_data=self.rebuild_input_data,
            config_files_directory=self.config_dirpath,
        )

    def custom_input_data_frame(self, input_data_frame, **kwargs):
        pass

    # On redéfini les variables
    def _set_used_as_input_variables(self):
        # ne garde pas toutes les variables par défaut de ErfsFprSurveyScenario :
        wprms = [
            "weight_familles",
            "weight_foyers",
            "weight_individus",
            "weight_menages",
            "wprm",
        ]
        # on retire les colonnes à zéro de l'ERFS-FPR
        inherited_but_ignored_variables = [
            "taxe_habitation",
        ]
        self.used_as_input_variables = list(
            set(self.used_as_input_variables) - set(inherited_but_ignored_variables)
        )

        # variables leximpact :
        leximpact_variables = None

        variables_to_keep_or_to_calculate = ["age"]

        ids = [
            # TODO Choisir une clef d'identification unique entre openfisca-survey-manager et openfisca-france-data ? :'-D
            # sachant que les valeurs existent dans openfisca-core.populations.group_population.GroupPopulation.members_entity_id
            # openfisca-france-data :
            "idfoy",
            "idfam",
            "idmen",
            "idmen_original",
        ]
        roles = [
            # TODO comme ci dessus pour les variables d'indentifiant
            "noindiv",  # source : ERFS-FPR
            "quifoy",
            "quifam",
            "quimen",
        ]

        specific_variables = ["taux_capacite_travail", "taux_incapacite"]

        leximpact_variables = (
            wprms
            + variables_to_keep_or_to_calculate
            + ids
            + roles
            + future_monte_carlo_variables
            + specific_variables
        )
        self.used_as_input_variables = list(
            set(self.used_as_input_variables + leximpact_variables)
        )
