package com.example.elhexx.codeqr;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import com.google.zxing.Result;

import me.dm7.barcodescanner.zxing.ZXingScannerView;


import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {


    private ZXingScannerView scannerView;
    TextView textView;
    RequestQueue requestQueue;
    String url = "http://192.168.8.100/upd";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.qr_code);



    }

    public void scanCode(View view) {
        scannerView = new ZXingScannerView(this);
        scannerView.setResultHandler(new ZXingScannerResultHandler());

        setContentView(scannerView);
        scannerView.startCamera();

    }

    public void post(final String fname, final String lname) {
        textView = (TextView) findViewById(R.id.textView);
        requestQueue = Volley.newRequestQueue(this);

        StringRequest postRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>()
                {
                    @Override
                    public void onResponse(String response) {
                        // response
                        //textView.append(URL);
                        textView.setText("Response "+ response);
                        Toast.makeText(MainActivity.this, response, Toast.LENGTH_SHORT).show();
                    }
                },
                new Response.ErrorListener()
                {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // error
                        textView.setText("Error.Response " + error.getMessage().toString());
                    }
                }
        ) {
            @Override
            protected Map<String, String> getParams()
            {
                Map<String, String>  params = new HashMap<String, String>();
                params.put("fname", fname);
                params.put("lname", lname);

                return params;
            }
        };
        requestQueue.add(postRequest);
    }

    @Override
    public void onPause() {
        super.onPause();
        Toast.makeText(MainActivity.this, "you stopped the scan", Toast.LENGTH_SHORT).show();

        scannerView.stopCamera();
        setContentView(R.layout.qr_code);
    }


    class ZXingScannerResultHandler implements ZXingScannerView.ResultHandler {


        @Override
        public void handleResult(Result result) {
            String resultCode = result.getText();
            Toast.makeText(MainActivity.this, resultCode, Toast.LENGTH_SHORT).show();

            setContentView(R.layout.qr_code);
            scannerView.stopCamera();

            String names [] = resultCode.split(" ");
            post(names[0], names[1]);


        }


    }
}
