import logging
import datetime
from googleapiclient.discovery import build
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_API_KEY
from homeassistant.helpers.entity import Entity
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'hayoutubelivealert'
SCAN_INTERVAL = datetime.timedelta(minutes=5)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required('channel_id'): cv.string,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    api_key = config[CONF_API_KEY]
    channel_id = config['channel_id']

    if not api_key or not channel_id:
        _LOGGER.error("You must provide an API key and channel ID")
        return False

    add_entities([YouTubeSensor(api_key, channel_id)], True)

class YouTubeSensor(Entity):
    def __init__(self, api_key, channel_id):
        self._state = None
        self._api_key = api_key
        self._channel_id = channel_id
        self._name = "YouTube Live Stream"
        self._live_url = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return {
            "live_url": self._live_url
        }

    def update(self):
        try:
            youtube = build('youtube', 'v3', developerKey=self._api_key)
            request = youtube.search().list(part='snippet', channelId=self._channel_id, type='video', eventType='live')
            response = request.execute()

            _LOGGER.debug("YouTube API response: %s", response)  # 增加日誌以檢查 API 回應

            if response['items']:
                self._state = "Live"
                self._live_url = f"https://www.youtube.com/watch?v={response['items'][0]['id']['videoId']}"
                _LOGGER.info("Live stream found: %s", self._live_url)
            else:
                self._state = "Not Live"
                self._live_url = None
                _LOGGER.info("No live stream found.")
        except Exception as e:
            _LOGGER.error("Error fetching data from YouTube API: %s", e)
            self._state = "Error"
            self._live_url = None
