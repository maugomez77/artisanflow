import { useApi } from '../hooks/useApi'

interface Stats {
  total_artisans: number
  total_products: number
  active_orders: number
  monthly_revenue_usd: number
  top_crafts: string[]
  top_markets: string[]
  fulfillment_success_rate: number
}

interface Weather {
  temperature_c?: number
  avg_humidity_pct?: number
  packaging_advisory?: string
  error?: string
}

export default function Dashboard({ t }: { t: (k: string) => string }) {
  const { data: stats, loading } = useApi<Stats>('/stats')
  const { data: weather } = useApi<Weather>('/research/weather')
  const { data: insightsData } = useApi<{ insights: any[] }>('/insights?priority=high')

  if (loading || !stats) return <div className="loading"><div className="spinner" /> Loading...</div>

  const isHighHumidity = (weather?.avg_humidity_pct || 0) > 70

  return (
    <div>
      <div className="page-header">
        <h2>{t('dashboard')}</h2>
        <p>Oaxacan artisan marketplace overview</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{stats.total_artisans}</div>
          <div className="stat-label">{t('total_artisans')}</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.total_products}</div>
          <div className="stat-label">{t('total_products')}</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.active_orders}</div>
          <div className="stat-label">{t('active_orders')}</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">${stats.monthly_revenue_usd.toLocaleString()}</div>
          <div className="stat-label">{t('monthly_revenue')}</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.fulfillment_success_rate}%</div>
          <div className="stat-label">{t('fulfillment_rate')}</div>
        </div>
      </div>

      <div className="grid-2">
        <div className="card">
          <div className="card-header">
            <h3>{t('top_crafts')}</h3>
          </div>
          {stats.top_crafts.map((c, i) => (
            <div key={c} style={{ padding: '8px 0', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ textTransform: 'capitalize' }}>{c.replace(/_/g, ' ')}</span>
              <span className="badge badge-standard">#{i + 1}</span>
            </div>
          ))}
        </div>

        <div className="card">
          <div className="card-header">
            <h3>{t('top_markets')}</h3>
          </div>
          {stats.top_markets.map((m, i) => (
            <div key={m} style={{ padding: '8px 0', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between' }}>
              <span>{m}</span>
              <span className="badge badge-standard">#{i + 1}</span>
            </div>
          ))}
        </div>
      </div>

      {weather && !weather.error && (
        <div className={`weather-card ${isHighHumidity ? 'warning' : ''}`} style={{ marginBottom: 24 }}>
          <h4>{t('weather_advisory')} - Oaxaca</h4>
          <p style={{ marginTop: 4 }}>
            {weather.temperature_c}°C | Humidity: {weather.avg_humidity_pct}%
          </p>
          <p style={{ marginTop: 4, fontWeight: 500, color: isHighHumidity ? 'var(--warning)' : 'var(--success)' }}>
            {weather.packaging_advisory}
          </p>
        </div>
      )}

      {insightsData?.insights && insightsData.insights.length > 0 && (
        <div>
          <h3 style={{ marginBottom: 12 }}>Priority {t('insights')}</h3>
          {insightsData.insights.slice(0, 3).map((ins: any) => (
            <div key={ins.id} className={`insight-card ${ins.priority}`}>
              <h4>{ins.title}</h4>
              <p>{ins.description}</p>
              <div className="insight-meta">
                <span className={`badge badge-${ins.priority}`}>{ins.priority}</span>
                <span>{ins.insight_type.replace(/_/g, ' ')}</span>
                <span>{ins.affected_artisans?.length || 0} artisans affected</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
