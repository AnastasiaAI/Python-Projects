package com.example.messageboard;

import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RelativeLayout;

import com.example.messageboard.adapter.CommentAdapter;
import com.example.messageboard.models.Comment;
import com.example.messageboard.models.Users;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;
import java.util.Date;

// Displays a list of comments for a particular landmark.
public class CommentFeedActivity extends AppCompatActivity {

    private static final String TAG = CommentFeedActivity.class.getSimpleName();

    private RecyclerView mRecyclerView;
    private RecyclerView.Adapter mAdapter;
    DatabaseReference mCommentRef;
    Users mCurrentUser;
    private ArrayList<Comment> mComments = new ArrayList<Comment>();

    // UI elements
    EditText commentInputBox;
    RelativeLayout layout;
    Button sendButton;


    /* TODO: right now mRecyclerView is using hard coded comments.
     * You'll need to add functionality for pulling and posting comments from Firebase
     */

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_comment_feed);

        String title=getIntent().getStringExtra("post_title");
        // TODO: replace this with the name of the landmark the user chose

        setTitle(title + ": Posts");

        // hook up UI elements
        layout = (RelativeLayout) findViewById(R.id.comment_layout);
        commentInputBox = (EditText) layout.findViewById(R.id.comment_input_edit_text);
        sendButton = (Button) layout.findViewById(R.id.send_button);


        mRecyclerView = (RecyclerView) findViewById(R.id.comment_recycler);
        mRecyclerView.setHasFixedSize(true);
        mRecyclerView.setLayoutManager(new LinearLayoutManager(this));



        DatabaseReference mUsersRef=FirebaseDatabase.getInstance().getReference().child("Users");

        mUsersRef.child(FirebaseAuth.getInstance().getCurrentUser().getUid()).addValueEventListener(new ValueEventListener()
        {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot)
            {
                mCurrentUser=dataSnapshot.getValue(Users.class);
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError)
            {

            }
        });



        // create an onclick for the send button
        setOnClickForSendButton();

        addComments();

        // use the comments in mComments to create an adapter. This will populate mRecyclerView
        // with a custom cell (with comment_cell_layout) for each comment in mComments
        setAdapterAndUpdateData();
    }


    private void addComments()
    {
        String key=getIntent().getStringExtra("post_key");
        mCommentRef= FirebaseDatabase.getInstance().getReference().child("Comments").child(key);

        mCommentRef.addValueEventListener(new ValueEventListener()
        {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot)
            {
                mComments.clear();

                for(DataSnapshot dc:dataSnapshot.getChildren())
                {
                    Comment comment=dc.getValue(Comment.class);
                    mComments.add(comment);
                }

                mAdapter.notifyDataSetChanged();
                if(mComments.size()>0)
                {
                    mRecyclerView.smoothScrollToPosition(mComments.size() - 1);
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError)
            {

            }
        });



    }

    private void setOnClickForSendButton()
    {
        sendButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {
                String text = commentInputBox.getText().toString();
                if (TextUtils.isEmpty(text)) {
                    // don't do anything if nothing was added
                    commentInputBox.requestFocus();
                } else

                {
                    // clear edit text, post comment
                    commentInputBox.setText("");
                    Comment comment=new Comment();
                    comment.setUsername(mCurrentUser.getName());
                    comment.setDate(new Date().getTime());
                    comment.setText(text);
                    mCommentRef.push().setValue(comment);
                }
            }
        });
    }

    private void setAdapterAndUpdateData() {
        // create a new adapter with the updated mComments array
        // this will "refresh" our recycler view
        mAdapter = new CommentAdapter(this, mComments);
        mRecyclerView.setAdapter(mAdapter);

        // scroll to the last comment




    }


    @Override
    public boolean onSupportNavigateUp() {
        finish();
        return true;
    }
}
