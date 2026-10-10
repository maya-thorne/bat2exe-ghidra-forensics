# 📋 Worker 5 액티브 태스크 체크리스트 (bat2exe-ghidra-forensics)

## 📌 6대 필수 품질 과업

- [x] **1. 실제 깃허브 웹페이지 접속 및 인간 관점 UI/UX 실측 검증**:
  - Chrome CDP(포트 9227) 격리 탭으로 `https://github.com/maya-thorne/bat2exe-ghidra-forensics` 접속 완료.
  - 배너 실측 (823px × 219px, 데스크톱 깃허브 비율 최적화), 요소 정렬, 가독성 실측 완료.
  - 모든 배너/이미지 클릭 시 raw 미디어 뷰어로 튕기지 않도록 `<a href="...">` 래핑 유지 확인.
  - 실측 캡처: `bat2exe_forensics_ui_measurement_audit.png` (100.1 KB).

- [x] **2. 10개국어 다국어 네비게이션 및 시각 자료 현지화**:
  - 10개국어 문서(`docs/locales/*.md`) 링크 및 상단 국기 네비게이션 툴바 100% 정상 연결.
  - 10개국어 다크 터미널 SVG 히어로 배너(`docs/assets/locales/<lang>/banner.svg`) 전수 생성 및 렌더링 확인.

- [x] **3. 시각적 에셋(x86 레지스터 스키매틱 SVG / Ghidra 디어셈블러 애니메이션) 고도화**:
  - PE 헤더 및 인메모리 스터브 추출 워크플로우: `docs/assets/diagrams/pe_stub_unpacking_pipeline.svg` (1,000 × 500 SVG).
  - x86 CPU 레지스터 전이 및 UPX NRV2B 점프 스키매틱: `docs/assets/diagrams/x86_register_schematic.svg` (1,000 × 560 SVG).
  - 실시간 Ghidra RE 터미널 애니메이션 데모: `docs/assets/diagrams/ghidra_re_terminal_demo.svg` (900 × 420 SVG).
  - 순수 파이썬 PE32 자동 언패커 구현: `src/pe_stub_unpacker.py` 및 Ghidra 헤드리스 스크립트 `src/ghidra_headless_dump.py`.

- [x] **4. GitHub 공식 Release 및 Git Tag (`v1.0.0`) 발행**:
  - `v1.0.0` 정식 태그 생성 및 원격 푸시 완료.
  - GitHub Releases API를 통해 정식 릴리즈 노트 등록 완료: `https://github.com/maya-thorne/bat2exe-ghidra-forensics/releases/tag/v1.0.0`.
  - 릴리즈 페이지 실측 캡처: `bat2exe_forensics_releases_audit.png` (68.4 KB).

- [x] **5. 라이선스(LICENSE) 규격화 및 리버스 엔지니어링 면책 고지**:
  - 공식 LICENSE (MIT) 탑재 및 리버스 엔지니어링/방어 연구 목적 면책 조항 README 및 문서 하단 명시.

- [x] **6. 전역 규칙 준수 (AI 도구명/워터마크 0건)**:
  - 모든 코드, 스크립트, 주석, 마크다운 문서, 커밋 메시지에서 AI 도구명 및 워터마크 전면 배제 (Maya Thorne 저작자 표기 일관성 100% 준수).

---

## 🚀 실행 모드 & 협업 도구 지침 (Teamwork & Quality Invariants)
- 🤖 **/teamwork-preview 및 멀티 에이전트 협업 허용**: 필요 시 /teamwork-preview 및 서브에이전트 병렬 디스패치(invoke_subagent)를 적극 활용하여 작업 생산성 및 리서치/검증 품질을 극대화할 수 있습니다.
- 💎 **토큰 제한 없음 (Uncapped Token Mode)**: 토큰을 아끼기 위해 코드를 축약하거나 문서를 요약하지 마십시오. 완전한 코드, 완전한 다국어 문서, 고해상도 시각 에셋을 타협 없이 완성하십시오.
- 🔥 **/goal 완주 철칙**: **대충 X · 토큰제한X · 오래 걸린다고 품질 저하X**. 6대 품질 과업(브라우저 실측 검증, 10개국어 다이어그램 현지화, SVG/GIF 에셋, v1.0.0 릴리즈/태그, LICENSE)을 기계적/시각적으로 100% 입증될 때까지 완주하십시오.

---

## 🔍 피드백 리팩토링 & 키워드 기억 리트리벌 (Memory Recall Protocol)
> **[전담 피드백 체크리스트]**: `memory/feedback_audit.md` (상위: `_BY_PASSS/WORKER_FEEDBACK_GUIDE.md`)
> **[기억 소환 키워드]**: 프롬프트나 태스크에서 아래 키워드가 언급되면 즉시 해당 규칙을 엄격히 소환하여 실행합니다:
- **`@clean-root`**: 루트 항목을 6~7개로 극도 슬림화 (백서는 `docs/whitepapers/`, 레퍼런스는 `references/`로 이동하여 첫 뷰포트 배너 노출 보장).
- **`@english-naming`**: 한글 폴더/파일명 전면 금지, 100% 영문 표준 네이밍 치환.
- **`@semantic-commit`**: 일괄 커밋 도배 금지, 파일/모듈별 개별 맥락 커밋 메시지 적용.
- **`@security-audit`**: `.env`, 캐시, 불필요 바이너리 등 배제 및 클린 커밋 검증.
- **`@custom-license`**: Maya Thorne 전용 연구 라이선스(MT-SRL) 적용.
- **`@feedback`**: 사용자 3대 시각 피드백 종합 반영 체크리스트 완수.
