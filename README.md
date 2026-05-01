# 🌱 Irrigation IoT

![ESP32](https://img.shields.io/badge/ESP32-DevKit%20V4-red?logo=espressif)
![MicroPython](https://img.shields.io/badge/MicroPython-1.22.0-blue)
![MQTT](https://img.shields.io/badge/MQTT-3.1.1%2F5.0-orange)
![Blynk](https://img.shields.io/badge/Blynk-Cloud-green)

---

## 📃 Descrição

O Irrigation ESP32 é um sistema IoT de automação de irrigação desenvolvido com ESP32 e MicroPython, com integração em tempo real via protocolo MQTT utilizando a plataforma Blynk Cloud.
O sistema realiza o monitoramento contínuo da umidade do solo (simulada via potenciômetro), acionando automaticamente uma válvula controlada por servo motor quando necessário. Além disso, permite controle manual tanto por botão físico quanto remotamente via aplicativo Blynk.
A solução implementa mecanismos de segurança como timeout automático de irrigação, evitando desperdício de água e possíveis falhas operacionais. A arquitetura segue um modelo modular, separando responsabilidades entre controle de hardware, comunicação MQTT e lógica de negócio.

---

## 💻 Tecnologias Utilizadas

- **ESP32**: Microcontrolador principal do sistema.
- **MicroPython**: Linguagem utilizada para programação embarcada.
- **MQTT**: Protocolo leve para comunicação IoT.
- **Blynk Cloud**: Plataforma para controle remoto e monitoramento.
- **Wokwi**: Simulador de circuitos eletrônicos.
- **PWM / ADC**: Controle de servo motor e leitura analógica.

---

## 🛎️ Funcionalidades

- Monitoramento contínuo da umidade do solo.
- Acionamento automático da irrigação baseado em threshold.
- Controle manual via botão físico.
- Controle remoto via Blynk (MQTT).
- Sistema de timeout de segurança para desligamento automático.
- Alertas de solo seco.
- Feedback em tempo real do estado da válvula.

---

## ▶️ Como Executar

### Pré-requisitos

- Conta no Wokwi
- Token do Blynk Cloud

### Passos

1. Acesse o link da simulação no Wokwi
2. Acesse o site ou Instale o App (disponível nas lojas de aplicativos) do Blynk
3. Configure um projeto e adicione os Widgets correspondentes no Blynk
4. Configure o token do Blynk no arquivo `main.py`:
   ```python
   BLYNK_TOKEN = "SEU_TOKEN_AQUI"
5. Clique em Start Simulation
6. Interaja com:
- Potenciômetro → simula umidade
- Botão → controle manual
- App Blynk → controle remoto

## 📡 Comunicação MQTT

### Tópicos utilizados

ds/Umidade: envio da umidade atual
ds/Válvula: estado da irrigação (ligado/desligado)
ds/Alerta: alerta de solo seco
downlink/ds/Acionador: comando remoto

---

## 🔌 Simulação do Projeto

[A simulação completa pode ser acessada no Wokwi](https://wokwi.com/projects/450288761201413121)

---

## 🎥 Apresentação do Projeto

[Apresentação](https://youtu.be/7ijt-u6mrDE)
