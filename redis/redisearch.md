## RediSearch
- RediSearch는 Redis 해시에 저장한 데이터를 인덱싱하고 해당 데이터를 조회하기 위한 쿼리 언어 제공.
- 데이터에 대해 복잡한 쿼리 및 집계를 실행할 수 있도록 하여 Redis를 훨씬 더 범용적인 데이터베이스로 활용.

### RediSearch 설치
```
docker exec -it redis-search-2 redis-cli
```

### 입력 데이터 예시
```
HSET movie:11002 title "Star Wars: Episode V - The Empire Strikes Back" plot "After the Rebels are brutally overpowered by the Empire on the ice planet Hoth, Luke Skywalker begins Jedi training with Yoda, while his friends are pursued by Darth Vader and a bounty hunter named Boba Fett all over the galaxy." release_year 1980 genre "Action" rating 8.7 votes 1127635 imdb_id tt0080684
HSET movie:11004 title "Heat" plot "A group of professional bank robbers start to feel the heat from police when they unknowingly leave a clue at their latest heist." release_year 1995 genre "Thriller" rating 8.2 votes 559490 imdb_id tt0113277
```

### 해시 검색
```
HMGET movie:11002
```

### 제목과 등급을 가져오기
```
HMGET movie:11002 title rating
```

### Rating 조절
```
HINCRBYFLOAT movie:11002 rating 0.1
```

### 인덱스 생성
```
FT.CREATE idx:movie ON hash PREFIX 1 "movie:" SCHEMA title TEXT SORTABLE release_year NUMERIC SORTABLE rating NUMERIC SORTABLE genre TAG SORTABLE
```

### 쿼리
```
FT.SEARCH idx:movie "war"
FT.SEARCH idx:movie "@title:war" RETURN 2 title release_year
```

### 데이터 추가
```
HSET movie:11033 title "Tomorrow Never Dies" plot "James Bond sets out to stop a media mogul's plan to induce war between China and the U.K in order to obtain exclusive global media coverage." release_year 1997 genre "Action" rating 6.5 votes 177732 imdb_id tt0120347
```

### 인덱싱된 필드 검색
```
FT.SEARCH idx:movie "never" RETURN 2 title release_year
```

### 20초 뒤에 삭제
```
EXPIRE "movie:11033" 20
```

### 데이터베이스의 모든 RediSearch 인덱스 목록을 가져오기
```
FT._LIST
```

### 인덱스에 대한 정보 얻기
```
FT.INFO "idx:movie"
```

### 새 필드, 가중치 추가
```
FT.ALTER idx:movie SCHEMA ADD plot TEXT WEIGHT 0.5
```

### 새로운 쿼리
```
FT.SEARCH idx:movie "empire @genre:{Action}" RETURN 2 title plot
```

### 인덱스 삭제
```
FT.DROPINDEX idx:movie
```
