
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
2. 選擇 “Custom repositories”。
3. Repository輸入 https://github.com/Ikeli0320/HAYouTubeLiveAlert 。
4. Category選擇 integration 。
5. 搜索 `HAYouTubeLiveAlert`。
6. 選擇 `HAYouTubeLiveAlert` 並點擊 “Download”。

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
