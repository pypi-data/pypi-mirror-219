#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path
import re
import sys
from typing import Any, cast, Dict, List, Optional, Union

import mlflow
from mlflow import pyfunc
from mlflow.models import Model, ModelInputExample
from mlflow.models.model import MLMODEL_FILE_NAME
from mlflow.models.signature import ModelSignature
from mlflow.tracking.artifact_utils import _download_artifact_from_uri
from mlflow.utils.autologging_utils import autologging_integration
from mlflow.utils.environment import (
    _CONDA_ENV_FILE_NAME,
    _CONSTRAINTS_FILE_NAME,
    _mlflow_conda_env,
    _process_conda_env,
    _process_pip_requirements,
    _PYTHON_ENV_FILE_NAME,
    _PythonEnv,
    _REQUIREMENTS_FILE_NAME,
    _validate_env_arguments,
)
from mlflow.utils.file_utils import write_to
from mlflow.utils.model_utils import (
    _add_code_from_conf_to_system_path,
    _get_flavor_configuration,
    _validate_and_prepare_target_save_path,
)
from mlflow.utils.requirements_utils import _get_pinned_requirement
import pandas as pd
import yaml

from datarobotx._version import __version__
from datarobotx.client import deployments as dep_client
from datarobotx.client import projects as proj_client
from datarobotx.common import config, utils
from datarobotx.common.client import retry_if_too_many_attempts
from datarobotx.models.autoanomaly import AutoAnomalyModel
from datarobotx.models.autocluster import AutoClusteringModel
from datarobotx.models.automl import AutoMLModel
from datarobotx.models.autopilot import AutopilotModel
from datarobotx.models.autots import AutoTSModel
from datarobotx.models.deployment import Deployment, ModelKind
from datarobotx.models.model import Model as drxModel
from datarobotx.models.model import ModelOperator
from datarobotx.viz.leaderboard import LeaderboardFormatter
from datarobotx.viz.modelcard import ModelCardFormatter

VERSION = __version__

logger = logging.getLogger("drx")

FLAVOR_NAME = "datarobot"
DRMODELS_DATA_SUBPATH = "model.datarobot"


def get_default_pip_requirements() -> List[str]:
    """
    :return: A list of default pip requirements for MLflow Models produced by this flavor.
             Calls to :func:`save_model()` and :func:`log_model()` produce a pip environment
             that, at minimum, contains these requirements.
    """
    return [_get_pinned_requirement("datarobotx")]


def get_default_conda_env() -> (Any | None):
    """
    :return: The default Conda environment for MLflow Models produced by calls to
             :func:`save_model()` and :func:`log_model()`.
    """
    return _mlflow_conda_env(additional_pip_deps=get_default_pip_requirements())


