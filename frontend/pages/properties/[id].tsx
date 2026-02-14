import { useEffect, useState } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'
import Layout from '../../components/Layout'
import OwnerHoverCard from '../../components/OwnerHoverCard'

export default function PropertyDetail() {
  const router = useRouter()
  const { id } = router.query
  const [prop, setProp] = useState<any>(null)
  const [units, setUnits] = useState<any[]>([])
  const [unitForm, setUnitForm] = useState({ unit_no: '', monthly_rent: '' })
  const [selectedUnit, setSelectedUnit] = useState<any | null>(null)
  const [priceForm, setPriceForm] = useState({ price: '', currency: 'USD', effective_date: '' })
  const [history, setHistory] = useState<any[]>([])
  const [editMode, setEditMode] = useState(false)
  const [editForm, setEditForm] = useState<any>({})
  const [people, setPeople] = useState<any[]>([])

  const fetch = async () => {
    if (!id) return
    const p = await axios.get(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/properties/${id}`)
    setProp(p.data)
    // Initialize editForm with owner_id extracted from owner object
    setEditForm({
      ...p.data,
      owner_id: p.data.owner?.id || p.data.owner_id || ''
    })
    const u = await axios.get(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/units/?property_id=${id}`)
    setUnits(u.data)
  }

  const fetchPeople = () => {
    axios.get(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/people/`).then(r => setPeople(r.data)).catch(() => setPeople([]))
  }

  useEffect(() => {
    fetch()
    fetchPeople()
  }, [id])

  const createUnit = async () => {
    await axios.post(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/units/?property_id=${id}`, { unit_no: unitForm.unit_no, monthly_rent: parseFloat(unitForm.monthly_rent) })
    setUnitForm({ unit_no: '', monthly_rent: '' })
    fetch()
  }

  const openUnit = async (unit: any) => {
    setSelectedUnit(unit)
    const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/units/${unit.id}/history`)
    setHistory(res.data)
  }

  const addPriceHistory = async () => {
    if (!selectedUnit) return
    await axios.post(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/units/${selectedUnit.id}/history`, { price: parseFloat(priceForm.price), currency: priceForm.currency, effective_date: priceForm.effective_date || undefined })
    setPriceForm({ price: '', currency: 'USD', effective_date: '' })
    openUnit(selectedUnit)
  }

  const savePropertyDetails = async () => {
    await axios.patch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/properties/${id}`, {
      name: editForm.name,
      type: editForm.type || null,
      address: editForm.address || null,
      google_maps_url: editForm.google_maps_url || null,
      website_social_media: editForm.website_social_media || null,
      owner_id: (editForm.owner_id && editForm.owner_id !== '') ? editForm.owner_id : null,
      source: editForm.source || null,
      notes: editForm.notes || null
    })
    setEditMode(false)
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
          <h2>Property</h2>
          <div className="page-meta">Unit inventory and pricing history.</div>
        </div>
      </div>
      {prop && (
        <div>
          <section className="card">
            <div className="card-header">
              <div>
                <h3>{prop.name}</h3>
                <div className="page-meta">{prop.address || 'No address yet'}</div>
              </div>
              <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                <span className="chip">{units.length} units</span>
                <button onClick={() => setEditMode(!editMode)} className="btn btn-ghost">
                  {editMode ? 'Cancel' : 'Edit details'}
                </button>
              </div>
            </div>

            {!editMode ? (
              // View Mode
              <div className="property-details">
                <div className="detail-section">
                  <div className="detail-row">
                    <span className="detail-label">Type:</span>
                    <span className="detail-value">{prop.type || '-'}</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">Address:</span>
                    <span
                      className="detail-value"
                      onClick={() => openGoogleMaps(prop.google_maps_url)}
                      style={{
                        cursor: prop.google_maps_url ? 'pointer' : 'default',
                        color: prop.google_maps_url ? '#0070f3' : 'inherit',
                        textDecoration: prop.google_maps_url ? 'underline' : 'none'
                      }}
                    >
                      {prop.address || '-'}
                    </span>
                  </div>
                  {prop.google_maps_url && (
                    <div className="detail-row">
                      <span className="detail-label">Maps Link:</span>
                      <a href={prop.google_maps_url} target="_blank" rel="noopener noreferrer" className="detail-value">
                        View on Google Maps
                      </a>
                    </div>
                  )}
                  {prop.website_social_media && (
                    <div className="detail-row">
                      <span className="detail-label">Website/Social:</span>
                      <a href={prop.website_social_media} target="_blank" rel="noopener noreferrer" className="detail-value">
                        {prop.website_social_media}
                      </a>
                    </div>
                  )}
                  {prop.owner && (
                    <div className="detail-row">
                      <span className="detail-label">Owner:</span>
                      <span className="detail-value">
                        <OwnerHoverCard owner={prop.owner} />
                      </span>
                    </div>
                  )}
                  {prop.source && (
                    <div className="detail-row">
                      <span className="detail-label">Source:</span>
                      <span className="detail-value">{prop.source}</span>
                    </div>
                  )}
                  {prop.notes && (
                    <div className="detail-row">
                      <span className="detail-label">Notes:</span>
                      <span className="detail-value">{prop.notes}</span>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              // Edit Mode
              <div style={{ padding: '16px' }}>
                <div className="form-grid">
                  <div>
                    <label>Property Name</label>
                    <input
                      className="input"
                      value={editForm.name}
                      onChange={e => setEditForm({ ...editForm, name: e.target.value })}
                    />
                  </div>
                  <div>
                    <label>Type</label>
                    <select
                      className="input"
                      value={editForm.type || ''}
                      onChange={e => setEditForm({ ...editForm, type: e.target.value })}
                    >
                      <option value="">Select property type</option>
                      <option value="Rental Room">Rental Room</option>
                      <option value="Apartment">Apartment</option>
                      <option value="Rental House">Rental House</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                  <div>
                    <label>Address</label>
                    <input
                      className="input"
                      value={editForm.address || ''}
                      onChange={e => setEditForm({ ...editForm, address: e.target.value })}
                    />
                  </div>
                  <div>
                    <label>Google Maps Link</label>
                    <input
                      className="input"
                      value={editForm.google_maps_url || ''}
                      onChange={e => setEditForm({ ...editForm, google_maps_url: e.target.value })}
                      placeholder="https://maps.google.com/..."
                    />
                  </div>
                  <div>
                    <label>Website / Social Media</label>
                    <input
                      className="input"
                      value={editForm.website_social_media || ''}
                      onChange={e => setEditForm({ ...editForm, website_social_media: e.target.value })}
                      placeholder="https://website.com or https://instagram.com/..."
                    />
                  </div>
                  <div>
                    <label>Owner / Landlord</label>
                    <select
                      className="input"
                      value={editForm.owner_id || ''}
                      onChange={e => setEditForm({ ...editForm, owner_id: e.target.value })}
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
                      value={editForm.source || ''}
                      onChange={e => setEditForm({ ...editForm, source: e.target.value })}
                      placeholder="e.g., Friend referral, Online listing, Direct inquiry"
                    />
                  </div>
                  <div style={{ gridColumn: '1 / -1' }}>
                    <label>Notes</label>
                    <textarea
                      className="input"
                      value={editForm.notes || ''}
                      onChange={e => setEditForm({ ...editForm, notes: e.target.value })}
                      placeholder="Any additional notes..."
                      rows={4}
                    />
                  </div>
                </div>
                <div className="actions" style={{ marginTop: 16 }}>
                  <button onClick={savePropertyDetails} className="btn btn-primary">Save changes</button>
                  <button onClick={() => setEditMode(false)} className="btn btn-ghost">Cancel</button>
                </div>
              </div>
            )}
          </section>

          <section className="card card-muted" style={{ marginTop: 16, marginBottom: 16 }}>
            <div className="section-title">Add a unit</div>
            <div className="form-grid">
              <input className="input" placeholder="Unit no" value={unitForm.unit_no} onChange={e => setUnitForm({ ...unitForm, unit_no: e.target.value })} />
              <input className="input" placeholder="Monthly rent" value={unitForm.monthly_rent} onChange={e => setUnitForm({ ...unitForm, monthly_rent: e.target.value })} />
            </div>
            <div className="actions" style={{ marginTop: 12 }}>
              <button onClick={createUnit} className="btn btn-primary">Add unit</button>
            </div>
          </section>

          <table className="table">
            <thead>
              <tr><th>Unit</th><th>Rent</th><th>Status</th><th></th></tr>
            </thead>
            <tbody>
              {units.map(u => (
                <tr key={u.id}>
                  <td data-label="Unit">{u.unit_no}</td>
                  <td data-label="Rent">{u.monthly_rent}</td>
                  <td data-label="Status">{u.status}</td>
                  <td data-label="Actions" className="align-right">
                    <button onClick={() => openUnit(u)} className="btn btn-ghost">View history</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {selectedUnit && (
            <section className="card" style={{ marginTop: 16 }}>
              <div className="card-header">
                <div>
                  <h4>Unit {selectedUnit.unit_no} price history</h4>
                  <div className="page-meta">Log rent changes over time.</div>
                </div>
              </div>
              <div className="form-grid">
                <input className="input" placeholder="Price" value={priceForm.price} onChange={e => setPriceForm({ ...priceForm, price: e.target.value })} />
                <input className="input" placeholder="Effective date (YYYY-MM-DD)" value={priceForm.effective_date} onChange={e => setPriceForm({ ...priceForm, effective_date: e.target.value })} />
              </div>
              <div className="actions" style={{ marginTop: 12 }}>
                <button onClick={addPriceHistory} className="btn btn-primary">Add price</button>
              </div>
              <table className="table" style={{ marginTop: 16 }}>
                <thead><tr><th>Price</th><th>Currency</th><th>Effective</th></tr></thead>
                <tbody>
                  {history.map(h => (
                    <tr key={h.id}>
                      <td data-label="Price">{h.price}</td>
                      <td data-label="Currency">{h.currency}</td>
                      <td data-label="Effective">{h.effective_date}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>
          )}

          <style jsx>{`
            .property-details {
              padding: 16px;
            }

            .detail-section {
              display: grid;
              gap: 16px;
            }

            .detail-row {
              display: flex;
              gap: 16px;
              padding: 12px 0;
              border-bottom: 1px solid #eee;
            }

            .detail-row:last-child {
              border-bottom: none;
            }

            .detail-label {
              font-weight: 600;
              min-width: 120px;
              color: #666;
            }

            .detail-value {
              flex: 1;
              color: #333;
            }

            .detail-value a {
              color: #0070f3;
              text-decoration: none;
            }

            .detail-value a:hover {
              text-decoration: underline;
            }

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

            textarea.input {
              font-family: inherit;
              resize: vertical;
            }
          `}</style>
        </div>
      )}
    </Layout>
  )
}
