import { Routes, Route, NavLink } from 'react-router-dom'
import { useLang } from './hooks/useLang'
import Dashboard from './pages/Dashboard'
import Artisans from './pages/Artisans'
import Products from './pages/Products'
import Orders from './pages/Orders'
import Buyers from './pages/Buyers'
import Fulfillment from './pages/Fulfillment'
import Quality from './pages/Quality'
import Shipments from './pages/Shipments'
import Subscriptions from './pages/Subscriptions'
import Insights from './pages/Insights'
import AITools from './pages/AITools'

function App() {
  const { lang, t, setLang } = useLang()

  const navItems = [
    { section: 'marketplace', items: [
      { path: '/', label: 'dashboard', icon: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg> },
      { path: '/artisans', label: 'artisans', icon: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg> },
      { path: '/products', label: 'products', icon: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg> },
      { path: '/buyers', label: 'buyers', icon: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg> },
    ]},
    { section: 'operations', items: [
      { path: '/orders', label: 'orders', icon: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg> },
      { path: '/fulfillment', label: 'fulfillment', icon: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg> },
      { path: '/quality', label: 'quality', icon: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg> },
      { path: '/shipments', label: 'shipments', icon: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg> },
      { path: '/subscriptions', label: 'subscriptions', icon: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg> },
    ]},
    { section: 'intelligence', items: [
      { path: '/insights', label: 'insights', icon: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg> },
      { path: '/ai-tools', label: 'ai_tools', icon: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2a10 10 0 1 0 10 10H12V2z"/><path d="M12 2a10 10 0 0 1 10 10"/><path d="M12 12l8.5-5"/></svg> },
    ]},
  ]

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1>ArtisanFlow</h1>
          <p>Oaxacan Artisan Marketplace</p>
        </div>
        <nav>
          {navItems.map(group => (
            <div key={group.section}>
              <div className="sidebar-section">{t(group.section)}</div>
              {group.items.map(item => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  end={item.path === '/'}
                  className={({ isActive }) => isActive ? 'active' : ''}
                >
                  {item.icon}
                  {t(item.label)}
                </NavLink>
              ))}
            </div>
          ))}
        </nav>
        <div className="lang-toggle">
          <button className={lang === 'en' ? 'active' : ''} onClick={() => setLang('en')}>EN</button>
          <button className={lang === 'es' ? 'active' : ''} onClick={() => setLang('es')}>ES</button>
        </div>
      </aside>

      <main className="main">
        <Routes>
          <Route path="/" element={<Dashboard t={t} />} />
          <Route path="/artisans" element={<Artisans t={t} />} />
          <Route path="/products" element={<Products t={t} />} />
          <Route path="/orders" element={<Orders t={t} />} />
          <Route path="/buyers" element={<Buyers t={t} />} />
          <Route path="/fulfillment" element={<Fulfillment t={t} />} />
          <Route path="/quality" element={<Quality t={t} />} />
          <Route path="/shipments" element={<Shipments t={t} />} />
          <Route path="/subscriptions" element={<Subscriptions t={t} />} />
          <Route path="/insights" element={<Insights t={t} />} />
          <Route path="/ai-tools" element={<AITools t={t} />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
