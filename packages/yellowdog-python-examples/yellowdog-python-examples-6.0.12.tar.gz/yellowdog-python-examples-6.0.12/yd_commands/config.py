"""
Common utility functions, mostly related to loading configuration data.
"""

import os
import re
from dataclasses import dataclass, field
from os import getenv
from os.path import abspath, dirname, join, normpath, relpath
from typing import Dict, List, Optional
from urllib.parse import urlparse
from uuid import uuid4

from toml import TomlDecodeError
from yellowdog_client.model import (
    ComputeRequirement,
    ConfiguredWorkerPool,
    ProvisionedWorkerPool,
    WorkRequirement,
)

from yd_commands.args import ARGS_PARSER
from yd_commands.config_keys import *
from yd_commands.printing import print_error, print_log
from yd_commands.type_check import check_list, check_str
from yd_commands.validate_properties import validate_properties
from yd_commands.variables import (
    UTCNOW,
    add_substitutions,
    load_toml_file_with_variable_substitutions,
    substitute_variable_str,
)


@dataclass
class ConfigCommon:
    url: str
    key: str
    secret: str
    namespace: str
    name_tag: str
    use_pac: bool


# Environment variable names for 'common' settings
YD_KEY = "YD_KEY"
YD_SECRET = "YD_SECRET"
YD_NAMESPACE = "YD_NAMESPACE"
YD_TAG = "YD_TAG"
YD_URL = "YD_URL"

TASK_BATCH_SIZE_DEFAULT = 2000
DEFAULT_URL = "https://portal.yellowdog.co/api"

NAMESPACE_SEPARATOR = "::"


@dataclass
class ConfigWorkRequirement:
    args: List[str] = field(default_factory=list)
    capture_taskoutput: bool = True
    completed_task_ttl: Optional[float] = None  # In minutes
    csv_files: Optional[List[str]] = None
    docker_env: Optional[Dict] = None
    docker_password: Optional[str] = None
    docker_username: Optional[str] = None
    env: Dict = field(default_factory=dict)
    exclusive_workers: Optional[bool] = None
    executable: Optional[str] = None
    finish_if_any_task_failed: bool = False
    finish_if_all_tasks_finished: bool = True
    flatten_input_paths: Optional[bool] = None
    flatten_upload_paths: Optional[bool] = None
    fulfil_on_submit: bool = False
    input_files: List[str] = field(default_factory=list)
    instance_types: Optional[List[str]] = None
    max_retries: int = 0
    max_workers: Optional[int] = None
    min_workers: Optional[int] = None
    optional_inputs: List[Dict] = field(default_factory=list)
    output_files: List[str] = field(default_factory=list)
    output_files_required: List[str] = field(default_factory=list)
    priority: float = 0.0
    providers: Optional[List[str]] = None
    ram: Optional[List[float]] = None
    regions: Optional[List[str]] = None
    task_batch_size: int = TASK_BATCH_SIZE_DEFAULT
    task_count: int = 1
    task_data: Optional[str] = None
    task_data_file: Optional[str] = None
    task_name: Optional[str] = None
    task_group_name: Optional[str] = None
    task_type: Optional[str] = None
    tasks_per_worker: Optional[int] = None
    upload_files: List[Dict] = field(default_factory=list)
    vcpus: Optional[List[float]] = None
    verify_at_start: List[str] = field(default_factory=list)
    verify_wait: List[str] = field(default_factory=list)
    worker_tags: Optional[List[str]] = None
    wr_data_file: Optional[str] = None
    wr_name: Optional[str] = None


CR_BATCH_SIZE_DEFAULT = 10000
WP_VARIABLES_PREFIX = "__"


