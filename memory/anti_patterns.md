# 🚫 Worker 5 중복 방지 규칙 (Anti-Patterns)

1. **순수 텍스트 배치 난독화 기법 나열 금지**:
   - `bat2exe-ghidra-forensics`는 순수 바이너리 역공학 전담이므로, 일반 텍스트 배치 난독화 역사나 기법 백서를 다루지 않는다. (해당 내용은 Worker 1의 `batch-obfuscation-research`에 위임)

2. **텍스트 레벨 AST 구문 분석기 중복 금지**:
   - 텍스트 오토마타나 AST 구문 트리 파서를 구현하지 않는다. (해당 기능은 Worker 4의 `cmd-ast-deobfuscator`에 위임)

3. **엔드유저용 상용 CLI 탈난독화 도구 중복 금지**:
   - 일반 사용자를 위한 원클릭 탈난독화 패키지를 구현하지 않는다. (해당 기능은 Worker 2의 `batch-deobfuscator-re`에 위임)

4. **블루팀 관제 룰셋 중복 금지**:
   - SIEM / EDR 연동 Sigma 규칙이나 일반 YARA 룰을 작성하지 않는다. (해당 기능은 Worker 3의 `batch-forensics-and-ghidra-re`에 위임)
