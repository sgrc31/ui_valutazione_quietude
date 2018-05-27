int alte = 6;
int medie = 5;
int basse = 3;
int payload[12] = {0, 0, 250, 90, 250, 50, 250, 60, 250, 100, 200, 250};
int ripetizioni;

void setup() {
  Serial.begin(9600);
  pinMode(3, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  delay(100);
}

void loop() {
  if (Serial.available()) {
    for (int m = 0; m<12; m++) {
      payload[m] = Serial.parseInt();
    }
    if (payload[0] == 0) {
      alte = 11;
      medie = 10;
      basse = 9;
    } else {
      alte = 6;
      medie = 5;
      basse = 3;
    }
    switch (payload[1]) {
      case 1:
        ambulanza();
        break;
      case 2:
        allarme();
        break;
      case 3:
        campanello();
        break;
      case 4:
        fischietto();
        break;
      case 5:
        elettrodomestico();
        break;
      case 6:
        clacson();
        break;
    }
  }
  delay(10);
}

void accenditutto(int x) {
  analogWrite(alte, x);
  analogWrite(medie, x);
  analogWrite(basse, x);
}

void spegnitutto() {
  analogWrite(alte, 0);
  analogWrite(medie, 0);
  analogWrite(basse, 0);
}

void ambulanza() {
  for (ripetizioni = 0; ripetizioni < 3; ripetizioni++) {
    for (int i = 0; i < 2; i++) {
      accenditutto(payload[2]);
      delay(1100);
      accenditutto(payload[3]);
      delay(150);
      accenditutto(payload[2]);
      delay(150);
      accenditutto(payload[3]);
      delay(150);
    }
    spegnitutto();
    delay(150);
  }
}

void allarme() {
  for (ripetizioni = 0; ripetizioni < 25; ripetizioni++) {
    accenditutto(payload[4]);
    delay(100);
    accenditutto(payload[5]);
    delay(100);
  }
  spegnitutto();
}

void campanello() {
  for (ripetizioni = 0; ripetizioni < 3; ripetizioni++) {
    accenditutto(payload[6]);
    delay(500);
    spegnitutto();
    delay(50);
    accenditutto(payload[7]);
    delay(1000);
    spegnitutto();
    delay(800);
  }
}

void fischietto() {
  delay(180);
  for (ripetizioni = 0; ripetizioni < 4; ripetizioni++) {
    for (int i = 0; i < 10; i++) {
      accenditutto(payload[9]);
      delay(50);
      accenditutto(payload[8]);
      delay(50);
    }
    spegnitutto();
    delay(480);
  }
}

void elettrodomestico() {
  for (ripetizioni = 0; ripetizioni < 6; ripetizioni++) {
    accenditutto(payload[10]);
    delay(200);
    spegnitutto();
    delay(100);
    accenditutto(payload[10]);
    delay(200);
    spegnitutto();
    delay(100);
    delay(400);
  }
}

void clacson() {
  for (ripetizioni = 0; ripetizioni < 2; ripetizioni++) {
    for (int i = 0; i < 2; i++) {
      accenditutto(payload[11]);
      delay(400);
      spegnitutto();
      delay(150); 
    }
    for (int b=0; b<2; b++) {
      accenditutto(payload[11]);
      delay(1200);
      spegnitutto();
      delay(150);
    }
  }
}


