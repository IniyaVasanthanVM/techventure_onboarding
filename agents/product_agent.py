from agno.agent import Agent

class ProductAgent:
    """
    Banking Product Recommendation Agent
    Matches customers with appropriate banking products based on
    business profile, risk assessment, and credit evaluation
    """
    
    def __init__(self):
        self.agent = Agent(
            name="Product_Agent",
            model="google:gemini-2.0-flash",
            instructions="""You are a banking product specialist.
            Recommend appropriate banking products, account types, credit facilities,
            and services based on business profile, industry, and risk assessment."""
        )
        
        # Product catalog
        self.account_types = {
            "premium": "Premium Business Banking",
            "standard": "Standard Business Account",
            "basic": "Basic Business Checking",
            "startup": "Startup Business Account"
        }
        
        self.credit_products = {
            "tier1": ["Business Line of Credit ($250K+)", "Term Loan", "Equipment Financing", "Commercial Real Estate Loan"],
            "tier2": ["Business Line of Credit ($100K)", "Term Loan", "Invoice Financing"],
            "tier3": ["Secured Line of Credit ($50K)", "Invoice Financing", "Equipment Loan"],
            "tier4": ["Secured Credit Card", "Merchant Cash Advance"],
            "none": ["Not Eligible - Build Business History"]
        }
        
        self.credit_cards = {
            "platinum": "Platinum Business Card (3% cashback)",
            "gold": "Gold Business Card (2% cashback)",
            "standard": "Standard Business Card (1% cashback)",
            "secured": "Secured Business Card"
        }
    
    def run(self, input_data):
        """
        Recommend appropriate banking products
        
        Returns:
            - account_type: Recommended business account
            - credit_products: List of available credit products
            - credit_card: Recommended card
            - additional_services: Value-added services
            - pricing_tier: Fee structure tier
        """
        
        industry = input_data.get("industry", "").lower()
        revenue = input_data.get("financials", {}).get("revenue", 0)
        credit_score = input_data.get("credit_score", 0)
        compliance_score = input_data.get("compliance_score", 0)
        risk_level = input_data.get("risk_level", "UNKNOWN")
        employees = input_data.get("employees", 0)
        business_age = input_data.get("business_age", "")
        credit_limit = input_data.get("credit_limit", 0)
        
        # ========================================
        # Account Type Recommendation
        # ========================================
        
        if revenue >= 5000000 and credit_score >= 75:
            account_type = self.account_types["premium"]
            pricing_tier = "Tier 1 - Premium (Fees waived)"
        elif revenue >= 1000000 and credit_score >= 60:
            account_type = self.account_types["standard"]
            pricing_tier = "Tier 2 - Standard ($25/month)"
        elif revenue >= 500000 or "3-5" in business_age or "5+" in business_age:
            account_type = self.account_types["standard"]
            pricing_tier = "Tier 3 - Standard ($25/month)"
        else:
            account_type = self.account_types["basic"]
            pricing_tier = "Tier 4 - Basic ($15/month)"
        
        # Startup special program
        if "less than 1 year" in business_age.lower() and industry in ["saas", "tech", "consulting"]:
            account_type = self.account_types["startup"]
            pricing_tier = "Startup Program (Fees waived 1st year)"
        
        # ========================================
        # Credit Products Recommendation
        # ========================================
        
        if credit_score >= 80 and compliance_score >= 80 and revenue >= 2000000:
            credit_tier = "tier1"
            loan_products = self.credit_products["tier1"]
        elif credit_score >= 70 and compliance_score >= 70 and revenue >= 1000000:
            credit_tier = "tier2"
            loan_products = self.credit_products["tier2"]
        elif credit_score >= 60 and compliance_score >= 60 and revenue >= 500000:
            credit_tier = "tier3"
            loan_products = self.credit_products["tier3"]
        elif credit_score >= 50 and compliance_score >= 60:
            credit_tier = "tier4"
            loan_products = self.credit_products["tier4"]
        else:
            credit_tier = "none"
            loan_products = self.credit_products["none"]
        
        # ========================================
        # Credit Card Recommendation
        # ========================================
        
        if credit_score >= 80 and risk_level == "LOW":
            credit_card = self.credit_cards["platinum"]
            card_limit = min(credit_limit * 0.3, 100000)
        elif credit_score >= 70:
            credit_card = self.credit_cards["gold"]
            card_limit = min(credit_limit * 0.25, 50000)
        elif credit_score >= 60:
            credit_card = self.credit_cards["standard"]
            card_limit = min(credit_limit * 0.2, 25000)
        else:
            credit_card = self.credit_cards["secured"]
            card_limit = 5000
        
        card_limit = round(card_limit, -3)  # Round to nearest thousand
        
        # ========================================
        # Industry-Specific Recommendations
        # ========================================
        
        additional_services = []
        
        if industry in ["saas", "tech", "software"]:
            additional_services.extend([
                "ACH/Wire Transfer Services",
                "International Payment Gateway",
                "API Banking Integration",
                "Treasury Management"
            ])
        
        if industry in ["retail", "e-commerce", "restaurant"]:
            additional_services.extend([
                "Merchant Services (2.5% processing)",
                "Point of Sale Financing",
                "Same-Day Deposits",
                "Inventory Financing"
            ])
        
        if industry in ["manufacturing", "construction"]:
            additional_services.extend([
                "Equipment Financing",
                "Payroll Services",
                "Fleet Card Services",
                "Supply Chain Financing"
            ])
        
        if industry in ["healthcare", "professional services"]:
            additional_services.extend([
                "Lockbox Services",
                "ACH Collections",
                "Professional Liability Insurance",
                "Retirement Plan Services"
            ])
        
        # Universal services for all accounts
        additional_services.extend([
            "Mobile Banking",
            "Bill Pay Services",
            "Remote Deposit Capture"
        ])
        
        # Premium services for high-value clients
        if revenue >= 5000000:
            additional_services.extend([
                "Dedicated Relationship Manager",
                "Foreign Exchange Services",
                "Cash Management Services",
                "Commercial Insurance Brokerage"
            ])
        
        # ========================================
        # Special Programs
        # ========================================
        
        special_programs = []
        
        if "less than 1 year" in business_age.lower():
            special_programs.append("New Business Support Program")
        
        if employees >= 50:
            special_programs.append("Large Employer Program - Payroll & Benefits")
        
        if industry in ["saas", "tech"]:
            special_programs.append("Innovation Banking - VC/PE Connections")
        
        if revenue >= 10000000:
            special_programs.append("Corporate Banking Services")
        
        # ========================================
        # Value Proposition
        # ========================================
        
        value_proposition = self._generate_value_prop(
            account_type, credit_tier, industry, revenue
        )
        
        llm_analysis = self.agent.run(f"Recommend best banking products for {industry} business with revenue ₹{revenue/100000:.1f}L, credit score {credit_score}. Account: {account_type}, Products: {loan_products}. Provide brief rationale in 2 to 3 lines only.")
        llm_response = str(llm_analysis.content) if hasattr(llm_analysis, 'content') else str(llm_analysis)

        return {
            "account_type": account_type,
            "pricing_tier": pricing_tier,
            "loan_products": loan_products,
            "credit_tier": credit_tier,
            "credit_card": credit_card,
            "card_limit": card_limit,
            "additional_services": additional_services,
            "special_programs": special_programs,
            "value_proposition": value_proposition,
            "recommended_credit_limit": credit_limit,
            "llm_analysis": llm_response
        }
    
    def _generate_value_prop(self, account_type, credit_tier, industry, revenue):
        """Generate personalized value proposition"""
        
        if "Premium" in account_type:
            return f"Premium banking designed for established {industry} businesses. Waived fees, dedicated support, and exclusive financing."
        elif "Startup" in account_type:
            return f"Specialized banking for growing {industry} startups. First year free, mentorship access, and flexible credit."
        else:
            return f"Comprehensive banking solutions for {industry} businesses. Competitive rates and full-service support."