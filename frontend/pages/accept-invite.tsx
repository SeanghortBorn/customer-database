import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import axios from 'axios'

export default function AcceptInvitePage() {
  const router = useRouter()
  const { token } = router.query
  const [message, setMessage] = useState('')

  useEffect(() => {
    if (!token) return
    const accept = async () => {
      try {
        const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/invites/accept?token=${token}`)
        if (res.data && res.data.email) {
          // redirect to register with email and invite_token
          router.push(`/register?email=${encodeURIComponent(res.data.email)}&invite_token=${encodeURIComponent(token as string)}`)
        } else {
          setMessage('Invite accepted — please sign in')
          router.push('/login')
        }
      } catch (err: any) {
        setMessage(err?.response?.data?.detail || 'Invite acceptance failed')
      }
    }
    accept()
  }, [token])

  return (
    <div className="auth-shell">
      <div className="auth-card float-in">
        <h2>Accepting invite...</h2>
        <p>{message || 'We are validating the invitation and setting up your access.'}</p>
      </div>
    </div>
  )
}
