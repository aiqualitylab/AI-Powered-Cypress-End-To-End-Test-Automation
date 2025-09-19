import os
import subprocess
from dotenv import load_dotenv
from colorama import init
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings

# Init colorama
init(autoreset=True)

# Load environment variables
load_dotenv()

# --- CONFIG ---
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
JIRA_ISSUE_KEY = os.getenv("JIRA_ISSUE_KEY", "KAN-1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate required environment variables
required_vars = ["JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_DOMAIN", "OPENAI_API_KEY"]
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {missing_vars}")

# LLM setup
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# --- State ---
class QAState(dict):
    requirements: str = ""
    cypress_test_code: str = ""
    playwright_test_code: str = ""

# --- Fetch Jira Requirements (placeholder) ---
def fetch_jira_requirements(state: QAState, domain, issue_key, email, token):
    print(f"📥 Fetching Jira issue {issue_key} from {domain}...")
    state["requirements"] = (
        "As a user, I want to log into the system using valid credentials "
        "so that I can access my dashboard."
    )
    return state

# --- Vector Store (placeholder) ---
def create_or_update_vector_store(state: QAState, embeddings):
    print("📚 Updating vector store with requirements...")
    return state

# --- Generate Cypress Tests ---
def generate_cypress_tests(state: QAState):
    prompt = f"""
Convert the following Jira requirement into comprehensive Cypress test code

Requirement:
{state['requirements']}

Generate Cypress JavaScript code that:

1. Includes proper describe() and it() blocks
2. Has appropriate test data setup
3. Includes assertions for the requirements
4. Handles common web elements (forms, buttons, etc.)
5. Includes proper wait conditions
6. Uses cy.visit() to navigate to a test URL (use 'https://the-internet.herokuapp.com/login' as placeholder)
7. Includes both positive and negative test cases for login functionality
8. Uses realistic selectors and test data
9. Add cy.wait(3000) after form submission to handle slow responses
10. Uses proper waits and assertions with timeout: 10000
11. Checks for success redirect to /secure page
12. Checks for error flash messages
13. valid username: tomsmith and password: SuperSecretPassword!.

Output only valid Cypress JavaScript code without markdown formatting.
"""
    try:
        response = llm.invoke(prompt)
        state["cypress_test_code"] = response.content
        print("✅ Generated Cypress test code")
    except Exception as e:
        print(f"❌ Error generating Cypress tests: {e}")
        state["cypress_test_code"] = f"// Error generating tests: {e}"
    return state

# --- Generate Playwright Tests ---
def generate_playwright_tests(state: QAState):
    prompt = f"""
Convert the following Jira requirement into comprehensive Playwright test code

Requirement:
{state['requirements']}

Generate Playwright JavaScript code that:

1. Uses @playwright/test
2. Includes proper test.describe() and test() blocks
3. Has appropriate test data setup
4. Includes assertions for the requirements
5. Handles common web elements (forms, buttons, etc.)
6. Navigates to 'https://the-internet.herokuapp.com/login' as placeholder
7. Includes both positive and negative test cases for login functionality
8. Uses realistic selectors and test data
9. Adds proper waits and timeout: 10000
10. Checks for success redirect to /secure page
11. Checks for error flash messages
12. valid username: tomsmith and password: SuperSecretPassword!.

Output only valid Playwright JavaScript code without markdown formatting.
"""
    try:
        response = llm.invoke(prompt)
        state["playwright_test_code"] = response.content
        print("✅ Generated Playwright test code")
    except Exception as e:
        print(f"❌ Error generating Playwright tests: {e}")
        state["playwright_test_code"] = f"// Error generating Playwright tests: {e}"
    return state

# --- Save & Run Cypress ---
def save_and_run_cypress_tests(state: QAState):
    test_path = "cypress/e2e/generated_tests.cy.js"
    os.makedirs(os.path.dirname(test_path), exist_ok=True)
    with open(test_path, "w") as f:
        f.write(state.get("cypress_test_code", "// No Cypress test code"))
    print(f"✅ Cypress test saved to {test_path}")
    try:
        subprocess.run(["npx", "cypress", "run", "--spec", test_path], check=True, shell=True)
        print("✅ Cypress tests executed successfully")
    except Exception as e:
        print(f"❌ Error running Cypress tests: {e}")

# --- Save & Run Playwright ---
def save_and_run_playwright_tests(state: QAState):
    test_path = "playwright/tests/generated_tests.spec.js"
    os.makedirs(os.path.dirname(test_path), exist_ok=True)
    with open(test_path, "w") as f:
        f.write(state.get("playwright_test_code", "// No Playwright test code"))
    print(f"✅ Playwright test saved to {test_path}")
    try:
        subprocess.run(["npx", "playwright", "test", test_path], check=True, shell=True)
        print("✅ Playwright tests executed successfully")
    except Exception as e:
        print(f"❌ Error running Playwright tests: {e}")

# --- Main ---
if __name__ == "__main__":
    print("🚀 QA Test Workflow: Cypress first, then Playwright sequentially")

    state = QAState()

    print("\n1️⃣ Fetching Jira requirements...")
    state = fetch_jira_requirements(state, JIRA_DOMAIN, JIRA_ISSUE_KEY, JIRA_EMAIL, JIRA_API_TOKEN)

    print("\n2️⃣ Creating vector store...")
    create_or_update_vector_store(state, embeddings)

    print("\n3️⃣ Generating Cypress tests...")
    state = generate_cypress_tests(state)

    print("\n4️⃣ Generating Playwright tests...")
    state = generate_playwright_tests(state)

    print("\n⚡ Running Cypress tests first...")
    save_and_run_cypress_tests(state)

    print("\n⚡ Running Playwright tests next...")
    save_and_run_playwright_tests(state)

    print("\n🎉 Workflow completed!")
    print("\n🔍 Next steps:")
    print("   • Cypress: check cypress/e2e/generated_tests.cy.js")
    print("   • Playwright: check playwright/tests/generated_tests.spec.js")
    print("   • Run Cypress manually: npx cypress run --spec cypress/e2e/generated_tests.cy.js")
    print("   • Run Playwright manually: npx playwright test playwright/tests/generated_tests.spec.js")
