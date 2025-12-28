import os

# Nombre de la carpeta de destino (la misma que antes)
OUTPUT_FOLDER = "./dataset_respiratorio_es"

# Contenido optimizado de los nuevos 4 archivos
files_data = {
    "tos_ferina.txt": """# TOS FERINA (COQUELUCHE): GUÍA DEL PACIENTE

## ¿Qué es?
Es una infección bacteriana muy contagiosa conocida como la "tos de los 100 días". Causa ataques de tos violentos e incontrolables que pueden dificultar la respiración. Es **extremadamente peligrosa en bebés**.

## Síntomas (Fases)
1. **Inicio (1-2 semanas):** Parece un resfriado común (moqueo, fiebre leve).
2. **Ataques (Semana 2 en adelante):**
   * Tos rápida y violenta seguida de un sonido de "gallo" o silbido al intentar tomar aire (**Whoop**).
   * Vómitos después de toser.
   * Agotamiento extremo tras el ataque.

## ¡ALERTA EN BEBÉS! (Emergencia)
Los bebés menores de 6 meses a menudo **NO tosen**. En su lugar, pueden presentar:
* **Apnea:** Dejan de respirar por segundos.
* **Cianosis:** Se ponen azules o morados.
* Si ve esto, **vaya a Urgencias de inmediato**.

## Tratamiento y Prevención
* **Antibióticos:** Matan la bacteria y reducen el contagio, pero la tos puede durar semanas porque el daño en las vías respiratorias tarda en sanar.
* **Vacunación (La Clave):** Es vital que las embarazadas se vacunen (vacuna Tdap) en cada embarazo para pasar defensas al bebé antes de nacer.""",

    "tuberculosis.txt": """# TUBERCULOSIS (TB): GUÍA DEL PACIENTE

## ¿Qué es?
Una infección bacteriana grave que ataca principalmente los pulmones. Se transmite por el aire (al toser o hablar), no por compartir platos o ropa.

## Dos Tipos de TB (Muy Importante)
1. **TB Latente ("Dormida"):** Tiene la bacteria pero **no está enfermo** y **no contagia**. Necesita tratamiento preventivo para que no se "despierte" en el futuro.
2. **TB Activa ("Enferma"):** La bacteria está atacando y **sí contagia**.

## Síntomas de TB Activa
* **Tos intensa** que dura más de 3 semanas.
* **Tos con sangre** o flema.
* Dolor en el pecho.
* **Sudores nocturnos** (empapar las sábanas).
* Pérdida de peso sin motivo y fiebre.

## Tratamiento (Regla de Oro)
Se trata con antibióticos durante **6 a 9 meses**.
* **¡PELIGRO!** Si deja de tomar las pastillas porque "ya se siente bien", la bacteria se vuelve fuerte (resistente) y la enfermedad puede regresar siendo **mortal e in-curable**. Debe terminar el tratamiento completo.""",

    "sinusitis.txt": """# SINUSITIS (CONGESTIÓN DE LOS SENOS PARANASALES)

## ¿Qué es?
Es la inflamación de los huecos llenos de aire detrás de la frente y los pómulos (senos). Generalmente ocurre después de un resfriado.
* **Aguda:** Dura menos de 4 semanas.
* **Crónica:** Dura más de 12 semanas.

## Síntomas Clave
* **Dolor o presión facial:** En la frente, ojos o dientes, que empeora al inclinarse hacia adelante.
* **Nariz tapada** y moco espeso (amarillo o verde).
* Pérdida del olfato.

## Tratamiento en Casa
La mayoría (98%) son virales y **no necesitan antibióticos**.
1. **Lavados Nasales:** Use agua salina (suero) para limpiar el moco.
2. **Vapor:** Respire vapor de agua caliente.
3. **Analgésicos:** Ibuprofeno o Paracetamol para el dolor facial.
4. **Descongestionantes:** Úselos máximo 3 días (si se usan más, empeoran la congestión).

## Cuándo ver al médico
* Si los síntomas duran **más de 10 días** sin mejorar.
* Si tiene fiebre alta.
* **Emergencia:** Si tiene hinchazón/rojez alrededor de los ojos, visión doble o dolor de cabeza severo y rigidez en el nuca.""",

    "sleep_apnea.txt": """# APNEA OBSTRUCTIVA DEL SUEÑO (AOS)

## ¿Qué es?
Es un trastorno donde **deja de respirar** repetidamente mientras duerme porque su garganta se cierra. Esto baja el oxígeno en sangre y fragmenta su sueño, impidiendo el descanso.

## Síntomas (Lo que nota su pareja)
* **Ronquidos fuertes.**
* **Pausas en la respiración** seguidas de un resoplido o jadeo (como si se ahogara).
* **Somnolencia excesiva** durante el día (riesgo de dormirse conduciendo).
* Despertarse con boca seca o dolor de cabeza.

## Tratamiento Principal: CPAP
La máquina CPAP envía aire a presión a través de una mascarilla para mantener la garganta abierta.
* **Es el tratamiento más efectivo.**
* **Consejo:** Úsela toda la noche, todas las noches. Si le molesta, consulte con su médico para ajustar la mascarilla, pero no la abandone (protege su corazón).

## Cambios de Estilo de Vida
* **Bajar de peso:** A menudo mejora mucho la apnea.
* **Dormir de lado:** Evita que la lengua caiga hacia atrás.
* **Evitar el alcohol y sedantes:** Relajan la garganta y empeoran los paros respiratorios."""
}

# Crear carpeta si no existe
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
    print(f"📁 Carpeta verificada: {OUTPUT_FOLDER}")

# Escribir archivos
for filename, content in files_data.items():
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Archivo añadido/actualizado: {filename}")
    except Exception as e:
        print(f"❌ Error escribiendo {filename}: {e}")

print("\n🎉 ¡Todos los archivos han sido procesados e integrados!")