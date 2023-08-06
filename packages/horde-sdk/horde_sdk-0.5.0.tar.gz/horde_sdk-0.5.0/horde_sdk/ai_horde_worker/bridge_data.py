import pathlib
import urllib.parse

from loguru import logger
from pydantic import BaseModel, Field, field_validator, model_validator

from horde_sdk.ai_horde_api.consts import ALCHEMY_FORMS
from horde_sdk.ai_horde_worker.locale_info.bridge_data_fields import BRIDGE_DATA_FIELD_DESCRIPTIONS

_UNREASONABLE_NUMBER_OF_MODELS = 1000
"""1000"""


class HordeBridgeDataFile(BaseModel):
    #
    # Shared Worker-type Settings
    #

    api_key: str = Field(
        default="0000000000",
        title="API Key",
    )
    """The API key to use to authenticate with the Horde API. Defaults to the anonymous API key."""

    default_worker_name: str = Field("An Awesome AI Horde Worker", alias="worker_name")
    """The default name for any worker type. This is used to easily identify the worker.

    Note that if the user switches to a different worker type after having run a different worker type, the name will
    be rejected by the Horde API. This is because the name is unique to the worker type.
    """

    models_folder_parent: str = "./"
    """The directories to use to store the model folders. The spirit of this derives from `XDG_CACHE_HOME`, but it is
    not a *volatile* cache. It is the ordinary location for the models. Defaults to the current working directory."""

    temp_dir: str = "./tmp/"
    """The directory to use for temporary files such as model caches. Defaults to `./tmp/`."""

    allow_unsafe_ip: bool = True
    """Whether to allow img2img from unsafe IP addresses. This is only relevant if img2img is enabled."""

    priority_usernames: list[str] = Field(default_factory=list)
    """A list of usernames to prioritize. The API always considers this worker's user to be on this list."""

    stats_output_frequency: int = Field(default=30, json_schema_extra={"unit": "seconds"})
    """The frequency at which to output stats to the console, in seconds. Set to 0 to disable."""
    disable_terminal_ui: bool = False
    """Whether to disable the terminal UI. This is useful for running the worker in a container."""
    always_download: bool = True
    """Whether to always download models, without prompting for permission for each one."""
    suppress_speed_warnings: bool = False
    """Whether to suppress warnings about slower than ideal generations."""
    horde_url: str = ""  # TODO: consts.DEFAULT_HORDE_API_URL
    """The URL of the Horde API to use. Defaults to the official API."""

    @field_validator("horde_url")
    def url_validator(cls, v: str) -> str:
        parsed_url = urllib.parse.urlparse(v)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError(f"Invalid URL: {v}")
        return v

    @field_validator("api_key")
    def api_key_length(cls, v: str) -> str:
        if v == "0000000000":
            return v
        if len(v) != 22:
            raise ValueError("API key must be 22 characters long")
        return v

    @field_validator("forms")
    def forms_validator(cls, v: list) -> list:
        if not isinstance(v, list):
            raise ValueError("forms must be a list")
        validated_forms = []
        for form in v:
            form = str(form).lower()
            form = form.replace("-", "_")
            if form not in ALCHEMY_FORMS.__members__:
                raise ValueError(f"Invalid form: {form}")
            validated_forms.append(form)
        return validated_forms

    @field_validator("models_folder_parent", "temp_dir")
    def is_dir(cls, v: str) -> str:
        paths_list = []
        # Does it specific multiple directories?
        if ";" in v:
            for sub_v in v.split(";"):
                paths_list.append(sub_v)
        else:
            paths_list.append(v)
        for sub_v in paths_list:
            # See if it's a well-formed path, but don't check if it exists
            pathlib.Path(sub_v).absolute()

        return v


