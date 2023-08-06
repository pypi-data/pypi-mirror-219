from amazon_sagemaker_jupyter_scheduler.logging import init_api_operation_logger
from jupyter_server.extension.application import ExtensionApp
from amazon_sagemaker_jupyter_scheduler.handlers import (
    AdvancedEnvironmentsHandler,
    SageMakerImagesListHandler,
    ValidateVolumePathHandler,
    FeatureAccessControlHandler
)

class SageMakerSchedulingApp(ExtensionApp):
    name = "amazon_sagemaker_jupyter_scheduler"
    handlers = [
        (r"/advanced_environments", AdvancedEnvironmentsHandler),
        (r"/sagemaker_images", SageMakerImagesListHandler),
        (r"/validate_volume_path", ValidateVolumePathHandler),
        (r"/sagemaker_feature_enabled", FeatureAccessControlHandler),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        init_api_operation_logger(self.log)
