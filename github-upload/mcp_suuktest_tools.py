"""
DaVinci Resolve MCP 서버 - Suuktest 폴더 관리 툴
이 코드를 davinci_mcp_server.py에 추가하세요

최상위 폴더: /Users/Shared/suuktest
"""

from pathlib import Path
from collections import defaultdict
import os

# ============================================
# 설정
# ============================================
SUUKTEST_ROOT = "/Users/Shared/suuktest"

# 지원 파일 형식
MEDIA_EXTENSIONS = {
    'video': ['.mov', '.mp4', '.mxf', '.r3d', '.braw', '.avi', '.mkv', '.dng', '.dpx', '.exr'],
    'audio': ['.wav', '.aif', '.aiff', '.mp3', '.aac', '.m4a', '.flac'],
    'image': ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.psd', '.exr'],
    'timeline': ['.xml', '.fcpxml', '.aaf', '.edl'],
}


# ============================================
# Suuktest 폴더 관리 툴
# ============================================

@server.call_tool()
async def suuktest_scan_structure(
    show_details: bool = False
) -> dict:
    """
    Suuktest 폴더 구조 스캔
    
    Args:
        show_details: 상세 정보 표시 여부
    
    Returns:
        {
            "root": "/Users/Shared/suuktest",
            "structure": {
                "mac3": {
                    "CJU_SE": {
                        "video": 150,
                        "audio": 200,
                        "xml": 5
                    }
                }
            },
            "total_size_gb": 500.5
        }
    """
    root_path = Path(SUUKTEST_ROOT)
    
    if not root_path.exists():
        return {"error": f"Suuktest folder not found: {SUUKTEST_ROOT}"}
    
    structure = {}
    total_size = 0
    
    # 1단계 폴더 (예: mac3)
    for level1 in sorted(root_path.iterdir()):
        if not level1.is_dir() or level1.name.startswith('.'):
            continue
        
        structure[level1.name] = {}
        
        # 2단계 폴더 (예: CJU_SE)
        for level2 in sorted(level1.iterdir()):
            if not level2.is_dir() or level2.name.startswith('.'):
                continue
            
            # 파일 타입별 카운트
            file_counts = defaultdict(int)
            folder_size = 0
            
            for file in level2.rglob("*"):
                if file.is_file():
                    ext = file.suffix.lower()
                    file_type = _get_file_type(ext)
                    file_counts[file_type] += 1
                    folder_size += file.stat().st_size
            
            total_size += folder_size
            
            structure[level1.name][level2.name] = {
                "files": dict(file_counts),
                "size_gb": folder_size / (1024**3)
            }
    
    return {
        "root": SUUKTEST_ROOT,
        "structure": structure,
        "total_size_gb": total_size / (1024**3)
    }


@server.call_tool()
async def suuktest_import_folder(
    subfolder_path: str,
    organize_by_extension: bool = True,
    import_timelines: bool = True
) -> dict:
    """
    Suuktest의 특정 서브폴더를 미디어풀에 임포트
    
    Args:
        subfolder_path: 서브폴더 경로 (예: "mac3/CJU_SE")
        organize_by_extension: 확장자별로 정리할지 여부
        import_timelines: XML 파일을 타임라인으로 임포트할지 여부
    
    Returns:
        {
            "success": True,
            "imported": {
                "video": 150,
                "audio": 200,
                "timelines": 5
            },
            "bin_name": "CJU_SE"
        }
    """
    resolve = get_resolve()
    project = resolve.GetProjectManager().GetCurrentProject()
    media_pool = project.GetMediaPool()
    media_storage = resolve.GetMediaStorage()
    root_folder = media_pool.GetRootFolder()
    
    # 경로 확인
    source_path = Path(SUUKTEST_ROOT) / subfolder_path
    
    if not source_path.exists():
        return {"error": f"Folder not found: {source_path}"}
    
    # 프로젝트 빈 생성
    project_bin_name = Path(subfolder_path).name
    project_bin = _get_or_create_bin(media_pool, root_folder, project_bin_name)
    
    # 미디어 파일 찾기
    media_files = defaultdict(list)
    
    for category, extensions in MEDIA_EXTENSIONS.items():
        for ext in extensions:
            files = list(source_path.glob(f"**/*{ext}"))
            media_files[category].extend([str(f) for f in files])
    
    # 임포트 결과
    imported_counts = defaultdict(int)
    
    # 타임라인 임포트
    if import_timelines and media_files['timeline']:
        for xml_file in media_files['timeline']:
            try:
                timeline = media_pool.ImportTimelineFromFile(xml_file)
                if timeline:
                    imported_counts['timelines'] += 1
            except:
                pass
    
    # 미디어 파일 임포트
    for category in ['video', 'audio', 'image']:
        if not media_files[category]:
            continue
        
        if organize_by_extension:
            # 확장자별 빈 생성
            category_bin = _get_or_create_bin(
                media_pool, 
                project_bin, 
                category.capitalize()
            )
            media_pool.SetCurrentFolder(category_bin)
        else:
            media_pool.SetCurrentFolder(project_bin)
        
        # 임포트
        clips = media_storage.AddItemListToMediaPool(media_files[category])
        
        if clips:
            count = len(clips) if isinstance(clips, list) else 1
            imported_counts[category] = count
    
    return {
        "success": True,
        "imported": dict(imported_counts),
        "bin_name": project_bin_name,
        "source_path": str(source_path)
    }


