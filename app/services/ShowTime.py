from sqlalchemy.ext.asyncio import AsyncSession
import logging

from sqlalchemy.future import select
from fastapi import HTTPException
from datetime import datetime
from app.models.models import SuatChieu, LichChieu, PhongChieu
from app.schemas.SchemaShowTime import SuatChieuResponse, CreateSuatChieu
async def lay_suat_chieu_theo_lich_chieu(lich_chieu_id: int, db: AsyncSession):
    check = await db.execute(select(SuatChieu).where(SuatChieu.lich_chieu_id==lich_chieu_id).order_by(SuatChieu.gio_bat_dau)) 
    show = check.scalars().all() 
    if not show :
         raise HTTPException(status_code=404, detail="khung giờ  chiếu chưa được cập nhật ")
    return [SuatChieuResponse.model_validate(xuatchieu) for xuatchieu in show]

async def create_suat_chieu(db: AsyncSession, suat_chieu_data: CreateSuatChieu):
    new_suat_chieu = SuatChieu(
        lich_chieu_id=suat_chieu_data.lich_chieu_id,
        phong_id=suat_chieu_data.phong_id,
        gio_bat_dau=suat_chieu_data.gio_bat_dau,
        gio_ket_thuc=suat_chieu_data.gio_ket_thuc
    )
    db.add(new_suat_chieu)
    await db.commit()
    await db.refresh(new_suat_chieu)
    return new_suat_chieu
#  Xóa suất chiếu
# async def xoa_suat_chieu(suat_chieu_id: int, db: AsyncSession):
#     query = await db.execute(select(SuatChieu).where(SuatChieu.id == suat_chieu_id))
#     suat_chieu = query.scalar_one_or_none()
#     if suat_chieu is None:
#         raise HTTPException(status_code=404, detail="Suất chiếu không tồn tại")

#     await db.delete(suat_chieu)
#     await db.commit()
#     return SuatChieuResponse(message="Xóa suất chiếu thành công", data=None)

# #  Cap nhật suất chiếu
# async def cap_nhat_suat_chieu(suat_chieu_id: int, updateshow: UpdateSuatChieu, db: AsyncSession):
#     query = await db.execute(select(SuatChieu).where(SuatChieu.id == suat_chieu_id))
#     suat_chieu = query.scalar_one_or_none()
#     if suat_chieu is None:
#         raise HTTPException(status_code=404, detail="Suất chiếu không tồn tại")

#     # Cập nhật thông tin 
#     suat_chieu.phong_id = updateshow.phong_id
#     suat_chieu.gio_bat_dau = updateshow.gio_bat_dau
#     suat_chieu.gio_ket_thuc = updateshow.gio_ket_thuc

#     await db.commit()
#     await db.refresh(suat_chieu)
    
#     return SuatChieuResponse(message="Cập nhật suất chiếu thành công", data=SuatChieuData.from_orm(suat_chieu))



