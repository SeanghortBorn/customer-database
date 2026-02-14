import Link from 'next/link'

export default function Home() {
  return (
    <div style={{ padding: 24 }}>
      <h1>Zoneer — Customer & Property Manager (PWA scaffold)</h1>
      <p>Front-end placeholder. Use the navigation below to explore the scaffolded UI.</p>
      <ul>
        <li><Link href="/people">People (contacts)</Link></li>
        <li><Link href="/properties">Properties</Link></li>
      </ul>
    </div>
  )
}
