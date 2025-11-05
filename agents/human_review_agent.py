from agno.agent import Agent

class HumanReviewAgent:
    def __init__(self):
        self.agent = Agent(
            name="Human_Review_Agent",
            model="google:gemini-2.0-flash", 
            instructions="Prepare case summary for human review."
        )
    
    def run(self, input_data):
        summary = {
            "kyc": input_data.get("kyc_status"),
            "credit": input_data.get("credit_score"),
            "compliance": input_data.get("compliance_score"),
            "documents": input_data.get("documents_status"),
            "recommendation": input_data.get("recommendation")
        }
        
        return {
            "summary": summary,
            "options": ["Approve", "Reject", "Request More Info"]
        }