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

import os
from typing import Dict, List

import yaml

from datarobotx.openblueprints.mapping_object import MappingObject


def blueprint_mappings() -> List[MappingObject]:
    """Helper tool to read mappings from yaml"""
    task_mappings_path = os.path.dirname(os.path.abspath(__file__))
    with open(
        os.path.join(task_mappings_path, "task_mappings.yaml"), encoding="UTF-8"
    ) as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)

    mappings = []
    for task, task_values in yaml_data["tasks"].items():
        mappings.append(
            MappingObject(
                dr_class=task,
                open_class=task_values["open_class"]
                if len(task_values["open_class"]) > 1
                else None,
                dr_class_params_mapping=task_values.get("parameters"),
                versions=task_values["versions"],
            )
        )
    return mappings


CONVERTER_MAPPINGS: Dict[str, MappingObject] = {d.dr_class: d for d in blueprint_mappings()}
CONVERTER_LOOKUP_MAPPINGS: Dict[str, str] = {
    k: v for d in blueprint_mappings() for k, v in d.get_class_mappings().items()
}
