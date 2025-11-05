from agno.agent import Agent

class ProductAgent:
    def __init__(self):
        self.agent = Agent(
            name="Product_Agent",
            model="google:gemini-2.0-flash",
            instructions="Recommend banking products based on business profile."
        )
    
    def run(self, input_data):
        industry = input_data.get("industry", "")
        
        if industry.lower() == "saas":
            account = "SaaS Pro Account"
        else:
            account = "Standard Business Account"
            
        return {
            "account_type": account,
            "loan_offer": "Startup Loan - $50K", 
            "credit_card": "Platinum Biz Card"
        }