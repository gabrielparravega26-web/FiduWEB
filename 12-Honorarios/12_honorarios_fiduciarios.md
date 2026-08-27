# 12 Honorarios Fiduciarios

12. Honorarios Fiduciarios
Documentos relacionados: 00_arquitectura_modulos_sistema.md  (módulo 12,
complementario) · 01_fideicomiso_estructura_campos_validaciones.md  (sección 1.1
— excepción expresa a la prohibición de autocontratación) ·
03_patrimonio_bienes_valuacion.md  (los cobros generan movimientos_patrimonio ) ·
06_instrucciones_autorizacion_maker_checker.md .
1. Marco legal
Art. 394 LGTOC / Art. 106 LIC: prohíben la autocontratación (transferencias entre el
patrimonio propio del ﬁduciario y el patrimonio del ﬁdeicomiso), salvo el cobro explícito
de honorarios ﬁduciarios estipulados en contrato. Este módulo especiﬁca esa única
excepción autorizada.
2. Principio de diseño
Todo cobro de honorarios debe (a) estar estipulado en el documento_constitutivo  desde el
origen o en un convenio modiﬁcatorio posterior, (b) pasar por el ﬂujo de instrucción y
autorización del documento 6 igual que cualquier otro movimiento, y (c) generar su propio
movimiento_patrimonio  con tipo_movimiento  explícitamente identiﬁcado como
honorarios — nunca disfrazado como otro tipo de disposición.
3. Modelo de datos — esquemas_honorarios
Campo Descripción Tipo de
dato
Obligatorio Regla / validación
id_esquema
Identiﬁcador
único Numérico Sí Autogenerado
numero_fideicomiso
Fideicomiso
al que aplica
Relación
(FK)
Sí —
tipo_honorario
Naturaleza
del cobro
Catálogo Sí
Apertura /
administración
periódica / por
operación / extinción
monto_o_porcentaje
Monto ﬁjo o
porcentaje
sobre
patrimonio
Numérico Sí —

Campo Descripción Tipo de
dato
Obligatorio Regla / validación
base_calculo
Sobre qué
se calcula,
si es
porcentaje
Catálogo Condicional
patrimonio_inicial
/ saldo vigente / monto
de la operación
periodicidad
Frecuencia
de cobro
Catálogo Condicional
Obligatorio para
administración
periódica  — mensual
/ trimestral / anual
moneda
Moneda del
esquema
Catálogo
(ISO 4217) Sí —
documento_soporte
Cláusula
contractual
o convenio
que lo
estipula
Relación
(FK —
documento
9)
Sí
Sin este soporte, ningún
cobro derivado es
válido
4. Modelo de datos — cobros_honorarios
Campo Descripción Tipo de
dato
Obligatorio Regla / validación
id_cobro
Identiﬁcador
único Numérico Sí Autogenerado
id_esquema
Esquema que
origina el
cobro
Relación
(FK) Sí —
id_instruccion
Instrucción
que autoriza
el cobro
(documento
6)
Relación
(FK)
Sí Ningún cobro se ejecuta sin
pasar por Maker-Checker
id_movimiento
Movimiento
patrimonial
generado
(documento
3)
Relación
(FK) Sí
tipo_movimiento =
honorarios_fiduciarios
fecha_cobro
Fecha
efectiva Fecha Sí —

Campo Descripción Tipo de
dato
Obligatorio Regla / validación
monto_cobrado
Monto
efectivamente
cobrado
Numérico Sí
Debe corresponder al
cálculo derivado de
esquemas_honorarios
5. Validaciones críticas
Ningún cobro sin esquema previamente documentado: el sistema no debe permitir
capturar una instrucción de tipo honorarios si no existe un esquema_honorarios  vigente
y respaldado documentalmente para ese ﬁdeicomiso.
Veriﬁcación de monto: el sistema debe alertar (no necesariamente bloquear) si
monto_cobrado  se desvía del cálculo esperado según esquemas_honorarios , como
control adicional contra cobros indebidos disfrazados de honorarios legítimos.
Vacíos funcionales abiertos
1. Tratamiento ﬁscal (IVA/retenciones): no se ha deﬁnido cómo se calculan y registran
impuestos sobre el cobro de honorarios — requiere validación con el área ﬁscal de la
institución.
2. Prorrateo entre múltiples ﬁdeicomisarios: cuando el patrimonio distribuye a varios
ﬁdeicomisarios, falta deﬁnir si el honorario se cobra sobre el patrimonio total antes de
distribución o se prorratea entre las partes.
3. Honorarios en especie: el modelo asume cobro monetario; falta conﬁrmar si existe algún
escenario donde el honorario se cubra con parte del patrimonio en especie (ej. un bien), lo
cual tendría implicaciones adicionales en el documento 3.
