# API Design

# Core Service

These are all the remote procedure calls that should sit under the core service.

## RegisterDataFunction

This is a service that registers a function that produces some data. This data
is stored ephemerally ready to be accessed by tasks.

**gRPC Mode**: Unary request/response

### Request Message

* **DataFunctionName**: A globally unique name for the data function, if
conflicting name is detected on the server, a conflict is raised 
* **DataFunctionHash**: A hash of the AST segment that defines the data function
* **GitCommitHash**: The hash of the latest git commit
* **InputModel**:**&#x20;**&#x41; marshalled JSON schema of the accepted input
model. This model must be satisfied by the execution model of the workflow that
owns the task.
* **OutputModel**: A marshalled JSON schema that defines a single record of the
output of the data function. The data function should produce an array of this
schema that is streamed to the orchestrator for caching. The schema is validated
once at retrieval time. 
* **Settings**: settings related to the data produced by this data function,
such as:
  * **TTL**: 0=clean up immediately after DAG execution of all tasks that depend
  on it. >0 = live time in seconds
  * **Timeout**: A timeout for the lifecyle of the data function

### Response Message

* **Status**: Successful | Failed
* **Message**:**&#x20;**&#x41; message as to why the data function registration
failed

## RegisterTask

An RPC that allows the registration of a task with the core orchestrator.

**gRPC** **Mode**: Unary request/response

### Request Message

* **TaskHash**: the hash of the AST segment corresponding to the task function
* **Name**: the task name
* **Description**: the task description
* **GitCommitHash**:**&#x20;**&#x74;he hash of the current git command (inferred
directly from the local .git folder if present)
* **ExecutionSettings**: settings governing the execution:
  * **ExecutionTimeout**: the timeout that should be applied to executing the
  task
  * **RetryCount:&#x20;**&#x68;ow many times the task should be retried on
  failure
  * **BackoffStrategy**: linear | exponential
  * **Deadline**: A deadline that is used as an SLA value. If this deadline is
  exceeded then an alert is raised on the execution status of this task.
* **InputModel**: a marshalled json schema that follows the JSON Schema
Standard. The validation and pointers extension of the json schema are not
enforced at registration time or runtime, though may be supported
* **OutputModel**: a marshalled json schema that follows the JSON Schema
Standard. The validation and pointers extension of the json schema are not
enforced at registration time or runtime, though may be supported
* **RequiredDataFunctions**: An array of all of the required data functions that
this task requires.

### Response Message

* **Status**: Successful | Failed
* **Message**: A message as to why the task registration failed

## RegisterWorkflow

A service that allows the creation of a workflow referencing previously
registered tasks.

**gRPC Mode**: Unary request/response

### Request Message

* **WorkflowName**: A unique string identifier for the workflow. This is a
globally unique definition of the workflow.
* **Description**: A textual explanation of the workflow's purpose.
* **GitCommitHash**: The current version control commit hash matching the
deployment workspace state.
* **WorkflowHash**: A hash of the workflow structure, factoring in the tasks,
dependencies, and execution models.
* **Tasks**: A list of structural identifiers linking to independent,
pre-registered tasks (including local stubs of cross-language definitions).
* **Edges**: A list of dependencies between workflows.
* **ExecutionSettings**: A dictionary map of pipeline configuration parameters
that define how a workflow runs:
  * **PriorityQueue**: definition of tasks that should take priority over other
  tasks in parallel execution
  * **ConcurrencyLimit**: a limit on the number of tasks that should be executed
  in parallel at any moment in time
* **ExectionParametersModel:&#x20;**&#x41; marshalled JSON schema stating the
model of the execution parameters that should be provided at runtime.
* **HaltOnFailure**: A flag that states whether parallel execution of tasks
should be stopped if a task suffers a failure.
* **ConnectionUrl**: The URL of the gRPC server that exposes the workflow. This
must match the local or cloud implementation - it is what the core orchestrator
'sees'

### Response Message

