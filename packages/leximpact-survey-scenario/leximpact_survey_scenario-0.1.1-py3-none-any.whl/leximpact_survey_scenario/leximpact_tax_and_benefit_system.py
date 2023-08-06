import logging
import numpy as np
from openfisca_core import reforms

from openfisca_france_data import france_data_tax_benefit_system
from openfisca_france_data.model.base import (
    ETERNITY,
    YEAR,
    Individu,
    Menage,
    FoyerFiscal,
    Variable,
)

log = logging.getLogger(__name__)


# Neutralisation de variables composantes du traitement indicidaire car elles ne sont pas identifiables dans les données ERFS-FPR
neutralized_variables = [
    "indemnite_residence",
    "supplement_familial_traitement",
    "indemnite_compensatrice_csg",
]


class leximpact_tbs_extension(reforms.Reform):
    def apply(self):
        class quimen(Variable):
            is_period_size_independent = True
            value_type = int
            entity = Individu
            label = "Rôle dans le ménage"
            definition_period = ETERNITY

        class quifam(Variable):
            is_period_size_independent = True
            value_type = int
            entity = Individu
            label = "Rôle dans la famille"
            definition_period = ETERNITY

        class quifoy(Variable):
            is_period_size_independent = True
            value_type = int
            entity = Individu
            label = "Rôle dans le foyer fiscal"
            definition_period = ETERNITY

        class idmen(Variable):
            is_period_size_independent = True
            value_type = int
            entity = Individu
            label = "Identifiant ménage dans openfisca-france-data"
            definition_period = ETERNITY

        class idmen_original(Variable):
            is_period_size_independent = True
            value_type = int
            entity = Menage
            label = "Identifiant ménage dans erfs-fpr"
            definition_period = ETERNITY

        class idfam(Variable):
            is_period_size_independent = True
            value_type = int
            entity = Individu
            label = "Identifiant famille dans openfisca-france-data"
            definition_period = ETERNITY

        class idfoy(Variable):
            is_period_size_independent = True
            value_type = int
            entity = Individu
            label = "Identifiant foyer fiscal dans openfisca-france-data"
            definition_period = ETERNITY

        class menage_id(Variable):
            is_period_size_independent = True
            value_type = int
            entity = Individu
            label = "Identifiant ménage"  # dans openfisca-survey-manager ?
            definition_period = ETERNITY

        class famille_id(Variable):
            is_period_size_independent = True
            value_type = int
            entity = Individu
            label = "Identifiant famille"  # dans openfisca-survey-manager ?
            definition_period = ETERNITY

        class foyer_fiscal_id(Variable):
            is_period_size_independent = True
            value_type = int
            entity = Individu
            label = "Identifiant foyer fiscal"  # dans openfisca-survey-manager ?
            definition_period = ETERNITY

        class noindiv(Variable):
            is_period_size_independent = True
            value_type = str  # champ texte de 10 caractères
            entity = Individu
            label = "Identifiant des individus dans l'enquête ERFS-FPR de l'INSEE"
            definition_period = ETERNITY

        class rpns_imposables(Variable):
            value_type = float
            entity = Individu
            label = "Revenus imposables des professions non salariées individuels"
            definition_period = YEAR

            def formula(individu, period):
                rag = individu("rag", period)
                ric = individu("ric", period)
                rnc = individu("rnc", period)

                return rag + ric + rnc

        class rfr_plus_values_hors_rni(Variable):
            value_type = float
            entity = FoyerFiscal
            label = "Plus-values hors RNI entrant dans le calcul du revenu fiscal de référence (PV au barème, PV éxonérées ..)"
            definition_period = YEAR

            def formula_2018_01_01(foyer_fiscal, period):
                return foyer_fiscal("assiette_csg_plus_values", period)

        class plus_values_prelevement_forfaitaire_unique_ir(Variable):
            value_type = float
            entity = FoyerFiscal
            label = "Plus-values soumises au prélèvement forfaitaire unique (partie impôt sur le revenu)"
            reference = (
                "https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000036377422/"
            )
            definition_period = YEAR

            def formula_2018_01_01(foyer_fiscal, period):
                return foyer_fiscal("assiette_csg_plus_values", period)

        class iaidrdi(Variable):
            value_type = float
            entity = FoyerFiscal
            label = "Impôt après imputation des réductions d'impôt"
            definition_period = YEAR

            def formula(foyer_fiscal, period, parameters):
                """
                Impôt après imputation des réductions d'impôt
                """
                ip_net = foyer_fiscal("ip_net", period)
                reductions = foyer_fiscal("reductions", period)

                return np.maximum(0, ip_net - reductions)

        variables = [
            quimen,
            quifam,
            quifoy,
            idmen,
            idmen_original,
            idfam,
            idfoy,
            menage_id,
            famille_id,
            foyer_fiscal_id,
            noindiv,
        ]

        # Adaptation de variables du fait des variables de revenus du capital imputées
        updated_variables = [
            iaidrdi,
            plus_values_prelevement_forfaitaire_unique_ir,
            rfr_plus_values_hors_rni,
            rpns_imposables,
        ]

        for variable in variables:
            if variable == Variable:
                continue
            try:
                self.add_variable(variable)
            except AttributeError:
                self.update_variable(variable)
        for neutralized_variable in neutralized_variables:
            log.info(f"Neutralizing {neutralized_variable}")
            if self.get_variable(neutralized_variable):
                self.neutralize_variable(neutralized_variable)
        for updated_variable in updated_variables:
            self.update_variable(updated_variable)


leximpact_tbs = leximpact_tbs_extension(france_data_tax_benefit_system)
