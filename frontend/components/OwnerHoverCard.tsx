import React, { useState } from 'react'
import Link from 'next/link'

type Owner = {
  id: string
  first_name: string
  last_name?: string
  phone?: string
  email?: string
  telegram?: string
  title?: string
}

interface OwnerHoverCardProps {
  owner: Owner | null | undefined
}

export default function OwnerHoverCard({ owner }: OwnerHoverCardProps) {
  const [showTooltip, setShowTooltip] = useState(false)

  if (!owner) {
    return <span className="page-meta">No owner</span>
  }

  const fullName = `${owner.first_name} ${owner.last_name || ''}`.trim()
  const role = owner.title || 'Owner'

  return (
    <div
      className="owner-hover-card"
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
    >
      <Link href="/people" className="owner-link">
        <span>{fullName || 'Unknown'}</span>
      </Link>

      {showTooltip && (
        <div className="tooltip tooltip-top">
          <div className="tooltip-content">
            <div className="tooltip-header">
              <span className="tooltip-name">{fullName || 'Unknown'}</span>
              <span className="tooltip-role">{role}</span>
            </div>
            {owner.email && (
              <div className="tooltip-row">
                <span className="tooltip-label">Email:</span>
                <a href={`mailto:${owner.email}`}>{owner.email}</a>
              </div>
            )}
            {owner.phone && (
              <div className="tooltip-row">
                <span className="tooltip-label">Phone:</span>
                <a href={`tel:${owner.phone}`}>{owner.phone}</a>
              </div>
            )}
            {owner.telegram && (
              <div className="tooltip-row">
                <span className="tooltip-label">Telegram:</span>
                <a href={`https://t.me/${owner.telegram}`} target="_blank" rel="noopener noreferrer">
                  @{owner.telegram}
                </a>
              </div>
            )}
          </div>
        </div>
      )}

      <style jsx>{`
        .owner-hover-card {
          position: relative;
          display: inline-block;
        }

        .owner-link {
          color: #0070f3;
          text-decoration: none;
          cursor: pointer;
          border-bottom: 1px dotted #0070f3;
        }

        .owner-link:hover {
          text-decoration: underline;
        }

        .tooltip {
          position: absolute;
          bottom: 100%;
          left: 50%;
          transform: translateX(-50%);
          margin-bottom: 8px;
          z-index: 1000;
        }

        .tooltip-content {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 12px;
          border-radius: 8px;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
          white-space: nowrap;
          font-size: 14px;
          line-height: 1.5;
        }

        .tooltip-header {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-bottom: 8px;
          padding-bottom: 8px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }

        .tooltip-name {
          font-weight: 600;
        }

        .tooltip-role {
          font-size: 12px;
          opacity: 0.8;
          background: rgba(255, 255, 255, 0.2);
          padding: 2px 6px;
          border-radius: 4px;
        }

        .tooltip-row {
          display: flex;
          gap: 8px;
          margin-bottom: 4px;
        }

        .tooltip-row:last-child {
          margin-bottom: 0;
        }

        .tooltip-label {
          font-weight: 500;
          opacity: 0.9;
        }

        .tooltip-row a {
          color: #fff;
          text-decoration: none;
          word-break: break-all;
        }

        .tooltip-row a:hover {
          text-decoration: underline;
        }

        .tooltip::after {
          content: '';
          position: absolute;
          top: 100%;
          left: 50%;
          transform: translateX(-50%);
          border: 6px solid transparent;
          border-top-color: #667eea;
        }
      `}</style>
    </div>
  )
}
