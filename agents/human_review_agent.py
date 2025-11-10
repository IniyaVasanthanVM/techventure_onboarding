from agno.agent import Agent

class HumanReviewAgent:
    """
    Human Review Preparation Agent
    Prepares comprehensive case summaries and recommendations
    for manual review by banking officers
    """
    
    def __init__(self):
        self.agent = Agent(
            name="Human_Review_Agent",
            model="google:gemini-2.0-flash",
            instructions="""You are a senior banking analyst preparing cases for human review.
            Summarize all relevant information clearly and concisely.
            Highlight key decision factors, risks, and recommendations."""
        )
    
    def run(self, input_data):
        """
        Prepare comprehensive review package
        
        Returns:
            - summary: Condensed overview of all assessments
            - options: Available decision options
            - key_concerns: Critical items requiring attention
            - recommended_action: Suggested decision
            - priority: Review priority level
            - reviewer_notes: Pre-filled analysis
        """
        
        # Extract all relevant data
        credit_score = input_data.get("credit_score", 0)
        compliance_score = input_data.get("compliance_score", 0)
        kyc_status = input_data.get("kyc_status", "UNKNOWN")
        documents_status = input_data.get("documents_status", "UNKNOWN")
        risk_level = input_data.get("risk_level", "UNKNOWN")
        risk_factors = input_data.get("risk_factors", [])
        decision = input_data.get("decision", "UNKNOWN")
        reasoning = input_data.get("reasoning", "")
        
        # Additional details
        aml_checks = input_data.get("aml_checks", {})
        financial_ratios = input_data.get("financial_ratios", {})
        credit_limit = input_data.get("credit_limit", 0)
        edd_required = input_data.get("edd_required", False)
        
        # ========================================
        # Create Executive Summary
        # ========================================
        
        summary = {
            "kyc": kyc_status,
            "credit": credit_score,
            "compliance": compliance_score,
            "documents": documents_status,
            "risk_level": risk_level,
            "recommendation": decision,
            "credit_limit": credit_limit
        }
        
        # ========================================
        # Identify Key Concerns
        # ========================================
        
        key_concerns = []
        
        # Critical concerns
        if compliance_score < 70:
            key_concerns.append(f"⚠️ LOW COMPLIANCE SCORE: {compliance_score}/100")
        
        if credit_score < 60:
            key_concerns.append(f"⚠️ LOW CREDIT SCORE: {credit_score}/100")
        
        if edd_required:
            key_concerns.append("⚠️ ENHANCED DUE DILIGENCE REQUIRED")
        
        if aml_checks.get("pep_screening") == "FLAGGED":
            key_concerns.append("⚠️ PEP (POLITICALLY EXPOSED PERSON) DETECTED")
        
        if aml_checks.get("adverse_media") == "FLAGGED":
            key_concerns.append("⚠️ ADVERSE MEDIA FOUND")
        
        if risk_level in ["HIGH", "CRITICAL"]:
            key_concerns.append(f"⚠️ HIGH RISK CLASSIFICATION: {risk_level}")
        
        # Add specific risk factors
        for risk in risk_factors[:5]:  # Top 5 risks
            if risk not in str(key_concerns):  # Avoid duplicates
                key_concerns.append(f"• {risk}")
        
        # ========================================
        # Determine Priority Level
        # ========================================
        
        if (aml_checks.get("pep_screening") == "FLAGGED" or 
            edd_required or 
            risk_level == "CRITICAL"):
            priority = "🔴 HIGH PRIORITY - Immediate Review Required"
        elif credit_score < 60 or compliance_score < 65:
            priority = "🟡 MEDIUM PRIORITY - Review within 24 hours"
        else:
            priority = "🟢 STANDARD PRIORITY - Review within 48 hours"
        
        # ========================================
        # Generate Recommended Action
        # ========================================
        
        if compliance_score >= 70 and credit_score >= 65 and risk_level in ["LOW", "MEDIUM"]:
            recommended_action = "APPROVE"
            recommendation_rationale = "Scores meet approval thresholds. Acceptable risk profile."
        elif compliance_score < 60 or credit_score < 50 or risk_level == "CRITICAL":
            recommended_action = "REJECT"
            recommendation_rationale = "Significant risk factors present. Does not meet minimum standards."
        else:
            recommended_action = "REQUEST_MORE_INFO"
            recommendation_rationale = "Additional information needed to make informed decision."
        
        # ========================================
        # Prepare Reviewer Notes
        # ========================================
        
        reviewer_notes = f"""
APPLICATION REVIEW SUMMARY
=========================

OVERALL ASSESSMENT:
{reasoning}

KEY METRICS:
- Credit Score: {credit_score}/100 [{self._score_rating(credit_score)}]
- Compliance Score: {compliance_score}/100 [{self._score_rating(compliance_score)}]
- Risk Level: {risk_level}
- Proposed Credit Limit: ${credit_limit:,.0f}

AML/KYC CHECKS:
- Identity Verification: {aml_checks.get('identity_verification', 'N/A')}
- PEP Screening: {aml_checks.get('pep_screening', 'N/A')}
- Sanctions Screening: {aml_checks.get('sanctions_screening', 'N/A')}
- Adverse Media: {aml_checks.get('adverse_media', 'N/A')}
- Industry Risk: {aml_checks.get('industry_risk', 'N/A')}

FINANCIAL ANALYSIS:
- Debt-to-Income: {financial_ratios.get('debt_to_income_ratio', 'N/A')}
- Revenue/Employee: ${financial_ratios.get('revenue_per_employee', 0):,.0f}

RISK FACTORS:
{chr(10).join([f'- {rf}' for rf in risk_factors]) if risk_factors else '- None identified'}

AI RECOMMENDATION: {recommended_action}
Rationale: {recommendation_rationale}
"""
        
        # ========================================
        # Decision Options
        # ========================================
        
        options = [
            "Approve",
            "Approve with Conditions",
            "Reject",
            "Request More Information"
        ]
        
        # ========================================
        # Additional Documentation Suggestions
        # ========================================
        
        suggested_docs = []
        
        if credit_score < 65:
            suggested_docs.append("Updated Financial Statements")
            suggested_docs.append("Cash Flow Projections")
        
        if edd_required:
            suggested_docs.append("Source of Funds Documentation")
            suggested_docs.append("Beneficial Ownership Information")
        
        if aml_checks.get("pep_screening") == "FLAGGED":
            suggested_docs.append("PEP Risk Assessment Form")
            suggested_docs.append("Enhanced Background Check")
        
        llm_analysis = self.agent.run(f"Prepare review summary for human officer. Credit: {credit_score}, Compliance: {compliance_score}, Risk: {risk_level}, Key concerns: {key_concerns}. Provide recommendation in 2 to 3 lines only.")
        llm_response = str(llm_analysis.content) if hasattr(llm_analysis, 'content') else str(llm_analysis)

        return {
            "summary": summary,
            "options": options,
            "key_concerns": key_concerns,
            "recommended_action": recommended_action,
            "recommendation_rationale": recommendation_rationale,
            "priority": priority,
            "reviewer_notes": reviewer_notes,
            "suggested_additional_docs": suggested_docs,
            "review_required_by": "Banking Officer or Senior Underwriter",
            "escalation_required": edd_required or risk_level == "CRITICAL",
            "llm_analysis": llm_response
        }
    
    def _score_rating(self, score):
        """Convert numeric score to rating"""
        if score >= 80:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 60:
            return "Fair"
        elif score >= 50:
            return "Poor"
        else:
            return "Very Poor"