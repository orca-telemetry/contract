# README

Herein is the description of the API design / contract for the orca core
service, and for workers.

# Core Service

These are all the remote procedure calls that should sit under the core service.

## RegisterCodebaseSnapshot

This service takes a snapshot of the codebase and registers all the assets
stored within it.

All datafunctions, tasks, and workflows are registered via this RPC. The call is
idempotent on git commit has and codebase name.

### Request Message

* **WorkerName**: The name of the worker that implements the assets. Globally unique.
* **GitCommitHash**: The current git commit of codebase.
* **MD5**: An MD5 hash performed on the combination of DataFunctions, Tasks, and
    workflows. Used to check integrity server side and as a lookup index for contacting
    the worker when the worker notifies of it's readiness to serve.
* **DataFunctions**: An array of data functions
* **Tasks**: An array of tasks
* **Workflows**: An array of workflows
* **URL**: A connection URL that should be used to contact this worker.

### Response Message
* **Status**: Success | Failure 
* **Message**: A message detailing the failure (if at all)

### Models

The RPC validates the asset in dependency order: Data functions -> Tasks ->
Workflows. The data models for each are defined below:

#### DataFunction
* **Name**: A globally unique name for the data function, if
conflicting name is detected on the server, a conflict is raised 
* **Hash**: A hash of the AST segment that defines the data function
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

#### Task

* **TaskHash**: the hash of the AST segment corresponding to the task function
* **Name**: the task name
* **Description**: the task description
* **ExecutionSettings**: settings governing the execution:
  * **ExecutionTimeout**: the timeout that should be applied to executing the
  task
  * **RetryCount**: How many times the task should be retried on
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

#### Workflow
* **WorkflowName**: A unique string identifier for the workflow. This is a
    globally unique definition of the workflow.
* **Description**: A textual explanation of the workflow's purpose.
* **WorkflowHash**: A hash of the workflow structure, factoring in the tasks,
    dependencies, and execution models.
* **Edges**: An array of task dependencies in the workflow.
* **ExecutionSettings**: A dictionary map of pipeline configuration parameters
    that define how a workflow runs:
  * **PriorityQueue**: definition of tasks that should take priority over other
  tasks in parallel execution
  * **ConcurrencyLimit**: a limit on the number of tasks that should be executed
  in parallel at any moment in time
* **InputModel**: A marshalled JSON schema stating the model of the execution
parameters that should be provided at runtime.
* **HaltOnFailure**: A flag that states whether parallel execution of tasks
should be stopped if a task suffers a failure.

## RegisterServingStatus

This RPC notifies the core orchestrator of service status. It registers with an
MD5 hash that that would have been indexed at snapshot registration time.

### Request Message

* **Name**: The name of the worker.
* **MD5**: The MD5 hash of the workers state, including data functions, tasks,
    and workflows, and worker name. Does not factor in the git commit state.
* **ConnectionUrl**: The connection URL of the worker. This must be the gRPC URL
    that the core orchestrator must contact to request processing.
* **IsServing**: True | False - whether the worker is serving requests.

### Response Message

The main failure mode of this endpoint is if the worker has not registered
prior.

* **Status**: Successful | Failed
* **Message**: Message on why it failed

## TriggerWorkflow

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

## ExposeState

An RPC that exposes the inner (current) state of the orchestration stack. Used by CLI
tooling to build stubs locally that represent the remote state of tasks and
workflows.

### Request Message
- **GitCommitHash**: The git commit hash to generate the state for. If omitted, provides the latest state. Take priority over timestamp.
- **Timestamp**: A timestamp that can be provided to capture the state from. The
  closest commit to this timestamp will be used.
- **Repository**: A repository to filter against. If provided, all assets
(Tasks, Workflows, DataFunctions etc.) registered in this repository will be
omitted from the response to this RPC.

### Response Message
- **Tasks**: An array of tasks.
- **Workflows**: An array of workflows, and their references to tasks.
- **DataFunctions**: An array of data functions.

## QueryTaskResult

An RPC that queries past task results. Uses Conjunctive Normal Form to construct
queries to give the user _enough_ flexibility whilst also remaining
maintainable. Results are streamed back to the worker.

### RequestMessage

- **Name**: The name of the task to return results for.
- **ExecutionParameterFilters**: A list of `FilterGroup` objects applied to
  the execution parameters. Groups are evaluated with AND between them. If
  omitted, no filtering is applied to execution parameters.
