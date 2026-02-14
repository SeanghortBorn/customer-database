import Link from 'next/link'
import { useEffect, useState } from 'react'

export default function Layout({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  const [notification, setNotification] = useState<string | null>(null)

  useEffect(() => {
    setIsAuthenticated(!!(typeof window !== 'undefined' && localStorage.getItem('auth_token')))

    // websocket for realtime notifications (MVP)
    if (typeof window !== 'undefined') {
      let wsUrl = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}`.replace(/^http/, 'ws') + '/ws'
      try {
        const ws = new WebSocket(wsUrl)
        ws.onmessage = (ev) => {
          try {
            const msg = JSON.parse(ev.data)
            setNotification(`${msg.event}: ${JSON.stringify(msg.payload)}`)
            setTimeout(() => setNotification(null), 4000)
          } catch (e) {
            console.log('ws msg', ev.data)
          }
        }
        ws.onopen = () => console.log('ws connected')
        ws.onclose = () => console.log('ws closed')
      } catch (e) {
        console.log('ws error', e)
      }
    }
  }, [])

  const logout = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token')
      window.location.href = '/'
    }
  }

  return (
    <div style={{ maxWidth: 1000, margin: '24px auto', padding: 16 }}>
      <header style={{ marginBottom: 20 }}>
        <h1><Link href="/">Zoneer</Link></h1>
        <nav style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <Link href="/people" style={{ marginRight: 12 }}>People</Link>
          <Link href="/properties" style={{ marginRight: 12 }}>Properties</Link>
          <input placeholder="Search people / properties" style={{ padding: '4px 8px', borderRadius: 6, border: '1px solid #ddd' }} onKeyDown={async (e) => {
            if (e.key === 'Enter') {
              const q = (e.target as HTMLInputElement).value
              const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/search/?q=${encodeURIComponent(q)}`)
              const data = await res.json()
              alert(JSON.stringify(data, null, 2))
            }
          }} />
          {!isAuthenticated ? (
            <>
              <Link href="/login" style={{ marginRight: 8 }}>Sign in</Link>
              <Link href="/register">Register</Link>
            </>
          ) : (
            <>
              <Link href="/admin" style={{ marginRight: 12 }}>Admin</Link>
              <button onClick={logout}>Sign out</button>
            </>
          )}
        </nav>
      </header>

      {notification && (
        <div style={{ position: 'fixed', right: 20, top: 20, background: '#111827', color: '#fff', padding: '8px 12px', borderRadius: 6 }}>{notification}</div>
      )}

      <main>{children}</main>
    </div>
  )
}
