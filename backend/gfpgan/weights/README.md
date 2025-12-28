# GFPGAN Weights

Los archivos de pesos de GFPGAN son demasiado grandes para incluirlos en el repositorio de GitHub (>100MB).

## Descargar los archivos necesarios:

Descarga estos archivos y colócalos en esta carpeta (`backend/gfpgan/weights/`):

1. **alignment_WFLW_4HG.pth** (184.70 MB)
   - Necesario para la detección facial y alineación

2. **detection_Resnet50_Final.pth** (104.43 MB)
   - Necesario para la detección de rostros

## Fuentes de descarga:

Puedes obtener estos archivos de:
- Repositorio oficial de GFPGAN: https://github.com/TencentARC/GFPGAN
- O desde el sistema de mejora de calidad facial que estés usando

## Estructura esperada:

```
backend/gfpgan/weights/
├── README.md (este archivo)
├── alignment_WFLW_4HG.pth
└── detection_Resnet50_Final.pth
```
