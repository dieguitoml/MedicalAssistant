/**
 * Componente del mensaje individual 
 */

import type {Message} from '../types/chat'

interface ChatMessageProps {
    message : Message
}

export function ChatMessage ({message} : ChatMessageProps){
    const isUser = message.role === 'user'
    return(
        <div 
         className = {`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 animate-slideIn`}
         >
            <div
             className = {`max-w-[75%] rounded-2xl px-4 py-3 shadow-md
                ${isUser ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white'
                : 'bg-white text-gray-800 border border-gray-200'
                  }
             `}
            >
               <p className ="text-sm leading-relaxed whitespace-pre-wrap">
                {message.content}
               </p>
               <div
                className = {`text-xs mt-2 ${isUser  ? 'text-blue-100' : 'text-gray-500'} `}
                >
                    {message.timestamp.toLocaleTimeString('es-ES',{
                        hour : '2-digit',
                        minute : '2-digit'
                    })}
                </div>
            </div>

        </div>
    )
}