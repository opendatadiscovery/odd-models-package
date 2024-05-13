
generate_models: generate_entities generate_metrics

generate_entities:
	datamodel-codegen --input ./opendatadiscovery-specification/specification/entities.yaml --output odd_models/models/models.py --input-file-type openapi --output-model-type pydantic_v2.BaseModel
generate_metrics:
	datamodel-codegen --input ./opendatadiscovery-specification/specification/metrics.yaml --output odd_models/models/metrics.py --input-file-type openapi --output-model-type pydantic_v2.BaseModel
generate_client:
	docker run \
			--rm \
			-v ${PWD}/opendatadiscovery-specification/specification:/spec/ \
			-v ${PWD}/_generated:/generated \
			-v ${PWD}/openapi_generator/api_client:/openapi_generator/api_client \
			openapitools/openapi-generator-cli:v5.4.0 generate \
			-i /spec/odd_api.yaml \
			-g python \
			-o /generated \
			-t openapi_generator/api_client \
			--additional-properties=packageName=odd_models.api_client
	mv -f _generated/odd_models/api_client/api/* odd_models/api_client
	rm -rf _generated/

