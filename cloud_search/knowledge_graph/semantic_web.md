## Semantic Web(시멘틱 웹)
컴퓨터가 사람을 대신하여 정보를 읽고, 이해하고 가공하여 새로운 정보를 만들어 낼 수 있도록 만든 차세대 지능형 웹 (자체적으로 탐색 및 수집, 논리 추론을 하는 정보처리 기능)
인터넷 정보를 의미망으로 통합한 “온톨로지 형태”로 이루어지며, 정보를 이해하고 다양한 정보 간 의미 요소를 연결함으로써 지능적 판단에 따라 추출, 가공하는 처리방식을 말한다. XML, RDF 등(정보 content 구조에 따른 명세서로서의 역할. 해당 분야의 지식 공유와 재사용. 해당 영역의 제약과 가정에 대한 명시. 지식과 프로세스의 분리 등의 장점을 가진다.)

**RDF**
RDF 스키마는 property에 대한 추가 정보를 제공함으로써 사용 방법을 보다 명확히 함. (Domain, Range)
Resource(Book, Person, Publisher)의 타입을 기술(type, class)
Not Like XML Schema
Resource를 설명하는데 있어 의미 표현을 추가한 것

**Domain(정의역), Range(공역)**
Domain은 property의 subject 클래스를 알려준다.
Range는 property의 Object(Value) 클래스를 알려준다.

**분산된 데이터의 웹에서**
Ora가 글을 작성했다 + Ora가 영화에 나왔다 = Ora가 글을 쓰고 영화에 나왔다.
