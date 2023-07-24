## Apache Nutch
1. seed.txt에서 URL 목록을 읽고 URL을 regex-urlfilter 정규식과 비교하고 지원되는 URL로 crawldb를 업데이트.
2. bin/nutch에서 crawldb, segments 등을 생성하고 가져올 수 있는 URL의 목록을 만들어 segments 아래에 현재 시간으로 dir을 만든다.
3. 웹페이지 데이터 또는 이미지를 binary 데이터로 가져와 content에 저장.
4. content의 저장물은 parse_data와 parse_text로 분리.

- service.model.request의 seedList.seedUrl을 NutchServer가 읽고, Injector를 실행.
- Injector는 fetch 전의 URL들이 crawlDB에 추가. Inject는 Text 형태의 Seed URL을 Nutch가 URL을 관리하기 위한 메타데이터 저장소에 추가하는 작업. 크롤링 시작 URL 역할.
- Generator는 Partitioner를 통해 동일한 도메인을 동일한 Partition에서 처리.
- compare 함수 통해 topN URL 선택.
- fetch는 위에 의해 생성된 URL을 fetch, partition을 통해 Host 별로 1개의 queue 할당, 작업. Generate URL로부터 HTML Raw 파일 생성. segments 단위로 저장.
- parser는 fetch 이후의 분석, content를 parseTest, parseData로 분리.
- CrawlDB는 크롤링을 위해 관리하는 URL 메타정보를 쌓기 위한 DB. HDFS로 압축 저장.
- UpdateCrawlDB는 가져온 URL을 기준으로 DB Update 수행, inlinks, outlinks, fetchTime, score Update

**CrawlBase**
url : CrawlStatus(현재 상태를 나타내는 필드)에 사용
crawlDatum : 메타데이터를 저장 / crawlHistory : 역순으로 정렬된 CrawlDatum 개체 목록

**CrawlList**
url : CrawlHistory 필드에 사용(CrawlList는 다중의 동시적 크롤링을 위해 CrawlBase와 분리)

**FetchedContent**
url : BytesWritable, FetchStatus(fetch, 에러 코드, 기타 fetch 정보에 대한 상태를 가지며 메타 데이터를 저장 - 다른 tool을 통해 CrawlBase로 반환되는 필드) 필드에 사용

**ParsedContent**
url : MapWritable 필드에 사용 / MapWritable : Writable(Text) 또는 Writable[] 객체를 포함하고 컨텐츠 (href, header 등) 내의 각각 다른 모든 유형의 요소들 parsing

**Processing**
parsedContext를 가져와서 여러 개의 특정 데이터 파츠로 변환(Scoring에 사용). CrawlBase 업데이트, Parsed Content 분석, 다른 소스의 Data Integration 처리. Processer의 일부는 컨텐츠를 Scorer가 필요로 하는 포멧으로 변환.
Scoring
- url : Float 형으로 각각의 Field에 사용 / Field : 이름, 값, score, Text의 Float형 필드. (Lucene semantic)을 필요로 하며 Score와 함께 인덱싱된 필드는 Field Boost 되었다 함)
- Scoring : 분석 시 각 Field의 형식을 출력하여 특정 데이터 파츠를 가져옴.
- Indexing : 문서의 Boost를 토대로 무서의 최종 Score를 생성.

**Web Database**
Nutch가 수집한 모든 URL에 대한 정보를 포함하며 여기에는 각각의 페이지들을 이어주는 링크 정보 포함.

**Segment list**
각각의 Segment는 fetch된 페이지와 Index 정보를 포함. (검색은 Segment 단위로 이루어짐)
Segment
FetchList : fetch된 페이지들의 이름을 가진 파일. Web DB에 의해 생성. 웹 페이지의 분석과 랭킹 알고리즘을 적용하기 위한 Basic Data로 사용됨.

