import Link from 'next/link'
import Layout from '../components/Layout'

export default function Home() {
  return (
    <Layout>
      <section className="hero float-in">
        <div className="hero-panel">
          <h1 className="hero-title">A calm command center for Zoneer.</h1>
          <p>
            Organize people, properties, and unit history in one place. Designed for property teams who need
            clarity, speed, and clean handoffs.
          </p>
          <div className="actions" style={{ marginTop: 16 }}>
            <Link href="/people" className="btn btn-primary">View people</Link>
            <Link href="/properties" className="btn btn-outline">Browse properties</Link>
          </div>
        </div>
        <div className="grid">
          <div className="stat-card">
            <div className="stat-title">Active contacts</div>
            <div className="stat-value">Centralized list</div>
          </div>
          <div className="stat-card">
            <div className="stat-title">Property ops</div>
            <div className="stat-value">Units + price history</div>
          </div>
          <div className="stat-card">
            <div className="stat-title">Sharing</div>
            <div className="stat-value">Controlled access</div>
          </div>
        </div>
      </section>

      <section className="card">
        <div className="card-header">
          <h3>Quick actions</h3>
          <span className="chip">Zoneer workspace</span>
        </div>
        <ul className="list">
          <li className="list-item">
            <div>
              <strong>Invite a teammate</strong>
              <div className="page-meta">Give secure access in seconds.</div>
            </div>
            <Link href="/admin" className="btn btn-ghost">Open admin</Link>
          </li>
          <li className="list-item">
            <div>
              <strong>Map view</strong>
              <div className="page-meta">See property locations in context.</div>
            </div>
            <Link href="/map" className="btn btn-ghost">Open map</Link>
          </li>
        </ul>
      </section>
    </Layout>
  )
}
