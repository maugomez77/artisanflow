import { useApi } from '../hooks/useApi'

export default function Subscriptions({ t }: { t: (k: string) => string }) {
  const { data, loading } = useApi<{ subscriptions: any[]; total: number }>('/subscriptions')
  const { data: buyersData } = useApi<{ buyers: any[] }>('/buyers')

  if (loading) return <div className="loading"><div className="spinner" /> Loading...</div>

  const buyerMap: Record<string, string> = {}
  buyersData?.buyers?.forEach(b => { buyerMap[b.id] = b.name })

  return (
    <div>
      <div className="page-header">
        <h2>{t('subscriptions')}</h2>
        <p>Curated subscription boxes of Oaxacan crafts</p>
      </div>

      <div className="grid-2">
        {data?.subscriptions.map(s => (
          <div className="card" key={s.id}>
            <div className="card-header">
              <h3 style={{ textTransform: 'capitalize' }}>{s.theme.replace(/_/g, ' ')} Box</h3>
              <span className={`badge badge-${s.status}`}>{s.status}</span>
            </div>
            <div style={{ fontSize: '0.9rem' }}>
              <p><strong>Buyer:</strong> {buyerMap[s.buyer_id] || s.buyer_id}</p>
              <p><strong>Frequency:</strong> {s.frequency}</p>
              <p><strong>Price:</strong> <span style={{ color: 'var(--success)', fontWeight: 600 }}>${s.price_usd}/box</span></p>
              <p><strong>Next Shipment:</strong> {s.next_shipment_date || 'TBD'}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
