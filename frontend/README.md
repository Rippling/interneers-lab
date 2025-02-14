# Bootcamp Frontend

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app), along with a few additional pacakges like SCSS, TypeScript, React router and Playwright.

## Table of Contents

-   [Getting Started](#getting-started)
-   [Setup](#setup)
-   [Running the Development Server](#running-the-development-server)
-   [Trying Things Out](#trying-things-out)
-   [Running Tests](#running-tests)
-   [Learn More](#learn-more)


## Getting Started

A general introduction to your project and its purpose. Explain what the app does and any key features.

## Setup

This section describes how to set up the project locally. Since the project files are already present, the setup is straightforward.

1.  **Navigate to the Project Directory:**

    ```bash
    cd bootcamp_frontend
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

## Trying Things Out

This section provides some examples of how to modify the code and see the results in your local development environment.  Make sure the development server is running (`yarn start`) before trying these examples.

1.  **Editing `App.tsx`:**

    Open the `src/App.tsx` file in your code editor.  Make some changes to the content within the `App` component (e.g., change the text, add a new element). Save the file, and your changes will be automatically reflected in your browser.

2.  **SCSS Example:**

    In `src/App.tsx`, replace the line:

    ```typescript
    import './App.css';
    ```

    with:

    ```typescript
    import './App.scss';
    ```

    Save the file.  Now, any styles defined in `src/App.scss` will be applied to your application.  Modify `src/App.scss` to see the changes.

3.  **Routing Example:**

    In `src/index.tsx`, replace the line:

    ```typescript
    import App from './App';
    ```

    with:

    ```typescript
    import App from './AppWithRouter';
    ```

    Save the file.  This will enable routing in your application.

4.  **API Call Example:**

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

    ```bash
    yarn test
    ```

    These tests verify the functionality of individual components or functions in isolation. They are typically located in the `src/__tests__` directory (or alongside the components they test).

    Here are some additional commands for unit tests:

    *   **Run all tests in watch mode:**

        ```bash
        yarn test --watchAll
        ```

        This will run all tests and re-run them automatically whenever you make changes to your code.

    *   **Run a specific test file:**

        ```bash
        yarn test bootcamp_frontend/src/App.test.tsx  # Replace with the actual path
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
    yarn playwright install
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