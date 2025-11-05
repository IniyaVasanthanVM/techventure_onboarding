from agno.agent import Agent

class OrchestratorAgent:
    def __init__(self):
        self.agent = Agent(
            name="Orchestrator",
            model="google:gemini-2.0-flash",
            instructions="Make final decision based on all agent outputs. Return APPROVE, REJECT, or HUMAN_REVIEW with clear reason."
        )
    
    def run(self, input_data):
        credit_score = input_data.get('credit_score', 0)
        compliance_score = input_data.get('compliance_score', 0)
        documents_complete = input_data.get('complete', False)
        industry = input_data.get('industry', '').lower()
        
        if compliance_score < 50:
            decision = "REJECT"
            reason = f"Compliance score too low: {compliance_score}/100"
        elif credit_score < 50:
            decision = "REJECT" 
            reason = f"Credit score too low: {credit_score}/100"
        elif not documents_complete:
            decision = "REJECT"
            reason = "Incomplete documentation"
        elif industry in ["crypto", "gambling"]:
            decision = "REJECT"
            reason = f"High-risk industry: {industry}"
        elif 60 <= credit_score <= 75 or 60 <= compliance_score <= 75:
            decision = "HUMAN_REVIEW"
            reason = f"Borderline scores - Credit: {credit_score}, Compliance: {compliance_score}"
        else:
            decision = "APPROVE"
            reason = f"Strong application - Credit: {credit_score}, Compliance: {compliance_score}"
        
        hitl_required = (decision == "HUMAN_REVIEW")
        
        return {
            "decision": decision,
            "reasoning": reason,
            "hitl_required": hitl_required
        }