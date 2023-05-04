from kafka import KafkaProducer
from dotenv import load_dotenv
import os
import ssl

load_dotenv("/usr/src/app/.env")

def init_producer():
    sslSettings = ssl.SSLContext(ssl.PROTOCOL_TLS);
    sslSettings.verify_mode     = ssl.CERT_NONE
    brokers = os.getenv("KAFKA_ADVERTISED_HOST_NAME","").split(",")
    SASL_USERNAME=os.getenv("KAFKA_SASL_USERNAME")
    SASL_PASSWORD=os.getenv("KAFKA_SASL_PASSWORD")
    producer = KafkaProducer(bootstrap_servers=brokers,security_protocol="SASL_SSL",  sasl_mechanism="SCRAM-SHA-512", sasl_plain_username=SASL_USERNAME, sasl_plain_password=SASL_PASSWORD,ssl_context=sslSettings,api_version_auto_timeout_ms=100000)
    return producer