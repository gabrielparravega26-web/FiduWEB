# 2. Participantes, roles y datos legalmente obligatorios (KYC)

> **Documentos relacionados:** `01_fideicomiso_estructura_campos_validaciones.md` (documento padre — campo `partes_relacionadas`) · `01.1_gestion_estatus_contrato.md` · `02.1_beneficiario_controlador.md` (detalle del campo `beneficiario_controlador`).

El expediente KYC/KYC-B es un requisito bloqueante de ley, exigido por las **Disposiciones de Carácter General del Art. 115 de la LIC (PLD/FT)**: identificación del cliente, matriz de riesgo, monitoreo transaccional y reporte de operaciones inusuales/relevantes. No es un módulo opcional ni postergable — ninguna persona puede operar sin expediente aprobado.

## 1. Modelo relacional de partes (`fideicomiso_partes`)

Los roles del fideicomiso (fideicomitente, fideicomisario, comité técnico, delegado fiduciario) **no** se manejan como campos planos en el maestro del fideicomiso. Se manejan como una tabla puente persona↔rol↔fideicomiso. Esto es lo que permite que una misma persona sea, por ejemplo, fideicomitente y fideicomisario a la vez, que un rol tenga múltiples personas, y que los cambios de rol (sustitución, renuncia, incorporación) queden versionados en el tiempo en vez de sobrescribirse.

| Campo | Descripción | Tipo de dato | Obligatorio | Regla / validación |
|---|---|---|---|---|
| `id_relacion` | Identificador único del registro de participación | Numérico | Sí | Autogenerado |
| `numero_fideicomiso` | Fideicomiso al que pertenece la relación | Relación (FK) | Sí | Debe existir en catálogo de fideicomisos |
| `id_persona` | Persona física o moral participante | Relación (FK a expediente KYC) | Sí | Requiere expediente KYC vigente antes de poder asignarse |
| `rol` | Rol que funge en este fideicomiso | Catálogo | Sí | Fideicomitente / fideicomisario / miembro de comité técnico / delegado fiduciario / otro |
| `fecha_alta_rol` | Fecha desde la que ejerce el rol | Fecha | Sí | No puede ser anterior a `fecha_constitucion` del fideicomiso |
| `fecha_baja_rol` | Fecha en que cesó el rol (si aplica) | Fecha | No | Si existe, el registro pasa a histórico, nunca se borra |
| `facultades` | Alcance de actuación dentro del rol | Texto / catálogo | Condicional | Obligatorio para roles con capacidad de instrucción (fideicomitente, comité técnico) |
| `documento_soporte` | Acta o instrumento que acredita el rol | Relación a repositorio documental | Sí | Sin documento habilitante, el rol no es válido para efectos de instrucción |

> Regla de negocio clave: **nunca se sobrescribe una relación de rol**, se cierra (`fecha_baja_rol`) y se abre una nueva. Esto es lo que te da la evidencia inmutable de quién podía instruir qué y cuándo — indispensable si algún día una operación se cuestiona legalmente.

## 2. Expediente KYC obligatorio

Todo `id_persona` referenciado en `fideicomiso_partes` debe resolver a un expediente KYC completo **antes** de poder asignarse a un rol. El expediente se maneja como entidad independiente del fideicomiso — una persona se da de alta una sola vez y puede participar en múltiples fideicomisos, cada uno con su propia relación de rol.

Hay una bifurcación de diseño obligatoria: **persona física** y **persona moral** no comparten esquema. Intentar meterlas en una sola tabla plana genera campos huérfanos (una persona moral no tiene CURP; una física no tiene beneficiario controlador). El catálogo `id_persona` debe tener un discriminador `tipo_persona` que determina cuál sub-esquema aplica.

### 2.1 Datos obligatorios — persona física

| Campo | Descripción | Tipo de dato | Obligatorio | Regla / validación |
|---|---|---|---|---|
| `nombre_completo` | Nombre(s), apellido paterno, apellido materno | Texto | Sí | Debe coincidir exactamente con identificación oficial |
| `fecha_nacimiento` | Fecha de nacimiento | Fecha | Sí | Persona debe ser mayor de edad para fungir como parte facultada |
| `curp` | Clave Única de Registro de Población | Alfanumérico (18) | Sí (nacionales) | Formato validado; único en catálogo |
| `rfc` | Registro Federal de Contribuyentes | Alfanumérico (13) | Sí | Formato validado |
| `nacionalidad` | País de nacionalidad | Catálogo | Sí | — |
| `pais_residencia` | País de residencia fiscal | Catálogo | Sí | Determina régimen fiscal aplicable a rendimientos |
| `identificacion_oficial` | Tipo y número de identificación vigente | Catálogo + alfanumérico | Sí | INE, pasaporte o cédula profesional; requiere imagen digitalizada vigente |
| `domicilio_completo` | Calle, número, colonia, municipio, estado, CP | Texto estructurado | Sí | Requiere comprobante de domicilio no mayor a 3 meses |
| `actividad_economica` | Ocupación o actividad económica preponderante | Catálogo | Sí | Alimenta el análisis de origen de recursos |
| `pep` | Indicador de Persona Políticamente Expuesta | Booleano | Sí | Si es verdadero, activa expediente reforzado y aprobación de nivel superior |
| `origen_recursos` | Descripción del origen lícito de los recursos aportados | Texto | Sí | Obligatorio con mayor detalle si `pep = verdadero` |
| `nivel_riesgo_pld` | Clasificación de riesgo individual | Catálogo (calculado) | Sí | Calculado por el Risk Score ponderado — ver sección 3; determina periodicidad de revisión |
| `fecha_expediente` | Fecha de integración/última actualización del expediente | Fecha | Sí | Controla vigencia; expedientes vencidos bloquean asignación de nuevos roles |

