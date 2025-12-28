/**
 * Componente del Avatar
 */

import {useEffect,useRef, useState} from 'react'

interface AvatarProps {
    videoUrl: string | null
    audioUrl: string | null
    isLoading?: boolean
}

// URL de la imagen del avatar estático (debe estar en la carpeta public)
const AVATAR_STATIC_IMAGE = '/avatar_doctor.png'

export function Avatar({videoUrl, audioUrl, isLoading} :AvatarProps){
    const videoRef = useRef<HTMLVideoElement>(null)
    const audioRef = useRef<HTMLAudioElement>(null)
    const [showVideo, setShowVideo] = useState(false)

    useEffect(() => {
        if(videoUrl && videoRef.current){
            // Ocultar video mientras carga
            setShowVideo(false)
            videoRef.current.load();

            // Mostrar video solo cuando esté listo para reproducir
            const handleCanPlay = () => {
                setShowVideo(true)
                videoRef.current?.play().catch(err => {
                    console.warn('Error auto-playing video:',err)
                })
            }

            videoRef.current.addEventListener('canplay', handleCanPlay)

            return () => {
                videoRef.current?.removeEventListener('canplay', handleCanPlay)
            }
        } else {
            // Si no hay video, asegurarse de mostrar la imagen
            setShowVideo(false)
        }
    }, [videoUrl])

    useEffect(() => {
        // Reproducir audio solo cuando no hay video pero sí hay audio (TTS sin Avatar)
        if(audioUrl && !videoUrl && audioRef.current){
            audioRef.current.load();
            audioRef.current.play().catch(err => {
              console.warn('Error auto-playing audio:',err)
            })
        }
    }, [audioUrl, videoUrl])

    return (
        <div className = "relative w-full h-[400px] bg-gradient-to-br from-blue-50 to-green-50 rounded-2xl overflow-hidden shadow-xl">
            {/* Imagen estática del avatar - siempre visible hasta que el video esté listo */}
            <img
                src={AVATAR_STATIC_IMAGE}
                alt="Avatar Médico"
                className={`w-full h-full object-cover transition-opacity duration-300 ${
                    showVideo ? 'opacity-0 absolute' : 'opacity-100'
                }`}
            />

            {/* Video del avatar - solo visible cuando está listo */}
            {videoUrl && (
                <video
                    ref={videoRef}
                    src={videoUrl}
                    className={`w-full h-full object-cover transition-opacity duration-300 ${
                        showVideo ? 'opacity-100' : 'opacity-0'
                    }`}
                    autoPlay
                    muted={false}
                />
            )}

            {/* Overlay de carga */}
            {isLoading && (
                <div className="absolute inset-0 bg-black bg-opacity-30 flex flex-col items-center justify-center">
                    <div className="relative mb-4">
                        <div className="w-16 h-16 rounded-full bg-white bg-opacity-20 animate-pulse" />
                        <div className="absolute inset-0 flex items-center justify-center">
                            <span className="text-3xl">⏳</span>
                        </div>
                    </div>
                    <p className="text-white font-medium">
                        Generando respuesta...
                    </p>
                    <p className="text-sm text-white text-opacity-80 mt-1">
                        Esto puede tomar 2-5 segundos
                    </p>
                </div>
            )}
        {videoUrl && (
        <div className="absolute bottom-4 right-4 bg-green-500 text-white px-3 py-1 rounded-full text-xs font-medium shadow-lg flex items-center gap-2">
          <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
          Hablando
        </div>
        )}
        {audioUrl && !videoUrl && (
        <div className="absolute bottom-4 right-4 bg-blue-500 text-white px-3 py-1 rounded-full text-xs font-medium shadow-lg flex items-center gap-2">
          <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
          Reproduciendo audio
        </div>
        )}
        {/* Audio element para reproducir TTS sin video */}
        {audioUrl && !videoUrl && (
          <audio ref={audioRef} src={audioUrl} />
        )}
        </div>
    )
}