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
    st.markdown("**Streamlining small business account onboarding with AI agents**")
    
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Choose Mode", [
        "📝 New Application", 
        "🤖 Agent Demo"
    ])
    
    if app_mode == "📝 New Application":
        new_application_page()
    elif app_mode == "🤖 Agent Demo":
        agent_demo_page()

def new_application_page():
    st.header("📝 New Business Application")
    
    with st.form("application_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Business Information")
            business_name = st.text_input("Business Name*")
            industry = st.selectbox("Industry*", [
                "SaaS", "Retail", "Restaurant", "Manufacturing", 
                "Consulting", "Healthcare", "Other"
            ])
            revenue = st.selectbox("Annual Revenue*", [
                "Under $100K", "$100K-$500K", "$500K-$1M", 
                "$1M-$5M", "Over $5M"
            ])
            employees = st.number_input("Number of Employees*", min_value=1, value=5)
            
        with col2:
            st.subheader("Owner Information")
            owner_name = st.text_input("Owner Name*")
            owner_email = st.text_input("Email*")
            business_age = st.selectbox("Business Age*", [
                "Less than 1 year", "1-2 years", "3-5 years", "5+ years"
            ])
        
        st.subheader("Document Upload")
        tax_id = st.checkbox("Tax ID Document")
        business_license = st.checkbox("Business License")
        bank_statement = st.checkbox("Bank Statement")
        
        submitted = st.form_submit_button("Submit Application")
        
        if submitted:
            if not all([business_name, industry, revenue, employees, owner_name, owner_email]):
                st.error("Please fill in all required fields (*)")
            else:

                app_data = {
                    "business_name": business_name,
                    "industry": industry,
                    "revenue": revenue,
                    "employees": employees,
                    "owner_name": owner_name,
                    "owner_email": owner_email,
                    "business_age": business_age,
                    "documents": {
                        "tax_id": tax_id,
                        "license": business_license,
                        "bank_statement": bank_statement
                    },
                    "identity": {
                        "id_verified": True,
                        "pep_check": "clear"
                    },
                    "financials": {
                        "revenue": 1500000 if "Over" in revenue else 500000,
                        "debt": 100000
                    },
                    "application_id": f"APP-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                    "submitted_date": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
            
                st.session_state.demo_data = app_data
                st.success("Application submitted! Go to '🤖 Agent Demo' to process it.")
                st.json(app_data)

def agent_demo_page():
    st.header("🤖 Multi-Agent Demo")
    st.markdown("See how our AI agents process applications in real-time")
    
    if 'demo_data' not in st.session_state:
        st.session_state.demo_data = {
            "business_name": "StableTech Solutions",
            "industry": "Healthcare", 
            "revenue": "$5M-$10M",   
            "employees": 25,
            "owner_name": "Dr. Sarah Johnson",
            "owner_email": "sarah@stabletech.com",
            "business_age": "5+ years", 
            "documents": {
                "tax_id": True,
                "license": True, 
                "bank_statement": True  
            },
            "identity": {
                "id_verified": True,
                "pep_check": "clear"  
            },
            "financials": {
                "revenue": 8000000, 
                "debt": 50000        
            }
        }
    
    st.subheader("Application")
    st.json(st.session_state.demo_data)
        
    if st.button("🚀 Process with AI Agents", type="primary"):
        with st.spinner("Processing with multi-agent system..."):
            result = {}
            app_data = st.session_state.demo_data
            
            # Document Agent
            with st.expander("📄 Document Agent - Analyzing Documents", expanded=True):
                doc_result = document_agent.run(app_data)
                result.update(doc_result)
                app_data["documents_status"] = "COMPLETE" if doc_result["complete"] else "INCOMPLETE"
                st.json(doc_result)
            
            # KYC Agent
            with st.expander("🔒 KYC Agent - Identity Verification", expanded=True):
                kyc_result = kyc_agent.run(app_data)
                result.update(kyc_result)
                st.json(kyc_result)
            
            # Credit Agent  
            with st.expander("💰 Credit Agent - Financial Analysis", expanded=True):
                credit_result = credit_agent.run(app_data)
                result.update(credit_result)
                st.json(credit_result)
            
            # Product Agent
            with st.expander("🎯 Product Agent - Recommendations", expanded=True):
                product_result = product_agent.run(app_data)
                result.update(product_result)
                st.json(product_result)
            
            # Orchestrator - Clean Display
            with st.expander("🔄 Orchestrator - Final Decision", expanded=True):
                orchestrator_result = orchestrator.run(result)
                result.update(orchestrator_result)
            
                decision = orchestrator_result["decision"]
                reasoning = orchestrator_result["reasoning"]
                
                if decision == "APPROVE":
                    st.success(f"✅ **Decision: {decision}**")
                elif decision == "REJECT":
                    st.error(f"❌ **Decision: {decision}**")
                else:
                    st.warning(f"⚠️ **Decision: {decision}**")
                
                st.info(f"**Reason:** {reasoning}")
                st.write(f"**Human Review Required:** {orchestrator_result['hitl_required']}")
            
            # Communication
            with st.expander("✉️ Communication Agent - Customer Update", expanded=True):
                comm_result = communication_agent.run({"status": orchestrator_result["decision"]})
                result.update(comm_result)
                
                st.success("📧 **Customer Message:**")
                st.write(comm_result["customer_message"])
            
            # Human Review if needed
            if result.get("hitl_required"):
                with st.expander("👥 Human Review Required", expanded=True):
                    human_result = human_review_agent.run(result)
                    result.update({"human_review": human_result})
                    st.json(human_result)
            
            st.session_state.last_result = result
        
        st.success("✅ Processing Complete!")
        
        # Final result
        if 'last_result' in st.session_state:
            st.subheader("🎯 Final Results Summary")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                status = st.session_state.last_result.get('decision', 'UNKNOWN')
                if status == "APPROVE":
                    st.success(f"**Status:** {status}")
                elif status == "REJECT":
                    st.error(f"**Status:** {status}")
                else:
                    st.warning(f"**Status:** {status}")
                
                st.info(f"**Credit Score:** {st.session_state.last_result.get('credit_score', 'N/A')}")
                
            with col2:
                st.info(f"**Compliance Score:** {st.session_state.last_result.get('compliance_score', 'N/A')}")
                st.info(f"**Account Type:** {st.session_state.last_result.get('account_type', 'N/A')}")
                
            with col3:
                st.info(f"**Documents:** {'✅ Complete' if st.session_state.last_result.get('complete') else '❌ Incomplete'}")
                st.info(f"**KYC Status:** {st.session_state.last_result.get('kyc_status', 'N/A')}")

if __name__ == "__main__":
    main()