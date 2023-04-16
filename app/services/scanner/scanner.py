import atexit
import logging
import threading
import time

from web3.contract import ContractEvent, EventData

from app import crud, models
from app.core.config import EthereumSettings
from app.db.session import SessionLocal
from app.utils import always_restart


class EventScanner(threading.Thread):
    logger = logging.getLogger("event_scanner")

    def __init__(self, network: EthereumSettings, event: ContractEvent, handler):
        super().__init__()
        self.network = network
        self.event = event
        self.handler = handler
        self.db_record: models.EventScanner = None

    def init_db_session(self):
        self.db = SessionLocal()
        atexit.register(lambda: self.db.close())

    def init_db_record(self) -> None:
        self.db_record, _ = crud.event_scanner.get_or_create(
            self.db,
            obj_in={
                "contract_address": self.event.address,
                "event_name": self.event.event_name,
            },
            defaults={"last_processed_block_num": self.network.w3.eth.block_number},
        )

    def get_last_processed_block(self) -> int:
        self.db.refresh(self.db_record)
        return self.db_record.last_processed_block_num

    def save_last_processed_block(self, block_num: int) -> None:
        self.db_record, _ = crud.event_scanner.update_or_create(
            self.db,
            obj_in={
                "contract_address": self.event.address,
                "event_name": self.event.event_name,
            },
            defaults={"last_processed_block_num": block_num},
        )

    def get_events(self, from_block: int, to_block: int) -> list[EventData]:
        return self.event.createFilter(
            fromBlock=from_block, toBlock=to_block
        ).get_all_entries()

    @always_restart
    def start_polling(self):
        self.init_db_session()
        self.init_db_record()
        while True:
            last_block_processed = self.get_last_processed_block()
            last_network_block = self.network.w3.eth.block_number
            last_block_confirmed = last_network_block - self.network.confirmation_blocks

            if last_block_processed >= last_block_confirmed:
                self.logger.info("waiting for blocks...")
                time.sleep(self.network.polling_interval)
                continue

            if (
                last_block_confirmed - last_block_processed
                > self.network.scanning_blocks_max
            ):
                to_block = last_block_processed + self.network.scanning_blocks_max
                sleep_secs = self.network.speedy_polling_interval
            else:
                to_block = last_block_confirmed
                sleep_secs = self.network.polling_interval

            from_block = last_block_processed + 1

            self.logger.info(
                f"scanning {self.event.event_name} [{from_block}, {to_block}] / {last_block_confirmed}"
            )

            events = self.get_events(from_block, to_block)
            for event in events:
                self.logger.info(f"event received {event}")
                self.handler(self.db, event)

            last_block_processed = to_block
            self.save_last_processed_block(last_block_processed)
            time.sleep(sleep_secs)

    def run(self):
        self.start_polling()