@dataclass
class ConfigWorkerPool:
    compute_requirement_batch_size: int = CR_BATCH_SIZE_DEFAULT
    idle_node_shutdown_enabled: bool = True
    idle_node_shutdown_timeout: float = 5.0
    idle_pool_shutdown_enabled: bool = True
    idle_pool_shutdown_timeout: float = 30.0
    images_id: Optional[str] = (None,)
    instance_tags: Optional[Dict] = None
    maintainInstanceCount: bool = False  # Only for yd-instantiate
    max_nodes: int = 0
    max_nodes_set: bool = False  # Is max_nodes explicitly set?
    min_nodes: int = 0
    min_nodes_set: bool = False
    name: Optional[str] = None
    node_boot_timeout: float = 10.0
    target_instance_count: int = 0
    target_instance_count_set: bool = False
    template_id: Optional[str] = None
    user_data: Optional[str] = None
    user_data_file: Optional[str] = None
    user_data_files: Optional[List[str]] = None
    worker_pool_data_file: Optional[str] = None
    worker_tag: Optional[str] = None
    workers_per_vcpu: Optional[int] = None
    workers_per_node: int = 1


# CLI > YD_CONF > 'config.toml'
config_file = (
    getenv("YD_CONF", "config.toml")
    if ARGS_PARSER.config_file is None
    else ARGS_PARSER.config_file
)

try:
    print_log(f"Loading configuration data from: '{config_file}'")
    CONFIG_TOML: Dict = load_toml_file_with_variable_substitutions(config_file)
    try:
        validate_properties(CONFIG_TOML, f"'{config_file}'")
    except Exception as e:
        print_error(e)
        exit(1)
    CONFIG_FILE_DIR = dirname(abspath(config_file))

except FileNotFoundError as e:
    if ARGS_PARSER.config_file is not None:
        print_error(e)
        exit(1)
    # No config file, so create a stub config dictionary
    print_log(
        "No configuration file; expecting configuration data on command line "
        "or in environment variables"
    )
    CONFIG_TOML = {COMMON_SECTION: {}}
    CONFIG_FILE_DIR = os.getcwd()

except (PermissionError, TomlDecodeError) as e:
    print_error(
        f"Unable to load configuration data from '{config_file}': {e}",
    )
    exit(1)

except Exception as e:
    print_error(e)
    exit(1)


def load_config_common() -> ConfigCommon:
    """
    Load the configuration values for the 'common' section.
    """
    try:
        common_section = CONFIG_TOML[COMMON_SECTION]

        # Check for IMPORT directive (common section in a separate file)
        common_section_import_file = common_section.get(IMPORT, None)
        if common_section_import_file is not None:
            common_section = import_toml(common_section_import_file)

        # Replace common section properties with command line or
        # environment variable overrides. Precedence is:
        # command line > environment variable > config file
        for key_name, args_parser_value, env_var_name in [
            (KEY, ARGS_PARSER.key, YD_KEY),
            (SECRET, ARGS_PARSER.secret, YD_SECRET),
            (NAMESPACE, ARGS_PARSER.namespace, YD_NAMESPACE),
            (NAME_TAG, ARGS_PARSER.tag, YD_TAG),
            (URL, ARGS_PARSER.url, YD_URL),
        ]:
            if args_parser_value is not None:
                common_section[key_name] = args_parser_value
                print_log(f"Using '{key_name}' provided on command line")
            elif os.environ.get(env_var_name, None) is not None:
                common_section[key_name] = os.environ[env_var_name]
                print_log(
                    f"Using value of '{env_var_name}' environment variable "
                    f"for '{key_name}'"
                )

        url = substitute_variable_str(common_section.get(URL, DEFAULT_URL))
        if url != DEFAULT_URL:
            print_log(f"Using the YellowDog API at: {url}")

        # Exhaustive variable processing for common section variables
        # Note that add_substitutions() will perform all possible
        # substitutions for the items in its dictionary each time it's
        # called
        add_substitutions(subs={URL: url})
        key = substitute_variable_str(common_section[KEY])
        add_substitutions(subs={KEY: key})
        secret = substitute_variable_str(common_section[SECRET])
        add_substitutions(subs={SECRET: secret})
        namespace = substitute_variable_str(common_section[NAMESPACE])
        add_substitutions(subs={NAMESPACE: namespace})
        name_tag = substitute_variable_str(common_section[NAME_TAG])
        add_substitutions(subs={NAME_TAG: name_tag})

        return ConfigCommon(
            # Required
            key=key,
            secret=secret,
            namespace=namespace,
            name_tag=name_tag,
            # Optional
            url=url,
            use_pac=(
                True if ARGS_PARSER.use_pac else common_section.get(USE_PAC, False)
            ),
        )

    except KeyError as e:
        print_error(f"Missing configuration data: {e}")
        exit(1)


