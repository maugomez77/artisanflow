import { useState } from 'react'
import { useApi } from '../hooks/useApi'

export default function Artisans({ t }: { t: (k: string) => string }) {
  const [craft, setCraft] = useState('')
  const [community, setCommunity] = useState('')
  const params = new URLSearchParams()
  if (craft) params.set('craft_type', craft)
  if (community) params.set('community', community)
  const qs = params.toString() ? `?${params}` : ''

  const { data, loading } = useApi<{ artisans: any[]; total: number }>(`/artisans${qs}`, [craft, community])

  if (loading) return <div className="loading"><div className="spinner" /> Loading...</div>

  return (
    <div>
      <div className="page-header">
        <h2>{t('artisans')}</h2>
        <p>Master craftspeople from Oaxacan communities</p>
      </div>

      <div className="filter-bar">
        <select value={craft} onChange={e => setCraft(e.target.value)}>
          <option value="">All Crafts</option>
          <option value="alebrije">Alebrije</option>
          <option value="barro_negro">Barro Negro</option>
          <option value="textile">Textile</option>
          <option value="wood_carving">Wood Carving</option>
          <option value="jewelry">Jewelry</option>
          <option value="leather">Leather</option>
          <option value="candle">Candle</option>
          <option value="mezcal_craft">Mezcal Craft</option>
        </select>
        <select value={community} onChange={e => setCommunity(e.target.value)}>
          <option value="">All Communities</option>
          <option value="arrazola">Arrazola</option>
          <option value="san_bartolo_coyotepec">San Bartolo Coyotepec</option>
          <option value="teotitlan_del_valle">Teotitlan del Valle</option>
          <option value="san_martin_tilcajete">San Martin Tilcajete</option>
          <option value="ocotlan">Ocotlan</option>
          <option value="santa_maria_atzompa">Santa Maria Atzompa</option>
        </select>
      </div>

      <div className="card">
        <table className="data-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Craft</th>
              <th>Community</th>
              <th>Experience</th>
              <th>Rating</th>
              <th>Specialties</th>
            </tr>
          </thead>
          <tbody>
            {data?.artisans.map(a => (
              <tr key={a.id}>
                <td><strong>{a.name}</strong><br /><span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>{a.id}</span></td>
                <td><span style={{ textTransform: 'capitalize' }}>{a.craft_type.replace(/_/g, ' ')}</span></td>
                <td style={{ textTransform: 'capitalize' }}>{a.community.replace(/_/g, ' ')}</td>
                <td>{a.years_experience} years</td>
                <td>
                  <span style={{ color: 'var(--warning)', fontWeight: 600 }}>{'★'.repeat(Math.round(a.rating))}</span>
                  {' '}{a.rating.toFixed(1)}
                </td>
                <td style={{ fontSize: '0.82rem' }}>{(a.specialties || []).join(', ')}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div style={{ marginTop: 12, color: 'var(--text-muted)', fontSize: '0.85rem' }}>
          {data?.total} artisans
        </div>
      </div>
    </div>
  )
}
