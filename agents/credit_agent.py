from agno.agent import Agent

class CreditAgent:
    """
    Banking-Grade Credit Risk Assessment Agent
    Implements comprehensive credit scoring using financial ratios, 
    cash flow analysis, and industry-specific risk models
    """
    
    def __init__(self):
        self.agent = Agent(
            name="Credit_Agent",
            model="google:gemini-2.0-flash",
            instructions="""You are a banking credit risk analyst.
            Evaluate creditworthiness using financial statements, debt ratios,
            cash flow analysis, and business performance metrics.
            Apply industry-specific credit models."""
        )
        
    def run(self, input_data):
        """
        Execute comprehensive credit risk assessment
        
        Returns:
            - credit_score: 0-100 score
            - risk_level: LOW/MEDIUM/HIGH/VERY_HIGH
            - credit_limit: Recommended credit limit
            - interest_rate: Recommended rate
            - financial_ratios: Key metrics
            - risk_factors: Identified concerns
        """
        financials = input_data.get("financials", {})
        revenue = financials.get("revenue", 0)
        debt = financials.get("debt", 0)
        cash_flow_positive = financials.get("cash_flow_positive", False)
        debt_to_income = financials.get("debt_to_income", 0)
        
        business_age = input_data.get("business_age", "")
        industry = input_data.get("industry", "").lower()
        employees = input_data.get("employees", 0)
        documents = input_data.get("documents", {})
        
        score = 0
        risk_factors = []
        
        # === Revenue Analysis (30 points) ===
        if revenue >= 10000000:
            score += 30
            revenue_tier = "Tier 1 - Large Enterprise"
        elif revenue >= 5000000:
            score += 25
            revenue_tier = "Tier 2 - Mid-Market"
        elif revenue >= 1000000:
            score += 20
            revenue_tier = "Tier 3 - Small Business"
        elif revenue >= 500000:
            score += 15
            revenue_tier = "Tier 4 - Micro Business"
        elif revenue >= 100000:
            score += 10
            revenue_tier = "Tier 5 - Startup"
        else:
            score += 5
            revenue_tier = "Tier 6 - Early Stage"
            risk_factors.append("Very low revenue - high credit risk")
        
        # === Debt Analysis (25 points) ===
        # Calculate debt-to-income ratio if not provided
        if debt_to_income == 0 and revenue > 0:
            debt_to_income = debt / revenue
        
        if debt_to_income <= 0.2:
            score += 25
            debt_rating = "Excellent"
        elif debt_to_income <= 0.4:
            score += 20
            debt_rating = "Good"
        elif debt_to_income <= 0.6:
            score += 15
            debt_rating = "Fair"
            risk_factors.append("Moderate debt burden")
        elif debt_to_income <= 0.8:
            score += 8
            debt_rating = "Poor"
            risk_factors.append("High debt-to-income ratio")
        else:
            score += 0
            debt_rating = "Very Poor"
            risk_factors.append("Excessive debt burden - major concern")
        
        # === Cash Flow Analysis (20 points) ===
        if cash_flow_positive:
            score += 20
        else:
            score += 0
            risk_factors.append("Negative cash flow - unable to meet obligations")
        
        # === Business Maturity (15 points) ===
        if "5+" in business_age:
            score += 15
            maturity_rating = "Mature"
        elif "3-5" in business_age:
            score += 12
            maturity_rating = "Established"
        elif "1-2" in business_age:
            score += 7
            maturity_rating = "Growing"
            risk_factors.append("Limited operating history")
        else:
            score += 3
            maturity_rating = "New"
            risk_factors.append("New business - insufficient track record")
        
        # === Industry Risk Assessment (10 points) ===
        stable_industries = ["healthcare", "education", "saas", "consulting"]
        volatile_industries = ["restaurant", "retail", "construction"]
        high_risk_industries = ["crypto", "gambling", "cannabis"]
        
        if industry in stable_industries:
            score += 10
            industry_risk = "Low"
        elif industry in volatile_industries:
            score += 5
            industry_risk = "Medium"
            risk_factors.append(f"Volatile industry: {industry}")
        elif industry in high_risk_industries:
            score += 0
            industry_risk = "High"
            risk_factors.append(f"High-risk industry: {industry} - requires enhanced monitoring")
        else:
            score += 7
            industry_risk = "Medium"
        
        # === Financial Documentation (Bonus) ===
        if documents.get("financial_statement") and documents.get("bank_statement"):
            score += 5  # Bonus for complete financial docs
        elif not documents.get("bank_statement"):
            risk_factors.append("No bank statements - limited financial visibility")
        
        # === Employee Base Assessment ===
        if employees >= 50:
            score += 5  # Larger operation bonus
        elif employees < 5:
            risk_factors.append("Very small team - operational risk")
        
        # === Calculate Financial Ratios ===
        financial_ratios = {
            "debt_to_income_ratio": round(debt_to_income, 3),
            "revenue_per_employee": round(revenue / employees if employees > 0 else 0, 0),
            "debt_to_revenue_pct": round((debt / revenue * 100) if revenue > 0 else 0, 1)
        }
        
        # Normalize score
        score = max(0, min(100, score))
        
        # === Determine Risk Level ===
        if score >= 80:
            risk_level = "LOW"
        elif score >= 65:
            risk_level = "MEDIUM"
        elif score >= 50:
            risk_level = "HIGH"
        else:
            risk_level = "VERY_HIGH"
        
        # === Calculate Credit Limit ===
        # Base credit limit on revenue and risk level
        base_limit = revenue * 0.1  # 10% of annual revenue as baseline
        
        if risk_level == "LOW":
            credit_limit = base_limit * 1.5
            interest_rate = 6.5
        elif risk_level == "MEDIUM":
            credit_limit = base_limit * 1.0
            interest_rate = 8.5
        elif risk_level == "HIGH":
            credit_limit = base_limit * 0.5
            interest_rate = 12.0
        else:
            credit_limit = base_limit * 0.25
            interest_rate = 15.0
        
        # Cap credit limits based on maturity
        if "less than 1 year" in business_age.lower():
            credit_limit = min(credit_limit, 50000)
        elif "1-2" in business_age:
            credit_limit = min(credit_limit, 150000)
        
        credit_limit = round(credit_limit, -3)  # Round to nearest thousand
        
        # === Credit Decision ===
        if score >= 70:
            credit_decision = "APPROVE"
        elif score >= 50:
            credit_decision = "CONDITIONAL_APPROVE"
            risk_factors.append("Conditional approval - requires monitoring")
        else:
            credit_decision = "REJECT"
        
        # === Loan Products ===
        loan_products = []
        if score >= 75:
            loan_products = ["Business Line of Credit", "Term Loan", "Equipment Financing"]
        elif score >= 60:
            loan_products = ["Secured Line of Credit", "Invoice Financing"]
        elif score >= 50:
            loan_products = ["Merchant Cash Advance (Higher Rate)"]
        else:
            loan_products = ["Not Eligible"]
        
        llm_analysis = self.agent.run(f"Analyze credit risk for business with revenue ₹{revenue/100000:.1f}L, debt ratio {debt_to_income:.2f}, credit score {score}. Risk level: {risk_level}. Provide brief assessment in 2 to 3 lines only.")
        llm_response = str(llm_analysis.content) if hasattr(llm_analysis, 'content') else str(llm_analysis)

        return {
            "credit_score": score,
            "risk_level": risk_level,
            "credit_limit": credit_limit,
            "interest_rate": interest_rate,
            "credit_decision": credit_decision,
            "financial_ratios": financial_ratios,
            "risk_factors": risk_factors,
            "revenue_tier": revenue_tier,
            "debt_rating": debt_rating,
            "maturity_rating": maturity_rating,
            "industry_risk": industry_risk,
            "loan_products": loan_products,
            "monitoring_required": risk_level in ["HIGH", "VERY_HIGH"],
            "llm_analysis": llm_response
        }