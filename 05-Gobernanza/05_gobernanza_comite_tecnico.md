# 05 Gobernanza Comite Tecnico

5. Gobernanza y Comité Técnico
Documentos relacionados: 00_arquitectura_modulos_sistema.md  (módulo 5,
condicionalmente bloqueante) · 02_participantes_roles_kyc.md  (campo comite_tecnico
en el ﬁdeicomiso, rol miembro_comite_tecnico  en fideicomiso_partes ) ·
06_instrucciones_autorizacion_maker_checker.md  (las instrucciones de comité alimentan
este módulo) · 02.1_beneficiario_controlador.md  (el control del comité es criterio 2 de
determinación de beneﬁciario controlador).
1. Marco legal
LIC, Art. 80: el Comité Técnico es el órgano colegiado que instruye al ﬁduciario conforme a lo
establecido en el contrato.
Las instrucciones emanadas de un Comité Técnico requieren la carga del acta ﬁrmada o la
validación por ﬁrma electrónica avanzada de los miembros con quórum legal veriﬁcado.
2. Principio de diseño
Este módulo es condicional: solo aplica a ﬁdeicomisos donde comite_tecnico = verdadero
(documento 2). Cuando aplica, ninguna instrucción atribuida al comité es válida sin un acta que
acredite quórum suﬁciente — el comité no es un campo informativo, es una fuente de
instrucciones con su propia validación de legitimidad.
3. Modelo de datos — comites_tecnicos
Campo Descripción Tipo de
dato
Obligatorio Regla /
validación
id_comite
Identiﬁcador
único Numérico Sí Autogenerado
numero_fideicomiso
Fideicomiso
al que
pertenece
Relación
(FK) Sí
Único por
ﬁdeicomiso
(un comité
técnico por
contrato,
salvo que el
contrato
indique lo
contrario)
umbral_quorum_contratado Porcentaje
de quórum
exigido por
el contrato
Numérico
(%)
Sí Deﬁnido en el
documento
constitutivo;
no editable sin

Campo Descripción Tipo de
dato
Obligatorio Regla /
validación
convenio
modiﬁcatorio
fecha_constitucion_comite
Fecha de
instalación
formal del
comité
Fecha Sí —
estatus_comite
Estado
operativo Catálogo Sí
activo  /
inactivo
4. Modelo de datos — miembros_comite
Se apoya en fideicomiso_partes  (documento 2) para la identidad y el expediente KYC; aquí se
especiﬁca el detalle propio de la membresía en el comité.
Campo Descripción Tipo de
dato Obligatorio Regla / validación
id_membresia Identiﬁcador único Numérico Sí Autogenerado
id_comite
Comité al que
pertenece
Relación
(FK)
Sí —
id_relacion
Relación persona-rol en
fideicomiso_partes
(documento 2)
Relación
(FK) Sí
La persona debe tener rol
miembro_comite_tecnico
vigente
caracter
Calidad de la
membresía Catálogo Sí propietario  / suplente
cargo
Cargo dentro del
comité, si aplica
Texto No Ej. presidente, secretario
fecha_alta  /
fecha_baja
Vigencia de la
membresía Fecha Sí (alta) /
No (baja)
Mismo principio de no
sobrescritura que
fideicomiso_partes
5. Modelo de datos — actas_comite
Campo Descripción Tipo de dato Obligatorio
id_acta Identiﬁcador único Numérico Sí
id_comite Comité que sesionó Relación (FK) Sí
fecha_sesion Fecha de la sesión Fecha Sí

Campo Descripción Tipo de dato Obligatorio
asistentes_validados
Número de miembros propietarios
(o suplentes en su representación)
con asistencia validada
Numérico Sí
total_miembros_propietarios
Total de miembros propietarios
del comité a la fecha de la sesión
Numérico
(snapshot) Sí
quorum_calculado
asistentes_validados /
total_miembros_propietarios
Numérico (%,
derivado)
Sí
resultado_quorum
Si el quórum calculado alcanzó el
umbral contratado
Booleano
(derivado) Sí
acuerdos
Descripción de los acuerdos
tomados
Texto Sí
documento_acta
Acta ﬁrmada (repositorio
documental)
Relación (FK
—
documento
9)
Sí
metodo_validacion
Cómo se validó la legitimidad del
acta Catálogo Sí
digital_signature_hash  /
nom151_timestamp
Evidencia de ﬁrma electrónica
avanzada, si aplica Alfanumérico Condicional
estatus_acta Estado del acta Catálogo Sí
6. Validaciones críticas
Ninguna instrucción puede atribuirse a "Comité Técnico" sin un acta_comite con
estatus_acta = válida y resultado_quorum = verdadero.
Un acta con resultado_quorum = falso  no puede pasar a estatus_acta = válida  — los
acuerdos tomados sin quórum no tienen validez para efectos de instrucción, aunque el
documento pueda conservarse como registro histórico de la sesión.
Los suplentes solo cuentan para asistentes_validados  en representación formal de un
propietario ausente, no como voto adicional.
Vacíos funcionales abiertos
1. Carga extemporánea de actas: no hay regla sobre qué pasa si una instrucción se ejecuta
antes de que el acta que la sustenta esté formalmente cargada — ¿se permite con acta "en

trámite" y bloqueo de ejecución hasta regularizar, o se bloquea la instrucción por completo
desde el inicio?
2. Quórum de suplentes especíﬁco: falta deﬁnir si el contrato puede pactar un umbral de
quórum distinto cuando hay alta proporción de suplentes presentes, o si siempre se calcula
igual sin importar el carácter del asistente.
