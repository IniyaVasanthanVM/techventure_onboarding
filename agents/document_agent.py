from agno.agent import Agent
import re

class DocumentAgent:
    """
    Banking-Grade Document Verification Agent
    Implements comprehensive document validation following regulatory standards
    """
    
    def __init__(self):
        self.agent = Agent(
            name="Document_Agent",
            model="google:gemini-2.0-flash",
            instructions="""You are a banking document verification specialist.
            Analyze business documents for completeness, validity, and regulatory compliance.
            Check for red flags, inconsistencies, and missing critical information."""
        )
        
        # Required documents by category
        self.critical_docs = ["tax_id", "license", "bank_statement"]
        self.recommended_docs = ["financial_statement"]
        
    def run(self, input_data):
        """
        Execute document verification with banking standards
        
        Returns:
            - extracted_data: Document inventory
            - missing_fields: Critical missing documents
            - warnings: Non-critical missing documents
            - complete: Overall completeness status
            - verification_score: 0-100 score
            - status: COMPLETE/INCOMPLETE/CRITICAL_MISSING
        """
        documents = input_data.get("documents", {})
        business_age = input_data.get("business_age", "")
        industry = input_data.get("industry", "").lower()
        
        # Extract document status
        extracted = {
            "tax_id": documents.get("tax_id", False),
            "license": documents.get("license", False),
            "bank_statement": documents.get("bank_statement", False),
            "financial_statement": documents.get("financial_statement", False)
        }
        
        # Identify missing documents
        missing_critical = [k for k in self.critical_docs if not extracted.get(k)]
        missing_recommended = [k for k in self.recommended_docs if not extracted.get(k)]
        
        # Calculate verification score
        score = 0
        
        # Critical documents (70 points total)
        if extracted.get("tax_id"):
            score += 25  # EIN is mandatory
        if extracted.get("license"):
            score += 25  # Business license verification
        if extracted.get("bank_statement"):
            score += 20  # Banking history critical
            
        # Recommended documents (30 points)
        if extracted.get("financial_statement"):
            score += 30
        
        # Bonus for mature businesses with all docs
        if "5+" in business_age and score >= 90:
            score = min(100, score + 10)
        
        # Penalty for high-risk industries without full documentation
        if industry in ["crypto", "gambling", "cannabis"] and score < 100:
            score -= 10
            score = max(0, score)
        
        # Determine status
        complete = len(missing_critical) == 0
        
        if missing_critical:
            status = "CRITICAL_MISSING"
        elif missing_recommended:
            status = "INCOMPLETE"
        else:
            status = "COMPLETE"
        
        # Generate warnings
        warnings = []
        if missing_recommended:
            warnings.append(f"Recommended documents missing: {', '.join(missing_recommended)}")
        
        if not extracted.get("bank_statement"):
            warnings.append("Banking history unavailable - limits credit assessment")
        
        if industry in ["crypto", "gambling"] and not extracted.get("financial_statement"):
            warnings.append("High-risk industry requires enhanced documentation")
        
        # Document quality assessment
        quality_issues = []
        if "less than 1 year" in business_age.lower() and not extracted.get("financial_statement"):
            quality_issues.append("New business requires financial projections")

        llm_analysis = self.agent.run(f"Analyze these documents for a {industry} business with {business_age} operating history: {extracted}. Provide risk assessment in 2 to 3 lines only.")
        llm_response = str(llm_analysis.content) if hasattr(llm_analysis, 'content') else str(llm_analysis)

        
        return {
            "extracted_data": extracted,
            "missing_fields": missing_critical,
            "warnings": warnings,
            "quality_issues": quality_issues,
            "complete": complete,
            "verification_score": score,
            "status": status,
            "total_documents": sum([1 for v in extracted.values() if v]),
            "required_documents": len(self.critical_docs),
            "llm_analysis": llm_response
        }