@server.call_tool()
async def suuktest_import_all_xmls(
    subfolder_path: str
) -> dict:
    """
    Suuktest의 특정 서브폴더에 있는 모든 XML을 타임라인으로 임포트
    
    Args:
        subfolder_path: 서브폴더 경로 (예: "mac3/CJU_SE")
    
    Returns:
        {
            "success": True,
            "imported_timelines": ["edit_v1", "edit_v2", "final"],
            "failed": ["corrupted.xml"]
        }
    """
    resolve = get_resolve()
    project = resolve.GetProjectManager().GetCurrentProject()
    media_pool = project.GetMediaPool()
    
    # 경로 확인
    source_path = Path(SUUKTEST_ROOT) / subfolder_path
    
    if not source_path.exists():
        return {"error": f"Folder not found: {source_path}"}
    
    # XML 파일 찾기
    xml_files = []
    for ext in MEDIA_EXTENSIONS['timeline']:
        xml_files.extend(source_path.glob(f"**/*{ext}"))
    
    if not xml_files:
        return {
            "success": True,
            "imported_timelines": [],
            "message": "No XML files found"
        }
    
    # 각 XML 임포트
    imported_timelines = []
    failed = []
    
    for xml_file in xml_files:
        try:
            timeline = media_pool.ImportTimelineFromFile(str(xml_file))
            if timeline:
                imported_timelines.append(timeline.GetName())
            else:
                failed.append(xml_file.name)
        except Exception as e:
            failed.append(f"{xml_file.name}: {str(e)}")
    
    return {
        "success": True,
        "imported_timelines": imported_timelines,
        "failed": failed if failed else None,
        "total_found": len(xml_files)
    }


@server.call_tool()
async def suuktest_find_media_files(
    subfolder_path: Optional[str] = None,
    file_type: Optional[str] = None
) -> dict:
    """
    Suuktest 폴더에서 미디어 파일 검색
    
    Args:
        subfolder_path: 특정 서브폴더만 검색 (None이면 전체)
        file_type: 파일 타입 필터 (video, audio, image, timeline)
    
    Returns:
        {
            "search_path": "/Users/Shared/suuktest/mac3",
            "results": {
                "video": [
                    {
                        "name": "A001_C001.mov",
                        "path": "/Users/Shared/suuktest/mac3/...",
                        "size_mb": 500.5
                    }
                ]
            }
        }
    """
    root_path = Path(SUUKTEST_ROOT)
    search_path = root_path / subfolder_path if subfolder_path else root_path
    
    if not search_path.exists():
        return {"error": f"Folder not found: {search_path}"}
    
    # 파일 타입 필터
    if file_type:
        if file_type not in MEDIA_EXTENSIONS:
            return {"error": f"Invalid file type: {file_type}"}
        categories = {file_type: MEDIA_EXTENSIONS[file_type]}
    else:
        categories = MEDIA_EXTENSIONS
    
    # 파일 검색
    results = defaultdict(list)
    
    for category, extensions in categories.items():
        for ext in extensions:
            files = search_path.glob(f"**/*{ext}")
            
            for file in files:
                results[category].append({
                    "name": file.name,
                    "path": str(file),
                    "size_mb": file.stat().st_size / (1024 * 1024),
                    "parent": file.parent.name
                })
    
    return {
        "search_path": str(search_path),
        "results": dict(results),
        "total_files": sum(len(files) for files in results.values())
    }


