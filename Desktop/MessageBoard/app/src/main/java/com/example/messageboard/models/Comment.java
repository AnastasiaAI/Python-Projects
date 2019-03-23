package com.example.messageboard.models;

import java.util.Date;

// custom class made for storing a message. you can update this class
public class Comment {

    public String text;
    public String username;
    public long date;

    public Comment(String text, String username, long date) {
        this.text = text;
        this.username = username;
        this.date = date;
    }

    public Comment() {
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public long getDate() {
        return date;
    }

    public void setDate(long date) {
        this.date = date;
    }

    // returns a string indicating how long ago this post was made
    public String elapsedTimeString() {
        long diff = new Date().getTime() - date;
        long seconds = diff / 1000;
        long minutes = seconds / 60;
        long hours = minutes / 60;
        long days = hours / 24;
        int daysInt = Math.round(days);
        int hoursInt = Math.round(hours);
        int minutesInt = Math.round(minutes);
        if (daysInt == 1) {
            return "1 day";
        } else if (daysInt > 1) {
            return Integer.toString(daysInt) + " days";
        } else if (hoursInt == 1) {
            return "1 hour";
        } else if (hoursInt > 1) {
            return Integer.toString(hoursInt) + " hours";
        } else {
            return "less than an hour";
        }
    }
}

