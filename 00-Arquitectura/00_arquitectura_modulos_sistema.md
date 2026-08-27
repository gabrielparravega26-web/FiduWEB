# 0. Arquitectura de módulos del sistema fiduciario

> **Documentos relacionados:** `01_fideicomiso_estructura_campos_validaciones.md` · `01.1_gestion_estatus_contrato.md` · `02_participantes_roles_kyc.md` · `02.1_beneficiario_controlador.md`. Este documento es el mapa maestro: define qué módulos existen, su base legal, y cuáles son bloqueantes para que un fideicomiso llegue a `vigente` (ver máquina de estados en 1.1).

## 1. Criterio de análisis

Un fideicomiso no se "activa" por decisión administrativa — la transición `en_constitucion → vigente` (documento 1.1) ya exige patrimonio inicial registrado, partes con KYC vigente y documento constitutivo cargado. Eso implica que **la activación depende de que varios módulos existan y estén poblados antes de esa transición**, no después. El criterio para clasificar cada módulo como bloqueante o no es simple: *si su ausencia impide cumplir alguna validación de la máquina de estados o alguna prohibición legal del Art. 394 LGTOC / Art. 106 LIC, es bloqueante*.

## 2. Mapa de módulos

| # | Módulo | Base legal principal | Estado |
|---|---|---|---|
| 1 | **Fideicomiso (Núcleo/Maestro)** | LGTOC Arts. 381–407 | ✅ Especificado (docs 1, 1.1) |
| 2 | **Personas / Participantes (KYC-KYB)** | Art. 115 LIC (PLD/FT), CFF 32-B Ter–Quinquies | ✅ Especificado (docs 2, 2.1) |
| 3 | **Patrimonio** | LGTOC Art. 381 (autonomía patrimonial); CUB Anexo 33 | ✅ Especificado (doc 3) |
| 4 | **Cuentas** | CUB Anexo 33 (Cuentas de Orden, Grupo 8000) | ✅ Especificado (doc 4) |
| 5 | **Gobernanza y Comité Técnico** | LIC Art. 80 | ⬜ Pendiente |
| 6 | **Instrucciones y Autorización (Maker-Checker)** | CUB Título Cuarto y Capítulo V Bis | ⬜ Pendiente |
| 7 | **Contabilidad Fiduciaria (Cuentas de Orden)** | CUB Anexo 33; Criterios D-1 y B-6 | ⬜ Pendiente |
| 8 | **PLD / Monitoreo Transaccional continuo** | Art. 115 LIC | ⬜ Pendiente (KYC de alta ya cubierto en doc 2; esto es el monitoreo post-activación) |
| 9 | **Documentos y Repositorio** | Art. 89 Código de Comercio; NOM-151-SCFI | ⬜ Pendiente |
| 10 | **Auditoría y Trazabilidad** | CUB Capítulo V Bis (bitácora Append-Only) | ⬜ Transversal — parcialmente definido en doc 1.1, falta version genérica de sistema |
| 11 | **Reportes Regulatorios (SITI-CNBV)** | Sistema SITI de la CNBV | ⬜ Pendiente |
| 12 | **Honorarios Fiduciarios** | Excepción expresa del Art. 394 LGTOC / Art. 106 LIC | ⬜ Pendiente |
| 13 | **Notificaciones y Alertas** | Derivado de vigencias KYC, estatus, umbrales PLD | ⬜ Pendiente |

## 3. Clasificación por criticidad de activación

### 3.1 Núcleo bloqueante — sin esto, un fideicomiso NO puede llegar a `vigente`

