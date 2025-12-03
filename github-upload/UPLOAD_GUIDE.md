# GitHub 업로드 가이드

## 📦 준비된 파일들

다음 파일들이 `github-upload/` 폴더에 준비되어 있습니다:

### 메인 스크립트
- `suuktest_manager.py` - Suuktest 폴더 통합 관리 시스템
- `resolve_manager.py` - 범용 Resolve 관리 도구
- `organize_by_extension.py` - 미디어풀 정리 전용

### MCP 서버 확장
- `mcp_suuktest_tools.py` - Suuktest MCP 툴
- `mcp_xml_import_tools.py` - XML 임포트 MCP 툴

### 문서
- `README.md` - 메인 README
- `SUUKTEST_QUICKSTART.md` - Suuktest 퀵스타트
- `XML_IMPORT_GUIDE.md` - XML 임포트 가이드

### 설정 파일
- `.gitignore` - Git 제외 파일

---

## 🚀 GitHub에 업로드하기

### 방법 1: 터미널에서 직접 업로드 (추천)

```bash
# 1. github-upload 폴더로 이동
cd ~/Downloads/github-upload

# 2. Git 초기화 (처음만)
git init

# 3. 리모트 추가 (처음만)
git remote add origin https://github.com/feeldizDI/res.git

# 4. 파일 추가
git add .

# 5. 커밋
git commit -m "Add Suuktest folder management system and DaVinci Resolve automation tools"

# 6. 푸시
git push -u origin main

# 또는 브랜치가 master인 경우:
# git push -u origin master
```

### 방법 2: GitHub Desktop 사용

1. **GitHub Desktop 열기**
2. **File → Add Local Repository**
3. **github-upload 폴더 선택**
4. **Commit to main** 클릭
5. **Push origin** 클릭

### 방법 3: 기존 리포지토리에 추가

```bash
# 1. 기존 리포지토리 클론
git clone https://github.com/feeldizDI/res.git
cd res

# 2. github-upload 폴더의 파일들을 복사
cp -r ~/Downloads/github-upload/* .

# 3. 파일 추가 및 커밋
git add .
git commit -m "Add Suuktest folder management system and automation tools

Features:
- Suuktest folder integration (/Users/Shared/suuktest)
- XML/AAF/EDL timeline import
- Media pool auto-organization
- Offline clip relinking
- MCP server extensions for Claude AI integration
- Comprehensive documentation"

# 4. 푸시
git push origin main
```

---

## 📝 커밋 메시지 예시

### 간단한 버전
```bash
git commit -m "Add DaVinci Resolve automation tools"
```

### 상세한 버전
```bash
git commit -m "Add comprehensive DaVinci Resolve automation system

Features:
- Suuktest folder management system
- XML/AAF/EDL timeline import
- Media pool auto-organization by extension
- Offline clip auto-relinking
- MCP server extensions for Claude AI
- Interactive menu interface
- Full documentation

Tools included:
- suuktest_manager.py (main tool)
- resolve_manager.py (general purpose)
- organize_by_extension.py (media pool cleanup)
- mcp_suuktest_tools.py (Claude integration)
- mcp_xml_import_tools.py (Claude integration)
"
```

---

## 🔐 인증 문제 해결

### Personal Access Token (PAT) 사용

GitHub에서 비밀번호 대신 PAT를 사용해야 할 수 있습니다:

1. **GitHub.com 로그인**
2. **Settings → Developer settings → Personal access tokens**
3. **Generate new token (classic)**
4. **repo 권한 선택**
5. **토큰 생성 및 복사**

### 푸시 시 토큰 사용
```bash
git push https://YOUR_TOKEN@github.com/feeldizDI/res.git main
```

또는 자격 증명 저장:
```bash
git config credential.helper store
# 그 다음 push할 때 토큰 입력하면 저장됨
```

---

## 📊 업로드 후 확인사항

### GitHub 웹사이트에서 확인
1. https://github.com/feeldizDI/res 접속
2. 파일 목록 확인:
   - ✅ README.md
   - ✅ suuktest_manager.py
   - ✅ resolve_manager.py
   - ✅ organize_by_extension.py
   - ✅ mcp_suuktest_tools.py
   - ✅ mcp_xml_import_tools.py
   - ✅ SUUKTEST_QUICKSTART.md
   - ✅ XML_IMPORT_GUIDE.md
   - ✅ .gitignore

3. README.md가 제대로 렌더링되는지 확인

---

## 🎯 추가 Git 명령어

### 변경사항 확인
```bash
git status
```

### 특정 파일만 추가
```bash
git add suuktest_manager.py
git add README.md
```

### 이전 커밋 수정
```bash
git commit --amend -m "New commit message"
```

### 강제 푸시 (주의!)
```bash
git push -f origin main
```

### 브랜치 확인
```bash
git branch
```

### 브랜치 변경
```bash
git checkout main
# 또는
git checkout master
```

---

## ⚠️ 주의사항

1. **민감한 정보 제거**
   - API 키, 비밀번호 등이 코드에 없는지 확인
   - .gitignore에 민감한 파일 추가

2. **파일 크기**
   - 100MB 이상 파일은 Git LFS 사용
   - 불필요한 대용량 파일 제외

3. **라이센스**
   - 적절한 라이센스 파일 추가 고려

---

## 📞 문제 발생 시

### 오류: "remote: Permission denied"
→ GitHub 계정 권한 확인 또는 PAT 사용

### 오류: "Updates were rejected"
→ Pull 먼저 실행: `git pull origin main`

### 오류: "fatal: not a git repository"
→ `git init` 실행

### 파일이 추적되지 않음
→ `.gitignore` 확인 및 `git add -f [파일명]` 사용

---

## ✅ 완료!

업로드가 완료되면 다음 URL에서 확인하세요:
https://github.com/feeldizDI/res
