# import logging
# from datetime import datetime
# from typing import Any

# from eth_typing.evm import ChecksumAddress
# from sqlalchemy.orm import Session
# from web3.exceptions import ContractLogicError, TransactionNotFound

# from app import crud, models
# from app.core.config import EthereumSettings
# from app.db.session import SessionLocal


# class TransactionsService:
#     logger = logging.getLogger("transactions_service")

#     def _send_transaction(
#         self,
#         network: EthereumSettings,
#         to: ChecksumAddress,
#         data: str,
#         nonce: int | None = None,
#         gas_price: int | None = None,
#         gas: int | None = None,
#     ) -> tuple[str, dict[str, Any]]:
#         w3 = network.w3

#         if nonce is None:
#             nonce = w3.eth.get_transaction_count(network.account_address, "pending")

#         if gas_price is None:
#             gas_price = w3.eth.gas_price

#         tx_params = {
#             "from": network.account_address, #AAAAAAAAAAAAAAAAААААААААААААААААААААААААААААА
#             "to": to,
#             "data": data,
#         }
#         gas = w3.eth.estimate_gas(tx_params)
#         more_tx_params = {
#             "nonce": nonce,
#             "gas": gas,
#             "gasPrice": gas_price,
#         }
#         tx_params.update(more_tx_params)
#         w3.eth.call(tx_params)  # dry-run

#         signed_tx = w3.eth.account.sign_transaction(tx_params, network.private_key)
#         tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction).hex()

#         return tx_hash, tx_params

#     def _speed_up_tx_if_needed(
#         self, db: Session, network: EthereumSettings, tx: models.Transaction
#     ):
#         diff_seconds = (datetime.now() - tx.sent_at).seconds
#         if diff_seconds > network.speed_up_interval:
#             gas_price = int(int(tx.gas_price) * network.speed_up_gas_price_mul)

#             try:
#                 tx_hash, tx_params = self._send_transaction(
#                     network, tx.to, tx.nonce, gas_price
#                 )
#             except (ContractLogicError, ValueError) as e:
#                 self.logger.warning(
#                     f"cannot speed up tx with id={tx.id} because of {repr(e)}"
#                 )
#                 return

#             tx.tx_hashes.append(tx_hash)
#             tx.gas_limit = tx_params["gas"]
#             tx.gas_price = gas_price
#             db.commit()

#     def _process_pending_transaction(
#         self, db: Session, network: EthereumSettings, id: int, success_handler
#     ) -> None:
#         tx = crud.transaction.select_for_update(db, id)
#         for tx_hash in tx.tx_hashes:
#             try:
#                 receipt = network.w3.eth.get_transaction_receipt(tx_hash)
#             except TransactionNotFound:
#                 continue

#             try:
#                 if receipt["status"] == 1:
#                     tx.status = models.TxStatus.SUCCESS
#                     db.commit()
#                     success_handler(db, receipt)
#                     return
#                 elif receipt["blockNumber"] is None:
#                     continue
#                 else:
#                     tx.status = models.TxStatus.FAIL
#                     db.commit()
#                     return
#             except KeyError:
#                 continue

#         if tx.status == models.TxStatus.PENDING:
#             self._speed_up_tx_if_needed(db, network, tx)

#     def _process_unsent_transaction(
#         self, db: Session, network: EthereumSettings, id: int
#     ) -> None:
#         tx = crud.transaction.select_for_update(db, id)
#         try:
#             tx_hash, tx_params = self._send_transaction(network, tx.to, tx.data)
#             crud.transaction.update(
#                 db,
#                 db_obj=tx,
#                 update_data={
#                     "status": models.TxStatus.PENDING,
#                     "tx_hashes": [tx_hash],
#                     "nonce": tx_params["nonce"],
#                     "gas_price": tx_params["gasPrice"],
#                     "gas_limit": tx_params["gas"],
#                 },
#             )
#         except ContractLogicError:
#             tx.status = models.TxStatus.CONTRACT_LOGIC_ERROR
#             db.commit()
#         except ValueError:
#             tx.status = models.TxStatus.VALUE_ERROR
#             db.commit()

#     def process_pending_transactions(self, network: EthereumSettings, success_handler) -> None:
#         with SessionLocal() as db:
#             for id in crud.transaction.get_pending_transactions_ids(db):
#                 self._process_pending_transaction(db, network, id, success_handler)

#     def process_unsent_transactions(self, network: EthereumSettings) -> None:
#         with SessionLocal() as db:
#             for id in crud.transaction.get_unsent_transactions_ids(db):
#                 self._process_unsent_transaction(db, network, id)

#     def add_transaction_to_queue(
#         self,
#         db: Session,
#         to: ChecksumAddress,
#         data: str,
#     ) -> models.Transaction:
#         return crud.transaction.create(db, obj_in={"to": to, "data": data})
