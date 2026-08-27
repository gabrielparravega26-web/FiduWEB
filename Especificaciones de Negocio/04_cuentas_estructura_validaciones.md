# 4. Cuentas: estructura, segregación y validaciones

> **Documentos relacionados:** `00_arquitectura_modulos_sistema.md` (módulo 4, núcleo bloqueante) · `03_patrimonio_bienes_valuacion.md` (bienes tipo `efectivo` y `movimientos_patrimonio`) · `01.1_gestion_estatus_contrato.md` (valida cuenta maestra activa antes de `vigente`).

## 1. Marco legal

- **LGTOC, Art. 381**: la autonomía patrimonial exige que los recursos del fideicomiso residan en cuentas segregadas, nunca mezcladas con el patrimonio propio del fiduciario ni con el de otro fideicomiso.
- **CUB, Anexo 33 — Unicidad e independencia contable**: cada fideicomiso posee un libro mayor (*ledger*) independiente; no se permite consolidación de saldos entre distintos números de fideicomiso.
- **CUB, Anexo 33 — Partida doble e invariante contable**: todo asiento debe balancear a cero (Cargos − Abonos = 0). Este módulo registra la estructura operativa de cuentas; el motor de partida doble que traduce sus movimientos en pólizas contables se especifica en el módulo de Contabilidad Fiduciaria (documento 7, pendiente).
- **Regla de inviolabilidad #1** (perfil de sistema): jamás se permite mezcla de fondos o balances entre distintos fideicomisos o con la cuenta propia de la institución fiduciaria.

## 2. Principio de diseño

Un fideicomiso no tiene "una cuenta" — tiene una **cuenta maestra** obligatoria y, opcionalmente, **subcuentas** con propósito específico (por fideicomisario, por destino de recursos, por línea de inversión). Ambas se modelan en la misma tabla con auto-referencia jerárquica, no como estructuras separadas.

```
Cuenta maestra (obligatoria, 1 por fideicomiso)
   ├── Subcuenta: distribución a Fideicomisario A (opcional)
   ├── Subcuenta: reserva operativa (opcional)
   └── Subcuenta: inversión discrecional (opcional)
```

La cuenta representa el **contenedor operativo** de los recursos; el bien `tipo_bien = efectivo` (documento 3) representa el **activo patrimonial**. Ambos deben estar enlazados — una cuenta con saldo en efectivo sin su correspondiente `bien_fideicomitido`, o viceversa, es una inconsistencia que el sistema debe impedir.

## 3. Modelo de datos — `cuentas_fideicomiso`

| Campo | Descripción | Tipo de dato | Obligatorio | Regla / validación |
|---|---|---|---|---|
| `id_cuenta` | Identificador único | Numérico | Sí | Autogenerado |
| `numero_fideicomiso` | Fideicomiso al que pertenece | Relación (FK) | Sí | Debe existir en catálogo de fideicomisos |
| `id_cuenta_padre` | Cuenta maestra de la que depende, si es subcuenta | Relación (FK a sí misma) | Condicional | Nulo únicamente para la cuenta maestra; obligatorio para subcuentas |
| `tipo_cuenta` | Rol de la cuenta | Catálogo | Sí | `maestra` / `subcuenta` |
| `proposito` | Finalidad específica de la subcuenta | Catálogo | Condicional | Obligatorio para `subcuenta` (ej. distribución a fideicomisario, reserva operativa, inversión) |
| `id_bien` | Bien fideicomitido tipo `efectivo` asociado (documento 3) | Relación (FK a `bienes_fideicomitidos`) | Sí | Garantiza que toda cuenta con saldo tenga su contraparte patrimonial registrada |
| `moneda` | Moneda de la cuenta | Catálogo (ISO 4217) | Sí | Puede diferir de `moneda_patrimonio` del fideicomiso; requiere revaluación FIX/UDIS igual que en el módulo Patrimonio |
| `institucion_custodio` | Banco o custodio donde reside la cuenta | Catálogo | Sí | Debe ser una institución autorizada; si es la misma institución fiduciaria, activa validación de autocontratación (sección 5) |
| `numero_cuenta_externa` | CLABE o número de cuenta bancaria real, si aplica | Alfanumérico | Condicional | Obligatorio si la cuenta corresponde a una cuenta bancaria externa custodiada; no aplica a cuentas de orden puramente internas |
| `estatus_cuenta` | Estado operativo | Catálogo | Sí | `activa` / `cerrada` — nunca se elimina, solo se cierra con fecha y motivo |
| `fecha_apertura` | Fecha de apertura | Fecha | Sí | No puede ser anterior a `fecha_constitucion` del fideicomiso |
| `fecha_cierre` | Fecha de cierre, si aplica | Fecha | No | Obligatoria si `estatus_cuenta = cerrada` |
| `documento_soporte` | Contrato de apertura de cuenta o instrucción que la origina | Relación a repositorio documental | Sí | — |

