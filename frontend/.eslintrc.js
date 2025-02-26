module.exports = {
  extends: [
    "react-app", // Or your existing ESLint config
    "prettier", // This makes eslint-config-prettier active. It disables all formatting rules that might conflict with prettier.
  ],
  plugins: ["prettier"], // This enables eslint-plugin-prettier. Sets up rules to run prettier as an eslint rule.
  rules: {
    "prettier/prettier": ["error", { endOfLine: "auto" }], // This will display prettier errors as ESLint errors. The 'error' severity means that these errors will cause your build to fail. You can change this to 'warn' if you prefer.
  },
};
