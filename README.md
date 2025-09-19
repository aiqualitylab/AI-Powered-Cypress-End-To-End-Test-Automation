# AI-Powered QA Automation

> Automatically generate comprehensive end-to-end tests from Jira requirements using artificial intelligence with dual framework support (Cypress + Playwright) and real-time failure analysis.

[![Node.js](https://img.shields.io/badge/Node.js-v14+-green.svg)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org/)
[![Cypress](https://img.shields.io/badge/Cypress-13.17.0-brightgreen.svg)](https://cypress.io/)
[![Playwright](https://img.shields.io/badge/Playwright-Latest-blue.svg)](https://playwright.dev/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)](https://openai.com/)

## Overview

This system automates quality assurance by converting Jira requirements into executable tests using GPT-4o-mini for **both Cypress and Playwright frameworks**. It eliminates manual test writing while ensuring comprehensive coverage and consistent quality across multiple testing frameworks. **Enhanced with real-time AI-powered failure analysis and intelligent debugging assistance.**

## Key Features

- **🎯 Dual Framework Support**: Generate identical test scenarios for both Cypress and Playwright
- **🤖 Automated Test Generation**: Transform requirements into tests in minutes for both frameworks
- **🔗 Jira Integration**: Direct pipeline from tickets to executable tests  
- **🧠 AI-Powered Analysis**: Natural language processing for complex requirements
- **⚡ Sequential Test Execution**: Run Cypress tests first, then Playwright automatically
- **🔍 Real-Time AI Analysis**: Live error detection with intelligent debugging hints during test execution
- **🧩 Pattern-Based Intelligence**: Recognizes common testing issues across both frameworks
- **📊 Enhanced Error Recognition**: Contextual failure analysis with actionable remediation steps
- **✅ Consistent Quality**: Standardized test patterns and best practices for both frameworks
- **🔄 Multi-Scenario Coverage**: Automatic generation of positive and negative test cases

## ✨ Enhanced Dual Framework Architecture

### Framework Execution Flow
```
Jira Requirements → AI Parser → GPT-4o-mini Generator
                                      ↓
                            Cypress Test Generation
                                      ↓
                           Playwright Test Generation
                                      ↓
                              Save Both Test Files
                                      ↓
                             Execute Cypress Tests
                                      ↓
                            Execute Playwright Tests
                                      ↓
                          Combined Results & Analysis
```

### Framework Comparison & Benefits
| Feature | Cypress | Playwright | Implementation |
|---------|---------|------------|----------------|
| **Browser Support** | Chromium-based, Firefox | Chrome, Firefox, Safari, Edge | Complementary coverage |
| **Execution Speed** | Fast debugging | Parallel execution | Sequential run for comparison |
| **Element Handling** | jQuery-style | Modern selectors | Consistent test logic |
| **Network Stubbing** | Built-in | Advanced API mocking | Framework-specific approaches |
| **Screenshots/Videos** | Automatic | On-failure | Enhanced debugging |

## Architecture

**Technology Stack:**
- **LangGraph** for AI workflow orchestration
- **OpenAI GPT-4o-mini** for intelligent test generation and failure analysis
- **Cypress** for comprehensive end-to-end testing with excellent debugging
- **Playwright** for cross-browser automation and parallel execution
- **Atlassian Jira API** for requirement management
- **ChromaDB** for vector storage and intelligent retrieval
- **Colorama** for enhanced terminal output

## Quick Start

### Prerequisites
- Node.js v14+
- Python 3.8+
- Jira account with API access
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aiqualitylab/ai-powered-qa-automation.git
   cd ai-powered-qa-automation
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies for both frameworks**
   ```bash
   # Install Cypress
   npm install cypress --save-dev
   
   # Install Playwright
   npm install @playwright/test
   npx playwright install
   ```

4. **Create required directories**
   ```bash
   mkdir -p cypress/e2e
   mkdir -p playwright/tests
   mkdir -p jira_requirements
   mkdir -p vector_store
   ```

5. **Configure environment**
   ```bash
   cp .env.example .env
   ```

6. **Set environment variables**
   ```env
   JIRA_EMAIL=your-email@company.com
   JIRA_API_TOKEN=your-jira-api-token
   JIRA_DOMAIN=https://your-company.atlassian.net
   JIRA_ISSUE_KEY=KAN-1
   OPENAI_API_KEY=your-openai-api-key
   ```

7. **Run the dual-framework system**
   ```bash
   python qa_automation.py
   ```

## Usage

### Automated Dual Framework Execution
```bash
# Generate and run tests for both frameworks sequentially
python qa_automation.py
```

This command will:
1. Fetch Jira requirements
2. Generate Cypress test code
3. Generate Playwright test code
4. Save Cypress tests to `cypress/e2e/generated_tests.cy.js`
5. Save Playwright tests to `playwright/tests/generated_tests.spec.js`
6. Execute Cypress tests first
7. Execute Playwright tests second
8. Display combined results

### Manual Framework-Specific Commands

#### Cypress Commands
```bash
# Run Cypress interactively
npx cypress open

# Run generated Cypress tests headlessly
npx cypress run --spec cypress/e2e/generated_tests.cy.js

# Run all Cypress tests
npx cypress run
```

#### Playwright Commands
```bash
# Run generated Playwright tests
npx playwright test playwright/tests/generated_tests.spec.js

# Run Playwright tests with UI mode
npx playwright test --ui

# Run all Playwright tests
npx playwright test

# Run tests in headed mode
npx playwright test --headed

# Run tests in specific browser
npx playwright test --project=chromium
```

### Directory Structure After Setup
```
ai-powered-qa-automation/
├── qa_automation.py                    # Main dual-framework automation script
├── cypress/
│   ├── e2e/
│   │   └── generated_tests.cy.js      # AI-generated Cypress tests
│   └── cypress.config.js
├── playwright/
│   ├── tests/
│   │   └── generated_tests.spec.js    # AI-generated Playwright tests
│   └── playwright.config.js
├── jira_requirements/                  # Jira requirement storage
├── vector_store/                       # ChromaDB embeddings
├── package.json
└── .env
```

## Framework Configuration

### Cypress Configuration (`cypress.config.js`)
```javascript
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'https://the-internet.herokuapp.com',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: true,
    screenshotOnRunFailure: true,
    defaultCommandTimeout: 10000,
    requestTimeout: 15000,
    responseTimeout: 15000,
    retries: {
      runMode: 2,
      openMode: 0
    },
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
```

### Playwright Configuration (`playwright.config.js`)
```javascript
const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './playwright/tests',
  timeout: 30000,
  expect: {
    timeout: 10000
  },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'https://the-internet.herokuapp.com',
    trace: 'on-first-retry',
    video: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
});
```

## Test Generation Features

### AI-Generated Test Scenarios
Both frameworks generate tests with:
- ✅ Proper test structure (`describe`/`it` blocks for Cypress, `test.describe`/`test` for Playwright)
- ✅ Test data setup with realistic credentials
- ✅ Positive test cases (valid login: `tomsmith` / `SuperSecretPassword!`)
- ✅ Negative test cases (invalid credentials)
- ✅ Proper wait conditions and timeouts
- ✅ Success redirect verification (`/secure` page)
- ✅ Error message validation
- ✅ Screenshot capture on failures

### Example Generated Test Output

#### Cypress Test Structure
```javascript
describe('User Login Functionality', () => {
  it('should successfully log in with valid credentials', () => {
    cy.visit('/login');
    cy.get('#username').type('tomsmith');
    cy.get('#password').type('SuperSecretPassword!');
    cy.get('button[type="submit"]').click();
    cy.wait(3000);
    cy.url({ timeout: 10000 }).should('include', '/secure');
  });

  it('should display error with invalid credentials', () => {
    // Negative test case logic
  });
});
```

#### Playwright Test Structure
```javascript
const { test, expect } = require('@playwright/test');

test.describe('User Login Functionality', () => {
  test('should successfully log in with valid credentials', async ({ page }) => {
    await page.goto('/login');
    await page.fill('#username', 'tomsmith');
    await page.fill('#password', 'SuperSecretPassword!');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*\/secure/, { timeout: 10000 });
  });

  test('should display error with invalid credentials', async ({ page }) => {
    // Negative test case logic
  });
});
```

## Enhanced AI Failure Analysis

### Dual Framework Error Detection
The AI system provides intelligent analysis for both frameworks:

| Error Category | Cypress Detection | Playwright Detection | AI Solution |
|----------------|------------------|---------------------|-------------|
| 🔧 Installation | Cypress binary issues | Browser installation | `npx cypress install` / `npx playwright install` |
| 🔍 Element Selection | jQuery selectors | Modern selectors | Framework-specific selector strategies |
| ⏰ Timeouts | Command timeouts | Action timeouts | Increased timeout configurations |
| 🌐 Network Issues | cy.intercept() problems | Route handling | Framework-appropriate network mocking |
| 👁️ Visibility | Element not visible | Element not actionable | `cy.scrollIntoView()` / `scrollIntoViewIfNeeded` |

### Real-Time Monitoring Features
- **Live error detection** during test execution
- **Framework-specific debugging hints**
- **Comparative analysis** between Cypress and Playwright results
- **Color-coded terminal output** for immediate issue identification
- **Post-execution summary** with actionable recommendations

## Troubleshooting

### Common Issues & Solutions

#### Framework Installation
```bash
# Cypress installation issues
npx cypress install --force
npx cypress cache clear
npx cypress verify

# Playwright installation issues
npx playwright install
npx playwright install --with-deps
```

#### Authentication Issues
- Verify Jira API token hasn't expired
- Ensure email matches Jira account
- Test credentials: `curl -u email:token https://domain/rest/api/3/myself`

#### OpenAI API Issues
- Check API key validity and billing status
- Monitor rate limits for GPT-4o-mini model
- Verify model availability in your region

### Framework-Specific Debugging

#### Cypress Debugging
```bash
# Run with debug mode
DEBUG=cypress:* npx cypress run

# Open Cypress Test Runner for interactive debugging
npx cypress open
```

#### Playwright Debugging
```bash
# Run with debug mode
npx playwright test --debug

# Generate and view HTML report
npx playwright show-report

# Run with trace viewer
npx playwright test --trace on
```

## API Credentials Setup

### Jira API Token
1. Visit [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click "Create API token"
3. Name it "QA-Automation" and save the token

### OpenAI API Key
1. Go to [OpenAI API Dashboard](https://platform.openai.com/api-keys)
2. Click "Create new secret key"
3. Name it "QA-Automation" and copy the key immediately

## Performance & Comparison

### Execution Metrics
- **Cypress**: Excellent for debugging, real-time browser interaction
- **Playwright**: Superior for cross-browser testing, parallel execution
- **Combined Approach**: Maximum coverage with complementary strengths

### Best Practices
- Use Cypress for development and debugging
- Use Playwright for CI/CD and cross-browser validation
- Compare results between frameworks for comprehensive quality assurance
- Leverage framework-specific features (Cypress Studio, Playwright Codegen)


## Acknowledgments

Built with:
- [Cypress](https://cypress.io/) - End-to-end testing framework with excellent developer experience
- [Playwright](https://playwright.dev/) - Cross-browser automation library
- [OpenAI](https://openai.com/) - AI language models (GPT-4o-mini) for generation and analysis
- [LangGraph](https://langchain-ai.github.io/langgraph/) - AI workflow orchestration
- [ChromaDB](https://www.trychroma.com/) - Vector database for intelligent storage
- [Jira API](https://developer.atlassian.com/cloud/jira/) - Requirements integration
- [Colorama](https://pypi.org/project/colorama/) - Enhanced terminal output

---

*Transform your testing workflow from manual processes to AI-powered automation with dual framework support, providing comprehensive coverage through both Cypress and Playwright with intelligent, real-time failure analysis.*
