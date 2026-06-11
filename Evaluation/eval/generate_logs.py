import json
import sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.append(str(Path(__file__).parent.parent))  # lets us import from rag/
from rag.chatbot import answer

QUESTIONS = [
    # KYC - Customer Identification
    "What documents are required for KYC verification?",
    "What is the minimum age requirement for opening a bank account?",
    "How long must banks retain KYC records?",
    "What is enhanced due diligence and when is it required?",
    "What is simplified due diligence and when can it be applied?",
    "What information must be collected for corporate customers during KYC?",
    "How should banks verify the identity of a non-resident customer?",
    "What triggers a KYC refresh for an existing customer?",
    "What is a Politically Exposed Person (PEP) and how are they treated?",
    "How should banks handle customers who refuse to provide KYC documents?",

    # AML - Suspicious Activity
    "What is a Suspicious Activity Report (SAR) and when must it be filed?",
    "What are the key indicators of money laundering in retail banking?",
    "What is structuring and why is it considered suspicious?",
    "How should staff escalate a suspicious transaction internally?",
    "What is the tipping-off offence in AML compliance?",
    "What thresholds trigger mandatory transaction reporting?",
    "How are cash-intensive businesses treated under AML rules?",
    "What is layering in the context of money laundering?",
    "What is placement in the context of money laundering?",
    "What is integration in the context of money laundering?",

    # Regulatory & Compliance
    "What are the FATF 40 Recommendations?",
    "What does Basel III require of banks regarding capital adequacy?",
    "What is the role of the compliance officer in a bank?",
    "What penalties can a bank face for AML non-compliance?",
    "What is correspondent banking and what are its AML risks?",
    "What is de-risking and what are its consequences?",
    "How does GDPR interact with KYC data retention requirements?",
    "What is a National Risk Assessment in the context of AML?",
    "What is the Financial Action Task Force (FATF)?",
    "What is mutual evaluation in the FATF framework?",

    # Procedures & Controls
    "What is a risk-based approach to AML compliance?",
    "How should banks conduct customer risk scoring?",
    "What is transaction monitoring and how does it work?",
    "What are the four pillars of an AML compliance program?",
    "How should banks handle high-risk jurisdictions?",
    "What is a beneficial owner and how is ownership verified?",
    "What is the difference between KYC and CDD?",
    "What is ongoing monitoring in the context of customer due diligence?",
    "How should banks screen customers against sanctions lists?",
    "What is a false positive in transaction monitoring?",

    # Edge Cases & Robustness (useful for bias testing in Part 3)
    "Is there any situation where KYC checks can be skipped entirely?",
    "Can a bank open an account for an anonymous customer?",
    "What happens if a customer is found on a sanctions list after onboarding?",
    "How should a bank handle a walk-in customer with no fixed address?",
    "What if a customer provides documents that appear to be forged?",
    "Can a bank rely on KYC checks performed by a third party?",
    "What is the liability of a bank employee who files a false SAR?",
    "How should banks treat cryptocurrency transactions under AML rules?",
    "What is proliferation financing and how does it differ from money laundering?",
    "What obligations do banks have when closing a high-risk account?",
]

def generate_logs(output_path="eval/logs.jsonl"):
    Path("eval").mkdir(exist_ok=True) # ensure eval/ directory exists
    
    with open(output_path, "a") as f:
        for i, question in enumerate(QUESTIONS):
            print(f"[{i+1}/{len(QUESTIONS)}] {question}") # progress indicator in console
            try:
                result = answer(question) # get answer and metadata from chatbot
                result["timestamp"] = datetime.now(timezone.utc).isoformat() # add timestamp for when the question was answered
                f.write(json.dumps(result) + "\n") # write each result as a JSON line for easy parsing later
                f.flush()  # write immediately so progress isn't lost on crash
            except Exception as e:
                print(f"  ✗ Failed: {e}")

    print(f"\nDone. Logged to {output_path}")  

if __name__ == "__main__":
    generate_logs()