# DaVinci Resolve Automation Tools

DaVinci Resolve를 위한 포괄적인 자동화 및 미디어 관리 도구 모음입니다.

## 🌟 주요 기능

### 1. Suuktest 폴더 통합 관리 시스템
- **최상위 폴더**: `/Users/Shared/suuktest` 기반 자동 파일 관리
- 프로젝트 폴더 자동 스캔 및 임포트
- XML/AAF/EDL 타임라인 자동 임포트
- 오프라인 클립 자동 릴링크
- 확장자별 미디어풀 자동 정리

### 2. XML 타임라인 임포트
- FCP XML, Premiere XML, AAF, EDL 지원
- 폴더 배치 임포트
- 타임라인 설정 자동 보존

### 3. 미디어풀 자동 정리
- 확장자별 자동 분류 (Mov, Wav, Xml 등)
- 프로젝트별 빈 구조 생성
- 중복 방지 및 최적화

## 📦 도구 목록

### 독립 실행형 툴

#### `suuktest_manager.py` ⭐ 추천
Suuktest 폴더(`/Users/Shared/suuktest`) 기반 통합 관리 시스템

**기능:**
- Suuktest 폴더 구조 스캔 및 분석
- 프로젝트 폴더 일괄 임포트 (video, audio, image)
- XML 타임라인 자동 임포트
- 오프라인 클립 자동 릴링크
- 미디어풀 확장자별 정리
- 대화형 메뉴 인터페이스

**사용법:**
```bash
python3 suuktest_manager.py
```

#### `resolve_manager.py`
범용 DaVinci Resolve 관리 도구

**기능:**
- XML/AAF/EDL 타임라인 임포트
- 빈의 클립으로 타임라인 생성
- 미디어풀 자동 정리
- 클립 릴링크

**사용법:**
```bash
python3 resolve_manager.py
```

#### `organize_by_extension.py`
미디어풀 확장자별 자동 정리 전용 스크립트

**사용법:**
```bash
python3 organize_by_extension.py
```

### MCP 서버 확장 코드

Claude AI를 통한 음성/텍스트 명령으로 DaVinci Resolve 제어

#### `mcp_suuktest_tools.py`
Suuktest 폴더 관리 MCP 툴

**제공 툴:**
- `suuktest_scan_structure`: 폴더 구조 스캔
- `suuktest_import_folder`: 폴더 임포트
- `suuktest_import_all_xmls`: XML 타임라인 임포트
- `suuktest_find_media_files`: 미디어 파일 검색
- `suuktest_relink_clips`: 오프라인 클립 릴링크
- `suuktest_list_projects`: 프로젝트 목록

#### `mcp_xml_import_tools.py`
XML 타임라인 임포트 및 미디어풀 관리 MCP 툴

**제공 툴:**
- `import_timeline_from_file`: XML 파일 임포트
- `import_all_xml_from_folder`: 폴더 배치 임포트
- `get_clips_in_bin`: 빈의 클립 정보
- `get_media_pool_structure`: 미디어풀 구조 조회
- `create_timeline_from_bin_clips`: 빈에서 타임라인 생성
- `relink_offline_clips`: 오프라인 클립 릴링크

## 🚀 빠른 시작

### 1. 시스템 요구사항
- macOS (Apple Silicon 또는 Intel)
- DaVinci Resolve 18 이상
- Python 3.8 이상

### 2. 설치
```bash
# 리포지토리 클론
git clone https://github.com/feeldizDI/res.git
cd res

# 실행 권한 부여
chmod +x suuktest_manager.py
chmod +x resolve_manager.py
chmod +x organize_by_extension.py
```

### 3. 사용 예시

#### Suuktest 폴더 관리
```bash
# 대화형 메뉴 실행
python3 suuktest_manager.py

# 메뉴에서 선택:
# 1. Suuktest 폴더 스캔
# 2. 프로젝트 목록 보기
# 3. 폴더 임포트 (예: mac3/CJU_SE)
# 4. XML 타임라인 임포트
# 5. 미디어풀 자동 정리
# 6. 오프라인 클립 릴링크
```

#### XML 타임라인 임포트
```bash
python3 resolve_manager.py

# 메뉴에서 선택:
# 1. XML 파일 하나 임포트
# 2. 폴더의 모든 XML 임포트
```

## 📂 폴더 구조

```
res/
├── README.md                      # 이 파일
├── suuktest_manager.py            # Suuktest 통합 관리 (추천)
├── resolve_manager.py             # 범용 Resolve 관리
├── organize_by_extension.py       # 미디어풀 정리 전용
├── mcp_suuktest_tools.py          # MCP 서버 확장 (Suuktest)
├── mcp_xml_import_tools.py        # MCP 서버 확장 (XML)
├── SUUKTEST_QUICKSTART.md         # Suuktest 퀵스타트 가이드
└── XML_IMPORT_GUIDE.md            # XML 임포트 가이드
```

