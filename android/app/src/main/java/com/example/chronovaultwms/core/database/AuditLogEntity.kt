package com.example.chronovaultwms.core.database

import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Thực thể Nhật ký Vết Thao Tác (Audit Trail Log)
 * Phục vụ giám sát an ninh và truy vết hành động theo chuẩn Enterprise WMS
 * Phụ trách: TV1 - Phan Bá Hải Bình
 */
@Entity(tableName = "audit_logs")
data class AuditLogEntity(
    @PrimaryKey(autoGenerate = true)
    val logId: Long = 0,
    val timestamp: String,       // Thời điểm thao tác (VD: 10/11/2026 12:45:00)
    val actorName: String,       // Người thực hiện (VD: Phan Bá Hải Bình)
    val role: String,            // Vai trò (VD: DIRECTOR, INBOUND_STAFF)
    val action: String,          // Hành động (ĐĂNG NHẬP, THÊM ĐỒNG HỒ, XUẤT KHO...)
    val details: String,         // Mô tả chi tiết hành động
    val ipAddress: String = "192.168.1.100 - Mobile Terminal"
)

