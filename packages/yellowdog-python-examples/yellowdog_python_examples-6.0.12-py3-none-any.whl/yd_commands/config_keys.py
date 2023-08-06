"""
Configuration key strings
"""

ARGS = "arguments"  # List
CAPTURE_TASKOUTPUT = "captureTaskOutput"  # Bool
COMMON_SECTION = "common"  # No value
COMPLETED_TASK_TTL = "completedTaskTtl"  # Float
COMPUTE_REQUIREMENT_BATCH_SIZE = "computeRequirementBatchSize"  # Integer
CSV_FILE = "csvFile"  # String
CSV_FILES = "csvFiles"  # List of Strings
DEPENDENT_ON = "dependentOn"  # String
DOCKER_ENV = "dockerEnvironment"  # Dictionary
DOCKER_PASSWORD = "dockerPassword"  # String
DOCKER_USERNAME = "dockerUsername"  # String
ENV = "environment"  # Dictionary
EXCLUSIVE_WORKERS = "exclusiveWorkers"  # Boolean
EXECUTABLE = "executable"  # String
FINISH_IF_ALL_TASKS_FINISHED = "finishIfAllTasksFinished"  # Boolean
FINISH_IF_ANY_TASK_FAILED = "finishIfAnyTaskFailed"  # Boolean
FLATTEN_PATHS = "flattenInputPaths"  # Boolean
FLATTEN_UPLOAD_PATHS = "flattenUploadPaths"  # Boolean
FULFIL_ON_SUBMIT = "fulfilOnSubmit"  # Boolean
IDLE_NODE_SHUTDOWN_ENABLED = "idleNodeShutdownEnabled"  # Bool
IDLE_NODE_SHUTDOWN_TIMEOUT = "idleNodeShutdownTimeout"  # Float
IDLE_POOL_SHUTDOWN_ENABLED = "idlePoolShutdownEnabled"  # Bool
IDLE_POOL_SHUTDOWN_TIMEOUT = "idlePoolShutdownTimeout"  # Float
IMAGES_ID = "imagesId"  # String
IMPORT = "import"  # String
INPUT_FILES = "inputs"  # List of Strings
INPUTS_OPTIONAL = "inputsOptional"  # List of Strings
INSTANCE_TAGS = "instanceTags"  # List of Strings
INSTANCE_TYPES = "instanceTypes"  # List of Strings
KEY = "key"  # String
MAINTAIN_INSTANCE_COUNT = "maintainInstanceCount"  # Bool
MAX_NODES = "maxNodes"  # Integer
MAX_RETRIES = "maximumTaskRetries"  # Integer
MAX_WORKERS = "maxWorkers"  # Integer
MIN_NODES = "minNodes"  # Integer
MIN_WORKERS = "minWorkers"  # Integer
NAME = "name"  # String
NAMESPACE = "namespace"  # String
NAME_TAG = "tag"  # String
NODE_BOOT_TIMEOUT = "nodeBootTimeout"  # Float
OUTPUT_FILES = "outputs"  # List of Strings
OUTPUT_FILES_REQUIRED = "outputsRequired"  # List of Strings
PRIORITY = "priority"  # Float
PROVIDERS = "providers"  # List of Strings
RAM = "ram"  # List of two Floats
REGIONS = "regions"  # List of Strings
SECRET = "secret"  # String
TARGET_INSTANCE_COUNT = "targetInstanceCount"  # Integer
TASKS = "tasks"  # List of Tasks
TASK_BATCH_SIZE = "taskBatchSize"  # Integer
TASKS_PER_WORKER = "tasksPerWorker"  # Integer
TASK_COUNT = "taskCount"  # Integer
TASK_DATA = "taskData"  # String
TASK_DATA_FILE = "taskDataFile"  # String
TASK_GROUPS = "taskGroups"  # List of Task Groups
TASK_GROUP_NAME = "taskGroupName"  # String
TASK_NAME = "taskName"  # String
TASK_TYPE = "taskType"  # String
TASK_TYPES = "taskTypes"  # List of Strings
TEMPLATE_ID = "templateId"  # String
UPLOAD_FILES = "uploadFiles"  # List of Dicts
LOCAL_PATH = "localPath"  # String
UPLOAD_PATH = "uploadPath"  # String
URL = "url"  # String
USE_PAC = "usePAC"  # Boolean
USERDATA = "userData"  # String
USERDATAFILE = "userDataFile"  # String
USERDATAFILES = "userDataFiles"  # List of Strings
VARIABLES = "variables"  # Dictionary
VCPUS = "vcpus"  # List of two Floats
VERIFY_AT_START = "verifyAtStart"  # List of Strings
VERIFY_WAIT = "verifyWait"  # List of Strings
WORKERS_PER_VCPU = "workersPerVCPU"  # Integer
WORKERS_PER_NODE = "workersPerNode"  # Integer
WORKER_POOL_SECTION = "workerPool"  # No value
WORKER_TAG = "workerTag"  # String
WORKER_TAGS = "workerTags"  # List of Strings
WORK_REQUIREMENT_SECTION = "workRequirement"  # No value
WP_DATA = "workerPoolData"  # String
WP_NAME = "name"  # String
WR_DATA = "workRequirementData"  # String
WR_NAME = "name"  # String

