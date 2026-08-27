# 06 Instrucciones Autorizacion Maker Checker

6. Instrucciones y Autorización (Maker-Checker)
Documentos relacionados: 00_arquitectura_modulos_sistema.md  (módulo 6, requerido
para la primera operación) · 03_patrimonio_bienes_valuacion.md  y
04_cuentas_estructura_validaciones.md  (toda instrucción ejecutada genera
movimientos_patrimonio ) · 05_gobernanza_comite_tecnico.md  (instrucciones de origen
colegiado) · 09_documentos_repositorio.md  (NOM-151 y ﬁrma electrónica) ·
10_auditoria_trazabilidad.md .
1. Marco legal
CUB, Título Cuarto y Capítulo V Bis: exige separación de funciones a nivel del motor de ﬂujo —
ninguna operación de egreso o modiﬁcación contractual se ejecuta en un solo paso (principio
Maker-Checker / Control Dual).
Regla de inviolabilidad #2 (perﬁl de sistema): ninguna instrucción de salida de fondos o
cambio contractual puede ejecutarse con la autorización de un solo usuario.
Regla de inviolabilidad #3: ninguna operación puede ejecutarse sin estar vinculada a una
Carta de Instrucción o Acta de Comité ﬁrmada con e.ﬁrma/NOM-151.
Art. 89, Código de Comercio: validez jurídica de la Firma Electrónica Avanzada.
NOM-151-SCFI: conservación de mensajes de datos con sello de tiempo de un PSC
autorizado.
2. Principio de diseño
Este es el módulo que ejecuta operaciones sobre el patrimonio (documento 3) y las cuentas
(documento 4) — ningún otro módulo debe permitir modiﬁcar saldos directamente. El ﬂujo replica
exactamente el deﬁnido en el manual normativo: Maker →  Validación de sistema →  Checker →
Delegado Fiduciario (autorizador ﬁnal) →  Ejecución →  Evidencia NOM-151.
CAPTURISTA (Maker)  →   VALIDACIÓN SISTEMA  →   OFICIAL FIDUCIARIO (Checker)  →
DELEGADO FIDUCIARIO (Autorizador final)
   Crea la               PLD, saldo,              Revisa documentación
Firma con e.firma/token
   instrucción            reglas de bloqueo         y aprueba flujo

│

▼

EJECUCIÓN API + PÓLIZA CONTABLE

│

▼

                                                                    GENERACIÓN
DE EVIDENCIA NOM-151 + AUDIT TRAIL
3. Modelo de datos — instrucciones
Campo Descripción Tipo de dato Obligatorio Regla / valida
id_instruccion Identiﬁcador único Numérico Sí Autogenerado
numero_fideicomiso Fideicomiso afectado Relación (FK) Sí —
tipo_instruccion
Naturaleza de la
instrucción Catálogo Sí
Egreso / aport
cambio contra
origen_instruccion Fuente que la origina Catálogo Sí
Carta de instru
parte facultad
comité técnico
id_acta_origen
Acta de comité que la
sustenta, si
origen_instruccion
= acta_comite
Relación (FK
—
documento
5)
Condicional
Debe tener
estatus_act
válida
monto  / moneda
Monto e importe de la
instrucción
Numérico /
catálogo
Sí (si aplica
a egreso o
aportación)
—
descripcion
Detalle de la
instrucción
Texto Sí —
estatus_instruccion
Estado en el ﬂujo
Maker-Checker Catálogo Sí Ver máquina d
sección 4
usuario_maker  /
fecha_captura
Quién y cuándo
capturó
Usuario /
fecha
Sí —
usuario_checker  /
fecha_checker
Quién y cuándo revisó Usuario /
fecha
Condicional
Obligatorio a p
estatus =
validada_si
usuario_delegado  /
fecha_autorizacion
Delegado ﬁduciario
que autoriza en
deﬁnitiva
Usuario /
fecha Condicional
Obligatorio a p
estatus =
aprobada_ch
usuario debe t
Delegado_Fi
con poderes v
tokenizados

Campo Descripción Tipo de dato Obligatorio Regla / valida
documento_soporte
Carta de instrucción u
otro respaldo
Relación (FK
—
documento
9)
Sí —
digital_signature_hash
/ nom151_timestamp
Evidencia de ﬁrma
electrónica avanzada
del autorizador ﬁnal
Alfanumérico
Sí, a partir
de
ejecución
—
motivo_rechazo
Razón de rechazo, si
aplica Texto Condicional
Obligatorio si
estatus_ins
= rechazada
cualquier etap
4. Máquina de estados de estatus_instruccion
Estatus Descripción Quién puede transicionar
capturada Instrucción creada por el Maker Capturista
validada_sistema
Pasó las validaciones automáticas
(PLD, saldo, reglas de negocio)
Sistema (automático)
rechazada_sistema Falló alguna validación automática
Sistema (automático) —
regresa al Maker con motivo
aprobada_checker
El Oﬁcial Fiduciario revisó
documentación y aprobó Checker (≠ Maker)
rechazada_checker El Checker rechazó
Checker — regresa al Maker
con motivo
autorizada_delegado
El Delegado Fiduciario ﬁrmó con
e.ﬁrma/token
Delegado Fiduciario (≠
Maker, ≠ Checker)
ejecutada
Dispersión/asiento contable
ejecutado
Sistema (automático, tras
autorización)
cancelada
Cancelada antes de ejecución, con
motivo
Maker o Checker, mientras
no esté ejecutada
Regla de negocio: usuario_maker , usuario_checker  y usuario_delegado  deben ser tres
usuarios distintos — el sistema debe bloquear a nivel de base de datos, no solo de interfaz,
cualquier intento de que la misma persona ocupe dos roles en la misma instrucción.
5. Validaciones automáticas obligatorias (etapa "Validación
Sistema")

Replican el árbol de decisión del manual normativo (sección 7):
1. estatus_fideicomiso = vigente  (documento 1.1) — si no, rechazo automático.
2. Expediente KYC de las partes involucradas en estatus aprobado  (documento 2) — si no,
rechazo por incumplimiento PLD.
3. Consulta en tiempo real a listas de bloqueo (documento 2, sección 4) — coincidencia
conﬁrmada congela la instrucción y genera alerta UIF (documento 8).
4. Operación dentro del perﬁl transaccional esperado (documento 8) — si excede el umbral, se
escala como alerta de inusualidad, no se rechaza automáticamente.
5. Saldo disponible en la cuenta/bien afectado (documentos 3 y 4) suﬁciente para el monto
instruido.
6. Veriﬁcación de que la instrucción no constituye autocontratación no autorizada (documento 4,
sección 5) ni promesa de rendimiento garantizado (documento 1, sección 1.1).
Vacíos funcionales abiertos
1. SLA por etapa: no hay un plazo máximo deﬁnido para que una instrucción permanezca en
validada_sistema  o aprobada_checker  sin que el Checker o el Delegado actúen — riesgo
de instrucciones "atoradas" indeﬁnidamente, similar al vacío ya señalado para el estatus
suspendido  (documento 1.1).
2. Reintento tras rechazo: falta deﬁnir si una instrucción rechazada por el Checker puede
corregirse y reingresar como la misma instrucción (con historial de rechazo) o si
obligatoriamente debe capturarse como una instrucción nueva.
3. Delegados con poderes limitados por monto: el manual establece que el Delegado debe tener
poderes notariales vigentes y tokenizados, pero no se ha modelado si existen límites de
monto por delegado (facultades escalonadas) — pendiente de conﬁrmar con el área legal si
aplica en la práctica de la institución.
