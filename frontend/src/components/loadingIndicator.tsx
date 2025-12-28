/**
 * Indicador de carga mientras procesa la respuesta
 */

export function LoadingIndicator() {
    return (
        <div className = "flex items-center gap-3 bg-blue-50 text-blue-700 px-4 py-3 rounded-lg animate-slideIn">
            <div className = "flex gap-1">
                {[0,1,2].map((i) => (
                 <div 
                 key = {i}
                 className = "w-2 h-2 bg-blue-500 rounded-full animate-bounce"
                 style = {{animationDelay : `${i * 0.15}s`}}
                 />))
                }
            </div>
            <span className = "text-sm font-medium">
                Generando respuesta...    
            </span> 
        </div>
    )
}