# flake8: noqa

from ._version import __version__
from .common.config import Context
from .common.configurator import Configurator
from .common.dr_config import (
    DataConfig,
    DRConfig,
    FeaturesAutoTSConfig,
    FeaturesConfig,
    FeaturesSAFERConfig,
    FeaturesTSFeatureSettingConfig,
    FeaturesTSPeriodicityConfig,
    MetadataConfig,
    ModelingAutoMLConfig,
    ModelingAutoTSConfig,
    ModelingBiasFairnessConfig,
    ModelingConfig,
    ModelingModeConfig,
    PartitioningConfig,
    PartitioningDateTimeConfig,
    PartitioningDTBacktestConfig,
    PartitioningGroupConfig,
    PartitioningUserConfig,
    TargetAggregationConfig,
    TargetAutoMLConfig,
    TargetAutoTSConfig,
    TargetConfig,
)
from .common.transformations import featurize_explanations, melt_explanations
from .models.autoanomaly import AutoAnomalyModel
from .models.autocluster import AutoClusteringModel
from .models.automl import AutoMLModel
from .models.autots import AutoTSModel
from .models.colreduce import ColumnReduceModel
from .models.deploy import deploy
from .models.deployment import Deployment
from .models.evaluation import evaluate, import_parametric_model
from .models.featurediscovery import FeatureDiscoveryModel, Relationship
from .models.model import Model
from .models.selfdiscovery import SelfDiscoveryModel
from .models.share import share
from .models.sparkingest import downsample_spark, spark_to_ai_catalog, SparkIngestModel
from .openblueprints.blueprint_converter import BlueprintConverter

# __version__ is expected by downstream applications that need consume DRX as dependency like MLFlow
VERSION = __version__

DR_TRACKABLE = True
