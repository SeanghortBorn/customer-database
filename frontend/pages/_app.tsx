import '../styles/globals.css'
import type { AppProps } from 'next/app'
import { useEffect, useState } from 'react'
import axios from 'axios'

export default function App({ Component, pageProps }: AppProps) {
  const [hydrated, setHydrated] = useState(false)

  useEffect(() => {
    if (typeof window !== 'undefined') {
      // store token from query string (OAuth redirect)
      const params = new URLSearchParams(window.location.search)
      const tokenFromUrl = params.get('token')
      if (tokenFromUrl) {
        localStorage.setItem('auth_token', tokenFromUrl)
        // remove token from url
        const url = new URL(window.location.href)
        url.searchParams.delete('token')
        window.history.replaceState({}, '', url.toString())
      }
      const token = localStorage.getItem('auth_token')
      if (token) axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    }
    setHydrated(true)
  }, [])

  if (!hydrated) return null
  return <Component {...pageProps} />
}