* **Status**: Successful | Failed
* **Message**: Details of the DAG validation errors (e.g. cyclic dependencies)

### TriggerWorkflow

A service that initiates a single execution run of a defined workflow DAG,
managing execution schedules, webhooks, or explicit user interventions.

**gRPC Mode**: Unary request/response

### Request Message

* **WorkflowName**: The target workflow to execute, identified by its name.
* **LogicalDate**: The target execution timestamp. If null, then execution is
immediate.
* **ExecutionParameters**: A marshalled JSON struct of execution parameters that
are provided to the workflow, as per the workflow schema.
* **TriggerSource**: An enum denoting the origin of the event: CRON | Webhook |
UI | CLI.

### Response Message

* **WorkflowRunID**: A unique runtime execution tracker string generated by the
orchestrator core.
* **Status**: Accepted | Rejected
* **Message**: Information regarding parameter or trigger validation failures.

## QueryPastResults (Lookback API)

A data discovery service allowing worker execution runtimes or the orchestrator
core to look up historical output states derived from past executions.

**gRPC Mode**: Unary request/response

### Request Message

* **TaskName**: The name of the target task execution records being isolated.
* **LookbackFilters**: Target data filtering parameters including matching
entity IDs, historical time boundaries, and record count thresholds.

### Response Message

* **PastResults**: A list of past payload data contexts paired with their
respective logical run dates and provenance metadata.

## RegisterDataFunctionCompletion

An RPC that registers that a data function has completed.

**gRPC Mode**: Unary request/response

### Request Message

* **WorkflowRunID**: ID of the workflow run that requested the data function
* **Status**: Successful | Failed
* **Message**: A message provided by the client if it failed, and a stack trace
  if possible.

### Response Message

## RegisterTaskResult

A RPC that workers call to register the result of a task.

**gRPC Mode**: Unary request/Response

### Request Message

* **WorkflowRunID**: The ID of the workflow run
* **TaskName**: The name of the task in the workflow
* **Result**: The result data as a marshalled JSON object. Validated on
retrieval.
* **Status**: Successful | Failed
* **Message**: The message produced by the worker if the task failed (ideally
full stack trace)
* **ComputeMetrics**: A structured measurement block containing total
CPU-seconds and memory-GiB-seconds expended for this task.

### Response Message

# Worker Services

This defines the RPCs that should be implemented by the client worker services.

## ExecuteDataFunction

An RPC that executes a data function registered with the worker. The worker is
provided with a URI to stream data into.

**gRPC Mode**: Unary request / response

### Request Message

* **ExecutionParameters**: A JSON of execution parameters that follows the model
  expected by the data function.
* **WorkflowRunID**: The ID of the Workflow that required the data function
* **URI**: A URI for the data function to stream the data to

### Response Message

* **Status**: Succeeded | Failed
* **Message**: A message as to why the data function failed to start

## ExecuteWorkflowSegment

An RPC that executes a segment of a workflow, if not all. As tasks are executed
within the workflow, the results are streamed back to the orchestrator. If
Execution fails at any point, in a handled manner, a message is sent back that
states the failure. Continuation rules are followed on the core side. If it
fails in an unhandled manner (i.e. the application crashes and the connection
breaks), then a [keep alive
configuration](https://grpc.github.io/grpc/core/md_doc_keepalive.html) will
detect this and the core attempts to access the worker again, starting where it
left of with the configured backoff. Each retrieval of a task result is logged
in the database as an execution step completed.

**gRPC Mode**: Unary request/response 

### Request Message

* **WorkflowRunId**: The ID generated by the core that denotes the specific
workflow run.
* **ExecutionParameters**:**&#x20;**&#x4A;SON of the workflow execution
parameters.
* **DataURI**: Optional URI that provides the task a location to where the
required data (as per the data function) was stored. This URI can be queried v
* **Tasks**: An array of the tasks to execute for this workflow segment.

### Response Message
* **Status**: Successful | Failed
* **Message**: An error message to raise if failed
