import React from 'react'

export default function PeopleList({ people }: { people: any[] }) {
  return (
    <ul className="list">
      {people.map(p => (
        <li className="list-item" key={p.id}>
          <span>{p.first_name} {p.last_name}</span>
        </li>
      ))}
    </ul>
  )
}
