//Aquí definimos los tipos relacionados con el chat 

export interface Message {
    role : 'user' | 'assistant'
    content : string
    timestamp : Date
    audioUrl? : string
    videoUrl? : string
}

export interface ChatRequest {
    message : String
    use_tts : boolean
    use_avatar : boolean
}

export interface ChatResponse {
    text : string
    audio_url : string | null
    video_url : string | null
    processing_time : number
    timestamp : Date
}

export interface HealthResponse {
    status : string
    models_loaded : boolean
    services : {
        chat : boolean
        tts : boolean
        avatar : boolean
    }
}