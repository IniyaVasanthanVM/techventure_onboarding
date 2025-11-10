import streamlit as st
import json
from datetime import datetime
from agents.orchestrator_agent import OrchestratorAgent
from agents.document_agent import DocumentAgent
from agents.kyc_agent import KYCAgent
from agents.credit_agent import CreditAgent
from agents.product_agent import ProductAgent
from agents.communication_agent import CommunicationAgent
from agents.human_review_agent import HumanReviewAgent

# Initialize agents
orchestrator = OrchestratorAgent()
document_agent = DocumentAgent()
kyc_agent = KYCAgent()
credit_agent = CreditAgent()
product_agent = ProductAgent()
communication_agent = CommunicationAgent()
human_review_agent = HumanReviewAgent()

def main():
    st.set_page_config(
        page_title="TechVenture Bank Onboarding",
        page_icon="🏦",
        layout="wide"
    )
    
    st.title("🏦 TechVenture Bank - Multi-Agent Onboarding")
    st.markdown("**Small business account onboarding with AI agents**")
    
    # Initialize session state
    if 'applications' not in st.session_state:
        st.session_state.applications = {}
    if 'hitl_queue' not in st.session_state:
        st.session_state.hitl_queue = {}
    
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Choose Mode", [
        "📝 New Application",
        "🤖 Agent Demo",
        "👥 HITL Review"
    ])
    
    if app_mode == "📝 New Application":
        new_application_page()
    elif app_mode == "🤖 Agent Demo":
        agent_demo_page()
    elif app_mode == "👥 HITL Review":
        hitl_review_page()

def new_application_page():
    st.header("📝 New Business Application")
    
    with st.form("application_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Business Information")
            business_name = st.text_input("Business Name*")
            industry = st.selectbox("Industry*", [
                "SaaS", "E-commerce", "Restaurant", "Manufacturing",
                "Consulting", "Healthcare", "Construction", "Retail",
                "Crypto", "Gambling", "Other"
            ])
            revenue = st.selectbox("Annual Revenue*", [
                "Under $100K", "$100K-$500K", "$500K-$1M",
                "$1M-$5M", "$5M-$10M", "Over $10M"
            ])
            employees = st.number_input("Number of Employees*", min_value=1, value=5)
            
        with col2:
            st.subheader("Owner Information")
            owner_name = st.text_input("Owner Name*")
            owner_email = st.text_input("Email*")
            owner_ssn = st.text_input("SSN (last 4 digits)*", max_chars=4)
            business_age = st.selectbox("Business Age*", [
                "Less than 1 year", "1-2 years", "3-5 years", "5+ years"
            ])
        
        st.subheader("Document Upload")
        tax_id = st.checkbox("Tax ID Document (EIN)")
        business_license = st.checkbox("Business License")
        bank_statement = st.checkbox("Bank Statement (3 months)")
        financial_statement = st.checkbox("Financial Statement")
        
        st.subheader("Business Profile")
        col3, col4 = st.columns(2)
        with col3:
            average_transaction = st.number_input("Average Transaction Size ($)", min_value=0, value=5000)
            monthly_volume = st.number_input("Monthly Transaction Volume", min_value=0, value=100)
        with col4:
            has_international = st.checkbox("International Transactions")
            high_risk_countries = st.checkbox("Transactions with High-Risk Countries")
        
        submitted = st.form_submit_button("Submit Application")
        
        if submitted:
            if not all([business_name, industry, revenue, employees, owner_name, owner_email, owner_ssn]):
                st.error("Please fill in all required fields (*)")
            else:
                app_id = f"APP-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                app_data = {
                    "application_id": app_id,
                    "business_name": business_name,
                    "industry": industry,
                    "revenue": revenue,
                    "employees": employees,
                    "owner_name": owner_name,
                    "owner_email": owner_email,
                    "owner_ssn": owner_ssn,
                    "business_age": business_age,
                    "documents": {
                        "tax_id": tax_id,
                        "license": business_license,
                        "bank_statement": bank_statement,
                        "financial_statement": financial_statement
                    },
                    "business_profile": {
                        "avg_transaction": average_transaction,
                        "monthly_volume": monthly_volume,
                        "international": has_international,
                        "high_risk_countries": high_risk_countries
                    },
                    "identity": {
                        "id_verified": True,
                        "pep_check": "clear",
                        "sanctions_check": "clear",
                        "adverse_media": False
                    },
                    "financials": {
                        "revenue": extract_revenue_value(revenue),
                        "debt": 100000,
                        "cash_flow_positive": True,
                        "debt_to_income": 0.3
                    },
                    "submitted_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "PENDING"
                }
                
                st.session_state.applications[app_id] = app_data
                st.session_state.demo_data = app_data
                st.success(f"✅ Application {app_id} submitted! Go to '🤖 Agent Demo' to process it.")