- **ResultFilters**: A list of `FilterGroup` objects applied to the task
  result. Groups are evaluated with AND between them. If omitted, no filtering
  is applied to results.
- **OrderBy**: A list of statements that defines how results should be sorted.
    - **Key**: The key to sort by.
    - **Source**: Whether the key belongs to `RESULT` or
      `EXECUTION_PARAMETERS`.
    - **Direction**: The sort direction. One of: `ASC`, `DESC`.
- **ResultFields**: An optional list of keys to return from the result object.
  If omitted, the full result is returned. If specified, only the listed keys
  will be included in each result's `Result` payload.
- **PageSize**: The maximum number of results to return. Required.
- **PageToken**: An opaque token returned by a previous response used to fetch
  the next page. Omit on the first request.

### ResponseMessage

- **Results**: An array of task results:
    - **Name**: The name of the task.
    - **ExecutionParameters**: The parameters that executed the workflow the
      task belongs to, as a marshalled JSON string.
    - **Result**: The task result, as a marshalled JSON string. If
      `ResultFields` was specified in the request, only those fields will be
      present.
- **NextPageToken**: An opaque token to pass as `PageToken` in a subsequent
  request to retrieve the next page. Absent if there are no further results.

### Supporting Types

#### FilterGroup

A set of conditions joined by OR. At least one condition must be satisfied for
the group to pass. All `FilterGroup` objects in a list are AND-ed together.

- **Filters**: A non-empty list of `LeafFilter` objects. At least one must
  match for this group to be satisfied.

#### LeafFilter

A single condition evaluated against one KV pair.

- **Key**: The key to filter on.
- **Comparator**: The comparison operation to apply. One of:
    - `EQ` - equal to
    - `NEQ` - not equal to
    - `GT` - greater than
    - `GTE` - greater than or equal to
    - `LT` - less than
    - `LTE` - less than or equal to
    - `IN` - value is one of a set
    - `NOT_IN` - value is not any of a set
    - `EXISTS` - the key is present (no `Value` required)
    - `NOT_EXISTS` - the key is absent (no `Value` required)
    - `CONTAINS` - value contains the given substring
    - `PREFIX` - value starts with the given string
- **Value**: The value to compare against. For `IN` and `NOT_IN`, this is a
  list of strings. For `EXISTS` and `NOT_EXISTS`, this field is omitted. For
  all other comparators, this is a single string.

### Examples

#### Simple equality filter

```json
{
  "Name": "image-resize",
  "ExecutionParameterFilters": [
    {
      "Filters": [
        { "Key": "environment", "Comparator": "EQ", "Value": "production" }
      ]
    }
  ],
  "ResultFilters": [
    {
      "Filters": [
        { "Key": "status", "Comparator": "EQ", "Value": "success" }
      ]
    }
  ],
  "PageSize": 25
}
```

#### Compound CNF filter

Matches tasks where:
- `environment` is `production` OR `staging`, AND
- `region` is `us-east-1` OR `eu-west-1`, AND
- `status` is `success`, AND
- `duration_ms` is at most `3000`

```json
{
  "Name": "image-resize",
  "ExecutionParameterFilters": [
    {
      "Filters": [
        { "Key": "environment", "Comparator": "EQ", "Value": "production" },
        { "Key": "environment", "Comparator": "EQ", "Value": "staging" }
      ]
    },
    {
      "Filters": [
        { "Key": "region", "Comparator": "EQ", "Value": "us-east-1" },
        { "Key": "region", "Comparator": "EQ", "Value": "eu-west-1" }
      ]
    }
  ],
  "ResultFilters": [
    {
      "Filters": [
        { "Key": "status", "Comparator": "EQ", "Value": "success" }
      ]
    },
    {
      "Filters": [
        { "Key": "duration_ms", "Comparator": "LTE", "Value": "3000" }
      ]
    }
  ],
  "OrderBy": { "Key": "duration_ms", "Source": "RESULT", "Direction": "ASC" },
  "ResultFields": ["status", "duration_ms", "output_url"],
  "PageSize": 10
}
```

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
* **ExecutionParameters**:JSON of the workflow execution parameters.
* **DataURI**: Optional URI that provides the task a location to where the
required data (as per the data function) was stored. This URI can be queried v
* **Tasks**: An array of the tasks to execute for this workflow segment.

### Response Message
* **Status**: Successful | Failed
* **Message**: An error message to raise if failed
