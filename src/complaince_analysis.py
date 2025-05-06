import streamlit as st
import openai
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader

load_dotenv()

API_BASE = os.getenv("AZURE_OPENAI_ENDPOINT")
API_VERSION = "2024-12-01-preview"
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
MODEL_NAME = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")

client = AzureOpenAI(api_version=API_VERSION,api_key=API_KEY)

def call_azure_openai(messages):
    try:
        response = client.chat.completions.create(model=MODEL_NAME,
        messages=messages)
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error calling Azure OpenAI: {e}")
        return None

def extract_text_from_pdf(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return None

def main():
    st.title("Contract Compliance & Risk Evaluation")

    st.write("Upload the vendor agreement and the corporate compliance policy PDFs below.")
    agreement_pdf = st.file_uploader("Upload Vendor Agreement PDF", type="pdf")
    policy_pdf = st.file_uploader("Upload Corporate Compliance Policy PDF", type="pdf")

    if agreement_pdf and policy_pdf:
        agreement_text = extract_text_from_pdf(agreement_pdf)
        policy_text = extract_text_from_pdf(policy_pdf)

        if agreement_text and policy_text:
            if st.button("Run Analysis"):
                with st.spinner("Extracting and Mapping Clauses..."):
                    # Step 1: Extract relevant clauses
                    step1_prompt = f"""
                    You are a compliance agent. Extract sections related to Data Protection, Audit Rights, 
                    Anti-Corruption, and ESG from the following agreement text:
                    {agreement_text}
                    """
                    messages_step1 = [
                        {"role": "system", "content": "You are a helpful compliance assistant."},
                        {"role": "user", "content": step1_prompt},
                    ]
                    step1_result = call_azure_openai(messages_step1)
                    if step1_result:
                        st.subheader("Step 1: Extracted Clauses")
                        st.write(step1_result)

                    with st.spinner("Comparing with Corporate Policy..."):
                        # Step 2: Map to compliance policy
                        step2_prompt = f"""
                        Map the extracted clauses to each requirement in the corporate policy:
                        {policy_text}
                        Extracted Clauses:
                        {step1_result}
                        Provide a summary of met/not-met areas.
                        """
                        messages_step2 = [
                            {"role": "system", "content": "You are a helpful compliance assistant."},
                            {"role": "assistant", "content": step1_result},
                            {"role": "user", "content": step2_prompt},
                        ]
                        step2_result = call_azure_openai(messages_step2)
                        if step2_result:
                            st.subheader("Step 2: Compliance Mapping")
                            st.write(step2_result)

                    with st.spinner("Assigning Risk Levels..."):
                        # Step 3: Risk evaluation
                        step3_prompt = f"""
                        Based on the policy comparison, assign a risk level (Low, Medium, High) for each compliance area.
                        Mention any ambiguous clauses or missing details. Then provide final risk indicators.
                        Output your response in a markdown table format.
                        """
                        messages_step3 = [
                            {"role": "system", "content": "You are a helpful compliance assistant."},
                            {"role": "assistant", "content": step2_result},
                            {"role": "user", "content": step3_prompt},
                        ]
                        step3_result = call_azure_openai(messages_step3)
                        if step3_result:
                            st.subheader("Step 3: Risk Evaluation")
                            st.write(step3_result)

                    st.success("Analysis complete!")

if __name__ == "__main__":
    main()