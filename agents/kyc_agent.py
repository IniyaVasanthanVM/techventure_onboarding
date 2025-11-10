from agno.agent import Agent

class KYCAgent:
    """
    Banking-Grade KYC/AML Compliance Agent
    Implements comprehensive identity verification and anti-money laundering checks
    following BSA/AML, OFAC, and CIP regulations
    """
    
    def __init__(self):
        self.agent = Agent(
            name="KYC_Agent",
            model="google:gemini-2.0-flash",
            instructions="""You are a banking KYC/AML compliance specialist.
            Perform comprehensive identity verification, sanctions screening, PEP checks,
            and adverse media screening. Assess AML risk based on industry, geography, 
            and transaction patterns."""
        )
        
        # Risk categorization
        self.high_risk_industries = ["crypto", "gambling", "cannabis", "money services", "jewelry"]
        self.medium_risk_industries = ["real estate", "construction", "import/export"]
        self.low_risk_industries = ["saas", "healthcare", "education", "consulting"]
        
    def run(self, input_data):
        """
        Execute comprehensive KYC/AML assessment
        
        Returns:
            - compliance_score: 0-100 score
            - kyc_status: PASSED/FAILED/REVIEW_REQUIRED
            - aml_checks: Detailed check results
            - risk_level: LOW/MEDIUM/HIGH/CRITICAL
            - risk_factors: List of identified risks
        """
        identity = input_data.get("identity", {})
        documents = input_data.get("documents", {})
        industry = input_data.get("industry", "").lower()
        business_profile = input_data.get("business_profile", {})
        business_age = input_data.get("business_age", "")
        
        score = 0
        risk_factors = []
        
        # === Identity Verification (30 points) ===
        if identity.get("id_verified"):
            score += 30
        else:
            risk_factors.append("Identity verification incomplete")
        
        # === PEP & Sanctions Screening (25 points) ===
        pep_status = identity.get("pep_check", "").lower()
        sanctions_status = identity.get("sanctions_check", "").lower()
        
        if pep_status == "clear":
            score += 15
        elif pep_status == "flagged":
            score -= 20
            risk_factors.append("PEP (Politically Exposed Person) flagged")
        
        if sanctions_status == "clear":
            score += 10
        elif sanctions_status == "flagged":
            score = 0  # Auto-fail on sanctions hit
            risk_factors.append("OFAC/Sanctions list match - CRITICAL")
        
        # === Adverse Media Check (10 points) ===
        if not identity.get("adverse_media", True):
            score += 10
        else:
            risk_factors.append("Negative news/adverse media found")
        
        # === Document Verification (15 points) ===
        doc_count = sum([1 for doc in documents.values() if doc])
        if doc_count >= 4:
            score += 15
        elif doc_count == 3:
            score += 10
        elif doc_count == 2:
            score += 5
        else:
            risk_factors.append("Insufficient documentation for identity verification")
        
        # === Industry Risk Assessment (20 points) ===
        if industry in self.high_risk_industries:
            score -= 30
            risk_factors.append(f"High-risk industry: {industry}")
            industry_risk = "HIGH"
        elif industry in self.medium_risk_industries:
            score -= 10
            risk_factors.append(f"Medium-risk industry: {industry}")
            industry_risk = "MEDIUM"
        elif industry in self.low_risk_industries:
            score += 20
            industry_risk = "LOW"
        else:
            score += 10
            industry_risk = "MEDIUM"
        
        # === Transaction Pattern Analysis ===
        avg_transaction = business_profile.get("avg_transaction", 0)
        monthly_volume = business_profile.get("monthly_volume", 0)
        has_international = business_profile.get("international", False)
        high_risk_countries = business_profile.get("high_risk_countries", False)
        
        # Large transaction red flag
        if avg_transaction > 50000:
            risk_factors.append("Large average transaction size - enhanced monitoring required")
            score -= 5
        
        # High volume red flag
        if monthly_volume > 500:
            risk_factors.append("High transaction volume - requires enhanced due diligence")
            score -= 5
        
        # International transactions
        if has_international:
            score -= 5
            risk_factors.append("International transactions - additional scrutiny required")
        
        # High-risk countries (major red flag)
        if high_risk_countries:
            score -= 25
            risk_factors.append("Transactions with high-risk jurisdictions - CRITICAL")
        
        # === Business Maturity Bonus ===
        if "5+" in business_age:
            score += 10
        elif "3-5" in business_age:
            score += 5
        elif "less than 1 year" in business_age.lower():
            score -= 5
            risk_factors.append("New business - limited operating history")
        
        # Normalize score
        score = max(0, min(100, score))
        
        # === Determine Risk Level ===
        if score >= 80:
            risk_level = "LOW"
        elif score >= 60:
            risk_level = "MEDIUM"
        elif score >= 40:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"
        
        # === Determine KYC Status ===
        if sanctions_status == "flagged":
            kyc_status = "FAILED"
        elif score >= 70 and risk_level in ["LOW", "MEDIUM"]:
            kyc_status = "PASSED"
        elif score >= 50:
            kyc_status = "REVIEW_REQUIRED"
        else:
            kyc_status = "FAILED"
        
        # === AML Check Details ===
        aml_checks = {
            "identity_verification": "PASS" if identity.get("id_verified") else "FAIL",
            "pep_screening": pep_status.upper(),
            "sanctions_screening": sanctions_status.upper(),
            "adverse_media": "CLEAR" if not identity.get("adverse_media") else "FLAGGED",
            "industry_risk": industry_risk,
            "transaction_risk": "HIGH" if (avg_transaction > 50000 or high_risk_countries) else "MEDIUM" if has_international else "LOW"
        }
        
        # === Enhanced Due Diligence Requirements ===
        edd_required = False
        if risk_level in ["HIGH", "CRITICAL"] or kyc_status == "REVIEW_REQUIRED":
            edd_required = True
            risk_factors.append("Enhanced Due Diligence (EDD) required")
        
        llm_analysis = self.agent.run(f"Analyze KYC/AML risk for {industry} business. Compliance score: {score}, Risk level: {risk_level}, Risk factors: {risk_factors}. Provide brief assessment in 2 to 3 lines only.")
        llm_response = str(llm_analysis.content) if hasattr(llm_analysis, 'content') else str(llm_analysis)

        return {
            "compliance_score": score,
            "kyc_status": kyc_status,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "aml_checks": aml_checks,
            "edd_required": edd_required,
            "industry_risk": industry_risk,
            "recommendation": "Approve" if kyc_status == "PASSED" else "Reject" if kyc_status == "FAILED" else "Human Review",
            "llm_analysis": llm_response
        }