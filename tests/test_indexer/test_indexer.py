from unittest import IsolatedAsyncioTestCase

import indexer


class ExampleTest(IsolatedAsyncioTestCase):
    async def test_example(self):
        assert indexer