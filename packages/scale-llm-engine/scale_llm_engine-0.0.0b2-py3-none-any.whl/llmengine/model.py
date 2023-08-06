from llmengine.api_engine import DEFAULT_TIMEOUT, APIEngine, assert_self_hosted
from llmengine.data_types import (
    CreateLLMEndpointRequest,
    CreateLLMEndpointResponse,
    DeleteLLMEndpointResponse,
    GetLLMEndpointResponse,
    ListLLMEndpointsResponse,
)


class Model(APIEngine):
    """
    Model API. This API is used to get, list, delete, and (in the self-hosted case) create models. When using Scale Spellbook, create models using FineTune.create().

    See [Model Zoo](../../model_zoo) for the list of publicly available models.
    """

    @classmethod
    @assert_self_hosted
    def create(
        cls,
        model_name: str,
    ) -> CreateLLMEndpointResponse:
        """
        Create an LLM model endpoint. Note: This feature is only available for self-hosted users.

        Args:
            model_name (`str`):
                Name of the model

        Returns:
            CreateLLMEndpointResponse: ID of the created Model Endpoint.
        """
        request = CreateLLMEndpointRequest(
            model_name=model_name,
        )
        response = cls.post_sync(
            resource_name="v1/llm/model-endpoints",
            data=request.dict(),
            timeout=DEFAULT_TIMEOUT,
        )
        return CreateLLMEndpointResponse.parse_obj(response)

    @classmethod
    def get(
        cls,
        model_name: str,
    ) -> GetLLMEndpointResponse:
        """
        Get information about an LLM model endpoint.

        Args:
            model_name (`str`):
                Name of the model

        Returns:
            GetLLMEndpointResponse: object representing the LLM endpoint and configurations

        Example:
            ```python
            from llmengine import Model

            response = Model.get("llama-7b.suffix.2023-07-18-12-00-00")

            print(response.json())
            ```

        JSON Response:
            ```json
            {
                "id": "end_abc123",
                "name": "llama-7b.suffix.2023-07-18-12-00-00",
                "model_name": "llama-7b",
                "source": "hugging_face",
                "inference_framework": "text_generation_inference",
                "num_shards": 4
            }
            ```
        """
        response = cls._get(f"v1/llm/model-endpoints/{model_name}", timeout=DEFAULT_TIMEOUT)
        return GetLLMEndpointResponse.parse_obj(response)

    @classmethod
    def list(cls) -> ListLLMEndpointsResponse:
        """
        List LLM model endpoints available to call inference on. This includes publicly available endpoints as well as your fine-tuned model endpoints.

        Returns:
            ListLLMEndpointsResponse: list of model endpoints

        Example:
            ```python
            from llmengine import Model

            response = Model.list()
            print(response.json())
            ```

        JSON Response:
            ```json
            {
                "model_endpoints": [
                    {
                        "id": "end_abc123",
                        "name": "llama-7b",
                        "model_name": "llama-7b",
                        "source": "hugging_face",
                        "inference_framework": "text_generation_inference",
                        "num_shards": 4
                    },
                    {
                        "id": "end_def456",
                        "name": "llama-13b-deepspeed-sync",
                        "model_name": "llama-13b-deepspeed-sync",
                        "source": "hugging_face",
                        "inference_framework": "deepspeed",
                        "num_shards": 4
                    },
                    {
                        "id": "end_ghi789",
                        "name": "falcon-40b",
                        "model_name": "falcon-40b",
                        "source": "hugging_face",
                        "inference_framework": "text_generation_inference",
                        "num_shards": 4
                    },
                    {
                        "id": "end_jkl012",
                        "name": "mpt-7b-instruct",
                        "model_name": "mpt-7b-instruct",
                        "source": "hugging_face",
                        "inference_framework": "text_generation_inference",
                        "num_shards": 4
                    }
                ]
            }
            ```
        """
        response = cls._get("v1/llm/model-endpoints", timeout=DEFAULT_TIMEOUT)
        return ListLLMEndpointsResponse.parse_obj(response)

    @classmethod
    def delete(cls, model_name: str) -> DeleteLLMEndpointResponse:
        """
        Deletes an LLM model endpoint.

        Args:
            model_name (`str`):
                Name of the model

        Returns:
            response: whether the model was successfully deleted

        Example:
            ```python
            from llmengine import Model

            response = Model.delete("llama-7b.suffix.2023-07-18-12-00-00")
            print(response.json())
            ```

        JSON Response:
            ```json
            {
                "deleted": true
            }
            ```
        """
        response = cls._delete(f"v1/llm/model-endpoints/{model_name}", timeout=DEFAULT_TIMEOUT)
        return DeleteLLMEndpointResponse.parse_obj(response)
