package com.example.chronovaultwms

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.example.chronovaultwms.dashboard.DashboardOverviewFragment

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        if (savedInstanceState == null) {
            supportFragmentManager.beginTransaction()
                .replace(R.id.fragmentContainer, DashboardOverviewFragment())
                .commit()
        }
    }
}
