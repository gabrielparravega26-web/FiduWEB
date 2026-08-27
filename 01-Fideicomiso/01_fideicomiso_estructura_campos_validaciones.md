# 1. Fideicomiso: definición, taxonomía, campos obligatorios y validaciones

> **Documentos relacionados:** `01.1_gestion_estatus_contrato.md` (detalle del campo `estatus_fideicomiso`) · `01.2_catalogos_administrables.md` (detalle de `id_tipo_contrato`, `id_tipo_negocio`, `id_producto`, `id_subproducto`) · `02_participantes_roles_kyc.md` (detalle de `partes_relacionadas`) · `02.1_beneficiario_controlador.md`.

## 1. Definición operativa

Un **fideicomiso** es el contrato por el cual una persona (el **fideicomitente**) transmite a una institución fiduciaria (el **fiduciario**) la titularidad de bienes o derechos, con el fin de que ésta los destine a un fin lícito determinado en beneficio de uno o varios terceros (**fideicomisarios**), bajo la instrucción y vigilancia establecidas en el contrato constitutivo (**LGTOC, Arts. 381–407**).

La institución que funge como fiduciario debe estar expresamente autorizada para ello conforme a la **Ley de Instituciones de Crédito (LIC), Arts. 79–85 Bis**, y actúa a través de **Delegados Fiduciarios** nombrados por escritura pública y formalizados ante la CNBV — el campo `institucion_fiduciaria` (sección 5) debe validar contra ese catálogo de entidades autorizadas, no aceptar texto libre.

Para efectos de sistema, lo relevante de esta definición es que impone tres restricciones de diseño no negociables:

- **Segregación patrimonial**: los bienes fideicomitidos NO son propiedad del fiduciario ni del fideicomitente; el sistema debe tratar el patrimonio de cada fideicomiso como un libro contable aislado, nunca mezclable con el patrimonio propio de la institución ni con el de otro fideicomiso.
- **Instrucción documentada**: toda operación sobre el patrimonio debe originarse en una instrucción trazable (contractual, de comité técnico, o de la parte facultada). Sin documento habilitante, no hay movimiento válido.
- **Finalidad determinada**: el sistema debe amarrar cada fideicomiso a un fin lícito específico, porque ese fin es el que determina qué operaciones son procedentes y cuáles constituyen desviación (riesgo legal y de PLD).

### 1.1 Prohibiciones legales bloqueantes a nivel de sistema

Estas restricciones (**Art. 394 LGTOC** y **Art. 106 LIC**) no son reglas de negocio configurables — deben implementarse como validaciones de backend que ningún rol puede omitir:

- **Prohibición de garantía de rendimientos**: ningún campo o cláusula parametrizable puede prometer un rendimiento garantizado sobre el patrimonio aportado.
- **Prohibición de autocontratación**: bloqueo de transferencias entre el patrimonio propio de la institución fiduciaria y el patrimonio del fideicomiso, salvo el cobro explícito de honorarios fiduciarios estipulados en contrato.
- **Prohibición de manejo sin instrucción**: todo egreso debe estar vinculado a un ID de instrucción o de acta de comité técnico (ver `documento_soporte` en el modelo de instrucciones).

## 2. Tipo principal de fideicomiso (catálogo regulatorio — Reporte SITI Serie R24, CNBV)

Este clasificador **no es una taxonomía de producto libre** — es el catálogo cerrado que exige el **Reporte SITI Serie R24 de la CNBV** (desglose trimestral por número de contrato, sector, tipo y número de partes; ver manual normativo, sección 6). Por diseño regulatorio, el reporte **no admite clasificación múltiple**: cada fideicomiso debe resolver a un único tipo regulatorio.