def import_toml(filename: str) -> Dict:
    print_log(f"Loading imported common configuration data from: '{filename}'")
    try:
        common_config: Dict = load_toml_file_with_variable_substitutions(filename)
        return common_config[COMMON_SECTION]
    except (FileNotFoundError, PermissionError, TomlDecodeError) as e:
        print_error(f"Unable to load imported common configuration data: {e}")
        exit(1)


def load_config_work_requirement() -> Optional[ConfigWorkRequirement]:
    """
    Load the configuration data for a Work Requirement
    """
    try:
        wr_section = CONFIG_TOML[WORK_REQUIREMENT_SECTION]
    except KeyError:
        return ConfigWorkRequirement()
    try:
        # Allow WORKER_TAG if WORKER_TAGS is empty
        worker_tags = wr_section.get(WORKER_TAGS, None)
        if worker_tags is None:
            try:
                worker_tags = [wr_section[WORKER_TAG]]
            except KeyError:
                pass
        if worker_tags is not None:
            check_list(worker_tags)
            for index, worker_tag in enumerate(worker_tags):
                worker_tags[index] = substitute_variable_str(worker_tag)

        wr_data_file = wr_section.get(WR_DATA, None)
        if wr_data_file is not None:
            check_str(wr_data_file)
            wr_data_file = substitute_variable_str(wr_data_file)
            wr_data_file = pathname_relative_to_config_file(wr_data_file)

        # Check for properties set on the command line
        executable = (
            check_str(wr_section.get(EXECUTABLE, wr_section.get(EXECUTABLE, None)))
            if ARGS_PARSER.executable is None
            else ARGS_PARSER.executable
        )
        executable = substitute_variable_str(executable)

        task_type = (
            wr_section.get(TASK_TYPE, wr_section.get(TASK_TYPE, None))
            if ARGS_PARSER.task_type is None
            else ARGS_PARSER.task_type
        )
        if task_type is not None:
            check_str(task_type)
            task_type = substitute_variable_str(task_type)

        csv_file = wr_section.get(CSV_FILE, None)
        csv_files = wr_section.get(CSV_FILES, None)
        if csv_file and csv_files:
            print_error("Only one of 'csvFile' and 'csvFiles' should be set")
            exit(1)
        if csv_file:
            csv_files = [csv_file]

        task_batch_size = (
            wr_section.get(TASK_BATCH_SIZE, TASK_BATCH_SIZE_DEFAULT)
            if ARGS_PARSER.task_batch_size is None
            else ARGS_PARSER.task_batch_size
        )

        return ConfigWorkRequirement(
            args=wr_section.get(ARGS, []),
            capture_taskoutput=wr_section.get(CAPTURE_TASKOUTPUT, True),
            completed_task_ttl=wr_section.get(COMPLETED_TASK_TTL, None),
            csv_files=csv_files,
            docker_env=wr_section.get(DOCKER_ENV, None),
            docker_password=wr_section.get(DOCKER_PASSWORD, None),
            docker_username=wr_section.get(DOCKER_USERNAME, None),
            env=wr_section.get(ENV, {}),
            exclusive_workers=wr_section.get(EXCLUSIVE_WORKERS, None),
            executable=executable,
            finish_if_all_tasks_finished=wr_section.get(
                FINISH_IF_ALL_TASKS_FINISHED, True
            ),
            finish_if_any_task_failed=wr_section.get(FINISH_IF_ANY_TASK_FAILED, False),
            flatten_input_paths=wr_section.get(FLATTEN_PATHS, None),
            flatten_upload_paths=wr_section.get(FLATTEN_UPLOAD_PATHS, None),
            fulfil_on_submit=wr_section.get(FULFIL_ON_SUBMIT, False),
            input_files=wr_section.get(INPUT_FILES, []),
            instance_types=wr_section.get(INSTANCE_TYPES, None),
            max_retries=wr_section.get(MAX_RETRIES, 0),
            max_workers=wr_section.get(MAX_WORKERS, None),
            min_workers=wr_section.get(MIN_WORKERS, None),
            optional_inputs=wr_section.get(INPUTS_OPTIONAL, []),
            output_files=wr_section.get(OUTPUT_FILES, []),
            output_files_required=wr_section.get(OUTPUT_FILES_REQUIRED, []),
            priority=wr_section.get(PRIORITY, 0.0),
            providers=wr_section.get(PROVIDERS, None),
            ram=wr_section.get(RAM, None),
            regions=wr_section.get(REGIONS, None),
            task_batch_size=task_batch_size,
            task_count=wr_section.get(TASK_COUNT, 1),
            task_data=wr_section.get(TASK_DATA, None),
            task_data_file=wr_section.get(TASK_DATA_FILE, None),
            task_group_name=wr_section.get(TASK_GROUP_NAME, None),
            task_name=wr_section.get(TASK_NAME, None),
            task_type=task_type,
            tasks_per_worker=wr_section.get(TASKS_PER_WORKER, None),
            upload_files=wr_section.get(UPLOAD_FILES, []),
            vcpus=wr_section.get(VCPUS, None),
            verify_at_start=wr_section.get(VERIFY_AT_START, []),
            verify_wait=wr_section.get(VERIFY_WAIT, []),
            worker_tags=worker_tags,
            wr_data_file=wr_data_file,
            wr_name=wr_section.get(WR_NAME, None),
        )
    except KeyError as e:
        print_error(f"Missing configuration data: {e}")
        exit(1)
    except Exception as e:
        print_error(f"{e}")
        exit(1)


