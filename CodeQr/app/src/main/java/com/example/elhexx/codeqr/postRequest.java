package com.example.elhexx.codeqr;

import android.widget.TextView;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by elhexx on 10/17/17.
 */

public class postRequest  {
    RequestQueue requestQueue;
    String url = "http://192.168.201.122/upd";

    public void post(final String fname, final String lname) {

        StringRequest postRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>()
                {
                    @Override
                    public void onResponse(String response) {
                        // response
                        //textView.append(URL);
                        //textView.setText("Response "+ response);
                    }
                },
                new Response.ErrorListener()
                {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // error
                        //textView.setText("Error.Response " + error.getMessage().toString());
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
}
