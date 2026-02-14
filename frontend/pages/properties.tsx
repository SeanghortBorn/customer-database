import { useEffect, useState } from 'react'
import axios from 'axios'
import Layout from '../components/Layout'
import ShareDialog from '../components/ShareDialog'

type Property = {
  id: string
  name: string
  type?: string
  address?: string
  unit_count?: number
}

export default function PropertiesPage() {
  const [items, setItems] = useState<Property[]>([])
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ name: '', type: '', address: '' })
  const [sharing, setSharing] = useState<{ id: string | null, open: boolean }>({ id: null, open: false })

  const fetch = () => {
    axios.get(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/properties/`).then(r => setItems(r.data)).catch(() => setItems([]))
  }

  useEffect(() => { fetch() }, [])

  const create = async () => {
    await axios.post(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/properties/`, form)
    setShowForm(false)
    setForm({ name: '', type: '', address: '' })
    fetch()
  }

  return (
    <Layout>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Properties</h2>
        <div>
          <button onClick={() => setShowForm(s => !s)} style={{ marginRight: 8 }}>New Property</button>
        </div>
      </div>

      {showForm && (
        <div style={{ marginBottom: 12, maxWidth: 600 }}>
          <input placeholder="Name" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} />
          <input placeholder="Type" value={form.type} onChange={e => setForm({ ...form, type: e.target.value })} />
          <input placeholder="Address" value={form.address} onChange={e => setForm({ ...form, address: e.target.value })} />
          <div style={{ marginTop: 8 }}>
            <button onClick={create}>Create</button>
            <button onClick={() => setShowForm(false)} style={{ marginLeft: 8 }}>Cancel</button>
          </div>
        </div>
      )}

      <div style={{ marginBottom: 12 }}>
        <button onClick={async () => { const name = prompt('Saved view name'); if (!name) return; await axios.post(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/saved-views/`, { name, resource_type: 'properties', filters: {}, columns: [] }); alert('Saved view created') }}>Save current view</button>
        <button onClick={() => window.location.href = '/map'} style={{ marginLeft: 8 }}>Map view</button>
      </div>

      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Address</th>
            <th>Units</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {items.map(p => (
            <tr key={p.id}>
              <td><a href={`/properties/${p.id}`}>{p.name}</a></td>
              <td>{p.type}</td>
              <td>{p.address}</td>
              <td style={{ textAlign: 'center' }}>{p.unit_count ?? 0}</td>
              <td style={{ textAlign: 'right' }}>
                <button onClick={() => setSharing({ id: p.id, open: true })}>Share</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {sharing.open && sharing.id && (
        <div style={{ position: 'fixed', right: 24, top: 80 }}>
          <ShareDialog resourceType="property" resourceId={sharing.id} onClose={() => setSharing({ id: null, open: false })} onShared={fetch} />
        </div>
      )}
    </Layout>
  )
}
