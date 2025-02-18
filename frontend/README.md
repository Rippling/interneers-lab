# Interneers Lab 2025 - Frontend

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app), along with a few additional packages like SCSS, TypeScript, React router and Playwright.

## Table of Contents

-   [Getting Started](#getting-started)
-   [Prerequisites](#prerequisites)
-   [Setup](#setup)
-   [Running the Development Server](#running-the-development-server)
-   [Editor Setup - VS Code (Optional)](#editor-setup---vs-code-optional)
-   [Trying Things Out](#trying-things-out)
-   [Running Tests](#running-tests)
-   [Learn More](#learn-more)


## Getting Started

Welcome to the Engineers Lab 2025 frontend! This project provides a foundation for building web applications using React, TypeScript, and other related technologies. This README will guide you through the setup process and provide instructions on how to run the development server, explore various features, and execute tests.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- [Node.js Downloads](https://nodejs.org/en/download/)  
- [Yarn Install Docs](https://classic.yarnpkg.com/lang/en/docs/install/)  

**Verify**
- Check version and installation completion with `node --version` and `yarn --version` 


## Setup

This section describes how to set up the project locally. Since the project files are already present, the setup is straightforward.

1.  **Navigate to the Project Directory:**

    ```bash
    # All frontend commands should be run from the "frontend" directory
    cd frontend
    ```

2.  **Install Dependencies (One Time):**

    ```bash
    yarn install
    ```

    This command will install all the required dependencies listed in the `yarn.lock` file. You only need to run this command *once* when you first set up the project. If you later add new dependencies, you'll need to run it again.

## Running the Development Server

This section explains how to start the development server.

1.  **Start the Server:**

    ```bash
    yarn start
    ```

    This command will start the development server and automatically open the application in your default web browser.

2.  **Access the Application:**

    If the application doesn't open automatically, you can access it by navigating to `http://localhost:3000` in your web browser.

3.  **Editing `App.tsx`:**

    Open the `src/App.tsx` file in your code editor.  Make some changes to the content within the `App` component (e.g., change the text, add a new element). Save the file, and your changes will be automatically reflected in your browser.

4.  **Handling Port Conflicts:**

    If you encounter an error message indicating that port 3000 is already in use, you can change the port by modifying the `.env` file in the root of your project.

    *   Open the `.env` file.
    *   Change the `PORT=3000` line to a different port number, such as `PORT=3001`.
    *   Save the `.env` file.
    *   Run `yarn start` again.

    Alternatively, you can use the following command to start the server on a different port directly:

    ```bash
    PORT=3001 yarn start   # macOS
    $env:PORT = 3001; yarn start # Windows Powershell
    # Replace 3001 with your desired port
    ```

    The development server will now attempt to start on the new port you specified.

***Note:*** The first section here is primarily for testing that your setup is correct. The remaining sections are for you to explore and play around with if you'd like. We will be covering all of these items in the later weeks of the curriculum.

## Editor Setup - VS Code (Optional)

This project includes a `.vscode` folder with recommended settings for Visual Studio Code. To take advantage of these settings, especially the integration between ESLint and Prettier for automatic code formatting, please install the following extension:

-   **ESLint:** [link](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)

Once the ESLint extension is installed, VS Code will automatically use the settings in the `.vscode` folder to lint and format your code.

## Trying Things Out

This section provides some examples of how to modify the code and see the results in your local development environment.  Make sure the development server is running (`yarn start`) before trying these examples.

1.  **SCSS Example:**

    In `src/App.tsx`, replace the line:

    ```typescript
    import './App.css';
    ```

    with:

    ```typescript
    import './App.scss';
    ```

    Save the file.  Now, any styles defined in `src/App.scss` will be applied to your application.  Modify `src/App.scss` to see the changes.

2.  **Routing Example:**

    In `src/index.tsx`, replace the line:

    ```typescript
    import App from './App';
    ```

    with:

    ```typescript
    import App from './AppWithRouter';
    ```

    Save the file.  This will enable routing in your application.

3.  **API Call Example:**

    In `src/index.tsx`, replace the line:

    ```typescript
    import App from './App';
    ```

    with:

    ```typescript
    import App from './AppWithApi';
    ```

    Save the file. This will demonstrate how to make an API call in your application.

## Running Tests

This section describes how to run the project's tests. There are two types of tests in this project:

1.  **Unit Tests (Jest):**

    These tests verify the functionality of individual components or functions in isolation. They are typically located in the `src/__tests__` directory (or alongside the components they test).

    ```bash
    yarn test
    ```

    When you run the unit tests, you'll see that one test passes and one test fails. This is intentional. The failing test demonstrates what a failed test looks like. It's looking for the text "learn lorem ipsum react" within the `src/App.tsx` component, but the actual text in the component is "Learn React", which is why the test fails.


    Here are some additional commands for unit tests:

    *   **Run all tests in watch mode:**

        ```bash
        yarn test --watchAll
        ```

        This will run all tests and re-run them automatically whenever you make changes to your code.

    *   **Run a specific test file:**

        ```bash
        yarn test src/__tests__/App.test.tsx  # Replace with the actual path
        ```

        This command allows you to run a single test file.

    *   **Generate code coverage report:**

        ```bash
        yarn test -- --coverage
        ```

        This will generate a code coverage report, showing how much of your code is covered by your tests. The report will usually be in the `coverage` directory.

2.  **End-to-End Tests (Playwright):**

    These tests simulate user interactions with the application in a real browser environment.

    Before running Playwright tests, ensure Playwright browsers are installed:

    ```bash
    yarn playwright install # One time setup
    ```

    Now you can run the tests:

    ```bash
    yarn playwright test
    ```

    Here are some additional commands for Playwright tests:

    *   **Run Playwright tests in headed mode (visible browser):**

        ```bash
        yarn playwright test -- --headed
        ```

    *   **Run Playwright tests in debug mode:**

        ```bash
        yarn playwright test -- --debug
        ```

        You can combine `--headed` and `--debug` flags.

    *   **Show the HTML report of the tests:**

        ```bash
        yarn playwright show-report
        ```

## Learn More

This section provides links to relevant documentation and resources for further learning.

*   **Create React App:** [https://create-react-app.dev/](https://create-react-app.dev/)
*   **React Documentation:** [https://react.dev/learn](https://react.dev/learn)
*   **React Router Documentation:** [https://reactrouter.com/home](https://reactrouter.com/home)
*   **TypeScript Documentation:** [https://www.typescriptlang.org/docs/](https://www.typescriptlang.org/docs/)
*   **Sass Documentation:** [https://sass-lang.com/documentation](https://sass-lang.com/documentation)
*   **Jest Documentation:** [https://jestjs.io/docs/getting-started](https://jestjs.io/docs/getting-started)
*   **Playwright Documentation:** [https://playwright.dev/docs/intro](https://playwright.dev/docs/intro)
