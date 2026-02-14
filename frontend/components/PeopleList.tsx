import React from 'react'

export default function PeopleList({ people }: { people: any[] }) {
  return (
    <ul>
      {people.map(p => (
        <li key={p.id}>{p.first_name} {p.last_name}</li>
      ))}
    </ul>
  )
}
