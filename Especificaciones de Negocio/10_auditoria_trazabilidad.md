# 10 Auditoria Trazabilidad

10. Auditoría y Trazabilidad
Documentos relacionados: 00_arquitectura_modulos_sistema.md  (módulo 10, núcleo
bloqueante, transversal) · 01.1_gestion_estatus_contrato.md  (la tabla de auditoría de
cambios de estatus es una instancia especíﬁca de este esquema genérico — se recomienda
uniﬁcar). Todos los módulos escriben en este repositorio.
1. Marco legal
CUB, Capítulo V Bis: seguridad de la información y control interno. La bitácora de auditoría
debe ser Append-Only — sin permisos de UPDATE  ni DELETE  a nivel de motor de base de
datos, no solo a nivel de aplicación.
2. Principio de diseño
Este módulo es transversal: no pertenece a ningún ﬁdeicomiso ni módulo de negocio en particular,
sino que registra toda acción relevante ocurrida en cualquiera de los demás. La tabla de auditoría
de cambios de estatus deﬁnida en el documento 1.1 debe considerarse un caso de uso especíﬁco
de este esquema genérico, no una tabla independiente — se recomienda que ese módulo
consuma esta tabla central en vez de mantener su propio esquema paralelo.
3. Modelo de datos — bitacora_auditoria
Campo Descripción Tipo de dato Obligatorio Regla / validación
audit_id
Identiﬁcador
único del evento
(UUID)
Alfanumérico Sí —
timestamp_utc
Fecha y hora del
evento en UTC Fecha-hora Sí —
numero_fideicomiso
Fideicomiso
relacionado, si
aplica
Relación (FK) Condicional
Nulo para eventos a n
sistema o de persona
ﬁdeicomiso asociado
user_id
Usuario que
ejecutó la
acción
Relación (FK) Sí —
user_role
Rol del usuario
al momento de
la acción
Catálogo
(snapshot) Sí No se recalcula si el
usuario cambia desp
action_type Tipo de acción Catálogo Sí Ej. CHANGE_ESTATUS
APPROVE_DISBURSE

Campo Descripción Tipo de dato Obligatorio Regla / validación
CREATE_PERSONA ,
UPDATE_CATALOGO
resource_affected
Recurso/entidad
afectada Texto Sí Ej.
Instruccion_Oper
resource_id
Identiﬁcador del
recurso
afectado
Alfanumérico Sí —
ip_address IP de origen Alfanumérico Sí —
digital_signature_hash
Hash de ﬁrma
electrónica, si la
acción requirió
autorización
ﬁrmada
Alfanumérico Condicional
Obligatorio para acci
pasan por el módulo
(Instrucciones)
state_before
Estado del
recurso antes
de la acción
JSON Sí —
state_after
Estado del
recurso después
de la acción
JSON Sí —
4. Reglas de negocio
Append-Only real, no solo por convención de aplicación: los permisos de escritura a nivel de
motor de base de datos deben excluir UPDATE  y DELETE  sobre esta tabla para cualquier rol,
incluyendo administradores de base de datos — la inmutabilidad debe ser estructural, no solo
procedimental.
Cobertura universal: cualquier módulo que modiﬁque un dato regulado (estatus, montos,
expedientes KYC, catálogos, instrucciones) debe escribir en esta bitácora como parte de la
misma transacción que ejecuta el cambio — no como proceso asíncrono separado que pueda
fallar silenciosamente.
Consulta, no edición: la interfaz de usuario sobre esta tabla es exclusivamente de
lectura/búsqueda; no expone ninguna operación de escritura manual.
Vacíos funcionales abiertos
1. Retención y archivado a largo plazo: una bitácora Append-Only de un sistema en producción
por años puede volverse muy grande — falta deﬁnir una estrategia de archivado en frío que
preserve la inmutabilidad (ej. exportación ﬁrmada a almacenamiento WORM) sin
comprometer el rendimiento de consultas recientes.
2. Uniﬁcación con la tabla de auditoría de estatus (documento 1.1): falta la migración/decisión
formal de consolidar ambos esquemas — actualmente coexisten con campos casi idénticos.

3. Acceso de auditoría externa (CNBV/auditor): no se ha deﬁnido si existe un rol de solo lectura
para auditores externos con alcance limitado a un ﬁdeicomiso o periodo especíﬁco.
