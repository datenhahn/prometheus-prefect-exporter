import os
import logging
import time

from metrics.metrics import PrefectMetrics
from metrics.healthz import PrefectHealthz
from prometheus_client import start_http_server, REGISTRY


if __name__ == "__main__":
    """
    Main entry point for the PrefectMetrics exporter.
    """

    # Get environment variables or use default values
    loglevel = str(os.getenv("LOG_LEVEL", "INFO"))
    max_retries = int(os.getenv("MAX_RETRIES", "3"))
    metrics_port = int(os.getenv("METRICS_PORT", "8000"))
    offset_minutes = int(os.getenv("OFFSET_MINUTES", "5"))
    url = str(os.getenv("PREFECT_API_URL", "http://localhost:4200/api"))
    api_key = str(os.getenv("PREFECT_API_KEY", ""))

    # Configure logging
    logging.basicConfig(
        level=loglevel, format="%(asctime)s - %(name)s - [%(levelname)s] %(message)s"
    )
    logger = logging.getLogger("prometheus-prefect-exporter")

    # Configure headers for HTTP requests
    headers = {"accept": "application/json", "Content-Type": "application/json"}

    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    # check endpoint
    PrefectHealthz(
        url=url, headers=headers, max_retries=max_retries, logger=logger
    ).get_health_check()

    # Create an instance of the PrefectMetrics class
    metrics = PrefectMetrics(
        url=url,
        headers=headers,
        offset_minutes=offset_minutes,
        max_retries=max_retries,
        logger=logger,
    )

    # Register the metrics with Prometheus
    logger.info("Inizializing metrics...")
    REGISTRY.register(metrics)

    # Start the HTTP server to expose Prometheus metrics
    start_http_server(metrics_port)
    logger.info(f"Exporter listening on port :{metrics_port}")

    # Run the loop to collect Prefect metrics
    while True:
        time.sleep(5)
