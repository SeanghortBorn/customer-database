import React, { useState } from 'react'
import axios from 'axios'

export default function ShareDialog({ resourceType, resourceId, onClose, onShared }: { resourceType: string, resourceId: string, onClose: () => void, onShared: () => void }) {
  const [email, setEmail] = useState('')
  const [role, setRole] = useState('viewer')
  const [error, setError] = useState('')

  const submit = async () => {
    try {
      await axios.post(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/shares/`, { resource_type: resourceType, resource_id: resourceId, grantee_email: email, role })
      onShared()
      onClose()
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Share failed')
    }
  }

  const createLink = async () => {
    try {
      const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/shares/link?resource_type=${resourceType}&resource_id=${resourceId}&role=${role}`)
      const url = `${window.location.origin}${res.data.url}`
      await navigator.clipboard.writeText(url)
      onShared()
      onClose()
      alert('Link copied to clipboard: ' + url)
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Create link failed')
    }
  }

  return (
    <div style={{ background: '#fff', border: '1px solid #ddd', padding: 12, width: 320 }}>
      <h3>Share {resourceType}</h3>
      <div style={{ marginBottom: 8 }}>
        <label>Recipient email</label>
        <input value={email} onChange={e => setEmail(e.target.value)} style={{ width: '100%' }} />
      </div>
      <div style={{ marginBottom: 8 }}>
        <label>Role</label>
        <select value={role} onChange={e => setRole(e.target.value)}>
          <option value="viewer">Viewer</option>
          <option value="commenter">Commenter</option>
          <option value="editor">Editor</option>
        </select>
      </div>
      <div style={{ display: 'flex', gap: 8 }}>
        <button onClick={submit}>Share</button>
        <button onClick={onClose}>Cancel</button>
      </div>
      {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
    </div>
  )
}
