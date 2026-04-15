# Contract

Protobuf definitions and auto-generated gRPC stubs for the Orca distributed
processing system. This repo is the source of truth for service contracts across
all language implementations.

## Overview

Orca is a DAG-based algorithm orchestration system for distributed time-windowed
data processing. This repo contains:

- `service.proto` - canonical service and message definitions
- `vendor/validate.proto` - buf.build protovalidate rules
- `go/`, `python/`, `nodejs/` - auto-generated code (do not edit)

## Services

### OrcaCore

Central orchestrator service.

| Method | Request | Response | Description |
|--------|---------|----------|-------------|
| `RegisterProcessor` | `ProcessorRegistration` | `Status` | Processor announces supported algorithms on startup |
| `EmitWindow` | `Window` | `WindowEmitStatus` | Submit time-bounded context to trigger algorithm execution |
| `Expose` | `ExposeSettings` | `InternalState` | Export internal registry state for client synchronisation |

### OrcaProcessor

Distributed processor service, implemented by each processor node.

| Method | Request | Response | Description |
|--------|---------|----------|-------------|
| `ExecuteDagPart` | `ExecutionRequest` | `stream ExecutionResult` | Execute a portion of the algorithm DAG; streams results |
| `HealthCheck` | `HealthCheckRequest` | `HealthCheckResponse` | Heartbeat and metrics |

## Key Message Types

| Message | Description |
|---------|-------------|
| `Window` | Time-bounded processing context (`time_from`, `time_to`, `window_type_name`, `window_type_version`, `origin`) |
| `Algorithm` | Processing unit with name, version, window type, dependencies, and result type |
| `AlgorithmDependency` | DAG edge - references a required algorithm with optional lookback config |
| `ProcessorRegistration` | Processor self-announcement including supported algorithms and runtime info |
| `ExecutionRequest` | Algorithm execution packet containing window and resolved dependency results |
| `ExecutionResult` | Streaming result from a single algorithm execution |
| `Result` | Algorithm output - status plus one of `single_value`, `float_values`, or `struct_value` |
| `InternalState` | Full registry snapshot for client-side state cloning |
| `HealthCheckResponse` | Processor status with `ProcessorMetrics` (tasks, memory, CPU, uptime) |

### Enums

| Enum | Values |
|------|--------|
| `ResultType` | `NOT_SPECIFIED`, `STRUCT`, `VALUE`, `ARRAY`, `NONE` |
| `ResultStatus` | `RESULT_STATUS_SUCEEDED`, `RESULT_STATUS_HANDLED_FAILED`, `RESULT_STATUS_UNHANDLED_FAILED` |
| `HealthCheckResponse.Status` | `STATUS_SERVING`, `STATUS_TRANSITIONING`, `STATUS_NOT_SERVING`, `STATUS_UNKNOWN` |
| `WindowEmitStatus.StatusEnum` | `PROCESSING_TRIGGERED`, `NO_TRIGGERED_ALGORITHMS`, `TRIGGERING_FAILED` |

## Generated Code

All code under `go/`, `python/`, and `nodejs/` is generated. Do not edit manually - run `make build` to regenerate.

| Language | Directory | Generator | Notes |
|----------|-----------|-----------|-------|
| Go | `go/` | `protoc-gen-go` v1.33.0 + `protoc-gen-go-grpc` v1.6.0 | Package: `github.com/orca-telemetry/interface/protobufs/go` |
| Python | `python/` | `grpc_tools.protoc` | Includes `.pyi` type stubs |
| TypeScript | `nodejs/` | `protoc-gen-ts_proto` v2.7.7 | grpc-js compatible; oneofs as discriminated unions; snake_case → camelCase |

## Build

### Prerequisites

**protoc** (all languages):

Install via your package manager or from [github.com/protocolbuffers/protobuf/releases](https://github.com/protocolbuffers/protobuf/releases).

**Go:**

```sh
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

**Python:**

```sh
pip install grpcio-tools
```

**TypeScript / Node.js:**

```sh
npm install -g ts-proto
```

### Regenerate

```sh
make build
```

Runs `protoc` for all three language targets against `service.proto` and `vendor/validate.proto`.

## License

MIT © 2026 Orca
