import { useState } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'
import Link from 'next/link'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const router = useRouter()

  const submit = async (e: any) => {
    e.preventDefault()
    try {
      const data = new URLSearchParams()
      data.append('username', email)
      data.append('password', password)
      const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/auth/token`, data, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })
      localStorage.setItem('auth_token', res.data.access_token)
      axios.defaults.headers.common['Authorization'] = `Bearer ${res.data.access_token}`
      router.push('/')
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Login failed')
    }
  }

  const oauth = (provider: string) => {
    window.location.href = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/auth/login/${provider}`
  }

  return (
    <div className="auth-shell">
      <div className="auth-card float-in">
        <div style={{ marginBottom: 16 }}>
          <Link href="/" className="brand-title">
            Zoneer
          </Link>
          <div className="page-meta">Welcome back. Sign in to continue.</div>
        </div>
        <div className="actions" style={{ marginBottom: 16 }}>
          <button onClick={() => oauth('google')} className="btn btn-outline">Sign in with Google</button>
          <button onClick={() => oauth('microsoft')} className="btn btn-outline">Sign in with Microsoft</button>
        </div>
        <form onSubmit={submit}>
          <div className="form-grid">
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
            <button type="submit" className="btn btn-primary">Sign in</button>
            <Link href="/register" className="btn btn-ghost">Create account</Link>
          </div>
        </form>
        {error && <div style={{ color: 'var(--danger)', marginTop: 8 }}>{error}</div>}
      </div>
    </div>
  )
}
