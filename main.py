import logging
import os

from dotenv import load_dotenv

from frontend.app import app

load_dotenv()

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Environment-Konfiguration
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", "8080"))
    print(port)

    logger.info(f"Starting ChatBot application on {host}:{port}")
    logger.info(f"Debug mode: {debug}")

    try:
        app.run(debug=debug, host=host, port=port)
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        raise
