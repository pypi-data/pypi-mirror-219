from openfisca_france_data.erfs_fpr.comparison import ErfsFprtoInputComparator
from leximpact_survey_scenario.leximpact_survey_scenario import (
    LeximpactErfsSurveyScenario,
)


class LeximpactComparator(ErfsFprtoInputComparator):
    collection = None
    survey_name = None
    target_variables = None
    default_target_variables = [
        "chomage_imposable",
        "loyer",
        "retraite_imposable",
        "salaire_imposable",
        "niveau_de_vie",
        "ppa_menage",
        "unites_consommation",
        "revenu_disponible",
        "aspa_menage",
        "aah_menage",
        "rsa_menage",
        "aides_logement_menage",
        "paje_menage",
        "prestations_familiales_autres_menage",
    ]

    def __init__(
        self, annee_comparaison, collection=None, survey_name=None, target_variable=None
    ):
        self.annee_comparaison = annee_comparaison
        self.collection = collection
        self.survey_name = survey_name
        self.target_variable = target_variable

    def get_survey_scenario(self, data=None):
        collection = self.collection
        survey_name = self.survey_name
        annee_comparaison = self.annee_comparaison

        survey_scenario = LeximpactErfsSurveyScenario(
            final_year=annee_comparaison,
            rebuild_input_data=False,
            rebuild_openfisca_erfs_fpr=False,
            duplicates_rows=True,
            rebuild_imputation=False,
            collection=collection,
            survey_name=survey_name,
        )

        return survey_scenario
