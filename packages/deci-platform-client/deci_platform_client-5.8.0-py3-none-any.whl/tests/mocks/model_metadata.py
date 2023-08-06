import random

import factory
from deci_platform_client.models import (
    APIResponseBaselineModelResponseMetadata,
    BaselineModelResponseMetadata,
    DeepLearningTask,
    DeepLearningTaskLabel,
    FrameworkType,
    HardwareReturnSchema,
    HardwareType,
    HardwareTypeLabel,
    ModelMetadata,
)

from tests.helpers import get_enum_values, get_random_enum_value


class HardwareReturnSchemaFactory(factory.Factory):
    class Meta:
        model = HardwareReturnSchema

    name = factory.LazyFunction(lambda: get_random_enum_value(HardwareType))
    label = factory.LazyFunction(lambda: get_random_enum_value(HardwareTypeLabel))


class ModelMetadataFactory(factory.Factory):
    class Meta:
        model = ModelMetadata

    name = factory.Faker("name")
    framework = factory.LazyFunction(
        lambda: random.choice([v for v in get_enum_values(FrameworkType) if v != "pytorch"])
    )
    dlTask = factory.LazyFunction(lambda: get_random_enum_value(DeepLearningTask))
    primaryHardware = factory.LazyFunction(lambda: get_random_enum_value(HardwareType))
    inputDimensions = factory.LazyFunction(lambda: [[random.randint(1, 100) for _ in range(3)]])
    primaryBatchSize = factory.Faker("pyint", min_value=1, max_value=64)


class BaselineModelResponseMetadataFactory(factory.Factory):
    class Meta:
        model = BaselineModelResponseMetadata

    name = factory.Faker("name")
    benchmark = factory.LazyFunction(dict)
    framework = factory.LazyFunction(
        lambda: random.choice([v for v in get_enum_values(FrameworkType) if v != "pytorch"])
    )
    dlTask = factory.LazyFunction(lambda: get_random_enum_value(DeepLearningTask))
    dlTaskLabel = factory.LazyFunction(lambda: get_random_enum_value(DeepLearningTaskLabel))
    primaryHardware = factory.SubFactory(HardwareReturnSchemaFactory)
    inputDimensions = factory.LazyFunction(lambda: [random.randint(1, 100) for _ in range(3)])
    primaryBatchSize = factory.Faker("pyint", min_value=1, max_value=64)


class APIResponseBaselineModelResponseMetadataFactory(factory.Factory):
    class Meta:
        model = APIResponseBaselineModelResponseMetadata

    success = True
    data = factory.SubFactory(BaselineModelResponseMetadataFactory)
    message = ""
