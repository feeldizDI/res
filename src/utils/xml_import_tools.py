"""
DaVinci Resolve - XML/AAF/EDL 타임라인 임포트 및 미디어풀 관리 유틸리티
"""

import os
import glob
from typing import Optional, Dict, List, Any


# ============================================
# XML/AAF/EDL 타임라인 임포트 Functions
# ============================================

def import_timeline_from_file(
    resolve,
    file_path: str,
    timeline_name: Optional[str] = None
) -> dict:
    """XML/AAF/EDL 파일을 타임라인으로 임포트"""
    project = resolve.GetProjectManager().GetCurrentProject()
    media_pool = project.GetMediaPool()

    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}

    # 지원 형식 확인
    ext = os.path.splitext(file_path)[1].lower()
    supported_formats = ['.xml', '.fcpxml', '.aaf', '.edl']

    if ext not in supported_formats:
        return {
            "error": f"Unsupported format: {ext}",
            "supported_formats": supported_formats
        }

    try:
        # 타임라인 임포트
        timeline = media_pool.ImportTimelineFromFile(file_path)

        if not timeline:
            return {"error": "Failed to import timeline"}

        # 타임라인 이름 변경 (옵션)
        if timeline_name:
            timeline.SetName(timeline_name)

        # 타임라인 정보 가져오기
        current_name = timeline.GetName()
        fps = timeline.GetSetting("timelineFrameRate")
        width = timeline.GetSetting("timelineResolutionWidth")
        height = timeline.GetSetting("timelineResolutionHeight")

        return {
            "success": True,
            "timeline_name": current_name,
            "fps": fps,
            "resolution": f"{width}x{height}",
            "file_path": file_path
        }

    except Exception as e:
        return {"error": str(e)}


def import_all_xml_from_folder(
    resolve,
    folder_path: str,
    create_xml_bin: bool = True,
    recursive: bool = False
) -> dict:
    """폴더의 모든 XML/AAF/EDL 파일을 타임라인으로 임포트"""
    project = resolve.GetProjectManager().GetCurrentProject()
    media_pool = project.GetMediaPool()
    root_folder = media_pool.GetRootFolder()

    if not os.path.exists(folder_path):
        return {"error": f"Folder not found: {folder_path}"}

    # XML 파일 찾기
    xml_patterns = ['*.xml', '*.fcpxml', '*.aaf', '*.edl']
    xml_files = []

    for pattern in xml_patterns:
        if recursive:
            xml_files.extend(glob.glob(os.path.join(folder_path, '**', pattern), recursive=True))
        else:
            xml_files.extend(glob.glob(os.path.join(folder_path, pattern)))

    if not xml_files:
        return {
            "success": True,
            "imported_count": 0,
            "total_files": 0,
            "message": "No XML files found"
        }

    # Xml 빈 생성 (옵션)
    if create_xml_bin:
        xml_bin = None
        for subfolder in root_folder.GetSubFolderList():
            if subfolder.GetName() == "Xml":
                xml_bin = subfolder
                break

        if not xml_bin:
            xml_bin = media_pool.AddSubFolder(root_folder, "Xml")

    # 각 XML 파일 임포트
    imported_timelines = []
    failed_files = []

    for xml_file in xml_files:
        try:
            timeline = media_pool.ImportTimelineFromFile(xml_file)
            if timeline:
                imported_timelines.append(timeline.GetName())
            else:
                failed_files.append(os.path.basename(xml_file))
        except Exception as e:
            failed_files.append(f"{os.path.basename(xml_file)}: {str(e)}")

    return {
        "success": True,
        "imported_count": len(imported_timelines),
        "total_files": len(xml_files),
        "timelines": imported_timelines,
        "failed_files": failed_files if failed_files else None
    }


# ============================================
# 미디어풀 관리 Functions
# ============================================

