

# gAIOS — tu sistema operativo personal de IA

Clónalo, ejecuta `/setup` y se convierte en **tuyo** en **Claude Code o Codex**: una segunda mente + Jefe de Estado Mayor que guarda tu contexto, estructura tu trabajo, redacta con tu voz y ejecuta flujos de trabajo confiables.

Código abierto y con opiniones propias: completo listo para usar, no una pizarra en blanco. **Haz una bifurcación (fork) y adáptalo a cualquier rol, empresa o dominio.**

---

## Inicio rápido
1. **Clona** esta carpeta en tu máquina.
2. **Ábrela en Claude Code o Codex** y ejecuta **`/setup`** (en Codex: invoca la habilidad `setup` o simplemente pídele que "ejecute setup").
3. Responde la entrevista guiada (identidad, voz, prioridades, stack, equipo, límites). Rellena `CLAUDE.md`, `context/`, `references/voice.md` y `connections.md`.
4. Prueba el primer prompt: *"¿en qué debería enfocarme esta semana?"*

> **¿No estás seguro de qué escribir?** Echa un vistazo primero a [`examples/`](examples/) — guías orientativas por rol (fundador, operaciones, medtech regulado, creador, ventas) que muestran la *estructura* de un gAIOS completado. Son orientación, no datos: no las copiarás.
>
> La compatibilidad en tiempo de ejecución (Claude Code · Codex · otros) se resume en [Compatibilidad](#compatibility) más abajo.

---

## Contenido (la arquitectura)

**Los Cuatro Cs** — Contexto (conoce tu negocio) · Conexiones (alcanza tus recursos) · Capacidades (sabe cómo hacer el trabajo) · Cadencia (ejecuta sin que se lo pidas).

**Los Tres Ms** — Mentalidad · Método · Máquina (`references/3ms-framework.md`). *Ambos marcos inspirados en el trabajo de Nate Herk — ver `NOTICE`.*

**WAT — Flujos de trabajo · Agentes · Herramientas.** La IA probabilística razona; el código determinista ejecuta. Predecible, comprobable, auditable.

**Características (todas incluidas):**
- `/structure` — convierte cualquier entrada vaga en un encargo claro.
- `/triage` · `/daily` · `/weekly` — la capa de **Cadencia**: clasifica por lotes una bandeja de entrada, obtén un informe diario enfocado, ejecuta una revisión operativa semanal.
- `/wiki` — una segunda mente: deja notas en `raw/`, obtén conocimiento limpio y cruzado en `wiki/` (con un control de lint con escaneo de filtraciones).
- `/graph` · `/graph-query` · `/graph-ingest` — un **grafo de conocimiento** (graphify) sobre tu código + `wiki/`: constrúyelo/visualízalo, consulta relaciones e ingiere fuentes externas en la segunda mente.
- `/draft` · `/prep` · `/decide` — núcleo de Jefe de Estado Mayor: redacta comunicaciones en tu voz, prepara un informe de una página para cualquier reunión/persona y estructura + registra una decisión.
- `/workflow` — **flujos de trabajo dinámicos**: pipelines impulsados por objetivos, componibles, autoverificables con un control de calidad por paso.
- `/experiment` — un **bucle de autoinvestigación** (probar → medir → mantener/revertir → registrar), con un ejemplo de pronóstico ejecutable.
- `/exec-cockpit` — una plantilla de transición ejecutiva / cabina de mando.
- `tools/` — Python determinista (renderizador HTML con marca, lint de wiki, registro de experimentos).
- **Disciplina operativa** integrada en `CLAUDE.md` (pensar antes de actuar, simplicidad, cambios quirúrgicos, impulsado por objetivos, verificar antes de completar).
- Una **plantilla de kit de marca** (`brand-assets/`) para que las salidas se rendericen con tu identidad visual.

---

## Estructura
```
CLAUDE.md            ← el manual de operaciones (rellenado por /setup)
AGENTS.md            ← arranque de runtime para Codex / herramientas cruzadas (reproduce las reglas de CLAUDE.md)
examples/            ← guías orientativas por rol (cómo se ve lo bueno; no datos precargados)
context/             ← sobre ti, el negocio, el equipo, prioridades
wiki/  · raw/        ← segunda mente (wiki comprometido; raw ignorado por git)
projects/            ← flujos de trabajo activos
experiments/         ← arnés de autoinvestigación (+ ejemplo de pronóstico ejecutable)
tools/               ← Python determinista (capa de ejecución WAT)
references/sops/     ← flujos de trabajo / SOPs (incl. flujos dinámicos + ejemplos)
references/          ← marco 3ms, voz, guías de API
brand-assets/        ← plantilla CI/CD (tokens + vista previa)
connections.md       ← registro de sistemas que el AIOS puede alcanzar
decisions/log.md     ← registro de decisiones de solo adición
.claude/skills/      ← /setup, /structure, /triage, /daily, /weekly, /wiki, /graph, /graph-query, /graph-ingest, /draft, /prep, /decide, /workflow, /experiment, /exec-cockpit, /onboard, /audit, /level-up
.codex/skills/       ← enlace simbólico → .claude/skills (para que Codex descubra las mismas habilidades)
```

Consulta `EXPANSIONS.md` para saber qué añadir a medida que creces.

---

## Personaliza para tu dominio
El bloque `Guardrails` en `CLAUDE.md` se entrega con valores seguros por defecto. **Establece tu línea de datos sensibles y reglas de cumplimiento** (GDPR / HIPAA / SOC2 / dispositivos médicos / …) durante `/setup` — no ejecutes los valores por defecto sin cambios para un negocio regulado.

## Grafo de conocimiento (graphify)

gAIOS integra **[graphify](https://github.com/safishamsi/graphify)** — convierte tu código + el `wiki/` comprometido en un grafo de conocimiento navegable y consultable (interactivo `graph.html`, un `GRAPH_REPORT.md` de nodos centrales y conexiones sorprendentes, y un servidor MCP). Constrúyelo con `/graph`, consúltalo con `/graph-query` y alimenta tu segunda mente con fuentes externas mediante `/graph-ingest`.

```bash
python tools/graphify_setup.py install   # instala graphify y conecta las habilidades de Claude Code y Codex (también ofrecido por /setup)
```

El código se procesa **localmente**; solo se envía el `wiki/` desidentificado a tu sesión de IA host para la extracción (nunca `raw/`/`.env`/`.tmp/`), y `graphify-out/` es ignorado por git. Detalles: [`references/graphify-api.md`](references/graphify-api.md) · SOP: [`references/sops/knowledge-graph.md`](references/sops/knowledge-graph.md).

## Compatibilidad

gAIOS se ejecuta en cualquier herramienta de programación con agentes que lea un archivo de instrucciones del proyecto. **Claude Code tiene soporte de primer nivel; Codex / Codex CLI es compatible** mediante `AGENTS.md`.

| Runtime | Lee | Flujos de trabajo de gAIOS (habilidades) | Estado |
|---------|-------|--------------------------|--------|
| **Claude Code** | `CLAUDE.md` | Habilidades nativas con barra (`/setup`, `/structure`, …) en `.claude/skills/` | ✅ Soporte de primer nivel |
| **Codex / Codex CLI** | `AGENTS.md` → lo dirige a `CLAUDE.md` + `context/` | Descubrimiento automático desde `.codex/skills` (enlace simbólico → `.claude/skills`), o invocar por nombre | ✅ Compatible |
| **Otros agentes** (Cursor, Gemini CLI, Copilot, …) | `AGENTS.md` / `CLAUDE.md` | Pide un flujo de trabajo por nombre; el agente lee el `.claude/skills/*/SKILL.md` coincidente o `references/sops/` | ⚠️ Funciona mediante instrucciones |

**Usando gAIOS en Codex:** abre el repositorio en Codex CLI — carga `AGENTS.md` automáticamente, lo que lo dirige a `CLAUDE.md` y `context/` y reitera los límites de seguridad estrictos. Las habilidades del proyecto se cargan desde `.codex/skills` (un enlace simbólico a `.claude/skills`); en Windows sin soporte de enlaces simbólicos, el agente lee `.claude/skills/` directamente según lo indicado en `AGENTS.md`. Configura los servidores MCP en `~/.codex/config.toml` y mantén los secretos en `.env`. Detalles: [`AGENTS.md`](AGENTS.md).

> Una única fuente de verdad: `CLAUDE.md` contiene el contenido canónico relleno por `/setup`; `AGENTS.md` reproduce sus reglas para otros runtimes y le da prioridad ante cualquier conflicto.

## Licencia y atribución
gAIOS es **© 2026 Alireza Rezvani**, con licencia MIT (ver `LICENSE`). Está inspirado en el kit inicial AIS-OS de Nate Herk y sus marcos de Los Tres Ms / Los Cuatro Cs, que se acreditan como inspiración (ver `NOTICE`); esos nombres de marco son marcas comerciales de Nate Herk. Todo en este repositorio — la integración WAT, la wiki de segunda mente, el arnés de autoinvestigación, los flujos de trabajo dinámicos, la disciplina operativa y las herramientas — es obra de Alireza Rezvani. Por favor, mantén el crédito de inspiración a Nate Herk.
