from agno.agent import Agent

class KYCAgent:
    def __init__(self):
        self.agent = Agent(
            name="KYC_Agent", 
            model="google:gemini-2.0-flash",
            instructions="Perform KYC checks and identity verification. Return compliance_score between 0-100."
        )
    
    def run(self, input_data):
        identity = input_data.get("identity", {})
        documents = input_data.get("documents", {})
        industry = input_data.get("industry", "").lower()
        
        score = 50 
        
        if identity.get("id_verified"):
            score += 20
        if identity.get("pep_check") == "clear":
            score += 15
            
        doc_count = sum([1 for doc in documents.values() if doc])
        if doc_count == 3:
            score += 15
        elif doc_count == 2:
            score += 10
        elif doc_count == 1:
            score += 5
            
        if industry in ["crypto", "gambling"]:
            score -= 20
        elif industry in ["saas", "healthcare"]:
            score += 5
            
        score = max(0, min(100, score))
        
        return {
            "compliance_score": score,
            "kyc_status": "PASSED" if score >= 70 else "FAILED"
        }