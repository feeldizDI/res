#!/usr/bin/env python3
"""
DaVinci Resolve - Suuktest 폴더 통합 관리 시스템
최상위 폴더: /Users/Shared/suuktest

기능:
1. suuktest 폴더 구조 자동 스캔
2. 미디어 파일 자동 임포트 및 정리
3. XML/AAF 타임라인 자동 임포트
4. 프로젝트별 파일 관리
5. 오프라인 클립 자동 릴링크
"""

import sys
import os
import glob
from pathlib import Path
from collections import defaultdict

# DaVinci Resolve API 경로
resolve_script_api = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
resolve_script_lib = os.path.join(resolve_script_api, "Modules")
sys.path.append(resolve_script_lib)

try:
    import DaVinciResolveScript as dvr_script
except:
    print("❌ ERROR: DaVinciResolveScript module not found")
    sys.exit(1)


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
    'document': ['.pdf', '.doc', '.docx', '.txt', '.md']
}


class SuuktestManager:
    """Suuktest 폴더 기반 DaVinci Resolve 관리 클래스"""
    
    def __init__(self):
        self.root_path = Path(SUUKTEST_ROOT)
        
        if not self.root_path.exists():
            raise Exception(f"Suuktest folder not found: {SUUKTEST_ROOT}")
        
        # DaVinci Resolve 연결
        self.resolve = dvr_script.scriptapp("Resolve")
        if not self.resolve:
            raise Exception("Could not connect to DaVinci Resolve")
        
        self.project_manager = self.resolve.GetProjectManager()
        self.project = self.project_manager.GetCurrentProject()
        if not self.project:
            raise Exception("No project is currently open")
        
        self.media_pool = self.project.GetMediaPool()
        self.media_storage = self.resolve.GetMediaStorage()
        self.root_folder = self.media_pool.GetRootFolder()
        
        print(f"✅ Connected to DaVinci Resolve")
        print(f"📂 Project: {self.project.GetName()}")
        print(f"🗂️  Root folder: {SUUKTEST_ROOT}")
    
    
    def scan_folder_structure(self, show_files=False):
        """
        Suuktest 폴더 구조 스캔 및 출력
        
        Args:
            show_files: 파일까지 표시할지 여부
        """
        print(f"\n🔍 Scanning folder structure: {SUUKTEST_ROOT}")
        print("="*80)
        
        folder_stats = defaultdict(lambda: defaultdict(int))
        
        def scan_recursive(path, indent=0):
            try:
                entries = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
                
                for entry in entries:
                    if entry.name.startswith('.'):
                        continue
                    
                    prefix = "  " * indent
                    
                    if entry.is_dir():
                        # 폴더
                        print(f"{prefix}📁 {entry.name}/")
                        scan_recursive(entry, indent + 1)
                    elif show_files:
                        # 파일
                        ext = entry.suffix.lower()
                        size_mb = entry.stat().st_size / (1024 * 1024)
                        
                        # 파일 타입 분류
                        file_type = self._get_file_type(ext)
                        folder_stats[entry.parent.name][file_type] += 1
                        
                        icon = self._get_file_icon(ext)
                        print(f"{prefix}{icon} {entry.name} ({size_mb:.1f} MB)")
            
            except PermissionError:
                print(f"{prefix}⚠️  Permission denied")
        
        scan_recursive(self.root_path)
        
        # 통계 출력
        if folder_stats:
            print("\n" + "="*80)
            print("📊 Folder Statistics:")
            for folder, stats in folder_stats.items():
                print(f"\n  {folder}/")
                for file_type, count in stats.items():
                    print(f"    {file_type}: {count} files")
        
        print("="*80)
    
    
    def find_all_media_files(self, subfolder=None):
        """
        Suuktest 폴더에서 모든 미디어 파일 찾기
        
        Args:
            subfolder: 특정 서브폴더만 스캔 (None이면 전체)
        
        Returns:
            dict: 파일 타입별 파일 경로 리스트
        """
        search_path = self.root_path / subfolder if subfolder else self.root_path
        
        print(f"\n🔍 Finding media files in: {search_path}")
        
        media_files = defaultdict(list)
        
        for category, extensions in MEDIA_EXTENSIONS.items():
            for ext in extensions:
                pattern = f"**/*{ext}"
                files = list(search_path.glob(pattern))
                media_files[category].extend(files)
        
        # 통계 출력
        print("\n📊 Found media files:")
        total = 0
        for category, files in media_files.items():
            count = len(files)
            total += count
            if count > 0:
                print(f"  {category.capitalize()}: {count} files")
        
        print(f"  Total: {total} files")
        
        return media_files
    
    
    def import_folder_to_mediapool(self, subfolder_name, organize=True):
        """
        Suuktest의 특정 서브폴더를 미디어풀에 임포트
        
        Args:
            subfolder_name: 서브폴더 이름 (예: "mac3/CJU_SE")
            organize: 확장자별로 정리할지 여부
        """
        source_path = self.root_path / subfolder_name
        
        if not source_path.exists():
            print(f"❌ Folder not found: {source_path}")
            return
        
        print(f"\n📥 Importing from: {source_path}")
        
        # 미디어 파일 찾기
        media_files = self.find_all_media_files(subfolder_name)
        
        # 프로젝트 빈 생성
        project_bin_name = Path(subfolder_name).name
        project_bin = self._get_or_create_bin(project_bin_name)
        
        print(f"\n📁 Created/Using bin: {project_bin_name}")
        
        # 파일 타입별로 임포트
        imported_total = 0
        
        for category, files in media_files.items():
            if not files:
                continue
            
            if category == 'timeline':
                # XML 파일은 타임라인으로 임포트
                print(f"\n🎬 Importing timelines...")
                for xml_file in files:
                    timeline = self.media_pool.ImportTimelineFromFile(str(xml_file))
                    if timeline:
                        print(f"  ✅ {xml_file.name}")
                        imported_total += 1
            else:
                # 미디어 파일은 클립으로 임포트
                if organize:
                    # 카테고리별 빈 생성
                    category_bin = self._get_or_create_bin(
                        category.capitalize(),
                        parent=project_bin
                    )
                    self.media_pool.SetCurrentFolder(category_bin)
                else:
                    self.media_pool.SetCurrentFolder(project_bin)
                
                # 파일 경로를 문자열로 변환
                file_paths = [str(f) for f in files]
                
                # Media Storage를 통해 임포트
                print(f"\n📥 Importing {category} files...")
                clips = self.media_storage.AddItemListToMediaPool(file_paths)
                
                if clips:
                    count = len(clips) if isinstance(clips, list) else 1
                    print(f"  ✅ Imported {count} {category} files")
                    imported_total += count
                else:
                    print(f"  ⚠️  Failed to import {category} files")
        
        print(f"\n✅ Total imported: {imported_total} items")
    
    
    def import_all_xmls_from_subfolder(self, subfolder_name):
        """
        특정 서브폴더의 모든 XML을 타임라인으로 임포트
        
        Args:
            subfolder_name: 서브폴더 이름 (예: "mac3/CJU_SE")
        """
        source_path = self.root_path / subfolder_name
        
        if not source_path.exists():
            print(f"❌ Folder not found: {source_path}")
            return
        
        print(f"\n🎬 Importing XML timelines from: {source_path}")
        
        # XML 파일 찾기
        xml_files = []
        for ext in MEDIA_EXTENSIONS['timeline']:
            xml_files.extend(source_path.glob(f"**/*{ext}"))
        
        if not xml_files:
            print(f"⚠️  No XML files found")
            return
        
        print(f"   Found {len(xml_files)} XML files")
        
        # 각 XML 임포트
        imported = []
        failed = []
        
        for xml_file in xml_files:
            try:
                timeline = self.media_pool.ImportTimelineFromFile(str(xml_file))
                if timeline:
                    timeline_name = timeline.GetName()
                    imported.append(timeline_name)
                    print(f"  ✅ {xml_file.name} → {timeline_name}")
                else:
                    failed.append(xml_file.name)
                    print(f"  ❌ {xml_file.name}")
            except Exception as e:
                failed.append(f"{xml_file.name}: {str(e)}")
                print(f"  ❌ {xml_file.name}: {str(e)}")
        
        # 결과 요약
        print(f"\n📊 Import Summary:")
        print(f"  ✅ Successfully imported: {len(imported)}")
        print(f"  ❌ Failed: {len(failed)}")
        
        if imported:
            print(f"\n🎬 Imported timelines:")
            for name in imported:
                print(f"    - {name}")
    
    
    def auto_organize_mediapool_by_extension(self, source_bin_name=None):
        """
        미디어풀을 확장자별로 자동 정리
        
        Args:
            source_bin_name: 정리할 소스 빈 (None이면 루트)
        """
        print(f"\n🗂️  Auto-organizing media pool by extension...")
        
        # 소스 빈 결정
        if source_bin_name:
            source_bin = self._find_bin(source_bin_name)
            if not source_bin:
                print(f"❌ Bin '{source_bin_name}' not found")
                return
        else:
            source_bin = self.root_folder
        
        # 클립 가져오기
        clips = source_bin.GetClipList()
        
        if not clips:
            print(f"  No clips to organize")
            return
        
        print(f"  Found {len(clips)} clips")
        
        # 확장자별 그룹화
        extension_groups = defaultdict(list)
        
        for clip in clips:
            clip_name = clip.GetClipProperty("File Name") or clip.GetName()
            ext = Path(clip_name).suffix.lower()
            
            if ext:
                ext_clean = ext[1:]  # 점(.) 제거
                folder_name = ext_clean.capitalize()
                extension_groups[folder_name].append(clip)
        
        # 폴더 생성 및 이동
        moved_total = 0
        
        for folder_name, clips_list in extension_groups.items():
            target_bin = self._get_or_create_bin(folder_name)
            
            result = self.media_pool.MoveClips(clips_list, target_bin)
            if result:
                print(f"  ✅ Moved {len(clips_list)} clips to {folder_name}/")
                moved_total += len(clips_list)
        
        print(f"\n✅ Organized {moved_total} clips")
    
    
    def relink_all_offline_clips(self):
        """
        모든 오프라인 클립을 Suuktest 폴더에서 자동 릴링크
        """
        print(f"\n🔗 Relinking offline clips to Suuktest folder...")
        
        # 모든 클립 수집
        all_clips = self._get_all_clips_recursive()
        
        print(f"  Total clips in media pool: {len(all_clips)}")
        
        # 오프라인 클립 찾기
        offline_clips = []
        
        for clip in all_clips:
            file_path = clip.GetClipProperty("File Path")
            if not file_path or not os.path.exists(file_path):
                offline_clips.append(clip)
        
        if not offline_clips:
            print(f"  ✅ All clips are online")
            return
        
        print(f"  Found {len(offline_clips)} offline clips")
        
        # Suuktest 폴더에서 릴링크 시도
        result = self.media_pool.RelinkClips(offline_clips, str(self.root_path))
        
        # 결과 확인
        still_offline = 0
        for clip in offline_clips:
            file_path = clip.GetClipProperty("File Path")
            if not file_path or not os.path.exists(file_path):
                still_offline += 1
        
        relinked = len(offline_clips) - still_offline
        
        print(f"\n📊 Relink Summary:")
        print(f"  ✅ Relinked: {relinked}")
        print(f"  ❌ Still offline: {still_offline}")
    
    
    def list_suuktest_projects(self):
        """
        Suuktest 폴더의 프로젝트 구조 출력
        """
        print(f"\n📂 Suuktest Projects:")
        print("="*80)
        
        # 1단계 서브폴더 (예: mac3)
        for level1 in sorted(self.root_path.iterdir()):
            if not level1.is_dir() or level1.name.startswith('.'):
                continue
            
            print(f"\n📁 {level1.name}/")
            
            # 2단계 서브폴더 (예: CJU_SE)
            for level2 in sorted(level1.iterdir()):
                if not level2.is_dir() or level2.name.startswith('.'):
                    continue
                
                # 파일 타입별 카운트
                file_counts = defaultdict(int)
                total_size = 0
                
                for file in level2.rglob("*"):
                    if file.is_file():
                        ext = file.suffix.lower()
                        file_type = self._get_file_type(ext)
                        file_counts[file_type] += 1
                        total_size += file.stat().st_size
                
                size_gb = total_size / (1024**3)
                
                print(f"  📁 {level2.name}/ ({size_gb:.2f} GB)")
                
                for file_type, count in sorted(file_counts.items()):
                    if count > 0:
                        print(f"     {file_type}: {count} files")
        
        print("="*80)
    
    
    def show_mediapool_structure(self):
        """미디어풀 구조 트리 출력"""
        print(f"\n🌳 Media Pool Structure:")
        print("="*80)
        
        def print_folder(folder, indent=0):
            name = folder.GetName()
            clips = folder.GetClipList()
            clip_count = len(clips) if clips else 0
            
            prefix = "  " * indent
            print(f"{prefix}📁 {name}/ ({clip_count} clips)")
            
            subfolders = folder.GetSubFolderList()
            if subfolders:
                for subfolder in subfolders:
                    print_folder(subfolder, indent + 1)
        
        print_folder(self.root_folder)
        print("="*80)
    
    
    # ============================================
    # Helper Methods
    # ============================================
    
    def _get_file_type(self, ext):
        """파일 확장자로 타입 결정"""
        ext = ext.lower()
        for category, extensions in MEDIA_EXTENSIONS.items():
            if ext in extensions:
                return category
        return 'other'
    
    
    def _get_file_icon(self, ext):
        """파일 확장자로 아이콘 결정"""
        file_type = self._get_file_type(ext)
        icons = {
            'video': '🎥',
            'audio': '🔊',
            'image': '🖼️',
            'timeline': '🎬',
            'document': '📄',
            'other': '📄'
        }
        return icons.get(file_type, '📄')
    
    
    def _get_or_create_bin(self, bin_name, parent=None):
        """빈을 찾거나 생성"""
        if parent is None:
            parent = self.root_folder
        
        # 기존 빈 찾기
        for subfolder in parent.GetSubFolderList():
            if subfolder.GetName() == bin_name:
                return subfolder
        
        # 빈 생성
        new_bin = self.media_pool.AddSubFolder(parent, bin_name)
        return new_bin
    
    
    def _find_bin(self, bin_name, parent=None):
        """빈 찾기 (재귀)"""
        if parent is None:
            parent = self.root_folder
        
        for subfolder in parent.GetSubFolderList():
            if subfolder.GetName() == bin_name:
                return subfolder
            
            # 재귀 검색
            result = self._find_bin(bin_name, subfolder)
            if result:
                return result
        
        return None
    
    
    def _get_all_clips_recursive(self, folder=None):
        """모든 클립을 재귀적으로 수집"""
        if folder is None:
            folder = self.root_folder
        
        all_clips = []
        
        clips = folder.GetClipList()
        if clips:
            all_clips.extend(clips)
        
        subfolders = folder.GetSubFolderList()
        if subfolders:
            for subfolder in subfolders:
                all_clips.extend(self._get_all_clips_recursive(subfolder))
        
        return all_clips


