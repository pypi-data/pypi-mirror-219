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

from typing import Any, Dict, List, Optional


class MappingObject:
    """MappingObject is a simple representation of a DataRobot class to Open Source class"""

    def __init__(
        self,
        dr_class: str,
        open_class: Optional[str] = None,
        dr_class_params_mapping: Optional[Dict[str, Any]] = None,
        versions: Optional[List[str]] = None,
    ):
        self.dr_class = dr_class
        self.dr_class_params_mapping = (
            dr_class_params_mapping if dr_class_params_mapping is not None else {}
        )
        self.open_class = open_class
        self.versions = versions if versions is not None else []

    def get_class_mappings(self) -> Dict[str, str]:
        """Return a list of class and clone mappings from dr_class to open source open_class."""
        class_mapping = {self.dr_class: self.dr_class}
        # Add clone mappings
        for version in self.versions:
            class_mapping[version] = self.dr_class
        return class_mapping

    def get_open_representation(self, dr_class_params: Optional[Dict[str, Any]] = None) -> str:
        # If no class is defined or the class has no good mapping, return "passthrough" with quotes
        if self.open_class is None or self.open_class == "passthrough":
            return '"passthrough"'

        # If the open class is a complex passthrough directly constructed
        if "(" in self.open_class:
            return self.open_class

        # Convert the dr_class_params to open_class_params
        dr_class_params = dr_class_params if dr_class_params is not None else {}
        open_class_param_string = ""
        for key, val in dr_class_params.items():
            if key in self.dr_class_params_mapping:
                open_class_param_string += f"{self.dr_class_params_mapping[key]}={val}"

        return f"{self.open_class}({open_class_param_string})"

    def get_required_imports(self) -> Optional[str]:
        # If no class is defined or the class has no good mapping, return "passthrough" with quotes
        if self.open_class is None or self.open_class == "passthrough":
            return None

        open_class_parts = self.open_class.split(".")
        return (
            open_class_parts[0] if len(open_class_parts) == 1 else ".".join(open_class_parts[:-1])
        )
