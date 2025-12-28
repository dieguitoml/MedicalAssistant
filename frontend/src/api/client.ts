/**
 * Cliente HTTP para interactuar con el backend FastAPI
 * 
 */
import axios from 'axios'
import type {ChatRequest, ChatResponse, HealthResponse} from '../types/chat'


//Configurar cliente axios

const apiClient = axios.create({
    baseURL : 'http://localhost:8000',
    timeout : 1000000,
    headers : {
        'Content-Type' : 'application/json'
    }
})

/**
 * Enviar un mensaje al chat, el backend responderá con un ChatResponse
 */

export async function sendMessage(
    message : string,
    useTts : boolean,
    useAvatar : boolean
) : Promise<ChatResponse> {
    const request: ChatRequest = {
        message,
        use_tts : useTts,
        use_avatar : useAvatar
    }

    console.log('Sending request:', request) // Debug

    const response = await apiClient.post<ChatResponse>('/api/chat',request)
    return response.data
}  


/**
 * Verificar el estado de salud del backend
 */

export async function checkHealth() : Promise<HealthResponse> {
    const response = await apiClient.get<HealthResponse>('/api/health')
    return response.data
}

/**
 * Obtener ejemplos de preguntas del backend
 */

export async function getExamples() : Promise<string[]> {
    const response = await apiClient.get<{examples : string[]}>('/api/chat/examples')
    return response.data.examples
}

/**
 * Limpiar el chat
 */

export async function clearHistory() : Promise<void> {
    await apiClient.post('/api/chat/clear')
}