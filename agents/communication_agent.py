from agno.agent import Agent

class CommunicationAgent:
    def __init__(self):
        self.agent = Agent(
            name="Communication_Agent",
            model="google:gemini-2.0-flash",
            instructions="Generate friendly, short customer communication. Keep it under 3 sentences."
        )
    
    def run(self, input_data):
        status = input_data.get("status", "Processing")
        
        prompt = f"Write a short, friendly customer update about their application status: {status}. Keep it under 3 sentences."
        response = self.agent.run(prompt)
        
        message = str(response.content) if hasattr(response, 'content') else str(response)
        
        return {
            "customer_message": message
        }