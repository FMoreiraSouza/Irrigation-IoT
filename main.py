from machine import Pin, PWM, ADC
import time
from blynk import Blynk

pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)

servo_pin = PWM(Pin(18), freq=50)
led_pin = Pin(19, Pin.OUT)
botao_pin = Pin(17, Pin.IN, Pin.PULL_UP)

UMIDADE_SECO = 40
TIMEOUT_SEGURANCA = 10

irrigacao_ativa = False
botao_pressionado = False
ultima_acao_botao = 0
inicio_irrigacao = 0
ultimo_alerta_tempo = 0

def servo_abrir():
    servo_pin.duty(77)
    print("SERVO: ABERTO")

def servo_fechar():
    servo_pin.duty(25)
    print("SERVO: FECHADO")

def ler_umidade():
    valor_adc = pot.read()
    return int((valor_adc / 4095) * 100)

def alternar_irrigacao():
    """Alterna o estado de irrigação e envia status ao Blynk."""
    global irrigacao_ativa, inicio_irrigacao
    
    if not irrigacao_ativa:
        print("\n" + "="*50)
        print("INICIANDO IRRIGAÇÃO")
        print("="*50)
        
        irrigacao_ativa = True
        inicio_irrigacao = time.time()
        
        servo_abrir()
        
        client.publish("ds/Válvula", "1")
        
        print("IRRIGAÇÃO ATIVA")
        
    else:
        tempo_total = int(time.time() - inicio_irrigacao)
        
        print("\n" + "="*50)
        print("PARANDO IRRIGAÇÃO")
        print("="*50)
        
        irrigacao_ativa = False
        
        servo_fechar()
        
        client.publish("ds/Válvula", "0")
        
        umidade_final = ler_umidade()
        client.publish("ds/Umidade", str(umidade_final))
        
        print(f"Tempo total: {tempo_total} segundos")
        print(f"Umidade final: {umidade_final}%")

def verificar_timeout():
    """Verifica se o tempo limite de irrigação foi atingido."""
    global irrigacao_ativa, ultimo_alerta_tempo
    
    if not irrigacao_ativa:
        return
    
    tempo_decorrido = time.time() - inicio_irrigacao
    tempo_restante = TIMEOUT_SEGURANCA - tempo_decorrido
    
    if tempo_decorrido >= TIMEOUT_SEGURANCA:
        print("\nTIMEOUT ATINGIDO! Fechando automaticamente...")
        
        alternar_irrigacao()
        
        umidade_final = ler_umidade()
        client.publish("ds/Umidade", str(umidade_final))
        
        print(f"Umidade final após timeout: {umidade_final}%")
        return
    
    if tempo_restante <= 5 and time.time() - ultimo_alerta_tempo >= 5:
        print(f"ALERTA: Fechamento automático em {int(tempo_restante)}s")
        ultimo_alerta_tempo = time.time()

def mensagens(topic, value):
    """Função chamada quando uma mensagem downlink é recebida do Blynk."""
    print(f"Tópico: {topic}")
    print(f"Valor: {value}")
    
    if "ds/Acionador" in topic:
        valor = str(value).strip()
        
        print(f"COMANDO ACIONADOR DETECTADO: '{valor}'")
                
        if valor == "1" and not irrigacao_ativa:
            alternar_irrigacao()
        
        elif valor == "0" and irrigacao_ativa:
            alternar_irrigacao()

client = Blynk(
    "TXWN8KMT4D6j_gtkW6B3NDL7qE4sSxuL",
    mensagens,
    "Wokwi-GUEST",
    "",
    False
)

client.subscribe("downlink/ds/Acionador")

servo_fechar()
led_pin.value(0)
client.publish("ds/Válvula", "0") 

print("\n" + "="*60)
print("SISTEMA IRRIGAÇÃO")
print("="*60)

ultima_atualizacao = time.time()
contador = 0

while True:
    try:
        if time.time() - ultima_atualizacao >= 1:
            umidade = ler_umidade()
            
            client.publish("ds/Umidade", str(umidade))
            
            verificar_timeout()
            
            if not irrigacao_ativa:
                alerta = "1" if umidade < UMIDADE_SECO else "0"
                client.publish("ds/Alerta", alerta)
            
            estado_valvula_ds = "1" if irrigacao_ativa else "0"
            client.publish("ds/Válvula", estado_valvula_ds) 
            
            contador += 1
            if contador >= 5:
                if irrigacao_ativa:
                    tempo_irrigacao = int(time.time() - inicio_irrigacao)
                    tempo_restante = TIMEOUT_SEGURANCA - tempo_irrigacao
                    print(f"IRRIGANDO {tempo_irrigacao}s | Restante: {tempo_restante}s | Válvula: {estado_valvula_ds}")
                else:
                    print(f"Status: Umidade={umidade}% | Alerta={'SIM' if umidade < UMIDADE_SECO else 'NÃO'} | Válvula: {estado_valvula_ds}")
                contador = 0
            
            ultima_atualizacao = time.time()
        
        botao_atual = botao_pin.value()
        
        if botao_atual == 0 and not botao_pressionado:
            botao_pressionado = True
            tempo_atual = time.time()
            
            if tempo_atual - ultima_acao_botao > 0.5:
                alternar_irrigacao()
                ultima_acao_botao = tempo_atual
        
        if botao_atual == 1 and botao_pressionado:
            botao_pressionado = False
        
        if irrigacao_ativa:
            led_pin.value(0) 
        else:
            led_pin.value(1 if ler_umidade() < UMIDADE_SECO else 0) 
        
        time.sleep(0.05)
        
    except Exception as e:
        print(f"ERRO CRÍTICO NO LOOP PRINCIPAL: {e}")
        servo_fechar()
        irrigacao_ativa = False
        botao_pressionado = False
        try:
            client.publish("ds/Válvula", "0")
        except:
            pass
        time.sleep(1)