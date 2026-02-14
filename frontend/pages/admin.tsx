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
      <h2>Admin — Invite user</h2>
      <div style={{ maxWidth: 560 }}>
        <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} style={{ width: '100%', marginBottom: 8 }} />
        <select value={role} onChange={e => setRole(e.target.value)} style={{ marginBottom: 8 }}>
          <option value="viewer">Viewer</option>
          <option value="commenter">Commenter</option>
          <option value="editor">Editor</option>
          <option value="admin">Admin</option>
        </select>
        <div>
          <button onClick={invite}>Send invite</button>
        </div>
        {result && (
          <div style={{ marginTop: 12 }}>
            Invite token: <code>{result.token}</code>
            <div>Accept URL: <code>{result.accept_url}</code></div>
          </div>
        )}
      </div>
    </Layout>
  )
}
