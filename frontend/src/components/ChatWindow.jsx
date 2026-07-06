import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2 } from 'lucide-react';
import MessageBubble from './MessageBubble';
import { sendChatMessage } from '../services/api';

export default function ChatWindow() {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I am your Smart English Concierge. I can correct your grammar, save vocabulary, and help you practice. How can I help today?", isUser: false }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;
    
    // Add user message to UI immediately
    const userMsg = { id: Date.now(), text: input, isUser: true };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      // Connect to real FastAPI backend
      const response = await sendChatMessage(userMsg.text);
      
      // Add AI response to UI
      const aiMsg = { 
        id: Date.now() + 1, 
        text: response.message, 
        isUser: false,
        skill: response.skill,
        data: response.data
      };
      setMessages(prev => [...prev, aiMsg]);
    } catch (error) {
      console.error("Chat error:", error);
      const errorMsg = { 
        id: Date.now() + 1, 
        text: "Sorry, I couldn't reach the backend server. Please ensure the FastAPI server is running on port 8000.", 
        isUser: false 
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-full bg-[#F8F9FA]">
      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-10">
        <div className="max-w-4xl mx-auto w-full">
          {messages.map(msg => (
            <MessageBubble key={msg.id} message={msg} isUser={msg.isUser} />
          ))}
          
          {/* Loading Animation */}
          {isLoading && (
            <div className="flex justify-start mb-6">
              <div className="bg-white px-5 py-4 rounded-2xl rounded-tl-sm shadow-sm border border-gray-100 flex items-center gap-3 text-gray-500">
                <Loader2 size={18} className="animate-spin text-[#4285F4]" />
                <span className="text-sm font-medium">Processing your request...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="p-4 sm:p-6 bg-white border-t border-gray-100 shadow-[0_-4px_10px_rgba(0,0,0,0.02)] z-10">
        <div className="max-w-4xl mx-auto relative flex items-end gap-3">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message here..."
            className="w-full bg-[#F1F3F4] text-gray-800 rounded-2xl px-6 py-4 outline-none focus:ring-2 focus:ring-[#4285F4] focus:bg-white transition-all resize-none"
            rows="1"
            style={{ minHeight: '56px', maxHeight: '150px' }}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className="flex-shrink-0 bg-[#4285F4] hover:bg-[#3367D6] disabled:bg-blue-300 disabled:cursor-not-allowed text-white w-14 h-14 rounded-full flex items-center justify-center transition-colors shadow-md"
          >
            <Send size={20} className="ml-1" />
          </button>
        </div>
        <div className="max-w-4xl mx-auto text-center mt-3">
          <span className="text-xs text-gray-400">Press Enter to send, Shift + Enter for new line.</span>
        </div>
      </div>
    </div>
  );
}
