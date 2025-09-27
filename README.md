# AI-Powered QA Automation

> Automatically generate comprehensive tests from Jira requirements using artificial intelligence with triple framework support (Cypress + Playwright + Supertest) and comprehensive error handling.

[![Node.js](https://img.shields.io/badge/Node.js-v14+-green.svg)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org/)
[![Cypress](https://img.shields.io/badge/Cypress-13.17.0-brightgreen.svg)](https://cypress.io/)
[![Playwright](https://img.shields.io/badge/Playwright-Latest-blue.svg)](https://playwright.dev/)
[![Supertest](https://img.shields.io/badge/Supertest-Latest-red.svg)](https://github.com/visionmedia/supertest)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)](https://openai.com/)

## Overview

This system automates quality assurance by converting Jira requirements into executable tests using GPT-4o-mini for **three comprehensive testing frameworks**: Cypress (E2E), Playwright (E2E), and Supertest (API). It eliminates manual test writing while ensuring comprehensive coverage across UI and API layers with consistent quality. **Enhanced with comprehensive error handling and framework-specific debugging assistance.**

## Key Features

- **🎯 Triple Framework Support**: Generate test scenarios for Cypress, Playwright, and Supertest
- **⚡ Super-Fast API Testing**: Lightning-fast Supertest + Jest API validation
- **🤖 Automated Test Generation**: Transform requirements into tests in minutes across all frameworks
- **🔗 Jira Integration**: Direct pipeline from tickets to executable tests  
- **🧠 AI-Powered Analysis**: Natural language processing for complex requirements
- **⚡ Optimized Sequential Execution**: Run Cypress → Playwright → Supertest (super-fast API validation)
- **🔍 Comprehensive Error Handling**: Enhanced error detection and debugging across all frameworks
- **🧩 Framework-Specific Intelligence**: Optimized test generation for each framework's strengths
- **📊 Detailed Test Reports**: Clear execution results and framework-specific insights
- **✅ Consistent Quality**: Standardized test patterns and best practices for all frameworks
- **🔄 Multi-Layer Coverage**: API validation + E2E automation for complete testing

## ✨ Enhanced Triple Framework Architecture

### Framework Execution Flow
```
               Jira Requirements → AI Parser → GPT-4o-mini Generator
                                      ↓
                            E2E Test Generation (Cypress)
                                      ↓
                          E2E Test Generation (Playwright)
                                      ↓
                            API Test Generation (Supertest)
                                      ↓
                              Save All Test Files
                                      ↓
                             Execute Cypress Tests (E2E)
                                      ↓
                            Execute Playwright Tests (E2E)
                                      ↓
                           Execute Supertest Tests (API)
                                      ↓
                          Combined Results & Analysis
```

## Architecture

**Technology Stack:**
- **LangGraph** for AI workflow orchestration
- **OpenAI GPT-4o-mini** for intelligent test generation and failure analysis
- **Supertest + Jest** for lightning-fast API endpoint testing
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

3. **Install Node.js dependencies for all frameworks**
   ```bash
   # Install Supertest + Jest for API testing
   npm install supertest jest express --save-dev
   
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
   mkdir -p supertest/tests
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

7. **Run the triple-framework system**
   ```bash
   python qa_automation.py
   ```

## Usage

### Automated Triple Framework Execution
```bash
# Generate and run tests for all three frameworks sequentially
python qa_automation.py
```

This command will:
1. Fetch Jira requirements
2. Generate Cypress E2E test code
3. Generate Playwright E2E test code
4. Generate Supertest API test code
5. Save Cypress tests to `cypress/e2e/generated_tests.cy.js`
6. Save Playwright tests to `playwright/tests/generated_tests.spec.js`
7. Save Supertest tests to `supertest/tests/generated_tests.spec.js`
8. Execute Cypress tests first (E2E debugging)
9. Execute Playwright tests second (cross-browser E2E)
10. Execute Supertest tests third (super-fast API validation)
11. Display combined results

### Manual Framework-Specific Commands

#### Supertest + Jest Commands (API Testing)
```bash
# Run generated API tests
npx jest supertest/tests/generated_tests.spec.js

# Run all API tests with coverage
npx jest supertest/ --coverage

# Run API tests in watch mode
npx jest supertest/ --watch

# Run API tests with verbose output
npx jest supertest/ --verbose
```

#### Cypress Commands (E2E Testing)
```bash
# Run Cypress interactively
npx cypress open

# Run generated Cypress tests headlessly
npx cypress run --spec cypress/e2e/generated_tests.cy.js

# Run all Cypress tests
npx cypress run
```

#### Playwright Commands (E2E Testing)
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
├── qa_automation.py                    # Main triple-framework automation script
├── app.js                             # Auto-generated Express app for Supertest
├── cypress/
│   ├── e2e/
│   │   └── generated_tests.cy.js      # AI-generated Cypress tests
│   └── cypress.config.js
├── playwright/
│   ├── tests/
│   │   └── generated_tests.spec.js    # AI-generated Playwright tests
│   └── playwright.config.js
├── supertest/
│   ├── tests/
│   │   └── generated_tests.spec.js    # AI-generated Supertest API tests
│   └── jest.config.js
├── jira_requirements/                  # Jira requirement storage
├── vector_store/                       # ChromaDB embeddings
├── package.json
└── .env
```

## Framework Configuration

### Jest Configuration (`jest.config.js`)
```javascript
module.exports = {
  testEnvironment: 'node',
  testMatch: ['**/supertest/**/*.spec.js'],
  collectCoverageFrom: [
    'app.js',
    'routes/**/*.js'
  ],
  coverageDirectory: 'coverage',
  verbose: true,
  setupFilesAfterEnv: ['<rootDir>/supertest/setup.js']
};
```

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
All frameworks generate tests with:
- ✅ **Supertest**: Direct API endpoint testing with request/response validation
- ✅ **Cypress**: Proper test structure (`describe`/`it` blocks) with UI interaction
- ✅ **Playwright**: Modern test structure (`test.describe`/`test`) with cross-browser support
- ✅ Test data setup with realistic credentials
- ✅ Positive test cases (valid login: `tomsmith` / `SuperSecretPassword!`)
- ✅ Negative test cases (invalid credentials)
- ✅ Proper wait conditions and timeouts
- ✅ Success validation (API 200 status, UI redirect to `/secure`)
- ✅ Error handling (API 401 status, UI error messages)
- ✅ Screenshot capture on failures (E2E tests)

### Example Generated Test Output

#### Supertest API Test Structure
```javascript
const request = require('supertest');
const app = require('../../app');

describe('API Login Functionality', () => {
  test('should successfully authenticate with valid credentials', async () => {
    const response = await request(app)
      .post('/api/login')
      .send({
        username: 'tomsmith',
        password: 'SuperSecretPassword!'
      });
    
    expect(response.status).toBe(200);
    expect(response.body.message).toBe('Login successful');
  });

  test('should reject invalid credentials', async () => {
    const response = await request(app)
      .post('/api/login')
      .send({
        username: 'invalid',
        password: 'wrong'
      });
    
    expect(response.status).toBe(401);
  });
});
```

#### Cypress E2E Test Structure
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

#### Playwright E2E Test Structure
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

### Real-Time Monitoring Features
- **Comprehensive error handling** during test execution across all frameworks
- **Framework-specific debugging guidance** for API and UI issues
- **Sequential execution** with clear status reporting for each framework
- **Color-coded terminal output** for immediate issue identification
- **Post-execution summary** with framework-specific results and next steps

## Performance & Optimization

### Speed Comparison
- **Supertest**: ~100-500ms per test (API only)
- **Cypress**: ~2-5 seconds per test (UI automation)
- **Playwright**: ~3-8 seconds per test (cross-browser)

### Best Practices
- Use Supertest for rapid API feedback in development
- Use Cypress for debugging UI interactions and user flows
- Use Playwright for comprehensive cross-browser CI/CD validation
- Compare API responses with UI behavior for complete coverage
- Leverage the speed of API tests to catch issues early

## Troubleshooting

### Common Issues & Solutions

#### Framework Installation
```bash
# Supertest + Jest installation issues
npm install supertest jest express --save-dev
npm test -- --detectOpenHandles

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

#### Supertest Debugging
```bash
# Run with debug output
DEBUG=supertest npx jest supertest/

# Run single test file
npx jest supertest/tests/generated_tests.spec.js --verbose

# Check Express app manually
node -e "const app = require('./app'); console.log('Express app loaded successfully');"
```

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

## Performance Metrics & Comparison

### Execution Metrics
- **Supertest**: Ultra-fast API validation, immediate feedback on backend issues
- **Cypress**: Excellent for debugging, real-time browser interaction
- **Playwright**: Superior for cross-browser testing, parallel execution
- **Combined Approach**: Maximum coverage with layered validation (API → UI → Cross-browser)

### Coverage Benefits
- **API Layer**: Backend logic, authentication, data validation
- **UI Layer**: User experience, visual elements, user flows
- **Cross-browser**: Compatibility across different browsers and devices
- **Integration**: End-to-end data flow from API to UI

## Acknowledgments

Built with:
- [Supertest](https://github.com/visionmedia/supertest) - HTTP assertion library for API testing
- [Jest](https://jestjs.io/) - JavaScript testing framework with excellent mocking capabilities
- [Cypress](https://cypress.io/) - End-to-end testing framework with excellent developer experience
- [Playwright](https://playwright.dev/) - Cross-browser automation library
- [OpenAI](https://openai.com/) - AI language models (GPT-4o-mini) for generation and analysis
- [LangGraph](https://langchain-ai.github.io/langgraph/) - AI workflow orchestration
- [ChromaDB](https://www.trychroma.com/) - Vector database for intelligent storage
- [Jira API](https://developer.atlassian.com/cloud/jira/) - Requirements integration
- [Colorama](https://pypi.org/project/colorama/) - Enhanced terminal output

---

*Transform your testing workflow from manual processes to AI-powered automation with triple framework support, providing comprehensive coverage through API testing (Supertest), E2E automation (Cypress), and cross-browser validation (Playwright) with comprehensive error handling and framework-specific debugging guidance.*
