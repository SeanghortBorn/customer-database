import React from 'react'

export default function PropertyList({ properties }: { properties: any[] }) {
  return (
    <ul className="list">
      {properties.map(p => (
        <li className="list-item" key={p.id}>
          <span>{p.name}</span>
          <span className="page-meta">{p.unit_count ?? 0} units</span>
        </li>
      ))}
    </ul>
  )
}