@server.call_tool()
async def suuktest_relink_clips(
    subfolder_path: Optional[str] = None
) -> dict:
    """
    오프라인 클립을 Suuktest 폴더에서 자동 릴링크
    
    Args:
        subfolder_path: 특정 서브폴더에서만 검색 (None이면 전체)
    
    Returns:
        {
            "success": True,
            "total_clips": 200,
            "offline_clips": 10,
            "relinked": 8,
            "still_offline": 2
        }
    """
    resolve = get_resolve()
    project = resolve.GetProjectManager().GetCurrentProject()
    media_pool = project.GetMediaPool()
    root_folder = media_pool.GetRootFolder()
    
    # 릴링크 경로
    if subfolder_path:
        relink_path = str(Path(SUUKTEST_ROOT) / subfolder_path)
        if not os.path.exists(relink_path):
            return {"error": f"Folder not found: {relink_path}"}
    else:
        relink_path = SUUKTEST_ROOT
    
    # 모든 클립 수집
    all_clips = _get_all_clips_recursive(root_folder)
    
    # 오프라인 클립 찾기
    offline_clips = []
    
    for clip in all_clips:
        file_path = clip.GetClipProperty("File Path")
        if not file_path or not os.path.exists(file_path):
            offline_clips.append(clip)
    
    if not offline_clips:
        return {
            "success": True,
            "total_clips": len(all_clips),
            "offline_clips": 0,
            "message": "All clips are online"
        }
    
    # 릴링크 시도
    result = media_pool.RelinkClips(offline_clips, relink_path)
    
    # 결과 확인
    still_offline = 0
    for clip in offline_clips:
        file_path = clip.GetClipProperty("File Path")
        if not file_path or not os.path.exists(file_path):
            still_offline += 1
    
    relinked = len(offline_clips) - still_offline
    
    return {
        "success": True,
        "total_clips": len(all_clips),
        "offline_clips": len(offline_clips),
        "relinked": relinked,
        "still_offline": still_offline,
        "relink_path": relink_path
    }


@server.call_tool()
async def suuktest_list_projects() -> dict:
    """
    Suuktest 폴더의 프로젝트 목록
    
    Returns:
        {
            "projects": [
                {
                    "path": "mac3/CJU_SE",
                    "files": {
                        "video": 150,
                        "audio": 200
                    },
                    "size_gb": 50.5
                }
            ]
        }
    """
    root_path = Path(SUUKTEST_ROOT)
    
    if not root_path.exists():
        return {"error": f"Suuktest folder not found: {SUUKTEST_ROOT}"}
    
    projects = []
    
    # 1단계 폴더
    for level1 in sorted(root_path.iterdir()):
        if not level1.is_dir() or level1.name.startswith('.'):
            continue
        
        # 2단계 폴더
        for level2 in sorted(level1.iterdir()):
            if not level2.is_dir() or level2.name.startswith('.'):
                continue
            
            # 파일 분석
            file_counts = defaultdict(int)
            total_size = 0
            
            for file in level2.rglob("*"):
                if file.is_file():
                    ext = file.suffix.lower()
                    file_type = _get_file_type(ext)
                    file_counts[file_type] += 1
                    total_size += file.stat().st_size
            
            project_path = f"{level1.name}/{level2.name}"
            
            projects.append({
                "path": project_path,
                "files": dict(file_counts),
                "size_gb": total_size / (1024**3),
                "has_timelines": file_counts['timeline'] > 0
            })
    
    return {
        "root": SUUKTEST_ROOT,
        "projects": projects,
        "total_projects": len(projects)
    }


# ============================================
# Helper Functions
# ============================================

def _get_file_type(ext):
    """파일 확장자로 타입 결정"""
    ext = ext.lower()
    for category, extensions in MEDIA_EXTENSIONS.items():
        if ext in extensions:
            return category
    return 'other'


def _get_or_create_bin(media_pool, parent_folder, bin_name):
    """빈을 찾거나 생성"""
    # 기존 빈 찾기
    for subfolder in parent_folder.GetSubFolderList():
        if subfolder.GetName() == bin_name:
            return subfolder
    
    # 빈 생성
    new_bin = media_pool.AddSubFolder(parent_folder, bin_name)
    return new_bin


def _get_all_clips_recursive(folder):
    """모든 클립을 재귀적으로 수집"""
    all_clips = []
    
    clips = folder.GetClipList()
    if clips:
        all_clips.extend(clips)
    
    subfolders = folder.GetSubFolderList()
    if subfolders:
        for subfolder in subfolders:
            all_clips.extend(_get_all_clips_recursive(subfolder))
    
    return all_clips


# ============================================
# 사용 예시
# ============================================

"""
# Suuktest 폴더 구조 스캔
structure = await suuktest_scan_structure(show_details=True)

# 특정 폴더 임포트
result = await suuktest_import_folder(
    subfolder_path="mac3/CJU_SE",
    organize_by_extension=True
)

# XML 타임라인 임포트
timelines = await suuktest_import_all_xmls(
    subfolder_path="mac3/CJU_SE"
)

# 미디어 파일 검색
files = await suuktest_find_media_files(
    subfolder_path="mac3",
    file_type="video"
)

# 오프라인 클립 릴링크
result = await suuktest_relink_clips(
    subfolder_path="mac3/CJU_SE"
)

# 프로젝트 목록
projects = await suuktest_list_projects()
"""
