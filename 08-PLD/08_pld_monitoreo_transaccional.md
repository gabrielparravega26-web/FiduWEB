# 08 Pld Monitoreo Transaccional

8. PLD y Monitoreo Transaccional continuo
Documentos relacionados: 00_arquitectura_modulos_sistema.md  (módulo 8, requerido
para la primera operación) · 02_participantes_roles_kyc.md  (KYC de alta, matriz de riesgo
y listas de bloqueo — este módulo cubre el monitoreo posterior, no la foto inicial) ·
06_instrucciones_autorizacion_maker_checker.md  (evalúa cada instrucción en curso).
1. Marco legal
Disposiciones de Carácter General del Art. 115 de la LIC (PLD/FT): identiﬁcación del cliente,
matriz de riesgo, monitoreo transaccional y reporte de operaciones inusuales/relevantes.
El expediente KYC (documento 2) cubre la identiﬁcación inicial; este módulo cubre la vigilancia
continua de las operaciones ya en curso.
2. Principio de diseño
Cada persona y cada ﬁdeicomiso tienen un perﬁl transaccional esperado — lo que es "normal"
para ellos. Toda instrucción (documento 6) se evalúa contra ese perﬁl antes y durante su
ejecución; una desviación signiﬁcativa no bloquea automáticamente la operación (a diferencia de
una coincidencia en lista negra), pero genera una alerta que un humano — el Oﬁcial de
Cumplimiento — debe resolver.
3. Modelo de datos — perfil_transaccional_esperado
Campo Descripción Tipo de
dato
Obligatorio Regla /
validación
id_perfil Identiﬁcador único Numérico Sí Autogenerado
numero_fideicomiso
Fideicomiso al que
aplica
Relación
(FK)
Sí —
monto_esperado_periodo
Monto esperado
de movimiento en
el periodo de
referencia
Numérico Sí
Declarado al
alta, ajustable
con revisión
frecuencia_esperada
Número de
operaciones
esperadas en el
periodo
Numérico Sí —
periodo_referencia
Unidad de tiempo
del perﬁl Catálogo Sí
Mensual /
trimestral

Campo Descripción Tipo de
dato
Obligatorio Regla /
validación
fecha_ultima_revision
Última vez que se
recalculó/conﬁrmó
el perﬁl
Fecha Sí
Sujeto a la
misma
periodicidad
de revisión de
riesgo del
documento 2
4. Modelo de datos — alertas_pld
Campo Descripción Tipo de
dato Obligatorio Regla / validación
id_alerta
Identiﬁcador
único
Numérico Sí Autogenerado
numero_fideicomiso
Fideicomiso
relacionado
Relación
(FK) Sí —
id_instruccion
Instrucción
que generó la
alerta, si
aplica
Relación
(FK —
documento
6)
Condicional —
tipo_alerta
Naturaleza de
la alerta Catálogo Sí
Operación inusual
/ operación
relevante (≥ $7,50
USD) / operación
en efectivo /
coincidencia en
lista de bloqueo
motivo
Descripción
de por qué se
generó
Texto Sí
Ej. "monto excede
perﬁl esperado en
45%"
fecha_generada
Fecha de la
alerta
Fecha Sí —
estatus_alerta
Estado de
atención
Catálogo Sí
pendiente  /
en_revision  /
descartada  /
reportada_uif
usuario_oficial_cumplimiento
Quién la
atiende Usuario Condicional
Obligatorio a parti
de en_revision
fecha_resolucion Fecha de
cierre de la
Fecha Condicional Obligatoria si
estatus_alerta

Campo Descripción Tipo de
dato
Obligatorio Regla / validación
alerta es descartada
reportada_uif
justificacion_resolucion
Motivo
documentado
de la
resolución
Texto Sí (al
resolver)
No se puede cerra
una alerta sin
justiﬁcación
escrita
5. Reglas de negocio
Alertamiento por desviación: si una instrucción supera el monto_esperado_periodo
(prorrateado) en más de 30%, o la frecuencia_esperada  en la misma proporción, se genera
automáticamente una alerta_pld  de tipo operación inusual  y la instrucción asociada se
congela en el ﬂujo del documento 6 hasta que la alerta se resuelva.
Operaciones relevantes: toda operación en efectivo o transferencia que supere $7,500 USD (o
su equivalente) genera automáticamente una alerta de tipo operación relevante ,
independientemente de si se desvía o no del perﬁl esperado.
Coincidencia en listas de bloqueo (documento 2, sección 4): genera alerta_pld  de máxima
severidad y congela no solo la instrucción, sino todas las operaciones pendientes de esa
persona hasta resolución del Oﬁcial de Cumplimiento.
Ninguna alerta se autorresuelve por only paso del tiempo — requiere acción y justiﬁcación
humana documentada.
Vacíos funcionales abiertos
1. Determinación inicial del perﬁl transaccional esperado: no está deﬁnido si se captura como
declaración del cliente al alta, se calcula con datos históricos tras los primeros meses de
operación, o es un híbrido — esto afecta directamente qué tan conﬁable es la alerta desde el
día uno.
2. Revisión periódica del perﬁl: falta amarrar la periodicidad de recálculo del perﬁl a la matriz de
riesgo del documento 2 (sección 3), de forma análoga a la vigencia de expediente KYC.
3. Reporte formal a la UIF: el estatus reportada_uif  existe como marcador, pero falta el
modelo de datos del reporte formal en sí (folio, fecha de envío, acuse) — probablemente debe
vivir en el documento 11 (Reportes Regulatorios) y conectarse aquí por referencia.
