/**
 * Input component para mensajes del chat
 */

import {useState} from 'react'
import type {KeyboardEvent} from 'react'
import {Send, Trash2, Volume2, Video} from 'lucide-react'

interface ChatInputProps {
    onSend : (message: string, useTts?: boolean, useAvatar?: boolean) => void
    disabled? : boolean
    placeholder? : string
    onClear? : () => void
}

export function ChatInput({onSend, disabled, placeholder, onClear} : ChatInputProps){
    const [input, setInput] = useState('')
    const [useTts, setUseTts] = useState(true)
    const [useAvatar, setUseAvatar] = useState(true)

    const handleSend = () => {
        if(input.trim() && !disabled){
            onSend(input.trim(), useTts, useAvatar)
            setInput('')
        }
    }

    const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
       if(e.key === 'Enter' && !e.shiftKey) {
         e.preventDefault()
         handleSend()
       }
    }    

    return (
        <div className = "p-4 border-t border-gray-200 bg-gray-50 space-y-3">
            {/* Checkboxes para opciones */}
            <div className = "flex gap-4 items-center">
                <label className = "flex items-center gap-2 cursor-pointer group">
                    <input
                      type = "checkbox"
                      checked = {useTts}
                      onChange = {(e) => setUseTts(e.target.checked)}
                      disabled = {disabled}
                      className = "w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2 cursor-pointer disabled:opacity-50"
                    />
                    <Volume2 className = {`w-5 h-5 ${useTts ? 'text-blue-600' : 'text-gray-400'} transition-colors`} />
                    <span className = "text-sm font-medium text-gray-700 group-hover:text-blue-600 transition-colors">
                      Respuesta con audio
                    </span>
                </label>

                <label className = "flex items-center gap-2 cursor-pointer group">
                    <input
                      type = "checkbox"
                      checked = {useAvatar}
                      onChange = {(e) => setUseAvatar(e.target.checked)}
                      disabled = {disabled}
                      className = "w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2 cursor-pointer disabled:opacity-50"
                    />
                    <Video className = {`w-5 h-5 ${useAvatar ? 'text-blue-600' : 'text-gray-400'} transition-colors`} />
                    <span className = "text-sm font-medium text-gray-700 group-hover:text-blue-600 transition-colors">
                      Respuesta con video
                    </span>
                </label>
            </div>

            {/* Input y botones */}
            <div className = "flex gap-3">
                <input
                  type = "text"
                  value = {input}
                  onChange = {(e) => setInput(e.target.value)}
                  onKeyDown = {handleKeyDown}
                  placeholder={placeholder ||"Escribe tu consulta médica aquí..."}
                  disabled = {disabled}
                  className = "flex-1 px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                />
                {onClear && (
                    <button
                      onClick = {onClear}
                      disabled = {disabled}
                      className = "px-4 py-3 bg-gray-200 text-gray-700 rounded-xl hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 font-medium flex items-center gap-2"
                      title="Limpiar chat"
                    >
                      <Trash2 className = "w-5 h-5" />
                    </button>
                )}
                <button
                  onClick = {handleSend}
                  disabled = {disabled || !input.trim()}
                  className = "px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl hover:from-blue-600 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 font-medium flex items-center gap-2 shadow-lg hover:shadow-xl"
                >
                    <Send className = "w-5 h-5 " />
                    Enviar
                </button>
            </div>
        </div>
    )
}
