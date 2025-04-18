from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import List

from app.models.models import Ve, SuatChieu, LichChieu, Phim, PhongChieu, Ghe, ThanhToan
from app.schemas.schemas import VeDetailResponse

async def get_all_ve_details(user_id: int, db: AsyncSession) -> List[dict]:
    """Lấy ra chi tiết toàn bộ vé đã mua của người dùng."""
    result = await db.execute(
        select(Ve)
        .options(
            joinedload(Ve.suat_chieu).joinedload(SuatChieu.lich_chieu).joinedload(LichChieu.phim),
            joinedload(Ve.suat_chieu).joinedload(SuatChieu.phong),
            joinedload(Ve.ghe),
            joinedload(Ve.thanh_toan)
        )
        .where(Ve.user_id == user_id, Ve.trang_thai == "Đã xác nhận")
        .order_by(Ve.created_at.desc())
    )
    ves = result.scalars().all()

    if not ves:
        raise HTTPException(status_code=404, detail="Không tìm thấy vé nào đã mua")

    ve_details = []
    for ve in ves:
        ve_detail = VeDetailResponse(
            id=ve.id,
            ten_phim=ve.suat_chieu.lich_chieu.phim.ten_phim,
            anh_phim=ve.suat_chieu.lich_chieu.phim.hinh_anh ,
            ngay_chieu=ve.suat_chieu.lich_chieu.ngay_chieu,
            gio_bat_dau=ve.suat_chieu.gio_bat_dau,
            gio_ket_thuc=ve.suat_chieu.gio_ket_thuc,
            phong_chieu=ve.suat_chieu.phong.ten_phong,
            ghe=ve.ghe.so_ghe,
            gia_ve=float(ve.gia_ve),
            so_tien_thanh_toan=float(ve.thanh_toan.so_tien) if ve.thanh_toan else 0.0,
            created_at=ve.created_at
        )
        ve_details.append(ve_detail.model_dump())  # Chuyển đổi thành dictionary

    return ve_details  # Trả về danh sách dictionary thay vì object
