---
name: korean-persona-search
description: "한국어 퍼소나 데이터셋(nvidia/Nemotron-Personas-Korea, 100만 행)에서 직무·지역·연령·학력 등 다축 조건으로 후보를 검색하고 다양성 샘플링으로 N개를 반환. 한국 페르소나/한국인 캐릭터/한국 시나리오 에이전트 정의에 근거가 필요하거나, '한국어 페르소나 찾아줘', '한국 직장인 페르소나', '특정 지역/연령대 페르소나'를 요청하면 반드시 이 스킬을 사용할 것. 데이터셋 다운로드·로컬 캐시·Parquet 필터·다양성 샘플링까지 일괄 처리한다."
---

# Korean Persona Search — Nemotron-Personas-Korea Lookup

NVIDIA의 [Nemotron-Personas-Korea](https://huggingface.co/datasets/nvidia/Nemotron-Personas-Korea) (CC BY 4.0, 100만 행) 데이터셋에서 한국어 퍼소나를 다축 조건으로 검색하고, 결과를 다양성 보장하면서 N개로 샘플링한다.

## 왜 이 스킬이 필요한가

데이터셋은 **1.7B 토큰** 규모라 매번 전체 로딩이 비현실적이다. 이 스킬은 (1) 최초 사용 시 로컬 캐시로 다운로드하고, (2) Parquet **predicate pushdown**으로 메모리에 올리지 않고 필터링하며, (3) 다양성 샘플링으로 편향을 방지한다.

## 사용 시점

다음 상황에서 호출한다:
- 새 에이전트/팀 정의에 한국적 맥락의 퍼소나 근거가 필요할 때
- 특정 직무·지역·연령·학력 조합의 한국인 캐릭터가 필요할 때
- 가상 인터뷰·설문·UX 리서치용 페르소나가 필요할 때

호출하지 말 것:
- 영어/일본어 등 다른 언어 페르소나 (이 데이터셋은 한국 한정)
- 실존 인물 검색 (이 데이터셋은 합성 페르소나)

## 워크플로우

### Step 1: 캐시 준비

스크립트는 자동으로 캐시 상태를 점검한다. 미설치 또는 캐시 부재 시 안내가 출력된다.

```bash
python skills/korean-persona-search/scripts/download.py
```

캐시 경로(기본): `~/.cache/korean-persona-search/`. 환경변수 `KOREAN_PERSONA_CACHE_DIR`로 변경 가능.

의존성: `huggingface_hub`, `pyarrow`. 미설치 시 스크립트가 정확한 설치 명령을 출력한다.

### Step 2: 검색

`scripts/search.py`에 필터·샘플링 옵션을 전달하여 정규화된 JSON 카드를 받는다.

```bash
python skills/korean-persona-search/scripts/search.py \
  --province 서울 \
  --age-min 28 --age-max 38 \
  --occupation-contains 개발 \
  --n 5 --diversity sex,district \
  --persona-types professional,arts
```

자세한 옵션과 예시는 `references/filter-cookbook.md` 참조.

### Step 3: 결과 활용

출력은 JSON 배열, 각 원소는 정규화된 **퍼소나 카드**:

```json
{
  "uuid": "03b4f36a18e6469386d0286dddd513c8",
  "demographics": {
    "sex": "남자", "age": 34, "marital_status": "배우자있음",
    "education_level": "대학교 졸업", "bachelors_field": "공학",
    "occupation": "응용 소프트웨어 개발자",
    "province": "서울", "district": "서울-강남구",
    "family_type": "...", "housing_type": "아파트", "military_status": "..."
  },
  "personas": {
    "summary": "...",
    "professional": "...",
    "arts": "..."
  },
  "context": {
    "cultural_background": "...",
    "skills_and_expertise": [...],
    "hobbies_and_interests": [...],
    "career_goals_and_ambitions": "..."
  }
}
```

**필요한 퍼소나 텍스트만 요청**하면 페이로드가 줄어든다. 7종 중 선택: `summary | professional | sports | arts | travel | culinary | family`.

## 다양성 샘플링

`--diversity sex,province` 처럼 키를 지정하면, 1차 필터 후보군에서 해당 축의 분포가 고르도록 N개를 뽑는다 (라운드로빈 + 잔여 확률 가중). 기본 `seed=0`로 재현 가능.

다양성 미지정 시 단순 무작위 샘플링.

## 주의

- **PII 없음**: 합성 데이터셋이므로 실존 인물과 매칭되지 않는다. 그래도 출처 표기 필수 (CC BY 4.0).
- **편향 인식**: 데이터셋은 한국의 "현실 분포"를 반영하므로, 특정 직무·지역·연령은 자연스럽게 희소하다. 희소 조건 검색 시 결과가 비어 있을 수 있다. 이때 필터를 완화하라.
- **캐시 용량**: 기본 Parquet 캐시 ≈ 수 GB. `--shard-only N`으로 일부 shard만 받을 수 있다 (속도 우선 시).

## 참조

- 필드 스키마 상세: `references/schema.md`
- 검색 패턴 모음: `references/filter-cookbook.md`
- 데이터셋 카드: https://huggingface.co/datasets/nvidia/Nemotron-Personas-Korea
