from agno.agent import Agent

class CommunicationAgent:
    """
    Customer Communication Agent
    Generates professional, personalized communications for various
    application statuses and customer interactions
    """
    
    def __init__(self):
        self.agent = Agent(
            name="Communication_Agent",
            model="google:gemini-2.0-flash",
            instructions="""You are a professional banking communications specialist.
            Generate clear, friendly, and professional customer messages.
            Maintain appropriate tone based on decision outcome.
            Be empathetic for rejections, enthusiastic for approvals."""
        )
    
    def run(self, input_data):
        """
        Generate customer communication based on decision
        
        Returns:
            - customer_message: Formatted message
            - communication_type: Email/SMS/Letter
            - next_steps: List of actions for customer
        """
        
        status = input_data.get("status", "Processing")
        business_name = input_data.get("business_name", "Valued Customer")
        reasoning = input_data.get("reasoning", "")
        
        # Generate appropriate message based on status
        if status == "APPROVE":
            message = self._generate_approval_message(business_name, reasoning)
            comm_type = "Email + Welcome Package"
            next_steps = [
                "Check your email for account setup instructions",
                "Complete online banking enrollment",
                "Schedule appointment with your relationship manager",
                "Review and sign account agreements",
                "Make initial deposit to activate account"
            ]
        
        elif status == "REJECT":
            message = self._generate_rejection_message(business_name, reasoning)
            comm_type = "Email"
            next_steps = [
                "Review the specific reasons for decline",
                "Address identified concerns (if possible)",
                "Consider reapplying after 6 months",
                "Contact us for alternative banking options",
                "Request detailed explanation if needed"
            ]
        
        elif status == "HUMAN_REVIEW":
            message = self._generate_review_message(business_name, reasoning)
            comm_type = "Email + SMS Alert"
            next_steps = [
                "Our team is conducting additional review",
                "You may receive a call for clarification",
                "Decision expected within 2-3 business days",
                "No action required at this time",
                "Check application status online"
            ]
        
        else:
            message = self._generate_processing_message(business_name)
            comm_type = "Email Confirmation"
            next_steps = [
                "Application received and under review",
                "Processing time: 1-2 business days",
                "Check email for updates",
                "Status available in online portal"
            ]
        
        return {
            "customer_message": message,
            "communication_type": comm_type,
            "next_steps": next_steps,
            "status": status
        }
    
    def _generate_approval_message(self, business_name, reasoning):
        """Generate approval message"""
        return f"""Dear {business_name},

🎉 Congratulations! Your TechVenture Bank business account application has been APPROVED.

We're excited to welcome you to our banking family and support your business growth. Your application demonstrated strong financial health and compliance with our banking standards.

Your account manager will contact you within 24 hours to complete the onboarding process and discuss the suite of services available to you.

Welcome to TechVenture Bank!

Best regards,
TechVenture Bank Onboarding Team"""
    
    def _generate_rejection_message(self, business_name, reasoning):
        """Generate rejection message"""
        return f"""Dear {business_name},

Thank you for your interest in TechVenture Bank. After careful review, we regret to inform you that we are unable to approve your business account application at this time.

Reason: {reasoning}

We understand this may be disappointing. This decision was based on our current lending and risk criteria. We encourage you to consider reapplying after addressing the identified concerns.

If you have questions, please contact our support team at support@techventurebank.com.

Thank you for considering TechVenture Bank.

Sincerely,
TechVenture Bank Application Team"""
    
    def _generate_review_message(self, business_name, reasoning):
        """Generate human review message"""
        return f"""Dear {business_name},

Thank you for submitting your business account application to TechVenture Bank.

Your application is currently under additional review by our specialized team. This is a standard process for certain applications to ensure we provide you with the best banking solutions.

Review Status: {reasoning}

We expect to complete our review within 2-3 business days. A member of our team may contact you if additional information is needed.

We appreciate your patience and look forward to serving your banking needs.

Best regards,
TechVenture Bank Review Team"""
    
    def _generate_processing_message(self, business_name):
        """Generate processing confirmation"""
        return f"""Dear {business_name},

Thank you for choosing TechVenture Bank. We have received your business account application and our team is currently reviewing your submission.

We appreciate your interest and will provide an update within 1-2 business days.

Best regards,
TechVenture Bank"""