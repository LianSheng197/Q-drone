#include <Servo.h>

/*Python*/
int speed_value[5]={0,0,0,0,0};

/*count outtime*/
int count_outtime = 0;

/* Switch is open */
bool isOpen = false;

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
int trigPin = 6; //Trig Pin
int echoPin = 7; //Echo Pin
int thr_mid = 1490, thr_max = 1800, thr_mini = 1150;
int thr_up1 = 1700;
int thr_up2 = 1600;
int thr_down = 1350;
int throttle_output = 1505;
int yaw_output = 1500;
int mode = 0;

/*SBUS_Servo*/
Servo CH1;
Servo CH2;
Servo CH3;
Servo CH4;
Servo CH7;

void setup()
{
    Serial.begin(115200);

    CH1.attach(8);
    CH2.attach(9);
    CH3.attach(10);
    CH4.attach(11);
    CH7.attach(12);
    pinMode(echoPin, INPUT);
    pinMode(trigPin, OUTPUT);
    pinMode(2, INPUT);
    pinMode(3, INPUT);
    pinMode(13, INPUT);
    while(true){
        
        if(digitalRead(13) == LOW){
            Servo_output(1000, 1000, 1000, 2000,1510);
            for(int i=0;i<5000;i++){
            toArray();
            delay(1);
            }
            break;
        }
        else{
            Servo_output(1490, 1490, 1490, 1490,1510);
            toArray();
        delay(10);
        }
    }
}

void loop()
{
    if(digitalRead(13) == LOW){
        if(!isOpen){
            Serial.println("<OPEN>");
            isOpen = true;
        }
        
        
        if(speed_value[2]==0){
            mode=0;
        throttle_output=0;
        }
        else{
            mode=1510;
        AutoHigh();
        speed_value[2]=0;
        }
        Serial.println(cm);
        toArray();
        Servo_output(speed_value[0], speed_value[1], throttle_output, speed_value[3],mode);
        delay(20);
    } 
    else {
        Serial.println("<CLOSE>");
        toArray();
        isOpen = false;
        delay(20);
    }
    
    
}
/*
 * CH1 MID1505 
 * CH2 MID1505
 * CH3 MID1480
 * CH4 MID1505
 */
void Servo_output(int CH_1, int CH_2, int CH_3, int CH_4,int CH_7)
{

    CH1.writeMicroseconds(CH_1);
    CH2.writeMicroseconds(CH_2);
    CH3.writeMicroseconds(CH_3);
    CH4.writeMicroseconds(CH_4);
    CH7.writeMicroseconds(CH_7);
    /*for(int i=1300;i<1700;i++){
    CH1.writeMicroseconds(i);
    CH2.writeMicroseconds(i);
    CH3.writeMicroseconds(i);
    CH4.writeMicroseconds(i);
    CH7.writeMicroseconds(i);}*/
    delay(10);
}

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
    int duration = pulseIn(echoPin, HIGH,20000);
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
