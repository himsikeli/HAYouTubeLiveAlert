import unittest
import os
from unittest.mock import patch, MagicMock
from custom_components.hayoutubelivealert.sensor import YouTubeSensor

class TestYouTubeSensor(unittest.TestCase):

	def setUp(self):
		self.api_key = os.getenv("YOUTUBE_API_KEY", "test_api_key")
		self.channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"
		self.sensor = YouTubeSensor(self.api_key, self.channel_id)

	@patch('custom_components.hayoutubelivealert.sensor.build')
	def test_update_live(self, mock_build):
		# Mock the YouTube API response for a live stream
		mock_youtube = MagicMock()
		mock_search = MagicMock()
		mock_list = MagicMock()
		mock_execute = MagicMock()
		
		mock_execute.return_value = {'items': [{'id': {'videoId': 'live_video_id'}}]}
		mock_list.execute.return_value = mock_execute.return_value
		mock_search.list.return_value = mock_list
		mock_youtube.search.return_value = mock_search
		mock_build.return_value = mock_youtube

		self.sensor.update()

		# Print the mocked response
		print(mock_execute.return_value)

		self.assertEqual(self.sensor.state, "Live")
		self.assertEqual(self.sensor.extra_state_attributes['live_url'], "https://www.youtube.com/watch?v=live_video_id")

	def test_something(self):
		# Add your test case here
		pass

if __name__ == '__main__':
	unittest.main()