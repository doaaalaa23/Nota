from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.presentation.schemas.contract_schema import (
    CreateContractRequest,
    UpdateContractRequest,
    ContractResponse,
)
from app.application.usecases.create_contract import CreateContractUseCase
from app.application.usecases.get_contract import GetContractUseCase
from app.application.usecases.get_all_contract import GetAllContractUseCase
from app.application.usecases.contract_status import GetContractStatusUseCase
from app.application.usecases.update_contract import UpdateContractUseCase
from app.application.usecases.delete_contract import DeleteContractUseCase
from app.application.usecases.contract_exists import ContractExistsUseCase
from app.domain.repositories.contract_repository import ContractRepository
from app.infrastructure.repositories.contract_repository_impl import ContractRepositoryImpl
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.database.session import get_db
from app.presentation.routes.dependencies import get_current_user_id
from sqlalchemy.orm import Session
import traceback

router = APIRouter(prefix="/api/contracts", tags=["contracts"])


def get_contract_repository(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> ContractRepository:
    repository = ContractRepositoryImpl(db)
    repository.set_user_id(user_id)
    return repository


def get_user_repository(
    db: Session = Depends(get_db),
) -> UserRepositoryImpl:
    return UserRepositoryImpl(db)



@router.post("/", response_model=ContractResponse, status_code=status.HTTP_201_CREATED)
async def create_contract(
    request: CreateContractRequest,
    repository: ContractRepository = Depends(get_contract_repository),
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
    user_id: int = Depends(get_current_user_id),
):
    try:
        use_case = CreateContractUseCase(repository, user_repository)
        created = use_case.execute(
            product_id=request.product_id,
            client_id=request.client_id,
            sale_date=request.sale_date,
            sale_price=request.sale_price,
            receiving_price=request.receiving_price,
            installment_value=request.installment_value,
            paying_day=request.paying_day,
            first_installment=request.first_installment,
            user_id=user_id,
        )
        return created
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{contract_id}", response_model=ContractResponse)
async def get_contract(contract_id: str, repository: ContractRepository = Depends(get_contract_repository)):
    try:
        use_case = GetContractUseCase(repository)
        contract = use_case.execute(contract_id=contract_id)
        if not contract:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contract {contract_id} not found")
        return contract
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[ContractResponse])
async def get_all_contracts(repository: ContractRepository = Depends(get_contract_repository)):
    try:
        use_case = GetAllContractUseCase(repository)
        return use_case.execute()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{contract_id}", response_model=ContractResponse)
async def update_contract(
    contract_id: str,
    request: UpdateContractRequest,
    repository: ContractRepository = Depends(get_contract_repository),
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
    user_id: int = Depends(get_current_user_id),
):
    try:
        exists_use_case = ContractExistsUseCase(repository)
        if not exists_use_case.execute(contract_id=contract_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contract {contract_id} not found")

        from app.domain.models.contract_model import Contract as DomainContract

        get_use_case = GetContractUseCase(repository)
        existing_contract = get_use_case.execute(contract_id=contract_id)

        domain_contract = DomainContract(
            product_id=request.product_id,
            client_id=existing_contract.client_id,
            sale_date=request.sale_date,
            sale_price=request.sale_price,
            receiving_price=request.receiving_price,
            installment_value=request.installment_value,
            paying_day=request.paying_day,
            first_installment=request.first_installment,
            contract_id=int(contract_id),
        )

        use_case = UpdateContractUseCase(repository, user_repository)
        updated = use_case.execute(contract_id, domain_contract, user_id=user_id)

        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contract {contract_id} not found")

        return updated
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{contract_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contract(contract_id: str, repository: ContractRepository = Depends(get_contract_repository)):
    try:
        exists_use_case = ContractExistsUseCase(repository)
        if not exists_use_case.execute(contract_id=contract_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contract {contract_id} not found")

        use_case = DeleteContractUseCase(repository)
        success = use_case.execute(contract_id=contract_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contract {contract_id} not found")
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/{contract_id}/status")
def get_status(
    contract_id: int,
    repository: ContractRepository = Depends(get_contract_repository)
      
):
    try:
        use_case = GetContractStatusUseCase(repository)
        status = use_case.execute(contract_id)
    except ValueError:
        traceback.print_exc()
        raise HTTPException(status_code=404, detail="Contract not found")

    return {"status": status}