import unittest
from unittest.mock import AsyncMock, patch
import bot

class TestBot(unittest.IsolatedAsyncioTestCase):
    @patch('bot.aiohttp.ClientSession.get')
    async def test_sale_command(self, mock_get):
        mock_ctx = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json.return_value = [{'title': 'Test Game', 'storeID': '1', 'salePrice': '10.00', 'normalPrice': '20.00', 'thumb': 'http://example.com/thumb.jpg'}]
        mock_get.return_value.__aenter__.return_value = mock_response

        await bot.sale(mock_ctx, game_name='Test Game')

        mock_ctx.send.assert_called_once()
        self.assertIn('Test Game', mock_ctx.send.call_args[1]['embed'].title)

    async def test_handle_deals_exact_match(self):
        mock_ctx = AsyncMock()
        deals = [{'title': 'Test Game', 'storeID': '1', 'salePrice': '10.00', 'normalPrice': '20.00', 'thumb': 'http://example.com/thumb.jpg'}]

        await bot.handle_deals(mock_ctx, 'Test Game', deals)

        mock_ctx.send.assert_called_once()
        self.assertIn('Test Game', mock_ctx.send.call_args[1]['embed'].title)

    async def test_handle_deals_no_match(self):
        mock_ctx = AsyncMock()
        deals = []

        await bot.handle_deals(mock_ctx, 'Nonexistent Game', deals)

        mock_ctx.send.assert_called_once()
        self.assertIn('No deals found for Nonexistent Game', mock_ctx.send.call_args[1]['embed'].title)

    async def test_handle_close_matches_single(self):
        mock_ctx = AsyncMock()
        deals = [{'title': 'Test Game', 'storeID': '1', 'salePrice': '10.00', 'normalPrice': '20.00', 'thumb': 'http://example.com/thumb.jpg'}]
        close_matches = [('Test Game', 90)]

        await bot.handle_close_matches(mock_ctx, 'Test Game', deals, close_matches)

        mock_ctx.send.assert_called_once()
        self.assertIn('Test Game', mock_ctx.send.call_args[1]['embed'].title)

    async def test_handle_close_matches_multiple(self):
        mock_ctx = AsyncMock()
        deals = [{'title': 'Test Game 1', 'storeID': '1', 'salePrice': '10.00', 'normalPrice': '20.00', 'thumb': 'http://example.com/thumb.jpg'},
                 {'title': 'Test Game 2', 'storeID': '2', 'salePrice': '15.00', 'normalPrice': '30.00', 'thumb': 'http://example.com/thumb2.jpg'}]
        close_matches = [('Test Game 1', 90), ('Test Game 2', 85)]

        await bot.handle_close_matches(mock_ctx, 'Test Game', deals, close_matches)

        mock_ctx.send.assert_called_once()
        self.assertIn('Multiple deals found for Test Game', mock_ctx.send.call_args[1]['embed'].title)

    async def test_send_no_deals_found(self):
        mock_ctx = AsyncMock()

        await bot.send_no_deals_found(mock_ctx, 'Nonexistent Game')

        mock_ctx.send.assert_called_once()
        self.assertIn('No deals found for Nonexistent Game', mock_ctx.send.call_args[1]['embed'].title)

    async def test_send_deal_with_discount(self):
        mock_ctx = AsyncMock()
        deals = [{'title': 'Test Game', 'storeID': '1', 'salePrice': '10.00', 'normalPrice': '20.00', 'thumb': 'http://example.com/thumb.jpg'}]

        await bot.send_deal(mock_ctx, deals, 'Test Game')

        mock_ctx.send.assert_called_once()
        self.assertIn('Test Game', mock_ctx.send.call_args[1]['embed'].title)
        self.assertIn('50%', mock_ctx.send.call_args[1]['embed'].fields[1].value)

    async def test_send_deal_no_discount(self):
        mock_ctx = AsyncMock()
        deals = [{'title': 'Test Game', 'storeID': '1', 'salePrice': '20.00', 'normalPrice': '20.00', 'thumb': 'http://example.com/thumb.jpg'}]

        await bot.send_deal(mock_ctx, deals, 'Test Game')

        mock_ctx.send.assert_called_once()
        self.assertIn('Test Game', mock_ctx.send.call_args[1]['embed'].title)
        self.assertIn('No discount available', mock_ctx.send.call_args[1]['embed'].fields[1].value)

    async def test_info_command(self):
        mock_ctx = AsyncMock()

        await bot.info(mock_ctx)

        mock_ctx.send.assert_called_once()
        self.assertIn('Game Sale Bot', mock_ctx.send.call_args[1]['embed'].title)
        @patch('bot.aiohttp.ClientSession.get')
        async def test_sale_command(self, mock_get):
            mock_ctx = AsyncMock()
            mock_response = AsyncMock()
            mock_response.json.return_value = [{'title': 'Test Game', 'storeID': '1', 'salePrice': '10.00', 'normalPrice': '20.00', 'thumb': 'http://example.com/thumb.jpg'}]
            mock_get.return_value.__aenter__.return_value = mock_response

            await bot.sale(mock_ctx, game_name='Test Game')

            mock_ctx.send.assert_called_once()
            self.assertIn('Test Game', mock_ctx.send.call_args[1]['embed'].title)

        async def test_handle_deals_exact_match(self):
            mock_ctx = AsyncMock()
            deals = [{'title': 'Test Game', 'storeID': '1', 'salePrice': '10.00', 'normalPrice': '20.00', 'thumb': 'http://example.com/thumb.jpg'}]

            await bot.handle_deals(mock_ctx, 'Test Game', deals)

            mock_ctx.send.assert_called_once()
            self.assertIn('Test Game', mock_ctx.send.call_args[1]['embed'].title)

        async def test_handle_deals_no_match(self):
            mock_ctx = AsyncMock()
            deals = []

            await bot.handle_deals(mock_ctx, 'Nonexistent Game', deals)

            mock_ctx.send.assert_called_once()
            self.assertIn('No deals found for Nonexistent Game', mock_ctx.send.call_args[1]['embed'].title)

        async def test_handle_close_matches_single(self):
            mock_ctx = AsyncMock()
            deals = [{'title': 'Test Game', 'storeID': '1', 'salePrice': '10.00', 'normalPrice': '20.00', 'thumb': 'http://example.com/thumb.jpg'}]
            close_matches = [('Test Game', 90)]

            await bot.handle_close_matches(mock_ctx, 'Test Game', deals, close_matches)

            mock_ctx.send.assert_called_once()
            self.assertIn('Test Game', mock_ctx.send.call_args[1]['embed'].title)

        async def test_handle_close_matches_multiple(self):
            mock_ctx = AsyncMock()
            deals = [{'title': 'Test Game 1', 'storeID': '1', 'salePrice': '10.00', 'normalPrice': '20.00', 'thumb': 'http://example.com/thumb.jpg'},
                     {'title': 'Test Game 2', 'storeID': '2', 'salePrice': '15.00', 'normalPrice': '30.00', 'thumb': 'http://example.com/thumb2.jpg'}]
            close_matches = [('Test Game 1', 90), ('Test Game 2', 85)]

            await bot.handle_close_matches(mock_ctx, 'Test Game', deals, close_matches)

            mock_ctx.send.assert_called_once()
            self.assertIn('Multiple deals found for Test Game', mock_ctx.send.call_args[1]['embed'].title)

        async def test_send_no_deals_found(self):
            mock_ctx = AsyncMock()

            await bot.send_no_deals_found(mock_ctx, 'Nonexistent Game')

            mock_ctx.send.assert_called_once()
            self.assertIn('No deals found for Nonexistent Game', mock_ctx.send.call_args[1]['embed'].title)

        async def test_send_deal_with_discount(self):
            mock_ctx = AsyncMock()
            deals = [{'title': 'Test Game', 'storeID': '1', 'salePrice': '10.00', 'normalPrice': '20.00', 'thumb': 'http://example.com/thumb.jpg'}]

            await bot.send_deal(mock_ctx, deals, 'Test Game')

            mock_ctx.send.assert_called_once()
            self.assertIn('Test Game', mock_ctx.send.call_args[1]['embed'].title)
            self.assertIn('50%', mock_ctx.send.call_args[1]['embed'].fields[1].value)

        async def test_send_deal_no_discount(self):
            mock_ctx = AsyncMock()
            deals = [{'title': 'Test Game', 'storeID': '1', 'salePrice': '20.00', 'normalPrice': '20.00', 'thumb': 'http://example.com/thumb.jpg'}]

            await bot.send_deal(mock_ctx, deals, 'Test Game')

            mock_ctx.send.assert_called_once()
            self.assertIn('Test Game', mock_ctx.send.call_args[1]['embed'].title)
            self.assertIn('No discount available', mock_ctx.send.call_args[1]['embed'].fields[1].value)

        async def test_info_command(self):
            mock_ctx = AsyncMock()

            await bot.info(mock_ctx)

            mock_ctx.send.assert_called_once()
            self.assertIn('Game Sale Bot', mock_ctx.send.call_args[1]['embed'].title)
if __name__ == '__main__':
    unittest.main()