def extract_revenue_value(revenue_str):
    """Extract numeric revenue from string"""
    if "Under" in revenue_str:
        return 50000
    elif "$100K-$500K" in revenue_str:
        return 300000
    elif "$500K-$1M" in revenue_str:
        return 750000
    elif "$1M-$5M" in revenue_str:
        return 2500000
    elif "$5M-$10M" in revenue_str:
        return 7500000
    elif "Over $10M" in revenue_str:
        return 15000000
    return 0

def agent_demo_page():
    st.header("🤖 Multi-Agent Processing Pipeline")
    st.markdown("**Orchestration with sequential agent execution**")
    
    if 'demo_data' not in st.session_state:
        st.info("ℹ️ No application submitted. Using default demo application.")
        st.session_state.demo_data = {
            "application_id": "APP-DEMO-001",
            "business_name": "StableTech Solutions",
            "industry": "Healthcare",
            "revenue": "$5M-$10M",
            "employees": 25,
            "owner_name": "Dr. Sarah Johnson",
            "owner_email": "sarah@stabletech.com",
            "owner_ssn": "1234",
            "business_age": "5+ years",
            "documents": {
                "tax_id": True,
                "license": True,
                "bank_statement": True,
                "financial_statement": True
            },
            "business_profile": {
                "avg_transaction": 15000,
                "monthly_volume": 200,
                "international": False,
                "high_risk_countries": False
            },
            "identity": {
                "id_verified": True,
                "pep_check": "clear",
                "sanctions_check": "clear",
                "adverse_media": False
            },
            "financials": {
                "revenue": 8000000,
                "debt": 50000,
                "cash_flow_positive": True,
                "debt_to_income": 0.15
            },
            "submitted_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "PENDING"
        }
    
    st.subheader("📋 Application Details")
    with st.expander("View Application Data", expanded=False):
        st.json(st.session_state.demo_data)
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.info(f"**Application ID:** {st.session_state.demo_data.get('application_id', 'N/A')}")
    with col2:
        if st.button("🚀 Process Application", type="primary", use_container_width=True):
            process_application()

