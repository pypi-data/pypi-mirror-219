import os
from unittest.mock import patch

import pytest

from amazon_sagemaker_jupyter_scheduler.aws_config import get_aws_account_id
from amazon_sagemaker_jupyter_scheduler.clients import STSAsyncBotoClient


TEST_AWS_ACCOUNT_ID_STUDIO = "898989898989"


@pytest.mark.asyncio
@patch.dict(os.environ, {"AWS_ACCOUNT_ID": TEST_AWS_ACCOUNT_ID_STUDIO}, clear=True)
async def test_async_cache_studio_base():
    get_aws_account_id.cache_clear()
    assert await get_aws_account_id() == TEST_AWS_ACCOUNT_ID_STUDIO


@pytest.mark.asyncio
@patch.object(STSAsyncBotoClient, "get_caller_identity")
@patch.dict(os.environ, {}, clear=True)
async def test_async_cache_standalone_multiple_call(mock_sts_identity):
    TEST_ACCOUNT_ID_STANDALONE = 888888888888
    get_aws_account_id.cache_clear()
    mock_sts_identity.return_value = {"Account": TEST_ACCOUNT_ID_STANDALONE}
    assert await get_aws_account_id() == TEST_ACCOUNT_ID_STANDALONE

    # future calls should return from cache and not call aws account
    await get_aws_account_id()
    await get_aws_account_id()

    assert 1 == mock_sts_identity.call_count

    get_aws_account_id.cache_clear()