| # | Tipo regulatorio (CNBV) | Finalidad / alcance |
|---|---|---|
| 1 | **Administración** | El fiduciario administra bienes o flujos según instrucción, sin transmitir dominio final |
| 2 | **Inversión** | El patrimonio se destina a generar rendimientos (discrecional o no discrecional), incluyendo vehículos de inversión estructurados (CKD, CERPI, FIBRA) |
| 3 | **Garantía** | El patrimonio respalda el cumplimiento de una obligación (crédito, contrato) |
| 4 | **Inmobiliario** | Fideicomisos cuyo objeto principal son bienes inmuebles: administración, desarrollo o traslación de dominio inmobiliario |
| 5 | **Testamentario** | Sustituye o complementa disposiciones sucesorias |
| 6 | **Público, Gubernamental o Estatal** | Constituido por entidades de gobierno (federal, estatal o municipal) |
| 7 | **De fomento** | Constituido para fines de fomento económico o desarrollo (distinto de un fideicomiso público operativo) |
| 8 | **De caridad** | Fines filantrópicos o de beneficencia |
| 9 | **Otros** | Cualquier finalidad lícita no comprendida en las categorías anteriores |

> **Este catálogo de 9 valores no es directamente administrable ni directamente seleccionable en el alta del fideicomiso.** El sistema captura un `tipo_contrato` de negocio (catálogo administrable) que mapea obligatoriamente a uno de estos 9 valores. El modelo completo de catálogos administrables — `tipo_contrato`, `tipo_negocio`, `producto`, `subproducto` — y sus reglas de gobierno se especifican en `01.2_catalogos_administrables.md`.

## 3. Tipo de negocio (línea de negocio / vertical)

Este clasificador determina **quién opera** el fideicomiso dentro de la institución y qué controles sectoriales aplican — es independiente del tipo regulatorio y no se reporta a CNBV. Se maneja como catálogo administrable (`cat_tipo_negocio`, ver `01.2_catalogos_administrables.md`); el listado siguiente es el conjunto sugerido de arranque, no un catálogo cerrado:

- **Corporativo / empresarial**
- **Inmobiliario**
- **Infraestructura y energía**
- **Mercado de capitales (emisor)**
- **Público / gubernamental**
- **Patrimonial y sucesorio (banca privada)**
- **Filantrópico / social**

## 4. Productos y subproductos

El producto es la **oferta comercial concreta** dentro de un tipo de contrato; el subproducto es su variante operativa. Ambos se manejan como catálogos administrables en cascada (`cat_producto`, `cat_subproducto`) — ver estructura completa, campos y reglas de gobierno en `01.2_catalogos_administrables.md`. El listado siguiente ejemplifica la relación esperada entre tipo regulatorio y producto, no es el catálogo definitivo:

| Tipo regulatorio (CNBV) | Producto (ejemplo) | Subproductos típicos |
|---|---|---|
| Administración | Administración de flujos / bienes | Administración de flujos, administración con reversión |
| Inversión | Inversión discrecional / no discrecional | Inversión discrecional, inversión no discrecional, vehículos estructurados (CKD, CERPI, FIBRA) |
| Garantía | Garantía de cumplimiento | Garantía inmobiliaria, garantía de fuente de pago, garantía de cartera |
| Inmobiliario | Administración / desarrollo / traslación inmobiliaria | Administración de inmuebles en renta, desarrollo inmobiliario, traslativo de dominio |
| Testamentario | Sucesorio | Fideicomiso testamentario, fideicomiso de protección de activos |
| Público, Gubernamental o Estatal | Administración pública | Fideicomiso de inversión y administración público |
| De fomento | Fomento económico | Fideicomiso de fomento económico o desarrollo sectorial |
| De caridad | Filantrópico | Fideicomiso de beneficencia, fideicomiso de apoyo social |
| Otros | Según finalidad declarada | Requiere justificación documental de la finalidad específica en `documento_constitutivo` |

> Regla de negocio: `producto` siempre depende de `tipo_contrato` (relación padre-hijo), y `subproducto` siempre depende de `producto`. El sistema debe filtrar en cascada — nunca permitir capturar un subproducto huérfano de un producto incompatible con el `tipo_contrato` seleccionado.

## 5. Datos maestros obligatorios para identificación en sistema

Estos son los campos que, si faltan, impiden dar de alta un fideicomiso operable. Son el mínimo indispensable para trazabilidad, PLD y contabilidad segregada — no una lista exhaustiva de todo el expediente.

