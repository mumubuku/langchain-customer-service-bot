import { Sidebar } from './Sidebar'
import { ChatWindow } from './ChatWindow'

export default function App() {
  return (
    <main className="grid grid-cols-5 h-screen">
     

      <Sidebar className="col-span-1" />
      <ChatWindow className="col-span-4" />
    </main>
  )
}
