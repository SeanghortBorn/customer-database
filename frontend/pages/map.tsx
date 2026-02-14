import { useEffect, useState } from 'react'
import axios from 'axios'
import Layout from '../components/Layout'

export default function MapPage() {
  const [props, setProps] = useState<any[]>([])

  useEffect(() => {
    axios.get(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/properties/`).then(r => setProps(r.data)).catch(() => setProps([]))
  }, [])

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h2>Map view</h2>
          <div className="page-meta">Jump to property locations in Google Maps.</div>
        </div>
      </div>
      <section className="card">
        <div className="card-header">
          <h3>Locations</h3>
          <span className="chip">{props.length} places</span>
        </div>
        <ul className="list">
          {props.map(p => (
            <li className="list-item" key={p.id}>
              <div>
                <strong>{p.name}</strong>
                <div className="page-meta">{p.address || 'No address yet'}</div>
              </div>
              {p.google_maps_url ? (
                <a className="btn btn-ghost" href={p.google_maps_url} target="_blank" rel="noreferrer">Open map</a>
              ) : (
                <span className="page-meta">No map link</span>
              )}
            </li>
          ))}
        </ul>
      </section>
    </Layout>
  )
}
