'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { workspaceApi, listApi } from '@/lib/api';
import { authService } from '@/lib/auth';

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
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedList, setSelectedList] = useState<List | null>(null);
  const [newListName, setNewListName] = useState('');
  const [newListDesc, setNewListDesc] = useState('');
  const [error, setError] = useState('');
  const [creating, setCreating] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const initPage = async () => {
      if (!authService.isAuthenticated()) {
        router.push('/login');
        return;
      }
      
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
    
    initPage();
  }, [workspaceId, router]);

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
    }
  };

  const handleCreateList = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Prevent double submissions
    if (creating) return;
    
    setError('');
    setCreating(true);

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
    } finally {
      setCreating(false);
    }
  };

  const handleEditList = async (e: React.FormEvent) => {
    e.preventDefault();
    if (submitting || !selectedList) return;
    
    setError('');
    setSubmitting(true);

    try {
      await listApi.update(selectedList.id, {
        name: newListName,
        description: newListDesc || undefined,
      });

      setShowEditModal(false);
      setSelectedList(null);
      setNewListName('');
      setNewListDesc('');
      loadData();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteList = async () => {
    if (submitting || !selectedList) return;
    
    setError('');
    setSubmitting(true);

    try {
      await listApi.delete(selectedList.id);

      setShowDeleteModal(false);
      setSelectedList(null);
      loadData();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const openEditModal = (list: List, e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setSelectedList(list);
    setNewListName(list.name);
    setNewListDesc(list.description || '');
    setShowEditModal(true);
  };

  const openDeleteModal = (list: List, e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setSelectedList(list);
    setShowDeleteModal(true);
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
              <div
                key={list.id}
                className="relative rounded-lg bg-white p-6 shadow hover:shadow-lg transition-shadow"
              >
                <Link href={`/workspace/${workspaceId}/list/${list.id}`} className="block">
                  <h3 className="text-lg font-semibold text-gray-900 pr-16">{list.name}</h3>
                  {list.description && (
                    <p className="mt-2 text-sm text-gray-600">{list.description}</p>
                  )}
                  <p className="mt-4 text-xs text-gray-400">
                    Created {new Date(list.created_at).toLocaleDateString()}
                  </p>
                </Link>
                <div className="absolute top-4 right-4 flex gap-2">
                  <button
                    onClick={(e) => openEditModal(list, e)}
                    className="p-1.5 rounded hover:bg-gray-100 text-gray-600 hover:text-blue-600"
                    title="Edit list"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button
                    onClick={(e) => openDeleteModal(list, e)}
                    className="p-1.5 rounded hover:bg-gray-100 text-gray-600 hover:text-red-600"
                    title="Delete list"
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
                  disabled={creating}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  disabled={creating}
                >
                  {creating ? 'Creating...' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit List Modal */}
      {showEditModal && selectedList && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-xl font-bold mb-4">Edit List</h2>
            <form onSubmit={handleEditList}>
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
                  onClick={() => {
                    setShowEditModal(false);
                    setSelectedList(null);
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

      {/* Delete List Modal */}
      {showDeleteModal && selectedList && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-xl font-bold mb-4 text-red-600">Delete List</h2>
            <p className="text-gray-700 mb-6">
              Are you sure you want to delete <strong>{selectedList.name}</strong>? 
              This action cannot be undone and will delete all columns and items within this list.
            </p>
            <div className="flex gap-3 justify-end">
              <button
                type="button"
                onClick={() => {
                  setShowDeleteModal(false);
                  setSelectedList(null);
                }}
                className="rounded-md bg-gray-200 px-4 py-2 text-sm font-semibold text-gray-900 hover:bg-gray-300"
                disabled={submitting}
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteList}
                className="rounded-md bg-red-600 px-4 py-2 text-sm font-semibold text-white hover:bg-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
                disabled={submitting}
              >
                {submitting ? 'Deleting...' : 'Delete List'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
