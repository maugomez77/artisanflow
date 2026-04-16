import { useState, useEffect, useCallback } from 'react'

const API_BASE = (import.meta.env.VITE_API_URL || '') + '/api'

export function useApi<T>(path: string, deps: any[] = []) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchData = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const resp = await fetch(`${API_BASE}${path}`)
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
      const json = await resp.json()
      setData(json)
    } catch (e: any) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }, [path])

  useEffect(() => {
    fetchData()
  }, [fetchData, ...deps])

  return { data, loading, error, refetch: fetchData }
}

export async function apiPost(path: string, body: any) {
  const resp = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
  return resp.json()
}
