import os
import requests
import subprocess
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONFIG ---
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
JIRA_ISSUE_KEY = os.getenv("JIRA_ISSUE_KEY", "KAN-1")

# Validate required environment variables
required_vars = ["JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_DOMAIN", "OPENAI_API_KEY"]
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {missing_vars}")

# LLM setup (OpenAI)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# --- State ---
class QAState(dict):
    requirements: str = ""
    test_code: str = ""

# Step 1: Fetch requirements from Jira
def fetch_jira_requirements(state: QAState):
    domain = JIRA_DOMAIN.replace('https://', '').replace('http://', '')
    url = f"https://{domain}/rest/api/3/issue/{JIRA_ISSUE_KEY}"
    
    try:
        response = requests.get(
            url,
            auth=(JIRA_EMAIL, JIRA_API_TOKEN),
            headers={"Accept": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        
        issue = response.json()
        description = issue.get("fields", {}).get("description")
        summary = issue.get("fields", {}).get("summary", "")
        
        if isinstance(description, dict):
            state["requirements"] = extract_text_from_adf(description) or summary
        else:
            state["requirements"] = description or summary
            
        print(f"✅ Fetched Jira issue {JIRA_ISSUE_KEY}: {state['requirements'][:100]}...")
        return state
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching Jira issue: {e}")
        state["requirements"] = f"Error fetching requirements: {e}"
        return state

def extract_text_from_adf(adf_content):
    if not isinstance(adf_content, dict):
        return str(adf_content)
    
    text_parts = []
    
    def extract_text(node):
        if isinstance(node, dict):
            if node.get("type") == "text":
                text_parts.append(node.get("text", ""))
            elif "content" in node:
                for child in node["content"]:
                    extract_text(child)
        elif isinstance(node, list):
            for item in node:
                extract_text(item)
    
    extract_text(adf_content)
    return " ".join(text_parts)

# Step 2: Generate Cypress tests
def generate_cypress_tests(state: QAState):
    prompt = f"""
    Convert the following Jira requirement into comprehensive Cypress test code:
    
    Requirement:
    {state['requirements']}
    
    Generate Cypress JavaScript code that:
    1. Includes proper describe() and it() blocks
    2. Has appropriate test data setup
    3. Includes assertions for the requirements
    4. Handles common web elements (forms, buttons, etc.)
    5. Includes proper wait conditions
    6. Uses cy.visit() to navigate to a test URL (use 'https://example.com' as placeholder)
    7. Includes both positive and negative test cases for login functionality
    8. Uses realistic selectors and test data
    
    Output only valid Cypress JavaScript code without markdown formatting.
    """
    
    try:
        response = llm.invoke(prompt)
        state["test_code"] = response.content
        print("✅ Generated Cypress test code")
        return state
    except Exception as e:
        print(f"❌ Error generating tests: {e}")
        state["test_code"] = f"// Error generating tests: {e}"
        return state

# Step 3: Save test code to file and run it
def save_test_code(state: QAState):
    os.makedirs("cypress/e2e", exist_ok=True)
    filepath = "cypress/e2e/generated_tests.cy.js"
    
    with open(filepath, "w") as f:
        f.write(state["test_code"])
    
    print(f"✅ Saved test file: {filepath}")
    
    # Display generated test
    print("\n" + "="*60)
    print("📝 GENERATED CYPRESS TEST CODE")
    print("="*60)
    print(state["test_code"])
    print("="*60)
    
    # Run Cypress test automatically
    if state["test_code"].strip():  # Only run if code was generated
        try:
            print("\n🏃 Running Cypress test...")
            subprocess.run(
                ["npx", "cypress", "run", "--spec", filepath],
                shell=True,
                check=True
            )
            print("✅ Cypress test run completed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running Cypress test: {e}")
    
    # Next steps
    print("\n🚀 NEXT STEPS:")
    print("1. Ensure Node.js is installed from https://nodejs.org/")
    print("2. Ensure Cypress is installed: npm install cypress --save-dev")
    print(f"\n📁 Test file saved at: {os.path.abspath(filepath)}")
    
    return state

# --- Build Graph ---
def create_qa_workflow():
    graph = StateGraph(QAState)
    
    graph.add_node("FetchReqs", fetch_jira_requirements)
    graph.add_node("GenerateTests", generate_cypress_tests)
    graph.add_node("SaveTests", save_test_code)
    
    graph.set_entry_point("FetchReqs")
    graph.add_edge("FetchReqs", "GenerateTests")
    graph.add_edge("GenerateTests", "SaveTests")
    graph.add_edge("SaveTests", END)
    
    return graph.compile()

# Main execution
if __name__ == "__main__":
    print("🚀 Starting QA Test Generation Workflow")
    print("-" * 40)
    
    try:
        app = create_qa_workflow()
        result = app.invoke(QAState())
        print("\n✅ Test generation completed successfully!")
        
    except Exception as e:
        print(f"❌ Workflow failed: {e}")
        import traceback
        traceback.print_exc()
