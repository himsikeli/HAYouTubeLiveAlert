
# HAYouTubeLiveAlert

HAYouTubeLiveAlert 是一個 Home Assistant 自訂元件，當您關注的 YouTube 頻道開始直播時，該元件將會通知您。

## 功能

- 使用 YouTube Data API v3 獲取直播狀態和直播連結
- 當直播開始時，通過 Home Assistant 發送通知

## 安裝

### 前置準備

1. **獲取 YouTube Data API 金鑰**
   - 前往 [Google Cloud Console](https://console.cloud.google.com/).
   - 創建新專案或選擇現有專案。
   - 啟用 YouTube Data API v3。
   - 創建 API 金鑰，並保存此金鑰以供後續使用。

### 在 Home Assistant 中安裝自訂元件

#### 手動安裝

1. 在 Home Assistant 配置資料夾中，創建 `custom_components` 資料夾（如果尚未存在）。
2. 在 `custom_components` 資料夾中創建一個名為 `hayoutubelivealert` 的資料夾。
3. 在 `hayoutubelivealert` 資料夾中創建以下文件：
   - `__init__.py`
   - `sensor.py`
   - `manifest.json`

#### 使用 HACS 安裝

1. 打開 Home Assistant，進入 HACS（Home Assistant Community Store）。
2. 點擊 “Integrations”。
3. 點擊右上角的 “+” 按鈕，並搜索 `HAYouTubeLiveAlert`。
4. 選擇 `HAYouTubeLiveAlert` 並點擊 “Install”。

### 編寫文件內容

#### `__init__.py`

```python
# 這個文件可以保持空白
```

#### `manifest.json`

```json
{
  "domain": "hayoutubelivealert",
  "name": "HAYouTubeLiveAlert Sensor",
  "documentation": "https://github.com/Ikeli0320/HAYouTubeLiveAlert",
  "requirements": ["google-api-python-client==2.30.0"],
  "dependencies": [],
  "codeowners": ["@Ikeli0320"]
}
```

#### `sensor.py`

```python
import logging
import datetime
from googleapiclient.discovery import build
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_API_KEY

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'hayoutubelivealert'
SCAN_INTERVAL = datetime.timedelta(minutes=5)

def setup_platform(hass, config, add_entities, discovery_info=None):
    api_key = config.get(CONF_API_KEY)
    channel_id = config.get('channel_id')

    if not api_key or not channel_id:
        _LOGGER.error("You must provide an API key and channel ID")
        return False

    add_entities([YouTubeSensor(api_key, channel_id)], True)

class YouTubeSensor(SensorEntity):
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
        youtube = build('youtube', 'v3', developerKey=self._api_key)
        request = youtube.search().list(part='snippet', channelId=self._channel_id, type='video', eventType='live')
        response = request.execute()

        if response['items']:
            self._state = "Live"
            self._live_url = f"https://www.youtube.com/watch?v={response['items'][0]['id']['videoId']}"
        else:
            self._state = "Not Live"
            self._live_url = None
```

### 配置 Home Assistant

在 `configuration.yaml` 文件中，加入以下內容：

```yaml
sensor:
  - platform: hayoutubelivealert
    api_key: YOUR_API_KEY
    channel_id: YOUR_CHANNEL_ID
```

## 使用 Node-RED 進行自動化

使用 Node-RED 來處理自動化訊息並發送通知。例如，當 `YouTube Live Stream` 感應器的狀態變為 `Live` 時，發送通知。

## 貢獻

歡迎提交問題（issues）和拉取請求（pull requests）。有任何問題，請聯繫 [Ikeli0320](mailto:您的電子郵件).

## 授權

這個專案基於 [MIT 授權](LICENSE) 進行授權。
