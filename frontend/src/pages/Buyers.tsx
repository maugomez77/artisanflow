import { useState } from 'react'
import { useApi } from '../hooks/useApi'

export default function Buyers({ t }: { t: (k: string) => string }) {
  const [buyerType, setBuyerType] = useState('')
  const qs = buyerType ? `?buyer_type=${buyerType}` : ''
  const { data, loading } = useApi<{ buyers: any[]; total: number }>(`/buyers${qs}`, [buyerType])

  if (loading) return <div className="loading"><div className="spinner" /> Loading...</div>

  return (
    <div>
      <div className="page-header">
        <h2>{t('buyers')}</h2>
        <p>Global buyers and collectors</p>
      </div>

      <div className="filter-bar">
        <select value={buyerType} onChange={e => setBuyerType(e.target.value)}>
          <option value="">All Types</option>
          <option value="interior_designer">Interior Designer</option>
          <option value="luxury_retailer">Luxury Retailer</option>
          <option value="collector">Collector</option>
          <option value="gallery">Gallery</option>
          <option value="hotel_chain">Hotel Chain</option>
          <option value="corporate">Corporate</option>
          <option value="individual">Individual</option>
        </select>
      </div>

      <div className="card">
        <table className="data-table">
          <thead>
            <tr>
              <th>Buyer</th>
              <th>Type</th>
              <th>Company</th>
              <th>Country</th>
              <th>Orders</th>
              <th>Total Spent</th>
              <th>Tier</th>
              <th>Preferences</th>
            </tr>
          </thead>
          <tbody>
            {data?.buyers.map(b => (
              <tr key={b.id}>
                <td><strong>{b.name}</strong><br /><span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>{b.email}</span></td>
                <td style={{ textTransform: 'capitalize' }}>{b.type.replace(/_/g, ' ')}</td>
                <td>{b.company || '-'}</td>
                <td>{b.country}</td>
                <td>{b.total_orders}</td>
                <td style={{ fontWeight: 600, color: 'var(--success)' }}>${b.total_spent_usd.toLocaleString()}</td>
                <td><span className={`badge badge-${b.membership_tier === 'premium' ? 'museum' : b.membership_tier === 'professional' ? 'premium' : 'standard'}`}>{b.membership_tier}</span></td>
                <td style={{ fontSize: '0.82rem' }}>{(b.preferences || []).join(', ')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
