# Suuktest 폴더 관리 시스템 - 퀵 스타트 가이드

## 📂 최상위 폴더 설정
```
/Users/Shared/suuktest
```

이 폴더를 기준으로 DaVinci Resolve가 모든 파일을 자동으로 읽고 쓸 수 있습니다.

---

## 🚀 빠른 시작 (3단계)

### 1단계: 스크립트 다운로드
- **[suuktest_manager.py](computer:///mnt/user-data/outputs/suuktest_manager.py)** - 독립 실행형 툴

### 2단계: 실행
```bash
python3 ~/Downloads/suuktest_manager.py
```

### 3단계: 메뉴에서 선택
```
1. Scan Suuktest folder structure       # 폴더 구조 확인
2. List all Suuktest projects           # 프로젝트 목록
3. Import folder to media pool          # 폴더 임포트
4. Import all XMLs from subfolder       # XML 타임라인 임포트
5. Auto-organize media pool             # 자동 정리
6. Relink all offline clips             # 오프라인 클립 릴링크
```

---

## 💡 실전 예시

### 예시 1: CJU_SE 프로젝트 임포트

```bash
# 스크립트 실행
python3 suuktest_manager.py

# 메뉴 선택
Select option: 3

# 서브폴더 입력
Enter subfolder: mac3/CJU_SE

# 자동 정리 여부
Organize by extension? y

# 결과:
✅ Total imported: 355 items
  - Video: 150 clips
  - Audio: 200 clips
  - Timelines: 5

📁 Created bins:
  - CJU_SE/
    ├─ Video/
    ├─ Audio/
    └─ Image/
```

### 예시 2: XML 타임라인만 임포트

```bash
Select option: 4
Enter subfolder: mac3/CJU_SE

# 결과:
✅ Imported 5/5 timelines:
  - edit_v1
  - edit_v2
  - rough_cut
  - fine_cut
  - final
```

### 예시 3: 오프라인 클립 자동 릴링크

```bash
Select option: 6

# 결과:
📊 Relink Summary:
  ✅ Relinked: 145 clips
  ❌ Still offline: 5 clips
  
  Suuktest 폴더에서 자동으로 파일을 찾아 연결했습니다.
```

---

## 🌳 폴더 구조 예시

### Suuktest 폴더 구조:
```
/Users/Shared/suuktest/
├─ mac3/
│  ├─ CJU_SE/
│  │  ├─ A001_C001.mov
│  │  ├─ A001_C002.mov
│  │  ├─ audio.wav
│  │  ├─ edit_v1.xml
│  │  └─ edit_v2.xml
│  └─ PROJECT_2/
│     └─ ...
└─ mac4/
   └─ ...
```

### 임포트 후 미디어풀 구조:
```
Master/
├─ CJU_SE/
│  ├─ Video/ (150 clips)
│  ├─ Audio/ (200 clips)
│  └─ Image/ (5 clips)
└─ PROJECT_2/
   └─ ...

Timelines:
├─ edit_v1
├─ edit_v2
├─ rough_cut
└─ final
```

---

## 🤖 Claude 자동화 (MCP 통합)

### MCP 서버에 코드 추가

1. **MCP 서버 파일 열기**
```bash
code ~/path/to/davinci_mcp_server.py
```

2. **[mcp_suuktest_tools.py](computer:///mnt/user-data/outputs/mcp_suuktest_tools.py) 내용 복사**

3. **MCP 서버 재시작**

### Claude를 통한 사용

```
사용자: Suuktest 폴더 구조를 보여줘

Claude: [suuktest_scan_structure 실행]
        📂 Suuktest 폴더 구조:
        
        mac3/
          - CJU_SE/ (50.5 GB)
            video: 150 files
            audio: 200 files
            xml: 5 files
        
        mac4/
          - PROJECT_2/ (30.2 GB)
            ...
```

```
사용자: mac3/CJU_SE 폴더를 미디어풀에 임포트해줘

Claude: [suuktest_import_folder 실행]
        ✅ 355개 파일을 CJU_SE 빈으로 임포트했습니다:
        - Video: 150개
        - Audio: 200개
        - Timeline: 5개
```

```
사용자: 모든 XML을 타임라인으로 가져와줘

Claude: [suuktest_import_all_xmls 실행]
        ✅ 5개의 타임라인을 임포트했습니다:
        - edit_v1
        - edit_v2
        - rough_cut
        - fine_cut
        - final
```

```
사용자: 오프라인 클립들을 자동으로 릴링크해줘

Claude: [suuktest_relink_clips 실행]
        ✅ 200개 클립 중 10개가 오프라인이었고,
        8개를 성공적으로 릴링크했습니다.
```

---

## 📋 주요 기능

### 1. 폴더 스캔 및 분석
- Suuktest 전체 구조 자동 스캔
- 프로젝트별 파일 타입 및 용량 분석
- 비디오/오디오/XML 파일 자동 감지

### 2. 자동 임포트
- 폴더 전체를 미디어풀로 일괄 임포트
- 확장자별 자동 분류 (Mov, Wav, Xml 등)
- 프로젝트별 빈 자동 생성

### 3. XML 타임라인 임포트
- FCP XML, Premiere XML, AAF, EDL 지원
- 폴더의 모든 XML을 타임라인으로 자동 임포트
- 원본 설정 보존 (FPS, 해상도 등)

### 4. 클립 관리
- 오프라인 클립 자동 감지
- Suuktest 폴더에서 자동 릴링크
- 재귀적 검색으로 모든 서브폴더 탐색

### 5. 미디어풀 자동 정리
- 확장자별 빈 생성 (Mov/, Wav/, Xml/)
- 프로젝트별 구조 유지
- 중복 방지 및 기존 빈 재사용

---

## 🎯 실전 워크플로우

### 시나리오: 새 프로젝트 시작

```bash
# 1. Suuktest 폴더 구조 확인
Select option: 2
# → 사용 가능한 프로젝트 목록 확인

# 2. 프로젝트 폴더 임포트
Select option: 3
Enter subfolder: mac3/CJU_SE
Organize by extension? y
# → 모든 미디어 파일이 타입별로 정리되어 임포트됨

# 3. XML 타임라인 임포트
Select option: 4
Enter subfolder: mac3/CJU_SE
# → 편집 시퀀스가 타임라인으로 임포트됨

# 4. 오프라인 클립 릴링크 (필요시)
Select option: 6
# → 오프라인 클립이 자동으로 연결됨

# 5. 최종 구조 확인
Select option: 7
# → 미디어풀 구조 확인
```

### 결과:
```
🌳 Media Pool Structure:
====================================
📁 Master/ (0 clips)
  📁 CJU_SE/ (0 clips)
    📁 Video/ (150 clips)
    📁 Audio/ (200 clips)
    📁 Image/ (5 clips)
====================================

🎬 Timelines:
1. edit_v1 (FPS: 24, Tracks: 2)
2. edit_v2 (FPS: 24, Tracks: 2)
3. rough_cut (FPS: 24, Tracks: 3)
4. fine_cut (FPS: 24, Tracks: 2)
5. final (FPS: 24, Tracks: 2)
```

---

## 🔧 고급 기능

### 특정 파일 타입만 검색
```bash
Select option: 8
Enter subfolder: mac3
# → mac3 폴더의 모든 미디어 파일 검색

# 결과:
📊 Found media files:
  Video: 150 files
  Audio: 200 files
  Timeline: 5 files
  Total: 355 files
```

### 폴더 구조 상세 보기
```bash
Select option: 1
Show files? y

# 결과:
📁 mac3/
  📁 CJU_SE/
    🎥 A001_C001.mov (500.5 MB)
    🎥 A001_C002.mov (520.3 MB)
    🔊 audio_01.wav (50.2 MB)
    🎬 edit_v1.xml (0.5 MB)
    ...
```

---

## ⚡ 성능 팁

### 대용량 프로젝트 (1000+ 파일)
1. **분할 임포트**: 서브폴더별로 나눠서 임포트
2. **프록시 사용**: 고해상도 원본은 나중에 릴링크
3. **SSD 사용**: Suuktest 폴더를 SSD에 배치

### 네트워크 드라이브
- Suuktest를 로컬 SSD에 복사 후 작업
- 완료 후 네트워크로 백업

### XML 임포트 최적화
- 큰 XML은 DaVinci Resolve에서 직접 열기
- 작은 XML들은 배치 임포트

---

## 🔍 문제 해결

### Q: "Folder not found" 오류
**A:** Suuktest 폴더 경로 확인
```bash
ls -la /Users/Shared/suuktest
```

### Q: 파일이 오프라인 상태
**A:** 
1. 파일이 실제로 Suuktest 폴더에 있는지 확인
2. 권한 확인: `sudo chmod -R 755 /Users/Shared/suuktest`
3. Relink 기능 사용 (옵션 6)

### Q: XML 임포트가 안 됨
**A:**
1. XML 형식 확인 (FCP XML, Premiere XML 등)
2. DaVinci Resolve 버전 확인
3. XML 파일 직접 열어서 오류 확인

### Q: 미디어풀이 너무 복잡함
**A:**
1. 자동 정리 기능 사용 (옵션 5)
2. 불필요한 빈 삭제
3. 프로젝트별로 빈 분리

---

## 📚 추가 리소스

### 지원 파일 형식

**Video:**
- `.mov`, `.mp4`, `.mxf`, `.r3d`, `.braw`
- `.avi`, `.mkv`, `.dng`, `.dpx`, `.exr`

**Audio:**
- `.wav`, `.aif`, `.aiff`, `.mp3`, `.aac`
- `.m4a`, `.flac`

**Timeline:**
- `.xml` (FCP 7)
- `.fcpxml` (FCP X)
- `.aaf` (Avid)
- `.edl` (Legacy)

### 권장 폴더 구조
```
/Users/Shared/suuktest/
├─ [워크스테이션]/
│  └─ [프로젝트명]/
│     ├─ video/
│     ├─ audio/
│     ├─ xml/
│     └─ docs/
```

---

## 🎓 다음 단계

1. **독립 툴 테스트**: `suuktest_manager.py` 실행
2. **MCP 통합**: Claude 자동화 설정
3. **워크플로우 커스터마이징**: 필요에 맞게 수정

---

## 📞 요약

✅ **최상위 폴더**: `/Users/Shared/suuktest`
✅ **독립 툴**: `suuktest_manager.py`
✅ **MCP 통합**: `mcp_suuktest_tools.py`
✅ **자동 기능**: 임포트, 정리, 릴링크, XML 타임라인

모든 파일을 Suuktest 폴더에 두면 DaVinci Resolve가 자동으로 찾아서 관리합니다!
