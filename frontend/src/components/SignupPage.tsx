import React, { useState } from "react";

interface SignupPageProps {
  onSignup: (
    username: string,
    email: string,
    password: string,
  ) => Promise<boolean>;
  onSwitchToLogin: () => void;
}

function SignupPage({ onSignup, onSwitchToLogin }: SignupPageProps) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setSubmitting(true);
    await onSignup(username, email, password);
    setSubmitting(false);
  };

  return (
    <section className="mx-auto flex min-h-[70vh] max-w-7xl items-center justify-center px-6 py-10">
      <div className="w-full max-w-md rounded-3xl border border-slate-200 bg-white p-8 shadow-xl">
        <h1 className="text-3xl font-bold text-slate-900">Sign Up</h1>

        <form className="mt-6 grid gap-4" onSubmit={handleSubmit}>
          <input
            className="rounded-xl border border-slate-300 px-4 py-3"
            placeholder="Username"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
          />
          <input
            className="rounded-xl border border-slate-300 px-4 py-3"
            placeholder="Email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
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
            {submitting ? "Creating..." : "Create Account"}
          </button>
        </form>

        <button
          className="mt-4 text-sm font-semibold text-cyan-700 hover:underline"
          onClick={onSwitchToLogin}
        >
          Already have an account? Login
        </button>
      </div>
    </section>
  );
}

export default SignupPage;
