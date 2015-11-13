package com.oychang.wifigatherer;

import android.content.ContentValues;
import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.location.Location;
import android.net.wifi.ScanResult;

import java.util.List;


public class Database extends SQLiteOpenHelper {
    private static final String DB_NAME = "LocationData.db";
    private static final int DB_VERSION = 2;

    public static final class Readings {
        public static final String TABLE_NAME = "Readings";

        public static final String ID = "_id";
        private static final String ID_COL = ID + " INTEGER PRIMARY KEY AUTOINCREMENT";

        public static final String TIME = "time";
        private static final String TIME_COL = TIME + " INTEGER NOT NULL";

        public static final String LAT = "lat";
        private static final String LAT_COL = LAT + " FLOAT NOT NULL";

        public static final String LON = "lon";
        private static final String LON_COL = LON + " FLOAT NOT NULL";

        public static final String BSSID = "bssid";
        private static final String BSSID_COL = BSSID + " TEXT NOT NULL";

        public static final String SSID = "ssid";
        private static final String SSID_COL = SSID + " TEXT NOT NULL";

        public static final String LEVEL = "level";
        private static final String LEVEL_COL = LEVEL + " INTEGER NOT NULL";

        public static final String SPEED = "speed";
        private static final String SPEED_COL = SPEED + " FLOAT NOT NULL";

        public static final String ACCURACY = "accuracy";
        private static final String ACCURACY_COL = ACCURACY + " FLOAT NOT NULL";

        public static final String BEARING = "bearing";
        private static final String BEARING_COL = BEARING + " FLOAT NOT NULL";

        protected static final String SCHEMA = generateSchema(TABLE_NAME, ID_COL, TIME_COL,
                LAT_COL, LON_COL, BSSID_COL, SSID_COL, LEVEL_COL, SPEED_COL, ACCURACY_COL,
                BEARING_COL);
    }

    private SQLiteDatabase mWritableDatabase;

    // ***********************************************************************

    public Database(Context context) {
        super(context, DB_NAME, null, DB_VERSION);
        mWritableDatabase = getWritableDatabase();
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL(Readings.SCHEMA);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS " + Readings.TABLE_NAME);
        onCreate(db);
    }

    private static String generateSchema(String tableName,
                                         String... columnDefs) {
        final StringBuilder ret = new StringBuilder();
        // Build beginning of CREATE statement
        ret.append("CREATE TABLE IF NOT EXISTS ");
        ret.append(tableName);
        ret.append('(');

        // Build columns of table
        for (int i = 0; i < columnDefs.length - 1; i++) {
            ret.append(columnDefs[i]);
            ret.append(',');
        }
        if (columnDefs.length > 0)
            ret.append(columnDefs[columnDefs.length - 1]);

        // Build end
        ret.append(')');
        ret.append(';');
        return ret.toString();
    }

    // ***********************************************************************

    public void addResults(List<ScanResult> results, Location loc, final long time) {
        final double lat = loc.getLatitude();
        final double lon = loc.getLongitude();
        final float speed = loc.getSpeed();
        final float accuracy = loc.getAccuracy();
        final float bearing = loc.getBearing();

        ContentValues map = new ContentValues();
        for (ScanResult res : results) {
            map.put(Readings.TIME, time);
            map.put(Readings.LAT, lat);
            map.put(Readings.LON, lon);
            map.put(Readings.BSSID, res.BSSID);
            map.put(Readings.SSID, res.SSID);
            map.put(Readings.LEVEL, res.level);
            map.put(Readings.SPEED, speed);
            map.put(Readings.ACCURACY, accuracy);
            map.put(Readings.BEARING, bearing);

            mWritableDatabase.insert(Readings.TABLE_NAME, null, map);
        }
    }
}
