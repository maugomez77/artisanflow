import { useApi } from '../hooks/useApi'

export default function Shipments({ t }: { t: (k: string) => string }) {
  const { data, loading } = useApi<{ shipments: any[]; total: number }>('/shipments')

  if (loading) return <div className="loading"><div className="spinner" /> Loading...</div>

  return (
    <div>
      <div className="page-header">
        <h2>{t('shipments')}</h2>
        <p>International shipment tracking from Oaxaca</p>
      </div>

      <div className="card" style={{ marginBottom: 24 }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Tracking</th>
              <th>Order</th>
              <th>Carrier</th>
              <th>Destination</th>
              <th>Status</th>
              <th>Insurance</th>
              <th>Events</th>
            </tr>
          </thead>
          <tbody>
            {data?.shipments.map(s => (
              <tr key={s.id}>
                <td style={{ fontFamily: 'monospace', fontSize: '0.82rem' }}>{s.tracking_number}</td>
                <td>{s.order_id}</td>
                <td style={{ textTransform: 'uppercase', fontWeight: 600 }}>{s.carrier}</td>
                <td>{s.destination_country}</td>
                <td><span className={`badge badge-${s.status === 'delivered' ? 'delivered' : s.status === 'in_transit' ? 'shipped' : 'pending'}`}>{s.status.replace(/_/g, ' ')}</span></td>
                <td style={{ color: 'var(--success)' }}>${s.insurance_usd}</td>
                <td>{s.events?.length || 0}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h3 style={{ marginBottom: 16 }}>Shipment Timeline</h3>
      {data?.shipments.filter(s => s.events?.length > 0).map(s => (
        <div className="card" key={s.id} style={{ marginBottom: 16 }}>
          <h4 style={{ fontSize: '0.95rem', marginBottom: 8 }}>
            {s.tracking_number} → {s.destination_country}
            {s.temperature_sensitive && <span className="badge badge-high" style={{ marginLeft: 8 }}>Temp Sensitive</span>}
          </h4>
          <div style={{ paddingLeft: 16, borderLeft: '2px solid var(--primary)' }}>
            {s.events.map((e: any, i: number) => (
              <div key={i} style={{ marginBottom: 8, paddingLeft: 12 }}>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>{e.date?.slice(0, 10)}</div>
                <div style={{ display: 'flex', gap: 8 }}>
                  <span className={`badge badge-${e.status === 'delivered' ? 'delivered' : e.status === 'customs' ? 'pending' : 'shipped'}`}>{e.status}</span>
                  <span>{e.location}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
