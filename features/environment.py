import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

import allure
from allure_commons.types import AttachmentType

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def before_all(context):
    """
    Carga variables desde .env y configura flags.
    Variables soportadas:
      - BASE_URL (default: https://www.saucedemo.com)
      - BROWSER   (solo 'chrome' soportado aquí; default: chrome)
      - HEADLESS  (true/false; default: true)
      - SCREENSHOTS_EVERY_STEP (true/false; default: true)
    """
    load_dotenv()
    context.base_url = os.getenv("BASE_URL", "https://www.saucedemo.com")
    context.browser_name = os.getenv("BROWSER", "chrome").lower()
    context.headless = os.getenv("HEADLESS", "true").lower() == "true"
    context.screenshots_every_step = os.getenv("SCREENSHOTS_EVERY_STEP", "true").lower() == "true"


def _chrome_options(headless: bool):
    opts = webdriver.ChromeOptions()
    if headless:
        # El nuevo headless mejora estabilidad en Chrome reciente
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1366,768")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    return opts


def before_scenario(context, scenario):
    """
    Arranca el navegador por escenario y toma un screenshot inicial.
    """
    if context.browser_name != "chrome":
        raise RuntimeError(f"Solo soportado Chrome por ahora. Valor recibido: {context.browser_name}")

    options = _chrome_options(context.headless)
    service = ChromeService(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service, options=options)
    context.driver.set_page_load_timeout(30)
    # Mejor usar esperas explícitas en el POM; dejamos implicit a 0
    context.driver.implicitly_wait(0)

    _attach_png(context, f"START - {scenario.name}")


def after_step(context, step):
    """
    Toma screenshot en cada paso (Given/When/Then) con el estado del step.
    """
    if getattr(context, "screenshots_every_step", True):
        status = getattr(step.status, "name", None) if step.status is not None else "unknown"
        name = f"{step.keyword.strip()} {step.name} [{status}]"
        _attach_png(context, name)


def after_scenario(context, scenario):
    """
    Toma screenshot final (pase o falle). Si falla, adjunta uno extra etiquetado como FAILED.
    """
    status = getattr(scenario.status, "name", None) if scenario.status is not None else "unknown"
    _attach_png(context, f"END - {scenario.name} [{status}]")

    if status and status.lower() == "failed":
        _attach_png(context, f"FAILED - {scenario.name}")

    context.driver.quit()


# ---------- Helpers ----------
def _attach_png(context, name: str):
    """
    Adjunta screenshot PNG directamente a Allure y también lo guarda en disco (reports/screenshots).
    No rompe el test si el screenshot falla.
    """
    try:
        png_bytes = context.driver.get_screenshot_as_png()

        # Adjuntar en Allure (en memoria)
        ts = datetime.now().strftime("%H:%M:%S.%f")
        allure.attach(png_bytes, name=f"{name} @ {ts}", attachment_type=AttachmentType.PNG)

        # Guardar en disco
        safe_name = "".join(c if c.isalnum() or c in " -_[]()" else "_" for c in name)
        outdir = Path("reports/screenshots")
        outdir.mkdir(parents=True, exist_ok=True)
        # Evitar ':' en nombres de archivo en macOS/Windows
        ts_fs = ts.replace(":", "-")
        (outdir / f"{safe_name}_{ts_fs}.png").write_bytes(png_bytes)
    except Exception:
        pass
