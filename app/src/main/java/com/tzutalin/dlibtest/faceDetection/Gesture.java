package com.tzutalin.dlibtest.faceDetection;

import java.util.ArrayList;
import android.graphics.Point;

public abstract class Gesture {

    public abstract ArrayList<Float> relationsFromEncoding(ArrayList<Point> landmarks);
    public abstract boolean detect(ArrayList<Point> landmarks);
    public abstract void calibrate(ArrayList<ArrayList<Float>> me);
}
