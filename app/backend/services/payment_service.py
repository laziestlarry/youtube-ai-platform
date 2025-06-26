import uuid

from sqlalchemy.orm import Session

from app.backend import crud, schemas


class PaymentService:
    def payout_to_payoneer(
        self, db: Session, user_id: int, amount: float
    ) -> schemas.TransactionInDB:
        """
        Simulates initiating a payout to Payoneer.
        """
        print(f"Initiating Payoneer payout of ${amount} for user {user_id}...")

        # 1. Create a transaction record in our database
        transaction_in = schemas.TransactionCreate(
            user_id=user_id,
            amount=-abs(amount),  # Payouts are negative
            type="payout",
            status="processing",
            provider="payoneer",
        )
        db_transaction = crud.transaction.create(db, obj_in=transaction_in)

        # 2. TODO: Make the actual API call to Payoneer
        # provider_id = payoneer_sdk.payouts.create(...)
        # For now, we simulate a success and update our record.
        provider_id = f"payoneer_{uuid.uuid4()}"
        updated_transaction = crud.transaction.update(
            db,
            db_obj=db_transaction,
            obj_in={"status": "completed", "provider_transaction_id": provider_id},
        )

        print(f"Payoneer payout successful. Transaction ID: {updated_transaction.id}")
        return updated_transaction