> Regla de negocio: `numero_cuenta_externa`, cuando existe, debe ser **único en todo el sistema** — no solo dentro del fideicomiso. Dos fideicomisos jamás pueden compartir la misma cuenta bancaria externa; esa validación es la implementación directa de la regla de segregación patrimonial.

## 4. Saldo de cuenta (derivado, no almacenado)

El saldo de una cuenta **no es un campo editable** — se deriva de la suma de `movimientos_patrimonio` (documento 3) cuyo `id_bien` corresponda al `id_bien` enlazado a esta cuenta. Esto evita que existan dos fuentes de verdad del mismo saldo (una en el libro de movimientos, otra en la cuenta) que puedan desincronizarse.

> **Refinamiento pendiente sobre el documento 3**: la tabla `movimientos_patrimonio` debe extenderse con un campo `id_cuenta` (FK opcional) para los movimientos de efectivo, de forma que un movimiento pueda identificar tanto el bien patrimonial afectado como la cuenta operativa específica por la que transitó — relevante cuando existen múltiples subcuentas de efectivo bajo el mismo bien.

## 5. Validaciones críticas

- **Segregación entre fideicomisos**: constraint de unicidad en `numero_cuenta_externa` a nivel de sistema completo (no solo por fideicomiso).
- **Prohibición de autocontratación** (Art. 394 LGTOC / Art. 106 LIC — ya establecida en documento 1, sección 1.1): si `institucion_custodio` coincide con la propia institución fiduciaria actuando en cuenta propia, cualquier movimiento entre esa cuenta y el patrimonio del fideicomiso debe bloquearse, salvo que el `tipo_movimiento` asociado en `movimientos_patrimonio` sea explícitamente `honorarios_fiduciarios` con instrucción y documento soporte.
- **Cuenta maestra única y obligatoria**: un fideicomiso no puede tener más de una cuenta con `tipo_cuenta = maestra` activa simultáneamente.
- **No apertura de subcuenta sin cuenta maestra activa**: el sistema debe bloquear el alta de cualquier `subcuenta` si la cuenta maestra del fideicomiso no está en estatus `activa`.
- **Consistencia con Patrimonio**: la suma de saldos derivados de todas las cuentas activas de un fideicomiso debe coincidir con la suma de las últimas valuaciones vigentes de los bienes `tipo_bien = efectivo` en el documento 3. Cualquier discrepancia es un hallazgo de auditoría automático.

## 6. Regla de activación (refuerzo a 1.1)

Para que un fideicomiso transite `en_constitucion → vigente`, debe existir **exactamente una cuenta con `tipo_cuenta = maestra` y `estatus_cuenta = activa`**, enlazada a un `bien_fideicomitido` válido conforme al documento 3. Sin cuenta maestra activa, el patrimonio no tiene dónde residir operativamente, aunque ya esté declarado en el módulo Patrimonio.

## Vacíos funcionales abiertos

1. **Cuentas bancarias externas vs. cuentas de orden puramente internas**: falta decidir si el sistema modela cuentas bancarias reales con conciliación bancaria automatizada (vía API del banco custodio), o si únicamente lleva el registro de orden y la conciliación bancaria es un proceso externo/manual. Esto tiene implicación de alcance técnico significativa para módulos futuros.
2. **Extensión de `movimientos_patrimonio` con `id_cuenta`** (señalado en sección 4) — requiere actualizar el documento 3 una vez confirmado el diseño.
3. **Límite de subcuentas por fideicomiso**: no hay regla que evite proliferación descontrolada de subcuentas; podría requerirse un máximo configurable o una justificación obligatoria por subcuenta adicional.

¿Resolvemos alguno de estos vacíos, actualizamos el documento 3 con el campo `id_cuenta`, o continuamos con el siguiente módulo del orden recomendado — **Documentos y Repositorio**?
