import { useApi } from '../hooks/useApi'

export default function Insights({ t }: { t: (k: string) => string }) {
  const { data, loading } = useApi<{ insights: any[]; total: number }>('/insights')

  if (loading) return <div className="loading"><div className="spinner" /> Loading...</div>

  return (
    <div>
      <div className="page-header">
        <h2>{t('insights')}</h2>
        <p>AI-generated marketplace intelligence</p>
      </div>

      {data?.insights.map(ins => (
        <div key={ins.id} className={`insight-card ${ins.priority}`}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <h4>{ins.title}</h4>
            <span className={`badge badge-${ins.priority}`}>{ins.priority}</span>
          </div>
          <p style={{ marginTop: 8 }}>{ins.description}</p>
          <div className="insight-meta">
            <span style={{ textTransform: 'capitalize' }}>{ins.insight_type.replace(/_/g, ' ')}</span>
            <span>{ins.affected_artisans?.length || 0} artisans affected</span>
            <span>IDs: {(ins.affected_artisans || []).join(', ')}</span>
          </div>
        </div>
      ))}
    </div>
  )
}
