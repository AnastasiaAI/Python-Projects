package com.example.messageboard;

import android.app.ProgressDialog;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.example.messageboard.models.Users;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class RegistrationActivity extends AppCompatActivity {

    EditText etName,etEmail,etPassword;
    FirebaseAuth mAuth;
    ProgressDialog progressDialog;
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_registration);
        mAuth=FirebaseAuth.getInstance();
        etName=findViewById(R.id.et_name);
        etEmail=findViewById(R.id.et_email);
        etPassword=findViewById(R.id.et_password);

        Button RegisterButton=findViewById(R.id.register_button);

        RegisterButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {
                if(etName.getText().toString().isEmpty() ||etEmail.getText().toString().isEmpty() ||etPassword.getText().toString().isEmpty())
                {
                    Toast.makeText(RegistrationActivity.this, "Input field is missing", Toast.LENGTH_SHORT).show();
                }

                else
                {
                    progressDialog= new ProgressDialog(RegistrationActivity.this);
                    progressDialog.setTitle("Uploading Details");
                    progressDialog.setMessage("Please Wait");
                    progressDialog.show();
                    String email=etEmail.getText().toString();
                    String password=etPassword.getText().toString();
                    createUser(email,password);
                }

            }
        });
    }


    public void createUser(String email,String password)
    {


        mAuth.createUserWithEmailAndPassword(email, password)
                .addOnCompleteListener(this, new OnCompleteListener<AuthResult>()
                {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task)
                    {
                        if (task.isSuccessful())
                        {
                            DatabaseReference mRef= FirebaseDatabase.getInstance().getReference().child("Users");
                            Users user=new Users();
                            user.setName(etName.getText().toString());
                            user.setEmail(etEmail.getText().toString());
                            user.setPassword(etPassword.getText().toString());

                            mRef.child(mAuth.getCurrentUser().getUid()).setValue(user).addOnCompleteListener(new OnCompleteListener<Void>()
                            {
                                @Override
                                public void onComplete(@NonNull Task<Void> task)
                                {
                                    if(task.isSuccessful())
                                    {
                                        progressDialog.dismiss();
                                        Toast.makeText(RegistrationActivity.this, "Registration Successfull", Toast.LENGTH_SHORT).show();
                                        finish();
                                    }

                                    else
                                    {
                                        progressDialog.dismiss();
                                        Toast.makeText(RegistrationActivity.this, "Try again later", Toast.LENGTH_SHORT).show();
                                    }
                                }
                            });
                        }

                        else
                        {
                            progressDialog.dismiss();
                            Toast.makeText(RegistrationActivity.this, "Authentication failed.",Toast.LENGTH_SHORT).show();
                        }


                    }
                });


    }
}
