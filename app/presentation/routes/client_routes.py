from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.presentation.schemas.client_schema import (
    CreateClientRequest,
    UpdateClientRequest,
    ClientResponse
)
from app.application.usecases.create_client import CreateClientUseCase
from app.application.usecases.get_client import (GetClientUseCase , GetClientByNameUseCase)
from app.application.usecases.get_all_client import GetAllClientUseCase
from app.application.usecases.update_client import UpdateClientUseCase
from app.application.usecases.delete_client import DeleteClientUseCase
from app.application.usecases.client_exists import ClientExistsUseCase
from app.application.usecases.get_account_statment import GetAccountStatementUseCase
from app.domain.repositories.client_repository import ClientRepository
from app.infrastructure.repositories.client_repository_impl import ClientRepositoryImpl
from app.infrastructure.database.session import get_db
from app.presentation.routes.dependencies import get_current_user_id
from sqlalchemy.orm import Session
import traceback

router = APIRouter(prefix="/api/clients", tags=["clients"])


def get_client_repository(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> ClientRepository:
    repository = ClientRepositoryImpl(db)
    repository.set_user_id(user_id)
    return repository


@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def create_client(
    request: CreateClientRequest,
    repository: ClientRepository = Depends(get_client_repository)
):
    try:
        use_case = CreateClientUseCase(repository)
        created_client = use_case.execute(
            client_id=request.client_id,
            client_name=request.client_name,
            client_email=request.client_email,
            phone_numbers=request.phone_numbers,
            surety=request.surety,
            surety_num=request.surety_num,
            address=request.address
        )
        return created_client
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(e)}")


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: str,
    repository: ClientRepository = Depends(get_client_repository)
):
    try:
        use_case = GetClientUseCase(repository)
        client = use_case.execute(client_id=client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with ID {client_id} not found"
            )
        return client
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(e)}")

@router.get("/name/{client_name}", response_model=List[ClientResponse])
async def get_client_by_name(
    client_name: str,
    repository: ClientRepository = Depends(get_client_repository)
):
    try:
        use_case = GetClientByNameUseCase(repository)
        clients = use_case.execute(client_name=client_name)
        return clients
    except ValueError as e:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/", response_model=List[ClientResponse])
async def get_all_clients(
    repository: ClientRepository = Depends(get_client_repository)
):
    try:
        use_case = GetAllClientUseCase(repository)
        clients = use_case.execute()
        return clients
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(e)}")


@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: str,
    request: UpdateClientRequest,
    repository: ClientRepository = Depends(get_client_repository)
):
    try:
        exists_use_case = ClientExistsUseCase(repository)
        if not exists_use_case.execute(client_id=client_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with ID {client_id} not found"
            )

        from app.domain.models.client_model import Client, Phone

        phone_objects = [Phone(number) for number in request.phone_numbers]

        updated_client = Client(
            client_id=client_id,
            client_name=request.client_name,
            client_email=request.client_email,
            phone_numbers=phone_objects,
            surety=request.surety,
            surety_num=request.surety_num,
            address=request.address
        )

        use_case = UpdateClientUseCase(repository)
        result = use_case.execute(client_id=client_id, client=updated_client)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with ID {client_id} not found"
            )

        return result
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(e)}")


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: str,
    repository: ClientRepository = Depends(get_client_repository)
):
    try:
        exists_use_case = ClientExistsUseCase(repository)
        if not exists_use_case.execute(client_id=client_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with ID {client_id} not found"
            )

        use_case = DeleteClientUseCase(repository)
        success = use_case.execute(client_id=client_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with ID {client_id} not found"
            )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{client_id}/account-statement")
def get_account_statement(
    client_id: str,
    repository: ClientRepository = Depends(get_client_repository)
   
):
    try:
        use_case = GetAccountStatementUseCase(repository)
        return use_case.execute(client_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))    