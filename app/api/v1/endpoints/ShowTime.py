from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.Database import get_db
from app.schemas.SchemaShowTime import  SuatChieuData  , CreateSuatChieu, UpdateSuatChieu, SuatChieuResponse
from app.services.ShowTime import lay_suat_chieu_theo_lich_chieu  , create_suat_chieu    # tao_suat_chieu, xoa_suat_chieu, cap_nhat_suat_chieu, 

router = APIRouter(prefix="/admin", tags=["Suất chiếu"])


@router.post("/suat-chieu/", response_model=SuatChieuResponse)
async def add_suat_chieu(suat_chieu: CreateSuatChieu, db: AsyncSession = Depends(get_db)):
    new_suat_chieu = await create_suat_chieu(db, suat_chieu)
    return {"message": "Suất chiếu được tạo thành công", "data": new_suat_chieu}

# #   xóa suất chiếu
# @router.delete("/suat-chieu/{suat_chieu_id}", response_model=SuatChieuResponse)
# async def delete_suat_chieu(suat_chieu_id: int, db: AsyncSession = Depends(get_db)):
#     return await xoa_suat_chieu(suat_chieu_id, db)

# #  Cập nhật suất chiếu
# @router.put("/suat-chieu/{suat_chieu_id}", response_model=SuatChieuResponse)
# async def update_suat_chieu(suat_chieu_id: int, updateshow: UpdateSuatChieu, db: AsyncSession = Depends(get_db)):
#     return await cap_nhat_suat_chieu(suat_chieu_id, updateshow, db)

# lấy danh sách suất chiếu 
@router.get("/lich-chieu/{lich_chieu_id}", response_model=list[SuatChieuData])
async def get_suat_chieu_theo_lich_chieu(lich_chieu_id: int, db: AsyncSession = Depends(get_db)):
    return await lay_suat_chieu_theo_lich_chieu(lich_chieu_id, db)