| Campo | Descripción | Tipo de dato | Obligatorio | Regla / validación |
|---|---|---|---|---|
| `numero_fideicomiso` | Identificador único institucional | Alfanumérico | Sí | Único, inmutable una vez asignado |
| `institucion_fiduciaria` | Entidad que funge como fiduciario | Catálogo | Sí | Debe existir en catálogo de fiduciarias autorizadas |
| `id_tipo_contrato` | Tipo de contrato (catálogo administrable — sección 2 y `01.2_catalogos_administrables.md`) | Relación (FK a `cat_tipo_contrato`) | Sí | Debe estar `activo`; su mapeo regulatorio se resuelve automáticamente |
| `tipo_regulatorio_snapshot` | Código CNBV resuelto al momento de constitución (derivado, inmutable) | Alfanumérico | Sí (autogenerado) | No se recalcula si el mapeo del `tipo_contrato` cambia después — ver `01.2_catalogos_administrables.md`, sección 7 |
| `id_tipo_negocio` | Línea de negocio (catálogo administrable — sección 3) | Relación (FK a `cat_tipo_negocio`) | Sí | Determina flujo de aprobación interno |
| `id_producto` | Producto comercial (catálogo administrable — sección 4) | Relación (FK a `cat_producto`) | Sí | Filtrado en cascada por `id_tipo_contrato` |
| `id_subproducto` | Variante operativa | Relación (FK a `cat_subproducto`) | Sí | Filtrado en cascada por `id_producto` |
| `fecha_constitucion` | Fecha de firma del contrato | Fecha | Sí | No puede ser futura |
| `fecha_vigencia_fin` | Fecha o condición de término | Fecha / condición | Sí (una de las dos) | Si es indefinido, requiere justificación documentada |
| `partes_relacionadas` | Participantes del fideicomiso (ver documento 2 — `fideicomiso_partes`) | Relación (tabla puente) | Sí | Mínimo un fideicomitente y un fideicomisario activos |
| `moneda_patrimonio` | Moneda funcional del patrimonio | Catálogo (ISO 4217) | Sí | Determina la moneda base de todas las cuentas asociadas |
| `patrimonio_inicial` | Monto de aportación con el que se apertura el contrato | Numérico | Sí | **Inmutable** una vez registrado; no se actualiza con movimientos posteriores — es la referencia de origen para conciliación y auditoría |
| `estatus_fideicomiso` | Estado operativo actual | Catálogo | Sí | Catálogo cerrado de 6 valores y máquina de estados completa en `01.1_gestion_estatus_contrato.md` — controla qué operaciones son permitidas |
| `nivel_riesgo_pld` | Clasificación de riesgo para PLD | Catálogo | Sí | Alimenta la periodicidad de revisión de expediente |
| `oficial_relacion` | Responsable interno del expediente | Usuario del sistema | Sí | Debe tener rol autorizado activo |
| `jurisdiccion` | País / entidad federativa que rige el contrato | Catálogo | Sí | Determina normativa aplicable y reportes regulatorios |
| `documento_constitutivo` | Referencia al contrato origen | Relación a repositorio documental | Sí | No editable directo; solo mediante convenio modificatorio versionado |

### 5.1 Patrimonio inicial vs. saldo vigente

`patrimonio_inicial` y el patrimonio actual del fideicomiso son dos conceptos distintos que no deben vivir en el mismo campo:

- **`patrimonio_inicial`** (en el maestro del fideicomiso): monto fijo, capturado una sola vez al constituir el contrato. Es el punto de partida para conciliación y auditoría — "¿con cuánto se abrió esto?".
- **Saldo vigente del patrimonio**: se deriva de un libro de movimientos (aportaciones, rendimientos, disposiciones, valuaciones) que pertenece a la rama de **Patrimonio** del árbol, no al maestro de identificación. El sistema calcula el saldo vigente sumando el histórico de movimientos sobre el `patrimonio_inicial`, nunca actualizando el campo original.

Esto también resuelve un control de auditoría: si `patrimonio_inicial` fuera editable, cualquier ajuste posterior sería indistinguible de un error de captura original — perderías la capacidad de detectar manipulación retroactiva del punto de partida.

## Vacíos funcionales abiertos

El control de **autorización dual** para `estatus_fideicomiso` quedó resuelto en `01.1_gestion_estatus_contrato.md`. El vacío que permanece abierto en este documento es el desglose a detalle de la rama **Patrimonio** (tipos de bienes y su esquema de valuación) — pendiente para una siguiente sesión.
