'use client';

import { useEffect, useState } from 'react';
import { authService } from '@/lib/auth';
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
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedWorkspace, setSelectedWorkspace] = useState<Workspace | null>(null);
  const [newWorkspaceName, setNewWorkspaceName] = useState('');
  const [newWorkspaceDesc, setNewWorkspaceDesc] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const router = useRouter();

  useEffect(() => {
    checkAuth();
    loadWorkspaces();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const checkAuth = async () => {
    if (!authService.isAuthenticated()) {
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
    if (submitting) return;
    
    setError('');
    setSubmitting(true);

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
    } finally {
      setSubmitting(false);
    }
  };

  const handleEditWorkspace = async (e: React.FormEvent) => {
    e.preventDefault();
    if (submitting || !selectedWorkspace) return;
    
    setError('');
    setSubmitting(true);

    try {
      await workspaceApi.update(selectedWorkspace.id, {
        name: newWorkspaceName,
        description: newWorkspaceDesc || undefined,
      });
      
      setShowEditModal(false);
      setSelectedWorkspace(null);
      setNewWorkspaceName('');
      setNewWorkspaceDesc('');
      loadWorkspaces();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteWorkspace = async () => {
    if (submitting || !selectedWorkspace) return;
    
    setError('');
    setSubmitting(true);

    try {
      await workspaceApi.delete(selectedWorkspace.id);
      
      setShowDeleteModal(false);
      setSelectedWorkspace(null);
      loadWorkspaces();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const openEditModal = (workspace: Workspace, e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setSelectedWorkspace(workspace);
    setNewWorkspaceName(workspace.name);
    setNewWorkspaceDesc(workspace.description || '');
    setShowEditModal(true);
  };

  const openDeleteModal = (workspace: Workspace, e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setSelectedWorkspace(workspace);
    setShowDeleteModal(true);
  };

  const handleLogout = async () => {
    authService.logout();
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
                  <div
                    key={workspace.id}
                    className="relative rounded-lg bg-white p-6 shadow hover:shadow-lg transition-shadow"
                  >
                    <Link href={`/workspace/${workspace.id}`} className="block">
                      <h3 className="text-lg font-semibold text-gray-900">{workspace.name}</h3>
                      {workspace.description && (
                        <p className="mt-2 text-sm text-gray-600">{workspace.description}</p>
                      )}
                      <p className="mt-4 text-xs text-gray-400">
                        Created {new Date(workspace.created_at).toLocaleDateString()}
                      </p>
                    </Link>
                    <div className="absolute top-4 right-4 flex gap-2">
                      <button
                        onClick={(e) => openEditModal(workspace, e)}
                        className="p-1.5 rounded hover:bg-gray-100 text-gray-600 hover:text-blue-600"
                        title="Edit workspace"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </button>
                      <button
                        onClick={(e) => openDeleteModal(workspace, e)}
                        className="p-1.5 rounded hover:bg-gray-100 text-gray-600 hover:text-red-600"
                        title="Delete workspace"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </div>
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
                  disabled={submitting}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  disabled={submitting}
                >
                  {submitting ? 'Creating...' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit Workspace Modal */}
      {showEditModal && selectedWorkspace && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-xl font-bold mb-4">Edit Workspace</h2>
            <form onSubmit={handleEditWorkspace}>
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
                  onClick={() => {
                    setShowEditModal(false);
                    setSelectedWorkspace(null);
                  }}
                  className="rounded-md bg-gray-200 px-4 py-2 text-sm font-semibold text-gray-900 hover:bg-gray-300"
                  disabled={submitting}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  disabled={submitting}
                >
                  {submitting ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Delete Workspace Modal */}
      {showDeleteModal && selectedWorkspace && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-xl font-bold mb-4 text-red-600">Delete Workspace</h2>
            <p className="text-gray-700 mb-6">
              Are you sure you want to delete <strong>{selectedWorkspace.name}</strong>? 
              This action cannot be undone and will delete all lists, items, and data within this workspace.
            </p>
            <div className="flex gap-3 justify-end">
              <button
                type="button"
                onClick={() => {
                  setShowDeleteModal(false);
                  setSelectedWorkspace(null);
                }}
                className="rounded-md bg-gray-200 px-4 py-2 text-sm font-semibold text-gray-900 hover:bg-gray-300"
                disabled={submitting}
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteWorkspace}
                className="rounded-md bg-red-600 px-4 py-2 text-sm font-semibold text-white hover:bg-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
                disabled={submitting}
              >
                {submitting ? 'Deleting...' : 'Delete Workspace'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
