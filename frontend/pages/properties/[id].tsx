import { useEffect, useState } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'
import Layout from '../../components/Layout'

export default function PropertyDetail() {
  const router = useRouter()
  const { id } = router.query
  const [prop, setProp] = useState<any>(null)
  const [units, setUnits] = useState<any[]>([])
  const [unitForm, setUnitForm] = useState({ unit_no: '', monthly_rent: '' })
  const [selectedUnit, setSelectedUnit] = useState<any | null>(null)
  const [priceForm, setPriceForm] = useState({ price: '', currency: 'USD', effective_date: '' })
  const [history, setHistory] = useState<any[]>([])

  const fetch = async () => {
    if (!id) return
    const p = await axios.get(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/properties/${id}`)
    setProp(p.data)
    const u = await axios.get(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/units/?property_id=${id}`)
    setUnits(u.data)
  }

  useEffect(() => { fetch() }, [id])

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

  return (
    <Layout>
      <h2>Property</h2>
      {prop && (
        <div>
          <h3>{prop.name}</h3>
          <div>{prop.address}</div>
          <h4 style={{ marginTop: 12 }}>Units</h4>
          <div style={{ marginBottom: 8 }}>
            <input placeholder="Unit no" value={unitForm.unit_no} onChange={e => setUnitForm({ ...unitForm, unit_no: e.target.value })} />
            <input placeholder="Monthly rent" value={unitForm.monthly_rent} onChange={e => setUnitForm({ ...unitForm, monthly_rent: e.target.value })} />
            <button onClick={createUnit}>Add unit</button>
          </div>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr><th>Unit</th><th>Rent</th><th>Status</th><th></th></tr>
            </thead>
            <tbody>
              {units.map(u => (
                <tr key={u.id}>
                  <td>{u.unit_no}</td>
                  <td>{u.monthly_rent}</td>
                  <td>{u.status}</td>
                  <td><button onClick={() => openUnit(u)}>View / History</button></td>
                </tr>
              ))}
            </tbody>
          </table>

          {selectedUnit && (
            <div style={{ marginTop: 16, padding: 12, border: '1px solid #e5e7eb', background: '#fff' }}>
              <h4>Unit {selectedUnit.unit_no} — Price history</h4>
              <div style={{ marginBottom: 8 }}>
                <input placeholder="Price" value={priceForm.price} onChange={e => setPriceForm({ ...priceForm, price: e.target.value })} />
                <input placeholder="Effective date (YYYY-MM-DD)" value={priceForm.effective_date} onChange={e => setPriceForm({ ...priceForm, effective_date: e.target.value })} />
                <button onClick={addPriceHistory}>Add price</button>
              </div>
              <table style={{ width: '100%' }}>
                <thead><tr><th>Price</th><th>Currency</th><th>Effective</th></tr></thead>
                <tbody>
                  {history.map(h => (
                    <tr key={h.id}><td>{h.price}</td><td>{h.currency}</td><td>{h.effective_date}</td></tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </Layout>
  )
}
