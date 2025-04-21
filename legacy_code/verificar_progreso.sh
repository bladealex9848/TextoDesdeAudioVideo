#!/bin/bash

# Contar videos en cada directorio
ORIGINALES=$(find videos_originales -name "*.mp4" | wc -l)
CONVERTIDOS=$(find videos_convertidos -name "*_car_compatible.mp4" | wc -l)

# Calcular porcentaje de progreso
TOTAL=$((ORIGINALES + CONVERTIDOS))
PORCENTAJE=$((CONVERTIDOS * 100 / TOTAL))

echo "=== PROGRESO DE CONVERSIÓN ==="
echo "Videos originales restantes: $ORIGINALES"
echo "Videos convertidos: $CONVERTIDOS"
echo "Total de videos: $TOTAL"
echo "Progreso: $PORCENTAJE%"
echo "==============================="

# Listar los últimos 5 videos convertidos
echo ""
echo "Últimos videos convertidos:"
ls -lt videos_convertidos/ | grep "_car_compatible.mp4" | head -5
