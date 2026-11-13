package com.example.chronovaultwms.core.network

import com.example.chronovaultwms.core.database.ProductEntity
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Query

data class LoginRequest(
    val username: String,
    val passwordHash: String
)

data class LoginResponse(
    val success: Boolean,
    val token: String?,
    val userId: String?,
    val fullName: String?,
    val role: String?,
    val message: String?
)

interface ApiService {
    @POST("api/auth/login")
    suspend fun login(@Body request: LoginRequest): Response<LoginResponse>

    @GET("api/products")
    suspend fun getProducts(
        @Query("page") page: Int = 1,
        @Query("limit") limit: Int = 20
    ): Response<List<ProductEntity>>
}

