import aioredis

class RedisManager:
    def __init__(self, redis_url="redis://localhost"):
        self.redis = aioredis.from_url(redis_url, decode_responses=True)

    async def set_ghe_tam_thoi(self, suat_chieu_id, ghe_id, user_id, timeout=300):
        """
        Giữ ghế nếu chưa bị đặt, đặt timeout (5 phút)
        """
        key = f"ghe:{ghe_id}:{suat_chieu_id}"
        if await self.redis.exists(key):
            return False
        await self.redis.setex(key, timeout, user_id)
        return True

    async def kiem_tra_ghe(self, suat_chieu_id, ghe_id):
        """
        Kiểm tra ghế có đang bị giữ trong Redis không
        """
        key = f"ghe:{ghe_id}:{suat_chieu_id}"
        return await self.redis.exists(key)

    async def get_user_giu_ghe(self, suat_chieu_id, ghe_id):
        """
        Lấy ID người đang giữ ghế
        """
        key = f"ghe:{ghe_id}:{suat_chieu_id}"
        user_id = await self.redis.get(key)
        return int(user_id) if user_id else None

    async def xoa_ghe_tam_thoi(self, suat_chieu_id, ghe_id):
        """
        Xóa trạng thái giữ ghế khỏi Redis
        """
        key = f"ghe:{ghe_id}:{suat_chieu_id}"
        await self.redis.delete(key)

    async def xoa_ghe_cua_user(self, suat_chieu_id, user_id):
        """
        Xóa tất cả các ghế mà user này đang giữ trong 1 suất chiếu
        """
        pattern = f"ghe:*:{suat_chieu_id}"
        keys = await self.redis.keys(pattern)
        for key in keys:
            current_user = await self.redis.get(key)
            if current_user == str(user_id):
                await self.redis.delete(key)

    async def close(self):
        """
        Đóng kết nối Redis
        """
        await self.redis.close()


# Khởi tạo Redis Manager
redis_manager = RedisManager()

# import aioredis

# class RedisManager:
#     def __init__(self, redis_url="redis://localhost"):
#         self.redis = aioredis.from_url(redis_url, decode_responses=True)

#     async def set_ghe_tam_thoi(self, suat_chieu_id, ghe_id, user_id, timeout=300):
#         """Giữ ghế nếu chưa bị đặt, đặt timeout (5 phút)"""
#         key = f"ghe:{ghe_id}:{suat_chieu_id}"
#         if await self.redis.exists(key):  # Kiểm tra nếu ghế đã bị giữ
#             return False
#         await self.redis.setex(key, timeout, user_id)
#         return True

#     async def kiem_tra_ghe(self, suat_chieu_id, ghe_id):
#         """Kiểm tra ghế có đang bị giữ trong Redis không"""
#         key = f"ghe:{ghe_id}:{suat_chieu_id}"
#         return await self.redis.exists(key)  # Trả về True/False trực tiếp

#     async def get_user_giu_ghe(self, suat_chieu_id, ghe_id):  # Đồng bộ tên hàm
#         """Lấy ID người đang giữ ghế"""
#         key = f"ghe:{ghe_id}:{suat_chieu_id}"
#         user_id = await self.redis.get(key)
#         return int(user_id) if user_id else None

#     async def xoa_ghe_tam_thoi(self, suat_chieu_id, ghe_id):
#         """Xóa trạng thái giữ ghế khỏi Redis"""
#         key = f"ghe:{ghe_id}:{suat_chieu_id}"
#         await self.redis.delete(key)

#     async def close(self):
#         """Đóng kết nối Redis khi không cần dùng nữa"""
#         await self.redis.close()
        

# # Khởi tạo Redis Manager
# redis_manager = RedisManager()