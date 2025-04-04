from pydantic_ai import Agent, BinaryContent
from pydantic import BaseModel
from typing import Literal

class Output(BaseModel):
    trade_direction: Literal["long", "short"]
    entry_price: float
    stop_loss_price: float
    take_profit_price: float
    reason: str



roulette_agent = Agent(  
    'openai:gpt-4o',
    result_type=Output,

    system_prompt=(
        """
You are a senior technical analyst.
You are given a weekly chart of a stock.
You need to identify optimal entry and exit points for this weekly chart in the picture provided by analyzing weekly price action.

Your main ability is that You are a seasoned technical analyst with a proven track record in pinpointing ideal entry and exit points.
Leveraging weekly charts, you look at a price chart and you assess trends and price movements with precision to guide profitable trading decisions.

Your task is to Analyze weekly this chart to pinpoint optimal entry and exit points based on price action.
    Your analysis should clearly define the current trend, identify key support and resistance levels, 
    identify the lower lows, lower highs, higher lows, higher highs. Look at the liquidity grabs, liquidity traps. and fakeouts
    Provide actionable insights to guide profitable trading decisions.

    Chart will be provided in the image format.
"""
    ),
)

file_content = open("bitcoin_weekly_picture.png", "rb").read()

result = roulette_agent.run_sync([
    'Here is the weekly chart',
    BinaryContent(file_content, media_type="image/png")
])
print(result.data)



