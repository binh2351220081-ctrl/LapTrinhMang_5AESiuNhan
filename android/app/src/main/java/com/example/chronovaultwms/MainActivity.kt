package com.example.chronovaultwms

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.doOnPreDraw
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.chronovaultwms.product.ProductListFragment
import com.example.chronovaultwms.core.auth.SessionManager

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.fragmentContainer)) { view, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            view.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        // Request one additional frame after the first layout (also refreshes emulator surfaces).
        findViewById<android.view.View>(R.id.fragmentContainer).doOnPreDraw { view ->
            view.postInvalidateOnAnimation()
        }

        // A fresh launch always starts at login; configuration changes retain the current screen.
        if (savedInstanceState == null || supportFragmentManager.findFragmentById(R.id.fragmentContainer) == null) {
            SessionManager(this).clearSession()
            supportFragmentManager.beginTransaction()
                .replace(R.id.fragmentContainer, ProductListFragment())
                .commitNow()
        }
    }
}
