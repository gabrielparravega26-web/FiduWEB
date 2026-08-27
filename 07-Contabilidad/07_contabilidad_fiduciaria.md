# 07 Contabilidad Fiduciaria

7. Contabilidad Fiduciaria (Cuentas de Orden)
Documentos relacionados: 00_arquitectura_modulos_sistema.md  (módulo 7,
requerido para la primera operación) · 03_patrimonio_bienes_valuacion.md  (origen de
los movimientos a contabilizar) · 04_cuentas_estructura_validaciones.md  ·
06_instrucciones_autorizacion_maker_checker.md  (toda ejecución genera póliza) ·
11_reportes_regulatorios_siti.md  (consume los saldos de este módulo).
1. Marco legal
CUB, Anexo 33: la contabilidad de ﬁdeicomisos se registra exclusivamente en Cuentas
de Orden (Grupo 8000), nunca en el balance general de la institución.
Unicidad e independencia contable: cada ﬁdeicomiso posee un libro mayor
independiente; no se permite consolidación de saldos entre distintos números de
ﬁdeicomiso.
Partida doble e invariante contable: todo asiento debe balancear a cero (∑Cargos −
∑Abonos = 0).
Multi-moneda y valorización: operaciones registradas en la moneda pactada, con
revaluación simultánea a MXN usando el Tipo de Cambio FIX de Banxico o el valor de
UDIS.
2. Principio de diseño
Este módulo no origina movimientos — los recibe del módulo de Patrimonio
(movimientos_patrimonio , documento 3) y del módulo de Instrucciones (documento 6)
una vez ejecutadas, y los traduce en pólizas de partida doble sobre el catálogo mínimo de
Cuentas de Orden. Es el punto donde la operación se vuelve contablemente auditable ante la
CNBV.
3. Modelo de datos — polizas_contables
Campo Descripción Tipo de
dato
Obligatorio Regla /
validación
id_poliza
Identiﬁcador
único Numérico Sí Autogenerado
numero_fideicomiso
Fideicomiso
al que
pertenece
Relación
(FK) Sí
El libro mayor
nunca consolida
entre
ﬁdeicomisos

Campo Descripción Tipo de
dato
Obligatorio Regla /
validación
id_movimiento
Movimiento
patrimonial
que origina
la póliza
Relación
(FK —
documento
3)
Sí —
id_instruccion
Instrucción
que autorizó
el
movimiento
Relación
(FK —
documento
6)
Sí, salvo
pólizas de
revaluación
automática
—
fecha_poliza
Fecha
contable Fecha Sí —
tipo_poliza
Naturaleza
de la póliza
Catálogo Sí
Apertura /
aportación /
disposición /
revaluación /
honorarios /
cierre
estatus_poliza Estado Catálogo Sí
contabilizada
/ reversada  —
nunca se edita,
solo se reversa
con póliza de
reverso explícita
4. Modelo de datos — asientos_contables
Campo Descripción Tipo de
dato
Obligatorio Regla /
validación
id_asiento
Identiﬁcador
único Numérico Sí Autogenerado
id_poliza
Póliza a la
que
pertenece
Relación
(FK) Sí —
cuenta_cnbv Subcuenta
de Cuentas
de Orden
afectada
Catálogo Sí 8111-001 /
8111-002 /
8111-003 /
8112-001,
conforme al

Campo Descripción Tipo de
dato
Obligatorio Regla /
validación
mapeo del
documento 3
naturaleza
Cargo o
abono Catálogo Sí
cargo  /
abono
monto
Monto del
asiento en
la moneda
original
Numérico Sí —
moneda
Moneda del
asiento
Catálogo
(ISO
4217)
Sí —
monto_mxn_equivalente
Monto
revaluado a
MXN
Numérico Sí
Calculado con
FIX/UDIS
vigente a
fecha_poliza
Regla de negocio no negociable: para cada id_poliza , ∑monto_mxn_equivalente  de
asientos con naturaleza = cargo  debe ser exactamente igual a
∑monto_mxn_equivalente  de asientos con naturaleza = abono . El sistema no debe
permitir contabilizar una póliza que no balancee a cero — es la invariante contable del
manual, aplicada como constraint de base de datos, no solo como validación de negocio.
5. Cierre contable periódico
Campo Descripción
Tipo de
dato Obligatorio
Regla /
validación
id_cierre
Identiﬁcador
único Numérico Sí Autogenerado
numero_fideicomiso
Fideicomiso
cerrado
Relación
(FK)
Sí —
periodo
Periodo
contable
(mensual)
Fecha
(mes/año)
Sí —
saldo_cierre_por_subcuenta Saldo ﬁnal
de cada
subcuenta
Numérico
(derivado)
Sí Debe
coincidir con
la suma de
valuaciones

Campo Descripción Tipo de
dato
Obligatorio Regla /
validación
CNBV al
corte
vigentes del
documento 3
fecha_cierre  /
usuario_cierre
Trazabilidad
del cierre
Fecha /
usuario Sí
Una vez
cerrado el
periodo, no se
contabilizan
pólizas
retroactivas a
ese periodo —
solo pólizas
de ajuste en
el periodo
abierto actual
Vacíos funcionales abiertos
1. Reversión de pólizas: se estableció el principio (nunca editar, solo reversar), pero falta el
modelo de datos del "asiento de reverso" y quién tiene autorización para generarlo —
probablemente requiera el mismo esquema Maker-Checker del documento 6.
2. Ajustes por diferencial cambiario: falta deﬁnir la periodicidad y el tipo de póliza
especíﬁco para registrar la variación FIX/UDIS entre valuaciones, cuando no hay
movimiento operativo pero sí variación de tipo de cambio.
3. Consulta consolidada multi-ﬁdeicomiso para la institución (sin romper la unicidad
contable por ﬁdeicomiso): la institución necesita reportes agregados internos sin violar
la regla de no consolidación — falta deﬁnir si esto es una vista de solo lectura fuera del
libro mayor o un mecanismo distinto.