def get_clips_in_bin(
    resolve,
    bin_name: Optional[str] = None
) -> dict:
    """특정 빈의 모든 클립 정보 가져오기"""
    project = resolve.GetProjectManager().GetCurrentProject()
    media_pool = project.GetMediaPool()

    # 빈 찾기
    if bin_name:
        root_folder = media_pool.GetRootFolder()
        target_folder = None

        for subfolder in root_folder.GetSubFolderList():
            if subfolder.GetName() == bin_name:
                target_folder = subfolder
                break

        if not target_folder:
            return {"error": f"Bin '{bin_name}' not found"}

        clips = target_folder.GetClipList()
    else:
        current_folder = media_pool.GetCurrentFolder()
        clips = current_folder.GetClipList()
        bin_name = current_folder.GetName()

    if not clips:
        return {
            "bin": bin_name,
            "count": 0,
            "clips": []
        }

    # 클립 정보 수집
    clip_list = []
    for clip in clips:
        clip_info = {
            "name": clip.GetClipProperty("File Name") or clip.GetName(),
            "file_path": clip.GetClipProperty("File Path"),
            "duration": clip.GetClipProperty("Duration"),
            "fps": clip.GetClipProperty("FPS"),
            "resolution": clip.GetClipProperty("Resolution"),
            "codec": clip.GetClipProperty("Video Codec Name"),
            "type": clip.GetClipProperty("Type"),
        }
        clip_list.append(clip_info)

    return {
        "bin": bin_name,
        "count": len(clip_list),
        "clips": clip_list
    }


def get_media_pool_structure(resolve) -> dict:
    """미디어풀의 전체 구조를 트리 형태로 가져오기"""
    project = resolve.GetProjectManager().GetCurrentProject()
    media_pool = project.GetMediaPool()
    root_folder = media_pool.GetRootFolder()

    def get_folder_structure(folder):
        clips = folder.GetClipList()
        subfolders = folder.GetSubFolderList()

        structure = {
            "name": folder.GetName(),
            "clips": len(clips) if clips else 0,
            "subfolders": {}
        }

        if subfolders:
            for subfolder in subfolders:
                subfolder_name = subfolder.GetName()
                structure["subfolders"][subfolder_name] = get_folder_structure(subfolder)

        return structure

    return get_folder_structure(root_folder)


def create_timeline_from_bin_clips(
    resolve,
    bin_name: str,
    timeline_name: Optional[str] = None
) -> dict:
    """빈의 모든 클립으로 타임라인 생성"""
    project = resolve.GetProjectManager().GetCurrentProject()
    media_pool = project.GetMediaPool()
    root_folder = media_pool.GetRootFolder()

    # 빈 찾기
    source_bin = None
    for subfolder in root_folder.GetSubFolderList():
        if subfolder.GetName() == bin_name:
            source_bin = subfolder
            break

    if not source_bin:
        return {"error": f"Bin '{bin_name}' not found"}

    # 클립 가져오기
    clips = source_bin.GetClipList()

    if not clips:
        return {"error": f"No clips in bin '{bin_name}'"}

    # 타임라인 이름 결정
    if not timeline_name:
        timeline_name = f"{bin_name}_Timeline"

    # 타임라인 생성
    timeline = media_pool.CreateTimelineFromClips(timeline_name, clips)

    if timeline:
        return {
            "success": True,
            "timeline_name": timeline.GetName(),
            "clip_count": len(clips)
        }
    else:
        return {"error": "Failed to create timeline"}


def relink_offline_clips(
    resolve,
    media_folder_path: str,
    bin_name: Optional[str] = None
) -> dict:
    """오프라인 클립들을 특정 폴더의 미디어로 자동 릴링크"""
    project = resolve.GetProjectManager().GetCurrentProject()
    media_pool = project.GetMediaPool()
    root_folder = media_pool.GetRootFolder()

    if not os.path.exists(media_folder_path):
        return {"error": f"Folder not found: {media_folder_path}"}

    # 클립 수집
    all_clips = []

    if bin_name:
        # 특정 빈만
        target_bin = None
        for subfolder in root_folder.GetSubFolderList():
            if subfolder.GetName() == bin_name:
                target_bin = subfolder
                break

        if not target_bin:
            return {"error": f"Bin '{bin_name}' not found"}

        clips = target_bin.GetClipList()
        if clips:
            all_clips.extend(clips)
    else:
        # 전체 미디어풀
        def get_clips_recursive(folder):
            clips = folder.GetClipList()
            if clips:
                all_clips.extend(clips)

            subfolders = folder.GetSubFolderList()
            if subfolders:
                for subfolder in subfolders:
                    get_clips_recursive(subfolder)

        get_clips_recursive(root_folder)

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
    result = media_pool.RelinkClips(offline_clips, media_folder_path)

    # 릴링크 후 다시 확인
    still_offline = 0
    for clip in offline_clips:
        file_path = clip.GetClipProperty("File Path")
        if not file_path or not os.path.exists(file_path):
            still_offline += 1

    relinked_count = len(offline_clips) - still_offline

    return {
        "success": True,
        "total_clips": len(all_clips),
        "offline_clips": len(offline_clips),
        "relinked": relinked_count,
        "still_offline": still_offline
    }
