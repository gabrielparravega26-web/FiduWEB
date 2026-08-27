# 3. Patrimonio: bienes fideicomitidos, valuación y libro de movimientos

> **Documentos relacionados:** `00_arquitectura_modulos_sistema.md` (módulo 3, núcleo bloqueante) · `01_fideicomiso_estructura_campos_validaciones.md` (campo `patrimonio_inicial`, sección 5.1) · `01.1_gestion_estatus_contrato.md` (valida `patrimonio_inicial` + bien fideicomitido identificado antes de `vigente`) · `04_cuentas_estructura_validaciones.md` (enlace vía `id_cuenta` en `movimientos_patrimonio`).

## 1. Marco legal

- **LGTOC, Art. 381**: el fideicomiso se constituye sobre bienes o derechos determinados que el fideicomitente transmite al fiduciario. La autonomía patrimonial exige que esos bienes sean **identificables**, no solo valorizados — un monto sin bien asociado no satisface el requisito legal de afectación patrimonial.
- **CUB, Anexo 33**: la contabilidad de fideicomisos se registra exclusivamente en **Cuentas de Orden** (Grupo 8000), nunca en el balance de la institución. El catálogo mínimo mapea subcuentas específicas por tipo de bien (sección 3 de este documento).
- **CUB, Criterios D-1 y B-6**: tratamiento contable de cuentas de orden y estados financieros de operaciones por cuenta de terceros.

## 2. Principio de diseño

`patrimonio_inicial` (documento 1) es un **monto agregado de referencia**, no la fuente de verdad del patrimonio. La fuente de verdad son dos estructuras relacionales independientes:

1. **`bienes_fideicomitidos`** — el inventario de bienes/derechos identificables que integran el patrimonio (qué es cada cosa).
2. **`movimientos_patrimonio`** — el libro de movimientos que registra cada evento que afecta el patrimonio en el tiempo (aportaciones, rendimientos, disposiciones, valuaciones).

El saldo vigente del patrimonio **se deriva, nunca se almacena como campo editable**: es la suma de `patrimonio_inicial` más el histórico de `movimientos_patrimonio`. Esto ya quedó establecido como regla en el documento 1, sección 5.1 — aquí se especifica la estructura que lo hace posible.

## 3. Catálogo de tipos de bien (mapeo a Cuentas de Orden CNBV)

| Tipo de bien | Subcuenta CNBV | Naturaleza | Descripción |
|---|---|---|---|
| **Efectivo** | 8111-001 | Deudora | Saldo líquido y cuentas bancarias del fideicomiso |
| **Inmuebles** | 8111-002 | Deudora | Terrenos, edificaciones y derechos inmobiliarios en custodia |
| **Títulos / valores** | 8111-003 | Deudora | Portafolios de inversión, acciones y demás instrumentos financieros |
| **Otros bienes / derechos** | *Pendiente* | Deudora | Derechos de cobro, bienes muebles distintos a los anteriores y cualquier otro bien lícito no cubierto por las 3 subcuentas anteriores |
| — (contrapartida, no es un bien) | 8112-001 | Acreedora | Responsabilidades por Fideicomisos — contrapartida contable del patrimonio aportado, se registra en el módulo de Contabilidad (documento 7, pendiente) |

> **Vacío señalado desde ahora**: el manual normativo fuente solo documenta 3 subcuentas de bien (8111-001/002/003) como catálogo mínimo. Para "Otros bienes / derechos" (ej. derechos de cobro, cartera crediticia, participaciones societarias no bursátiles) falta confirmar la subcuenta CNBV específica contra el catálogo completo del Anexo 33 — no debe asumirse ni inventarse un código. Mientras se confirma, el sistema puede operar con un tipo `otros` con subcuenta `pendiente_de_clasificar`, pero **no debe permitirse que un fideicomiso llegue a `vigente` con bienes en ese estado** — ver regla de activación en sección 6.

## 4. Modelo de datos — `bienes_fideicomitidos`

| Campo | Descripción | Tipo de dato | Obligatorio | Regla / validación |
|---|---|---|---|---|
| `id_bien` | Identificador único del bien | Numérico | Sí | Autogenerado |
| `numero_fideicomiso` | Fideicomiso al que pertenece | Relación (FK) | Sí | Debe existir en catálogo de fideicomisos |
| `tipo_bien` | Clasificación del bien (sección 3) | Catálogo | Sí | Determina la subcuenta CNBV aplicable |
| `subcuenta_cnbv` | Subcuenta de Cuentas de Orden derivada de `tipo_bien` | Catálogo (derivado) | Sí | No editable directo — se resuelve automáticamente desde `tipo_bien` |
| `descripcion` | Descripción específica del bien | Texto | Sí | Ej. dirección del inmueble, ISIN del valor, descripción del derecho |
| `moneda` | Moneda en que está denominado el bien | Catálogo (ISO 4217) | Sí | Puede diferir de `moneda_patrimonio` del fideicomiso; requiere revaluación (sección 5) |
| `valor_aportacion_inicial` | Valor del bien al momento de su aportación | Numérico | Sí | **Inmutable** — mismo principio que `patrimonio_inicial` (documento 1, sección 5.1) |
| `fecha_aportacion` | Fecha en que el bien ingresó al patrimonio | Fecha | Sí | No puede ser anterior a `fecha_constitucion` del fideicomiso |
| `documento_soporte` | Acta, escritura o instrumento que acredita la aportación | Relación a repositorio documental | Sí | Sin este soporte, el bien no es válido para efectos de activación |
| `estatus_bien` | Estado actual del bien | Catálogo | Sí | `activo` / `enajenado` / `liquidado` — nunca se elimina, solo cambia de estatus con movimiento de baja asociado |

