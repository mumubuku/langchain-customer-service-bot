import { useState } from 'react'

export function ChatWindow({ className }: { className?: string }) {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  async function sendMessage() {
    if (!input.trim() || loading) return
    const question = input
    setInput('')
    setLoading(true)

    // 先显示提问
    setMessages((prev) => [...prev, { q: question, a: '🤔 正在思考中...', loading: true }])

    try {
      const res = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 'u123', question })
      })
      const data = await res.json()

      // 替换最后一条 loading 消息
      setMessages((prev) => [
        ...prev.slice(0, -1),
        { q: question, a: data.answer, src: data.sources }
      ])
    } catch (e) {
      setMessages((prev) => [
        ...prev.slice(0, -1),
        { q: question, a: '❌ 出错了，请稍后重试。' }
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={`flex flex-col h-full ${className}`}>
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((m, idx) => (
          <div key={idx} className="space-y-1">
            <div className="bg-blue-100 text-blue-900 rounded-lg p-3 max-w-[80%] ml-auto shadow">
              <div className="text-sm font-medium">🙋 {m.q}</div>
            </div>
            <div className="bg-gray-100 text-gray-800 rounded-lg p-3 max-w-[80%] shadow">
              <div className="text-sm whitespace-pre-line">{m.a}</div>
              {m.src?.length > 0 && (
                <div className="text-xs text-gray-500 mt-1">
                  📎 引用：{m.src.map((s: any) => s.source).join('，')}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="p-3 border-t flex gap-3 bg-white">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          disabled={loading}
          className="flex-1 border border-gray-300 px-3 py-2 rounded-xl text-sm shadow-sm focus:outline-none disabled:bg-gray-100"
          placeholder={loading ? '请稍候...' : '请输入问题...'}
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded-xl shadow hover:bg-blue-700 transition disabled:opacity-50"
        >
          {loading ? '发送中...' : '发送'}
        </button>
      </div>
    </div>
  )
}
