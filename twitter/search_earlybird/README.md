## 실시간 검색 시스템, 대용량 쿼리 및 콘텐츠 업데이트 지원
**전체 트윗 검색 인덱스를 3개의 클러스터로 분할**
- 지난 7일 동안 게시된 모든 공개 트윗을 인덱싱하는 실시간 클러스터
- 동일한 기간 Private 트윗을 인덱싱하는 보호 클러스터
- 약 2일 전까지 게시된 모든 트윗을 인덱싱하는 아카이브 클러스터

```
Partition Manager : 파티션 매핑 관리, 인덱스 로드 및 플러시 처리
Real-time Indexer : 트윗의 Kafka 스트림을 지속적으로 읽고 업데이트
Query Engine : 분산 인덱스에 대한 검색 쿼리 실행 처리, 용어 기반 가지치기, 캐싱 등 다양한 최적화
Document Preprocesser : 원시 트윗을 인덱싱에 적합한 문서 표현으로 변환, 트윗 텍스트 및 메타데이터 토큰화, 정규화 및 분석 처리, write path 처리는 "Ingester"에서 관리
Index Writer : 트윗 문서를 인덱스에 쓰고 게시 목록 및 용어 사전을 포함하여 인덱스 구조 유지
Segment Manager : 파티션 내의 인덱스 세그먼트 관리, 인덱스 세그먼트를 디스크에 병합, 최적화 및 플러시하거나 라이브 세그먼트의 스냅샷을 생성하기 위해 HDFS로 플러시하는 일 담당
Searcher : 쿼리 대기 시간을 최소화하기 위해 캐싱 및 병렬 쿼리 실행과 같은 기술을 사용하여 인덱스에 대해 쿼리 실행. 채점 모델, 순위 알고리즘으로 결과 제공
```

## 중요 데이터 구조
- 문서 ID 목록에 대한 용어 간의 매핑을 저장하는 역색인. 해시 맵 형태(고유 용어, 트윗 목록)
- Doc ID 목록으로 저장소를 최적화하는 게시물 목록

