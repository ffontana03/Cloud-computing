from confluent_kafka import Producer
import json
import time
import random

# Si connette ai nostri 3 nodi locali
###
#conf = {
#    'bootstrap.servers': 'localhost:9094,localhost:9095,localhost:9096',
#    'client.id': 'ecommerce-producer',
#    'acks': 'all' # GARANZIA ZERO DATA LOSS: aspetta che tutti i nodi abbiano salvato il dato
#}
###

conf = {
    'bootstrap.servers': 'localhost:9094,localhost:9095,localhost:9096',
    'client.id': 'ecommerce-producer',
    'acks': 'all',
    
    # --- LA SICUREZZA TOTALE ---
    'security.protocol': 'SASL_SSL',       #Usa SIA Password SIA Crittografia
    'sasl.mechanism': 'PLAIN',             
    'sasl.username': 'admin_ecommerce',    
    'sasl.password': 'PasswordSicura123!', 
    'ssl.ca.location': 'broker.crt'        #Il certificato per leggere i dati criptati
}

producer = Producer(conf)
topic = 'ordini-ecommerce'

print("🛒 Avvio del Producer (Ricezione Ordini)...")

try:
    while True:
        ordine = {
            "id_ordine": random.randint(1000, 9999),
            "prodotto": random.choice(["Laptop", "Smartphone", "Cuffie", "Monitor"]),
            "prezzo": random.randint(50, 1500)
        }
        messaggio = json.dumps(ordine)
        
        producer.produce(topic, value=messaggio.encode('utf-8'))
        producer.flush()
        print(f"✅ Ordine inviato a Kafka: {messaggio}")
        
        time.sleep(2) # Un ordine ogni 2 secondi

except KeyboardInterrupt:
    print("\n🛑 Producer fermato.")