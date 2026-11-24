from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.calculation_factory import CalculationFactory
from app.models import Calculation
from app.schemas import CalculationCreate, CalculationRead
from app.users import get_session

router = APIRouter(prefix="/calculations", tags=["Calculations"])


@router.get("", response_model=list[CalculationRead])
def browse_calculations(session: Session = Depends(get_session)):
    return session.scalars(select(Calculation).order_by(Calculation.id)).all()


@router.get("/{calculation_id}", response_model=CalculationRead)
def read_calculation(calculation_id: int, session: Session = Depends(get_session)):
    calculation = session.get(Calculation, calculation_id)
    if calculation is None:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calculation


@router.post("", response_model=CalculationRead, status_code=status.HTTP_201_CREATED)
def add_calculation(data: CalculationCreate, session: Session = Depends(get_session)):
    result = CalculationFactory.calculate(data)
    calculation = Calculation(a=data.a, b=data.b, type=data.type, result=result)
    session.add(calculation)
    session.commit()
    session.refresh(calculation)
    return calculation


@router.put("/{calculation_id}", response_model=CalculationRead)
def edit_calculation(calculation_id: int, data: CalculationCreate, session: Session = Depends(get_session)):
    calculation = session.get(Calculation, calculation_id)
    if calculation is None:
        raise HTTPException(status_code=404, detail="Calculation not found")
    calculation.a = data.a
    calculation.b = data.b
    calculation.type = data.type
    calculation.result = CalculationFactory.calculate(data)
    session.commit()
    session.refresh(calculation)
    return calculation


@router.delete("/{calculation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(calculation_id: int, session: Session = Depends(get_session)):
    calculation = session.get(Calculation, calculation_id)
    if calculation is None:
        raise HTTPException(status_code=404, detail="Calculation not found")
    session.delete(calculation)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
