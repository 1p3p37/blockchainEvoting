import hashlib
import hmac
import json
import logging
import random
import time
from decimal import Decimal
from string import ascii_letters, digits


from app.core.config import settings

logger = logging.getLogger("utils")


def decimal_to_str(d: Decimal) -> Decimal:
    return format(
        d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize(), "f"
    )


def random_string(length: int = 16) -> str:
    return "".join((random.choice(ascii_letters + digits) for _ in range(length)))


def always_restart(func):
    logger = logging.getLogger(f"{func.__name__}_runner")

    def wrapper(self, *args, **kwargs):
        while True:
            try:
                func(self, *args, **kwargs)
            except:
                logger.exception(
                    f"An error occured while executing {func.__name__}, restarting in {settings.ethereum.always_restart_interval} seconds..."
                )
                time.sleep(settings.ethereum.always_restart_interval)

    return wrapper


def get_hmac_signature(msg: bytes | str, secret_key: str | bytes) -> str:
    if isinstance(msg, str):
        # delete spaces
        msg = json.dumps(json.loads(msg), separators=(",", ":")).encode()
    if isinstance(secret_key, str):
        secret_key = bytes(secret_key, "utf-8")

    logger.info(f"JSON msg: {msg}")
    return hmac.new(
        secret_key,
        msg=msg,
        digestmod=hashlib.sha256,
    ).hexdigest()
