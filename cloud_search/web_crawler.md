## Web Crawler
- Fetch : Fetch는 다음에 방문할 URL을 가져와서 페이지를 방문한다. 방문이란 HTTP 요청을 보내 Response Body를 가져오는 과정. Body의 Dom 해석은 Parse 단계로 넘어간다.
= Multi-Thread Downloader
- Parse : 가져온 페이지 내의 다른 HyperLink를 추출하는 과정.
= URL extraction
- Dup URL Elim : 중복 URL 제거 단계

**Freshness, Revisiting, Scheduler**
- Uniform : 페이지의 성격이나 업데이트 주기에 관계 없이 페이지 재방문.
- Lambda Crawl : 자주 변화하는 페이지에 재방문 간격을 점점 줄여가지만 너무 많이 변화하면 거꾸로 점수를 깎는다 : 얼마나 자주 바뀌는지, 유저들이 얼마나 찾는지
- Machine Learning : 페이지 변경 여부를 예측 모델링
 ex) Multi-Aramed bandit : 카지노에서 어떤 슬롯머신에 투자를 해야 이익을 최대화할 수 있을지에 대한 문제를 풀기 위해 만들어진 알고리즘
- content seen : 중복 문서 필터링. 문장을 단어로 쪼갠 뒤 유사도 측정 등.
 ex) “~다”, “데”, “것” 등 흔히 등장하는 단어 : Stop-word 우선적으로 제거하는데 형태소 분리.

**Parallel Crawler : 어떻게 작업을 분리할까?**
Master-Slave : SPOF - Master Node가 사망하면 나머지 크롤러들의 작업도 X
Stand-Alone : 혼자서도 잘 해요. >> Firewall mode, Cross-over mode, Exchange mode

**URL exchange minimization**
- Parallel crawler은 성능이 가장 높다 알려져 있다. URL 교환이 자주 일어나기에 네트워크 비용도 높아진다는 것이 단점.
**Batch communication**
- URL set을 크롤러들끼리 한 번에 주고 받는 방법. 배치 단위로 URL 교환하기에 네트워크 통신량이 비교적 적다.
