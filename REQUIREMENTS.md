# Requirements

# Functional Requirements

## Core execution model

* **\[FR-F-CEM-01]** Define workflows as directed acyclic graphs (DAGs) of discrete tasks with explicit dependency edges.
* **\[FR-F-CEM-02]** Execute tasks in dependency order, respecting fan-out and fan-in.
* **\[FR-F-CEM-03]** Support parallel execution of independent tasks up to a configurable concurrency limit.
* **\[FR-F-CEM-04]** Enforce task-level and DAG-level timeouts, terminating hung processes cleanly.
* **\[FR-F-CEM-05]** Support task prioritisation via configurable priority queues.
* **\[FR-F-CEM-06]** Execute pipelines against arbitrary historical dates (backfill), producing results identical to those of a live run on that date.
* **\[FR-F-CEM-07]** Guarantee idempotent task execution: re-running a task with the same inputs and the same logical date produces the same outputs with known side-effects, and if not (in the event of data collection) throw a warning.

## Scheduling and triggering

* **\[FR-F-ST-01]** Trigger pipeline runs on CRON expressions with minute resolution. If the scheduler is offline, then missed executions are scheduled to run on restart with configurable catch up limits.
* **\[FR-F-ST-02]** Trigger pipeline runs on external events via an API webhook that other integrations plug into. Missed API webhook queries are not logged if the scheduler is offline.
* **\[FR-F-ST-03]** Allow manual ad-hoc execution of any pipeline with arbitrary runtime parameters, from the UI and from the CLI
* **\[FR-F-ST-04]** Support parameterised pipelines where any value in the DAG definition can be overridden at trigger time. This is satisfied by allowing workflows to be triggered with a parameterised model. 

## Core Execution Model

* **\[FR-C-CEM-01]Cross language workflow definitions**: Tasks are language agnostic definitions, defined as pure functions in Python, Go, Zig, etc. When building workflows, tasks registered with the core orchestrator can be referenced locally, regardless of their language of implementation.
* **\[FR-C-CEM-02]Task workflow separation**: Tasks can be registered independently to workflows. This in effect leaves them 'dangling' ready to be adopted by a workflow in the future.

## Data handling

* **\[FR-C-DH-01]Typed data contracts at every task boundary.** Each task declares the schema of its input and output. This should be used to enforce correctness at **registration** time with the orchestrator. During runtime, the orchestrator validates data against the registered input/output schemas before execution begins. Schema violations halt the run and report the violating field, not a generic downstream error.
* **\[FR-C-DH-02]Native in-memory object passing between tasks.** Any object of any size can be passed from one task to the next without manual serialisation. For tasks running in the same thread, the object can be made available in memory. For tasks not operating on the same thread, a storage backend can be configured (S3, GCS, Azure Blob, File). They are referenced by a clean API only. The schema of these objects is enforced and lifecycle configurations can be attached to them.
* **\[FR-C-DH-03]Lookback**. Tasks should be able to depend on the result of past results of the task, filtering for matches like specific IDs, time ranges, counts, etc.

## Scheduling and Triggering

* **\[FR-C-ST-01]Task based Triggering of Workflows.** Tasks can trigger other workflows through triggering events like connection to the webhook. This is explicit and is a registered side effect of the task.

## Migration and ecosystem

* **\[FR-C-ME-01]Native Airflow DAG import.** Existing Airflow DAGs can be mapped to the Orca pattern in one day, allowing teams to migrate incrementally; there is no forced cut-over.

# Non-Functional Requirements

## Reliability and resilience

* **\[NFR-F-RR-01]** Retry failed tasks automatically with configurable attempt count and exponential backoff
* **\[NFR-F-RR-02]** Continue executing independent branches of a DAG when one branch fails, unless explicit halt-on-failure is configured
* **\[NFR-F-RR-03]** Persist execution state durably so that a scheduler or worker crash does not lose the DAG execution state. Workflows are resumed on restart. Workflows where blob data is lost from in-memory runs are not restarted.
* **\[NFR-F-RR-04]** Provide high availability for the scheduler via active-passive or active-active failover with no manual intervention
* **\[NFR-F-RR-05]** Enforce SLA deadlines per task and per DAG, emitting alerts when a deadline is missed before downstream consumers are affected

## Security and governance

