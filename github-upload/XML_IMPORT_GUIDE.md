# DaVinci Resolve XML 임포트 및 파일 관리 가이드

## 📦 제공된 파일들

### 1. `resolve_manager.py` - 독립 실행형 관리 툴
Mac Studio에서 바로 실행 가능한 대화형 관리 프로그램

### 2. `mcp_xml_import_tools.py` - MCP 서버 확장 코드
MCP 서버에 추가하여 Claude가 자동으로 사용할 수 있는 툴

---

## 🚀 방법 1: 독립 실행형 툴 사용 (추천)

### 실행 방법
```bash
# 터미널에서
python3 ~/Downloads/resolve_manager.py
```

### 메뉴
```
1. Import XML/AAF/EDL to Timeline      # XML 파일 하나 임포트
2. Import all XMLs from folder         # 폴더 전체 XML 임포트
3. List all timelines                  # 타임라인 목록 보기
4. Organize media pool by extension    # 확장자별 정리
5. Create timeline from bin            # 빈의 클립으로 타임라인 생성
6. Relink clips to folder              # 오프라인 클립 릴링크
7. Show media pool structure           # 미디어풀 구조 보기
8. Exit                                # 종료
```

### 사용 예시

#### XML 파일 하나 임포트
```
Select option: 1
Enter XML file path: /Users/Shared/suuktest/mac3/CJU_SE/edit.xml
Enter timeline name: Main Edit

✅ Successfully imported timeline: Main Edit
   Frame Rate: 24
   Resolution: 1920x1080
```

#### 폴더의 모든 XML 임포트
```
Select option: 2
Enter folder path: /Users/Shared/suuktest/mac3/CJU_SE

📂 Scanning folder: /Users/Shared/suuktest/mac3/CJU_SE
   Found 5 XML files
   
📥 Importing timeline from: edit_v1.xml
✅ Successfully imported timeline: edit_v1
📥 Importing timeline from: edit_v2.xml
✅ Successfully imported timeline: edit_v2
...

✅ Imported 5/5 timelines
```

#### 빈의 클립으로 타임라인 생성
```
Select option: 5
Enter bin name: Mov
Enter timeline name: All Footage

🎬 Creating timeline from bin: Mov
   Found 150 clips
✅ Created timeline: All Footage
```

#### 오프라인 클립 릴링크
```
Select option: 6
Enter media folder path: /Users/Shared/suuktest/mac3/CJU_SE

🔗 Relinking clips to: /Users/Shared/suuktest/mac3/CJU_SE
   Found 200 clips in media pool
   Found 10 offline clips
✅ Successfully relinked clips
```

---

## 🤖 방법 2: MCP 서버 통합 (고급)

### MCP 서버에 코드 추가

1. **MCP 서버 파일 열기**
```bash
code ~/path/to/davinci_mcp_server.py
```

2. **`mcp_xml_import_tools.py` 내용 복사**
   - 전체 코드를 MCP 서버 파일에 추가

3. **MCP 서버 재시작**
```bash
# MCP 서버 종료 후 재시작
```

### Claude를 통한 사용

MCP 서버에 툴을 추가하면 Claude가 자동으로 사용할 수 있습니다:

```
사용자: /Users/Shared/suuktest/mac3/CJU_SE 폴더의 모든 XML을 타임라인으로 임포트해줘

Claude: [import_all_xml_from_folder 툴 실행]
        ✅ 5개의 XML 파일을 타임라인으로 임포트했습니다:
        - edit_v1
        - edit_v2
        - rough_cut
        - fine_cut
        - final
```

```
사용자: Mov 빈의 모든 클립으로 타임라인 만들어줘

Claude: [create_timeline_from_bin_clips 툴 실행]
        ✅ "Mov_Timeline" 타임라인을 생성했습니다 (150개 클립)
```

```
사용자: 오프라인 클립들을 /Users/Shared/media 폴더에서 찾아서 릴링크해줘

Claude: [relink_offline_clips 툴 실행]
        ✅ 200개 클립 중 10개가 오프라인이었고, 8개를 성공적으로 릴링크했습니다.
```

---

## 📋 주요 기능 상세

### 1. XML/AAF/EDL 임포트

**지원 포맷:**
- `.xml` - Final Cut Pro XML
- `.fcpxml` - Final Cut Pro X XML
- `.aaf` - Avid AAF
- `.edl` - Edit Decision List

