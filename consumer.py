from confluent_kafka import Consumer
import json
import time

#conf = {
#    'bootstrap.servers': 'localhost:9094,localhost:9095,localhost:9096',
#    'group.id': 'gruppo-fatturazione',
#    'auto.offset.reset': 'earliest'
#}

conf = {
    'bootstrap.servers': 'localhost:9094,localhost:9095,localhost:9096',
    'group.id': 'gruppo-fatturazione', # Identificativo del gruppo di lettura
    'auto.offset.reset': 'earliest',   # Riparte dall'inizio se cade
    
    # --- LA SICUREZZA TOTALE ---
    'security.protocol': 'SASL_SSL',       #Usa SIA Password SIA Crittografia
    'sasl.mechanism': 'PLAIN',             
    'sasl.username': 'admin_ecommerce',    
    'sasl.password': 'PasswordSicura123!', 
    'ssl.ca.location': 'broker.crt'        #Il certificato per leggere i dati criptati
}

consumer = Consumer(conf)
topic = 'ordini-ecommerce'
consumer.subscribe([topic])

print("💳 Avvio del Consumer (Elaborazione Pagamenti)...")

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        
        if msg is None: continue
        if msg.error():
            print(f"Errore: {msg.error()}"); continue
            
        ordine = json.loads(msg.value().decode('utf-8'))
        print(f"⏳ Elaborazione ordine {ordine['id_ordine']} in corso...")
        
        time.sleep(4) # Simulazione di lentezza (4 secondi)
        print(f"✅ Ordine {ordine['id_ordine']} processato con successo!\n")

except KeyboardInterrupt:
    print("\n🛑 Consumer fermato.")
finally:
    consumer.close()