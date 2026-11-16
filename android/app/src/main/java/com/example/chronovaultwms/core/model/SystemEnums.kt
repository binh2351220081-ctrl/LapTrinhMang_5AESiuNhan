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
    OUTBOUND("Xuất kho bàn giao đơn vị tiếp nhận"),
    INTERNAL_TRANSFER("Điều chuyển vị trí nội bộ"),
    AUDIT_ADJUSTMENT("Điều chỉnh sau kiểm kê"),
    RETURN_SUPPLIER("Trả hàng nhà cung cấp"),
    RETURN_DEALER("Đơn vị tiếp nhận gửi hoàn trả")
}

enum class SerialLifecycleStatus(val statusName: String) {
    ORDERED("Đã đặt hàng"),
    IN_TRANSIT("Đang trên đường về"),
    IN_STOCK("Đang lưu kho"),
    ALLOCATED("Đã khóa giữ chỗ cho lệnh điều phối"),
    DISPATCHED("Đã xuất bến / Bàn giao vận chuyển"),
    DELIVERED("Đã bàn giao cho đơn vị tiếp nhận"),
    RETURNED("Đơn vị tiếp nhận gửi trả lại kho"),
    DEFECTIVE("Hàng lỗi / Hư hỏng / Chờ bảo hành"),
    LIQUIDATED("Đã xuất tiêu hủy khỏi kho")
}

enum class ItemCondition(val conditionName: String) {
    PERFECT("Hoàn hảo / Mới 100%"),
    MINOR_SCRATCH("Trầy xước hộp ngoài nhẹ"),
    DEFECTIVE("Lỗi máy / Không hoạt động")
}

