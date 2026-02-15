'use client';

import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';
import { workspaceApi } from '@/lib/api';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

interface Workspace {
  id: string;
  name: string;
  description?: string;
  created_at: string;
}

export default function DashboardPage() {
  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newWorkspaceName, setNewWorkspaceName] = useState('');
  const [newWorkspaceDesc, setNewWorkspaceDesc] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  useEffect(() => {
    checkAuth();
    loadWorkspaces();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const checkAuth = async () => {
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) {
      router.push('/login');
    }
  };

  const loadWorkspaces = async () => {
    try {
      const data = await workspaceApi.list();
      setWorkspaces(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateWorkspace = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      await workspaceApi.create({
        name: newWorkspaceName,
        description: newWorkspaceDesc || undefined,
      });
      
      setShowCreateModal(false);
      setNewWorkspaceName('');
      setNewWorkspaceDesc('');
      loadWorkspaces();
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleLogout = async () => {
    await supabase.auth.signOut();
    router.push('/');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold tracking-tight text-gray-900">
            My Workspaces
          </h1>
          <button
            onClick={handleLogout}
            className="rounded-md bg-gray-600 px-4 py-2 text-sm font-semibold text-white hover:bg-gray-500"
          >
            Logout
          </button>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {error && (
          <div className="mb-4 rounded-md bg-red-50 p-4">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        {loading ? (
          <div className="text-center">
            <p className="text-gray-500">Loading workspaces...</p>
          </div>
        ) : (
          <>
            <div className="mb-6">
              <button
                onClick={() => setShowCreateModal(true)}
                className="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-500"
              >
                Create Workspace
              </button>
            </div>

            {workspaces.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-gray-500">No workspaces yet. Create your first workspace to get started!</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {workspaces.map((workspace) => (
                  <Link
                    key={workspace.id}
                    href={`/workspace/${workspace.id}`}
                    className="block rounded-lg bg-white p-6 shadow hover:shadow-lg transition-shadow"
                  >
                    <h3 className="text-lg font-semibold text-gray-900">{workspace.name}</h3>
                    {workspace.description && (
                      <p className="mt-2 text-sm text-gray-600">{workspace.description}</p>
                    )}
                    <p className="mt-4 text-xs text-gray-400">
                      Created {new Date(workspace.created_at).toLocaleDateString()}
                    </p>
                  </Link>
                ))}
              </div>
            )}
          </>
        )}
      </main>

      {/* Create Workspace Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-xl font-bold mb-4">Create New Workspace</h2>
            <form onSubmit={handleCreateWorkspace}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Workspace Name *
                  </label>
                  <input
                    type="text"
                    required
                    value={newWorkspaceName}
                    onChange={(e) => setNewWorkspaceName(e.target.value)}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900"
                    placeholder="My Workspace"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Description
                  </label>
                  <textarea
                    value={newWorkspaceDesc}
                    onChange={(e) => setNewWorkspaceDesc(e.target.value)}
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