class ImageWorkerBridgeDataFile(BaseModel):
    """The bridge data file for a Dreamer or Alchemist worker."""

    #
    # Dreamer
    #

    allow_controlnet: bool = False
    """Whether to allow the use of ControlNet. This requires img2img to be enabled."""

    allow_img2img: bool = True
    """Whether to allow the use of img2img."""

    allow_lora: bool = False
    """Whether to allow the use of LoRA."""

    max_lora_cache_size: int = Field(
        default=10,
        ge=10,
        le=2048,  # I do not foresee anyone having a 2TB lora cache
        json_schema_extra={"unit": "GB"},
    )
    """The maximum size of the LoRA cache, in gigabytes."""

    allow_inpainting: bool = Field(
        default=False,
        alias="allow_painting",
    )
    """Whether to allow the use of inpainting."""

    allow_post_processing: bool = False
    """Whether to allow the use of post-processing."""

    blacklist: list[str] = Field(
        default_factory=list,
    )
    """A list of terms or phrases to blacklist. Jobs containing these terms will be not be assigned to this worker."""

    censor_nsfw: bool = False
    """Whether to censor NSFW content."""

    censorlist: list[str] = Field(
        default_factory=list,
    )
    """A list of terms to allow through the censor. Jobs containing these terms will not be censored for those words
    alone."""

    disable_disk_cache: bool = False
    """Whether to disable the disk cache."""

    dynamic_models: bool = False
    """Whether to dynamically switch the models loaded to correspond to the models with the longest queues."""

    max_dynamic_models_to_download: int = Field(
        default=10,
        ge=0,
        le=_UNREASONABLE_NUMBER_OF_MODELS,
        alias="max_models_to_download",
    )
    """The maximum number of models to download."""

    number_of_dynamic_models_to_load: int = Field(
        default=1,
        ge=0,
        le=_UNREASONABLE_NUMBER_OF_MODELS,
    )
    """The number of dynamic models to load at a time."""

    max_power: int = Field(
        default=8,
        ge=1,
        le=512,
        json_schema_extra={"unit": "* (8 * 64 * 64) pixels"},
    )
    """The factor in the equation `max_power * (8 * 64 * 64)`. This will be the maximum number of pixels that can be
    generated (with inference) in a single job by this worker."""

    image_models_to_load: list[str]
    """A list of models to load. This can be a list of model names, or a list of model loading instructions, such as
    `top 100` or `all models`."""

    image_models_to_skip: list = Field(
        default_factory=list,
    )
    """When a meta model loading instruction is given, like `top 100`, models in this list will be skipped."""

    nsfw: bool = True
    """Whether to allow NSFW content."""

    queue_size: int = Field(default=1, ge=1, le=4)
    """The number of jobs to queue."""

    threads: int = Field(
        default=1,
        ge=1,
        le=16,  # 8 already seems incredibly out of reach for most people, but I have set it to 16 just in case
    )
    """The number of threads to use for inference."""

    require_upfront_kudos: bool = False
    """Whether to require upfront kudos for jobs. This effectively makes the worker reject jobs from
    the anonymous API key, or from keys with no kudos."""

    ram_to_leave_free: str = Field(
        default="80%",
        pattern=r"^\d+%$|^\d+$",
        json_schema_extra={"unit": "Percent or MB"},
    )
    """The amount of RAM to leave free for the system to use. This is a percentage or a number in megabytes."""

    vram_to_leave_free: str = Field(
        default="80%",
        pattern=r"^\d+%$|^\d+$",
        json_schema_extra={"unit": "Percent or MB"},
    )
    """The amount of VRAM to leave free for the system to use. This is a percentage or a number in megabytes."""

    #
    # Alchemist Settings
    #

    alchemist_name: str = "An Awesome Alchemist"
    """The name of the worker if it is an alchemist. This is used to easily identify the worker."""

    forms: list[str] = ["caption", "nsfw", "interrogation", "post-process"]
    """The type of services or processing an alchemist worker will provide."""

    @model_validator(mode="before")
    def root_validator(cls, values: dict) -> dict:
        if not values.get("allow_img2img", None) and values.get("allow_controlnet", None):
            logger.warning(
                (
                    "allow_controlnet is set to True, but allow_img2img is set to False. "
                    "ControlNet requires img2img to be enabled. Setting allow_controlnet to false."
                ),
            )
            values["allow_controlnet"] = False
        return values

    @field_validator("image_models_to_load")
    def models_to_load_validator(cls, v: list) -> list:
        if not isinstance(v, list):
            v = [v]
        if not v:
            v = ["top 2"]
            logger.warning("No models specified in bridgeData.yaml. Defaulting to top 2 models.")
        return v

    @field_validator("ram_to_leave_free", "vram_to_leave_free")
    def ram_to_leave_free_validator(cls, v: str | int | float) -> str | int | float:
        if isinstance(v, str):
            if v.isdigit():
                v = int(v)
            elif v.endswith("%"):
                _ = float(v[:-1])
                if _ < 0 or _ > 100:
                    raise ValueError("RAM to leave free must be between 0 and 100%")
        else:
            if v < 0:
                raise ValueError("RAM to leave free must be greater than or equal to 0")
        return v


class ScribeBridgeDataFile(BaseModel):
    # Scribe Settings
    kai_url: str = "http://localhost:5000"
    """The URL of the KoboldAI API to use. Defaults to the official API."""

    max_context_length: int = Field(
        default=1024,
        ge=1,
        le=16384,  # This is just a sanity check, I doubt anyone would want to go this high
        json_schema_extra={"unit": "tokens"},
    )
    """The maximum number of tokens to use for context with a scribe job."""

    max_length: int = Field(
        default=80,
        ge=1,
        le=16384,  # This is just a sanity check, I doubt anyone would want to go this high
        json_schema_extra={"unit": "tokens"},
    )
    """The maximum number of tokens to generate for a scribe job."""

    branded_model: bool = True
    """If true, this is a custom scribe model, and the horde API will identify uniquely to this worker's API key."""


# Get all BaseModels from the current file
ALL_DATA_FILES_TYPES = [HordeBridgeDataFile, ImageWorkerBridgeDataFile, ScribeBridgeDataFile]


# Dynamically add descriptions to the fields of all the base models
for data_file_type in ALL_DATA_FILES_TYPES:
    for field_name, field in data_file_type.model_fields.items():
        if field_name in BRIDGE_DATA_FIELD_DESCRIPTIONS:
            field.description = BRIDGE_DATA_FIELD_DESCRIPTIONS[field_name]
