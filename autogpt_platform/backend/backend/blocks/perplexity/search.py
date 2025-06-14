from backend.blocks.perplexity._auth import (
    PerplexityCredentials,
    PerplexityCredentialsField,
    PerplexityCredentialsInput,
)
from backend.data.block import Block, BlockCategory, BlockOutput, BlockSchema
from backend.data.model import SchemaField
from backend.util.request import requests


class PerplexitySearchBlock(Block):
    class Input(BlockSchema):
        credentials: PerplexityCredentialsInput = PerplexityCredentialsField()
        query: str = SchemaField(description="The search query")
        number_of_results: int = SchemaField(
            description="Number of results to return",
            default=10,
            advanced=True,
        )

    class Output(BlockSchema):
        results: list = SchemaField(
            description="List of search results",
            default_factory=list,
        )
        error: str = SchemaField(description="Error message if the request failed")

    def __init__(self):
        super().__init__(
            id="676f67ce-04d7-4c42-b917-bc2b4f7d66bf",
            description="Searches the web using Perplexity's search API",
            categories={BlockCategory.SEARCH},
            input_schema=PerplexitySearchBlock.Input,
            output_schema=PerplexitySearchBlock.Output,
        )

    def run(
        self, input_data: Input, *, credentials: PerplexityCredentials, **kwargs
    ) -> BlockOutput:
        url = "https://api.perplexity.ai/search"
        headers = {
            "Authorization": f"Bearer {credentials.api_key.get_secret_value()}",
        }

        params = {
            "q": input_data.query,
            "n": input_data.number_of_results,
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            yield "results", data.get("results", [])
        except Exception as e:
            yield "error", str(e)
