'use client';
import { useState } from 'react';

export default function Home() {
  const [messages, setMessages] = useState([
    { role: 'ai', text: 'Assalam-o-Alaikum! Your fresh Next.js workspace is ready. What project tasks or study topics are we working on today?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    
    const userQuery = input.trim();
    setMessages((prev) => [...prev, { role: 'user', text: userQuery }]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: userQuery }),
      });
      const data = await response.json();
      
      if (response.ok) {
        setMessages((prev) => [...prev, { role: 'ai', text: data.response }]);
      } else {
        setMessages((prev) => [...prev, { role: 'ai', text: `Error: ${data.detail}` }]);
      }
    } catch (err) {
      setMessages((prev) => [...prev, { role: 'ai', text: 'Unable to connect to the local server.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex h-screen items-center justify-center bg-[#1e1e2e] text-[#cdd6f4] p-4">
      <div className="w-full max-w-xl h-[80vh] bg-[#252538] rounded-xl flex flex-col overflow-hidden shadow-2xl border border-[#45475a]">
        <div className="bg-[#11111b] p-4 text-center border-b border-[#45475a]">
          <h1 className="text-lg font-bold text-[#cba6f7]">Personalized AI Workspace</h1>
          <p className="text-xs text-[#a6adc8] mt-0.5">Next.js Web Interface</p>
        </div>
        <div className="flex-1 p-4 overflow-y-auto flex flex-col gap-3">
          {messages.map((m, i) => (
            <div key={i} className={`p-3 rounded-xl max-w-[85%] whitespace-pre-wrap text-[0.95rem] ${m.role === 'user' ? 'bg-[#cba6f7] text-[#11111b] self-end font-medium' : 'bg-[#313244] text-[#cdd6f4] self-start border border-[#45475a]'}`}>
              {m.text}
            </div>
          ))}
          {loading && <div className="text-xs italic text-[#a6adc8] animate-pulse pl-1">Processing...</div>}
        </div>
        <div className="p-3 bg-[#11111b] flex gap-2 border-t border-[#45475a]">
          <input
            type="text"
            className="flex-1 bg-[#1e1e2e] border border-[#45475a] rounded-lg px-3 py-2 text-sm outline-none focus:border-[#cba6f7]"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask your companion..."
          />
          <button className="bg-[#cba6f7] text-[#11111b] px-4 py-2 rounded-lg font-bold text-sm" onClick={handleSend}>Send</button>
        </div>
      </div>
    </main>
  );
}