def load_config_worker_pool() -> Optional[ConfigWorkerPool]:
    """
    Load the configuration data for a Worker Pool
    """
    try:
        wp_section = CONFIG_TOML[WORKER_POOL_SECTION]
    except KeyError:
        return ConfigWorkerPool()
    try:
        worker_tag = substitute_variable_str(wp_section.get(WORKER_TAG, None))
        worker_pool_data_file = substitute_variable_str(wp_section.get(WP_DATA, None))
        if worker_pool_data_file is not None:
            worker_pool_data_file = pathname_relative_to_config_file(
                worker_pool_data_file
            )

        return ConfigWorkerPool(
            compute_requirement_batch_size=wp_section.get(
                COMPUTE_REQUIREMENT_BATCH_SIZE, CR_BATCH_SIZE_DEFAULT
            ),
            idle_node_shutdown_enabled=wp_section.get(IDLE_NODE_SHUTDOWN_ENABLED, True),
            idle_node_shutdown_timeout=wp_section.get(IDLE_NODE_SHUTDOWN_TIMEOUT, 5.0),
            idle_pool_shutdown_enabled=wp_section.get(IDLE_POOL_SHUTDOWN_ENABLED, True),
            idle_pool_shutdown_timeout=wp_section.get(IDLE_POOL_SHUTDOWN_TIMEOUT, 30.0),
            images_id=wp_section.get(IMAGES_ID, None),
            instance_tags=wp_section.get(INSTANCE_TAGS, None),
            maintainInstanceCount=wp_section.get(MAINTAIN_INSTANCE_COUNT, False),
            max_nodes=wp_section.get(
                MAX_NODES, max(1, wp_section.get(TARGET_INSTANCE_COUNT, 1))
            ),
            max_nodes_set=(False if wp_section.get(MAX_NODES) is None else True),
            min_nodes=wp_section.get(MIN_NODES, 0),
            min_nodes_set=(False if wp_section.get(MIN_NODES) is None else True),
            name=substitute_variable_str(
                wp_section.get(WP_NAME, None),
            ),
            node_boot_timeout=wp_section.get(NODE_BOOT_TIMEOUT, 10.0),
            target_instance_count=wp_section.get(TARGET_INSTANCE_COUNT, 1),
            target_instance_count_set=(
                False if wp_section.get(TARGET_INSTANCE_COUNT) is None else True
            ),
            template_id=wp_section.get(TEMPLATE_ID, None),
            user_data=wp_section.get(USERDATA, None),
            user_data_file=wp_section.get(USERDATAFILE, None),
            user_data_files=wp_section.get(USERDATAFILES, None),
            worker_pool_data_file=worker_pool_data_file,
            worker_tag=worker_tag,
            workers_per_vcpu=wp_section.get(WORKERS_PER_VCPU, None),
            workers_per_node=wp_section.get(WORKERS_PER_NODE, 1),
        )

    except KeyError as e:
        print_error(f"Missing configuration data: {e}")
        exit(1)


