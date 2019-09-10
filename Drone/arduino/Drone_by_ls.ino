#include <Servo.h>

/*Python*/
int speed_value[5];
/*count outtime*/
int count_outtime = 0;
/*PID_Control*/
float pitch_error, sum_pitch, roll_error, sum_roll;
float pitch = 0.0, roll = 0.0;
float Kp = 40, Ki = 0.00;
int pitch_output, roll_output, pitch_mid = 1500, roll_mid = 1500;
int range = 200;
int pitch_MAX = pitch_mid + range, pitch_MINI = pitch_mid - range;
int roll_MAX = roll_mid + range, roll_MINI = roll_mid - range;

/*AutoHigh*/
float cm;
int trigPin = 10; //Trig Pin
int echoPin = 11; //Echo Pin
int thr_mid = 1500, thr_max = 1800, thr_mini = 1150;
int thr_up1 = 1250;
int thr_up2 = 1350;
int thr_down = 1700;
int throttle_output = 1500;
int yaw_output = 1500;
int mode = 1334;
/*SBUS_Servo*/
Servo CH1;
Servo CH2;
Servo CH3;
Servo CH4;

void setup()
{
    Serial.begin(115200);

    CH1.attach(3);
    CH2.attach(5);
    CH3.attach(6);
    CH4.attach(8);

    pinMode(echoPin, INPUT);
    pinMode(trigPin, OUTPUT);
    pinMode(12, INPUT);
}

void loop()
{
    //Serial.println(cm);

    //  if(digitalRead(12)==HIGH){
    //  if(false){
    //    roll=0;
    //    pitch=0;
    //  }
    //  else{
    //
//    X();
    toArray();
//    AutoHigh();
//    PI_roll();
//    PI_pitch();
    Servo_output(speed_value[0], speed_value[1], speed_value[2], speed_value[3]);
//    Servo_output(1700,1500,1300,1100);

//    Serial.println((String)pitch_output + ", " + (String)roll_output + ", " + (String)throttle_output + ", " + (String)yaw_output);
//    Serial.println((String)speed_value[0] + ", " + (String)speed_value[1] + ", " +  (String)speed_value[2]+ ", " + (String)speed_value[3]);
}

void Servo_output(int CH_1, int CH_2, int CH_3, int CH_4)
{

    CH1.writeMicroseconds(CH_1);
    CH2.writeMicroseconds(CH_2);
    CH3.writeMicroseconds(CH_3);
    CH4.writeMicroseconds(CH_4);
    delay(50);
//    for(int i=1150; i<=1900;i+=5)
//    {
//          CH1.writeMicroseconds(i);
//          CH2.writeMicroseconds(i);
//          CH3.writeMicroseconds(i);
//          CH4.writeMicroseconds(i);
//          delay(40);
//    }
}

// ch3: 0
void AutoHigh()
{

    X();
    if (cm < 65) {
        throttle_output = thr_up1;
    }
    else if (cm < 95) {
        throttle_output = thr_up2;
    }
    else if (cm < 105) {
        throttle_output = thr_mid;
    }
    else {
        throttle_output = thr_down;
    }
}
void X()
{
    digitalWrite(trigPin, LOW);
    delayMicroseconds(5);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    int duration = pulseIn(echoPin, HIGH);
    cm = (duration / 2) / 29.1;
}
void PI_roll()
{
    roll += speed_value[0];
    roll_error = roll;
    sum_roll += roll_error;
    roll_output = ((Kp * roll_error) * (cm / 100)) + (Ki * sum_roll) + 1500;
    if (roll_output > roll_MAX) {
        Serial.println(roll_output);
        roll_output = roll_MAX;
    }
    else if (roll_output < roll_MINI) {
        roll_output = roll_MINI;
    }
    //roll_output=1500+speed_value[0]*4;
}
void PI_pitch()
{
    pitch += speed_value[1];
    pitch_error = pitch;
    sum_pitch += pitch_error;
    pitch_output = Kp * pitch_error * cm / 100 + Ki * sum_pitch + 1500;
    if (pitch_output > pitch_MAX) {
        pitch_output = pitch_MAX;
    }
    else if (pitch_output < pitch_MINI) {
        pitch_output = pitch_MINI;
    }
}

void toArray()
{
    if(Serial.available()){
        count_outtime = 0;
        String dir = Serial.readStringUntil('A');
        String tmp = "";
        int count = 0;
        for (unsigned int i = 0; i < dir.length(); i++) {
            if (dir[i] == ',') {
                speed_value[count] = tmp.toInt();
                tmp = "";
                count += 1;
            }
            else {
                tmp += dir[i];
            }
        }
    }
    else {
        count_outtime += 1;

        if (count_outtime > 10) {
            for(int i=0; i<5; i++){
                speed_value[i] = 0;
            }
        }
    }
}
