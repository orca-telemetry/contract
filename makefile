
build:
	protoc \
		--go_out=go \
		--go_opt=paths=source_relative \
		--go-grpc_out=go \
		--go-grpc_opt=paths=source_relative \
		*.proto vendor/*.proto
	python -m grpc_tools.protoc \
    --proto_path=./ \
    --python_out=./python \
    --pyi_out=./python \
    --grpc_python_out=./python \
		*.proto vendor/*.proto
	protoc \
		--plugin=protoc-gen-ts=`which protoc-gen-ts_proto` \
		--ts_proto_out=./nodejs \
		--ts_proto_opt=esModuleInterop=true \
		--ts_proto_opt=useExactTypes=true \
		--ts_proto_opt=outputServices=grpc-js \
		--ts_proto_opt=forceLong=string \
		--ts_proto_opt=env=node \
		--ts_proto_opt=useOptionals=all \
		--ts_proto_opt=oneof=unions-value \
		--ts_proto_opt=snakeToCamel=keys_json \
		--ts_proto_opt=outputClientImpl=true \
		*.proto vendor/*.proto
