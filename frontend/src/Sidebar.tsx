import { useEffect, useState } from 'react'

export function Sidebar({ className }: { className?: string }) {
  const [docs, setDocs] = useState<any[]>([])
  const [refreshing, setRefreshing] = useState(false)

  // 获取当前文档列表
  async function fetchDocs() {
    try {
      const res = await fetch('/docss')
      const data = await res.json()
      setDocs(data.documents)
    } catch (err) {
      console.error('❌ 获取文档失败:', err)
    }
  }

  // 删除文档
  async function handleDelete(filename: string) {
    const formData = new FormData()
    formData.append('filename', filename)
    await fetch('/docss/delete', { method: 'POST', body: formData })
    fetchDocs()
  }

  // 上传 PDF
  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return
    const formData = new FormData()
    formData.append('file', file)
    await fetch('/upload', { method: 'POST', body: formData })
    fetchDocs()
  }

  // 刷新向量库
  async function handleRefresh() {
    setRefreshing(true)
    await fetch('/refresh', { method: 'POST' })
    setRefreshing(false)
    alert('✅ 向量库已刷新完成')
  }

  useEffect(() => {
    fetchDocs()
  }, [])

  return (
    <div className={"p-4 border-r overflow-y-auto " + className}>
      <h2 className="text-lg font-bold mb-4">📄 文档管理</h2>

      <input type="file" accept=".pdf" onChange={handleUpload} className="mb-4" />

      <ul className="space-y-2">
        {docs.map((doc) => (
          <li key={doc.filename} className="flex justify-between items-center bg-gray-100 px-2 py-1 rounded shadow-sm">
            <span className="truncate text-sm">{doc.filename}</span>
            <button
              onClick={() => handleDelete(doc.filename)}
              className="text-red-500 text-xs hover:underline"
            >
              删除
            </button>
          </li>
        ))}
      </ul>

      <button
        onClick={handleRefresh}
        disabled={refreshing}
        className="mt-6 text-sm text-blue-600 hover:underline disabled:opacity-50"
      >
        🔄 {refreshing ? '刷新中...' : '刷新向量库'}
      </button>
    </div>
  )
}
