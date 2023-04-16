from app import crud, custom_types
from app.core.config import settings
from app.db.session import SessionLocal


def init_db():
    db = SessionLocal()

    # crud.currency.get_or_create(
    #     db,
    #     obj_in={
    #         "symbol": "ETH",
    #         "blockchain": custom_types.Blockchain.ethereum.value,
    #     },
    # )


if __name__ == "__main__":
    print("Initializing data ...")
    init_db()
    print("All data successfully initialized!")
