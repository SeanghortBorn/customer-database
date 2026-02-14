import { useState } from 'react'
import axios from 'axios'
import Layout from '../components/Layout'

export default function AdminPage() {
  const [email, setEmail] = useState('')
  const [role, setRole] = useState('editor')
  const [result, setResult] = useState<any>(null)

  const invite = async () => {
    const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/invites/`, { email, role })
    setResult(res.data)
  }

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h2>Admin</h2>
          <div className="page-meta">Invite teammates and control access.</div>
        </div>
      </div>
      <section className="card">
        <div className="card-header">
          <h3>Invite a user</h3>
          <span className="chip">Role-based access</span>
        </div>
        <div className="form-grid">
          <input className="input" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
          <select className="select" value={role} onChange={e => setRole(e.target.value)}>
            <option value="viewer">Viewer</option>
            <option value="commenter">Commenter</option>
            <option value="editor">Editor</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        <div className="actions" style={{ marginTop: 16 }}>
          <button onClick={invite} className="btn btn-primary">Send invite</button>
        </div>
        {result && (
          <div className="card card-muted" style={{ marginTop: 16 }}>
            <div className="page-meta">Invite token</div>
            <div><strong>{result.token}</strong></div>
            <div className="page-meta" style={{ marginTop: 8 }}>Accept URL</div>
            <div style={{ wordBreak: 'break-all' }}>{result.accept_url}</div>
          </div>
        )}
      </section>
    </Layout>
  )
}