**Fetch Output**
fetch된 파일의 정보를 포함한 파일. fetcher_content, fetcher_text 두 가지 타입.
- fetcher_content : 원본 데이터 그대로 가짐.
- fetcher_text : text 형식의 데이터만을 가짐.
- fetch 과정이 끝난 후 fetch된 웹페이지에서 <key, value> 형식의 index.data로 재구성된다.
- key : 현재 페이지가 존재하는 Segment 내에서 사용되는 일련번호 // vlaue : 문서 내용
fetch output 데이터는 Nutch Reader에 의해 조치가 가능한 포멧으로 저장.

**Ingector**
```
Data Source를 crawlBase에 주입하여 새로운 CrawlBase, CrawlHistory 객체를 생성.
crawlBase에서 URL의 상태를 업데이트하거나 수동으로 변경할 때 사용.
```

**Generator**
```
CrawlBase에서 CrawlList 생성 - Generator 내의 Filter는 CrawlBase URL의 부분 집합에서만 실행되도록 생성 가능.
```

**Fetcher**
```
CrawlList를 가져와서 FetchedContent 객체 생성.
```

**UpdateCrawl**
```
CrawlBase의 URL을 FetchedStatus 객체로 업데이트.
```

**FetchedContent**
```
데이터베이스에 새로운 URL을 추가하지 않고 현재 URL만 업데이트.
```

**Parser**
```
FetchContent 소스에서 ParsedContent 객체 생성 - 여러 조건에 따른 parser 다중 실행 가능.
```

**Processors**
- New URL : ParsedContent 소스에서 parsing된 새로운 URL을 가지고 crawlBase를 업데이트하는 프로세서.
- HTML : ParsedContent의 HTML 소스에 대한 특정한 Processing을 수행하는 프로세서.
- Link : URL의 inlink와 outlink에 대한 특정한 데이터베이스를 생성하는 프로세서.
- BlackList : 블랙리스트 URL은 indexing 과정에서 해당 URL과 콘텐츠를 제거하는 프로세서.
- Other : 언어 식별. redirection된 URL의 처리 및 Scoring과 같은 기카 특징 기능을 수행하는 프로세서.

**Scorers**
- Html Scorer : html을 분석하여 Scoring.
- Link Scorer : 링크 분석을 통해 page-rank 유형의 score를 생성.
- Other Scorer : 기타 특정 기능을 수행하는 scorer

**Indexer : 여러 개의 Scoring 객체에서 Lucene Index 생성.**
- Query Tools : Nutch 내에서 사용되는 Query Tool

## Architecture
### InjectorJob
```
Injector는 Crawling과 관련된 데이터를 저장하기 위해서 Apache Nutch가 만드는 디렉터리인 CrawlDB에 필요한 URL을 추가하는 역할을 수행.
InjectorJob이 수행된 뒤에는 fetch되지 않은 다수의 URL들이 CrawlDB에 추가.
```