### 2.2 Datos obligatorios — persona moral

| Campo | Descripción | Tipo de dato | Obligatorio | Regla / validación |
|---|---|---|---|---|
| `razon_social` | Denominación o razón social completa | Texto | Sí | Debe coincidir con acta constitutiva |
| `rfc` | Registro Federal de Contribuyentes | Alfanumérico (12) | Sí | Formato validado |
| `fecha_constitucion` | Fecha de constitución de la sociedad | Fecha | Sí | — |
| `pais_constitucion` | País/jurisdicción de constitución | Catálogo | Sí | Determina si aplica régimen de entidad extranjera |
| `giro_actividad` | Objeto social / actividad económica preponderante | Catálogo | Sí | Alimenta el análisis de origen de recursos |
| `representante_legal` | Persona física con poder de representación | Relación (FK a persona física) | Sí | Debe tener expediente físico propio y poder notarial vigente |
| `beneficiario_controlador` | Persona(s) física(s) que ejercen control real (>25% o control efectivo) | Relación (FK a persona física, multivalor) | Sí | Obligatorio por normativa PLD; sin este dato el expediente no puede activarse |
| `estructura_accionaria` | Composición accionaria relevante | Documento / texto estructurado | Sí | Requiere soporte documental (libro de accionistas o equivalente) |
| `domicilio_fiscal` | Domicilio fiscal registrado | Texto estructurado | Sí | Requiere comprobante vigente |
| `pep_vinculado` | Indica si algún beneficiario controlador o representante es PEP | Booleano | Sí | Si es verdadero, activa expediente reforzado |
| `nivel_riesgo_pld` | Clasificación de riesgo de la entidad | Catálogo (calculado) | Sí | Calculado por el Risk Score ponderado — ver sección 3; determina periodicidad de revisión |
| `fecha_expediente` | Fecha de integración/última actualización del expediente | Fecha | Sí | Controla vigencia |

> Vacío funcional a cerrar: si `beneficiario_controlador` queda vacío o incompleto en una persona moral, el sistema **no debe permitir** que esa persona se asigne a ningún rol en `fideicomiso_partes` — es el punto donde más comúnmente se filtran contingencias de PLD, porque es un dato que depende de terceros (la propia empresa) y tiende a quedar pendiente "para después".

## 3. Matriz de riesgo y periodicidad de revisión del expediente

`nivel_riesgo_pld` no es un catálogo capturado a criterio libre: el sistema debe calcularlo mediante el **Risk Score** ponderado exigido por el marco PLD, combinando cuatro factores cuyo peso conjunto suma 1.00:

$$P_{\text{riesgo}} = (w_{\text{cli}} \cdot R_{\text{cliente}}) + (w_{\text{geo}} \cdot R_{\text{geografía}}) + (w_{\text{pro}} \cdot R_{\text{producto}}) + (w_{\text{tra}} \cdot R_{\text{transaccional}})$$

El resultado numérico determina automáticamente tanto la categoría de riesgo como la periodicidad obligatoria de renovación del expediente — esto es lo que resuelve la vigencia de `fecha_expediente`:

| Categoría | Rango de score | Periodicidad de renovación | Requisito adicional |
|---|---|---|---|
| **Bajo** | 0.0 – 0.39 | Cada 2 años | — |
| **Medio** | 0.40 – 0.69 | Cada 12 meses | — |
| **Alto** | 0.70 – 1.00 | Cada 6 meses | Escalamiento automático al Oficial de Cumplimiento; aprobación obligatoria de EDD (*Enhanced Due Diligence*) antes de activar el expediente |

> Regla de sistema: si `pep = verdadero` o `pep_vinculado = verdadero`, el expediente se clasifica automáticamente como mínimo en categoría **Alto**, sin importar el resultado del score — el indicador PEP no es un factor más de la ponderación, es un forzador de categoría.

## 4. Verificación contra listas de bloqueo

Antes de activar cualquier expediente (física o moral) o de permitir su asignación a un rol en `fideicomiso_partes`, el sistema debe consultar en tiempo real:

- Lista de Personas Bloqueadas de la UIF / SHCP.
- Listado SAT 69-B (Empresas Facturadoras de Operaciones Simuladas — EFOS).
- Listas OFAC, ONU, Interpol y Listado PEP.

| Campo | Descripción | Tipo de dato | Obligatorio | Regla / validación |
|---|---|---|---|---|
| `resultado_listas_bloqueo` | Resultado de la consulta más reciente | Catálogo | Sí | Sin coincidencia / coincidencia potencial (revisión manual) / coincidencia confirmada |
| `fecha_ultima_consulta_listas` | Fecha de la última verificación | Fecha | Sí | Debe repetirse en cada renovación de expediente y, idealmente, en cada operación relevante |

> Hard stop: `resultado_listas_bloqueo = coincidencia confirmada` bloquea el expediente por completo y debe generar automáticamente un ticket de alerta a la UIF — no solo impedir la asignación de roles, sino congelar cualquier operación ya en curso de esa persona.

## Vacíos funcionales abiertos

Ninguno pendiente en el alcance de este documento — la periodicidad de revisión quedó resuelta en la sección 3. El vacío relacionado con cadenas de beneficiario controlador no resolubles se documenta en `02.1_beneficiario_controlador.md`.
