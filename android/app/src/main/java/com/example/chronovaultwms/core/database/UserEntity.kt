package com.example.chronovaultwms.core.database

import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Thực thể Người Dùng & Phân Quyền (RBAC User Entity)
 * Thuộc Phân hệ 1.2: Quản trị Hệ thống & Người dùng (TV1 - Phan Bá Hải Bình)
 */
@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey
    val userId: String,          // Mã người dùng (VD: USR-001)
    val username: String,        // Tên đăng nhập (VD: binh_director)
    val password: String,        // Mật khẩu (VD: admin123)
    val fullName: String,        // Họ và tên (VD: Phan Bá Hải Bình)
    val role: String,            // DIRECTOR, WAREHOUSE_MANAGER, INBOUND_STAFF, OUTBOUND_STAFF, INVENTORY_AUDITOR
    val department: String,      // Phòng ban (VD: Ban Giám Đốc, Kho Vận, Kế Toán...)
    val email: String,           // Email liên hệ
    val status: String = "ACTIVE"// Trạng thái: ACTIVE (Đang hoạt động), LOCKED (Khóa)
)
