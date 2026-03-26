# gn_module_occhab/statistics.py

from geonature.core.gn_meta.models.datasets import TDatasets
from sqlalchemy import func, select

from geonature.utils.env import db
from gn_module_occhab.models import OccurenceHabitat, Station


def get_dataset_nb_observations(id_dataset):
    """
    Retourne le nombre d'occurrences d'habitats pour un JDD donné.
    Utilisé pour alimenter la colonne "Nombre de données" dans les listes JDD / CA.
    """
    return (
        select(func.count(OccurenceHabitat.id_habitat))
        .join(OccurenceHabitat.station)
        .where(Station.id_dataset == id_dataset)
    )


def get_dataset_statistics(id_dataset):
    """
    Retourne les statistiques affichées dans la fiche d'un JDD.
    """
    nb_stations = db.session.scalar(
        select(func.count(Station.id_station)).where(Station.id_dataset == id_dataset)
    )
    nb_habitats = db.session.scalar(
        select(func.count(OccurenceHabitat.id_habitat))
        .join(OccurenceHabitat.station)
        .where(Station.id_dataset == id_dataset)
    )
    return [
        {"label": "Nombre de stations", "value": nb_stations},
        {"label": "Nombre d'habitats (relevés)", "value": nb_habitats},
    ]


def get_acquisition_framework_statistics(id_acquisition_framework):
    """
    Retourne les statistiques affichées dans la fiche d'un CA.
    """
    nb_stations = db.session.scalar(
        select(func.count(Station.id_station))
        .join(Station.dataset)
        .where(TDatasets.id_acquisition_framework == id_acquisition_framework)
    )
    nb_habitats = db.session.scalar(
        select(func.count(OccurenceHabitat.id_habitat))
        .join(OccurenceHabitat.station)
        .join(Station.dataset)
        .where(TDatasets.id_acquisition_framework == id_acquisition_framework)
    )
    return [
        {"label": "Nombre de stations", "value": nb_stations},
        {"label": "Nombre d'habitats (relevés)", "value": nb_habitats},
    ]
