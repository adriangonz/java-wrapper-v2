import logging

logger = logging.getLogger(__name__)


class NoJava:
    def predict(self, X, feature_names=[], meta=None):
        logger.debug(f"[PYTHON] Input was {len(X)} elemnets long")

        total = sum(X)
        logger.debug(f"[PYTHON] Total was {total}")

        return [total]
