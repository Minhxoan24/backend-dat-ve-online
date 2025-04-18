from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api.v1.endpoints import ( websocket ,Account ,Booking ,film ,FilmSearch ,historyfilm ,MovieCommetntary ,
                                  Schedule ,ShowTime  , ChairList, ChooseChair,payment  ,CommentFilm )





app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả origin (hoặc chỉ định origin cụ thể)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(websocket.router)
app.include_router(Account.router)
app.include_router(film.router)
app.include_router(Booking.router)
app.include_router(Schedule.router)
app.include_router(ShowTime.router)
app.include_router(ChairList.router)
app.include_router(ChooseChair.router)
app.include_router(historyfilm.router)
app.include_router(FilmSearch.router)
app.include_router(MovieCommetntary.router)
app.include_router(payment.router)
app.include_router(CommentFilm.router)







# app.include_router()
# .\venv\Scripts\activate
#  uvicorn app.main:app --reload
# http://10.0.2.2:8000/account/
# uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 
#http://192.168.1.239:8000
