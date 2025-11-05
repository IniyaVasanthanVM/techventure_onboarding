from agno.agent import Agent

class CreditAgent:
    def __init__(self):
        self.agent = Agent(
            name="Credit_Agent",
            model="google:gemini-2.0-flash", 
            instructions="Analyze creditworthiness and financial health. Return credit_score between 0-100."
        )
    
    def run(self, input_data):
        financials = input_data.get("financials", {})
        revenue = financials.get("revenue", 0)
        debt = financials.get("debt", 0)
        business_age = input_data.get("business_age", "")
        
        score = 50 
        
        if revenue > 5000000:
            score += 30
        elif revenue > 1000000:
            score += 20
        elif revenue > 500000:
            score += 10
            
        if debt < 50000:
            score += 20
        elif debt < 200000:
            score += 10
            
        if "5+" in business_age:
            score += 15
        elif "3-5" in business_age:
            score += 10
        elif "1-2" in business_age:
            score += 5
            
        score = max(0, min(100, score))
        
        return {
            "credit_score": score
        }