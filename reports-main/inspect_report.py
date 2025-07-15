# MCPのツールを実行するためのコード（ローカル実行確認用）
from datetime import datetime, timedelta
import asyncio

async def main(location: str, days: int):
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
        
        print(f"天気予報を取得しました: {location}, {days}日間")
        return sample_forecast
        
    except Exception as e:
        print(f"天気予報の取得に失敗しました: {str(e)}")
        raise


if __name__ == "__main__":
  try:
      asyncio.run(main("東京", 5))
  except KeyboardInterrupt:
      print("\n天気予報取得ツールを終了します。")
  except Exception as e:
      print(f"天気予報取得ツールの実行中にエラーが発生しました: {e}")
