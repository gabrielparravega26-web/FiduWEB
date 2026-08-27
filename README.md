# FiduWEB

Documentación técnica y de negocio para la arquitectura, operación y control de fideicomisos en México.

## Descripción general

Este repositorio centraliza la documentación funcional, operativa y de arquitectura del sistema FiduWEB. Su objetivo es servir como referencia para análisis, diseño, validación, gobernanza, controles y cumplimiento normativo relacionado con fideicomisos, participantes, cuentas, patrimonio, reportes y procedimientos internos.

La documentación está organizada por módulo para facilitar la consulta, la navegación y la trazabilidad del proyecto.

## Objetivos

- Consolidar la definición de requisitos de negocio del sistema.
- Documentar las reglas de validación, estructura y controles del fideicomiso.
- Establecer la arquitectura funcional y técnica del módulo.
- Registrar obligaciones regulatorias, KYC, PLD, auditoría, reportes y autorizaciones.
- Servir como base para desarrollo, pruebas, validación y gobernanza del proyecto.

## Estructura del repositorio

### Manual base
- [MANUAL DE ESPECIFICACIÓN NORMATIVA Y ARQUITECTURA TÉCNICO-LEGAL PARA EL MANEJO DE FIDEICOMISOS EN MÉXICO.docx](MANUAL%20DE%20ESPECIFICACIÓN%20NORMATIVA%20Y%20ARQUITECTURA%20TÉCNICO-LEGAL%20PARA%20EL%20MANEJO%20DE%20FIDEICOMISOS%20EN%20MÉXICO.docx)

### Módulos

#### 00-Arquitectura
- [00-Arquitectura/00_arquitectura_modulos_sistema.md](00-Arquitectura/00_arquitectura_modulos_sistema.md)

#### 01-Fideicomiso
- [01-Fideicomiso/01_fideicomiso_estructura_campos_validaciones.md](01-Fideicomiso/01_fideicomiso_estructura_campos_validaciones.md)
- [01-Fideicomiso/01.1_gestion_estatus_contrato.md](01-Fideicomiso/01.1_gestion_estatus_contrato.md)
- [01-Fideicomiso/01.2_catalogos_administrables.md](01-Fideicomiso/01.2_catalogos_administrables.md)

#### 02-Participantes
- [02-Participantes/02_participantes_roles_kyc.md](02-Participantes/02_participantes_roles_kyc.md)
- [02-Participantes/02.1_beneficiario_controlador.md](02-Participantes/02.1_beneficiario_controlador.md)

#### 03-Patrimonio
- [03-Patrimonio/03_patrimonio_bienes_valuacion.md](03-Patrimonio/03_patrimonio_bienes_valuacion.md)

#### 04-Cuentas
- [04-Cuentas/04_cuentas_estructura_validaciones.md](04-Cuentas/04_cuentas_estructura_validaciones.md)

#### 05-Gobernanza
- [05-Gobernanza/05_gobernanza_comite_tecnico.md](05-Gobernanza/05_gobernanza_comite_tecnico.md)

#### 06-Autorizaciones
- [06-Autorizaciones/06_instrucciones_autorizacion_maker_checker.md](06-Autorizaciones/06_instrucciones_autorizacion_maker_checker.md)

#### 07-Contabilidad
- [07-Contabilidad/07_contabilidad_fiduciaria.md](07-Contabilidad/07_contabilidad_fiduciaria.md)

#### 08-PLD
- [08-PLD/08_pld_monitoreo_transaccional.md](08-PLD/08_pld_monitoreo_transaccional.md)

#### 09-Documentos
- [09-Documentos/09_documentos_repositorio.md](09-Documentos/09_documentos_repositorio.md)

#### 10-Auditoria
- [10-Auditoria/10_auditoria_trazabilidad.md](10-Auditoria/10_auditoria_trazabilidad.md)

#### 11-Reportes
- [11-Reportes/11_reportes_regulatorios_siti.md](11-Reportes/11_reportes_regulatorios_siti.md)

#### 12-Honorarios
- [12-Honorarios/12_honorarios_fiduciarios.md](12-Honorarios/12_honorarios_fiduciarios.md)

#### 13-Notificaciones
- [13-Notificaciones/13_notificaciones_alertas.md](13-Notificaciones/13_notificaciones_alertas.md)

## Alcance funcional

La documentación cubre los siguientes dominios clave:

- Administración del fideicomiso
- Registro y validación de cuentas
- Participantes, roles, KYC y beneficiarios
- Patrimonio, bienes y valuación
- Transferencias, autorizaciones y aprobaciones
- Contabilidad fiduciaria
- Monitoreo PLD y alertas transaccionales
- Trazabilidad, auditoría y evidencia documental
- Reportes regulatorios y comités técnicos
- Gestión de documentación y notificaciones

## Uso recomendado

Este repositorio puede utilizarse como:

- base de análisis para requisitos funcionales
- referencia para diseño de flujos y validaciones
- documentación de gobernanza y controles
- insumo para desarrolladores, analistas y auditores
- punto de partida para la implementación del sistema en fases

## Estado

El repositorio se encuentra en fase de documentación funcional y arquitectura, con especificaciones consolidadas para la operación del fideicomiso y los controles del negocio.

## Nota

La información incluida en este repositorio tiene carácter documental y de referencia para el diseño del sistema. Cualquier implementación técnica adicional deberá validarse contra los procesos, regulaciones y políticas internas de la organización.
