import { supabase } from './supabase';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

async function getAuthToken(): Promise<string | null> {
  const { data: { session } } = await supabase.auth.getSession();
  return session?.access_token || null;
}

async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const token = await getAuthToken();
  
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
    ...options.headers,
  };

  const response = await fetch(`${API_URL}${url}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(error.detail || 'Request failed');
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

// Workspace API
export const workspaceApi = {
  create: (data: { name: string; description?: string }) => 
    fetchWithAuth('/workspaces', { method: 'POST', body: JSON.stringify(data) }),
  
  list: () => 
    fetchWithAuth('/workspaces'),
  
  get: (id: string) => 
    fetchWithAuth(`/workspaces/${id}`),
  
  update: (id: string, data: { name?: string; description?: string }) => 
    fetchWithAuth(`/workspaces/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  
  delete: (id: string) => 
    fetchWithAuth(`/workspaces/${id}`, { method: 'DELETE' }),
  
  invite: (workspaceId: string, data: { email: string; role: string }) =>
    fetchWithAuth(`/workspaces/${workspaceId}/invite`, { method: 'POST', body: JSON.stringify(data) }),
  
  members: (workspaceId: string) =>
    fetchWithAuth(`/workspaces/${workspaceId}/members`),
  
  updateRole: (workspaceId: string, memberId: string, role: string) =>
    fetchWithAuth(`/workspaces/${workspaceId}/members/${memberId}/role`, {
      method: 'PATCH',
      body: JSON.stringify({ role })
    }),
  
  removeMember: (workspaceId: string, memberId: string) =>
    fetchWithAuth(`/workspaces/${workspaceId}/members/${memberId}`, { method: 'DELETE' }),
};

// List API
export const listApi = {
  create: (workspaceId: string, data: { name: string; description?: string }) =>
    fetchWithAuth(`/workspaces/${workspaceId}/lists`, { method: 'POST', body: JSON.stringify(data) }),
  
  list: (workspaceId: string) =>
    fetchWithAuth(`/workspaces/${workspaceId}/lists`),
  
  get: (listId: string) =>
    fetchWithAuth(`/lists/${listId}`),
  
  update: (listId: string, data: { name?: string; description?: string }) =>
    fetchWithAuth(`/lists/${listId}`, { method: 'PATCH', body: JSON.stringify(data) }),
  
  delete: (listId: string) =>
    fetchWithAuth(`/lists/${listId}`, { method: 'DELETE' }),
};

// Column API
export const columnApi = {
  create: (listId: string, data: Record<string, unknown>) =>
    fetchWithAuth(`/lists/${listId}/columns`, { method: 'POST', body: JSON.stringify(data) }),
  
  list: (listId: string) =>
    fetchWithAuth(`/lists/${listId}/columns`),
  
  update: (columnId: string, data: Record<string, unknown>) =>
    fetchWithAuth(`/columns/${columnId}`, { method: 'PATCH', body: JSON.stringify(data) }),
  
  delete: (columnId: string) =>
    fetchWithAuth(`/columns/${columnId}`, { method: 'DELETE' }),
};

// Item API
export const itemApi = {
  create: (listId: string, data: { title?: string; values?: Record<string, unknown> }) =>
    fetchWithAuth(`/lists/${listId}/items`, { method: 'POST', body: JSON.stringify(data) }),
  
  list: (listId: string, limit = 100, offset = 0) =>
    fetchWithAuth(`/lists/${listId}/items?limit=${limit}&offset=${offset}`),
  
  get: (itemId: string) =>
    fetchWithAuth(`/items/${itemId}`),
  
  update: (itemId: string, data: { title?: string; values?: Record<string, unknown> }) =>
    fetchWithAuth(`/items/${itemId}`, { method: 'PATCH', body: JSON.stringify(data) }),
  
  delete: (itemId: string) =>
    fetchWithAuth(`/items/${itemId}`, { method: 'DELETE' }),
};

// Comment API
export const commentApi = {
  create: (itemId: string, content: string) =>
    fetchWithAuth(`/items/${itemId}/comments`, { 
      method: 'POST', 
      body: JSON.stringify({ content }) 
    }),
  
  list: (itemId: string) =>
    fetchWithAuth(`/items/${itemId}/comments`),
  
  delete: (commentId: string) =>
    fetchWithAuth(`/comments/${commentId}`, { method: 'DELETE' }),
};

// Relationship API
export const relationshipApi = {
  create: (listId: string, data: { name: string; target_list_id: string; relationship_type: string }) =>
    fetchWithAuth(`/lists/${listId}/relationships`, { method: 'POST', body: JSON.stringify(data) }),
  
  list: (listId: string) =>
    fetchWithAuth(`/lists/${listId}/relationships`),
  
  delete: (relationshipId: string) =>
    fetchWithAuth(`/relationships/${relationshipId}`, { method: 'DELETE' }),
  
  createLink: (relationshipId: string, data: { source_item_id: string; target_item_id: string }) =>
    fetchWithAuth(`/relationships/${relationshipId}/links`, { method: 'POST', body: JSON.stringify(data) }),
  
  listLinks: (relationshipId: string) =>
    fetchWithAuth(`/relationships/${relationshipId}/links`),
  
  deleteLink: (linkId: string) =>
    fetchWithAuth(`/links/${linkId}`, { method: 'DELETE' }),
};

// Audit API
export const auditApi = {
  list: (workspaceId: string, limit = 100, offset = 0) =>
    fetchWithAuth(`/workspaces/${workspaceId}/audit?limit=${limit}&offset=${offset}`),
};
