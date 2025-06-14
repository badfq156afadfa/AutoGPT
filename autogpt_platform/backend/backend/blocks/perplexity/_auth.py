from typing import Literal

from pydantic import SecretStr

from backend.data.model import APIKeyCredentials, CredentialsField, CredentialsMetaInput
from backend.integrations.providers import ProviderName

PerplexityCredentials = APIKeyCredentials
PerplexityCredentialsInput = CredentialsMetaInput[
    Literal[ProviderName.PERPLEXITY],
    Literal["api_key"],
]

TEST_CREDENTIALS = APIKeyCredentials(
    id="01234567-89ab-cdef-0123-456789abcdef",
    provider="perplexity",
    api_key=SecretStr("mock-perplexity-api-key"),
    title="Mock Perplexity API key",
    expires_at=None,
)

TEST_CREDENTIALS_INPUT = {
    "provider": TEST_CREDENTIALS.provider,
    "id": TEST_CREDENTIALS.id,
    "type": TEST_CREDENTIALS.type,
    "title": TEST_CREDENTIALS.title,
}


def PerplexityCredentialsField() -> PerplexityCredentialsInput:
    """Creates a Perplexity credentials input on a block."""
    return CredentialsField(
        description="The Perplexity integration requires an API Key."
    )
