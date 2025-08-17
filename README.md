# Proyecto de Automatización Web (Python + Behave + Selenium + Allure + POM)

Proyecto base para pruebas E2E usando **Behave** (BDD), **Selenium WebDriver**, reportes con **Allure**, y **Page Object Model (POM)**.

---

## 📁 Estructura 
```
webAutomation/
├─ features/
│  ├─ login.feature
│  └─ steps/
│     └─ login_steps.py
├─ pages/
│  └─ login_page.py
├─ environment.py
├─ requirements.txt
├─ behave.ini            # opcional, recomendado
└─ reports/
   ├─ allure-results/
   └─ allure-report/
```

---

## 🔧 Requisitos
- Python 3.11+ (probado con 3.13)
- Google Chrome instalado
- **Allure CLI** (para abrir reportes):
  - macOS: `brew install allure`

---

## 🚀 Configuración rápida
```bash
# 1) Crear y activar un entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 2) Instalar dependencias
python -m pip install -U pip
pip install -r requirements.txt
```

### Variables de entorno (opcional)
Crea un archivo `.env` en la raíz para parametrizar:
```env
BASE_URL=https://www.saucedemo.com
BROWSER=chrome
HEADLESS=true
SCREENSHOTS_EVERY_STEP=true
```
> `environment.py` las lee automáticamente. `HEADLESS=true` corre sin abrir ventana; pon `false` para ver el navegador.

---

## 🧩 Qué hay en el proyecto
- **POM**: `pages/login_page.py` contiene localizadores y acciones de la página de login.
- **Steps**: `features/steps/login_steps.py` mapea Given/When/Then al POM.
- **Hooks**: `environment.py` levanta/cierra el navegador por escenario y adjunta screenshots a Allure.
- **Feature**: `features/login.feature` con escenarios de login exitoso y de error.

---

## ▶️ Cómo ejecutar
### Opción A – Comando directo con Allure
```bash
# Genera resultados Allure + salida pretty
python -m behave -f "allure_behave.formatter:AllureFormatter" -o reports/allure-results -f pretty
```

### Opción B – Configurar `behave.ini` (recomendado)
Crea `behave.ini` con:
```ini
[behave]
paths = features
color = true
stdout_capture = no
stderr_capture = no
log_capture = no
format = pretty

[behave.userdata]
allure_report_dir = reports/allure-results

[behave.formatters]
allure = allure_behave.formatter:AllureFormatter
```
Ejecuta:
```bash
python -m behave -f allure
# o con pretty también
python -m behave -f allure -f pretty
```

---

## 📊 Ver el reporte de Allure
```bash
# Servidor local (lo abre en el navegador)
allure serve reports/allure-results

# Generar sitio estático y abrirlo
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

---

## 🧱 Page Object Model (POM)
`pages/login_page.py` define métodos típicos del POM:
- `open()` para abrir la URL base
- `login(user, pwd)` para autenticarse
- `assert_logged_in()` verifica que el inventario se muestre
- `assert_error_contains(text)` valida mensaje de error

Los steps consumen ese POM en `features/steps/login_steps.py`:
- `Given que estoy en la página de login` → crea la página y abre la URL
- `When inicio sesión con usuario "..." y clave "..."` → llama a `login`
- `Then debería ver el inventario` → aserción de login
- `Then debería ver un mensaje de error que contiene "..."` → aserción de error

`environment.py` arranca Chrome con opciones (headless configurable), usa **webdriver-manager** para el driver, y adjunta **screenshots en cada paso** al reporte de Allure.

---

## 🏷️ Filtrado por etiquetas / Features puntuales
```bash
# Solo escenarios con etiqueta @ui
python -m behave -t @ui -f "allure_behave.formatter:AllureFormatter" -o reports/allure-results -f pretty

# Solo un feature
python -m behave features/login.feature -f "allure_behave.formatter:AllureFormatter" -o reports/allure-results -f pretty
```

---

## 🛠️ Troubleshooting
- **`ModuleNotFoundError: No module named 'behave'`**: Activa el venv y reinstala: `source .venv/bin/activate && pip install -r requirements.txt`.
- **`TypeError: ... Path(..., NoneType)`**: Asegúrate de que `-o` se aplique al formateador **Allure** y no a `pretty`. Usa el orden: `-f allure_behave.formatter:AllureFormatter -o reports/allure-results -f pretty` o configura `behave.ini`.
- **`FileExistsError: ... reports/allure-results`**: Si existe **un archivo** con ese nombre, elimínalo y crea el directorio: `rm -f reports/allure-results && mkdir -p reports/allure-results`.
- **`zsh: parse error near ')'`**: Evita pegar comentarios o caracteres especiales; usa comillas en el nombre del formateador.
- **Comentarios en línea del INI**: No pongas comentarios al final de la línea (p. ej., `format = pretty  # comentario`). Haz el comentario en su propia línea.

---

## 🚦 CI/CD (GitHub Actions)
**Workflow:** `.github/workflows/behave-allure.yml`

**¿Qué hace?**
- Instala dependencias y configura Chrome headless.
- Ejecuta `behave` con el formateador de **Allure** para generar `reports/allure-results`.
- Genera el **HTML** de Allure en `reports/allure-report`.
- Sube el reporte como **artifact** y, en `push`, lo publica en **GitHub Pages**.

**Variables usadas en el workflow**
```
BROWSER=chrome
HEADLESS=true
ALLURE_RESULTS_DIR=reports/allure-results
ALLURE_REPORT_DIR=reports/allure-report
```

**Cómo ver resultados en CI**
- **Artifact:** “allure-report” (descargable desde la pestaña del job).
- **GitHub Pages (en push):** el enlace queda en el *Run summary* del workflow.

**Ejecutar lo mismo en local**
```bash
python -m behave -f "allure_behave.formatter:AllureFormatter" -o reports/allure-results -f pretty
allure serve reports/allure-results
```

**Badge opcional (reemplaza OWNER/REPO y archivo .yml si difiere):**
```md
![CI](https://github.com/OWNER/REPO/actions/workflows/behave-allure.yml/badge.svg)
```

---

## ✅ Comandos rápidos
```bash
# Setup
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

# Run con Allure (sin behave.ini)
python -m behave -f "allure_behave.formatter:AllureFormatter" -o reports/allure-results -f pretty

# Ver reporte
allure serve reports/allure-results
```
