import React from 'react';
import { Bot, User } from 'lucide-react';

export default function MessageBubble({ message, isUser }) {
  return (
    <div className={`flex w-full mb-6 ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex max-w-[85%] md:max-w-[75%] gap-4 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        
        {/* Avatar */}
        <div className="flex-shrink-0 mt-1">
          {isUser ? (
            <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center shadow-sm">
              <User size={16} className="text-gray-600" />
            </div>
          ) : (
            <div className="w-8 h-8 rounded-full bg-[#4285F4] flex items-center justify-center shadow-sm">
              <Bot size={18} className="text-white" />
            </div>
          )}
        </div>

        {/* Message Content */}
        <div className="flex flex-col">
          <div className={`px-5 py-3.5 rounded-2xl shadow-sm ${
            isUser 
              ? 'bg-[#4285F4] text-white rounded-tr-sm' 
              : 'bg-white text-gray-800 border border-gray-100 rounded-tl-sm'
          }`}>
            <p className="whitespace-pre-wrap leading-relaxed">{message.text}</p>
            
            {/* Structured data rendering for specific skills */}
            {!isUser && message.data && (
              <div className="mt-3 pt-3 border-t border-gray-100 space-y-2 text-sm">
                
                {/* Grammar Checker output */}
                {message.data.corrected_text && (
                  <div className="bg-green-50 p-3 rounded-lg">
                    <span className="font-bold text-green-700 block mb-1">Correction:</span>
                    <span className="text-gray-800">{message.data.corrected_text}</span>
                  </div>
                )}
                {message.data.explanation && (
                  <div className="mt-2 text-gray-600">
                    <span className="font-semibold text-blue-600">Explanation: </span>
                    <span>{message.data.explanation}</span>
                  </div>
                )}

                {/* Vocab Saver output */}
                {message.skill === 'vocab-saver' && message.data.entry && (
                  <div className="bg-blue-50 p-3 rounded-lg mt-2 text-gray-800">
                    <p className="mb-1"><strong className="text-[#4285F4]">Word:</strong> {message.data.entry.word}</p>
                    <p><strong className="text-[#4285F4]">Meaning:</strong> {message.data.entry.meaning}</p>
                  </div>
                )}
              </div>
            )}
          </div>
          
          {/* Tag indicating which skill handled the request */}
          {!isUser && message.skill && (
            <div className="flex items-center gap-1 mt-2 ml-2">
              <span className="inline-block w-2 h-2 rounded-full bg-green-400"></span>
              <span className="text-xs text-gray-400 font-medium">
                Skill invoked: {message.skill}
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
