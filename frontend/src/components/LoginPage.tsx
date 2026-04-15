import React, { useState } from "react";

interface LoginPageProps {
  onLogin: (username: string, password: string) => Promise<boolean>;
  onSwitchToSignup: () => void;
}

function LoginPage({ onLogin, onSwitchToSignup }: LoginPageProps) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setSubmitting(true);
    await onLogin(username, password);
    setSubmitting(false);
  };

  return (
    <section className="mx-auto flex min-h-[70vh] max-w-7xl items-center justify-center px-6 py-10">
      <div className="w-full max-w-md rounded-3xl border border-slate-200 bg-white p-8 shadow-xl">
        <h1 className="text-3xl font-bold text-slate-900">Login</h1>

        <form className="mt-6 grid gap-4" onSubmit={handleSubmit}>
          <input
            className="rounded-xl border border-slate-300 px-4 py-3"
            placeholder="Username"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
          />
          <input
            className="rounded-xl border border-slate-300 px-4 py-3"
            type="password"
            placeholder="Password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />

          <button
            className="rounded-xl bg-cyan-600 px-5 py-3 font-semibold text-white"
            type="submit"
            disabled={submitting}
          >
            {submitting ? "Signing in..." : "Login"}
          </button>
        </form>

        <button
          className="mt-4 text-sm font-semibold text-cyan-700 hover:underline"
          onClick={onSwitchToSignup}
        >
          Don’t have an account? Sign up
        </button>
      </div>
    </section>
  );
}

export default LoginPage;
