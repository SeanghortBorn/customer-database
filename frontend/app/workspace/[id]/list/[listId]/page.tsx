'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { listApi, columnApi, itemApi } from '@/lib/api';
import { authService } from '@/lib/auth';

interface List {
  id: string;
  workspace_id: string;
  name: string;
  description?: string;
}

interface Column {
  id: string;
  key: string;
  name: string;
  type: string;
  position?: number;
}

interface Item {
  id: string;
  title?: string;
  values: Record<string, any>;
  created_at: string;
}

export default function ListPage() {
  const params = useParams();
  const router = useRouter();
  const workspaceId = params.id as string;
  const listId = params.listId as string;

  const [list, setList] = useState<List | null>(null);
  const [columns, setColumns] = useState<Column[]>([]);
  const [items, setItems] = useState<Item[]>([]);
  const [loading, setLoading] = useState(true);
  const [showColumnModal, setShowColumnModal] = useState(false);
  const [showEditColumnModal, setShowEditColumnModal] = useState(false);
  const [showDeleteColumnModal, setShowDeleteColumnModal] = useState(false);
  const [selectedColumn, setSelectedColumn] = useState<Column | null>(null);
  const [showItemModal, setShowItemModal] = useState(false);
  const [showEditItemModal, setShowEditItemModal] = useState(false);
  const [showDeleteItemModal, setShowDeleteItemModal] = useState(false);
  const [selectedItem, setSelectedItem] = useState<Item | null>(null);
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  // Column form state
  const [columnKey, setColumnKey] = useState('');
  const [columnName, setColumnName] = useState('');
  const [columnType, setColumnType] = useState('text');

  // Item form state
  const [itemTitle, setItemTitle] = useState('');
  const [itemValues, setItemValues] = useState<Record<string, any>>({});

  useEffect(() => {
    checkAuth();
    loadData();
  }, [listId]);

  const checkAuth = async () => {
    if (!authService.isAuthenticated()) {
      router.push('/login');
    }
  };

  const loadData = async () => {
    try {
      const [listData, columnsData, itemsData] = await Promise.all([
        listApi.get(listId),
        columnApi.list(listId),
        itemApi.list(listId),
      ]);
      setList(listData);
      setColumns(columnsData.sort((a: Column, b: Column) => 
        (a.position || 0) - (b.position || 0)
      ));
      setItems(itemsData);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateColumn = async (e: React.FormEvent) => {
    e.preventDefault();
    if (submitting) return;
    
    setError('');
    setSubmitting(true);

    try {
      await columnApi.create(listId, {
        key: columnKey,
        name: columnName,
        type: columnType,
      });

      setShowColumnModal(false);
      setColumnKey('');
      setColumnName('');
      setColumnType('text');
      loadData();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleEditColumn = async (e: React.FormEvent) => {
    e.preventDefault();
    if (submitting || !selectedColumn) return;
    
    setError('');
    setSubmitting(true);

    try {
      await columnApi.update(selectedColumn.id, {
        name: columnName,
        type: columnType,
      });

      setShowEditColumnModal(false);
      setSelectedColumn(null);
      setColumnKey('');
      setColumnName('');
      setColumnType('text');
      loadData();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteColumn = async () => {
    if (submitting || !selectedColumn) return;
    
    setError('');
    setSubmitting(true);

    try {
      await columnApi.delete(selectedColumn.id);

      setShowDeleteColumnModal(false);
      setSelectedColumn(null);
      loadData();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const openEditColumnModal = (column: Column) => {
    setSelectedColumn(column);
    setColumnKey(column.key);
    setColumnName(column.name);
    setColumnType(column.type);
    setShowEditColumnModal(true);
  };

  const openDeleteColumnModal = (column: Column) => {
    setSelectedColumn(column);
    setShowDeleteColumnModal(true);
  };

  const handleCreateItem = async (e: React.FormEvent) => {
    e.preventDefault();
    if (submitting) return;
    
    setError('');
    setSubmitting(true);

    try {
      await itemApi.create(listId, {
        title: itemTitle || undefined,
        values: itemValues,
      });

      setShowItemModal(false);
      setItemTitle('');
      setItemValues({});
      loadData();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleEditItem = async (e: React.FormEvent) => {
    e.preventDefault();
    if (submitting || !selectedItem) return;
    
    setError('');
    setSubmitting(true);

    try {
      await itemApi.update(selectedItem.id, {
        title: itemTitle || undefined,
        values: itemValues,
      });

      setShowEditItemModal(false);
      setSelectedItem(null);
      setItemTitle('');
      setItemValues({});
      loadData();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteItem = async () => {
    if (submitting || !selectedItem) return;
    
    setError('');
    setSubmitting(true);

    try {
      await itemApi.delete(selectedItem.id);

      setShowDeleteItemModal(false);
      setSelectedItem(null);
      loadData();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const openEditItemModal = (item: Item) => {
    setSelectedItem(item);
    setItemTitle(item.title || '');
    setItemValues(item.values || {});
    setShowEditItemModal(true);
  };

  const openDeleteItemModal = (item: Item) => {
    setSelectedItem(item);
    setShowDeleteItemModal(true);
  };

  const handleItemValueChange = (columnKey: string, value: any) => {
    setItemValues(prev => ({ ...prev, [columnKey]: value }));
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-gray-500">Loading...</p>
      </div>
    );
  }

  if (!list) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-red-500">List not found</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          <Link
            href={`/workspace/${workspaceId}`}
            className="text-sm text-blue-600 hover:text-blue-500 mb-2 inline-block"
          >
            ← Back to Workspace
          </Link>
          <h1 className="text-3xl font-bold tracking-tight text-gray-900">
            {list.name}
          </h1>
          {list.description && (
            <p className="mt-1 text-sm text-gray-600">{list.description}</p>
          )}
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {error && (
          <div className="mb-4 rounded-md bg-red-50 p-4">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        <div className="mb-6 flex gap-3">
          <button
            onClick={() => setShowColumnModal(true)}
            className="rounded-md bg-green-600 px-4 py-2 text-sm font-semibold text-white hover:bg-green-500"
          >
            Add Column
          </button>
          <button
            onClick={() => setShowItemModal(true)}
            className="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-500"
            disabled={columns.length === 0}
          >
            Add Item
          </button>
        </div>

        {columns.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <p className="text-gray-500">No columns yet. Add columns to define your data structure!</p>
          </div>
        ) : (
          <div className="bg-white shadow rounded-lg overflow-hidden">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Title
                    </th>
                    {columns.map((col) => (
                      <th
                        key={col.id}
                        className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            {col.name}
                            <span className="ml-1 text-gray-400">({col.type})</span>
                          </div>
                          <div className="flex gap-1">
                            <button
                              onClick={() => openEditColumnModal(col)}
                              className="p-1 rounded hover:bg-gray-200 text-gray-600 hover:text-blue-600"
                              title="Edit column"
                            >
                              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                              </svg>
                            </button>
                            <button
                              onClick={() => openDeleteColumnModal(col)}
                              className="p-1 rounded hover:bg-gray-200 text-gray-600 hover:text-red-600"
                              title="Delete column"
                            >
                              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                              </svg>
                            </button>
                          </div>
                        </div>
                      </th>
                    ))}
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {items.length === 0 ? (
                    <tr>
                      <td
                        colSpan={columns.length + 2}
                        className="px-6 py-4 text-center text-sm text-gray-500"
                      >
                        No items yet. Click "Add Item" to get started!
                      </td>
                    </tr>
                  ) : (
                    items.map((item) => (
                      <tr key={item.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {item.title || '-'}
                        </td>
                        {columns.map((col) => (
                          <td key={col.id} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {item.values[col.key] !== undefined && item.values[col.key] !== null
                              ? String(item.values[col.key])
                              : '-'}
                          </td>
                        ))}
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          <div className="flex gap-2">
                            <button
                              onClick={() => openEditItemModal(item)}
                              className="p-1 rounded hover:bg-gray-100 text-gray-600 hover:text-blue-600"
                              title="Edit item"
                            >
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                              </svg>
                            </button>
                            <button
                              onClick={() => openDeleteItemModal(item)}
                              className="p-1 rounded hover:bg-gray-100 text-gray-600 hover:text-red-600"
                              title="Delete item"
                            >
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                              </svg>
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>

      {/* Create Column Modal */}
      {showColumnModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-xl font-bold mb-4">Add New Column</h2>
            <form onSubmit={handleCreateColumn}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Column Key (identifier) *
                  </label>
                  <input
                    type="text"
                    required
                    value={columnKey}
                    onChange={(e) => setColumnKey(e.target.value)}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900"
                    placeholder="customer_name"
                    pattern="[a-z_]+"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Display Name *
                  </label>
                  <input
                    type="text"
                    required
                    value={columnName}
                    onChange={(e) => setColumnName(e.target.value)}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900"
                    placeholder="Customer Name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Type *
                  </label>
                  <select
                    value={columnType}
                    onChange={(e) => setColumnType(e.target.value)}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900"
                  >
                    <option value="text">Text</option>
                    <option value="number">Number</option>
                    <option value="date">Date</option>
                    <option value="email">Email</option>
                    <option value="phone">Phone</option>
                    <option value="url">URL</option>
                  </select>
                </div>
              </div>
              <div className="mt-6 flex gap-3 justify-end">
                <button
                  type="button"
                  onClick={() => setShowColumnModal(false)}
                  className="rounded-md bg-gray-200 px-4 py-2 text-sm font-semibold text-gray-900 hover:bg-gray-300"
                  disabled={submitting}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="rounded-md bg-green-600 px-4 py-2 text-sm font-semibold text-white hover:bg-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  disabled={submitting}
                >
                  {submitting ? 'Creating...' : 'Add Column'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Create Item Modal */}
      {showItemModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full max-h-[80vh] overflow-y-auto">
            <h2 className="text-xl font-bold mb-4">Add New Item</h2>
            <form onSubmit={handleCreateItem}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Title (optional)
                  </label>
                  <input
                    type="text"
                    value={itemTitle}
                    onChange={(e) => setItemTitle(e.target.value)}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900"
                    placeholder="Item title"
                  />
                </div>
                {columns.map((col) => (
                  <div key={col.id}>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      {col.name}
                    </label>
                    <input
                      type={col.type === 'number' ? 'number' : col.type === 'date' ? 'date' : 'text'}
                      value={itemValues[col.key] || ''}
                      onChange={(e) => handleItemValueChange(col.key, e.target.value)}
                      className="w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900"
                      placeholder={`Enter ${col.name.toLowerCase()}`}
                    />
                  </div>
                ))}
              </div>
              <div className="mt-6 flex gap-3 justify-end">
                <button
                  type="button"
                  onClick={() => setShowItemModal(false)}
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
                  {submitting ? 'Creating...' : 'Add Item'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit Column Modal */}
      {showEditColumnModal && selectedColumn && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-xl font-bold mb-4">Edit Column</h2>
            <form onSubmit={handleEditColumn}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Column Key (cannot be changed)
                  </label>
                  <input
                    type="text"
                    disabled
                    value={columnKey}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-gray-500 bg-gray-100"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Display Name *
                  </label>
                  <input
                    type="text"
                    required
                    value={columnName}
                    onChange={(e) => setColumnName(e.target.value)}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900"
                    placeholder="Customer Name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Type *
                  </label>
                  <select
                    value={columnType}
                    onChange={(e) => setColumnType(e.target.value)}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900"
                  >
                    <option value="text">Text</option>
                    <option value="number">Number</option>
                    <option value="date">Date</option>
                    <option value="email">Email</option>
                    <option value="phone">Phone</option>
                    <option value="url">URL</option>
                  </select>
                </div>
              </div>
              <div className="mt-6 flex gap-3 justify-end">
                <button
                  type="button"
                  onClick={() => {
                    setShowEditColumnModal(false);
                    setSelectedColumn(null);
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

      {/* Delete Column Modal */}
      {showDeleteColumnModal && selectedColumn && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-xl font-bold mb-4 text-red-600">Delete Column</h2>
            <p className="text-gray-700 mb-6">
              Are you sure you want to delete the column <strong>{selectedColumn.name}</strong>? 
              This will remove this column from all items and cannot be undone.
            </p>
            <div className="flex gap-3 justify-end">
              <button
                type="button"
                onClick={() => {
                  setShowDeleteColumnModal(false);
                  setSelectedColumn(null);
                }}
                className="rounded-md bg-gray-200 px-4 py-2 text-sm font-semibold text-gray-900 hover:bg-gray-300"
                disabled={submitting}
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteColumn}
                className="rounded-md bg-red-600 px-4 py-2 text-sm font-semibold text-white hover:bg-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
                disabled={submitting}
              >
                {submitting ? 'Deleting...' : 'Delete Column'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Edit Item Modal */}
      {showEditItemModal && selectedItem && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full max-h-[80vh] overflow-y-auto">
            <h2 className="text-xl font-bold mb-4">Edit Item</h2>
            <form onSubmit={handleEditItem}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Title (optional)
                  </label>
                  <input
                    type="text"
                    value={itemTitle}
                    onChange={(e) => setItemTitle(e.target.value)}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900"
                    placeholder="Item title"
                  />
                </div>
                {columns.map((col) => (
                  <div key={col.id}>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      {col.name}
                    </label>
                    <input
                      type={col.type === 'number' ? 'number' : col.type === 'date' ? 'date' : 'text'}
                      value={itemValues[col.key] || ''}
                      onChange={(e) => handleItemValueChange(col.key, e.target.value)}
                      className="w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900"
                      placeholder={`Enter ${col.name.toLowerCase()}`}
                    />
                  </div>
                ))}
              </div>
              <div className="mt-6 flex gap-3 justify-end">
                <button
                  type="button"
                  onClick={() => {
                    setShowEditItemModal(false);
                    setSelectedItem(null);
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

      {/* Delete Item Modal */}
      {showDeleteItemModal && selectedItem && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-xl font-bold mb-4 text-red-600">Delete Item</h2>
            <p className="text-gray-700 mb-6">
              Are you sure you want to delete this item{selectedItem.title ? ` "${selectedItem.title}"` : ''}? 
              This action cannot be undone.
            </p>
            <div className="flex gap-3 justify-end">
              <button
                type="button"
                onClick={() => {
                  setShowDeleteItemModal(false);
                  setSelectedItem(null);
                }}
                className="rounded-md bg-gray-200 px-4 py-2 text-sm font-semibold text-gray-900 hover:bg-gray-300"
                disabled={submitting}
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteItem}
                className="rounded-md bg-red-600 px-4 py-2 text-sm font-semibold text-white hover:bg-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
                disabled={submitting}
              >
                {submitting ? 'Deleting...' : 'Delete Item'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
