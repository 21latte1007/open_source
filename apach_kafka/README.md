## Apache Kafka
### ZooKeeper 서비스를 시작
```
sudo bin/zookeeper-server-start.sh config/zookeeper.properties
```
### Kafka 브로커 서비스를 시작
```
sudo bin/kafka-server-start.sh config/server.properties
```

### 입력 주제 생성
```
sudo bin/kafka-topics.sh --create \
    --bootstrap-server localhost:9092 \
    --replication-factor 1 \
    --partitions 1 \
    --topic streams-plaintext-input
```

### 출력 주제 생성
```
sudo bin/kafka-topics.sh --create \
    --bootstrap-server localhost:9092 \
    --replication-factor 1 \
    --partitions 1 \
    --topic streams-wordcount-output
```

### 입력 데이터 예제 생성
```
echo -e "all streams lead to kafka\nhello kafka streams\njoin kafka summit" > /tmp/file-input.txt
```

### 입력 데이터를 입력 주제로 송신
```
cat /tmp/file-input.txt | sudo bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic streams-plaintext-input
```

### 입력 데이터 스트림 처리
```
sudo bin/kafka-run-class.sh org.apache.kafka.streams.examples.wordcount.WordCountDemo
```

### 출력 데이터 확인
```
sudo bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 \
    --topic streams-wordcount-output \
    --from-beginning \
    --formatter kafka.tools.DefaultMessageFormatter \
    --property print.key=true \
    --property key.deserializer=org.apache.kafka.common.serialization.StringDeserializer \
    --property value.deserializer=org.apache.kafka.common.serialization.LongDeserializer
```
