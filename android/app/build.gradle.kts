plugins {
    alias(libs.plugins.android.application)
    id("com.google.devtools.ksp")
}

android {
    namespace = "com.example.chronovaultwms"
    compileSdk {
        version = release(37)
    }
    buildFeatures {
        viewBinding = true
    }

    defaultConfig {
        applicationId = "com.example.chronovaultwms"
        minSdk = 26
        targetSdk = 37
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            optimization {
                enable = false
            }
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
}

dependencies {
    implementation(libs.androidx.activity.ktx)
    implementation(libs.androidx.appcompat)
    implementation(libs.androidx.constraintlayout)
    implementation(libs.androidx.core.ktx)
    implementation(libs.material)
    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(libs.androidx.junit)
        // --- 1. JETPACK NAVIGATION (Điều hướng màn hình) ---
        val navVersion = "2.7.7"
        implementation("androidx.navigation:navigation-fragment-ktx:$navVersion")
        implementation("androidx.navigation:navigation-ui-ktx:$navVersion")

        // --- 2. ROOM DATABASE (Lưu trữ CSDL Offline SQLite) ---
        val roomVersion = "2.7.1"
        implementation("androidx.room:room-runtime:$roomVersion")
        implementation("androidx.room:room-ktx:$roomVersion")
        // Sử dụng KSP chuẩn cho Room Database trong Android hiện đại:
        ksp("androidx.room:room-compiler:$roomVersion")

        // --- 3. RETROFIT 2 & OKHTTP (Lập trình mạng, Gọi API Backend) ---
        val retrofitVersion = "2.9.0"
        implementation("com.squareup.retrofit2:retrofit:$retrofitVersion")
        implementation("com.squareup.retrofit2:converter-gson:$retrofitVersion")
        implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")

        // --- 4. COROUTINES & LIFECYCLE (Xử lý đa luồng & MVVM ViewModel) ---
        implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
        implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.7.0")
        implementation("androidx.lifecycle:lifecycle-livedata-ktx:2.7.0")

        // --- 5. BẢO MẬT LƯU TRỮ (Lưu Token đăng nhập mã hóa) ---
        implementation("androidx.security:security-crypto:1.1.0-alpha06")

}