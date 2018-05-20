#define alte 11
#define medie 10
#define basse 9
char miavar;
int ripetizioni;

void setup() {
  Serial.begin(9600);
  pinMode(alte, OUTPUT);
  pinMode(medie, OUTPUT);
  pinMode(basse, OUTPUT);
  delay(100);
}

void loop() {
  if (Serial.available()) {
    //Serial.println(Serial.available());
    miavar = Serial.read();
    switch (miavar) {
      case '1':
        ambulanza();
        break;
      case '2':
        allarme();
        break;
      case '3':
        campanello();
        break;
      case '4':
        fischietto();
        break;
      case '5':
        elettrodomestico();
        break;
      case '6':
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
      accenditutto(250);
      delay(1100);
      accenditutto(90);
      delay(150);
      accenditutto(250);
      delay(150);
      accenditutto(90);
      delay(150);
    }
    spegnitutto();
    delay(150);
  }
}

void allarme() {
  for (ripetizioni = 0; ripetizioni < 25; ripetizioni++) {
    accenditutto(250);
    delay(100);
    accenditutto(50);
    delay(100);
  }
  spegnitutto();
}

void campanello() {
  for (ripetizioni = 0; ripetizioni < 3; ripetizioni++) {
    accenditutto(250);
    delay(500);
    spegnitutto();
    delay(50);
    accenditutto(20);
    delay(1000);
    spegnitutto();
    delay(800);
  }
}

void fischietto() {
  delay(180);
  for (ripetizioni = 0; ripetizioni < 4; ripetizioni++) {
    for (int i = 0; i < 10; i++) {
      accenditutto(100);
      delay(50);
      accenditutto(250);
      delay(50);
    }
    spegnitutto();
    delay(480);
  }
}

void elettrodomestico() {
  for (ripetizioni = 0; ripetizioni < 6; ripetizioni++) {
    accenditutto(200);
    delay(200);
    spegnitutto();
    delay(100);
    accenditutto(200);
    delay(200);
    spegnitutto();
    delay(100);
    delay(400);
  }
}

void clacson() {
  for (ripetizioni = 0; ripetizioni < 2; ripetizioni++) {
    for (int i = 0; i < 2; i++) {
      accenditutto(250);
      delay(400);
      spegnitutto();
      delay(150); 
    }
    for (int b=0; b<2; b++) {
      accenditutto(250);
      delay(1200);
      spegnitutto();
      delay(150);
    }
  }
}


