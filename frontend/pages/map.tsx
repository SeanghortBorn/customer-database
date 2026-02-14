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
      <h2>Map view (simple)</h2>
      <p>This view links to each property's Google Maps URL (if available).</p>
      <ul>
        {props.map(p => (
          <li key={p.id}>{p.name} — {p.address} {p.google_maps_url ? <a href={p.google_maps_url} target="_blank">Map</a> : null}</li>
        ))}
      </ul>
    </Layout>
  )
}
