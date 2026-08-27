# 13 Notificaciones Alertas

13. Notiﬁcaciones y Alertas
Documentos relacionados: 00_arquitectura_modulos_sistema.md  (módulo 13,
complementario) · 01.1_gestion_estatus_contrato.md  (vacío abierto: escalación de
suspendido  prolongado — este módulo es el mecanismo natural para resolverlo) ·
02_participantes_roles_kyc.md  (vencimiento de expedientes) ·
08_pld_monitoreo_transaccional.md  (alertas PLD).
1. Marco legal
No deriva de un artículo especíﬁco — es un módulo de mitigación de riesgo operativo que
hace ejecutables, sin depender de revisión manual, las obligaciones de vigilancia que sí son
de origen legal (vigencia de KYC, resolución de alertas PLD, control de estatus contractual).
2. Principio de diseño
Este módulo es un motor de reglas que observa al resto del sistema y genera notiﬁcaciones
cuando se cumple una condición temporal o de umbral — no origina datos de negocio
propios, solo reacciona a ellos.
3. Modelo de datos — reglas_notificacion
Campo Descripción Tipo de
dato Obligatorio Regla / validación
id_regla
Identiﬁcador
único
Numérico Sí Autogenerado
tipo_evento
Condición
que dispara
la
notiﬁcación
Catálogo Sí
Vencimiento próximo de
expediente KYC / cambio
de
estatus_fideicomiso
/ alerta PLD generada /
documento próximo a
vencer / instrucción sin
resolver (Maker-Checker)
/ suspensión prolongada
sin resolución

Campo Descripción Tipo de
dato
Obligatorio Regla / validación
destinatario_rol
Rol que
debe recibir
la
notiﬁcación
Catálogo Sí
Oﬁcial de cumplimiento /
delegado ﬁduciario /
oﬁcial de relación /
administrador de
catálogos
canal
Medio de
envío
Catálogo Sí Sistema (bandeja
interna) / correo / SMS
anticipacion_dias
Días de
anticipación
antes del
evento, si
aplica
Numérico Condicional Obligatorio para eventos
de vencimiento
activo
Si la regla
está en
operación
Booleano Sí —
4. Modelo de datos — notificaciones_generadas
Campo Descripción Tipo de
dato
Obligatorio Regla /
validación
id_notificacion
Identiﬁcador
único Numérico Sí Autogenerado
id_regla
Regla que la
originó
Relación
(FK)
Sí —
numero_fideicomiso  /
id_persona
Entidad
relacionada
Relación
(FK)
Condicional
Al menos uno
de los dos
debe estar
presente
fecha_generada
Fecha de
generación Fecha Sí —
fecha_leida
Fecha en
que el
destinatario
la marcó
como
atendida
Fecha No —

Campo Descripción Tipo de
dato
Obligatorio Regla /
validación
estatus_notificacion Estado Catálogo Sí
pendiente
/ leida  /
escalada
5. Regla de escalación (propuesta para cerrar el vacío del
documento 1.1)
Si una notiﬁcación de tipo suspensión prolongada sin resolución  permanece
pendiente  más allá de un umbral conﬁgurable (ej. 30 días naturales desde que el
ﬁdeicomiso entró a suspendido ), el sistema debe generar automáticamente una segunda
notiﬁcación de mayor severidad (escalada ) dirigida a un rol jerárquicamente superior al
destinatario_rol  original — implementando así, de forma operativa, el límite de tiempo
que el documento 1.1 dejó pendiente de deﬁnir.
Vacíos funcionales abiertos
1. Integración real de canales: falta deﬁnir el proveedor/mecanismo técnico de envío de
correo y SMS — es una decisión de implementación, no de negocio, pero condiciona el
alcance de este módulo.
2. Umbral conﬁgurable de escalación: el ejemplo de 30 días en la sección 5 es una
propuesta inicial — falta validarlo con el área de cumplimiento como el plazo máximo
aceptable de negocio, no solo técnico.
3. Notiﬁcaciones al cliente externo (ﬁdeicomitente/ﬁdeicomisario): el diseño actual
asume destinatarios internos únicamente; falta deﬁnir si el sistema debe notiﬁcar
directamente a las partes del ﬁdeicomiso (ej. vencimiento de su propio expediente KYC)
o si ese contacto sigue un canal distinto fuera del sistema.
