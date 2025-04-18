from fastapi import FastAPI, WebSocket

class WebSocketManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        """Chấp nhận kết nối WebSocket từ client"""
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        """Ngắt kết nối WebSocket"""
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """Gửi thông báo đến tất cả các client đang kết nối"""
        for connection in self.active_connections:
            await connection.send_json(message)

# Tạo một instance để sử dụng trong ứng dụng
socket_manager = WebSocketManager()