# ============================================
# 메인 메뉴
# ============================================

def main():
    """대화형 메뉴"""
    try:
        manager = SuuktestManager()
        
        while True:
            print("\n" + "="*80)
            print("🗂️  SUUKTEST FOLDER MANAGER")
            print(f"📂 Root: {SUUKTEST_ROOT}")
            print("="*80)
            print("1. Scan Suuktest folder structure")
            print("2. List all Suuktest projects")
            print("3. Import folder to media pool")
            print("4. Import all XMLs from subfolder")
            print("5. Auto-organize media pool by extension")
            print("6. Relink all offline clips")
            print("7. Show media pool structure")
            print("8. Find all media files")
            print("9. Exit")
            print("="*80)
            
            choice = input("\nSelect option (1-9): ").strip()
            
            if choice == "1":
                show_files = input("Show files? (y/n): ").strip().lower() == 'y'
                manager.scan_folder_structure(show_files)
            
            elif choice == "2":
                manager.list_suuktest_projects()
            
            elif choice == "3":
                subfolder = input("Enter subfolder (e.g., mac3/CJU_SE): ").strip()
                organize = input("Organize by extension? (y/n): ").strip().lower() == 'y'
                manager.import_folder_to_mediapool(subfolder, organize)
            
            elif choice == "4":
                subfolder = input("Enter subfolder (e.g., mac3/CJU_SE): ").strip()
                manager.import_all_xmls_from_subfolder(subfolder)
            
            elif choice == "5":
                bin_name = input("Enter source bin name (or Enter for root): ").strip()
                if bin_name == "":
                    bin_name = None
                manager.auto_organize_mediapool_by_extension(bin_name)
            
            elif choice == "6":
                manager.relink_all_offline_clips()
            
            elif choice == "7":
                manager.show_mediapool_structure()
            
            elif choice == "8":
                subfolder = input("Enter subfolder (or Enter for all): ").strip()
                if subfolder == "":
                    subfolder = None
                manager.find_all_media_files(subfolder)
            
            elif choice == "9":
                print("\n👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid option")
    
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