### GeneratorJob
```
InjectorJob을 수행하고 CrawlDB에 추가된 URL들을 fetch하기 전에 GeneratorJob을 수행. GeneratorJob은 새로운 batch를 생성하고 InjectorJob 이후에 URL이 추가된 webtable에서 fetch 작업을 수행할 URL들을 가져온다.
```
**Mapper**
webtable에서 모든 URL을 읽어온다.
1. URL이 이전에 generate되었을 경우(mark가 생성되어 batchID가 있는 경우) Skip.
2. 선택적으로 URLNormalizer 또는 URLFilters를 사용하여 빠른 generate에 대한 제어가 가능.
3. URL의 fetch time을 확인.(fetch time이 현재 시점보다 이전일 경우에 우선적으로 fetch 실행.)
4. URL에 대한 socring 실행.
5. fetch가 필요한 모든 URL에 대해서 score와 함께 산출.
**Partition**
모든 URL은 도메인, 호스트 또는 IP로 나눠진다. 동일한 도메인(호스트, IP)의 모든 URL은 동일한 파티션에서 동일한 reduce task로 처리. 각 파티션 내에서 모든 URL은 score 순서대로 정렬.
1. 선택적으로 Partitioning하는 동안 normalize 처리를 할 수 있고 이것은 URL의 빠른 Partisioning을 비황성화한다. IP로 partitioning을 할 경우 DNS 분석 시 많은 부하가 걸릴 수 있다.
**Reducer**
파티션의 모든 URL을 읽고 선택하는 역할을 하는데, 전체 URL 수가 한계에 도달하거나 도메인 당 URL 수가 한계에 도달할 때까지 계속해서 작업 진행.
1. 해당 도메인의 URL 수가 generate.max.count 속성 값을 초과하는 경우 URL 선택 중단. Reducer는 map을 사용하여 추적이 이뤄지는데, 동일한 도메인의 경우 같은 reduce task 내에서 처리되기 때문에
**Result**
maximum topN URL이 선택되고 webtable에 마킹이 이루어짐(항상 score로 선택되지는 않음). 각 reducer(파티션)은 topN/reduce의 연산 결과를 통해 URL을 Generate할 수 있다. Partitioning으로 모든 reducer가 generate 가능한 URL 개수를 선택할 수 있는 건 아니지만 확장성을 얻게 된다.
```
ex) top N = 2500 / generate.max.count = 100 / reducer = 5
10, 100, 1000 => 10, 100, 100
```

### FetcherJob
```
FetcherJob은 GeneratorJob에 의해 생성된 URL을 fetch하는 역할을 수행
command로 실행 시 설정한 파라미터에 따라 특정 batchID의 선택적인 URL 또는 모든 URL을 가져와 Fetch
```
**Mapper**
GeneratorJob에서의 역할과 마찬가지로 webtable에서 모든 URL을 읽어온다.
1. generator mark의 일치여부 확인.
2. URL에 fetcher mark가 있을 때 continue일 경우 skip. 반대일 경우 현재 batchID의 batch에서 fetch되었던 모든 URL들을 다시 refetch하는 작업을 수행.
3. 랜덤으로 생성된 int 값을 키값으로 산출(모든 URL에 대한 shuffle)
**Partition**
Host 별로 Partitioning 작업이 이루어진다.
**Reducer**
FetcherJob의 Reducer는 Host, Domain, Ip의 대기 큐를 지원한다.
1. 랜덤화된 URL을 fetch queue에 넣고 fetch queue에서 fetch할 항목을 스캔. 밸런스 있는 fetch를 위해 도메인(Host, IP)당 1개의 queue가 설정된다.
2. 각각의 URL에 대해 fetch 작업을 수행.
3. webtable에 성공, 실패 여부 출력(fetchTime 값을 현재 시간으로 설정)
4. parsing이 구성된 경우 ParseUtil class를 사용하여 해당 content Parsing(fetch 안 된 것 제외)

### ParserJob
```
ParserJob은 FetcherJob 이후에 fetch된 URL을 Parsing(구문 분석)하는 역할을 수행, 설정된 batchID 내의 모든 URL을 대상으로 이루어지며 CMD로 실행 시 파라미터에 따라 전체, 부분 Parsing 진행.
```
**Mapper**
webtable에서 모든 URL을 읽어온다.
1. fetch mark의 일치 여부 확인.
2. URL이 이미 parsing되었다면 skip.
3. row 단위 Parsing.
4. row 단위 Parsing된 결과 webtable에 출력.

