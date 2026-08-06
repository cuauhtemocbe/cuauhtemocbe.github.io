# Cuauhtémoc Bautista

**AI Engineer — agentes LLM, data apps y templates de infraestructura**

🌐 [cuauhtemocbe.com](https://cuauhtemocbe.com/)
💼 [LinkedIn](https://www.linkedin.com/in/cuauhtemocbe)

Índice de mis proyectos en GitHub. Cada uno vive en su propio repo, con código
abierto, tests y CI; los que están desplegados enlazan su demo en vivo.

---

## Proyectos

### 🤖 IA / LLMs

- **[translate-and-teach](https://github.com/cuauhtemocbe/translate-and-teach)** — Analizador de frases español→inglés con análisis gramatical y tips de aprendizaje, usando Llama 3.3 70B vía Together.ai. React + TypeScript, 54 tests, CI. · [Demo](https://translate-and-teach-production.up.railway.app/)
- **[reel-forge-ts](https://github.com/cuauhtemocbe/reel-forge-ts)** — Generador local de reels verticales a partir de imágenes + guion, con pacing, transiciones y captions decididos dinámicamente por **Claude Code CLI**. Tests con Vitest.
- **[agentic-evals](https://github.com/cuauhtemocbe/agentic-evals)** — Prácticas de evaluación de agentes (agentic evals): entorno reproducible con Docker + Poetry + JupyterLab.
- **[Ollama-Open-WebUI](https://github.com/cuauhtemocbe/Ollama-Open-WebUI)** — Instalación automatizada de Ollama + Open WebUI con Docker para correr LLMs localmente con interfaz tipo ChatGPT.

### 📊 Data Science / ML

- **[btc-predictor](https://github.com/cuauhtemocbe/btc-predictor)** — Webapp de ML para predecir el precio de Bitcoin al día siguiente, con registro de predicciones, error histórico y simulación de PnL. Tests con pytest y mutation testing (100% score, Cosmic Ray).
- **[AvocadoDash](https://github.com/cuauhtemocbe/AvocadoDash)** — Tablero interactivo (Python Dash) para analizar precios y ventas de aguacate en EE. UU. (2015–2018). Tests con pytest y CI. · [Demo](https://avocadodash-production.up.railway.app/)
- **[homicides-rate-visualizer](https://github.com/cuauhtemocbe/homicides-rate-visualizer)** — Simulador interactivo de escenarios hipotéticos de homicidios en México (2000–2026). React + TypeScript + Vite, tests con Vitest y CI. · [Demo](https://homicides-rate-visualizer-production.up.railway.app/)
- **[judicial-candidates-mx](https://github.com/cuauhtemocbe/judicial-candidates-mx)** — Webapp en Flask para comparar y analizar candidaturas judiciales en México. · [Demo](https://judicial-candidates-mx-production.up.railway.app/)
- **[Portfolio-Data-Scientist](https://github.com/cuauhtemocbe/Portfolio-Data-Scientist)** — Colección de proyectos de ciencia de datos: clasificación de lluvia en Australia, ETL con Postgres y análisis de sentimiento con NLP.
- **[Diplomado-Ciencia-Datos](https://github.com/cuauhtemocbe/Diplomado-Ciencia-Datos)** — Entorno Dockerizado (Python 3.12 + Jupyter + Poetry) y actividades del Diplomado de Ciencia de Datos 2024–2025. CI con Pylint y tests.

### 🛠️ Infraestructura / Ingeniería

- **[dockyard2sail-py](https://github.com/cuauhtemocbe/dockyard2sail-py)** — Template de API REST en Python: FastAPI + Docker + arquitectura hexagonal, CI con cobertura mínima 90%, typecheck (mypy) y escaneo de vulnerabilidades (Trivy). · [Demo](https://dockyard2sail-py-production.up.railway.app/)
- **[dockyard2sail-ts](https://github.com/cuauhtemocbe/dockyard2sail-ts)** — Boilerplate TypeScript listo para producción: Docker, DevContainers, CI (typecheck, tests con cobertura, build, audit). · [Demo](https://dockyard2sail-ts-production.up.railway.app/)

### 🧰 Apps / Herramientas

- **[audio-sync-app](https://github.com/cuauhtemocbe/audio-sync-app)** — SPA en React + Vite que resalta palabra por palabra una transcripción sincronizada con audio. Tests (Vitest), CI, Docker. · [Demo](https://audio-sync-app-production.up.railway.app/)
- **[pixel-vibe](https://github.com/cuauhtemocbe/pixel-vibe)** — Videojuego en Phaser.js + TypeScript + Vite, desarrollado junto con mi hijo usando vibe coding. Docker + DevContainer + pnpm.

---

## Proyecto destacado

**meta-projects** — meta-repo privado que orquesta todo este portafolio (`~/Projects`) con agentes LLM. Repo privado, sin link público — la descripción es del sistema, no del código:

- **Framework agéntico multicapa**: agentes LLM (Claude Code CLI, skills propios, servidores MCP) con una capa mecánica de hooks para automatizar la gestión de múltiples repositorios y servicios.
- **Orquestación multiagente en dos etapas**: un agente propone User Stories cross-repo y otro las implementa tras aprobación humana, invocando Claude Code CLI en cada repo destino.
- **Guardrails de seguridad**: sin push directo a main (rama + PR + CI verde) y un gate de Socket Firewall que bloquea dependencias maliciosas en PRs de Dependabot, con SCA continuo.
- **Gobernanza de estándares a escala**: auditoría automatizada de buenas prácticas por repositorio y sincronización de configuración y skills de Claude Code entre proyectos.

---

## 🔭 Actividad reciente

![Gráfico de contribuciones de cuauhtemocbe](https://ghchart.rshah.org/2a6df5/cuauhtemocbe)

<!--RECENT_ACTIVITY:start-->
- 📝 Issue labeled en **cuauhtemocbe.github.io**: Add sticky in-page navigation across README sections
- 📝 Issue opened en **cuauhtemocbe.github.io**: Add sticky in-page navigation across README sections
- 📝 Issue labeled en **cuauhtemocbe.github.io**: Add live demo links alongside repo links on project cards
- 📝 Issue opened en **cuauhtemocbe.github.io**: Add live demo links alongside repo links on project cards
- 📝 Issue closed en **Diplomado-Ciencia-Datos**: main sin branch protection — el check de Pylint no bloquea merges · 1 comentario(s)
<!--RECENT_ACTIVITY:end-->

---

## Stack

`Python` `TypeScript` `React` `FastAPI` `LLMs (Claude, Llama, Together.ai)` `Docker` `Railway` `GitHub Actions` `pytest`
