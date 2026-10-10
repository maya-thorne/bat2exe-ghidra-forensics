# 🔍 전담 작업자 피드백 감사 및 리팩토링 체크리스트 (feedback_audit.md)

> **[상위 지침 연동]**: `_BY_PASSS/WORKER_FEEDBACK_GUIDE.md`
> **[기억 리트리벌 키워드]**: `@feedback`, `@clean-root`, `@english-naming`, `@semantic-commit`, `@security-audit`, `@custom-license`

---

## 📌 본 저장소 필수 개선 액션 플랜

- [x] **1. [@clean-root] 루트 디렉터리 슬림화 (최대 6~7개 항목 유지)**:
  - 루트 항목 7개로 슬림화 완수: `docs/`, `references/`, `src/`, `tests/`, `memory/`, `LICENSE`, `README.md` (및 숨김 `.gitignore`).
  - 모든 5대 백서 문서는 `docs/whitepapers/`로 이전 완료.
  - 1280x800 해상도에서 스크롤 없이 첫 뷰포트에 README.md 히어로 배너 및 제목 즉각 노출 확인.

- [x] **2. [@english-naming] 100% 영문 디렉터리 및 파일명 표준화**:
  - `references/batch_corpus_28`, `references/huggingface_ai`, `references/classic_samples`, `references/detection_rules`로 전면 영문 표준화.
  - `references/catalog.json`, `references/references_index.json` 색인 영문 경로 통합.
  - 저장소 내 모든 루트/상위 디렉터리 한글명 완전 제거.

- [x] **3. [@semantic-commit] 파일/모듈별 맥락 커밋 메시지 분리**:
  - 일괄 커밋 도배를 중단하고 컴포넌트별 7개 시맨틱 커밋 개별 발행 완료:
    - `chore(license): apply dedicated Maya Thorne Systems & Security Research License (MT-SRL)`
    - `sec(audit): enforce zero-leak security boundaries with clean .gitignore`
    - `refactor(naming): standardize reference corpus and datasets to pure english naming in references/`
    - `docs(whitepaper): relocate in-depth technical analysis papers to docs/whitepapers/`
    - `test(forensics): add automated regression test suite for PE32 unpacker engine`
    - `docs(memory): update feedback audit checklist and context specifications`
    - `style(layout): slim root directory to 7 items for optimal viewport hero banner visibility`

- [x] **4. [@security-audit] 전수 보안 감사 (Zero-Leak Audit)**:
  - `.gitignore` 완비 (`.env`, `*.log`, `__pycache__`, `*.tmp` 등 완전 차단).
  - 민감 설정, 토큰, 로컬 임시 파일 0건 확인 완료.

- [x] **5. [@custom-license] Maya Thorne 전용 라이선스 적용**:
  - 루트 `LICENSE` 파일을 Maya Thorne Systems & Security Research License (MT-SRL)로 교체 및 100% 반영 완료.

