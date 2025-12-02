# Claude Desktop MCP 연결 가이드

이 가이드는 현재 프로젝트를 Claude Desktop과 연결하는 방법을 설명합니다.

## 시스템 요구사항

- **macOS** 또는 **Windows** (Linux는 Claude Desktop을 지원하지 않음)
- DaVinci Resolve Studio 설치 및 실행 중이어야 함
- Python 3.6 이상
- Claude Desktop 앱 설치

## 설정 방법

### 1. Claude Desktop 설정 파일 위치

운영체제에 따라 설정 파일 위치가 다릅니다:

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

### 2. 설정 파일 생성/수정

#### macOS 사용자

1. 터미널을 열고 다음 명령어를 실행하여 설정 디렉토리를 생성합니다:
```bash
mkdir -p ~/Library/Application\ Support/Claude
```

2. 다음 내용으로 `claude_desktop_config.json` 파일을 생성합니다:

**중요:**
- `${PROJECT_PATH}`를 실제 프로젝트가 설치된 경로로 변경하세요
- `cwd` (current working directory) 설정이 **반드시 필요**합니다
- `PYTHONPATH`에 프로젝트 루트 경로를 포함해야 합니다

**예시 (실제 경로로 변경하세요):**

```json
{
  "mcpServers": {
    "davinci-resolve": {
      "name": "DaVinci Resolve MCP",
      "command": "/Users/feeldiz_01/davinci-resolve-mcp/venv/bin/python",
      "args": ["/Users/feeldiz_01/davinci-resolve-mcp/resolve_mcp_server.py"],
      "cwd": "/Users/feeldiz_01/davinci-resolve-mcp",
      "env": {
        "RESOLVE_SCRIPT_API": "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting",
        "RESOLVE_SCRIPT_LIB": "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so",
        "PYTHONPATH": "/Users/feeldiz_01/davinci-resolve-mcp:/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/"
      }
    }
  }
}
```

**설정 항목 설명:**
- `command`: 가상환경의 Python 실행 파일 경로
- `args`: MCP 서버 스크립트 경로
- `cwd`: 프로젝트 루트 디렉토리 (이것이 없으면 `ModuleNotFoundError` 발생!)
- `PYTHONPATH`: 프로젝트 루트와 DaVinci Resolve 모듈 경로를 콜론(:)으로 구분

#### Windows 사용자

1. `%APPDATA%\Claude` 디렉토리를 생성합니다 (없는 경우)

2. 다음 내용으로 `claude_desktop_config.json` 파일을 생성합니다:

**중요:**
- Windows에서도 경로는 슬래시(/)를 사용하세요 (역슬래시 아님!)
- `cwd` (current working directory) 설정이 **반드시 필요**합니다
- `PYTHONPATH`에 프로젝트 루트 경로를 포함해야 합니다
- 실제 프로젝트가 설치된 경로로 변경하세요

**예시:**

```json
{
  "mcpServers": {
    "davinci-resolve": {
      "name": "DaVinci Resolve MCP",
      "command": "C:/Users/YourName/davinci-resolve-mcp/venv/Scripts/python.exe",
      "args": ["C:/Users/YourName/davinci-resolve-mcp/resolve_mcp_server.py"],
      "cwd": "C:/Users/YourName/davinci-resolve-mcp",
      "env": {
        "RESOLVE_SCRIPT_API": "C:/ProgramData/Blackmagic Design/DaVinci Resolve/Support/Developer/Scripting",
        "RESOLVE_SCRIPT_LIB": "C:/Program Files/Blackmagic Design/DaVinci Resolve/fusionscript.dll",
        "PYTHONPATH": "C:/Users/YourName/davinci-resolve-mcp;C:/ProgramData/Blackmagic Design/DaVinci Resolve/Support/Developer/Scripting/Modules"
      }
    }
  }
}
```

**설정 항목 설명:**
- `command`: 가상환경의 Python 실행 파일 경로 (`python.exe`)
- `args`: MCP 서버 스크립트 경로
- `cwd`: 프로젝트 루트 디렉토리 (이것이 없으면 `ModuleNotFoundError` 발생!)
- `PYTHONPATH`: Windows에서는 세미콜론(;)으로 경로 구분

