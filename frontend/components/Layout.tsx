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
    <div className="app-shell">
      <header className="topbar">
        <div className="topbar-inner">
          <div className="brand">
            <Link href="/" className="brand-title">
              Zoneer
            </Link>
            <span className="brand-subtitle">Property ops and customer care</span>
          </div>
          <nav className="nav-links">
            <Link href="/people" className="nav-link">People</Link>
            <Link href="/properties" className="nav-link">Properties</Link>
            <Link href="/map" className="nav-link">Map</Link>
            <input
              className="search-input"
              placeholder="Search people or properties"
              onKeyDown={async (e) => {
                if (e.key === 'Enter') {
                  const q = (e.target as HTMLInputElement).value
                  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/search/?q=${encodeURIComponent(q)}`)
                  const data = await res.json()
                  alert(JSON.stringify(data, null, 2))
                }
              }}
            />
            {!isAuthenticated ? (
              <>
                <Link href="/login" className="nav-link">Sign in</Link>
                <Link href="/register" className="nav-link">Register</Link>
              </>
            ) : (
              <>
                <Link href="/admin" className="nav-link">Admin</Link>
                <button onClick={logout} className="btn btn-outline">Sign out</button>
              </>
            )}
          </nav>
        </div>
      </header>

      {notification && (
        <div className="toast">{notification}</div>
      )}

      <main className="content-shell">{children}</main>
    </div>
  )
}
