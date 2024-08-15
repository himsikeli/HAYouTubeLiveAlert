import datetime
import logging
import voluptuous as vol
from homeassistant.helpers.entity import Entity
from homeassistant.helpers import config_validation as cv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = datetime.timedelta(hours=1)  # 將更新間隔設為1小時

CONF_API_KEY = 'api_key'
CONF_CHANNEL_ID = 'channel_id'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_CHANNEL_ID): cv.string,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    api_key = config[CONF_API_KEY]
    channel_id = config[CONF_CHANNEL_ID]

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

            if response['items']:
                self._state = "Live"
                self._live_url = f"https://www.youtube.com/watch?v={response['items'][0]['id']['videoId']}"
            else:
                self._state = "Offline"
                self._live_url = None

        except HttpError as e:
            if e.resp.status == 403 and 'quotaExceeded' in e.content.decode():
                _LOGGER.error("YouTube API quota exceeded.")
            else:
                _LOGGER.error(f"HTTP error occurred: {e}")
            self._state = "Error"
            self._live_url = None

        except Exception as e:
            _LOGGER.error(f"An error occurred: {e}")
            self._state = "Error"
            self._live_url = None