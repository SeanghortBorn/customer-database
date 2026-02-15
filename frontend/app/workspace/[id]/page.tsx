'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { workspaceApi, listApi } from '@/lib/api';
import { supabase } from '@/lib/supabase';

interface Workspace {
  id: string;
  name: string;
  description?: string;
}

interface List {
  id: string;
  name: string;
  description?: string;
  created_at: string;
}

export default function WorkspacePage() {
  const params = useParams();
  const router = useRouter();
  const workspaceId = params.id as string;

  const [workspace, setWorkspace] = useState<Workspace | null>(null);
  const [lists, setLists] = useState<List[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newListName, setNewListName] = useState('');
  const [newListDesc, setNewListDesc] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    checkAuth();
    loadData();
  }, [workspaceId]);

  const checkAuth = async () => {
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) {
      router.push('/login');
    }
  };

  const loadData = async () => {
    try {
      const [workspaceData, listsData] = await Promise.all([
        workspaceApi.get(workspaceId),
        listApi.list(workspaceId),
      ]);
      setWorkspace(workspaceData);
      setLists(listsData);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateList = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      await listApi.create(workspaceId, {
        name: newListName,
        description: newListDesc || undefined,
      });

      setShowCreateModal(false);
      setNewListName('');
      setNewListDesc('');
      loadData();
    } catch (err: any) {
      setError(err.message);
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-gray-500">Loading...</p>
      </div>
    );
  }

  if (!workspace) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-red-500">Workspace not found</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div>
              <Link
                href="/dashboard"
                className="text-sm text-blue-600 hover:text-blue-500 mb-2 inline-block"
              >
                ← Back to Workspaces
              </Link>
              <h1 className="text-3xl font-bold tracking-tight text-gray-900">
                {workspace.name}
              </h1>
              {workspace.description && (
                <p className="mt-1 text-sm text-gray-600">{workspace.description}</p>
              )}
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {error && (
          <div className="mb-4 rounded-md bg-red-50 p-4">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        <div className="mb-6">
          <button
            onClick={() => setShowCreateModal(true)}
            className="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-500"
          >
            Create List
          </button>
        </div>

        {lists.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500">No lists yet. Create your first list to start organizing data!</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {lists.map((list) => (
              <Link
                key={list.id}
                href={`/workspace/${workspaceId}/list/${list.id}`}
                className="block rounded-lg bg-white p-6 shadow hover:shadow-lg transition-shadow"
              >
                <h3 className="text-lg font-semibold text-gray-900">{list.name}</h3>
                {list.description && (
                  <p className="mt-2 text-sm text-gray-600">{list.description}</p>
                )}
                <p className="mt-4 text-xs text-gray-400">
                  Created {new Date(list.created_at).toLocaleDateString()}
                </p>
              </Link>
            ))}
          </div>
        )}
      </main>

      {/* Create List Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-xl font-bold mb-4">Create New List</h2>
            <form onSubmit={handleCreateList}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    List Name *
                  </label>
                  <input
                    type="text"
                    required
                    value={newListName}
                    onChange={(e) => setNewListName(e.target.value)}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900"
                    placeholder="Customers"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Description
                  </label>
                  <textarea
                    value={newListDesc}
                    onChange={(e) => setNewListDesc(e.target.value)}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900"
                    rows={3}
                    placeholder="Optional description"
                  />
                </div>
              </div>
              <div className="mt-6 flex gap-3 justify-end">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="rounded-md bg-gray-200 px-4 py-2 text-sm font-semibold text-gray-900 hover:bg-gray-300"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-500"
                >
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
