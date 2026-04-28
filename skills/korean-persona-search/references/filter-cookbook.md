# 필터 쿡북 — 자주 쓰는 검색 패턴

`search.py`의 옵션을 조합한 실용 패턴 모음. 그대로 복사해서 쓰거나 변형해서 사용한다.

## 옵션 요약

| 옵션 | 의미 | 예시 |
|------|------|------|
| `--province NAME` | 광역 단위 (17종) | `--province 서울` |
| `--district NAME` | 시군구 (252종, `province-시군구` 포맷) | `--district 서울-강남구` |
| `--sex NAME` | "남자" 또는 "여자" | `--sex 여자` |
| `--age-min N` / `--age-max N` | 연령 범위 (19~99) | `--age-min 25 --age-max 39` |
| `--education-level NAME` | 학력 (7종) | `--education-level "대학교 졸업"` |
| `--bachelors-field NAME` | 전공 계열 (11종) | `--bachelors-field 공학` |
| `--marital-status NAME` | 혼인 상태 (4종) | `--marital-status 미혼` |
| `--family-type NAME` | 가구 유형 (39종) | `--family-type "부부+미혼자녀"` |
| `--housing-type NAME` | 주거 (6종) | `--housing-type 아파트` |
| `--military-status NAME` | 병역 (2종) | `--military-status 병역필` |
| `--occupation-contains TEXT` | 직업명 부분일치 | `--occupation-contains 개발` |
| `--keywords A,B,C` | 페르소나 텍스트 부분일치 (OR) | `--keywords "스타트업,디자인"` |
| `--persona-types LIST` | 출력 페르소나 종류 | `--persona-types professional,arts` |
| `--n N` | 결과 개수 (기본 5) | `--n 10` |
| `--seed N` | 무작위 시드 (기본 0) | `--seed 42` |
| `--diversity LIST` | 다양성 축 | `--diversity sex,province,age_band` |
| `--shard-only N` | 첫 N개 shard만 사용 (속도 우선) | `--shard-only 1` |
| `--out PATH` | 파일 저장 (기본: stdout) | `--out _workspace/personas.json` |

## 패턴 1: 서울 IT 직장인 5명 (성별 균형)

```bash
python skills/korean-persona-search/scripts/search.py \
  --province 서울 \
  --age-min 28 --age-max 42 \
  --bachelors-field 공학 \
  --occupation-contains 개발 \
  --diversity sex,district \
  --persona-types professional \
  --n 5
```

## 패턴 2: 지방 소도시 자영업자 (다양한 업종)

```bash
python skills/korean-persona-search/scripts/search.py \
  --keywords "자영업,소상공인,가게,운영" \
  --diversity province,age_band,occupation_root \
  --persona-types summary,professional,family \
  --n 6
```

## 패턴 3: 20대 대학생/취준생 페르소나

```bash
python skills/korean-persona-search/scripts/search.py \
  --age-min 20 --age-max 26 \
  --marital-status 미혼 \
  --keywords "대학,학생,진로,취업" \
  --diversity sex,province,bachelors_field \
  --persona-types summary,arts,sports \
  --n 8
```

## 패턴 4: 워킹맘 페르소나 (UX 리서치용)

```bash
python skills/korean-persona-search/scripts/search.py \
  --sex 여자 \
  --age-min 30 --age-max 45 \
  --marital-status 배우자있음 \
  --family-type "부부+미혼자녀" \
  --keywords "직장,일,경력,자녀" \
  --diversity province,occupation_root \
  --persona-types professional,family \
  --n 5
```

## 패턴 5: 60대 이상 시니어 (지역 다양)

```bash
python skills/korean-persona-search/scripts/search.py \
  --age-min 60 --age-max 80 \
  --diversity province,sex,occupation_root \
  --persona-types summary,family,culinary \
  --n 6
```

## 패턴 6: 키워드 기반 자유 검색 (다양성 우선)

```bash
python skills/korean-persona-search/scripts/search.py \
  --keywords "창업,디자인,브랜드" \
  --diversity sex,age_band,province \
  --persona-types professional,arts \
  --n 7 \
  --seed 42
```

## 다양성 축 키 일람

`--diversity` 옵션에 사용할 수 있는 키:

| 키 | 의미 | 비고 |
|----|------|------|
| `sex` | 성별 | 2종 |
| `province` | 광역 | 17종 |
| `district` | 시군구 | 252종 (province 균형 후 district 다양화 권장) |
| `age` | 정확 연령 | 너무 세분화됨, 권장하지 않음 |
| `age_band` | 연령대 | 자동 산출: 20대/30대/40대/... |
| `education_level` | 학력 | 7종 |
| `bachelors_field` | 전공 | 11종 |
| `family_type` | 가구 | 39종 |
| `marital_status` | 혼인 | 4종 |
| `occupation_root` | 직업 대분류 | 자동 추출: 첫 어절 또는 KSCO 대분류 추정 |

여러 키를 조합하면 라운드로빈으로 가능한 다양성을 확보한다.

## 결과 비어있을 때

희소 조건이면 결과가 0~소수일 수 있다:
- 필터 강도 완화 (예: 시군구 → 광역)
- 키워드 OR 확대
- `--shard-only`를 늘리거나 제거

## 출력 후처리

JSON 출력은 `_workspace/personas.json`처럼 파일로 저장하면 다른 에이전트가 참조하기 좋다. 정규화된 카드 구조는 `SKILL.md`의 "결과 활용" 섹션 참조.
