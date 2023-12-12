import asyncio
import unittest
import aiohttp


class TestCollectibleRoutes(unittest.TestCase):  # inherit from unittest.TestCase

    base_url = "http://localhost:1111/financialService"

    async def getWallet(self, session):
        async with session.get(f"{self.base_url}/getWallet/1") as response:
            return response.status

    def test_concurrent_buy_and_sell(self):
        async def run_test(num_requests=4000):
            async with aiohttp.ClientSession() as session:
                tasks_login = [asyncio.create_task(self.getWallet(session)) for _ in
                               range(num_requests)]

                response_login = await asyncio.gather(*tasks_login)
            for i in range(len(response_login)):
                self.assertEqual(response_login[i], 200)
                print(str(i) + " wallet")

        asyncio.run(run_test())


if __name__ == '__main__':
    unittest.main()