- **1. Fideicomiso (Maestro)** — obvio, es el registro raíz.
- **2. Personas / Participantes** — la transición a `vigente` exige mínimo un fideicomitente y un fideicomisario con KYC vigente (1.1, sección 2).
- **3. Patrimonio** — sin registro del bien/activo que respalda `patrimonio_inicial`, ese campo es un número sin sustento; la autonomía patrimonial (Art. 381 LGTOC) exige que el bien esté identificado, no solo valorizado.
- **4. Cuentas** — la segregación patrimonial (regla de inviolabilidad #1) exige que exista al menos una cuenta de orden asociada antes de que el fideicomiso pueda recibir o mantener recursos; sin cuenta, el patrimonio no tiene dónde "vivir" contablemente.
- **9. Documentos y Repositorio** — `documento_constitutivo` es requisito explícito de la transición a `vigente` (1.1); sin repositorio, ese campo no tiene qué referenciar.
- **10. Auditoría (base transversal)** — no es opcional activarlo después: cada acción de alta debe quedar auditada desde el primer registro, o se pierde trazabilidad del origen del fideicomiso.

### 3.2 Requerido para operación continua — no bloquea el alta, pero bloquea la primera operación

- **6. Instrucciones y Autorización (Maker-Checker)** — un fideicomiso puede estar `vigente` sin haber ejecutado ninguna operación todavía, pero la primera instrucción de egreso es imposible sin este módulo (regla de inviolabilidad #2 y #3).
- **7. Contabilidad Fiduciaria** — necesaria para que el `patrimonio_inicial` se traduzca en la póliza contable de apertura en Cuentas de Orden; sin esto, el patrimonio existe en el maestro pero no en el libro contable regulatorio.
- **5. Gobernanza y Comité Técnico** — bloqueante *solo* si el fideicomiso específico contempla comité técnico como órgano de decisión (campo condicional en doc 2). No todos los fideicomisos lo requieren, pero si el contrato lo establece, ninguna instrucción del comité es válida sin este módulo.
- **8. PLD / Monitoreo Transaccional continuo** — el KYC de alta (doc 2) cubre la foto inicial; este módulo cubre el monitoreo de operaciones ya en curso (perfil transaccional esperado, alertamiento de inusualidad) — necesario desde la primera transacción, no desde el alta.

### 3.3 Complementarios — necesarios para operación regulatoria completa, no bloquean la primera operación

- **11. Reportes Regulatorios (SITI-CNBV)** — periodicidad mensual/trimestral; el fideicomiso puede operar antes de que corra el primer ciclo de reporte, pero el módulo debe existir antes del primer corte regulatorio.
- **12. Honorarios Fiduciarios** — necesario para que la institución cobre, pero no impide que el fideicomiso reciba y resguarde patrimonio sin haberse cobrado honorarios todavía.
- **13. Notificaciones y Alertas** — mejora operativa (vencimiento de KYC, cambios de estatus, umbrales de riesgo); su ausencia no impide el cumplimiento legal mínimo, pero sin él el cumplimiento depende de revisión manual, lo cual es un riesgo operativo, no legal per se.

## 4. Dependencias entre módulos

```
1. Fideicomiso (Maestro)
   ├── requiere → 2. Personas (KYC)          [partes_relacionadas]
   ├── requiere → 3. Patrimonio               [patrimonio_inicial]
   ├── requiere → 4. Cuentas                  [cuenta de orden asociada]
   ├── requiere → 9. Documentos               [documento_constitutivo]
   └── requiere → 10. Auditoría               [transversal, desde el primer registro]

2. Personas (KYC)
   └── requiere → 2.1 Beneficiario Controlador [personas morales]

3. Patrimonio
   └── alimenta → 7. Contabilidad Fiduciaria   [póliza de apertura, Cuentas de Orden]

4. Cuentas
   └── alimenta → 7. Contabilidad Fiduciaria   [registro de saldo por cuenta]

5. Gobernanza / Comité Técnico (condicional)
   └── habilita → 6. Instrucciones             [acta como documento_soporte de instrucción]

6. Instrucciones y Autorización
   ├── requiere → 10. Auditoría                [bitácora de cada instrucción]
   ├── requiere → 9. Documentos                [NOM-151 + firma electrónica]
   └── ejecuta sobre → 3. Patrimonio y 4. Cuentas

8. PLD / Monitoreo Transaccional
   └── consume → 6. Instrucciones              [evalúa cada instrucción contra perfil esperado]

11. Reportes Regulatorios
   └── consume → 7. Contabilidad Fiduciaria    [saldos de Cuentas de Orden para R01/R24]
```

## 5. Orden de especificación recomendado

Dado que **3 (Patrimonio)** y **4 (Cuentas)** son núcleo bloqueante y además son prerrequisito de **7 (Contabilidad Fiduciaria)**, y que **9 (Documentos)** es prerrequisito transversal de casi todo lo demás, el orden sugerido para las próximas sesiones es:

1. **Patrimonio** — tipos de bienes, esquema de valuación, libro de movimientos (ya referenciado como pendiente desde doc 1).
2. **Cuentas** — cuenta maestra vs. subcuentas, mapeo a Cuentas de Orden 8111/8112.
3. **Documentos y Repositorio** — versión de convenios modificatorios, NOM-151.
4. **Gobernanza y Comité Técnico** — actas, quórum, facultades de instrucción.
5. **Instrucciones y Autorización (Maker-Checker)** — el módulo que finalmente ejecuta operaciones.
6. **Contabilidad Fiduciaria** — cierra el ciclo contable de todo lo anterior.
7. **PLD / Monitoreo Transaccional, Reportes SITI, Honorarios, Notificaciones** — fase de completitud regulatoria.

## Vacíos funcionales abiertos

Ninguno propio de este documento — es un mapa de planeación, no una especificación de campos. Los vacíos abiertos siguen siendo los ya documentados en 1.1 (plazo máximo de `suspendido`) y 2.1 (excepción de beneficiario controlador no identificable).

¿Iniciamos con **Patrimonio** conforme al orden sugerido, o prefieres priorizar otro módulo?
