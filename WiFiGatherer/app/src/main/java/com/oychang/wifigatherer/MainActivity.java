package com.oychang.wifigatherer;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.location.LocationProvider;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.util.Locale;


public class MainActivity extends Activity {
    private Database mDb;

    // ***********************************************************************

    private boolean mSensorsEnabled = false;
    private boolean mHaveNetwork = false;
    private boolean mHaveSatellites = false;
    private boolean mIsRecording = false;
    private TextView mMessages;
    private Button mSensorToggle;
    private Button mCaptureToggle;
    private TextView mWifiStatus;
    private TextView mGpsStatus;

    // ***********************************************************************

    private WifiManager mWifiManager;
    private LocationManager mLocManager;
    private Handler mHandler;
    private long mScanStartTime = 0;
    private Location mLastLocation = null;
    private LocationListener mLocListener = new LocationListener() {
        @Override
        public void onLocationChanged(Location location) {
            println(location.getAccuracy() + "m accuracy (" + location.getProvider() + ")");

            switch (location.getProvider()) {
            case LocationManager.GPS_PROVIDER:
                mHaveSatellites |= true;
                break;
            case LocationManager.NETWORK_PROVIDER:
                mHaveNetwork |= true;
                break;
            }
            updateStatusText();

            mLastLocation = location;
        }

        @Override
        public void onStatusChanged(String provider, int status, Bundle extras) {
            println(provider + " status changed");

            switch (status) {
            case LocationProvider.OUT_OF_SERVICE:
                println(provider + " out of service");
                break;
            case LocationProvider.AVAILABLE:
                println(provider + " available");
                break;
            case LocationProvider.TEMPORARILY_UNAVAILABLE:
                println(provider + " temp unavailable");
                break;
            }

            if (extras != null && extras.containsKey("satellites"))
                println("have " + extras.get("satellites") + " satellites");
        }

        @Override
        public void onProviderEnabled(String provider) {
            println(provider + " enabled");
        }

        @Override
        public void onProviderDisabled(String provider) {
            println(provider + " disabled");
        }

        private void updateStatusText() {
            final String sep = mHaveSatellites && mHaveNetwork ? " and " : "";
            final String info = (mHaveSatellites ? "GPS Location" : "") + sep + (mHaveNetwork ? "Network Location" : "");

            final String shown = info.equals("") ? getString(R.string.txt_no_gps_info) : "have " + info;
            mGpsStatus.setText(shown);
        }
    };
    private BroadcastReceiver mBroadReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            final String msg = "got scan results in " + (System.currentTimeMillis() - mScanStartTime) + " ms";
            mWifiStatus.setText(msg);

            if (mIsRecording) {
                mDb.addResults(mWifiManager.getScanResults(), mLastLocation, System.currentTimeMillis());
            }
        }
    };
    private Runnable mScanLoop = new Runnable() {
        @Override
        public void run() {
            mScanStartTime = System.currentTimeMillis();
            mWifiManager.startScan();
            mHandler.postDelayed(mScanLoop, 3500);
        }
    };

    // ***********************************************************************

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // store pointers to view elements
        mMessages = (TextView) findViewById(R.id.txt_messages);
        mSensorToggle = (Button) findViewById(R.id.btn_sensor);
        mCaptureToggle = (Button) findViewById(R.id.btn_capture);
        mWifiStatus = (TextView) findViewById(R.id.txt_wifi_status);
        mGpsStatus = (TextView) findViewById(R.id.txt_gps_status);

        // setup gps manager
        mLocManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);

        // setup wifi manager
        mWifiManager = (WifiManager) getSystemService(Context.WIFI_SERVICE);
        IntentFilter wifiFilter = new IntentFilter();
        wifiFilter.addAction(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION);
        registerReceiver(mBroadReceiver, wifiFilter);

        // setup handler for automatic scanning
        mHandler = new Handler();

        // setup database
        mDb = new Database(this);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        // remove gps updates
        mLocManager.removeUpdates(mLocListener);
        // remove wifi updates
        mHandler.removeCallbacks(mScanLoop);
        unregisterReceiver(mBroadReceiver);

        // shutdown database
        mDb.close();
    }

    /**
     * Helper method to print out timestamped internal information to user.
     *
     * @param text line of logging information to print out
     */
    private void println(String text) {
        mMessages.setText(String.format(Locale.US, "[%d] %s\n", System.currentTimeMillis() / 1000L, text));
    }

    /**
     * Toggle recording of data to SQLite DB and update related UI elements.
     *
     * @param _ capture button, used since onClick expects this parameter
     */
    public void captureToggle(View _) {
        if (!mSensorsEnabled) {
            println("sensors must be enabled");
            return;
        }

        mIsRecording = !mIsRecording;
        mCaptureToggle.setText(mIsRecording ? R.string.btn_stop_capture : R.string.btn_start_capture);
    }

    /**
     * Toggle sensors on/off and update related UI elements.
     *
     * @param _ sensor button, used since onClick expects this parameter
     */
    public void sensorToggle(View _) {
        if (mSensorsEnabled) {
            // remove gps updates
            mLocManager.removeUpdates(mLocListener);
            mGpsStatus.setText(R.string.txt_no_gps_info);
            // remove wifi updates
            mHandler.removeCallbacks(mScanLoop);
            mWifiStatus.setText(R.string.txt_no_wifi_info);
        } else {
            // add gps scanning
            mLocManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 2000, 0, mLocListener);
            mLocManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 25 * 1000, 0, mLocListener);

            // add wifi scanning
            mScanLoop.run();
        }

        mSensorsEnabled = !mSensorsEnabled;
        mSensorToggle.setText(mSensorsEnabled ? R.string.btn_stop_sensors : R.string.btn_start_sensors);
    }
}
