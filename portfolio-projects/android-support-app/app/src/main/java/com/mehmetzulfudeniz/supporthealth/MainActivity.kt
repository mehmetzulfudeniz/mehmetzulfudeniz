package com.mehmetzulfudeniz.supporthealth

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.compose.viewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.net.HttpURLConnection
import java.net.URI
import kotlin.system.measureTimeMillis

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                SupportHealthApp()
            }
        }
    }
}

data class EndpointCheckState(
    val url: String = "https://example.com",
    val loading: Boolean = false,
    val statusCode: Int? = null,
    val latencyMs: Long? = null,
    val message: String = "Enter an HTTPS endpoint and run a health check."
)

class SupportHealthViewModel : ViewModel() {
    private val _state = MutableStateFlow(EndpointCheckState())
    val state: StateFlow<EndpointCheckState> = _state.asStateFlow()

    fun updateUrl(value: String) {
        _state.value = _state.value.copy(url = value)
    }

    fun runCheck() {
        val target = _state.value.url.trim()
        if (!target.startsWith("https://")) {
            _state.value = _state.value.copy(
                message = "Use a valid HTTPS URL, for example https://example.com",
                statusCode = null,
                latencyMs = null
            )
            return
        }

        _state.value = _state.value.copy(loading = true, message = "Checking endpoint…")

        viewModelScope.launch {
            val result = withContext(Dispatchers.IO) { checkEndpoint(target) }
            _state.value = _state.value.copy(
                loading = false,
                statusCode = result.statusCode,
                latencyMs = result.latencyMs,
                message = result.message
            )
        }
    }

    private fun checkEndpoint(target: String): EndpointResult {
        var connection: HttpURLConnection? = null
        return try {
            val uri = URI(target)
            val url = uri.toURL()
            var code = 0
            val elapsed = measureTimeMillis {
                connection = (url.openConnection() as HttpURLConnection).apply {
                    requestMethod = "GET"
                    connectTimeout = 5_000
                    readTimeout = 5_000
                    instanceFollowRedirects = true
                    setRequestProperty("User-Agent", "SupportHealth/0.1")
                    connect()
                    code = responseCode
                }
            }

            EndpointResult(
                statusCode = code,
                latencyMs = elapsed,
                message = if (code in 200..399) {
                    "Endpoint is reachable."
                } else {
                    "Endpoint responded with HTTP $code."
                }
            )
        } catch (exception: Exception) {
            EndpointResult(
                statusCode = null,
                latencyMs = null,
                message = exception.message ?: "Endpoint check failed."
            )
        } finally {
            connection?.disconnect()
        }
    }
}

data class EndpointResult(
    val statusCode: Int?,
    val latencyMs: Long?,
    val message: String
)

@Composable
fun SupportHealthApp(viewModel: SupportHealthViewModel = viewModel()) {
    val state by viewModel.state.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Support Health") })
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Text(
                text = "Endpoint Diagnostics",
                style = MaterialTheme.typography.headlineSmall
            )

            Text(
                text = "A small support-engineering utility for checking service reachability and HTTP response latency.",
                style = MaterialTheme.typography.bodyMedium
            )

            OutlinedTextField(
                value = state.url,
                onValueChange = viewModel::updateUrl,
                label = { Text("HTTPS endpoint") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )

            Button(
                onClick = viewModel::runCheck,
                enabled = !state.loading,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(if (state.loading) "Checking…" else "Run health check")
            }

            Card(modifier = Modifier.fillMaxWidth()) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Text("Result", style = MaterialTheme.typography.titleMedium)
                    Text(state.message)
                    state.statusCode?.let { Text("HTTP status: $it") }
                    state.latencyMs?.let { Text("Latency: $it ms") }
                }
            }
        }
    }
}