def save_model(
    drx_model: Optional[ModelOperator | Deployment],
    path: Union[str, Path],
    conda_env: Optional[Any] = None,
    mlflow_model: Optional[mlflow.models.Model] = None,
    signature: ModelSignature = None,
    input_example: ModelInputExample = None,
    pip_requirements: Optional[List[str]] = None,
    extra_pip_requirements: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Save a drx model using MlFlow

    Implements the MLflow save_model() interface

    Parameters
    ----------
    model : ModelOperator or Deployment
        The drx model to be saved, one of model or mlflow_model must be supplied
    path : Union[str, Path]
        The local path where model will be saved
    conda_env :
        Conda environment to be saved
    mlflow_model :
        The MLFlow Model this flavor is being added to
    signature : ModelSignature
        Describes the model inputs and outputs using an MlFlow signature
    input_example :
        Input example provides one or several instances of valid model input. The example can be used as a hint of what
        data to feed the model. The given example will be converted to a Pandas DataFrame and then serialized to json
        using the Pandas split-oriented format. Bytes are base64-encoded.
    pip_requirements :
        Either an iterable of pip requirement strings (e.g. ["statsmodels", "-r requirements.txt", "-c constraints.txt"]
    extra_pip_requirements :
        Either an iterable of pip requirement strings (e.g. ["pandas", "-r requirements.txt", "-c constraints.txt"]) or
        the string path to a pip requirements file on the local filesystem (e.g. "requirements.txt"). If provided, this
        describes additional pip requirements that are appended to a default set of pip requirements generated
        automatically based on the user’s current software environment. Both requirements and constraints are
        automatically parsed and written to requirements.txt and constraints.txt files, respectively, and stored as
        part of the model. Requirements are also written to the pip section of the model’s conda environment
        (conda.yaml) file.
    metadata :
        custom metadata dictionary passed and stored in the MlModel files
    """
    assert drx_model is not None or mlflow_model is not None
    _validate_env_arguments(conda_env, pip_requirements, extra_pip_requirements)
    if path is not None:
        path = os.path.abspath(path)
    _validate_and_prepare_target_save_path(path)

    if drx_model:
        mlflow_model = _make_drx_model(drx_model, mlflow_model, signature, input_example, metadata)
    mlflow_model.save(os.path.join(path, MLMODEL_FILE_NAME))  # type: ignore[union-attr]
    # everything from here
    # down is a copy from
    # https://github.com/mlflow/mlflow/blob/8f192470d6425cce8fbe3287e452c795e3cbfa2f/mlflow/statsmodels.py#L193
    if conda_env is None:
        if pip_requirements is None:
            default_reqs = get_default_pip_requirements()
            # To ensure `_load_pyfunc` can successfully load the model during the dependency
            # inference, `mlflow_model.save` must be called beforehand to save an MLmodel file.
        else:
            default_reqs = None
        conda_env, pip_requirements, pip_constraints = _process_pip_requirements(
            default_reqs,
            pip_requirements,
            extra_pip_requirements,
        )
    else:
        conda_env, pip_requirements, pip_constraints = _process_conda_env(conda_env)

    with open(os.path.join(path, _CONDA_ENV_FILE_NAME), "w", encoding="UTF-8") as f:
        yaml.safe_dump(conda_env, stream=f, default_flow_style=False)

    # Save `constraints.txt` if necessary
    if pip_constraints:
        write_to(os.path.join(path, _CONSTRAINTS_FILE_NAME), "\n".join(pip_constraints))

    # Save `requirements.txt`
    if pip_requirements:
        write_to(os.path.join(path, _REQUIREMENTS_FILE_NAME), "\n".join(pip_requirements))

    _PythonEnv.current().to_yaml(os.path.join(path, _PYTHON_ENV_FILE_NAME))


def log_runs_from_model(
    drx_model: ModelOperator,
    log_models: bool = False,
    number_of_models_to_log: int = 10,
    experiment_id: Optional[str | int] = None,
) -> None:
    """Log challengers from a previously fit drx model to MLflow

    Use this function to log an experiment with MLflow for projects that
    have previously completed.

    Parameters
    ----------
    drx_model : ModelOperator
        drx model containing the challengers / leaderboard to be logged
    log_models : bool
        Whether to save the model as an artifact into the MLflow run result
    number_of_models_to_log : int
        The maximum number of models from the leaderboard that will be logged as runs.

    """
    handler = MLFlowFitHandler(
        log_models=log_models,
        number_of_models_to_log=number_of_models_to_log,
        remove_after_one=True,
        experiment_id=experiment_id,
    )
    logger.debug("Logging to Handler %s", handler.experiment_id)
    logger.addHandler(handler)
    logger.info("Logging the model to MlFlow", extra={"is_header": True})
    logger.debug("Logging to Experiment %s", experiment_id)
    extra: Dict[str, Union[str, bool, Optional[str], Optional[List[str]]]] = {}
    extra["leaderboard"] = drx_model._leaderboard
    assert drx_model._best_model is not None
    extra["project_id"] = drx_model._best_model._project_id
    extra["project_ready_for_logging"] = True
    logger.info("Logging Model for MLFlow", extra=extra)


def log_model(
    drx_model: Union[drxModel, ModelOperator],
    artifact_path: Optional[str] = None,
    conda_env: Optional[Any] = None,
    registered_model_name: Optional[str] = None,
    signature: Optional[ModelSignature] = None,
    input_example: Optional[ModelInputExample] = None,
    await_registration_for: int = 600,
    pip_requirements: Optional[str] = None,
    extra_pip_requirements: Optional[str] = None,
    metadata: Optional[str] = None,
) -> mlflow.models.model.ModelInfo:
    return Model.log(
        artifact_path=artifact_path,
        flavor=sys.modules[__name__],
        drx_model=drx_model,
        conda_env=conda_env,
        registered_model_name=registered_model_name,
        signature=signature,
        input_example=input_example,
        await_registration_for=await_registration_for,
        pip_requirements=pip_requirements,
        extra_pip_requirements=extra_pip_requirements,
        metadata=metadata,
    )


def _make_drx_model(
    model: Union[Model, ModelOperator, Deployment],
    mlflow_model: Optional[mlflow.modelx.model.Model] = None,
    signature: Optional[ModelSignature] = None,
    input_example: Optional[ModelInputExample] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> mlflow.models.Model:
    if mlflow_model is None:
        mlflow_model = mlflow.models.Model()
    if signature is not None:
        mlflow_model.signature = signature
    if input_example is not None:
        pass
    if metadata is None:
        metadata = {}
    if isinstance(model, drxModel):
        metadata["dr_model"] = model._model_id
        metadata["dr_project"] = model._project_id
    elif isinstance(model, ModelOperator):
        metadata["dr_model"] = model._best_model._model_id  # type: ignore[union-attr]
        metadata["dr_project"] = model._project_id
    elif isinstance(model, Deployment) and hasattr(model, "_deployment_id"):
        metadata["dr_deployment"] = model._deployment_id
        deployment_json = utils.create_task_new_thread(
            dep_client.get_deployment(cast(str, model._deployment_id))
        ).result()
        metadata["dr_model"] = deployment_json["model"]["id"]
        metadata["dr_project"] = deployment_json.get("projectId", None)
    else:
        raise TypeError("What did you pass in? Should be a drx Model or Deployment")
    mlflow_model.metadata = metadata
    pyfunc.add_to_model(
        mlflow_model,
        loader_module="datarobotx.mlflow.drx_mlflow",
        conda_env=_CONDA_ENV_FILE_NAME,
        python_env=_PYTHON_ENV_FILE_NAME,
        code=None,
    )
    mlflow_model.add_flavor(
        FLAVOR_NAME,
        datarobotx_version=VERSION,
        code=None,
    )
    return mlflow_model


def load_model(model_uri: str, dst_path: Optional[str | Path] = None) -> DrxMlflowModel:
    """
    Load a drx Model using MLflow

    Parameters
    ----------
    model_uri: str
        The location, in URI format, of the MLflow model. For example:
            - `/Users/me/path/to/local/model`
            - `relative/path/to/local/model`
            - `s3://my_bucket/path/to/model`
            - `runs:/<mlflow_run_id>/run-relative/path/to/model`
        For more information about supported URI schemes, see
        `Referencing Artifacts <https://www.mlflow.org/docs/latest/tracking.html#
        artifact-locations>`_.
    dst_path: str
        The local filesystem path to which to download the model artifact.
        This directory must already exist. If unspecified, a local output
        path will be created.

    Returns
    -------
    DrxMlflowModel
        A thin wrapper around a drx Model or Deployment
    """
    local_model_path = _download_artifact_from_uri(artifact_uri=model_uri, output_path=dst_path)
    flavor_conf = _get_flavor_configuration(model_path=local_model_path, flavor_name=FLAVOR_NAME)
    _add_code_from_conf_to_system_path(local_model_path, flavor_conf)
    datarobotx_model_file_path = os.path.join(local_model_path)
    return _load_model(path=datarobotx_model_file_path)


class DrxMlflowModel:
    project: ModelOperator
    model: Union[drxModel, AutopilotModel]
    deployment: Deployment

    def __init__(
        self,
        project_id: Optional[str] = None,
        model_id: Optional[str] = None,
        deployment_id: Optional[str] = None,
    ) -> None:
        assert (project_id is not None) or (deployment_id is not None)
        if deployment_id:
            self.deployment = Deployment(deployment_id)
            self.project = utils.create_task_new_thread(
                self.populate_project_from_deployment()
            ).result()
        else:
            self.model = AutoMLModel.from_project_id(project_id=cast(str, project_id))
            deployment = utils.create_task_new_thread(
                self.populate_deployment_from_project()
            ).result()
            if deployment:
                self.deployment = deployment
            self.model = drxModel(project_id=project_id, model_id=model_id)
            deployment = utils.create_task_new_thread(
                self.populate_deployment_from_project()
            ).result()
            if deployment:
                self.deployment = deployment

    def predict(
        self, X: pd.DataFrame, max_explanations: Optional[int] = None, batch_mode: bool = False
    ) -> pd.DataFrame:
        """Make predictions with a drx model in MLflow

        This function simply wraps the `predict` function of the AutoMLModel, AutoTSModel, or Deployment etc.

        Parameters
        ----------
        X : pd.DataFrame
            DataFrame to use for the productions.
        max_explanations : int
            the number of prediction explanantions to return if supported by this model.
        batch_mode : bool
            If the model is deployed using a DataRobot deployment, predict will use the real-time endpoint.
            To use batch predictions, set this to True.

        Returns
        -------
        pd.DataFrame
            The predictions and prediction explanations if requested.
        """
        if hasattr(self, "deployment"):
            return self.deployment.predict(
                X, max_explanations=max_explanations, batch_mode=batch_mode
            )
        else:
            return self.model.predict(X)

    def predict_proba(
        self, X: pd.DataFrame, max_explanations: Optional[int] = None, batch_mode: bool = False
    ) -> pd.DataFrame:
        if hasattr(self, "deployment"):
            return self.deployment.predict_proba(
                X, max_explanations=max_explanations, batch_mode=batch_mode
            )
        else:
            return self.model.predict_proba(X)

    def predict_unstructured(self, X: Dict[str, Any]) -> Any:
        if hasattr(self, "deployment"):
            return self.deployment.predict_unstructured(X)
        else:
            raise ValueError("Only deployments support unstructured predictions")

    async def populate_project_from_deployment(self) -> Optional[ModelOperator]:
        deployment_json, settings_json = await asyncio.gather(
            dep_client.get_deployment(cast(str, self.deployment._deployment_id)),
            dep_client.get_deployment_settings(cast(str, self.deployment._deployment_id)),
        )
        model_kind = ModelKind.infer_model_kind(
            settings_json=settings_json, deployment_json=deployment_json
        )
        if deployment_json.get("projectId", None):
            model_kind = ModelKind.infer_model_kind(
                settings_json=settings_json, deployment_json=deployment_json
            )
            if model_kind.isTimeSeries:
                return AutoTSModel.from_project_id(deployment_json.get("projectId"))
            elif model_kind.isAnomalyDetectionModel:
                return AutoAnomalyModel.from_project_id(deployment_json.get("projectId"))
            elif model_kind.isClustering:
                return AutoClusteringModel.from_project_id(deployment_json.get("projectId"))

            else:
                return AutoMLModel.from_project_id(deployment_json.get("projectId"))
        else:
            return None

    async def populate_deployment_from_project(self) -> Optional[Deployment]:
        assert self.model._project_id is not None
        deployment_json = await dep_client.search_deployments_for_match(self.model._project_id)
        if deployment_json:
            return Deployment(deployment_json["id"])
        else:
            return None


def _load_pyfunc(path: str | Path) -> mlflow.pyfunc.Model:
    """
    Load PyFunc implementation

    Called by `pyfunc.load_model`.
    :param path: Local filesystem path to the MLflow Model with the `statsmodels` flavor.
    """
    return _load_model(path)


def _load_model(path: str | Path) -> DrxMlflowModel:
    if ((Path(path) / Path("MLModel"))).exists():
        ml_model = (Path(path) / Path("MLModel")).read_text()
    elif (
        (Path(path) / Path("MLmodel"))
    ).exists():  # in databricks this is MLmodel which is super weird
        ml_model = (Path(path) / Path("MLmodel")).read_text()
    else:
        raise mlflow.MlflowException(f"Can't fild the MLModel file at {path}")
    loader = yaml.safe_load(ml_model)
    deployment_id = loader["metadata"].get("dr_deployment")
    model_id = loader["metadata"].get("dr_model")
    project_id = loader["metadata"].get("dr_project")
    model = DrxMlflowModel(project_id, model_id, deployment_id)
    return model


@autologging_integration(FLAVOR_NAME)  # type: ignore[misc]
def autolog(
    log_models: bool = False,
    disable: bool = False,  # pylint: disable=unused-argument
    silent: bool = False,  # pylint: disable=unused-argument
    number_of_models_to_log: int = 10,
) -> None:
    """
    Enable (or disable) automatic logging of DR models to MLflow

    Logs the following:
    - Metric scores for each model on the leaderboard
    - An html artifact of the leaderboard and the chosen champion

    Parameters
    ----------
    log_models: bool
        If `True`, trained models are logged as MLflow model artifacts.
        If `False`, trained models are not logged.
        Input examples and model signatures, which are attributes of MLflow models,
        are also omitted when `log_models` is `False`.
    disable: bool
        disable autologging. This argument is required by mlflow `autologging_utils`
        but not presently implemented.
    silent: bool
        This argument is required by mlflow `autologging_utils`, but not presently
        implemented.
    number_of_models_to_log int:
        Using DataRobot AutoML, DataRobot may generate hundreds of model variations.
        By default, the top 10 models will be logged as "runs" in MLFlow,
        you can raise or lower this number using this parameter.

    """
    logger.info("Auto-logging for MLflow", extra={"is_header": True})
    handler = MLFlowFitHandler(
        log_models=log_models, number_of_models_to_log=number_of_models_to_log
    )
    logger.addHandler(handler)


class MLFlowFitHandler(logging.Handler):
    """
    Logging handler for logging experiments to MLFlow

    This handler does not format entries for rendering but rather just logs stuff to MLFlow.

    Parameters
    ----------
    log_models : bool
        Whether the handler should log models to MLFlow
    number_of_models_to_log : int, default = 10
        How many models from the leaderboard to log
    remove_after_one : bool = False
        Whether this handler should remove itself after
        the first call to emit()
    experiment_id : str or int, optional
        Log to an existing MLFlow experiment id
    """

    def __init__(
        self,
        log_models: bool,
        number_of_models_to_log: int = 10,
        remove_after_one: bool = False,
        experiment_id: Optional[str | int] = None,
    ):
        super().__init__()
        self.addFilter(filter=lambda x: hasattr(x, "project_ready_for_logging"))
        self.log_models = log_models
        self.number_of_models_to_log = number_of_models_to_log
        self.remove_after_one = remove_after_one
        self.experiment_id = experiment_id

    def emit(self, record: logging.LogRecord) -> None:
        """Format and log metrics in separate thread to avoid blocking"""

        async def _wrapper(experiment_id: Optional[str | int] = None) -> None:
            """Log the metrics"""
            nonlocal record
            leaderboard: List[str] = getattr(record, "leaderboard")
            project_id = getattr(record, "project_id")
            if len(leaderboard) > 0:
                if len(leaderboard) > self.number_of_models_to_log:
                    models_list = leaderboard[0 : self.number_of_models_to_log]
                else:
                    models_list = leaderboard
                models_json: List[Dict[str, Any]]
                _, models_json, m_advanced_tuners = await asyncio.gather(
                    proj_client.get_project(project_id),
                    asyncio.gather(
                        *[proj_client.get_model(pid=project_id, model_id=id) for id in models_list]
                    ),
                    asyncio.gather(
                        *[
                            retry_if_too_many_attempts(
                                proj_client.get_advanced_tuning_parameters, pid=project_id, mid=id
                            )
                            for id in models_list
                        ]
                    ),
                )

                for m_json, m_advanced_params in zip(models_json, m_advanced_tuners):
                    model_number = "M" + str(m_json["modelNumber"]) + " "
                    if experiment_id:
                        mlflow.start_run(
                            run_name=model_number + m_json["modelType"],
                            experiment_id=self.experiment_id,
                        )
                    else:
                        mlflow.start_run(run_name=model_number + m_json["modelType"])
                    mlflow.log_dict(m_json, artifact_file="dr_model_info.yaml")
                    mlflow.log_params(
                        {
                            "datarobot_url": config.Context()._webui_base_url
                            + f"/projects/{project_id}/models/{m_json['id']}/blueprint",
                            "feature_list_name": m_json["featurelistName"],
                            "sample_pct": m_json["samplePct"],
                            "is_starred": m_json["isStarred"],
                        }
                    )
                    mlflow.log_params(
                        {
                            _metric_name_fixer(p["taskName"] + "_" + p["parameterName"]): p[
                                "currentValue"
                            ]
                            for p in m_advanced_params["tuningParameters"]
                        }
                    )
                    for m in m_json["metrics"]:
                        metric_val = LeaderboardFormatter._metric_parser(
                            m_json["metrics"][m]
                        )  # ignore: type[attr-defined]
                        try:
                            mlflow.log_metric(
                                _metric_name_fixer(m),
                                metric_val,
                            )
                        except mlflow.exceptions.MlflowException:
                            logger.debug("%s Invalid value not logged", m)
                    if self.log_models:
                        model = drxModel(project_id=project_id, model_id=m_json["id"])
                        log_model(model, artifact_path="model")
                    mlflow.end_run()
                if experiment_id:
                    mlflow.start_run(
                        run_name="Autopilot Complete Final Leaderboard",
                        experiment_id=self.experiment_id,
                    )
                else:
                    mlflow.start_run(run_name="Autopilot Complete Final Leaderboard")
                formatter = LeaderboardFormatter(attr="model", as_html=True)
                card_formatter = ModelCardFormatter(attr="model", as_html=True)
                project: AutopilotModel = AutoMLModel.from_project_id(project_id)
                in_record_project = logging.makeLogRecord({"model": project})
                in_record_project = await formatter.add_format_context(in_record_project)
                best_model_record = logging.makeLogRecord({"model": project._best_model})
                best_model_record = await card_formatter.add_format_context(best_model_record)
                mlflow.log_text(
                    formatter.format_html(in_record_project),
                    artifact_file="leaderboard.html",
                )
                mlflow.log_text(
                    card_formatter.format_html(best_model_record),
                    artifact_file="best_model.html",
                )
                log_model(
                    project, artifact_path="model"
                )  # we will always log the "champion model" in the latest run
                mlflow.end_run()

        # per https://github.com/mlflow/mlflow/issues/1550#issuecomment-1024492066 mlflow doesn't like async
        # so let's wait this one out and make sure it completes
        utils.create_task_new_thread(_wrapper(self.experiment_id), wait=True)
        run = mlflow.active_run()
        if run:
            mlflow.end_run()
        if self.remove_after_one:
            self.remove()

    def remove(self) -> None:
        logger.removeHandler(self)


def _metric_name_fixer(metric_name: str) -> str:
    """per mlflow docs Names may only contain alphanumerics, underscores (_),
    dashes (-), periods (.), spaces ( ), and slashes (/)
    """
    n = metric_name
    if metric_name.find("@"):
        n = n.replace("@", "_AT_")
    if metric_name.find("%"):
        n = n.replace("%", "_PCT_")
    if metric_name.find("("):
        n = n.replace("(", " ")
    if metric_name.find(")"):
        n = n.replace(")", " ")
    if metric_name.find("/"):
        n = n.replace("/", "-")
    if metric_name.find(":"):
        n = n.replace(":", "-")
    pattern = re.compile(r"""[^a-zA-Z0-9_\ \.-]""")
    n = re.sub(pattern=pattern, repl="_", string=n)
    return n
