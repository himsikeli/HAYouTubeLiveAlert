import homeassistant.helpers.config_validation as cv
import logging
import datetime
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
from googleapiclient.discovery import build

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'hayoutubelivealert'
SCAN_INTERVAL = datetime.timedelta(minutes=5)

CONF_API_KEY = 'api_key'
CONF_CHANNEL_ID = 'channel_id'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
	vol.Required(CONF_API_KEY): cv.string,
	vol.Required(CONF_CHANNEL_ID): cv.string,
})

class YouTubeSensor(Entity):
	def __init__(self, api_key, channel_id):
		self._api_key = api_key
		self._channel_id = channel_id
		self._state = None
		self._live_url = None

	@property
	def name(self):
		return "YouTube Live Alert"

	@property
	def state(self):
		return self._state

	@property
	def extra_state_attributes(self):
		return {
			"live_url": self._live_url
		}

	def update(self):
		youtube = build('youtube', 'v3', developerKey=self._api_key)
		request = youtube.search().list(part='snippet', channelId=self._channel_id, type='video', eventType='live')
		response = request.execute()

		if response['items']:
			self._state = "Live"
			self._live_url = f"https://www.youtube.com/watch?v={response['items'][0]['id']['videoId']}"
		else:
			self._state = "Offline"
			self._live_url = None

def setup_platform(hass, config, add_entities, discovery_info=None):
	api_key = config.get(CONF_API_KEY)
	channel_id = config.get(CONF_CHANNEL_ID)

	if not api_key or not channel_id:
		_LOGGER.error("API key or Channel ID not provided")
		return False

	add_entities([YouTubeSensor(api_key, channel_id)], True)

class YouTubeSensor(Entity):
    def __init__(self, api_key, channel_id):
        self._api_key = api_key
        self._channel_id = channel_id
        self._state = None
        self._live_url = None

    @property
    def name(self):
        return "YouTube Live Alert"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return {
            "live_url": self._live_url
        }

    def update(self):
        youtube = build('youtube', 'v3', developerKey=self._api_key)
        request = youtube.search().list(part='snippet', channelId=self._channel_id, type='video', eventType='live')
        response = request.execute()

        if response['items']:
            self._state = "Live"
            self._live_url = f"https://www.youtube.com/watch?v={response['items'][0]['id']['videoId']}"
        else:
            self._state = "Offline"
            self._live_url = None