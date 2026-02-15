import Link from 'next/link'

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center">
      <h1 className="text-4xl font-bold mb-8">Customer Database System (CDS)</h1>
      <div className="flex gap-4">
        <Link 
          href="/login" 
          className="rounded bg-blue-600 px-6 py-3 text-white hover:bg-blue-700"
        >
          Sign In
        </Link>
        <Link 
          href="/signup" 
          className="rounded border px-6 py-3 hover:bg-gray-100"
        >
          Sign Up
        </Link>
      </div>
    </div>
  )
}