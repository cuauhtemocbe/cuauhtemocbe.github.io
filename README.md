# Cuauhtémoc Bautista

**Manager AI Engineer — Liderazgo técnico de equipos de IA generativa en producción**

📧 [cuauhtemocbe@gmail.com](mailto:cuauhtemocbe@gmail.com)
🔗 [linkedin.com/in/cuauhtemocbe](https://www.linkedin.com/in/cuauhtemocbe)
📍 CDMX, México

Ingeniero de IA y científico de datos senior (8 años de experiencia), especializado en llevar agentes LLM a producción de forma confiable, con experiencia en fintech, banca/crédito y sector público regulado. El detalle de arquitectura, guardrails y evaluación continua está más abajo, en "Cómo trabajo".

Este repo reúne los proyectos personales más representativos de ese trabajo — cada uno vive en su propio repo, enlazado abajo.

---

## 🔭 Actividad reciente

![Gráfico de contribuciones de cuauhtemocbe](https://ghchart.rshah.org/2a6df5/cuauhtemocbe)

<!--RECENT_ACTIVITY:start-->
- 🔨 Push a **Diplomado-Ciencia-Datos**
- 🔨 Push a **Diplomado-Ciencia-Datos**
- 🔨 Push a **cuauhtemocbe.github.io**
- 📝 Issue labeled en **Diplomado-Ciencia-Datos**: explain group (shap 0.46.0) has no cp313 wheel — needs build tools or version bump
- 📝 Issue opened en **Diplomado-Ciencia-Datos**: explain group (shap 0.46.0) has no cp313 wheel — needs build tools or version bump
<!--RECENT_ACTIVITY:end-->

---

## Experiencia

**Manager AI Engineer — Auronix** · desde enero 2026 · 8 años de experiencia en IA/datos

- Lidero un equipo de 4 ingenieros: arquitectura técnica, aprobación de despliegues y rigor de ingeniería (testing, mutation testing, CI/CD).
- Diseñé la plataforma de agentes conversacionales adoptada como estándar de la empresa (LangGraph + Langfuse), sostenida en producción por evaluación continua con score >95%.

📄 [Ver CV](https://v0-portfolio-website-phi-lyart.vercel.app/) · [⬇️ Descargar PDF](assets/cv/cuauhtemoc-bautista-cv.pdf)

---

## Cómo trabajo

- **Evaluación continua antes de shippear**: capability evals, redteam adversarial y regression evals sobre golden datasets (score >95% en producción), más mutation testing (~99% en Auronix, 100% en `btc-predictor` con Cosmic Ray).
- **Guardrails de seguridad por defecto**: sin push directo a main (rama + PR + CI verde) y un gate de Socket Firewall que bloquea dependencias maliciosas en PRs de Dependabot, reforzado con SCA continuo — ver `meta-projects` y los repos de infraestructura abajo.
- **Gobernanza de estándares a escala**: auditoría automatizada de buenas prácticas por repositorio y sincronización de configuración/skills entre proyectos, detectando divergencias reales frente a simples retrasos.
- **Rigor de ingeniería verificable, no solo declarado**: cobertura de tests gateada en CI (`dockyard2sail-py`, 90% mínimo), tipado estricto (mypy) y escaneo de vulnerabilidades (Trivy) antes de build.

---

## Proyecto destacado

**meta-projects** — meta-repo privado que orquesta todo este portafolio (`~/Projects`) con agentes LLM. Repo privado, sin link público — la descripción es del sistema, no del código:

- **Framework agéntico multicapa**: sistema de agentes LLM (Claude Code CLI, skills propios, servidores MCP) con una capa mecánica de hooks para automatizar la gestión de múltiples repositorios y servicios.
- **Orquestación multiagente en dos etapas**: un agente propone User Stories cross-repo y otro las implementa tras aprobación humana, invocando Claude Code CLI en cada repo destino.
- **Guardrails de seguridad**: modelo de despliegue sin push directo a main (rama + PR + CI verde) y un gate de Socket Firewall que bloquea automáticamente dependencias maliciosas en PRs de Dependabot, reforzado con SCA continuo vía Socket Security.
- **Gobernanza de estándares a escala**: auditoría automatizada de buenas prácticas por repositorio y sincronización de configuración y skills de Claude Code entre proyectos.

---

## Proyectos

### 🤖 IA / LLMs

- **[agentic-evals](https://github.com/cuauhtemocbe/agentic-evals)** — Prácticas de evaluación de agentes (agentic evals): entorno reproducible con Docker + Poetry + JupyterLab.
- **[reel-forge-ts](https://github.com/cuauhtemocbe/reel-forge-ts)** — Generador local de reels/videos verticales a partir de imágenes + guion, con pacing, transiciones y captions decididos dinámicamente por **Claude Code CLI**. Con tests (Vitest).
- **[translate-and-teach](https://github.com/cuauhtemocbe/translate-and-teach)** — Analizador de frases español→inglés con análisis gramatical y tips de aprendizaje, usando Llama 3.3 70B vía Together.ai. React + TypeScript, 54 tests, CI (lint + test).
- **[Ollama-Open-WebUI](https://github.com/cuauhtemocbe/Ollama-Open-WebUI)** — Instalación automatizada de Ollama + Open WebUI con Docker para correr LLMs localmente con interfaz tipo ChatGPT.

### 📊 Data Science / ML

- **[btc-predictor](https://github.com/cuauhtemocbe/btc-predictor)** — Webapp de ML para predecir el precio de Bitcoin al día siguiente, con registro de predicciones, error histórico y simulación de PnL. Desplegado en Railway. Con tests (pytest) y mutation testing (100% score, Cosmic Ray).
- **[AvocadoDash](https://github.com/cuauhtemocbe/AvocadoDash)** — Tablero interactivo (Python Dash) para analizar precios y ventas de aguacate en EE. UU. (2015–2018). Con tests (pytest) y CI.
- **[homicides-rate-visualizer](https://github.com/cuauhtemocbe/homicides-rate-visualizer)** — Simulador interactivo de escenarios hipotéticos de homicidios en México (2000–2026). React + TypeScript + Vite. Tests (Vitest) y CI.
- **[judicial-candidates-mx](https://github.com/cuauhtemocbe/judicial-candidates-mx)** — Webapp en Flask para comparar y analizar candidaturas judiciales en México.

### 🛠️ Infraestructura / Ingeniería

- **[dockyard2sail-py](https://github.com/cuauhtemocbe/dockyard2sail-py)** — Template de API REST en Python: FastAPI + Docker + arquitectura hexagonal, CI con cobertura mínima 90%, typecheck (mypy) y escaneo de vulnerabilidades (Trivy).
- **[dockyard2sail-ts](https://github.com/cuauhtemocbe/dockyard2sail-ts)** — Boilerplate TypeScript listo para producción: Docker, DevContainers, CI (typecheck, tests con cobertura, build, audit).
- **[Diplomado-Ciencia-Datos](https://github.com/cuauhtemocbe/Diplomado-Ciencia-Datos)** — Entorno Dockerizado (Python 3.12 + Jupyter + Poetry) y actividades del Diplomado de Ciencia de Datos 2024–2025. CI (Pylint) y tests.

---

## Stack

`Python` `TypeScript` `FastAPI` `React` `LLMs (Claude, Llama, Together.ai)` `Langfuse` `Docker` `Railway` `GitHub Actions` `Poetry` `pytest`

---

<sub>Para refrescar el PDF del CV: regenerar `curriculum-vitae/out/CV.pdf` (`./scripts/generate_pdf.sh cvs/CV.md`) y copiarlo a `assets/cv/cuauhtemoc-bautista-cv.pdf` en este repo.</sub>
