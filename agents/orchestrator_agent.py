from agno.agent import Agent

class OrchestratorAgent:
    """
    Banking-Grade Decision Orchestrator
    Implements comprehensive decision logic with multiple approval gates,
    risk-based routing, and regulatory compliance checks
    """
    
    def __init__(self):
        self.agent = Agent(
            name="Orchestrator",
            model="google:gemini-2.0-flash",
            instructions="""You are a senior banking operations manager.
            Make final credit decisions based on comprehensive risk assessment.
            Consider KYC/AML compliance, credit risk, document verification,
            and regulatory requirements. Apply risk-based decision framework."""
        )
        
        # Decision thresholds
        self.AUTO_APPROVE_THRESHOLD = {
            "credit_score": 75,
            "compliance_score": 80,
            "risk_level": ["LOW"]
        }
        
        self.AUTO_REJECT_THRESHOLD = {
            "credit_score": 45,
            "compliance_score": 50,
            "kyc_status": ["FAILED"]
        }
        
    def run(self, input_data):
        """
        Execute comprehensive decision orchestration
        
        Decision Framework:
        1. Hard stops (regulatory/compliance failures)
        2. Risk scoring and aggregation
        3. Business rule evaluation
        4. Final decision with routing
        
        Returns:
            - decision: APPROVE/REJECT/HUMAN_REVIEW
            - reasoning: Detailed explanation
            - hitl_required: Boolean
            - risk_factors: Aggregated risks
            - approval_conditions: Any conditions for approval
        """
        
        # Extract all agent outputs
        credit_score = input_data.get('credit_score', 0)
        compliance_score = input_data.get('compliance_score', 0)
        documents_complete = input_data.get('complete', False)
        kyc_status = input_data.get('kyc_status', '')
        risk_level = input_data.get('risk_level', 'UNKNOWN')
        credit_risk = input_data.get('risk_level', 'UNKNOWN')  # From credit agent
        
        # Aggregate risk factors
        risk_factors = []
        risk_factors.extend(input_data.get('risk_factors', []))
        
        # Get detailed analysis
        aml_checks = input_data.get('aml_checks', {})
        credit_decision = input_data.get('credit_decision', '')
        edd_required = input_data.get('edd_required', False)
        financial_ratios = input_data.get('financial_ratios', {})
        
        decision = None
        reasoning = ""
        hitl_required = False
        approval_conditions = []
        
        # ========================================
        # STAGE 1: HARD STOPS (Auto-Reject)
        # ========================================
        
        # Check 1: Sanctions/OFAC Hit (Immediate Rejection)
        if aml_checks.get('sanctions_screening') == 'FLAGGED':
            decision = "REJECT"
            reasoning = "CRITICAL: Sanctions/OFAC list match detected. Regulatory prohibition."
            risk_factors.append("OFAC/Sanctions hit - account opening prohibited by law")
            return self._format_response(decision, reasoning, hitl_required, risk_factors, approval_conditions, input_data)
        
        # Check 2: KYC Failure
        if kyc_status == "FAILED":
            decision = "REJECT"
            reasoning = f"KYC/AML compliance check failed (Score: {compliance_score}/100). Unable to verify customer identity."
            return self._format_response(decision, reasoning, hitl_required, risk_factors, approval_conditions, input_data)
        
        # Check 3: Critical Document Missing
        if not documents_complete:
            decision = "REJECT"
            reasoning = "Critical documentation incomplete. Cannot proceed without required documents."
            missing = input_data.get('missing_fields', [])
            risk_factors.append(f"Missing critical documents: {', '.join(missing)}")
            return self._format_response(decision, reasoning, hitl_required, risk_factors, approval_conditions, input_data)
        
        # Check 4: Compliance Score Below Minimum
        if compliance_score < self.AUTO_REJECT_THRESHOLD['compliance_score']:
            decision = "REJECT"
            reasoning = f"Compliance score below minimum threshold ({compliance_score}/100 < {self.AUTO_REJECT_THRESHOLD['compliance_score']}/100)"
            return self._format_response(decision, reasoning, hitl_required, risk_factors, approval_conditions, input_data)
        
        # Check 5: Credit Score Too Low
        if credit_score < self.AUTO_REJECT_THRESHOLD['credit_score']:
            decision = "REJECT"
            reasoning = f"Credit score below minimum threshold ({credit_score}/100 < {self.AUTO_REJECT_THRESHOLD['credit_score']}/100). High default risk."
            return self._format_response(decision, reasoning, hitl_required, risk_factors, approval_conditions, input_data)
        
        # ========================================
        # STAGE 2: HUMAN REVIEW TRIGGERS
        # ========================================
        
        # Trigger 1: Enhanced Due Diligence Required
        if edd_required:
            decision = "HUMAN_REVIEW"
            reasoning = "Enhanced Due Diligence (EDD) required due to risk profile. Manual review mandatory."
            hitl_required = True
            risk_factors.append("EDD requirement triggered")
        
        # Trigger 2: Borderline Scores (Gray Zone)
        elif (50 <= credit_score <= 70) or (60 <= compliance_score <= 75):
            decision = "HUMAN_REVIEW"
            reasoning = f"Borderline risk scores require manual review. Credit: {credit_score}/100, Compliance: {compliance_score}/100"
            hitl_required = True
            risk_factors.append("Scores in manual review threshold range")
        
        # Trigger 3: High Risk Level from Any Agent
        elif risk_level in ["HIGH", "CRITICAL"] or credit_risk in ["HIGH", "VERY_HIGH"]:
            decision = "HUMAN_REVIEW"
            reasoning = f"High risk classification requires senior review. KYC Risk: {risk_level}, Credit Risk: {credit_risk}"
            hitl_required = True
            risk_factors.append("High risk classification from risk assessment")
        
        # Trigger 4: PEP Flagged
        elif aml_checks.get('pep_screening') == 'FLAGGED':
            decision = "HUMAN_REVIEW"
            reasoning = "Politically Exposed Person (PEP) detected. Enhanced scrutiny required per BSA/AML guidelines."
            hitl_required = True
            risk_factors.append("PEP status requires enhanced due diligence")
        
        # Trigger 5: Adverse Media
        elif aml_checks.get('adverse_media') == 'FLAGGED':
            decision = "HUMAN_REVIEW"
            reasoning = "Negative news/adverse media found. Reputation risk assessment required."
            hitl_required = True
            risk_factors.append("Adverse media requires investigation")
        
        # Trigger 6: High-Risk Industry
        elif aml_checks.get('industry_risk') == 'HIGH':
            decision = "HUMAN_REVIEW"
            reasoning = "High-risk industry classification. Enhanced monitoring protocols required."
            hitl_required = True
            approval_conditions.append("Enhanced transaction monitoring")
            approval_conditions.append("Quarterly account review")
        
        # Trigger 7: Large Credit Facility
        elif input_data.get('credit_limit', 0) > 5000000:
            decision = "HUMAN_REVIEW"
            reasoning = f"Credit limit exceeds auto-approval authority (₹{input_data.get('credit_limit', 0)/100000:.1f}L). Senior approval required."
            hitl_required = True
        
        # Trigger 8: Conditional Credit Approval
        elif credit_decision == "CONDITIONAL_APPROVE":
            decision = "HUMAN_REVIEW"
            reasoning = "Credit assessment returned conditional approval. Review of conditions required."
            hitl_required = True
            approval_conditions.append("Credit monitoring required")
        
        # ========================================
        # STAGE 3: AUTO-APPROVAL PATH
        # ========================================
        
        elif (credit_score >= self.AUTO_APPROVE_THRESHOLD['credit_score'] and 
              compliance_score >= self.AUTO_APPROVE_THRESHOLD['compliance_score'] and
              risk_level in self.AUTO_APPROVE_THRESHOLD['risk_level']):
            
            decision = "APPROVE"
            reasoning = f"Strong application metrics exceed auto-approval thresholds. Credit: {credit_score}/100, Compliance: {compliance_score}/100, Risk: {risk_level}"
            
            # Add standard conditions
            approval_conditions.append("Standard account monitoring")
            approval_conditions.append("Annual financial review")
        
        # ========================================
        # STAGE 4: DEFAULT TO HUMAN REVIEW
        # ========================================
        
        else:
            # Safety net - if doesn't clearly fit approve/reject, go to human review
            decision = "HUMAN_REVIEW"
            reasoning = f"Application requires manual assessment. Credit: {credit_score}/100, Compliance: {compliance_score}/100"
            hitl_required = True
            risk_factors.append("Does not meet auto-approval criteria")
        
        return self._format_response(decision, reasoning, hitl_required, risk_factors, approval_conditions, input_data)
    
    def _format_response(self, decision, reasoning, hitl_required, risk_factors, approval_conditions, input_data):
        """Format standardized orchestrator response"""

        llm_analysis = self.agent.run(f"Final decision analysis: {decision}. Credit: {input_data.get('credit_score')}, Compliance: {input_data.get('compliance_score')}, Risk factors: {risk_factors}. Justify the decision in 2 to 3 lines only.")
        llm_response = str(llm_analysis.content) if hasattr(llm_analysis, 'content') else str(llm_analysis)
        
        return {
            "decision": decision,
            "reasoning": reasoning,
            "hitl_required": hitl_required,
            "risk_factors": list(set(risk_factors)),  # Remove duplicates
            "approval_conditions": approval_conditions,
            "recommendation": decision,
            "confidence": "HIGH" if decision in ["APPROVE", "REJECT"] else "MEDIUM",
            "llm_analysis": llm_response
        }