## 5. Modelo de datos — `bienes_valuaciones` (histórico de valuación)

Cada bien requiere valuaciones periódicas que **no sobrescriben** la anterior — se acumulan como historial, igual que el resto de los registros regulatorios de este sistema.

| Campo | Descripción | Tipo de dato | Obligatorio | Regla / validación |
|---|---|---|---|---|
| `id_valuacion` | Identificador único | Numérico | Sí | Autogenerado |
| `id_bien` | Bien valuado | Relación (FK) | Sí | — |
| `fecha_valuacion` | Fecha de corte de la valuación | Fecha | Sí | — |
| `valor_valuado` | Valor determinado en esa fecha | Numérico | Sí | En la moneda del bien |
| `valor_mxn_equivalente` | Valor revaluado a moneda nacional | Numérico | Sí | Calculado con el **Tipo de Cambio FIX de Banxico** o el valor de **UDIS** vigente a la fecha de corte, según corresponda |
| `metodo_valuacion` | Cómo se determinó el valor | Catálogo | Sí | Avalúo pericial / precio de mercado / costo histórico / valorización FIX-UDIS |
| `fuente_valuacion` | Soporte de la valuación | Texto / relación a documento | Sí | Perito valuador certificado, fuente de mercado, o Banxico según el método |

> Regla de negocio: el **saldo vigente por bien** en cualquier fecha de corte es la última `bienes_valuaciones` registrada para ese bien, no `valor_aportacion_inicial`. El saldo vigente del patrimonio total del fideicomiso es la suma de las últimas valuaciones vigentes de todos sus bienes activos.

## 6. Modelo de datos — `movimientos_patrimonio` (libro de movimientos)

Este es el ledger que hace operativa la distinción `patrimonio_inicial` vs. saldo vigente (documento 1, sección 5.1).

| Campo | Descripción | Tipo de dato | Obligatorio | Regla / validación |
|---|---|---|---|---|
| `id_movimiento` | Identificador único | Numérico | Sí | Autogenerado |
| `numero_fideicomiso` | Fideicomiso afectado | Relación (FK) | Sí | — |
| `id_bien` | Bien afectado, si el movimiento es específico a un bien | Relación (FK) | Condicional | Nulo solo para movimientos a nivel de efectivo agregado |
| `id_cuenta` | Cuenta operativa por la que transitó el movimiento (documento 4) | Relación (FK a `cuentas_fideicomiso`) | Condicional | Obligatorio para movimientos de efectivo; nulo para movimientos que no transitan por una cuenta (ej. revaluación de un inmueble) |
| `tipo_movimiento` | Naturaleza del movimiento | Catálogo | Sí | Aportación adicional / rendimiento / disposición / gasto / revaluación |
| `monto` | Monto del movimiento | Numérico | Sí | Signo determina si incrementa o disminuye el saldo |
| `moneda` | Moneda del movimiento | Catálogo (ISO 4217) | Sí | — |
| `fecha_movimiento` | Fecha efectiva | Fecha | Sí | No puede ser anterior a `fecha_aportacion` del bien relacionado |
| `id_instruccion` | Instrucción que originó el movimiento | Relación (FK — módulo de Instrucciones, pendiente) | Sí, salvo revaluaciones automáticas | Regla de inviolabilidad #3: sin instrucción, no hay movimiento válido |
| `saldo_resultante` | Saldo del bien o del patrimonio tras el movimiento | Numérico (calculado) | Sí | No editable directo — se recalcula, nunca se captura a mano |
| `documento_soporte` | Evidencia del movimiento | Relación a repositorio documental | Sí | — |

> Regla de negocio crítica: **este libro es Append-Only**, igual que la bitácora de auditoría (documento 1.1). Ningún movimiento se edita ni se borra — un error se corrige con un movimiento de reverso explícito y trazable, nunca modificando el registro original.

## 7. Reglas de activación (refuerzo a 1.1)

Para que un fideicomiso pueda transitar `en_constitucion → vigente`:

- Debe existir **al menos un registro en `bienes_fideicomitidos`** con `estatus_bien = activo` y `subcuenta_cnbv` distinta de `pendiente_de_clasificar`.
- La suma de `valor_aportacion_inicial` de los bienes activos debe **coincidir exactamente** con `patrimonio_inicial` (documento 1). Cualquier discrepancia bloquea la activación — es la misma lógica de consistencia que exige el manual entre el Reporte R24 y el Reporte R01 a nivel regulatorio (documento 0, sección de Reportes), aplicada aquí a nivel de alta.

## Vacíos funcionales abiertos

1. **Subcuenta CNBV para "Otros bienes / derechos"**: falta confirmar contra el catálogo completo del Anexo 33 de la CUB — no se debe asumir un código.
2. **Periodicidad de revaluación por tipo de bien**: un inmueble no se revalúa con la misma frecuencia que un valor cotizado en bolsa; falta definir la periodicidad mínima obligatoria por `tipo_bien` (podría alimentarse de `nivel_riesgo_pld` del fideicomiso, o ser independiente).
3. **Movimientos multi-bien en una sola instrucción** (ej. una instrucción que aporta efectivo Y un inmueble simultáneamente): falta definir si `id_instruccion` admite relación 1-a-muchos con `movimientos_patrimonio` — probablemente sí, pero no está modelado explícitamente todavía.

¿Resolvemos alguno de estos tres antes de continuar, o seguimos con el módulo de **Cuentas** (siguiente en el orden recomendado del documento 0)?
