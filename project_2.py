# MicroPython para ESP32

# Author: Andres Perez
# 20252
from machine import Pin, PWM
from time import sleep, sleep_ms

MOTOR_PIN = 18
LED_PIN = 2
FREQ = 5000          # 5 kHz
RES_BITS = 8         # "resolución" lógica de 8 bits (0-255)

# Configurar PWM del motor y LED
motor_pwm = PWM(Pin(MOTOR_PIN), freq=FREQ, duty_u16=0)  # canal se gestiona internamente
led = Pin(LED_PIN, Pin.OUT)

# Helper: convertir 0-255 (8 bits) a 0-65535 (16 bits)
def duty8_to_u16(duty_8):
    if duty_8 < 0: duty_8 = 0
    if duty_8 > 255: duty_8 = 255
    # Escala lineal: 0..255 -> 0..65535
    return int(duty_8 * 257)   # 255*257 ≈ 65535

print("Control de motor PWM en ESP32 (MicroPython)")

try:
    while True:
        # Acelerar de 0 a 255
        for dc in range(0, 256):
            motor_pwm.duty_u16(duty8_to_u16(dc))
            sleep_ms(30)

        # Mantener velocidad máxima 2 s y LED encendido
        led.value(1)
        sleep(2)

        # Desacelerar de 255 a 0
        for dc in range(255, -1, -1):
            motor_pwm.duty_u16(duty8_to_u16(dc))
            sleep_ms(30)

        # Motor apagado 2 s y LED apagado
        led.value(0)
        sleep(2)

except KeyboardInterrupt:
    # Apaga todo al salir con Ctrl+C
    motor_pwm.duty_u16(0)
    led.value(0)
    motor_pwm.deinit()
    print("PWM detenido.")
