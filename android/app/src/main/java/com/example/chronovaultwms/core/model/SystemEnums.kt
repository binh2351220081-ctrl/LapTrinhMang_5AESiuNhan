package com.example.chronovaultwms.core.model

enum class UserRole(val roleName: String) {
    SYSTEM_ADMIN("Quản trị hệ thống"),
    STORE_OWNER("Chủ cửa hàng"),
    WAREHOUSE_MANAGER("Thủ kho (quản lý điều hành)"),
    OPERATIONS_STAFF("Nhân viên nhập - xuất kho"),
    ACCOUNTANT("Kế toán kho")
}

enum class MovementType(val typeName: String) {
    INBOUND("Nhập kho từ nhà cung cấp"),
    OUTBOUND("Xuất kho cho đại lý"),
    INTERNAL_TRANSFER("Điều chuyển vị trí nội bộ"),
    AUDIT_ADJUSTMENT("Điều chỉnh sau kiểm kê"),
    RETURN_SUPPLIER("Trả hàng nhà cung cấp"),
    RETURN_DEALER("Đại lý trả hàng")
}

enum class SerialLifecycleStatus(val statusName: String) {
    ORDERED("Đã đặt hàng"),
    IN_TRANSIT("Đang trên đường về"),
    IN_STOCK("Đang lưu kho"),
    ALLOCATED("Đã khóa giữ hàng cho đơn"),
    DISPATCHED("Đã xuất bến / Bàn giao vận chuyển"),
    DELIVERED("Đã giao thành công cho đại lý"),
    RETURNED("Khách hàng / Đại lý gửi trả lại"),
    DEFECTIVE("Hàng lỗi / Hư hỏng / Chờ bảo hành"),
    LIQUIDATED("Đã thanh lý xuất hủy")
}

enum class ItemCondition(val conditionName: String) {
    PERFECT("Hoàn hảo / Mới 100%"),
    MINOR_SCRATCH("Trầy xước hộp ngoài nhẹ"),
    DEFECTIVE("Lỗi máy / Không hoạt động")
}

