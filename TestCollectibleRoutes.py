import asyncio
import unittest
import aiohttp


class TestCollectibleRoutes(unittest.TestCase):  # inherit from unittest.TestCase

    base_url = "http://localhost:1111/collectibleService"

    async def buy_collectible(self, session, buy_request):
        async with session.post(f"{self.base_url}/buy", json=buy_request) as response:
            return response.status

    async def sell_collectible(self, session, sell_request):
        async with session.post(f"{self.base_url}/sell", json=sell_request) as response:
            return response.status

    def test_concurrent_buy_and_sell(self):

        async def run_test(buy_request, sell_request, num_requests=100):
            async with aiohttp.ClientSession() as session:
                tasks_buy = [asyncio.create_task(self.buy_collectible(session, buy_request)) for _ in
                             range(num_requests)]

                responses_buy = await asyncio.gather(*tasks_buy)

                tasks_sell = [asyncio.create_task(self.sell_collectible(session, sell_request)) for _ in
                              range(num_requests)]
                responses_sell = await asyncio.gather(*tasks_sell)

            for i in range(len(responses_buy)):
                self.assertEqual(responses_buy[i], 200)
                print(str(i) + "responses_buy")

            for i in range(len(responses_sell)):
                self.assertEqual(responses_sell[i], 200)
                print(str(i) + "sell")

        # Run the async function using asyncio.run
        buy_request = {
            "collectibleId": "1",
            "userId": "1",
            "shares": "10"
        }
        sell_request = {
            "collectibleId": "1",
            "userId": "1",
            "shares": "10"
        }
        asyncio.run(run_test(buy_request, sell_request))


if __name__ == '__main__':
    unittest.main()
