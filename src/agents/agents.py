from pydantic_ai import Agent, RunContext, BinaryContent, Tool
from pydantic import BaseModel
from typing import Literal
from src.agents.prompts import DAILY_ANALYST_PROMPT, SUPERVISOR_PROMPT

class Output(BaseModel):
    trade_direction: Literal["long", "short"]
    entry_price: float
    stop_loss_price: float
    take_profit_price: float
    reason: str


class Agents:
    def __init__(self):
        self.daily_analyst = Agent(
            'openai:gpt-4o',
            result_type=Output,
            system_prompt=DAILY_ANALYST_PROMPT,
            tools=[
                Tool(
                    name="call_supervisor",
                    description="Call the supervisor to get a final verdict",
                    function=self.call_supervisor
                )
            ],
            # model_settings={
            #     'temperature': 0.1,
            # }
        )

        self.weekly_analyst = Agent(
            'openai:gpt-4o',
            result_type=Output,
            system_prompt=(
                """
                You are a senior technical analyst.
                """
            )
        )

        self.hourly_analyst = Agent(
            'openai:gpt-4o',
            result_type=Output,
            system_prompt=(
                """
                You are a senior technical analyst.
                """
            )
        )

        self.supervisor = Agent(
            'openai:gpt-4o',
            result_type=Output,
            system_prompt=SUPERVISOR_PROMPT,
        )

    async def run_daily_analysis(self, image_data: bytes) -> Output:
        response = await self.daily_analyst.run(
            [
                'Here is the daily chart',
                BinaryContent(image_data, media_type="image/png")
            ]
        )
        return response.data

    async def run_weekly_analysis(self, data) -> Output:
        return await self.weekly_analyst.run(data)

    async def run_hourly_analysis(self, data) -> Output:
        return await self.hourly_analyst.run(data)

    async def call_supervisor(self, ctx: RunContext[str]) -> Output:
        response = await self.supervisor.run(ctx.messages)
        print("Supervisor response: ", response.data)
        return response.data