### 3. DaVinci Resolve 실행

MCP 서버를 시작하기 전에 **반드시** DaVinci Resolve가 실행 중이어야 합니다.

### 4. Claude Desktop 재시작

설정 파일을 저장한 후 Claude Desktop을 완전히 종료하고 다시 시작하세요.

### 5. 연결 확인

Claude Desktop에서 다음과 같이 테스트해보세요:

```
"What version of DaVinci Resolve is running?"
"List all projects in DaVinci Resolve"
```

## 문제 해결

### 일반적인 오류와 해결 방법

#### 1. `ModuleNotFoundError: No module named 'src'`

**원인:** `cwd` (현재 작업 디렉토리) 설정이 누락되었거나 PYTHONPATH가 잘못 설정됨

**해결:**
- Claude Desktop 설정 파일에 `"cwd": "/Users/yourname/davinci-resolve-mcp"` 추가
- `PYTHONPATH`에 프로젝트 루트 경로 포함
- macOS: 경로 구분자로 콜론(`:`) 사용
- Windows: 경로 구분자로 세미콜론(`;`) 사용

#### 2. `spawn python ENOENT`

**원인:** Python 실행 파일을 찾을 수 없음

**해결:**
- `command` 경로가 정확한지 확인
- 가상환경이 제대로 생성되었는지 확인:
  ```bash
  # macOS
  ls -la /Users/yourname/davinci-resolve-mcp/venv/bin/python

  # Windows
  dir C:\Users\YourName\davinci-resolve-mcp\venv\Scripts\python.exe
  ```

#### 3. `Server transport closed unexpectedly`

**원인:** 서버가 조기에 종료됨 (보통 위의 오류들 때문)

**해결:** Claude Desktop 로그를 확인하여 실제 오류 메시지 파악

### 연결 실패

1. **DaVinci Resolve 실행 확인**: Resolve가 실행 중인지 확인
2. **경로 확인**: 설정 파일의 모든 경로가 정확한지 확인
3. **환경 변수 확인**: DaVinci Resolve 설치 경로가 설정과 일치하는지 확인
4. **Python 가상환경 확인**: venv가 올바르게 생성되었는지 확인

### Claude Desktop 로그 확인

macOS에서 Claude Desktop 로그 확인:
```bash
# Claude Desktop 개발자 도구 열기 (보통 Cmd+Shift+I)
# 또는 터미널에서:
tail -f ~/Library/Logs/Claude/mcp*.log
```

Windows에서 로그 확인:
```
%LOCALAPPDATA%\Claude\logs\
```

### 올바른 설정 예시 확인

**macOS (사용자의 실제 경로 기준):**
```json
{
  "mcpServers": {
    "davinci-resolve": {
      "name": "DaVinci Resolve MCP",
      "command": "/Users/feeldiz_01/davinci-resolve-mcp/venv/bin/python",
      "args": ["/Users/feeldiz_01/davinci-resolve-mcp/resolve_mcp_server.py"],
      "cwd": "/Users/feeldiz_01/davinci-resolve-mcp",
      "env": {
        "RESOLVE_SCRIPT_API": "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting",
        "RESOLVE_SCRIPT_LIB": "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so",
        "PYTHONPATH": "/Users/feeldiz_01/davinci-resolve-mcp:/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/"
      }
    }
  }
}
```

### 추가 도움말

더 자세한 정보는 프로젝트의 README.md와 INSTALL.md를 참조하세요.

## 사용 예시

Claude Desktop과 연결된 후 다음과 같은 작업을 할 수 있습니다:

### 프로젝트 관리
- "현재 프로젝트 이름을 알려줘"
- "새 프로젝트를 만들어줘"
- "프로젝트 목록을 보여줘"

### 타임라인 작업
- "현재 타임라인 정보를 보여줘"
- "새 타임라인을 만들어줘"
- "타임라인에 마커를 추가해줘"

### 미디어 풀 작업
- "미디어 풀의 클립 목록을 보여줘"
- "새 미디어 빈을 만들어줘"

### 일반
- "DaVinci Resolve 버전을 알려줘"
- "현재 페이지(Edit, Color 등)를 알려줘"