## 📖 상세 가이드

### Suuktest 폴더 시스템
자세한 내용은 [SUUKTEST_QUICKSTART.md](SUUKTEST_QUICKSTART.md) 참조

**최상위 폴더**: `/Users/Shared/suuktest`

**권장 폴더 구조:**
```
/Users/Shared/suuktest/
├── mac3/
│   ├── CJU_SE/
│   │   ├── video/
│   │   ├── audio/
│   │   └── xml/
│   └── PROJECT_2/
└── mac4/
    └── ...
```

### XML 타임라인 임포트
자세한 내용은 [XML_IMPORT_GUIDE.md](XML_IMPORT_GUIDE.md) 참조

**지원 형식:**
- `.xml` - Final Cut Pro 7 XML
- `.fcpxml` - Final Cut Pro X XML
- `.aaf` - Avid AAF
- `.edl` - Edit Decision List

## 🤖 MCP 서버 통합 (선택사항)

Claude AI를 통해 DaVinci Resolve를 음성/텍스트 명령으로 제어할 수 있습니다.

### MCP 서버에 코드 추가

1. MCP 서버 파일 열기
```bash
code ~/path/to/davinci_mcp_server.py
```

2. `mcp_suuktest_tools.py` 또는 `mcp_xml_import_tools.py` 내용 복사

3. MCP 서버 재시작

### 사용 예시
```
사용자: mac3/CJU_SE 폴더를 미디어풀에 임포트해줘
Claude: [suuktest_import_folder 실행]
        ✅ 355개 파일을 임포트했습니다

사용자: 모든 XML을 타임라인으로 가져와줘
Claude: [suuktest_import_all_xmls 실행]
        ✅ 5개의 타임라인을 임포트했습니다
```

## 💡 실전 워크플로우

### 시나리오: 새 프로젝트 시작

```bash
# 1. Suuktest 매니저 실행
python3 suuktest_manager.py

# 2. 프로젝트 목록 확인
Select option: 2

# 3. 프로젝트 폴더 임포트
Select option: 3
Enter subfolder: mac3/CJU_SE
Organize by extension? y
# → Video, Audio, Image가 자동으로 빈에 정리됨

# 4. XML 타임라인 임포트
Select option: 4
Enter subfolder: mac3/CJU_SE
# → 편집 시퀀스가 타임라인으로 임포트됨

# 5. 오프라인 클립 릴링크 (필요시)
Select option: 6
# → 자동으로 파일 경로 연결

# 6. 완료!
```

**결과:**
```
🌳 Media Pool:
  📁 CJU_SE/
    ├─ Video/ (150 clips)
    ├─ Audio/ (200 clips)
    └─ Image/ (5 clips)

🎬 Timelines:
  - edit_v1
  - edit_v2
  - final
```

## 🔧 문제 해결

### Q: "Could not connect to DaVinci Resolve" 오류
**A:** DaVinci Resolve가 실행 중인지 확인

### Q: "Folder not found" 오류
**A:** Suuktest 폴더 경로 확인
```bash
ls -la /Users/Shared/suuktest
```

### Q: 파일이 오프라인 상태
**A:** 
1. 파일이 실제로 존재하는지 확인
2. 권한 확인: `sudo chmod -R 755 /Users/Shared/suuktest`
3. Relink 기능 사용

### Q: XML 임포트가 안 됨
**A:**
1. XML 형식 확인 (FCP XML, Premiere XML 등)
2. DaVinci Resolve 버전 확인
3. XML 파일 직접 열어서 오류 확인

## 🎯 지원 파일 형식

### Video
`.mov`, `.mp4`, `.mxf`, `.r3d`, `.braw`, `.avi`, `.mkv`, `.dng`, `.dpx`, `.exr`

### Audio
`.wav`, `.aif`, `.aiff`, `.mp3`, `.aac`, `.m4a`, `.flac`

### Timeline
`.xml`, `.fcpxml`, `.aaf`, `.edl`

### Image
`.jpg`, `.jpeg`, `.png`, `.tif`, `.tiff`, `.psd`, `.exr`

## 🏢 회사 정보

**Feeldiz DI Studio**
- 위치: Seoul, South Korea
- 전문 분야: Digital Intermediate, Color Grading, DCP Mastering
- 웹사이트: [feeldiz.com](https://feeldiz.com)

## 📄 라이센스

이 프로젝트는 Feeldiz DI Studio의 내부 도구입니다.

## 🤝 기여

내부 도구이므로 외부 기여는 받지 않습니다.

## 📞 지원

문제가 발생하면 Feeldiz DI Studio 기술팀에 문의하세요.

---

**Made with ❤️ by Feeldiz DI Studio**