ALL_KEYS = [
    ARGS,
    CAPTURE_TASKOUTPUT,
    COMMON_SECTION,
    COMPLETED_TASK_TTL,
    COMPUTE_REQUIREMENT_BATCH_SIZE,
    CSV_FILE,
    CSV_FILES,
    DEPENDENT_ON,
    DOCKER_ENV,
    DOCKER_PASSWORD,
    DOCKER_USERNAME,
    ENV,
    EXCLUSIVE_WORKERS,
    EXECUTABLE,
    FINISH_IF_ALL_TASKS_FINISHED,
    FINISH_IF_ANY_TASK_FAILED,
    FLATTEN_PATHS,
    FLATTEN_UPLOAD_PATHS,
    FULFIL_ON_SUBMIT,
    IDLE_NODE_SHUTDOWN_ENABLED,
    IDLE_NODE_SHUTDOWN_TIMEOUT,
    IDLE_POOL_SHUTDOWN_ENABLED,
    IDLE_POOL_SHUTDOWN_TIMEOUT,
    IMAGES_ID,
    IMPORT,
    INPUT_FILES,
    INPUTS_OPTIONAL,
    INSTANCE_TAGS,
    INSTANCE_TYPES,
    KEY,
    MAINTAIN_INSTANCE_COUNT,
    MAX_NODES,
    MAX_RETRIES,
    MAX_WORKERS,
    MIN_NODES,
    MIN_WORKERS,
    NAMESPACE,
    NAME_TAG,
    NODE_BOOT_TIMEOUT,
    OUTPUT_FILES,
    OUTPUT_FILES_REQUIRED,
    PRIORITY,
    PROVIDERS,
    RAM,
    REGIONS,
    SECRET,
    TARGET_INSTANCE_COUNT,
    TASKS,
    TASK_BATCH_SIZE,
    TASKS_PER_WORKER,
    TASK_COUNT,
    TASK_DATA,
    TASK_DATA_FILE,
    TASK_GROUPS,
    TASK_GROUP_NAME,
    TASK_NAME,
    TASK_TYPE,
    TASK_TYPES,
    TEMPLATE_ID,
    UPLOAD_FILES,
    LOCAL_PATH,
    UPLOAD_PATH,
    URL,
    USE_PAC,
    USERDATA,
    USERDATAFILE,
    USERDATAFILES,
    VARIABLES,
    VCPUS,
    VERIFY_AT_START,
    VERIFY_WAIT,
    WORKERS_PER_VCPU,
    WORKERS_PER_NODE,
    WORKER_POOL_SECTION,
    WORKER_TAG,
    WORKER_TAGS,
    WORK_REQUIREMENT_SECTION,
    WP_DATA,
    WP_NAME,
    WR_DATA,
    WR_NAME,
]
