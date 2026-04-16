import { useApi } from '../hooks/useApi'

export default function Fulfillment({ t }: { t: (k: string) => string }) {
  const { data, loading } = useApi<{ queued: any[]; in_progress: any[]; completed: any[] }>('/fulfillment/pipeline')

  if (loading || !data) return <div className="loading"><div className="spinner" /> Loading...</div>

  const renderCard = (task: any) => (
    <div className="kanban-card" key={task.id}>
      <div className="task-type">{task.task_type.replace(/_/g, ' ')}</div>
      <div className="task-meta">
        Order: {task.order_id}<br />
        Assigned: {task.assigned_to || 'Unassigned'}
      </div>
    </div>
  )

  return (
    <div>
      <div className="page-header">
        <h2>{t('fulfillment')}</h2>
        <p>Fulfillment pipeline — track orders from photo to ship</p>
      </div>

      <div className="kanban">
        <div className="kanban-column">
          <h4>
            Queued <span className="count">{data.queued.length}</span>
          </h4>
          {data.queued.map(renderCard)}
          {data.queued.length === 0 && <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>No queued tasks</p>}
        </div>
        <div className="kanban-column">
          <h4>
            In Progress <span className="count">{data.in_progress.length}</span>
          </h4>
          {data.in_progress.map(renderCard)}
          {data.in_progress.length === 0 && <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>No active tasks</p>}
        </div>
        <div className="kanban-column">
          <h4>
            Completed <span className="count">{data.completed.length}</span>
          </h4>
          {data.completed.map(renderCard)}
          {data.completed.length === 0 && <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>No completed tasks</p>}
        </div>
      </div>
    </div>
  )
}
