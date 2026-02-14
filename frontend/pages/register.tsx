import { useState, useEffect } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'

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
      await axios.post(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/auth/register`, body)
      router.push('/login')
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Registration failed')
    }
  }

  return (
    <div style={{ padding: 24 }}>
      <h2>Register</h2>
      <form onSubmit={submit} style={{ maxWidth: 400 }}>
        <div style={{ marginBottom: 8 }}>
          <label>Name</label>
          <input value={name} onChange={e => setName(e.target.value)} style={{ width: '100%' }} />
        </div>
        <div style={{ marginBottom: 8 }}>
          <label>Email</label>
          <input value={email} onChange={e => setEmail(e.target.value)} style={{ width: '100%' }} />
        </div>
        <div style={{ marginBottom: 8 }}>
          <label>Password</label>
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} style={{ width: '100%' }} />
        </div>
        <button type="submit">Create account</button>
      </form>
      {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
    </div>
  )
}
