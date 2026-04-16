import { useState, useCallback } from 'react'

type Lang = 'en' | 'es'

const translations: Record<string, Record<Lang, string>> = {
  dashboard: { en: 'Dashboard', es: 'Tablero' },
  artisans: { en: 'Artisans', es: 'Artesanos' },
  products: { en: 'Products', es: 'Productos' },
  orders: { en: 'Orders', es: 'Pedidos' },
  buyers: { en: 'Buyers', es: 'Compradores' },
  fulfillment: { en: 'Fulfillment', es: 'Cumplimiento' },
  quality: { en: 'Quality', es: 'Calidad' },
  shipments: { en: 'Shipments', es: 'Envios' },
  subscriptions: { en: 'Subscriptions', es: 'Suscripciones' },
  insights: { en: 'AI Insights', es: 'Perspectivas IA' },
  ai_tools: { en: 'AI Tools', es: 'Herramientas IA' },
  total_artisans: { en: 'Total Artisans', es: 'Total Artesanos' },
  total_products: { en: 'Total Products', es: 'Total Productos' },
  active_orders: { en: 'Active Orders', es: 'Pedidos Activos' },
  monthly_revenue: { en: 'Monthly Revenue', es: 'Ingresos Mensuales' },
  fulfillment_rate: { en: 'Fulfillment Rate', es: 'Tasa de Cumplimiento' },
  top_crafts: { en: 'Top Crafts', es: 'Mejores Artesanias' },
  top_markets: { en: 'Top Markets', es: 'Mejores Mercados' },
  marketplace: { en: 'Marketplace', es: 'Mercado' },
  operations: { en: 'Operations', es: 'Operaciones' },
  intelligence: { en: 'Intelligence', es: 'Inteligencia' },
  weather_advisory: { en: 'Weather Advisory', es: 'Aviso Meteorologico' },
  grade_quality: { en: 'Grade Quality', es: 'Evaluar Calidad' },
  optimize_pricing: { en: 'Optimize Pricing', es: 'Optimizar Precios' },
  match_buyers: { en: 'Match Buyers', es: 'Emparejar Compradores' },
  cultural_story: { en: 'Cultural Story', es: 'Historia Cultural' },
  demand_forecast: { en: 'Demand Forecast', es: 'Pronostico de Demanda' },
  shipping_optimizer: { en: 'Shipping Optimizer', es: 'Optimizador de Envio' },
}

export function useLang() {
  const [lang, setLang] = useState<Lang>('en')

  const t = useCallback((key: string): string => {
    return translations[key]?.[lang] || key
  }, [lang])

  const toggleLang = useCallback(() => {
    setLang(prev => prev === 'en' ? 'es' : 'en')
  }, [])

  return { lang, t, toggleLang, setLang }
}
