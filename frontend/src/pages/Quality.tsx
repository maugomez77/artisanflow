import { useApi } from '../hooks/useApi'

export default function Quality({ t }: { t: (k: string) => string }) {
  const { data, loading } = useApi<{ assessments: any[] }>('/quality')

  if (loading) return <div className="loading"><div className="spinner" /> Loading...</div>

  const ScoreBar = ({ score, label }: { score: number; label: string }) => {
    const pct = score * 10
    const level = pct >= 85 ? 'high' : pct >= 60 ? 'medium' : 'low'
    return (
      <div style={{ marginBottom: 4 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem' }}>
          <span>{label}</span>
          <span style={{ fontWeight: 600 }}>{score.toFixed(1)}</span>
        </div>
        <div className="score-bar">
          <div className={`score-bar-fill ${level}`} style={{ width: `${pct}%` }} />
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="page-header">
        <h2>{t('quality')}</h2>
        <p>Authenticity and craftsmanship assessments</p>
      </div>

      <div className="grid-2">
        {data?.assessments.map(q => (
          <div className="card" key={q.id}>
            <div className="card-header">
              <h3 style={{ fontSize: '0.95rem' }}>{q.product_id}</h3>
              <span className={`badge badge-${q.overall_grade}`}>{q.overall_grade}</span>
            </div>
            <ScoreBar score={q.authenticity_score} label="Authenticity" />
            <ScoreBar score={q.craftsmanship} label="Craftsmanship" />
            <ScoreBar score={q.materials_quality} label="Materials" />
            <ScoreBar score={q.finish_quality} label="Finish" />
            <ScoreBar score={q.cultural_accuracy} label="Cultural Accuracy" />
            <div style={{ marginTop: 12, padding: '8px 12px', background: 'var(--bg)', borderRadius: 'var(--radius)', fontSize: '0.82rem', color: 'var(--text-light)' }}>
              <strong>Inspector:</strong> {q.inspector}<br />
              {q.notes}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
