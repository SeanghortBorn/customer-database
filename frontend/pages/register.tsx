import { useState, useEffect } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'
import Link from 'next/link'

export default function RegisterPage() {
  const [email, setEmail] = useState('')
  const [name, setName] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const router = useRouter()

  // prefill from invite link (if present)
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search)
      const e = params.get('email')
      const token = params.get('token') || params.get('invite_token')
      if (e) setEmail(e)
      if (token) {
        // keep token in query so submit reads it; optionally show a message
      }
    }
  }, [])

  const submit = async (e: any) => {
    e.preventDefault()
    try {
      const body: any = { email, name, password }
      const params = new URLSearchParams(window.location.search)
      const inviteToken = params.get('invite_token')
      if (inviteToken) body.invite_token = inviteToken
      const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/auth/register`, body)
      // Save the access token and redirect to home
      if (res.data.access_token) {
        localStorage.setItem('auth_token', res.data.access_token)
        axios.defaults.headers.common['Authorization'] = `Bearer ${res.data.access_token}`
        router.push('/')
      } else {
        // Fallback if token not returned (legacy behavior)
        router.push('/login')
      }
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Registration failed')
    }
  }

  return (
    <div className="auth-shell">
      <div className="auth-card float-in">
        <div style={{ marginBottom: 16 }}>
          <Link href="/" className="brand-title">
            Zoneer
          </Link>
          <div className="page-meta">Create your account and join the workspace.</div>
        </div>
        <form onSubmit={submit}>
          <div className="form-grid">
            <div>
              <label>Name</label>
              <input className="input" value={name} onChange={e => setName(e.target.value)} />
            </div>
            <div>
              <label>Email</label>
              <input className="input" value={email} onChange={e => setEmail(e.target.value)} />
            </div>
            <div>
              <label>Password</label>
              <input className="input" type="password" value={password} onChange={e => setPassword(e.target.value)} />
            </div>
          </div>
          <div className="actions" style={{ marginTop: 16 }}>
            <button type="submit" className="btn btn-primary">Create account</button>
            <Link href="/login" className="btn btn-ghost">Back to sign in</Link>
          </div>
        </form>
        {error && <div style={{ color: 'var(--danger)', marginTop: 8 }}>{error}</div>}
      </div>
    </div>
  )
}
