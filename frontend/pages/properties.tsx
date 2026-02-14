import { useEffect, useState } from 'react'
import axios from 'axios'
import Link from 'next/link'
import Layout from '../components/Layout'
import ShareDialog from '../components/ShareDialog'
import OwnerHoverCard from '../components/OwnerHoverCard'

type Property = {
  id: string
  name: string
  type?: string
  address?: string
  unit_count?: number
  google_maps_url?: string
  website_social_media?: string
  owner_id?: string
  owner?: any
  source?: string
}

type Person = {
  id: string
  first_name: string
  last_name?: string
}

const PROPERTY_TYPES = [
  'Rental Room',
  'Apartment',
  'Rental House',
  'Other'
]

export default function PropertiesPage() {
  const [items, setItems] = useState<Property[]>([])
  const [people, setPeople] = useState<Person[]>([])
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({
    name: '',
    type: '',
    address: '',
    google_maps_url: '',
    website_social_media: '',
    owner_id: '',
    source: ''
  })
  const [sharing, setSharing] = useState<{ id: string | null, open: boolean }>({ id: null, open: false })

  const fetch = () => {
    axios.get(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/properties/`).then(r => setItems(r.data)).catch(() => setItems([]))
  }

  const fetchPeople = () => {
    axios.get(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/people/`).then(r => setPeople(r.data)).catch(() => setPeople([]))
  }

  useEffect(() => {
    fetch()
    fetchPeople()
  }, [])

  const create = async () => {
    await axios.post(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/properties/`, {
      name: form.name,
      type: form.type || null,
      address: form.address || null,
      google_maps_url: form.google_maps_url || null,
      website_social_media: form.website_social_media || null,
      owner_id: form.owner_id || null,
      source: form.source || null
    })
    setShowForm(false)
    setForm({
      name: '',
      type: '',
      address: '',
      google_maps_url: '',
      website_social_media: '',
      owner_id: '',
      source: ''
    })
    fetch()
  }

  const openGoogleMaps = (mapsUrl?: string) => {
    if (mapsUrl) {
      window.open(mapsUrl, '_blank')
    }
  }

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h2>Properties</h2>
          <div className="page-meta">Track buildings, locations, and unit counts.</div>
        </div>
        <div className="actions">
          <button onClick={() => setShowForm(s => !s)} className="btn btn-primary">New property</button>
          <button
            onClick={async () => {
              const name = prompt('Saved view name')
              if (!name) return
              await axios.post(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/saved-views/`, { name, resource_type: 'properties', filters: {}, columns: [] })
              alert('Saved view created')
            }}
            className="btn btn-outline"
          >
            Save view
          </button>
          <button onClick={() => window.location.href = '/map'} className="btn btn-ghost">Map view</button>
        </div>
      </div>

      {showForm && (
        <section className="card card-muted float-in">
          <div className="card-header">
            <h3>Add a property</h3>
          </div>
          <div className="form-grid">
            <div>
              <label>Property Name *</label>
              <input
                className="input"
                placeholder="e.g., Downtown Apartment Complex"
                value={form.name}
                onChange={e => setForm({ ...form, name: e.target.value })}
              />
            </div>
            <div>
              <label>Type</label>
              <select
                className="input"
                value={form.type}
                onChange={e => setForm({ ...form, type: e.target.value })}
              >
                <option value="">Select property type</option>
                {PROPERTY_TYPES.map(t => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </select>
            </div>
            <div>
              <label>Address</label>
              <input
                className="input"
                placeholder="e.g., 123 Main Street, City, Country"
                value={form.address}
                onChange={e => setForm({ ...form, address: e.target.value })}
              />
            </div>
            <div>
              <label>Google Maps Link</label>
              <input
                className="input"
                placeholder="https://maps.google.com/..."
                value={form.google_maps_url}
                onChange={e => setForm({ ...form, google_maps_url: e.target.value })}
              />
            </div>
            <div>
              <label>Website / Social Media</label>
              <input
                className="input"
                placeholder="https://website.com or https://instagram.com/..."
                value={form.website_social_media}
                onChange={e => setForm({ ...form, website_social_media: e.target.value })}
              />
            </div>
            <div>
              <label>Owner / Landlord</label>
              <select
                className="input"
                value={form.owner_id}
                onChange={e => setForm({ ...form, owner_id: e.target.value })}
              >
                <option value="">Select owner</option>
                {people.map(p => (
                  <option key={p.id} value={p.id}>
                    {p.first_name} {p.last_name || ''}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label>Source</label>
              <input
                className="input"
                placeholder="e.g., Friend referral, Online listing, Direct inquiry"
                value={form.source}
                onChange={e => setForm({ ...form, source: e.target.value })}
              />
            </div>
          </div>
          <div className="actions" style={{ marginTop: 16 }}>
            <button onClick={create} className="btn btn-primary">Create</button>
            <button onClick={() => setShowForm(false)} className="btn btn-ghost">Cancel</button>
          </div>
        </section>
      )}

      <section className="card">
        <div className="card-header">
          <h3>Portfolio</h3>
          <span className="chip">{items.length} properties</span>
        </div>
        <table className="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Address</th>
              <th>Owner</th>
              <th>Source</th>
              <th>Units</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {items.map(p => (
              <tr key={p.id}>
                <td data-label="Name"><Link href={`/properties/${p.id}`}>{p.name}</Link></td>
                <td data-label="Type">{p.type || '-'}</td>
                <td data-label="Address">
                  {p.address ? (
                    <span
                      onClick={() => openGoogleMaps(p.google_maps_url)}
                      style={{ cursor: p.google_maps_url ? 'pointer' : 'default', color: p.google_maps_url ? '#0070f3' : 'inherit', textDecoration: p.google_maps_url ? 'underline' : 'none' }}
                    >
                      {p.address}
                    </span>
                  ) : (
                    '-'
                  )}
                </td>
                <td data-label="Owner">
                  {p.owner ? <OwnerHoverCard owner={p.owner} /> : '-'}
                </td>
                <td data-label="Source">{p.source || '-'}</td>
                <td data-label="Units" className="align-center">{p.unit_count ?? 0}</td>
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
          <ShareDialog resourceType="property" resourceId={sharing.id} onClose={() => setSharing({ id: null, open: false })} onShared={fetch} />
        </div>
      )}

      <style jsx>{`
        label {
          display: block;
          margin-bottom: 6px;
          font-weight: 500;
          font-size: 14px;
          color: #333;
        }

        select.input {
          appearance: none;
          background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
          background-repeat: no-repeat;
          background-position: right 8px center;
          background-size: 20px;
          padding-right: 32px;
        }
      `}</style>
    </Layout>
  )
}