* **\[NFR-F-SG-01]** Role-based access control (RBAC) with at minimum: admin, editor, viewer, and auditor roles, scoped to individual pipelines or to pipeline groups
* **\[NFR-F-SG-02]** Secrets are never stored in pipeline code or in plain text. A secrets backend (Vault, AWS Secrets Manager, GCP Secret Manager) is the only supported storage for credentials
* **\[NFR-F-SG-03]** All user actions - trigger, pause, delete, edit, manual retry - are written to an immutable audit log with timestamp, actor identity, and parameters
* **\[NFR-F-SG-04]** Multi-tenancy: teams or projects are isolated such that one team cannot view, trigger, or modify another team's pipelines without explicit grant
* **\[NFR-F-SG-05]** Support for pipeline promotion across environments (dev -> staging -> production) without code changes, using environment-scoped configuration
* **\[NFR-F-SG-06]** Workspace should be tied to a git repository

## Developer Experience

* **\[NFR-C-DX-01]Low framework intrusion.** A valid task is a plain Python/Go/Zig function, with a specific interface definition. A valid workflow is an annotated composition of these functions. No framework base classes, no operator inheritance, no context objects are required to author or test a pipeline. The control flow needs to be obvious.
* **\[NFR-C-DX-02]Stubbed Remote Tasks.** Tasks registered with the core orchestrator that are implemented in another programming language are stubbed locally so that the local workflow definition can be built in a fully type safe manner.
* **\[NFR-C-DX-03]Single API surface.** Every configuration parameter (retries, caching, concurrency limits, SLA) is an optional keyword argument on the function definitions rather than a new abstraction.
* **\[NFR-C-DX-04]Independent unit testability.** Every task is directly callable as a Python function in a test suite. No running scheduler, no mocked framework context, and no test-specific plumbing is required. A full CI pipeline runs without a live orchestrator instance.

## Debugging and Observability

* **\[NFR-C-DO-01]One-command local replay of any historical task run.** Given a run ID and a task ID, the CLI reconstructs the exact inputs, parameters, and environment of that execution and runs it locally, including attaching a debugger. Production failures are reproducible on a laptop.
* **\[NFR-C-DO-02]Task result lineage**. Task results are tied to the task version which is tied to the version control. The construction of all datasets by virtue of tasks results can be traced back to the exact version of software.
* **\[NFR-C-DO-03]Cost attribution per task per run.** Compute cost (CPU-seconds, memory-GiB-seconds) are recorded per task execution and displayed alongside duration and status in the UI. Budget limits and cost anomaly alerts are configurable per pipeline.

## UI and interface

* **\[NFR-C-UI-01]The DAG graph is the permanent primary view.** It cannot be replaced or made secondary by any product update. The graph shows task status, execution time, data dependencies, and cost in a single view. Aesthetic additions are opt-in overlays.
* **\[NFR-C-UI-02]All data dependencies are visible as graph edges.** No implicit or hidden task coupling exists. Side-effects (such as workflow triggering from within a DAG) is visible as an edge to another graph. The graph is a complete and accurate model of execution; nothing discoverable only by reading source code.

## Data Handling

* **\[NFR-C-DH-01]The database of past results can be queried within a task using a simple API.** This result should be prepared for the task ahead of execution and passed in with the result of the previous task.

## Infrastructure and operations

* **\[NFR-C-IO-01]Stateless, horizontally scaleble workers.** Worker capacity scales by adding instances; no configuration change is required. The scheduler has no single-process throughput bottleneck. A 10x increase in DAG volume requires only more worker instances.
* **\[NFR-C-IO-02]Single-image deployment.** A fully functional production worker runs from one Docker image with one command. No separate metadata database configuration is required to reach a working state. Time-to-first-run for a new deployment is under 10 minutes.
* **\[NFR-C-IO-03]Host in my own cloud (or not).** The solution should run on some basic primitives (PostgreSQL, blob storage, secrets, stateless functions), and so I should be able to easily deploy in my cloud, if I choose not to use the hosted service.

## Pricing

* **\[NFR-C-PR-01]No per-task, per-run, or per-execution-minute pricing component.** At no point does a pricing signal incentivise an engineer to make a pipeline less modular or to combine steps that should be separate. Pricing, instead should be tied to the gross cost to running the solution. If hosting in your own cloud, then a flat monthly cost is all thats need to cover the cost of the product. Extra users incur a very marginal cost, as more users means more app complexity.
* **\[NFR-C-PR-02]Open-source execution engine.** The core scheduler, worker runtime(s), and DAG execution layer are open-source under a permissive or copyleft licence. They are never placed behind a commercial paywall. Pricing changes to commercial add-ons are announced with a minimum 12-month notice period.

## Toolboxes

* **\[NFR-C-TB-01]** Toolboxes should be provided on a license basis. These offer contained units of functionality as a task. Running in the customers cloud or hosted - offers discrete value.