### DbUpdateJob
```
ParseJob 완료 이후에 FetcherJob의 결과를 제공하여 마지막으로 가져온 URL을 기준으로 DB를 업데이트하는 역할 수행. 각 row의 inlinks, outlinks, fetchTime 및 score 업데이트.
```
**Mapper : webtable의 모든 URL 추출**
1. 모든 outlinks의 score 업데이트.
2. 모든 outlinks를 score와 anchor(linktest)와 함께 출력.
3. rowkey 자체를 score와 함께 출력.
**Partition : Reducer에서 inlinks 값이 score에 따라 정렬**
1. {url}에 따른 파티션
2. {url}에 따른 그룹화
3. {url, score}에 따른 정렬
**Reducer의 key는 webtable에서의 각각의 row이며 inlinks가 reduce의 값**
1. fetchTime 업데이트.
2. inlinks 업데이트(db.update.max.inlinks로 수정 가능).
3. inlinks 기반의 각각의 row가 가진 score 값을 업데이트.
4. 각각의 row를 webtable에 출력.
**Scoring**
1. 문서의 Scoring은 “Parse”, “Index”, “Score” 등에서 행해진다.
2. 구문분석은 lucene에서 지원하고 있으며 Nutch는 테스트에 가까운 간단한 구문 분석기만 제공하고 있다.
3. WebGraph는 Inlink용, Outlink용, 현재 점수보유 node용 데이터베이스 생성.
4. LinkRank는 WebGraph 생성 이후 반복링크 분석, 모든 URL에 대해 공통 점수로 시작. 들어오는 링크의 수와 해당 링크의 점수 및 페이지에서 나가는 링크의 수를 기반으로 각 URL에 대한 글로벌 점수 생성. 친족랭크 무시. 반복 횟수 구성 가능.
5. ScoreUpdater를 통해 LinkRank가 분석한 점수를 CrawlDB로 업데이트한다.
6. Link Score는 200가지 이상의 판단재료 중 하나.
7. Injector-scoring : 페이지의 URL이나 CrawlDatum 값을 전달하여 특정 URL에 대한 초기점수 계산.
   Generator-scoring : fetchList 생성 시 상위 N개의 점수 페이지를 정렬하고 선택하기 위한 정렬 값을 준비하는 방법을 구현.

## Apache Lucene - IndexSearcher
- Scoring : 문서의 랭킹에 있어 중요한 Term Weighting. 단어의 가중치.
  자주 출현하는 단어는 그 문서를 대표.  Term Frequency == tf
  여러 문서에 자주 출현하는 단어는 범용적인 단어로 중요도 하락 == idf
  단어의 가중치는 tf@idf
- Boost : term의 가중치를 결정하기 위해 사용 - content, url, title, anchor 등
- QueryNorm : Query의 Term을 정규화하기 위해 사용
- LengthNorm : content, url, title, anchor 등 정규화
- Coord : 평준화. Score가 아주 작은 숫자로 변동이 있을 경우 적절한 값을 곱해준다.

## Apache Nutch - plugin
**대표 플러그인**
```
IndexWriter : 크롤링된 데이터를 특정 BE에 쓰기.
IndexingFilter : 인덱싱된 필드에 메타데이터 추가 허용.
Exchange : 인덱스 작성기가 여러 개인 경우 특정 인덱스 작성기로 인덱싱하는 동안 문서 라우팅 가능.
Parser : 인덱싱할 데이터를 추출하기 위해 가져온 문서를 읽는 파서 구현 - 유능 위해선 필수.
HtmlParseFilter : Html 구문 분석에 메타데이터 추가.
Protocol : ftp, http 등으로부터 문서 파싱 가능.
URLFilter : URL 제한.
URLNormalizer : URL을 일반 형식으로 변환하고 선택적으로 대체를 수행.
ScoringFilter : CrawlDatum 및 결과 검색 색인에서 채점 변수 조작.
SegmentMergeFilter : 세그먼트 병합 중 필터링. URL보다 정교.
Extension Point : 확장 지점을 타사 기능으로 확장할 수 있는 플러그.
Extension : Extenstion Point의 타사 기능 향상, 인터페이스를 구현해야 하며 예상되는 형식으로 데이터를 반환해야 함.
Plugin : 하나 이상의 Extension implemention 모음. Extension Point 를 구동하는데 필요.
```
