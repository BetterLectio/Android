package dk.betterlectio.mobile;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Python py = Python.getInstance();
        PyObject app = py.getModule("app");
        app.callAttr("main");

        WebView myWebView = (WebView) findViewById(R.id.webview);
        WebSettings webSettings = myWebView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        myWebView.loadUrl("http://127.0.0.1:5000"); // Lav en url på betterlectio.dk som tillader at man ændre en ny api_url i localstorage. Måske et "mobile.betterlectio.dk" sub-domain
    }

}