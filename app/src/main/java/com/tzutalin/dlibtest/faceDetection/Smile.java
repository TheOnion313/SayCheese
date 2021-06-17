package com.tzutalin.dlibtest.faceDetection;

import android.graphics.Point;
import com.tzutalin.dlib.Constants;

import java.util.ArrayList;

public class Smile extends Gesture {
    private float smileMin, eyeMouthMin;

    public Smile(float smileMin, float eyeMouthMin) {
        this.smileMin = smileMin;
        this.eyeMouthMin = eyeMouthMin;
    }

    public static float distance(Point a, Point b) {
        return (float) Math.sqrt(Math.pow(a.x - b.x, 2)
                + Math.pow(a.y - b.y, 2)
        );
    }

    private static float MAR(ArrayList<Point> mouth) {
        float d3_9 = distance(mouth.get(3), mouth.get(9));
        float d2_10 = distance(mouth.get(2), mouth.get(10));
        float d4_8 = distance(mouth.get(4), mouth.get(8));

        float avgD = (d2_10 + d3_9 + d4_8) / 3;
        float horizontalD = distance(mouth.get(0), mouth.get(6));

        return avgD / horizontalD;
    }

    private static float MER(ArrayList<Point> encoding) {
        return distance(encoding.get(48), encoding.get(54)) / distance(encoding.get(36), encoding.get(45));
    }

    @Override
    public ArrayList<Float> relationsFromEncoding(ArrayList<Point> landmarks) {
        ArrayList<Float> relations = new ArrayList<>();

        int[] mouthRange = Constants.getMouthRange();
        ArrayList<Point> mouth = (ArrayList<Point>) landmarks.subList(mouthRange[0], mouthRange[1]);

        float mar = MAR(mouth), mer = MER(landmarks);
        relations.add(mar);
        relations.add(mer);

        return relations;
    }

    @Override
    public boolean detect(ArrayList<Point> landmarks) {
        ArrayList<Float> relations = this.relationsFromEncoding(landmarks);

        return relations.get(0) > this.smileMin && relations.get(1) > this.eyeMouthMin;
    }

    @Override
    public void calibrate(ArrayList<ArrayList<ArrayList<Float>>> me) {
        ArrayList<Float> marY = new ArrayList<>();
        ArrayList<Float> merY = new ArrayList<>();

        for(ArrayList<Float> rel : me.get(0)) {
            marY.add(rel.get(0));
            merY.add(rel.get(1));
        }

        this.smileMin = Math.min(marY);
    }
}
