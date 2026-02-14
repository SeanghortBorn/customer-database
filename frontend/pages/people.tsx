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
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>People</h2>
        <div>
          <button onClick={() => setShowForm(s => !s)} style={{ marginRight: 8 }}>New Person</button>
        </div>
      </div>

      <div style={{ marginBottom: 12 }}>
        <button onClick={async () => { const name = prompt('Saved view name'); if (!name) return; await axios.post(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/saved-views/`, { name, resource_type: 'people', filters: {}, columns: [] }); alert('Saved view created') }}>Save current view</button>
      </div>

      {showForm && (
        <div style={{ marginBottom: 12, maxWidth: 600 }}>
          <input placeholder="First name" value={form.first_name} onChange={e => setForm({ ...form, first_name: e.target.value })} />
          <input placeholder="Last name" value={form.last_name} onChange={e => setForm({ ...form, last_name: e.target.value })} />
          <input placeholder="Phone" value={form.phone} onChange={e => setForm({ ...form, phone: e.target.value })} />
          <input placeholder="Email" value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} />
          <div style={{ marginTop: 8 }}>
            <button onClick={create}>Create</button>
            <button onClick={() => setShowForm(false)} style={{ marginLeft: 8 }}>Cancel</button>
          </div>
        </div>
      )}

      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
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
              <td>{p.first_name} {p.last_name}</td>
              <td>{p.phone}</td>
              <td>{p.email}</td>
              <td style={{ textAlign: 'right' }}>
                <button onClick={() => setSharing({ id: p.id, open: true })}>Share</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {sharing.open && sharing.id && (
        <div style={{ position: 'fixed', right: 24, top: 80 }}>
          <ShareDialog resourceType="person" resourceId={sharing.id} onClose={() => setSharing({ id: null, open: false })} onShared={fetch} />
        </div>
      )}
    </Layout>
  )
}
