# 09 Documentos Repositorio

9. Documentos y Repositorio
Documentos relacionados: 00_arquitectura_modulos_sistema.md  (módulo 9, núcleo
bloqueante) · Es el repositorio referenciado por documento_constitutivo  (doc 1),
documento_soporte  (docs 1.1, 2, 2.1, 3, 4, 5, 6), y actas (doc 5).
1. Marco legal
Art. 89, Código de Comercio: las autorizaciones operativas y cartas de instrucción
digitales tienen plena validez jurídica si cumplen con la Firma Electrónica Avanzada.
NOM-151-SCFI: para cada documento/instrucción ﬁrmado digitalmente, se requiere
constancia de conservación de mensajes de datos con sello de tiempo (Timestamping)
de un PSC (Proveedor de Servicios de Certiﬁcación) autorizado por la Secretaría de
Economía.
2. Principio de diseño
Este módulo es el repositorio único al que todos los demás módulos apuntan vía
documento_soporte  — no debe existir almacenamiento de archivos disperso o duplicado en
otros módulos. Todo documento contractual (constitutivo, convenios modiﬁcatorios) se
versiona; nunca se sobrescribe un documento vigente, se marca histórico y se sube la nueva
versión.
3. Modelo de datos — documentos
Campo Descripción Tipo de dato Obligatorio Regla / validación
id_documento
Identiﬁcador
único Numérico Sí Autogenerado
numero_fideicomiso
Fideicomiso
relacionado,
si aplica
Relación (FK) Condicional
Nulo para
documentos a nivel
de persona
(identiﬁcaciones,
comprobantes KYC)
id_persona
Persona
relacionada,
si aplica
Relación (FK
—
documento
2)
Condicional
Nulo para
documentos a nivel
de ﬁdeicomiso
tipo_documento Clasiﬁcación
del
Catálogo Sí Contrato constitutivo
/ convenio

Campo Descripción Tipo de dato Obligatorio Regla / validación
documento modiﬁcatorio / acta
de comité /
identiﬁcación oﬁcial /
comprobante de
domicilio / carta de
instrucción / otro
version
Número de
versión Numérico Sí
Incremental; solo la
versión más reciente
puede tener
estatus_documento
= vigente
fecha_carga  /
usuario_carga
Trazabilidad
de carga
Fecha /
usuario
Sí —
hash_archivo
Hash del
archivo para
integridad
Alfanumérico Sí
Permite detectar
alteraciones
posteriores al archivo
original
nom151_timestamp
Sello de
tiempo
NOM-151, si
el
documento
requiere
ﬁrma
electrónica
avanzada
Alfanumérico Condicional
Obligatorio para
cartas de instrucción,
actas con ﬁrma
electrónica, y
convenios
modiﬁcatorios
psc_proveedor
Proveedor
de Servicios
de
Certiﬁcación
que emitió
el sello
Catálogo Condicional
Obligatorio junto con
nom151_timestamp
estatus_documento
Estado del
documento Catálogo Sí
vigente  /
historico  /
vencido
fecha_vencimiento
Fecha de
vencimiento,
si aplica
Fecha Condicional
Obligatorio para
documentos con
vigencia deﬁnida
(identiﬁcaciones,
comprobantes de
domicilio)

4. Reglas de negocio
No hard delete: ningún documento se elimina físicamente. Un documento reemplazado
pasa a historico , nunca se borra.
Documento constitutivo y convenios modiﬁcatorios son inmutables una vez cargados —
cualquier corrección se hace mediante una nueva versión con su propio
documento_soporte  de origen (ej. el convenio modiﬁcatorio que ampara el cambio),
nunca editando el archivo existente.
Vinculación obligatoria: ningún módulo debe permitir capturar un documento_soporte
que no exista como registro en esta tabla — se referencía por id_documento , no se sube
archivo de forma independiente dentro de otros módulos.
Vacíos funcionales abiertos
1. Política de retención documental: falta deﬁnir cuántos años deben conservarse los
documentos tras la extinción de un ﬁdeicomiso — normalmente existen plazos mínimos
ﬁscales y de conservación mercantil que deben conﬁrmarse con el área legal antes de
permitir cualquier purga o archivado en frío.
2. Formatos aceptados y límites de tamaño: no especiﬁcado — depende de la
infraestructura de almacenamiento que se deﬁna en la fase de implementación técnica.
3. Firma electrónica de terceros externos (ej. ﬁdeicomitente ﬁrma la carta de instrucción
fuera del sistema): falta deﬁnir cómo se integra o valida una ﬁrma electrónica avanzada
generada en una plataforma externa (PSC de terceros) contra este repositorio.
