import { useState } from 'react'
import { useApi } from '../hooks/useApi'

export default function Orders({ t }: { t: (k: string) => string }) {
  const [status, setStatus] = useState('')
  const qs = status ? `?status=${status}` : ''
  const { data, loading } = useApi<{ orders: any[]; total: number }>(`/orders${qs}`, [status])
  const { data: buyersData } = useApi<{ buyers: any[] }>('/buyers')

  if (loading) return <div className="loading"><div className="spinner" /> Loading...</div>

  const buyerMap: Record<string, string> = {}
  buyersData?.buyers?.forEach(b => { buyerMap[b.id] = b.name })

  return (
    <div>
      <div className="page-header">
        <h2>{t('orders')}</h2>
        <p>Order tracking and management</p>
      </div>

      <div className="filter-bar">
        <select value={status} onChange={e => setStatus(e.target.value)}>
          <option value="">All Statuses</option>
          <option value="pending">Pending</option>
          <option value="processing">Processing</option>
          <option value="photographed">Photographed</option>
          <option value="packed">Packed</option>
          <option value="shipped">Shipped</option>
          <option value="delivered">Delivered</option>
          <option value="returned">Returned</option>
        </select>
      </div>

      <div className="card">
        <table className="data-table">
          <thead>
            <tr>
              <th>Order ID</th>
              <th>Buyer</th>
              <th>Items</th>
              <th>Total</th>
              <th>Status</th>
              <th>Shipping</th>
              <th>Tracking</th>
            </tr>
          </thead>
          <tbody>
            {data?.orders.map(o => (
              <tr key={o.id}>
                <td><strong>{o.id}</strong></td>
                <td>{buyerMap[o.buyer_id] || o.buyer_id}</td>
                <td>{o.product_ids?.length || 0}</td>
                <td style={{ fontWeight: 600, color: 'var(--success)' }}>${o.total_usd.toLocaleString()}</td>
                <td><span className={`badge badge-${o.status}`}>{o.status}</span></td>
                <td style={{ textTransform: 'capitalize' }}>{o.shipping_method?.replace(/_/g, ' ')}</td>
                <td style={{ fontSize: '0.82rem', fontFamily: 'monospace' }}>{o.tracking_number || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div style={{ marginTop: 12, color: 'var(--text-muted)', fontSize: '0.85rem' }}>
          {data?.total} orders | Total: ${data?.orders.reduce((s: number, o: any) => s + o.total_usd, 0).toLocaleString()}
        </div>
      </div>
    </div>
  )
}
