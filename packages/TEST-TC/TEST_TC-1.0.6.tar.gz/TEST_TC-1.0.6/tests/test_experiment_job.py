import os
import subprocess

import mlflow
import pytest

from tc_uc4.datahandler.datahandler import DataHandler
from tc_uc4.utility.constants import predict_dataframe_columns
from tc_uc4.utility.resources import get_configuration

models = ["Abruzzo", "Abruzzo_F", "Abruzzo_M", "Basilicata", "Basilicata_F", "Basilicata_M", "Bolzano",
          "Bolzano_F", "Bolzano_M", "Calabria", "Calabria_F", "Calabria_M", "Campania", "Campania_F",
          "Campania_M", "Emilia-Romagna", "Emilia-Romagna_F", "Emilia-Romagna_M", "Friuli-Venezia-Giulia",
          "Friuli-Venezia-Giulia_F", "Friuli-Venezia-Giulia_M", "Italia", "Lazio", "Lazio_F", "Lazio_M",
          "Liguria", "Liguria_F", "Liguria_M", "Lombardia", "Lombardia_F", "Lombardia_M", "Molise",
          "Molise_F", "Molise_M", "Piemonte", "Piemonte_F", "Piemonte_M", "Puglia", "Puglia_F",
          "Puglia_M", "Sardegna", "Sardegna_F", "Sardegna_M", "Sicilia", "Sicilia_F", "Sicilia_M",
          "Toscana", "Toscana_F", "Toscana_M", "Trento", "Trento_F", "Trento_M", "Umbria", "Umbria_F",
          "Umbria_M", "Valle D Aosta", "Valle D Aosta_F", "Valle D Aosta_M", "Veneto", "Veneto_F", "Veneto_M"
          ]

expected_metrics = {
    "MAE": 1.557,
    "MAPE": 0.489,
    "MSE": 6.01,
    "Percentage Coverage": 80.66,
    "R2": -0.134,
    "RMSE": 2.098,
}


def test_job_experiment():
    experiment_name = "unittest"
    python_cmd = 'python'
    
    project_path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
    config_path = os.path.join(project_path, "tests/config")
    path_configs = experiment_name + "_path.toml"
    model_configs = experiment_name + "_prophet.toml"

    print(os.path.join(project_path, "experiments", "train_and_tune_prophet.py"))

    process = subprocess.Popen(f'{python_cmd} {os.path.join(project_path, "experiments", "train_and_tune_prophet.py")} -E {experiment_name}', shell=True)

    process.wait()

    experiment_folder = get_configuration("data_paths", config_path, path_configs)["experiment_folder"]
    experiment_folder = os.path.join(project_path, experiment_folder)
    model_name = get_configuration("model", config_path, model_configs)["model_name"]

    mlflow.set_tracking_uri(experiment_folder)
    experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id

    # Find best run
    run = mlflow.search_runs(experiment_ids=experiment_id).loc[0]

    # Test if trained models are present in artifacts
    model_uri = f"runs:/{run['run_id']}/{model_name}.pkl"
    model = mlflow.sklearn.load_model(model_uri)

    # Test model in models
    assert len(model.models_dict) == len(models)
    for id_pred, m in model.models_dict.items():
        assert id_pred.replace("/", "_") in models

        # Test parameters in specified range
        if m is not None:
            assert m.model.weekly_seasonality in [True, False]
            assert m.model.yearly_seasonality in [True, False]

    # Test model metrics
    for metric, expected_value in expected_metrics.items():
        assert pytest.approx(run[f"metrics.{metric}"], 0.1) == expected_value

    ################################################################
    # Test Job
    ################################################################

    predict_save_folder = get_configuration("data_paths", config_path, path_configs)["predict_save_folder"]
    process = subprocess.Popen(f'{python_cmd} {os.path.join(project_path, "jobs", "predict_prophet.py")} -E {experiment_name}',shell=True)
    process.wait()

    DH = DataHandler(predict_save_folder)
    predictions = DH.read("prophet_predictions.parquet", folder="")

    # Test predictions df shape
    assert len(predictions.columns) == len(predict_dataframe_columns)
    assert len(predictions) == 6100
    for col in predictions.columns:
        assert col in predict_dataframe_columns

    for row in predictions.iterrows():
        if row[1] is None:
            assert row[2] == 0.0
            assert row[3] == 0.0
            assert row[4] == 0.0
            assert row[5] == 0.0

    # Delete created folders
    process = subprocess.Popen(
        f'rm -rf {os.path.join(project_path, "tests/experiments")}',
        shell=True,
    )
    process = subprocess.Popen(
        f'rm -rf {os.path.join(project_path, "tests/data/output")}',
        shell=True,
    )
