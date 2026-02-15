'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { listApi, columnApi, itemApi } from '@/lib/api';
import { supabase } from '@/lib/supabase';

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
  const [showItemModal, setShowItemModal] = useState(false);
  const [error, setError] = useState('');

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
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) {
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
    setError('');

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
    }
  };

  const handleCreateItem = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

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
    }
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
                        {col.name}
                        <span className="ml-1 text-gray-400">({col.type})</span>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {items.length === 0 ? (
                    <tr>
                      <td
                        colSpan={columns.length + 1}
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
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="rounded-md bg-green-600 px-4 py-2 text-sm font-semibold text-white hover:bg-green-500"
                >
                  Add Column
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
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-500"
                >
                  Add Item
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
