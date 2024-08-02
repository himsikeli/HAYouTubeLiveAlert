# __init__.py

# 初始化模組，這裡可以匯入需要的子模組或進行其他初始化操作
from .sensor import YouTubeSensor

__all__ = ['YouTubeSensor']

# 這裡可以添加其他初始化邏輯，例如設定日誌或其他全域設定
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("HAYouTubeLiveAlert 模組已初始化")