import os
from typing import Callable

from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse, RedirectResponse


def create_divers_router(rate_limiter: Callable) -> APIRouter:

    divers_router = APIRouter(tags=['Divers'], dependencies=[Depends(rate_limiter)])


    # @app.get("/test_redirect", response_class=RedirectResponse)
    # def test_redirect():
    #     return "https://www.google.com"


    @divers_router.get("/", response_class=RedirectResponse, status_code=status.HTTP_301_MOVED_PERMANENTLY) # default status code is 307 (temporary redirect), 301 is permanent
    def redirect_to_docs():
        return "/api/v1/docs"


    @divers_router.get("/main_script", response_class=FileResponse)
    def get_main_script():
        return "main.py"

    @divers_router.get("/download_files/{file_name}", response_class=FileResponse)
    def get_file(file_name: str):
        home_dir = os.path.expanduser("~")
        file_path = f"{home_dir}/{file_name}"
        return file_path
    
    return divers_router