def process_application():
    """Execute the agent pipeline"""
    app_data = st.session_state.demo_data
    app_id = app_data.get('application_id')
    
    with st.spinner("🔄 Executing Agent Pipeline..."):
        pipeline_results = {}
        
        # Stage 1: Document Verification
        st.markdown("### 📄 Stage 1: Document Verification")
        with st.status("Processing documents...", expanded=True) as status:
            doc_result = document_agent.run(app_data)
            pipeline_results.update(doc_result)
            app_data["documents_status"] = doc_result.get("status", "INCOMPLETE")
            
            st.json(doc_result)
            
            if not doc_result.get("complete", False):
                status.update(label="❌ Document verification failed", state="error")
                st.error("**Pipeline Halted:** Incomplete documentation")
                return
            status.update(label="✅ Documents verified", state="complete")
        
        # Stage 2: KYC/AML Compliance
        st.markdown("### 🔒 Stage 2: KYC/AML Compliance Check")
        with st.status("Running compliance checks...", expanded=True) as status:
            kyc_result = kyc_agent.run(app_data)
            pipeline_results.update(kyc_result)
            
            st.json(kyc_result)
            
            if kyc_result.get("kyc_status") == "FAILED":
                status.update(label="❌ Compliance check failed", state="error")
                st.error("**Pipeline Halted:** Failed KYC/AML compliance")
                return
            status.update(label="✅ Compliance verified", state="complete")
        
        # Stage 3: Credit Risk Assessment
        st.markdown("### 💰 Stage 3: Credit Risk Assessment")
        with st.status("Analyzing creditworthiness...", expanded=True) as status:
            credit_result = credit_agent.run(app_data)
            pipeline_results.update(credit_result)
            
            st.json(credit_result)
            status.update(label="✅ Credit analysis complete", state="complete")
        
        # Stage 4: Product Recommendation
        st.markdown("### 🎯 Stage 4: Product Recommendation")
        with st.status("Matching products...", expanded=True) as status:
            product_result = product_agent.run(app_data)
            pipeline_results.update(product_result)
            
            st.json(product_result)
            status.update(label="✅ Products recommended", state="complete")
        
        # Stage 5: Orchestrator Decision
        st.markdown("### 🔄 Stage 5: Final Decision Engine")
        with st.status("Making final decision...", expanded=True) as status:
            orchestrator_result = orchestrator.run(pipeline_results)
            pipeline_results.update(orchestrator_result)
            
            decision = orchestrator_result["decision"]
            reasoning = orchestrator_result["reasoning"]
            risk_factors = orchestrator_result.get("risk_factors", [])
            
            if decision == "APPROVE":
                st.success(f"✅ **Decision: {decision}**")
                status.update(label="✅ Application approved", state="complete")
            elif decision == "REJECT":
                st.error(f"❌ **Decision: {decision}**")
                status.update(label="❌ Application rejected", state="error")
            else:
                st.warning(f"⚠️ **Decision: {decision}**")
                status.update(label="⚠️ Human review required", state="complete")
            
            st.info(f"**Reasoning:** {reasoning}")
            st.write(f"**Human Review Required:** {orchestrator_result['hitl_required']}")
            
            if risk_factors:
                st.warning("**Risk Factors Identified:**")
                for factor in risk_factors:
                    st.write(f"- {factor}")
        
        # Stage 6: Communication
        st.markdown("### ✉️ Stage 6: Customer Communication")
        with st.status("Generating customer message...", expanded=True) as status:
            comm_result = communication_agent.run({
                "status": decision,
                "business_name": app_data.get("business_name"),
                "reasoning": reasoning
            })
            pipeline_results.update(comm_result)
            
            st.success("📧 **Customer Message:**")
            st.info(comm_result["customer_message"])
            status.update(label="✅ Communication sent", state="complete")
        
        # Stage 7: HITL Queue
        if pipeline_results.get("hitl_required"):
            st.markdown("### 👥 Stage 7: Human Review Queue")
            with st.status("Adding to review queue...", expanded=True) as status:
                human_result = human_review_agent.run(pipeline_results)
                pipeline_results.update({"human_review": human_result})
                
                # Add to HITL queue
                st.session_state.hitl_queue[app_id] = {
                    "application": app_data,
                    "results": pipeline_results,
                    "review_data": human_result,
                    "queued_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                st.json(human_result)
                st.warning(f"⚠️ Application {app_id} added to HITL review queue")
                status.update(label="✅ Added to review queue", state="complete")
        
        st.session_state.last_result = pipeline_results
        app_data["status"] = decision
        app_data["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    st.success("✅ **Pipeline Execution Complete!**")
    display_final_summary()

def display_final_summary():
    """Display final results summary"""
    if 'last_result' not in st.session_state:
        return
    
    st.markdown("---")
    st.subheader("🎯 Final Results Dashboard")
    
    result = st.session_state.last_result
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status = result.get('decision', 'UNKNOWN')
        if status == "APPROVE":
            st.metric("Decision", "✅ APPROVED", delta="Success")
        elif status == "REJECT":
            st.metric("Decision", "❌ REJECTED", delta="Failed", delta_color="inverse")
        else:
            st.metric("Decision", "⚠️ REVIEW", delta="Pending")
    
    with col2:
        credit = result.get('credit_score', 0)
        st.metric("Credit Score", f"{credit}/100", 
                 delta="Good" if credit >= 70 else "Low", 
                 delta_color="normal" if credit >= 70 else "inverse")
    
    with col3:
        compliance = result.get('compliance_score', 0)
        st.metric("Compliance Score", f"{compliance}/100",
                 delta="Pass" if compliance >= 70 else "Fail",
                 delta_color="normal" if compliance >= 70 else "inverse")
    
    with col4:
        risk = result.get('risk_level', 'N/A')
        st.metric("Risk Level", risk)
    
    # Detailed breakdown
    with st.expander("📊 Detailed Breakdown", expanded=False):
        col5, col6 = st.columns(2)
        with col5:
            st.write("**Document Status:**", "✅ Complete" if result.get('complete') else "❌ Incomplete")
            st.write("**KYC Status:**", result.get('kyc_status', 'N/A'))
            st.write("**Account Type:**", result.get('account_type', 'N/A'))
        with col6:
            st.write("**Loan Eligibility:**", result.get('loan_offer', 'N/A'))
            st.write("**Credit Card:**", result.get('credit_card', 'N/A'))
            st.write("**HITL Required:**", "Yes" if result.get('hitl_required') else "No")

def hitl_review_page():
    st.header("👥 Human-in-the-Loop Review Interface")
    st.markdown("**Manual review and decision-making for flagged applications**")
    
    if not st.session_state.hitl_queue:
        st.info("📭 No applications pending human review")
        return
    
    st.success(f"📬 **{len(st.session_state.hitl_queue)}** application(s) awaiting review")
    
    # Select application to review
    app_ids = list(st.session_state.hitl_queue.keys())
    selected_app = st.selectbox("Select Application to Review", app_ids)
    
    if selected_app:
        review_item = st.session_state.hitl_queue[selected_app]
        app_data = review_item["application"]
        results = review_item["results"]
        review_data = review_item["review_data"]
        
        st.markdown("---")
        
        # Application Overview
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Application ID", selected_app)
            st.metric("Business Name", app_data.get("business_name"))
        with col2:
            st.metric("Industry", app_data.get("industry"))
            st.metric("Revenue", app_data.get("revenue"))
        with col3:
            st.metric("Submitted", review_item["queued_at"])
            st.metric("Owner", app_data.get("owner_name"))
        
        # Review Summary
        st.subheader("📋 AI Assessment Summary")
        summary = review_data.get("summary", {})
        
        col4, col5, col6, col7 = st.columns(4)
        with col4:
            st.info(f"**KYC Status**\n\n{summary.get('kyc', 'N/A')}")
        with col5:
            st.info(f"**Credit Score**\n\n{summary.get('credit', 'N/A')}/100")
        with col6:
            st.info(f"**Compliance**\n\n{summary.get('compliance', 'N/A')}/100")
        with col7:
            st.info(f"**Documents**\n\n{summary.get('documents', 'N/A')}")
        
        # Risk Factors
        if results.get("risk_factors"):
            st.warning("⚠️ **Risk Factors Identified:**")
            for factor in results["risk_factors"]:
                st.write(f"- {factor}")
        
        # AI Recommendation
        st.info(f"**AI Recommendation:** {summary.get('recommendation', 'N/A')}")
        st.write(f"**Reasoning:** {results.get('reasoning', 'N/A')}")
        
        # Detailed Data Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📄 Documents", "🔒 KYC/AML", "💰 Financials", "📊 Full Results"])
        
        with tab1:
            st.json(app_data.get("documents", {}))
        
        with tab2:
            st.json({
                "identity": app_data.get("identity", {}),
                "compliance_score": results.get("compliance_score"),
                "kyc_status": results.get("kyc_status"),
                "aml_checks": results.get("aml_checks", {})
            })
        
        with tab3:
            st.json({
                "financials": app_data.get("financials", {}),
                "credit_score": results.get("credit_score"),
                "risk_level": results.get("risk_level"),
                "credit_limit": results.get("credit_limit")
            })
        
        with tab4:
            st.json(results)
        
        # Human Decision Interface
        st.markdown("---")
        st.subheader("🎯 Human Decision")
        
        col8, col9 = st.columns([2, 1])
        
        with col8:
            decision_options = review_data.get("options", ["Approve", "Reject", "Request More Info"])
            human_decision = st.radio("Select Decision", decision_options, horizontal=True)
            
            human_notes = st.text_area("Reviewer Notes (Required)", 
                                      placeholder="Provide detailed reasoning for your decision...",
                                      height=100)
            
            if human_decision == "Request More Info":
                required_docs = st.multiselect("Additional Documents Required", 
                                              ["Updated Financial Statement", 
                                               "Bank Statements (6 months)",
                                               "Tax Returns", 
                                               "Business Plan",
                                               "Reference Letters",
                                               "Other"])
        
        with col9:
            st.write("**Reviewer Information**")
            reviewer_name = st.text_input("Reviewer Name", value="John Smith")
            reviewer_id = st.text_input("Reviewer ID", value="REV-001")
        
        # Submit Decision
        if st.button("✅ Submit Human Decision", type="primary", use_container_width=True):
            if not human_notes:
                st.error("Please provide reviewer notes before submitting")
            else:
                # Record decision
                final_decision = {
                    "application_id": selected_app,
                    "human_decision": human_decision.upper().replace(" ", "_"),
                    "reviewer_name": reviewer_name,
                    "reviewer_id": reviewer_id,
                    "notes": human_notes,
                    "reviewed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "ai_recommendation": summary.get('recommendation'),
                    "override": human_decision.upper() != summary.get('recommendation', '').upper()
                }
                
                if human_decision == "Request More Info":
                    final_decision["required_documents"] = required_docs
                
                # Update application status
                app_data["status"] = final_decision["human_decision"]
                app_data["human_review"] = final_decision
                
                # Remove from HITL queue
                del st.session_state.hitl_queue[selected_app]
                
                # Send notification
                comm_result = communication_agent.run({
                    "status": final_decision["human_decision"],
                    "business_name": app_data.get("business_name"),
                    "reasoning": human_notes
                })
                
                st.success(f"✅ Decision recorded: {human_decision}")
                st.info(f"📧 Notification sent to {app_data.get('owner_email')}")
                
                with st.expander("View Final Decision Record"):
                    st.json(final_decision)
                
                st.balloons()
                st.rerun()

if __name__ == "__main__":
    main()