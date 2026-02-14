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
    <div className="card" style={{ width: 340 }}>
      <div className="card-header">
        <h3>Share {resourceType}</h3>
        <span className="chip">Invite access</span>
      </div>
      <div className="form-grid">
        <div>
          <label>Recipient email</label>
          <input className="input" value={email} onChange={e => setEmail(e.target.value)} />
        </div>
        <div>
          <label>Role</label>
          <select className="select" value={role} onChange={e => setRole(e.target.value)}>
            <option value="viewer">Viewer</option>
            <option value="commenter">Commenter</option>
            <option value="editor">Editor</option>
          </select>
        </div>
      </div>
      <div className="actions" style={{ marginTop: 12 }}>
        <button onClick={submit} className="btn btn-primary">Share</button>
        <button onClick={createLink} className="btn btn-outline">Copy link</button>
        <button onClick={onClose} className="btn btn-ghost">Cancel</button>
      </div>
      {error && <div style={{ color: 'var(--danger)', marginTop: 8 }}>{error}</div>}
    </div>
  )
}
