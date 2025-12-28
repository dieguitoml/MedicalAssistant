/**
 * Custom hook para gestionar el estado del chat
 */

import {useState} from 'react'
import {sendMessage} from '../api/client'
import type {Message} from '../types/chat'

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)
  const [currentVideo, setCurrentVideo] = useState<string | null>(null)
  const [currentAudio, setCurrentAudio] = useState<string | null>(null)


  /**
   * Enviar un mensaje
   */

  const send = async(content: string, useTts: boolean, useAvatar: boolean) => {
    if(!content.trim()) return

    console.log('useChat send:', { content, useTts, useAvatar }) // Debug

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
        const response = await sendMessage(content, useTts, useAvatar)

        //Mensaje del asistente
        const assitantMessage : Message = {
            role : 'assistant',
            content : response.text,
            timestamp : new Date(), // Usar fecha actual ya que el backend no devuelve timestamp
            audioUrl : response.audio_url || undefined,
            videoUrl : response.video_url || undefined
        }

        setMessages(prev => [...prev, assitantMessage])
        if(response.video_url){
            setCurrentVideo(response.video_url)
        }
        if(response.audio_url){
            setCurrentAudio(response.audio_url)
        }

    } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Error desconocido'
        setError(errorMessage)
        console.error('Error al enviar el mensaje:', err)

        //Mensaje de error
        const errorMsg: Message = {
            role : 'assistant',
            content : `❌ Error: ${errorMessage}. Por favor, intenta de nuevo.`,
            timestamp : new Date()
        }
        setMessages(prev => [...prev, errorMsg])
    } finally {
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
        error,
        currentVideo,
        currentAudio,
        send,
        clear
    }
}

