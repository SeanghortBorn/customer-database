import React from 'react'

export default function PropertyList({ properties }: { properties: any[] }) {
  return (
    <ul>
      {properties.map(p => (
        <li key={p.id}>{p.name} — {p.unit_count ?? 0} units</li>
      ))}
    </ul>
  )
}
