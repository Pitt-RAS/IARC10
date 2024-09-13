// Set pin numbers
int FORWARD_PIN_1 = 12;
int BACKWARD_PIN_1 = 11;
int FORWARD_PIN_2 = 10;
int BACKWARD_PIN_2 = 9;

// determines how long the roomba will move and turn for. adjust as needed
int MOVE_DURATION = 1000;
int TURN_DURATION = 500;

void setup() {
    Serial.begin(9600);
    pinMode(FORWARD_PIN_1, OUTPUT);
    pinMode(BACKWARD_PIN_1, OUTPUT);
    pinMode(FORWARD_PIN_2, OUTPUT);
    pinMode(BACKWARD_PIN_2, OUTPUT);
}

void loop() {
    // randomly move/turn forward, backward, left, or right. pauses for move duraiton after each action
    int move = random(0, 4);
    switch(move) {
        case 0:
            forward();
            break;
        case 1:
            backward();
            break;
        case 2:
            left();
            break;
        case 3:
            right();
            break;
    }
    stop();
}

void forward() {
    digitalWrite(FORWARD_PIN_1, HIGH);
    digitalWrite(FORWARD_PIN_2, HIGH);
    digitalWrite(BACKWARD_PIN_1, LOW);
    digitalWrite(BACKWARD_PIN_2, LOW);
    delay(MOVE_DURATION);
}

void backward() {
    digitalWrite(FORWARD_PIN_1, LOW);
    digitalWrite(FORWARD_PIN_2, LOW);
    digitalWrite(BACKWARD_PIN_1, HIGH);
    digitalWrite(BACKWARD_PIN_2, HIGH);
    delay(MOVE_DURATION);
}

void left() {
    digitalWrite(FORWARD_PIN_1, LOW);
    digitalWrite(FORWARD_PIN_2, HIGH);
    digitalWrite(BACKWARD_PIN_1, HIGH);
    digitalWrite(BACKWARD_PIN_2, LOW);
    delay(TURN_DURATION);
}

void right() {
    digitalWrite(FORWARD_PIN_1, HIGH);
    digitalWrite(FORWARD_PIN_2, LOW);
    digitalWrite(BACKWARD_PIN_1, LOW);
    digitalWrite(BACKWARD_PIN_2, HIGH);
    delay(TURN_DURATION);
}

void stop() {
    digitalWrite(FORWARD_PIN_1, LOW);
    digitalWrite(FORWARD_PIN_2, LOW);
    digitalWrite(BACKWARD_PIN_1, LOW);
    digitalWrite(BACKWARD_PIN_2, LOW);
    delay(MOVE_DURATION);
}
