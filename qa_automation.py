import os
import re
import requests
import subprocess
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Init colorama for colored terminal output
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

# --- Paths ---
VECTOR_STORE_DIR = "vector_store"
REQUIREMENTS_DIR = "jira_requirements"

# --- IMPROVED AI ANALYZER ---
def analyze_error(error_text):
    """Improved error analysis with better pattern matching"""
    if not error_text:
        return "🤔 NO ERROR OUTPUT → Check if Cypress is installed and configured properly"
    
    error = error_text.lower()
   
    if 'cypress could not verify' in error or 'cypress verification' in error:
        return "🔧 CYPRESS INSTALL ISSUE → Run 'npx cypress install' or 'npx cypress verify'"
    elif 'not found' in error and ('element' in error or 'selector' in error):
        return "🔍 ELEMENT NOT FOUND → Check CSS selectors or add cy.wait() for dynamic content"
    elif 'timed out' in error or 'timeout' in error:
        return "⏰ TIMEOUT ERROR → Increase timeout with cy.get(selector, {timeout: 10000}) or add cy.wait()"
    elif 'not visible' in error or 'not actionable' in error:
        return "👁️ ELEMENT NOT VISIBLE → Add cy.scrollIntoView() or check if element is hidden/covered"
    elif 'expected' in error or 'assertion' in error:
        return "❌ ASSERTION FAILED → Check expected values, text content, or element states"
    elif 'network' in error or 'fetch' in error:
        return "🌐 NETWORK ISSUE → Check internet connection or add network stubbing"
    elif 'cypress run' in error:
        return "⚙️ CYPRESS CONFIG → Check cypress.config.js and baseUrl settings"
    elif 'unicode' in error or 'encoding' in error:
        return "🔤 ENCODING ISSUE → Fixed in script - should work now"
    else:
        return f"🤔 UNKNOWN ERROR → Check Cypress dashboard or run: npx cypress open\nError snippet: {error_text[:200]}..."

# --- State ---
class QAState(dict):
    requirements: str = ""
    test_code: str = ""

# --- Jira Fetch ---
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

# --- Vector Store ---
def create_or_update_vector_store(state: QAState, additional_doc_path=None):
    from langchain.docstore.document import Document
    os.makedirs(REQUIREMENTS_DIR, exist_ok=True)
    loader = DirectoryLoader(REQUIREMENTS_DIR, glob="*.txt")
    documents = loader.load()

    if state["requirements"]:
        documents.append(Document(page_content=state["requirements"]))

    if additional_doc_path and os.path.exists(additional_doc_path):
        with open(additional_doc_path, "r", encoding="utf-8") as f:
            content = f.read()
        documents.append(Document(page_content=content))

    if not documents:
        print("⚠️ No documents found. Skipping vector store creation.")
        return None

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    if os.path.exists(VECTOR_STORE_DIR) and os.listdir(VECTOR_STORE_DIR):
        db = Chroma(persist_directory=VECTOR_STORE_DIR, embedding_function=embeddings)
        db.add_documents(docs)
        db.persist()
    else:
        db = Chroma.from_documents(docs, embeddings, persist_directory=VECTOR_STORE_DIR)
        db.persist()

    return db

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
    10.Uses proper waits and assertions with timeout: 10000
    11.Checks for success redirect to /secure page
    12.Checks for error flash messages

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

# --- Save & Run Cypress with Live AI Analysis ---
def save_test_code(state: QAState):
    os.makedirs("cypress/e2e", exist_ok=True)
    filepath = "cypress/e2e/generated_tests.cy.js"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(state["test_code"])

    print(f"✅ Saved test file: {filepath}")
    print("\n📝 Generated test preview:")
    print("-" * 50)
    print(state["test_code"][:500] + "..." if len(state["test_code"]) > 500 else state["test_code"])
    print("-" * 50)

    if state["test_code"].strip():
        print("\n🧪 Running Cypress tests (live logs + AI analysis)...\n")

        try:
            process = subprocess.Popen(
                ["npx", "cypress", "run", "--spec", filepath],
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace"
            )

            full_output = ""
            for line in process.stdout:
                print(line, end="")
                full_output += line

                # AI hint if line looks like error
                if re.search(r"(error|failed|timed out|not found|assertion)", line, re.IGNORECASE):
                    ai_hint = analyze_error(line)
                    print(Fore.YELLOW + f"\n🤖 AI Hint: {ai_hint}\n" + Style.RESET_ALL)

            process.wait(timeout=300)

            if process.returncode == 0:
                print(Fore.GREEN + "\n✅ Cypress tests passed successfully!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "\n❌ Cypress tests failed!" + Style.RESET_ALL)
                print("\n🔍 Final AI Analysis (full logs):")
                analysis = analyze_error(full_output)
                print(Fore.CYAN + f"🤖 {analysis}" + Style.RESET_ALL)

        except subprocess.TimeoutExpired:
            print("⏰ Cypress run timed out after 5 minutes")
            process.kill()
        except FileNotFoundError:
            print("❌ Cypress not found. Please install with: npm install -g cypress")
            print("   Or run: npx cypress install")
        except Exception as e:
            print(f"❌ Unexpected error running Cypress: {e}")
            analysis = analyze_error(str(e))
            print(f"🤖 AI Suggestion: {analysis}")

    return state

# --- Workflow Graph ---
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

# --- Main ---
if __name__ == "__main__":
    print("🚀 Starting QA Test Generation Workflow with Enhanced AI Analysis")
    
    try:
        app = create_qa_workflow()
        state = QAState()
        
        print("\n1️⃣ Fetching Jira requirements...")
        state = fetch_jira_requirements(state)
        
        print("\n2️⃣ Creating vector store...")
        create_or_update_vector_store(state)
        
        print("\n3️⃣ Generating Cypress tests...")
        state = generate_cypress_tests(state)
        
        print("\n4️⃣ Saving and running tests...")
        save_test_code(state)
        
        print("\n✅ Test generation workflow completed!")
        print("\n🔍 Next steps:")
        print("   • Check the generated test file: cypress/e2e/generated_tests.cy.js")
        print("   • Run manually: npx cypress run --spec cypress/e2e/generated_tests.cy.js")
        print("   • Open Cypress UI: npx cypress open")
        
    except Exception as e:
        print(f"❌ Workflow failed: {e}")
        import traceback
        traceback.print_exc()
