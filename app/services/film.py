from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.future import select
from app.models.models import Phim ,LichChieu ,BinhLuan ,Ve 
from app.schemas.SchemaFilm import PhimSimpleResponse ,PhimUpdateSchema ,AddFilm ,AddFilmResponse ,DeleteFilmResponse 
from datetime import date
from sqlalchemy import select, update

# Lấy danh sách phim đang chiếu
async def list_film_showing(db: AsyncSession):
    query = await db.execute(
        select(Phim).where(
            (Phim.ngay_ket_thuc >= date.today()) & (Phim.ngay_khoi_chieu <= date.today())
        )
    )
    list_film = query.scalars().all()

    if not list_film:
        raise HTTPException(status_code=404, detail="Không có phim nào đang chiếu!")

    return [
        PhimSimpleResponse(
            id=film.id,
            title=film.ten_phim,
            image=film.hinh_anh,
            category=film.the_loai,
            trailer=film.trailer,
            duration=film.thoi_luong,
            trang_thai= True
        )
        for film in list_film
    ]

# Lấy danh sách phim sắp chiếu
async def list_film_upcoming(db: AsyncSession):
    query = await db.execute(
        select(Phim).where(Phim.ngay_khoi_chieu > date.today())
    )
    list_film = query.scalars().all()

    if not list_film:
        raise HTTPException(status_code=404, detail="Không có phim nào sắp chiếu!")

    return [
        PhimSimpleResponse(
            id=film.id,
            title=film.ten_phim,
            image=film.hinh_anh,
            category=film.the_loai,
            trailer=film.trailer,
            duration=film.thoi_luong,
            trang_thai= False 
        )
        for film in list_film
    ]
async def add_film(request: AddFilm, db: AsyncSession):
    if request.ngay_khoi_chieu >= request.ngay_ket_thuc:
        raise HTTPException(status_code=400, detail="Ngày khởi chiếu phải trước ngày kết thúc!")

    new_film = Phim(
        ten_phim=request.ten_phim,
        mo_ta=request.mo_ta,
        ngay_khoi_chieu=request.ngay_khoi_chieu,
        ngay_ket_thuc=request.ngay_ket_thuc,
        the_loai=request.the_loai,
        dao_dien=request.dao_dien,
        thoi_luong=request.thoi_luong,
        dien_vien=request.dien_vien,
        hinh_anh=request.hinh_anh,
        trailer=request.trailer
    )

    db.add(new_film)
    await db.commit()
    await db.refresh(new_film)
    return AddFilmResponse(message="Thêm phim thành công")

# Xóa phim
# async def delete_film(id_film: int, db: AsyncSession):
#     # Bước 1: Kiểm tra phim có tồn tại không
#     query = await db.execute(select(Phim).where(Phim.id == id_film))
#     result = query.scalar_one_or_none()

#     if not result:
#         raise HTTPException(status_code=404, detail="Không tìm thấy phim muốn xóa")

#     # Bước 2: Cập nhật các bản ghi trong bảng `lich_chieu` thay vì đặt phim_id thành NULL
#     # Cập nhật phim_id thành một giá trị hợp lệ, ví dụ 0 (hoặc ID phim mặc định khác)
#     update_stmt = (
#         update(LichChieu)
#         .where(LichChieu.phim_id == id_film)
#         .values(phim_id=0)  # Thay phim_id bằng giá trị hợp lệ (ví dụ: ID phim mặc định là 0)
#     )
#     await db.execute(update_stmt)
#     await db.commit()

#     # Bước 3: Xóa các bản ghi trong bảng `binh_luan` nếu có liên quan
#     update_binh_luan_stmt = (
#         update(BinhLuan)
#         .where(BinhLuan.phim_id == id_film)
#         .values(phim_id=None)  # Cập nhật phim_id thành NULL nếu cho phép
#     )
#     await db.execute(update_binh_luan_stmt)
#     await db.commit()

#     # Bước 4: Xóa các bản ghi trong bảng `ve` nếu có liên quan
#     update_ve_stmt = (
#         update(Ve)
#         .where(Ve.suat_chieu_id == id_film)
#         .values(suat_chieu_id=None)  # Hoặc xử lý khác tùy theo yêu cầu
#     )
#     await db.execute(update_ve_stmt)
#     await db.commit()

#     # Bước 5: Xóa phim khỏi bảng `Phim`
#     await db.delete(result)
#     await db.commit()

#     # Trả về thông báo thành công
#     return {"message": f"Xóa phim '{result.ten_phim}' thành công"}
async def update_phim(phim_id: int, phim_data: PhimUpdateSchema, db: AsyncSession):
    query = await db.execute(select(Phim).where(Phim.id == phim_id))
    phim = query.scalar_one_or_none()

    if not phim:
        raise HTTPException(status_code=404, detail="Không tìm thấy phim")

    update_data = phim_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(phim, key, value)

    await db.commit()
    await db.refresh(phim)
    return phim

