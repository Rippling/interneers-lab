import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

interface CreateCategoryPageProps {
  onCreate: (category: {
    title: string;
    description: string;
  }) => Promise<boolean>;
}

function CreateCategoryPage({ onCreate }: CreateCategoryPageProps) {
  const navigate = useNavigate();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setSaving(true);

    const created = await onCreate({ title, description });
    setSaving(false);

    if (created) {
      navigate("/categories");
    }
  };

  return (
    <section className="mx-auto max-w-3xl rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <h1 className="mb-4 text-3xl font-bold text-slate-900">Add Category</h1>
      <p className="mb-6 text-sm text-slate-500">
        Create a category for your own inventory. Other users will not see it.
      </p>

      <form className="grid gap-4" onSubmit={handleSubmit}>
        <input
          className="rounded-xl border border-slate-300 px-4 py-3"
          placeholder="Category title"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
        />
        <textarea
          className="rounded-xl border border-slate-300 px-4 py-3"
          placeholder="Description"
          rows={4}
          value={description}
          onChange={(event) => setDescription(event.target.value)}
        />

        <div className="flex items-center gap-4">
          <button
            className="rounded-xl bg-cyan-600 px-5 py-3 font-semibold text-white disabled:bg-slate-400"
            type="submit"
            disabled={saving}
          >
            {saving ? "Creating..." : "Create Category"}
          </button>
          <Link
            className="font-semibold text-slate-600 hover:underline"
            to="/categories"
          >
            Cancel
          </Link>
        </div>
      </form>
    </section>
  );
}

export default CreateCategoryPage;
