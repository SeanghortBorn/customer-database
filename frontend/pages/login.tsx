import { useState } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'

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
    <div style={{ padding: 24 }}>
      <h2>Sign in</h2>
      <div style={{ marginBottom: 12 }}>
        <button onClick={() => oauth('google')} style={{ marginRight: 8 }}>Sign in with Google</button>
        <button onClick={() => oauth('microsoft')}>Sign in with Microsoft</button>
      </div>
      <form onSubmit={submit} style={{ maxWidth: 400 }}>
        <div style={{ marginBottom: 8 }}>
          <label>Email</label>
          <input value={email} onChange={e => setEmail(e.target.value)} style={{ width: '100%' }} />
        </div>
        <div style={{ marginBottom: 8 }}>
          <label>Password</label>
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} style={{ width: '100%' }} />
        </div>
        <button type="submit">Sign in</button>
      </form>
      {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
    </div>
  )
}
