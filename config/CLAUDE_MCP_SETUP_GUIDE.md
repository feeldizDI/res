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
```json
{
  "mcpServers": {
    "davinci-resolve": {
      "name": "DaVinci Resolve MCP",
      "command": "/home/user/res/venv/bin/python",
      "args": ["/home/user/res/resolve_mcp_server.py"],
      "env": {
        "RESOLVE_SCRIPT_API": "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting",
        "RESOLVE_SCRIPT_LIB": "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so",
        "PYTHONPATH": "$PYTHONPATH:/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/"
      }
    }
  }
}
```

**중요:** `/home/user/res` 경로를 실제 프로젝트가 설치된 경로로 변경하세요!

예시:
```json
{
  "mcpServers": {
    "davinci-resolve": {
      "name": "DaVinci Resolve MCP",
      "command": "/Users/yourname/davinci-resolve-mcp/venv/bin/python",
      "args": ["/Users/yourname/davinci-resolve-mcp/resolve_mcp_server.py"],
      "env": {
        "RESOLVE_SCRIPT_API": "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting",
        "RESOLVE_SCRIPT_LIB": "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so",
        "PYTHONPATH": "$PYTHONPATH:/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/"
      }
    }
  }
}
```

#### Windows 사용자

1. `%APPDATA%\Claude` 디렉토리를 생성합니다 (없는 경우)

2. 다음 내용으로 `claude_desktop_config.json` 파일을 생성합니다:
```json
{
  "mcpServers": {
    "davinci-resolve": {
      "name": "DaVinci Resolve MCP",
      "command": "C:/path/to/your/davinci-resolve-mcp/venv/Scripts/python.exe",
      "args": ["C:/path/to/your/davinci-resolve-mcp/resolve_mcp_server.py"],
      "env": {
        "RESOLVE_SCRIPT_API": "C:/ProgramData/Blackmagic Design/DaVinci Resolve/Support/Developer/Scripting",
        "RESOLVE_SCRIPT_LIB": "C:/Program Files/Blackmagic Design/DaVinci Resolve/fusionscript.dll",
        "PYTHONPATH": "C:/ProgramData/Blackmagic Design/DaVinci Resolve/Support/Developer/Scripting/Modules"
      }
    }
  }
}
```

**중요:**
- Windows 경로는 슬래시(/)를 사용하세요
- 실제 프로젝트가 설치된 경로로 변경하세요
- DaVinci Resolve 설치 경로가 다른 경우 해당 경로도 수정하세요

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

### 연결 실패

1. **DaVinci Resolve 실행 확인**: Resolve가 실행 중인지 확인
2. **경로 확인**: 설정 파일의 모든 경로가 정확한지 확인
3. **환경 변수 확인**: DaVinci Resolve 설치 경로가 설정과 일치하는지 확인
4. **Python 가상환경 확인**: venv가 올바르게 생성되었는지 확인

### 로그 확인

문제가 발생한 경우 다음 위치에서 로그를 확인할 수 있습니다:
```
/home/user/res/logs/
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
