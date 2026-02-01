/**
 * Custom hook para gestionar el estado del chat
 */

import {useState} from 'react'
import {sendMessage, generateMedia} from '../api/client'
import type {Message} from '../types/chat'

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState<boolean>(false)
  const [loadingMedia, setLoadingMedia] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)
  const [currentVideo, setCurrentVideo] = useState<string | null>(null)
  const [currentAudio, setCurrentAudio] = useState<string | null>(null)


  /**
   * Enviar un mensaje
   */

  const send = async(content: string, useTts: boolean, useAvatar: boolean) => {
    if(!content.trim()) return

    console.log('useChat send:', { content, useTts, useAvatar })

    //Mensaje del usuario
    const userMessage : Message = {
        role : 'user',
        content,
        timestamp : new Date()
    }
    setMessages(prev => [...prev, userMessage])
    setLoading(true)
    setError(null)

    try{
        // 1. Obtener texto primero (sin audio/video para respuesta rápida)
        const textResponse = await sendMessage(content, false, false)

        // 2. Mostrar texto inmediatamente
        const assistantMessage : Message = {
            role : 'assistant',
            content : textResponse.text,
            timestamp : new Date()
        }
        setMessages(prev => [...prev, assistantMessage])
        setLoading(false) // Quitar loading del texto

        // 3. Si se pidió audio/video, generarlo en segundo plano
        if (useTts || useAvatar) {
            setLoadingMedia(true)
            generateMedia(textResponse.text, useAvatar)
                .then(mediaResponse => {
                    // Actualizar el mensaje con las URLs de audio/video
                    setMessages(prev => prev.map((msg, idx) =>
                        idx === prev.length - 1 && msg.role === 'assistant'
                            ? {
                                ...msg,
                                audioUrl: mediaResponse.audio_url || undefined,
                                videoUrl: mediaResponse.video_url || undefined
                              }
                            : msg
                    ))

                    if (mediaResponse.video_url) {
                        setCurrentVideo(mediaResponse.video_url)
                    }
                    if (mediaResponse.audio_url) {
                        setCurrentAudio(mediaResponse.audio_url)
                    }
                })
                .catch(err => {
                    console.error('Error generando media:', err)
                })
                .finally(() => {
                    setLoadingMedia(false)
                })
        }

    } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Error desconocido'
        setError(errorMessage)
        console.error('Error al enviar el mensaje:', err)

        const errorMsg: Message = {
            role : 'assistant',
            content : `Error: ${errorMessage}. Por favor, intenta de nuevo.`,
            timestamp : new Date()
        }
        setMessages(prev => [...prev, errorMsg])
        setLoading(false)
    }
  }
  /**
 * Limpiar el chat
 */

    const clear = () => {
    setMessages([])
    setCurrentVideo(null)
    setCurrentAudio(null)
    setError(null)
    }
    return {
        messages,
        loading,
        loadingMedia,
        error,
        currentVideo,
        currentAudio,
        send,
        clear
    }
}