def generate_id(prefix: str, max_length: int = 60) -> str:
    """
    Adds a combination of a UTC timestamp plus
    a few random hex characters. Checks length.
    """
    generated_id = (
        prefix + UTCNOW.strftime("_%y%m%d-%H%M%S-") + str(uuid4())[:3].lower()
    )
    if len(generated_id) > max_length:
        print_error(
            f"Error: Generated ID '{generated_id}' would exceed "
            f"maximum length ({max_length})"
        )
        exit(1)
    return generated_id


def pathname_relative_to_config_file(file: str) -> str:
    """
    Find the pathname of a file relative to the location
    of the config file
    """
    return normpath(relpath(join(CONFIG_FILE_DIR, file)))


# Utility functions for creating links to YD entities
def link_entity(base_url: str, entity: object) -> str:
    entity_type = type(entity)
    return link(
        base_url,
        "#/%s/%s" % ((entities.get(entity_type)), entity.id),
        camel_case_split(entity_type.__name__).upper(),
    )


def link(base_url: str, url_suffix: str = "", text: Optional[str] = None) -> str:
    url_parts = urlparse(base_url)
    base_url = url_parts.scheme + "://" + url_parts.netloc
    url = base_url + "/" + url_suffix
    if not text:
        text = url
    if text == url:
        return url
    else:
        return "%s (%s)" % (text, url)


def camel_case_split(value: str) -> str:
    return " ".join(re.findall(r"[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))", value))


entities = {
    ConfiguredWorkerPool: "workers",
    ProvisionedWorkerPool: "workers",
    WorkRequirement: "work",
    ComputeRequirement: "compute",
}


def update_config_work_requirement(config_wr: ConfigWorkRequirement):
    """
    Update a ConfigWorkRequirement Object with the current dictionary of
    variable substitutions. Returns the updated object.
    """
    config_wr_str_processed = substitute_variable_str(str(config_wr))
    # Note: 'literal_eval' doesn't work here
    return eval(config_wr_str_processed)


def unpack_namespace_in_prefix(namespace: str, prefix: str) -> (str, str):
    """
    Allow the prefix to include the namespace. Return the unpacked
    namespace, prefix.
    """
    elems = prefix.split(NAMESPACE_SEPARATOR)
    if len(elems) == 1:
        return namespace, prefix.lstrip("/")
    if len(elems) == 2:
        return elems[0] if elems[0] != "" else namespace, elems[1].lstrip("/")
