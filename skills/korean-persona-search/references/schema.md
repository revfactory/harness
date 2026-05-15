# Nemotron-Personas-Korea 필드 스키마

> 출처: https://huggingface.co/datasets/nvidia/Nemotron-Personas-Korea (CC BY 4.0, NVIDIA, 2026-04-20)

총 26개 필드, 100만 행. 모든 텍스트는 한국어.

## 식별자

| 필드 | 타입 | 설명 |
|------|------|------|
| `uuid` | string(32) | 고유 식별자 (32자 hex). 출처 추적용. |

## 인구통계 (검색 키로 적합)

| 필드 | 타입 | 카디널리티 | 값 예시 |
|------|------|----------|---------|
| `sex` | categorical | 2 | "남자", "여자" |
| `age` | int | 19~99 | 정수 |
| `marital_status` | categorical | 4 | "미혼", "배우자있음", "사별", "이혼" |
| `military_status` | categorical | 2 | (예: "병역필", "해당없음") |
| `family_type` | categorical | 39 | 39종 가구 구성 |
| `housing_type` | categorical | 6 | "아파트", "단독주택", "다세대주택" 등 |
| `education_level` | categorical | 7 | "초등학교 졸업"~"대학원 졸업" 7단계 |
| `bachelors_field` | categorical | 11 | "인문", "사회", "교육", "공학", "자연", "의약", "예체능" 등 |
| `occupation` | string(2~40) | 매우 다양 | "응용 소프트웨어 개발자", "하역 및 적재 관련 단순 종사원" 등 |
| `district` | categorical | 252 | 시군구 (예: "서울-강남구", "광주-서구") |
| `province` | categorical | 17 | 광역 (예: "서울", "광주", "경기", "제주") |
| `country` | categorical | 1 | "대한민국" 고정 |

**Tip:** `district` 값은 `{province}-{시군구}` 포맷이다. province로 1차 필터 후 district로 좁히는 것이 효율적이다.

## 퍼소나 텍스트 (7종)

각 행은 7가지 관점의 퍼소나 텍스트를 포함한다. 시나리오에 맞게 선택해서 사용한다.

| 필드 | 관점 | 활용 |
|------|------|------|
| `persona` | 종합 요약 | 짧은 한 줄 소개 |
| `professional_persona` | 직업·커리어 | 업무용 에이전트 정의에 핵심 |
| `sports_persona` | 운동·여가 | 라이프스타일 에이전트 |
| `arts_persona` | 예술·문화 | 콘텐츠/미디어 에이전트 |
| `travel_persona` | 여행 | 여행/관광 시나리오 |
| `culinary_persona` | 음식 | 식음료/외식 시나리오 |
| `family_persona` | 가족·관계 | 가정/육아/소비자 에이전트 |

## 컨텍스트 (보조 필드)

| 필드 | 타입 | 활용 |
|------|------|------|
| `cultural_background` | string | 문화·지역 배경 서술. 어댑터 스킬이 톤 조절에 사용. |
| `skills_and_expertise` | string | 전문 역량 서술 |
| `skills_and_expertise_list` | string | 구조화된 리스트 (파싱 가능) |
| `hobbies_and_interests` | string | 취미·관심사 서술 |
| `hobbies_and_interests_list` | string | 구조화된 리스트 |
| `career_goals_and_ambitions` | string | 커리어 목표·야망 |

## 원시 샘플 행 예시

```json
{
  "uuid": "03b4f36a18e6469386d0286dddd513c8",
  "sex": "남자",
  "age": 74,
  "marital_status": "배우자있음",
  "occupation": "하역 및 적재 관련 단순 종사원",
  "province": "광주",
  "district": "광주-서구",
  "country": "대한민국",
  "professional_persona": "광주 서구의 하역 현장에서 수십 년간 짐을 쌓아 올리며...",
  "sports_persona": "주말이면 무등산 자락을 느릿느릿 걸으며 땀을 흘리고...",
  "...": "..."
}
```

## 라이선스

**CC BY 4.0** — 상업/비상업 자유, 저작자 표기 필수.

생성된 에이전트 정의에 다음 한 줄 출처 표기를 권장:

> 본 에이전트의 한국어 퍼소나는 NVIDIA Nemotron-Personas-Korea (CC BY 4.0)의 합성 데이터를 기반으로 한다.
