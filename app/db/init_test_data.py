import random
from uuid import uuid4

from app import crud, models
from app.db.session import SessionLocal


def init_db():
    db = SessionLocal()

    currency = crud.currency.get_by_symbol_and_blockchain(db, "ETH", "ethereum")

    users = []
    for _ in range(5):
        user = {
            "id": str(uuid4()),
            "name": f"Client #{random.randint(0, 100000)}",
        }
        users.append(
            crud.user.create(
                db=db,
                obj_in=user,
            )
        )

    users_ids = [user.id for user in users]
    for _ in range(50):
        user_id = random.choice(users_ids)
        deposit_amount = random.randint(5000000, 50000000) / 100
        # crud.deposit.create(
        #     db=db,
        #     obj_in={
        #         "user_id": user_id,
        #         "amount": deposit_amount,
        #         "currency_id": currency.id,
        #         "status": models.Deposit.DepositStatus.SUCCESS,
        #     },
        # )
        # crud.withdrawal.create(
        #     db=db,
        #     obj_in={
        #         "user_id": user_id,
        #         "currency_id": currency.id,
        #         "amount": deposit_amount - 10000,
        #         "recipient_address": "0x48BcB848cd3de723Ec681a6c82b340E5A71F62C3",
        #     },
        # )


if __name__ == "__main__":
    init_db()
