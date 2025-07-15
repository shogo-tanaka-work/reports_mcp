#!/usr/bin/env python3
"""
Weather MCP Server
天気予報と天気警告情報を取得するMCPサーバ
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

# ライブラリのインポート
import httpx
from fastmcp import FastMCP

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastMCPのインスタンス化
mcp = FastMCP("Weather MCP Server")

# ヘルパー関数

async def get_weather_forecast(location: str, days: int = 5) -> Dict[str, Any]:
    """
    天気予報取得ツール
    指定された場所の天気予報を取得します
    
    Args:
        location: 場所名（例：東京、大阪）
        days: 予報日数（デフォルト：5日）
    
    Returns:
        天気予報データ
    """
    try:
        # 実際の天気予報API呼び出しの代わりに、サンプルデータを返す
        # 実際の実装では、OpenWeatherMap API等を使用
        sample_forecast = {
            "location": location,
            "forecast_days": days,
            "current_weather": {
                "temperature": 22.5,
                "humidity": 65,
                "condition": "曇り",
                "wind_speed": 12.3,
                "wind_direction": "北東"
            },
            "daily_forecast": []
        }
        
        # 日次予報データを生成
        for i in range(days):
            date = datetime.now() + timedelta(days=i)
            daily_data = {
                "date": date.strftime("%Y-%m-%d"),
                "day_of_week": date.strftime("%A"),
                "high_temp": 25 + i,
                "low_temp": 15 + i,
                "condition": "晴れ" if i % 2 == 0 else "雨",
                "precipitation_chance": 20 + (i * 10),
                "humidity": 60 + (i * 5),
                "wind_speed": 10 + (i * 2)
            }
            sample_forecast["daily_forecast"].append(daily_data)
        
        logger.info(f"天気予報を取得しました: {location}, {days}日間")
        return sample_forecast
        
    except Exception as e:
        logger.error(f"天気予報の取得に失敗しました: {str(e)}")
        raise


async def get_weather_warnings(location: str) -> Dict[str, Any]:
    """
    天気警告情報取得ツール
    指定された場所の天気警告情報を取得します
    
    Args:
        location: 場所名（例：東京、大阪）
    
    Returns:
        天気警告情報データ
    """
    try:
        # 実際の天気警告API呼び出しの代わりに、サンプルデータを返す
        # 実際の実装では、気象庁API等を使用
        sample_warnings = {
            "location": location,
            "issued_at": datetime.now().isoformat(),
            "warnings": [
                {
                    "type": "大雨警報",
                    "severity": "警報",
                    "description": "24時間降水量が100mmを超える見込みです",
                    "issued_time": datetime.now().isoformat(),
                    "valid_until": (datetime.now() + timedelta(hours=12)).isoformat(),
                    "affected_areas": [f"{location}南部", f"{location}北部"]
                },
                {
                    "type": "強風注意報",
                    "severity": "注意報",
                    "description": "最大風速15m/sの強風が予想されます",
                    "issued_time": datetime.now().isoformat(),
                    "valid_until": (datetime.now() + timedelta(hours=6)).isoformat(),
                    "affected_areas": [f"{location}全域"]
                }
            ],
            "total_warnings": 2
        }
        
        logger.info(f"天気警告情報を取得しました: {location}")
        return sample_warnings
        
    except Exception as e:
        logger.error(f"天気警告情報の取得に失敗しました: {str(e)}")
        raise


# MCPのツール

@mcp.tool()
async def get_weather_forecast_tool(location: str = "東京", days: int = 5) -> str:
    """
    天気予報を取得します
    
    Args:
        location: 場所名（例：東京、大阪、札幌）
        days: 予報日数（1-7日、デフォルト：5日）
    
    Returns:
        JSON形式の天気予報データ
    """
    if not location:
        return json.dumps({"error": "場所名を指定してください"}, ensure_ascii=False)
    
    if not (1 <= days <= 7):
        return json.dumps({"error": "予報日数は1-7日の範囲で指定してください"}, ensure_ascii=False)
    
    try:
        forecast_data = await get_weather_forecast(location, days)
        return json.dumps(forecast_data, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": f"天気予報の取得に失敗しました: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
async def get_weather_warnings_tool(location: str) -> str:
    """
    天気警告情報を取得します
    
    Args:
        location: 場所名（例：東京、大阪、札幌）
    
    Returns:
        JSON形式の天気警告情報データ
    """
    if not location:
        return json.dumps({"error": "場所名を指定してください"}, ensure_ascii=False)
    
    try:
        warnings_data = await get_weather_warnings(location)
        return json.dumps(warnings_data, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": f"天気警告情報の取得に失敗しました: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
async def get_weather_summary_tool(location: str) -> str:
    """
    天気予報と警告情報の概要を取得します
    
    Args:
        location: 場所名（例：東京、大阪、札幌）
    
    Returns:
        JSON形式の天気概要データ
    """
    if not location:
        return json.dumps({"error": "場所名を指定してください"}, ensure_ascii=False)
    
    try:
        # 天気予報と警告情報を並行して取得
        forecast_task = get_weather_forecast(location, 3)
        warnings_task = get_weather_warnings(location)
        
        forecast_data, warnings_data = await asyncio.gather(
            forecast_task, warnings_task, return_exceptions=True
        )
        
        # エラーハンドリング
        if isinstance(forecast_data, Exception):
            forecast_data = {"error": str(forecast_data)}
        if isinstance(warnings_data, Exception):
            warnings_data = {"error": str(warnings_data)}
        
        summary = {
            "location": location,
            "summary_generated_at": datetime.now().isoformat(),
            "forecast_summary": forecast_data,
            "warnings_summary": warnings_data
        }
        
        return json.dumps(summary, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"天気概要の取得に失敗しました: {str(e)}"}, ensure_ascii=False)


# エントリーポイント
if __name__ == "__main__":
    # MCPサーバとして直接実行される場合
    try:
        logger.info("Weather MCP Server を起動しています...")
        
        # MCPサーバを実行（同期的に実行）
        mcp.run()
        
    except KeyboardInterrupt:
        logger.info("Weather MCP Server を停止しています...")
    except Exception as e:
        logger.error(f"サーバエラー: {str(e)}")
        raise 