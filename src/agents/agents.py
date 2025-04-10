from pydantic_ai import Agent, RunContext, BinaryContent, Tool
from fastapi import UploadFile
from dataclasses import dataclass

from pydantic import BaseModel
from typing import Literal

import logfire

from src.agents.prompts import (
    DAILY_ANALYST_PROMPT,
    WEEKLY_ANALYST_PROMPT,
    SUPERVISOR_PROMPT,
    HOURLY_ANALYST_PROMPT,
)

logfire.configure()
Agent.instrument_all()


class Output(BaseModel):
    trade_direction: Literal["long", "short"]
    entry_price: float
    stop_loss_price: float
    take_profit_price: float
    reason: str


class SupervisorOutput(BaseModel):
    verdict: Literal["buy", "sell", "hold"]
    reason: str


@dataclass
class Deps:
    image_data: bytes


class Agents:
    def __init__(self):
        self.hourly_analyst = Agent(
            "openai:gpt-4o",
            result_type=Output,
            system_prompt=HOURLY_ANALYST_PROMPT,
            tools=[
                Tool(
                    name="call_supervisor",
                    description="Call the supervisor to get a final verdict",
                    function=self.call_supervisor,
                )
            ],
        )

        self.daily_analyst = Agent(
            "openai:gpt-4o",
            result_type=Output,
            system_prompt=DAILY_ANALYST_PROMPT,
            tools=[
                Tool(
                    name="call_supervisor",
                    description="Call the supervisor to get a final verdict",
                    function=self.call_supervisor,
                )
            ],
        )

        self.weekly_analyst = Agent(
            "openai:gpt-4o",
            result_type=Output,
            system_prompt=WEEKLY_ANALYST_PROMPT,
            tools=[
                Tool(
                    name="call_supervisor",
                    description="Call the supervisor to get a final verdict",
                    function=self.call_supervisor,
                )
            ],
        )

        self.supervisor = Agent(
            "openai:gpt-4o",
            system_prompt=SUPERVISOR_PROMPT,
        )

    async def run_hourly_analysis(self, image: UploadFile) -> Output:
        print("Running hourly analysis")

        file_content = await image.read()

        deps = Deps(image_data=file_content)

        response = await self.hourly_analyst.run(
            [
                "Here is the hourly chart",
                BinaryContent(file_content, media_type="image/png"),
            ],
            deps=deps,
        )
        print("Hourly analyst response: ", response.data)
        return response.data

    async def run_daily_analysis(self, image: UploadFile) -> Output:
        print("Running daily analysis")

        file_content = await image.read()

        deps = Deps(image_data=file_content)

        response = await self.daily_analyst.run(
            [
                "Here is the daily chart",
                BinaryContent(file_content, media_type="image/png"),
            ],
            deps=deps,
        )
        print("Daily analyst response: ", response.data)
        return response.data

    async def run_weekly_analysis(self, image: UploadFile) -> Output:
        print("Running weekly analysis")

        file_content = await image.read()

        deps = Deps(image_data=file_content)

        response = await self.weekly_analyst.run(
            [
                "Here is the weekly chart",
                BinaryContent(file_content, media_type="image/png"),
            ],
            deps=deps,
        )
        print("Weekly analyst response: ", response.data)
        return response.data

    # Tool function
    async def call_supervisor(self, ctx: RunContext[Deps], analysis: Output) -> Output:
        """Get the final verdict from the supervisor

        Args:
            ctx: The context
            analysis: The analysis from the daily analyst

        Returns:
            The final verdict from the supervisor
        """

        print("Supervisor running")
        print("Analysis: ", analysis)

        response = await self.supervisor.run(
            [
                f"""
                Check the analyst report and give a final verdict
                Analyst report: {analysis}

                Here is the image:
            """,
                BinaryContent(ctx.deps.image_data, media_type="image/png"),
            ],
            deps=ctx.deps,
            usage=ctx.usage,
        )

        print("Supervisor response: ", response.data)
        return response.data
