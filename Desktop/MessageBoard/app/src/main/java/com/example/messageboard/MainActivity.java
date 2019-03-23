package com.example.messageboard;

import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.location.Location;
import android.net.ConnectivityManager;
import android.net.Uri;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.messageboard.models.Post;
import com.example.messageboard.models.Users;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.location.LocationListener;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationServices;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity implements GoogleApiClient.ConnectionCallbacks, GoogleApiClient.OnConnectionFailedListener, LocationListener
{
    static
    {
        FirebaseDatabase.getInstance().setPersistenceEnabled(true);
    }
    private FirebaseAuth mAuth;
    private FirebaseAuth.AuthStateListener authListener;
    ListView mListView;
    DatabaseReference mRef;
    GoogleApiClient googleApiClient;
    LocationRequest mLocationRequest;
    Location mCurrentLocation;
    final ArrayList<Post> items= new ArrayList<>();
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        googleApiClient = new GoogleApiClient.Builder(this) // to get location
                .addApi(LocationServices.API)
                .addConnectionCallbacks(this)
                .addOnConnectionFailedListener(this).build();

        mListView=findViewById(R.id.topic_list);
        mAuth = FirebaseAuth.getInstance();
        authListener = new FirebaseAuth.AuthStateListener() {
            @Override
            public void onAuthStateChanged(@NonNull FirebaseAuth firebaseAuth)
            {
                FirebaseUser user = firebaseAuth.getCurrentUser();
                if (user == null)
                {
                    startActivity(new Intent(MainActivity.this, LoginActivity.class));
                    finish();
                }

                else
                {
                    googleApiClient.connect();
                }

            }
        };


    }




    @Override
    protected void onDestroy()
    {
        if (googleApiClient != null && googleApiClient.isConnected())
        {
            googleApiClient.disconnect();
        }
        super.onDestroy();
    }

    @Override
    protected void onResume()
    {
        super.onResume();

        if (googleApiClient != null && googleApiClient.isConnected())
        {
           startLocationUpdates();
        }

    }




    public void getData()
    {

        final PostAdapter adapter=new PostAdapter(this,items);
        mListView.setAdapter(adapter);
        mRef= FirebaseDatabase.getInstance().getReference().child("Post");
        mRef.addValueEventListener(new ValueEventListener()
        {

            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot)
            {
                items.clear();
                for(DataSnapshot dc: dataSnapshot.getChildren())
                {
                    Post item=dc.getValue(Post.class);
                    items.add(item);
                }

                adapter.notifyDataSetChanged();

            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });

    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu)
    {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.activity_main_drawer, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item)
    {
        new AlertDialog.Builder(MainActivity.this)
                .setMessage("Are you sure you want to Logout?")
                .setCancelable(false)
                .setPositiveButton("Yes", new DialogInterface.OnClickListener()
                {
                    public void onClick(DialogInterface dialog, int id)
                    {
                        signOut();
                    }
                })
                .setNegativeButton("No", null)
                .show();
        return super.onOptionsItemSelected(item);
    }



    public void signOut() {
        mAuth.signOut();
    }

    @Override
    public void onStart()
    {
        super.onStart();
        if (googleApiClient != null)
        {
            googleApiClient.connect();
        }

        mAuth.addAuthStateListener(authListener);
    }

    @Override
    public void onStop() {
        super.onStop();
        if (authListener != null) {
            mAuth.removeAuthStateListener(authListener);
        }
    }


    private boolean isNetworkConnected()
    {
        ConnectivityManager cm = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        return cm.getActiveNetworkInfo() != null;
    }

    @Override
    public void onConnected(@Nullable Bundle bundle)
    {
        createLocationRequest();
    }

    protected void createLocationRequest()
    {
        mLocationRequest = new LocationRequest();
        mLocationRequest.setInterval(1000);
        mLocationRequest.setFastestInterval(1000);
        mLocationRequest.setSmallestDisplacement(10f);
        mLocationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);
        startLocationUpdates();
    }

    protected void startLocationUpdates()
    {

        if(mLocationRequest!=null)
        {
            LocationServices.FusedLocationApi.requestLocationUpdates(googleApiClient, mLocationRequest, this);
        }
    }


    @Override
    public void onConnectionSuspended(int i) {

    }

    @Override
    public void onConnectionFailed(@NonNull ConnectionResult connectionResult) {

    }

    @Override
    public void onLocationChanged(Location location)
    {
        Log.d("locDetails",""+location.getLatitude()+" "+location.getLongitude());
        mCurrentLocation=location;
//        LocationServices.FusedLocationApi.removeLocationUpdates(googleApiClient, this);
        getData();
    }


    public class PostAdapter extends ArrayAdapter<Post>
    {

        Context mContext;
        private class ViewHolder
        {
            TextView title,distance,likes,dislikes;
            ImageView image;
        }

        public PostAdapter(Context context, ArrayList<Post> list)
        {
            super(context, R.layout.post_item, list);
            this.mContext=context;
        }

        @Override
        public View getView(final int position, View convertView, ViewGroup parent)
        {

            final Post item = getItem(position);
            ViewHolder viewHolder;
            if (convertView == null)
            {
                viewHolder = new ViewHolder();
                LayoutInflater inflater = LayoutInflater.from(getContext());
                convertView = inflater.inflate(R.layout.post_item, parent, false);
                viewHolder.title = convertView.findViewById(R.id.post_title);
                viewHolder.distance = convertView.findViewById(R.id.post_distance);
                viewHolder.image = convertView.findViewById(R.id.post_image);
                viewHolder.likes = convertView.findViewById(R.id.tv_likes);
                viewHolder.dislikes = convertView.findViewById(R.id.tv_dislikes);
                convertView.setTag(viewHolder);
            }
            else
            {
                viewHolder =(ViewHolder) convertView.getTag();
            }
            viewHolder.title.setText(item.getLandmark_name());
            Uri imageUri = Uri.parse("android.resource://" + getPackageName() + "/drawable/" + item.getFilename());
            viewHolder.image.setImageURI(imageUri);
            viewHolder.likes.setText(""+item.getLikes());
            viewHolder.dislikes.setText(""+item.getDislikes());
            int index=item.getCoordinates().indexOf(",");
            double lat=Double.parseDouble(item.getCoordinates().substring(0,index).trim());
            double lon=Double.parseDouble(item.getCoordinates().substring(index+1).trim());
            viewHolder.distance.setText(setUnit(getDistance(lat,lon)));

            viewHolder.image.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v)
                {

                    int index=item.getCoordinates().indexOf(",");
                    double lat=Double.parseDouble(item.getCoordinates().substring(0,index).trim());
                    double lon=Double.parseDouble(item.getCoordinates().substring(index+1).trim());

                    if(getDistance(lat,lon)<10)
                    {
                        startActivity(new Intent(getBaseContext(),CommentFeedActivity.class).putExtra("post_title",item.getLandmark_name())
                                .putExtra("post_key",String.valueOf(position+1)));
                    }

                    else
                    {
                        Toast.makeText(MainActivity.this, "You must be within 10 meters of a landmark to access its feed", Toast.LENGTH_SHORT).show();
                    }
                }
            });


            viewHolder.likes.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v)
                {

                    mRef.child(String.valueOf(position+1)).child("likes").setValue(item.getLikes()+1);
                }
            });

            viewHolder.dislikes.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v)
                {

                    mRef.child(String.valueOf(position+1)).child("dislikes").setValue(item.getDislikes()+1);
                }
            });


            return convertView;
        }


    }

    private float getDistance(double lat,double lon)
    {

        Location locationA=new Location("");
        locationA.setLatitude(lat);
        locationA.setLongitude(lon);

        float distance=Math.round(locationA.distanceTo(mCurrentLocation));
        return distance;
    }

    private String setUnit(float distance)
    {
        String unit="m";
        if(distance>1000)
        {
            distance=distance/1000;
            unit="km";
        }

        return distance+" "+unit+" away";
    }





}