## Architecture
![Twitter EarlyBird Architecture](https://github.com/21latte1007/open_source/assets/136875503/b2a4cc0e-2781-4af6-8ca6-8d21a36b6101)

## 코드 구조
### Root Dir
서버 구현 및 관련 클래스 : 검색 클래스, CPU 품질 요소, 서버 관리, 인덱스 구성, 기본 클래스, 서버 시작
```
EarlyBird Main > EarlyBird > EarlyBirdServer > PartitionManagerSetup
```

### Archive Dir
보관된 데이터의 관리 및 구성. EarlyBird Index 구성 처리 + /seg~ -> 세그먼트 빌드 업데이트
```
facotry.EbWireModule, factory.EbServerFactory 두 클래스로 데이터 파이프라인 집결
```

### Common Dir
로깅 요청 처리 및 Thrift 백엔드 기능을 위한 유틸리티 클래스
```
config/ -> EarlyBird 구성
userupdates/ -> 사용자 관련 데이터 처리
```

### Config Dir
서버 및 검색 쿼리 배포와 관련된 아카이브 클러스터에 대한 계층 구성 관리 전용
```
TierInfo -> factory.PartitionConfigUtil : tierName, Date, numPartition, maxTimeSlices, readType 등
TierConfig -> root.EbServerSerManager, archive.ArchiveTimeSlicer, factory.PartitionConfigUtil, partition.PartitionConfig
earlybird-tiers.yml의 값들 TierInfo에 매칭시켜 반환(불확실)
```

### Document Dir
다양한 Factory 및 Token Stream 작성자를 포함하여 문서 생성 및 처리
```
DocumentFactory -> document = data + fieldName + fieldType
ThriftIndexingEventDocumentFactory -> schema, cluster, decider
TweetDocument -> tweetID, timeSliceID, eventTimeMs, document
```

### Factory Dir
구성, Kafka 소비자 및 서버 인스턴스에 대한 유틸리티 factory 제공

### Index Dir
메모리 내 시간 매퍼, 트윗 ID Mapper 및 Facet을 비롯한 인덱스 관련 클래스 포함
- Facet : 검색 네비게이션, 검색 결과 세분화의 개념. 필터보다 유용하고 다양한 결과 제공(../cloud_search/SEO 참고)

### Segment Dir
segment 데이터 제공자 및 데이터 리더 클래스를 관리하기 위한 클래스 제공
```
segmentInfo : attachDocumentReaders, UpdateReaders, completeSegmentDocs, newDocumentReader
```

### Stat Dir
시스템과 관련된 통계를 추적, 보고 -> cpu, latency, errorcount, searchcount 등

### Tools Dir
Thrift 요청을 역질렬화하기 위한 유틸리티 클래스 보관

**Archive Segment**
- LuceneDir, MaxSegSize, TimeSliceID, Schema, SyncData, FacetCountingArray, DocValuesManager, DocIDToTweetIdMapper, TimeMapper, IndexExtensionData

### Partition Dir
Index 로더, Segment 작성기 및 시작 인덱서를 포함하여 파티션 및 인덱스 Segment 관리
```
FreshStartupHandler => EarlybirdWireModule, partition.kafkaStartUp
Post, PreOptimize => segmentbuildInfo, Manager, Topic, Factory, buffer
- EarlybirdIndex : tweetOffset, updateOffset, maxIndexedTweetId
- EarlybirdkafkaConsumer : BalancingKafkaConsumer, PartitionWriter, underlyingKafkaConsumer, earlybirdIndexFlusher, searchIndexingMetricset, IndexCaughtUpMonitor
- kafkaStartup : EarlybirdkafkaConsumer(^), startupUserEventIndexer, queryCacheManager, segmentManager, earlybirdIndexLoader, freshStartupHandler, userUpdatesStreamIndexer, userScrubGeoEventStreamIndexer 등 다수
- partitionConfig : tierName, clusterName, startedDate, IndexingHashPartition, maxEnabledLocalSegments, numPartition 등 다수
- segmentInfo : EarlybirdSegment, SegmentSyncInfo, Segment, EarlybirdIndexConfig
- segmentSyncInfo : Segment, SegmentSyncConfig 등 다수
```

### QueryCache Dir
캐시 구성 및 업데이트 작업을 포함하여 쿼리 및 쿼리 결과에 대한 캐싱 구현

### QueryParser Dir
쿼리 재작성기와 고빈도 용어 추출을 포함하는 파일. 쿼리 구문 분석 가능

### Search Dir
검색 요청 처리. 결과 수집기 및 Facet 수집기와 같은 읽기 경로 관련 클래스 포함
```
facets : 0.0 weight로 시작해 가중치 증가
queries : query문 Searcher로
relevance
  - collectors : schema, searchRequestInfo, scoringFunction, searcherStats, Cluster
  - scoring : lucene + reputation + textScore + reply + multipleRetry + retweet / favContrib, parusContrib, video…… scores
```

### Facet Dir
패싯 계산, 패싯 반복자, 패싯 레이블 공급자 및 패싯 응답 재작성 처리

### Index Dir
```
- column : 인덱스의 다양한 최적화 버전 포함. 문서 값 관리 및 업데이트 처리
- extensions : 인덱스 확장에 대한 클래스
- inverted : 반전된 인덱스 및 해당 구성 요소 / 게시 목록 및 용어 사전 처리(역색인)
- util : 검색 반복기 및 필터를 관리하기 위한 유틸리티 클래스. 검색 인덱싱 및 패싯 계산 효율적인 처리. 역색인. 모듈식 검색 인덱싱 시스템
```

### Ingester
원시 트윗 및 사용자 업데이트를 사용하고 변환하여 Earlybird가 사용하고 이후에 색인을 생성할 수 있도록 Kafka 주제에 작성하는 서비스
1. Tweet Injester
   색인 생성 기능하도록 다양한 필드와 기능 추출
2. UserUpdated Injester
   사용자 비활성화, 일시 중지 또는 보드에서 제외되었는지 여부 등 사용자 안전 정보

### feature_update_service
리트윗, 답글, 즐겨찾기 등의 트윗 기능 업데이트를 Earlybird에 전송하는 서비스. 이로부터 Ealrybird는 홈 타임라인 트윗의 순위를 매김
