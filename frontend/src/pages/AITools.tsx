import { useState } from 'react'
import { apiPost } from '../hooks/useApi'

export default function AITools({ t }: { t: (k: string) => string }) {
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [activeTool, setActiveTool] = useState('')

  const runTool = async (tool: string, endpoint: string, body: any) => {
    setLoading(true)
    setActiveTool(tool)
    setResult(null)
    try {
      const data = await apiPost(endpoint, body)
      setResult(data)
    } catch (e: any) {
      setResult({ error: e.message })
    }
    setLoading(false)
  }

  const tools = [
    {
      key: 'grade',
      title: t('grade_quality'),
      desc: 'AI quality/authenticity assessment using Claude Vision',
      action: () => runTool('grade', '/ai/grade', {
        name: 'Alebrije Dragon', craft_type: 'alebrije',
        description: 'Hand-carved copal wood dragon with intricate dot patterns',
        materials: ['copal wood', 'aniline dyes', 'natural pigments']
      }),
    },
    {
      key: 'pricing',
      title: t('optimize_pricing'),
      desc: 'Optimal pricing recommendations for different global markets',
      action: () => runTool('pricing', '/ai/pricing', { product_id: 'prod-001' }),
    },
    {
      key: 'match',
      title: t('match_buyers'),
      desc: 'Match products to buyer preferences using AI',
      action: () => runTool('match', '/ai/match', { buyer_id: 'buy-001' }),
    },
    {
      key: 'story',
      title: t('cultural_story'),
      desc: 'Generate bilingual cultural marketing narratives',
      action: () => runTool('story', '/ai/story', { product_id: 'prod-001' }),
    },
    {
      key: 'demand',
      title: t('demand_forecast'),
      desc: 'Predict demand trends by craft type and season',
      action: () => runTool('demand', '/ai/demand', { craft_type: 'alebrije', season: 'current' }),
    },
    {
      key: 'shipping',
      title: t('shipping_optimizer'),
      desc: 'Best carrier and route recommendations',
      action: () => runTool('shipping', '/ai/shipping', { order_id: 'ord-007', destination_country: 'FR' }),
    },
  ]

  return (
    <div>
      <div className="page-header">
        <h2>{t('ai_tools')}</h2>
        <p>Claude-powered intelligence for the marketplace</p>
      </div>

      <div className="grid-3">
        {tools.map(tool => (
          <div
            key={tool.key}
            className="ai-tool-card"
            onClick={tool.action}
            style={{ opacity: loading && activeTool !== tool.key ? 0.5 : 1 }}
          >
            <h4>{tool.title}</h4>
            <p>{tool.desc}</p>
            {loading && activeTool === tool.key && (
              <div style={{ marginTop: 8 }}>
                <div className="spinner" style={{ margin: '0 auto' }} />
              </div>
            )}
          </div>
        ))}
      </div>

      {result && (
        <div className="card" style={{ marginTop: 24 }}>
          <div className="card-header">
            <h3>AI Result: {activeTool}</h3>
          </div>
          <pre style={{
            background: 'var(--bg)',
            padding: 16,
            borderRadius: 'var(--radius)',
            overflow: 'auto',
            fontSize: '0.85rem',
            maxHeight: 500,
          }}>
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  )
}
