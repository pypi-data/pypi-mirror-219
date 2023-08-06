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

import logging
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING

from datarobotx.openblueprints.blueprint_mappings import (
    CONVERTER_LOOKUP_MAPPINGS,
    CONVERTER_MAPPINGS,
)
from datarobotx.openblueprints.blueprint_string_converter import BlueprintStringConverter
from datarobotx.openblueprints.enums import COLUMN_SELECTORS, PASSTHROUGH_STRING

logger = logging.getLogger(__package__)

if TYPE_CHECKING:
    from mypy_extensions import TypedDict

    class StageDict(TypedDict):
        name: str
        transform: str
        input: BlueprintInput
        imports: Optional[str]

    StagesDict = Dict[str, StageDict]
    BlueprintInput = List[str]
    BlueprintTask = List[str]
    BlueprintTaskType = str
    BlueprintStage = Tuple[BlueprintInput, BlueprintTask, BlueprintTaskType]
    BlueprintJson = Dict[str, BlueprintStage]


class BlueprintConverter(BlueprintStringConverter):
    @classmethod
    def convert(cls, blueprint_json: BlueprintJson) -> str:
        """Convert a blueprint to an open source representation block of code

        Parameters
        ----------
        blueprint_json : BlueprintJson
            A json formatted dictionary of a datarobot blueprint. Can be retrieved using the datarobot API.

        Returns
        -------
        str
        """

        # Extract the stage mappings from the blueprint
        stages = cls.extract_stages(blueprint_json)

        # Extract the estimator itself and its direct inputs from the blueprint
        _, estimator_stage_key = cls.extract_estimator_inputs(blueprint_json)

        blueprint_imports = sorted({str(s["imports"]) for _, s in stages.items() if s["imports"]})
        stage_input_paths = cls.construct_stage_input_paths(stages, estimator_stage_key)

        # Construct a preprocessing pipeline from the stage mappings
        preprocessor_pipeline = cls.build_preprocessor_pipeline(stages, stage_input_paths)

        # Construct a code representation of the blueprint from the preprocessing pipeline
        # and the estimator itself
        blueprint_code = cls.make_blueprint(
            blueprint_imports,
            preprocessor_pipeline,
            cls.extract_element_from_stage(stages[estimator_stage_key]),
        )

        return blueprint_code

    @classmethod
    def build_preprocessor_pipeline(
        cls, stages: StagesDict, stage_input_paths: List[List[str]]
    ) -> List[str]:
        """Build a preprocessor pipeline from blueprint stages"""
        preprocessor_pipeline = []
        for stage_input_path in stage_input_paths:
            # Determine what input will be used for this column transformer
            transformer_input_type = stage_input_path[0]
            if transformer_input_type not in COLUMN_SELECTORS:
                raise NotImplementedError("Input type does not have a supported mapping.")
            transformer_name = transformer_input_type
            transformer_column_selector = COLUMN_SELECTORS[transformer_input_type]

            # If there is a single step that exists in the path, create a ColumnTransformer
            # that passes through a single input type directly to the estimator.
            if len(stage_input_path) == 1:
                preprocessor_pipeline.append(
                    (
                        cls.make_column_transformer_element_from_pipeline(
                            transformer_name,
                            PASSTHROUGH_STRING,
                            transformer_column_selector,
                        )
                    )
                )
            # Else we should create a standard multistep ColumnTransformer
            else:
                # Aggregate the transformer steps
                # NOTE: We ignore the input type index 0 and the estimator index -1)
                transformer_steps = []
                for current_stage_id in stage_input_path[1:-1]:
                    current_stage = stages[current_stage_id]
                    transformer_name += f"_{current_stage['name']}"
                    transformer_steps.append(cls.extract_element_from_stage(current_stage))

                # Convert the steps to a ColumnTransformer
                transformer_pipeline_elements = cls.make_pipeline_elements_from_steps(
                    transformer_steps
                )
                transformer_pipeline = cls.make_pipeline_from_pipeline_elements(
                    transformer_pipeline_elements
                )
                preprocessor_pipeline.append(
                    cls.make_column_transformer_element_from_pipeline(
                        transformer_name,
                        transformer_pipeline,
                        transformer_column_selector,
                    )
                )
        return preprocessor_pipeline

    @classmethod
    def extract_stages(cls, blueprint_json: BlueprintJson) -> StagesDict:
        stages = {}
        for stage_name in sorted(blueprint_json.keys()):
            stage = cls.parse_blueprint_stage(blueprint_json[stage_name])
            stages[stage_name] = stage
        return stages

    @classmethod
    def construct_stage_input_paths(
        cls, stages: StagesDict, estimator_stage_key: str
    ) -> List[List[str]]:
        # Construct a recursive list of the end to end stages that must be touched
        stage_input_paths = []

        def dfs_stages_recursive(
            stages: StagesDict, current_stage: str, visited: List[str]
        ) -> None:
            visited.append(current_stage)
            input_stages = stages[current_stage]["input"]
            for input_stage in input_stages:
                if input_stage in COLUMN_SELECTORS:
                    # We want to revert the stored path since it was added in backwards order.
                    stages_visited = visited + [input_stage]
                    stage_input_paths.append(stages_visited[::-1])
                elif input_stage not in visited:
                    dfs_stages_recursive(stages, input_stage, visited.copy())

        dfs_stages_recursive(stages, estimator_stage_key, [])
        return stage_input_paths

    @classmethod
    def parse_blueprint_stage(cls, blueprint_stage: BlueprintStage) -> StageDict:
        """Convert a stage of a blueprint to an open representation mapping"""
        stage_input, stage_class, _ = blueprint_stage

        if len(stage_class) > 1:
            raise ValueError("Blueprints should only have one class action per stage")

        blueprint_parts = stage_class[0].split(" ")
        dr_class = blueprint_parts[0]
        dr_class_params = cls.extract_dr_class_params_from_blueprint_parts(blueprint_parts)

        dr_class, class_str, class_imports = cls.convert_blueprint_class_to_open_representation(
            dr_class, dr_class_params
        )
        return {
            "name": dr_class,
            "transform": class_str,
            "input": stage_input,
            "imports": class_imports,
        }

    @staticmethod
    def extract_dr_class_params_from_blueprint_parts(blueprint_parts: List[str]) -> Dict[str, str]:
        """Extract the input parameters and values from the blueprint class representation"""
        dr_class_params_str = None
        if len(blueprint_parts) == 2:
            dr_class_params_str = blueprint_parts[1]
        elif len(blueprint_parts) > 2:
            dr_class_params_str = "".join(blueprint_parts[1:])

        dr_class_params = {}
        if dr_class_params_str is not None:
            for param in dr_class_params_str.split(";"):
                param_parts = param.split("=")
                if len(param_parts) == 1:
                    dr_class_params[param_parts[0]] = "True"
                    continue
                if len(param_parts) > 2:
                    logger.warning(
                        "Model parameter %s is not a supported setting for "
                        "converting. Only params specified as name=value can be "
                        "converted to open source representations. This parameter "
                        "has multiple = values and cannot be parsed.",
                        param,
                    )
                    continue
                dr_class_params[param_parts[0]] = param_parts[1]
        return dr_class_params

    @staticmethod
    def convert_blueprint_class_to_open_representation(
        dr_class: str, dr_class_params: Dict[str, Any]
    ) -> Tuple[str, str, Optional[str]]:
        converter_class = CONVERTER_LOOKUP_MAPPINGS.get(dr_class)
        class_str = PASSTHROUGH_STRING
        class_imports = None
        if converter_class is not None:
            converter = CONVERTER_MAPPINGS[converter_class]
            class_str = converter.get_open_representation(dr_class_params)
            class_imports = converter.get_required_imports()
        return dr_class, class_str, class_imports

    @staticmethod
    def extract_element_from_stage(stage: StageDict) -> Tuple[str, str]:
        return str(stage["name"]), str(stage["transform"])

    @staticmethod
    def extract_estimator_inputs(blueprint_json: BlueprintJson) -> Tuple[List[str], str]:
        # Check for predictors as either type = "P" or if type includes
        # extra (e.g. "P shape=True") check that start is P
        estimator_stage_key = next(
            k
            for k, v in blueprint_json.items()
            if (v[2] == "P" or (len(v[2]) > 1 and v[2][0] == "P"))
        )
        estimator_stage = blueprint_json[estimator_stage_key]
        estimator_inputs = estimator_stage[0]
        return estimator_inputs, estimator_stage_key
