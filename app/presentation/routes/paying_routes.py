from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.presentation.schemas.paying_schema import (
    CreatePayingRequest,
    UpdatePayingRequest,
    PayingResponse,
)
from app.application.usecases.create_paying import CreatePayingUseCase
from app.application.usecases.get_all_payings import GetAllPayingsUseCase
from app.application.usecases.get_payings_by_contract import GetPayingsByContractUseCase
from app.application.usecases.delete_paying import DeletePayingUseCase
from app.application.usecases.update_paying import UpdatePayingUseCase
from app.domain.repositories.paying_repository import PayingRepository
from app.infrastructure.repositories.paying_repository_impl import PayingRepositoryImpl
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.database.session import get_db
from app.presentation.routes.dependencies import get_current_user_id
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/payings", tags=["payings"])


def get_paying_repository(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> PayingRepository:
    repository = PayingRepositoryImpl(db)
    repository.set_user_id(user_id)
    return repository


def get_user_repository(
    db: Session = Depends(get_db),
) -> UserRepositoryImpl:
    return UserRepositoryImpl(db)


@router.post("/", response_model=PayingResponse, status_code=status.HTTP_201_CREATED)
async def create_paying(
    request: CreatePayingRequest,
    repository: PayingRepository = Depends(get_paying_repository),
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
    user_id: int = Depends(get_current_user_id),
):
    try:
        use_case = CreatePayingUseCase(repository, user_repository)
        created = use_case.execute(
            paid_amount=request.paid_amount,
            contract_id=request.contract_id,
            client_id=request.client_id,
            paying_date=request.paying_date,
            notice=request.notice,
            user_id=user_id,
        )
        return created
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[PayingResponse])
async def get_all_payings(repository: PayingRepository = Depends(get_paying_repository)):
    try:
        use_case = GetAllPayingsUseCase(repository)
        return use_case.execute()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/contract/{contract_id}", response_model=List[PayingResponse])
async def get_payings_by_contract(contract_id: int, repository: PayingRepository = Depends(get_paying_repository)):
    try:
        use_case = GetPayingsByContractUseCase(repository)
        return use_case.execute(contract_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{paying_id}", response_model=PayingResponse)
async def update_paying(
    paying_id: int,
    request: UpdatePayingRequest,
    repository: PayingRepository = Depends(get_paying_repository),
):
    try:
        use_case = UpdatePayingUseCase(repository)
        updated = use_case.execute(
            paying_id=paying_id,
            paid_amount=request.paid_amount,
            paying_date=request.paying_date,
            notice=request.notice,
        )
        return updated
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{paying_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_paying(paying_id: int, repository: PayingRepository = Depends(get_paying_repository)):
    try:
        use_case = DeletePayingUseCase(repository)
        success = use_case.execute(paying_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Paying {paying_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))