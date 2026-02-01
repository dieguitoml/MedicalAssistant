/**
 * Aplicación principal - Asistente Médico
 */

import { useEffect, useRef, useState } from 'react'
import {useChat} from './hooks/useChat'
import {Avatar} from './components/Avatar'
import {ChatInput} from './components/ChatInput'
import {LoadingIndicator} from './components/loadingIndicator'
import {ChatMessage} from './components/ChatMessage'
import {AlertCircle, Stethoscope} from 'lucide-react'

function App() {
  const { messages, loading, loadingMedia, error, currentVideo, currentAudio, send, clear} = useChat()
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const [useTts, setUseTts] = useState(false)
  const [useAvatar, setUseAvatar] = useState(false)
  
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({behavior: 'smooth'})
  },[messages])

  //Ejemplos de preguntas médicas
  const examples = [
    "¿Qué es el COVID-19?",
    "¿Cuáles son los síntomas de la faringitis?",
    "¿Cómo se trata el asma?"
  ]

  return (
        <div className="flex flex-col h-screen bg-gradient-to-br from-blue-50 via-white to-green-50">
          <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-xl p-6">
            <div className = "flex items-center gap-3">
              <Stethoscope className = "w-8 h-8" />
              <div>
                <h1 className = "text-3xl font-bold">
                  Asistente Médico Virtual
                </h1>
                <p className = "text-blue-100 mt-1">
                  Consulta sobre tus enfermedades respiratorias con IA
                </p>
              </div>
            </div>
          </header>
          <div className="flex-1 flex gap-6 p-6 overflow-hidden max-w-7xl mx-auto w-full">
            <div className="w-1/3 space-y-4">
              <Avatar
                videoUrl = {currentVideo}
                audioUrl = {currentAudio}
                isLoading = {loading}
              />
              <div className="bg-white border-l-4 border-blue-500 rounded-lg p-4 shadow-md">
                <div className="flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" />
                  <div className="text-sm text-gray-600">
                    <strong className="text-gray-800">ℹ️ Información:</strong>
                    <p className="mt-1">
                      Este asistente proporciona información educativa.
                      No reemplaza una consulta médica profesional.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex-1 flex flex-col bg-white rounded-2xl shadow-xl">
              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-6">
                {messages.length === 0 ? (
                  <div className="h-full flex flex-col items-center justify-center text-gray-400">
                    <div className="text-center mb-8">
                      <p className="text-lg mb-2">👋 ¡Hola!</p>
                      <p>Pregúntame sobre enfermedades respiratorias</p>
                    </div>

                    {/* Ejemplos de preguntas */}
                    <div className="w-full max-w-md">
                      <p className="text-sm font-medium text-gray-500 mb-3">
                        💡 Preguntas de ejemplo:
                      </p>
                      <div className="space-y-2">
                        {examples.map((example, i) => (
                          <button
                            key={i}
                            onClick={() => send(example, useTts, useAvatar)}
                            disabled={loading || loadingMedia}
                            className="
                              w-full text-left px-4 py-3 bg-blue-50 hover:bg-blue-100
                              text-blue-700 rounded-lg transition-colors text-sm
                              disabled:opacity-50 disabled:cursor-not-allowed
                            "
                          >
                            {example}
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                ) : (
                  <>
                    {messages.map((msg, idx) => (
                      <ChatMessage key={idx} message={msg} />
                    ))}

                    {loading && <LoadingIndicator />}

                    <div ref={messagesEndRef} />
                  </>
                )}

                {/* Error Message */}
                {error && (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-4 mt-4">
                    <p className="text-red-600 text-sm">❌ {error}</p>
                  </div>
                )}
              </div>

              {/* Chat Input */}
              <div className="border-t p-6 bg-gray-50">
            <ChatInput
              onSend={(msg) => send(msg, useTts, useAvatar)}
              disabled={loading || loadingMedia}
              useTts={useTts}
              useAvatar={useAvatar}
              onTtsChange={setUseTts}
              onAvatarChange={setUseAvatar}
            />

            {/* Clear button */}
            {messages.length > 0 && (
              <button
                onClick={clear}
                disabled={loading || loadingMedia}
                className="mt-3 text-sm text-gray-500 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                🗑️ Reiniciar conversación
              </button>
            )}
             </div>
           </div>
          </div>
          {/* Footer */}
        <footer className="bg-white border-t py-4">
          <div className="max-w-7xl mx-auto px-6">
           <p className="text-center text-sm text-gray-500">
             <strong className="text-amber-600">⚠️ Aviso:</strong>{' '}
             Información con fines educativos. Consulta con un profesional de salud.
           </p>
         </div>
        </footer>
        </div>
  )
}

export default App
