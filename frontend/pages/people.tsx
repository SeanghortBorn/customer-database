import { useEffect, useState } from 'react'
import axios from 'axios'
import Layout from '../components/Layout'
import ShareDialog from '../components/ShareDialog'

type Person = {
  id: string
  first_name: string
  last_name?: string
  phone?: string
  email?: string
}

export default function PeoplePage() {
  const [people, setPeople] = useState<Person[]>([])
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ first_name: '', last_name: '', phone: '', email: '', title: '' })
  const [sharing, setSharing] = useState<{ id: string | null, open: boolean }>({ id: null, open: false })

  const fetch = () => {
    axios.get(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/people/`).then(r => setPeople(r.data)).catch(() => setPeople([]))
  }

  useEffect(() => { fetch() }, [])

  const create = async () => {
    await axios.post(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/people/`, form)
    setShowForm(false)
    setForm({ first_name: '', last_name: '', phone: '', email: '', title: '' })
    fetch()
  }

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h2>People</h2>
          <div className="page-meta">Manage your customer records and access.</div>
        </div>
        <div className="actions">
          <button onClick={() => setShowForm(s => !s)} className="btn btn-primary">New person</button>
          <button
            onClick={async () => {
              const name = prompt('Saved view name')
              if (!name) return
              await axios.post(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/saved-views/`, { name, resource_type: 'people', filters: {}, columns: [] })
              alert('Saved view created')
            }}
            className="btn btn-outline"
          >
            Save view
          </button>
        </div>
      </div>

      {showForm && (
        <section className="card card-muted float-in">
          <div className="card-header">
            <h3>Add a new person</h3>
          </div>
          <div className="form-grid">
            <input className="input" placeholder="First name" value={form.first_name} onChange={e => setForm({ ...form, first_name: e.target.value })} />
            <input className="input" placeholder="Last name" value={form.last_name} onChange={e => setForm({ ...form, last_name: e.target.value })} />
            <input className="input" placeholder="Phone" value={form.phone} onChange={e => setForm({ ...form, phone: e.target.value })} />
            <input className="input" placeholder="Email" value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} />
          </div>
          <div className="actions" style={{ marginTop: 16 }}>
            <button onClick={create} className="btn btn-primary">Create</button>
            <button onClick={() => setShowForm(false)} className="btn btn-ghost">Cancel</button>
          </div>
        </section>
      )}

      <section className="card">
        <div className="card-header">
          <h3>Directory</h3>
          <span className="chip">{people.length} records</span>
        </div>
        <table className="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Phone</th>
              <th>Email</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {people.map(p => (
              <tr key={p.id}>
                <td data-label="Name">{p.first_name} {p.last_name}</td>
                <td data-label="Phone">{p.phone || '-'}</td>
                <td data-label="Email">{p.email || '-'}</td>
                <td data-label="Actions" className="align-right">
                  <button onClick={() => setSharing({ id: p.id, open: true })} className="btn btn-ghost">Share</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      {sharing.open && sharing.id && (
        <div style={{ position: 'fixed', right: 24, top: 110 }}>
          <ShareDialog resourceType="person" resourceId={sharing.id} onClose={() => setSharing({ id: null, open: false })} onShared={fetch} />
        </div>
      )}
    </Layout>
  )
}
