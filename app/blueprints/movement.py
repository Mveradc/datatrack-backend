import enum
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.movement import Movement
from app.schemas.movement import MovementCreate, MovementOut, Headers
from app.core.database import get_psql
from app.core.auth import get_current_user
import uuid
import csv
from app.utils.csv_parser import parse_csv_with_header_detection

router = APIRouter(prefix="/movements", tags=["Movements"])

@router.get("/", response_model=list[MovementOut])
def get_movements(db: Session = Depends(get_psql), user: User = Depends(get_current_user)):
    if user.is_admin:
        return db.query(Movement).all()
    else:
        return db.query(Movement).filter(Movement.user_id == user.id).all()


# Insert movements manually (JSON)
@router.post("/manual", response_model=MovementOut)
def create_movement_manual(
    movement: MovementCreate,
    db: Session = Depends(get_psql),
    current_user: User = Depends(get_current_user)
):
    new_movement = Movement(
        user_id=current_user.id,
        concept=movement.concept,
        amount=movement.amount,
        date=movement.date,
        agg_concept=movement.agg_concept,
        extraordinary=movement.extraordinary,
        balance=movement.balance
    )
    db.add(new_movement)
    db.commit()
    db.refresh(new_movement)
    return new_movement

# Insert movements via CSV
@router.post("/csv")
async def create_movement_csv(
    movement: UploadFile = File(...),
    date: str = Form("fecha"),
    concept: str = Form("concepto"),
    amount: str = Form("importe"),
    balance: str = Form("saldo"),
    sep: str = Form(";"),
    db: Session = Depends(get_psql),
    current_user: User = Depends(get_current_user)
):
    if not movement.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    # Headers validation
    Headers(date=date, concept=concept, amount=amount, balance=balance)
    
    dict_headers = {
        date.lower() : "date",
        concept.lower() : "concept",
        amount.lower() : "amount",
        balance.lower() : "balance"
    }
    import io
    with movement.file as file_obj:
        text_file = io.TextIOWrapper(file_obj, encoding='utf-8')
        df = parse_csv_with_header_detection(text_file, headers=dict_headers, sep=sep)
    for movement in df.to_dict(orient='records'):
        db.add(Movement(
            user_id=current_user.id,
            concept=movement["concept"],
            amount=movement["amount"],
            date=movement["date"],
            balance=movement["balance"]
        ))
    db.commit()
    return {"detail": "Movements created successfully"}

@router.put("/{movement_id}")
def update_movement(
    movement_id: list[uuid.UUID],
    movement: MovementCreate,
    db: Session = Depends(get_psql),
    current_user: User = Depends(get_current_user)
):
    existing_movements = db.query(Movement).filter(Movement.id.in_(movement_id), Movement.user_id == current_user.id).all()
    if not existing_movements:
        raise HTTPException(status_code=404, detail="Movements not found")

    for existing_movement in existing_movements:
        existing_movement.concept = movement.concept
        existing_movement.amount = movement.amount
        existing_movement.date = movement.date
    existing_movement.agg_concept = movement.agg_concept
    existing_movement.extraordinary = movement.extraordinary
    existing_movement.balance = movement.balance
    
    db.commit()
    db.refresh(existing_movement)
    return {"detail": "Movements updated successfully", "movements": existing_movements}

@router.delete("/clear-all")
def clear_movements(
    db: Session = Depends(get_psql),
    current_user: User = Depends(get_current_user)
):
    '''
    Function to clear all movements for the current user.
    This is useful for testing purposes or when the user wants to reset their movements.
    '''
    movements = db.query(Movement).filter(Movement.user_id == current_user.id).all()
    for movement in movements:
        db.delete(movement)
    db.commit()
    return {"detail": "All movements cleared successfully"}

@router.delete("/{movement_id}", response_model=MovementOut)
def delete_movement(
    movement_id: uuid.UUID,
    db: Session = Depends(get_psql),
    current_user: User = Depends(get_current_user)
):
    movement = db.query(Movement).filter(Movement.id == movement_id, Movement.user_id == current_user.id).first()
    if not movement:
        raise HTTPException(status_code=404, detail="Movement not found")
    
    db.delete(movement)
    db.commit()
    return movement
