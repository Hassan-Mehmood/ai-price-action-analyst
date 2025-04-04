from src.agents.agents import Agents

class AnalysisService:
    def __init__(self):
        self.agents = Agents()

    async def analyze_daily(self, image_data: bytes):
        try:
            result = await self.agents.run_daily_analysis(image_data=image_data)
            return result
        except Exception as e:
            # Log the error and return a proper error response
            raise Exception(f"Error during daily analysis: {str(e)}") 