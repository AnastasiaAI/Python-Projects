package com.example.messageboard;

import android.content.Context;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;

public class LoginActivity extends AppCompatActivity
{
    FirebaseAuth mAuth;
    TextView mRegister;
    private EditText inputEmail, inputPassword;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        inputEmail = findViewById(R.id.et_LoginEmail);
        inputPassword = findViewById(R.id.et_LoginPassword);
        mRegister=findViewById(R.id.tv_register);
        inputEmail.setText("anastasia@gmail.com");
        inputPassword.setText("hello123");

        mRegister.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {
                startActivity(new Intent(getBaseContext(),RegistrationActivity.class));
            }
        });

        final Button loginButton = findViewById(R.id.button_login);
        mAuth = FirebaseAuth.getInstance();
        loginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String email = inputEmail.getText().toString();
                final String password = inputPassword.getText().toString();

                if (TextUtils.isEmpty(email) || TextUtils.isEmpty(password)) {
                    Toast.makeText(getApplicationContext(), "Enter complete details", Toast.LENGTH_SHORT).show();
                }

                else if (!isNetworkConnected())
                {
                    Toast.makeText(LoginActivity.this, "Check your network", Toast.LENGTH_SHORT).show();
                }

                else
                {
                    Toast.makeText(LoginActivity.this, "Please wait", Toast.LENGTH_SHORT).show();
                    loginUser(email,password);
                }


            }


        });


    }


    private void loginUser(String email, String password)
    {
        mAuth.signInWithEmailAndPassword(email, password)
                .addOnCompleteListener(this, new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task)
                    {
                        if (task.isSuccessful())
                        {
                            Toast.makeText(LoginActivity.this, "Login Successful", Toast.LENGTH_SHORT).show();
                            startActivity(new Intent(getBaseContext(),MainActivity.class));
                            finish();
                        }

                        else
                        {
                            Toast.makeText(LoginActivity.this, "Wrong Credentials!", Toast.LENGTH_SHORT).show();

                        }

                    }
                });
    }




    private boolean isNetworkConnected() {
        ConnectivityManager cm = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        return cm.getActiveNetworkInfo() != null;
    }
}
