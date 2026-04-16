import { useState } from 'react'
import { useApi } from '../hooks/useApi'

export default function Products({ t }: { t: (k: string) => string }) {
  const [craft, setCraft] = useState('')
  const [grade, setGrade] = useState('')
  const [category, setCategory] = useState('')

  const params = new URLSearchParams()
  if (craft) params.set('craft_type', craft)
  if (grade) params.set('quality_grade', grade)
  if (category) params.set('category', category)
  const qs = params.toString() ? `?${params}` : ''

  const { data, loading } = useApi<{ products: any[]; total: number }>(`/products${qs}`, [craft, grade, category])

  if (loading) return <div className="loading"><div className="spinner" /> Loading...</div>

  return (
    <div>
      <div className="page-header">
        <h2>{t('products')}</h2>
        <p>Handcrafted Oaxacan art and crafts</p>
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
        <select value={grade} onChange={e => setGrade(e.target.value)}>
          <option value="">All Grades</option>
          <option value="museum">Museum</option>
          <option value="premium">Premium</option>
          <option value="standard">Standard</option>
          <option value="artisan">Artisan</option>
        </select>
        <select value={category} onChange={e => setCategory(e.target.value)}>
          <option value="">All Categories</option>
          <option value="home_decor">Home Decor</option>
          <option value="wearable">Wearable</option>
          <option value="collectible">Collectible</option>
          <option value="functional">Functional</option>
          <option value="ceremonial">Ceremonial</option>
        </select>
      </div>

      <div className="card">
        <table className="data-table">
          <thead>
            <tr>
              <th>Product</th>
              <th>Craft</th>
              <th>Grade</th>
              <th>Price</th>
              <th>Wholesale</th>
              <th>Stock</th>
              <th>Category</th>
            </tr>
          </thead>
          <tbody>
            {data?.products.map(p => (
              <tr key={p.id}>
                <td>
                  <strong>{p.name}</strong>
                  <br /><span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>{p.description?.slice(0, 60)}...</span>
                </td>
                <td style={{ textTransform: 'capitalize' }}>{p.craft_type.replace(/_/g, ' ')}</td>
                <td><span className={`badge badge-${p.quality_grade}`}>{p.quality_grade}</span></td>
                <td style={{ fontWeight: 600, color: 'var(--success)' }}>${p.price_usd.toLocaleString()}</td>
                <td style={{ color: 'var(--text-muted)' }}>${p.wholesale_price_usd.toLocaleString()}</td>
                <td>{p.stock_count}</td>
                <td style={{ textTransform: 'capitalize' }}>{p.category.replace(/_/g, ' ')}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div style={{ marginTop: 12, color: 'var(--text-muted)', fontSize: '0.85rem' }}>
          {data?.total} products
        </div>
      </div>
    </div>
  )
}
