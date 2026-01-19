/**
 * Input component para mensajes del chat
 */

import {useState, useEffect, useRef} from 'react'
import type {KeyboardEvent} from 'react'
import {Send, Trash2, Volume2, Video, Mic, MicOff} from 'lucide-react'

interface ChatInputProps {
    onSend : (message: string) => void
    disabled? : boolean
    placeholder? : string
    onClear? : () => void
    useTts?: boolean
    useAvatar?: boolean
    onTtsChange?: (checked: boolean) => void
    onAvatarChange?: (checked: boolean) => void
}

export function ChatInput({onSend, disabled, placeholder, onClear, useTts = false, useAvatar = false, onTtsChange, onAvatarChange} : ChatInputProps){
    const [input, setInput] = useState('')
    const [isListening, setIsListening] = useState(false)
    const [sttSupported, setSttSupported] = useState(false)
    const recognitionRef = useRef<any>(null)

    // Inicializar Web Speech API
    useEffect(() => {
        const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition

        if (SpeechRecognition) {
            setSttSupported(true)
            const recognition = new SpeechRecognition()
            recognition.lang = 'es-ES'
            recognition.continuous = true  // Cambiado a true para seguir escuchando
            recognition.interimResults = true  // Mostrar resultados parciales
            recognition.maxAlternatives = 1

            recognition.onresult = (event: any) => {
                // Obtener el último resultado
                const lastResultIndex = event.results.length - 1
                const transcript = event.results[lastResultIndex][0].transcript
                const isFinal = event.results[lastResultIndex].isFinal

                console.log('[STT] Transcripción:', transcript, 'Final:', isFinal)

                // Actualizar el input con el resultado (final o provisional)
                setInput(transcript)
            }

            recognition.onerror = (event: any) => {
                console.error('[STT] Error en reconocimiento de voz:', event.error)
                if (event.error === 'no-speech') {
                    console.warn('[STT] No se detectó voz')
                }
                setIsListening(false)
            }

            recognition.onend = () => {
                console.log('[STT] Reconocimiento finalizado')
                setIsListening(false)
            }

            recognition.onstart = () => {
                console.log('[STT] Reconocimiento iniciado')
            }

            recognition.onspeechstart = () => {
                console.log('[STT] Voz detectada')
            }

            recognition.onspeechend = () => {
                console.log('[STT] Fin de voz detectado')
            }

            recognitionRef.current = recognition
        } else {
            setSttSupported(false)
            console.warn('Web Speech API no soportada en este navegador')
        }

        return () => {
            if (recognitionRef.current) {
                recognitionRef.current.abort()
            }
        }
    }, [])

    const handleSend = () => {
        if(input.trim() && !disabled){
            onSend(input.trim())
            setInput('')
        }
    }

    const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
       if(e.key === 'Enter' && !e.shiftKey) {
         e.preventDefault()
         handleSend()
       }
    }

    const toggleListening = () => {
        if (!recognitionRef.current || disabled) return

        if (isListening) {
            recognitionRef.current.stop()
            setIsListening(false)
        } else {
            try {
                // Reiniciar el input antes de empezar
                setInput('')
                recognitionRef.current.start()
                setIsListening(true)
                console.log('[STT] Iniciando grabación - HABLA AHORA')
            } catch (error) {
                console.error('[STT] Error al iniciar reconocimiento:', error)
                setIsListening(false)
            }
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
                      onChange = {(e) => onTtsChange?.(e.target.checked)}
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
                      onChange = {(e) => onAvatarChange?.(e.target.checked)}
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
                  placeholder={placeholder || (isListening ? "Escuchando..." : "Escribe o habla tu consulta médica...")}
                  disabled = {disabled}
                  className = "flex-1 px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                />
                {/* Botón de micrófono (STT) */}
                {sttSupported && (
                    <button
                      onClick = {toggleListening}
                      disabled = {disabled}
                      className = {`px-4 py-3 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 font-medium flex items-center gap-2 ${
                        isListening
                          ? 'bg-red-500 text-white hover:bg-red-600 animate-pulse'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      }`}
                      title={isListening ? "Detener grabación" : "Grabar por voz"}
                    >
                      {isListening ? <MicOff className = "w-5 h-5" /> : <Mic className = "w-5 h-5" />}
                    </button>
                )}
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
