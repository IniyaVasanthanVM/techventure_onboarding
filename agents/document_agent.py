from agno.agent import Agent

class DocumentAgent:
    def __init__(self):
        self.agent = Agent(
            name="Document_Agent",
            model="google:gemini-2.0-flash",
            instructions="Analyze business documents for completeness and validity."
        )
    
    def run(self, input_data):
        documents = input_data.get("documents", {})
        
        extracted = {
            "tax_id": documents.get("tax_id"),
            "license": documents.get("license"), 
            "bank_statement": documents.get("bank_statement")
        }
        
        missing = [k for k, v in extracted.items() if not v]
        complete = len(missing) == 0
        
        return {
            "extracted_data": extracted,
            "missing_fields": missing,
            "complete": complete
        }