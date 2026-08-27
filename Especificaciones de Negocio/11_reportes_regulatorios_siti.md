# 11 Reportes Regulatorios Siti

11. Reportes Regulatorios (SITI-CNBV)
Documentos relacionados: 00_arquitectura_modulos_sistema.md  (módulo 11,
complementario) · 07_contabilidad_fiduciaria.md  (fuente de los saldos para
R01/R24) · 01_fideicomiso_estructura_campos_validaciones.md  (datos maestros
para el desglose de R24) · 08_pld_monitoreo_transaccional.md  (fuente de los
reportes PLD/UIF).
1. Marco legal
Sistema Interinstitucional de Transferencia de Información (SITI) de la CNBV: exige
archivos de texto plano o XML estructurados con periodicidad deﬁnida por serie.
Reporte SITI Periodicidad Contenido core
Serie R01 —
Catálogo
Mínimo
Mensual /
trimestral
Saldo de Cuentas de Orden (efectivo, inmuebles,
títulos)
Serie R24 —
Fideicomisos Trimestral
Desglose por número de contrato, sector, tipo
(tipo_regulatorio_snapshot , documento 1.2),
y número de partes
Reportes PLD
(UIF)
Mensual /
inmediato
Operaciones inusuales, relevantes (> $7,500 USD) y
en efectivo
2. Principio de diseño
Este módulo no genera datos propios — extrae y formatea información que ya existe en
Contabilidad (documento 7), el maestro del ﬁdeicomiso (documento 1) y PLD (documento
8). Su responsabilidad es el formato de salida exigido por SITI y la validación de
consistencia cruzada entre reportes antes de su envío.
3. Modelo de datos — reportes_generados
Campo Descripción Tipo de dato Obligatorio Regla / validación
id_reporte
Identiﬁcador
único Numérico Sí Autogenerado
tipo_reporte Serie SITI Catálogo Sí R01 / R24 / PLD-UIF

Campo Descripción Tipo de dato Obligatorio Regla / validación
periodo
Periodo que
cubre
Fecha
(mes/trimestre) Sí —
fecha_corte
Fecha de
corte de los
datos
Fecha Sí —
fecha_generacion
Fecha en
que se
generó el
archivo
Fecha Sí —
usuario_genera
Usuario que
ejecutó la
generación
Usuario Sí —
archivo_generado
Referencia
al archivo
(texto plano
/ XML)
Relación (FK —
documento 9)
Sí —
estatus_reporte
Estado del
ciclo de
envío
Catálogo Sí
generado  /
enviado  /
aceptado  /
rechazado
folio_acuse_siti
Folio de
acuse del
portal SITI
Alfanumérico Condicional
Obligatorio si
estatus_reporte
es aceptado  o
rechazado
motivo_rechazo
Detalle del
rechazo, si
aplica
Texto Condicional
Obligatorio si
estatus_reporte
= rechazado
4. Reglas de formato y consistencia (obligatorias antes de
generar el archivo)
Formato de cifras: valores en moneda nacional, moneda extranjera valorizada y UDIS
valorizadas a la fecha de corte, con dos decimales, sin comas ni símbolos.
Consistencia R24 ↔  R01: el acumulado del Reporte R24 debe coincidir exactamente a
nivel de centavos con el saldo asentado en las Cuentas de Orden del Reporte R01
(documento 7). El sistema debe ejecutar esta validación de forma bloqueante antes de
permitir marcar el reporte como generado  — un descuadre aquí anticipa el rechazo
automático que haría el propio portal SITI.

Vacíos funcionales abiertos
1. Proceso de corrección y reenvío: falta deﬁnir el ﬂujo cuando SITI rechaza un reporte —
¿se corrige y reenvía como el mismo id_reporte  con nueva versión, o se genera un
reporte nuevo con referencia al rechazado?
2. Calendario de cortes por tipo de reporte: falta la parametrización exacta de fechas
límite de envío por serie (día hábil especíﬁco del mes/trimestre siguiente al periodo).
3. Reporte PLD-UIF inmediato: a diferencia de R01/R24 (periódicos), el reporte de
operación inusual puede requerir envío inmediato — falta deﬁnir el SLA máximo desde
que se genera una alerta_pld  (documento 8) con estatus = reportada_uif  hasta
que el reporte formal debe estar enviado.
