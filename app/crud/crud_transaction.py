# from sqlalchemy import select
# from sqlalchemy.orm import Session

# from app.crud.base import CRUD
# from app.models.transaction import Transaction, TxStatus


# class CRUDTransaction(CRUD[Transaction]):
#     def select_for_update(self, db: Session, id: int) -> Transaction:
#         return (
#             db.query(Transaction).filter(Transaction.id == id).with_for_update().one()
#         )

#     def get_unsent_transactions_ids(self, db: Session) -> list[int]:
#         return db.scalars(
#             select(Transaction.id).filter(
#                 Transaction.status.in_(
#                     (
#                         TxStatus.WAITING_FOR_SEND,
#                         TxStatus.CONTRACT_LOGIC_ERROR,
#                         TxStatus.VALUE_ERROR,
#                     )
#                 )
#             )
#         ).all()

#     def get_pending_transactions_ids(self, db: Session) -> list[int]:
#         return db.scalars(
#             select(Transaction.id).filter(Transaction.status == TxStatus.PENDING)
#         ).all()


# transaction = CRUDTransaction(Transaction)