**특징:**
- 자동으로 타임라인 생성
- 원본 프레임레이트, 해상도 유지
- 클립 메타데이터 보존

### 2. 미디어풀 자동 정리

**정리 방식:**
- 확장자별 자동 분류
- 폴더명: 첫 글자만 대문자 (Mov, Xml, Wav 등)
- 기존 폴더 재사용

**예시 구조:**
```
Master/
├─ Mov/        (150 clips)
├─ Mp4/        (30 clips)
├─ Wav/        (200 clips)
├─ Xml/        (5 clips)
└─ Aif/        (50 clips)
```

### 3. 타임라인 생성

**방법:**
- 빈의 모든 클립 사용
- 파일명 순서대로 배치
- 자동 트랙 할당

### 4. 클립 릴링크

**기능:**
- 오프라인 클립 자동 감지
- 폴더에서 일치하는 파일 검색
- 재귀적 검색 지원

---

## 💡 실전 워크플로우 예시

### 시나리오: XML 프로젝트 임포트 및 정리

```bash
# 1. resolve_manager.py 실행
python3 resolve_manager.py

# 2. XML 폴더 전체 임포트
Select option: 2
Enter folder path: /Users/Shared/suuktest/mac3/CJU_SE
# → 모든 XML이 타임라인으로 임포트됨

# 3. 미디어풀 정리
Select option: 4
Enter source bin name: Master
# → Mov, Wav, Xml 등으로 자동 분류

# 4. 오프라인 클립 릴링크
Select option: 6
Enter media folder path: /Users/Shared/suuktest/mac3/CJU_SE
# → 오프라인 클립 자동 릴링크

# 5. 미디어풀 구조 확인
Select option: 7
# → 최종 구조 확인
```

### 결과:
```
🌳 Media Pool Structure:
============================================================
📁 Master/ (0 clips)
  📁 Mov/ (150 clips)
  📁 Wav/ (200 clips)
  📁 Xml/ (5 clips)
  📁 Mp4/ (30 clips)
============================================================

Timelines:
1. edit_v1 (FPS: 24, Video Tracks: 2)
2. edit_v2 (FPS: 24, Video Tracks: 2)
3. rough_cut (FPS: 24, Video Tracks: 3)
4. fine_cut (FPS: 24, Video Tracks: 2)
5. final (FPS: 24, Video Tracks: 2)
```

---

## 🔧 문제 해결

### Q: "Could not connect to DaVinci Resolve" 오류
**A:** DaVinci Resolve가 실행 중인지 확인하세요.

### Q: XML 임포트 시 클립이 오프라인 상태
**A:** 
1. 미디어 파일 경로가 올바른지 확인
2. `relink_clips_to_folder` 기능으로 릴링크
3. 미디어 파일이 실제로 존재하는지 확인

### Q: 타임라인이 생성되지 않음
**A:**
1. 빈에 클립이 있는지 확인
2. 클립이 올바른 미디어 형식인지 확인
3. DaVinci Resolve 로그 확인

### Q: MCP 툴이 작동하지 않음
**A:**
1. MCP 서버가 재시작되었는지 확인
2. 코드가 올바르게 추가되었는지 확인
3. Claude가 MCP 서버에 연결되어 있는지 확인

---

## 📚 추가 참고사항

### 지원되는 XML 형식
- **Final Cut Pro 7 XML**: 가장 범용적
- **Final Cut Pro X XML**: 최신 FCP 프로젝트
- **Premiere Pro XML**: Adobe Premiere 교환
- **AAF**: Avid 표준 포맷
- **EDL**: 레거시 편집 리스트

### 타임라인 설정
임포트된 타임라인은 XML 파일의 설정을 따릅니다:
- 프레임레이트
- 해상도
- 타임코드 시작점
- 오디오 샘플레이트

### 성능 최적화
- 대용량 XML (1000+ 클립): 분할 임포트 권장
- 프록시 미디어 사용 권장
- SSD에 미디어 파일 배치

---

## 🎯 다음 단계

1. **독립 툴 사용**: `resolve_manager.py` 실행하여 XML 임포트 테스트
2. **MCP 통합**: 코드를 MCP 서버에 추가하여 Claude 자동화
3. **워크플로우 커스터마이징**: 필요에 맞게 스크립트 수정

---

## 📞 지원

문제가 발생하면:
1. DaVinci Resolve 로그 확인
2. Python 오류 메시지 확인
3. 스크립트 실행 로그 확인
