from jupyter_scheduler.exceptions import SchedulerError
from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.extension.handler import ExtensionHandlerMixin
import os
import tornado
import json
import time
import urllib
import botocore.exceptions
from async_timeout import timeout

from amazon_sagemaker_jupyter_scheduler.advanced_environments.sagemaker_advanced_environments import (
    SageMakerAdvancedEnvironments,
)
from amazon_sagemaker_jupyter_scheduler.advanced_environments.sagemaker_studio_advanced_environment import (
    SageMakerStudioAdvancedEnvironments,
)
from amazon_sagemaker_jupyter_scheduler.environment_detector import (
    JupyterLabEnvironmentDetector,
    JupyterLabEnvironment,
)
from amazon_sagemaker_jupyter_scheduler.app_metadata import (
    get_region_name,
    get_sagemaker_environment,
)

WEBAPP_SETTINGS_URL = "https://studiolab.sagemaker.aws/settings.json"
MAX_WAIT_TIME_FOR_API_CALL_SECS = 8.0


class AdvancedEnvironmentsHandler(ExtensionHandlerMixin, JupyterHandler):
    @tornado.web.authenticated
    async def get(self):
        try:
            async with timeout(MAX_WAIT_TIME_FOR_API_CALL_SECS):
                if (
                    get_sagemaker_environment()
                    == JupyterLabEnvironment.SAGEMAKER_STUDIO
                ):
                    self.log.info(f"SageMaker Studio environment detected")
                    envs = await SageMakerStudioAdvancedEnvironments().get_advanced_environments(
                        self.log
                    )
                else:
                    self.log.info(f"Vanilla JupyterLab environment detected")
                    envs = (
                        await SageMakerAdvancedEnvironments().get_advanced_environments(
                            self.log
                        )
                    )
                self.finish(envs.json())
        except botocore.exceptions.ClientError as error:
            self.set_status(error.response["ResponseMetadata"]["HTTPStatusCode"])
            self.finish(
                json.dumps(
                    {
                        "error_code": error.response["Error"]["Code"],
                        "message": error.response["Error"]["Message"],
                    }
                )
            )
        except SchedulerError as error:
            self.set_status(403)
            self.finish(
                json.dumps({"error_code": "NoCredentials", "message": str(error)})
            )
        except Exception as error:
            self.set_status(500)
            self.finish(json.dumps({"error": str(error)}))


class ValidateVolumePathHandler(ExtensionHandlerMixin, JupyterHandler):
    @tornado.web.authenticated
    async def post(self):
        try:
            body = self.get_json_body()
            if "file_path" in body:
                file_exist = os.path.exists(body["file_path"])
                self.set_status(200)
                self.finish(json.dumps({"file_path_exist": file_exist}))
            else:
                self.set_status(400)
                self.finish(json.dumps({"error": "invalid input"}))
        except Exception as e:
            self.log.exception(f"Encountered error when validating file path: {e}")
            self.set_status(500)
            self.finish(json.dumps({"error": e.msg}))


class SageMakerImagesListHandler(ExtensionHandlerMixin, JupyterHandler):
    @tornado.web.authenticated
    async def get(self):
        self.finish(
            json.dumps(
                FirstPartyImagesListProvider().get_first_party_images_list(
                    get_region_name()
                )
            )
        )


class FeatureAccessControlHandler(ExtensionHandlerMixin, JupyterHandler):
    @tornado.web.authenticated
    async def post(self):
        current_time_ms = int(time.time() * 1000)
        try:
            body = self.get_json_body()
            if "feature_name" in body:
                feature_name = body["feature_name"]
                download_request = urllib.request.Request(WEBAPP_SETTINGS_URL)
                with urllib.request.urlopen(download_request) as response_data:
                    self.set_status(200)
                    settings_data = json.load(response_data)
                    features_data = settings_data.get("featureAccessConfig", [])
                    for feature_data in features_data:
                        if feature_data["name"] == feature_name:
                            self.finish(
                                json.dumps(
                                    {
                                        "feature_found": True,
                                        "feature_enabled": int(time.time())
                                        > int(feature_data["time"]),
                                        "current_time_ms": current_time_ms,
                                    }
                                )
                            )
                            return
                    self.finish(
                        json.dumps(
                            {"feature_found": False, "current_time_ms": current_time_ms}
                        )
                    )
            else:
                self.set_status(400)
                self.finish(
                    json.dumps(
                        {"error": "invalid input", "current_time_ms": current_time_ms}
                    )
                )
        except urllib.error.HTTPError as e:
            self.log.exception(
                f"Encountered error [{e.status}] when downloading notebook"
            )
            self.set_status(e.status)
            self.finish(
                json.dumps({"error": e.msg, "current_time_ms": current_time_ms})
            )
        except Exception as e:
            self.log.exception(
                f"Encountered error when checking if feature is enabled: {e}"
            )
            self.set_status(500)
            self.finish(
                json.dumps({"error": e.msg, "current_time_ms": current_time_ms})
            )
