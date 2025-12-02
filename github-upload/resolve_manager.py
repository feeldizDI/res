#!/usr/bin/env python3
"""
DaVinci Resolve - XML 타임라인 임포트 및 파일 관리 통합 툴
사용법: python3 resolve_manager.py [옵션]

기능:
1. XML/AAF/EDL 파일을 타임라인으로 임포트
2. 미디어풀 파일 자동 정리
3. 타임라인 관리 (생성, 삭제, 복제)
4. 클립 자동 매칭 및 릴링크
"""

import sys
import os
import glob

# DaVinci Resolve API 경로
resolve_script_api = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
resolve_script_lib = os.path.join(resolve_script_api, "Modules")
sys.path.append(resolve_script_lib)

try:
    import DaVinciResolveScript as dvr_script
except:
    print("❌ ERROR: DaVinciResolveScript module not found")
    print("   Make sure DaVinci Resolve is installed")
    sys.exit(1)


class ResolveManager:
    def __init__(self):
        self.resolve = dvr_script.scriptapp("Resolve")
        if not self.resolve:
            raise Exception("Could not connect to DaVinci Resolve")
        
        self.project_manager = self.resolve.GetProjectManager()
        self.project = self.project_manager.GetCurrentProject()
        if not self.project:
            raise Exception("No project is currently open")
        
        self.media_pool = self.project.GetMediaPool()
        self.root_folder = self.media_pool.GetRootFolder()
        
        print(f"✅ Connected to project: {self.project.GetName()}")
    
    
    def import_timeline_from_xml(self, xml_path, timeline_name=None):
        """
        XML/AAF/EDL 파일을 타임라인으로 임포트
        
        Args:
            xml_path: XML 파일 경로
            timeline_name: 타임라인 이름 (None이면 파일명 사용)
        
        Returns:
            Timeline object or None
        """
        print(f"\n📥 Importing timeline from: {xml_path}")
        
        if not os.path.exists(xml_path):
            print(f"❌ ERROR: File not found: {xml_path}")
            return None
        
        # 파일 확장자 확인
        ext = os.path.splitext(xml_path)[1].lower()
        supported_formats = ['.xml', '.fcpxml', '.aaf', '.edl']
        
        if ext not in supported_formats:
            print(f"❌ ERROR: Unsupported format: {ext}")
            print(f"   Supported formats: {', '.join(supported_formats)}")
            return None
        
        # 타임라인 임포트
        try:
            imported_timeline = self.media_pool.ImportTimelineFromFile(xml_path)
            
            if imported_timeline:
                # 타임라인 이름 변경 (옵션)
                if timeline_name:
                    imported_timeline.SetName(timeline_name)
                
                current_name = imported_timeline.GetName()
                print(f"✅ Successfully imported timeline: {current_name}")
                
                # 타임라인 정보 출력
                fps = imported_timeline.GetSetting("timelineFrameRate")
                resolution = f"{imported_timeline.GetSetting('timelineResolutionWidth')}x{imported_timeline.GetSetting('timelineResolutionHeight')}"
                
                print(f"   Frame Rate: {fps}")
                print(f"   Resolution: {resolution}")
                
                return imported_timeline
            else:
                print(f"❌ Failed to import timeline")
                return None
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            return None
    
    
    def import_all_xml_from_folder(self, folder_path, create_bin=True):
        """
        폴더의 모든 XML 파일을 타임라인으로 임포트
        
        Args:
            folder_path: XML 파일들이 있는 폴더 경로
            create_bin: XML 폴더를 빈으로 생성할지 여부
        """
        print(f"\n📂 Scanning folder: {folder_path}")
        
        # XML 파일 찾기
        xml_patterns = ['*.xml', '*.fcpxml', '*.aaf', '*.edl']
        xml_files = []
        
        for pattern in xml_patterns:
            xml_files.extend(glob.glob(os.path.join(folder_path, pattern)))
            xml_files.extend(glob.glob(os.path.join(folder_path, '**', pattern), recursive=True))
        
        if not xml_files:
            print(f"⚠️  No XML files found in {folder_path}")
            return
        
        print(f"   Found {len(xml_files)} XML files")
        
        # XML 빈 생성 (옵션)
        if create_bin:
            xml_bin = None
            for subfolder in self.root_folder.GetSubFolderList():
                if subfolder.GetName() == "Xml":
                    xml_bin = subfolder
                    break
            
            if not xml_bin:
                xml_bin = self.media_pool.AddSubFolder(self.root_folder, "Xml")
                print(f"   Created Xml bin")
        
        # 각 XML 파일 임포트
        imported_count = 0
        for xml_file in xml_files:
            timeline = self.import_timeline_from_xml(xml_file)
            if timeline:
                imported_count += 1
        
        print(f"\n✅ Imported {imported_count}/{len(xml_files)} timelines")
    
    
    def list_timelines(self):
        """모든 타임라인 리스트 출력"""
        timelines = self.project.GetTimelineCount()
        
        print(f"\n📋 Total Timelines: {timelines}")
        
        for i in range(1, timelines + 1):
            timeline = self.project.GetTimelineByIndex(i)
            name = timeline.GetName()
            fps = timeline.GetSetting("timelineFrameRate")
            track_count = timeline.GetTrackCount("video")
            
            print(f"   {i}. {name}")
            print(f"      FPS: {fps}, Video Tracks: {track_count}")
    
    
    def organize_media_pool_by_extension(self, source_bin_name="Master"):
        """
        미디어풀을 확장자별로 자동 정리
        
        Args:
            source_bin_name: 정리할 소스 빈 이름
        """
        print(f"\n🗂️  Organizing media pool by extension...")
        
        # 소스 빈 찾기 (기본값: Master = root)
        if source_bin_name == "Master":
            source_folder = self.root_folder
        else:
            source_folder = None
            for subfolder in self.root_folder.GetSubFolderList():
                if subfolder.GetName() == source_bin_name:
                    source_folder = subfolder
                    break
            
            if not source_folder:
                print(f"❌ Bin '{source_bin_name}' not found")
                return
        
        # 클립 가져오기
        clips = source_folder.GetClipList()
        
        if not clips:
            print(f"   No clips in {source_bin_name}")
            return
        
        print(f"   Found {len(clips)} clips")
        
        # 확장자별 그룹화
        extension_groups = {}
        
        for clip in clips:
            clip_name = clip.GetClipProperty("File Name")
            if not clip_name:
                clip_name = clip.GetName()
            
            _, ext = os.path.splitext(clip_name)
            ext = ext.lower()
            
            if ext:
                ext_clean = ext[1:] if ext.startswith('.') else ext
                folder_name = ext_clean.capitalize()
                
                if folder_name not in extension_groups:
                    extension_groups[folder_name] = []
                
                extension_groups[folder_name].append(clip)
        
        # 폴더 생성 및 이동
        for folder_name, clips_list in extension_groups.items():
            # 폴더 찾거나 생성
            target_folder = None
            for subfolder in self.root_folder.GetSubFolderList():
                if subfolder.GetName() == folder_name:
                    target_folder = subfolder
                    break
            
            if not target_folder:
                target_folder = self.media_pool.AddSubFolder(self.root_folder, folder_name)
                print(f"   Created: {folder_name}/")
            
            # 클립 이동
            self.media_pool.MoveClips(clips_list, target_folder)
            print(f"   Moved {len(clips_list)} clips to {folder_name}/")
        
        print(f"✅ Organization complete")
    
    
    def relink_clips_to_folder(self, media_folder_path, recursive=True):
        """
        미디어 파일 자동 릴링크
        
        Args:
            media_folder_path: 미디어 파일들이 있는 폴더 경로
            recursive: 서브폴더까지 검색할지 여부
        """
        print(f"\n🔗 Relinking clips to: {media_folder_path}")
        
        # 모든 클립 가져오기
        all_clips = []
        
        def get_clips_recursive(folder):
            clips = folder.GetClipList()
            if clips:
                all_clips.extend(clips)
            
            subfolders = folder.GetSubFolderList()
            if subfolders:
                for subfolder in subfolders:
                    get_clips_recursive(subfolder)
        
        get_clips_recursive(self.root_folder)
        
        print(f"   Found {len(all_clips)} clips in media pool")
        
        # Offline 클립 찾기
        offline_clips = []
        for clip in all_clips:
            clip_property = clip.GetClipProperty("File Path")
            if not clip_property or not os.path.exists(clip_property):
                offline_clips.append(clip)
        
        print(f"   Found {len(offline_clips)} offline clips")
        
        if offline_clips:
            # 릴링크 시도
            result = self.media_pool.RelinkClips(offline_clips, media_folder_path)
            
            if result:
                print(f"✅ Successfully relinked clips")
            else:
                print(f"⚠️  Relink may have partial success")
        else:
            print(f"   All clips are already online")
    
    
    def create_timeline_from_clips(self, bin_name, timeline_name=None):
        """
        빈의 모든 클립으로 타임라인 생성
        
        Args:
            bin_name: 소스 빈 이름
            timeline_name: 생성할 타임라인 이름
        """
        print(f"\n🎬 Creating timeline from bin: {bin_name}")
        
        # 빈 찾기
        source_bin = None
        for subfolder in self.root_folder.GetSubFolderList():
            if subfolder.GetName() == bin_name:
                source_bin = subfolder
                break
        
        if not source_bin:
            print(f"❌ Bin '{bin_name}' not found")
            return None
        
        # 클립 가져오기
        clips = source_bin.GetClipList()
        
        if not clips:
            print(f"❌ No clips in bin '{bin_name}'")
            return None
        
        print(f"   Found {len(clips)} clips")
        
        # 타임라인 이름 결정
        if not timeline_name:
            timeline_name = f"{bin_name}_Timeline"
        
        # 타임라인 생성
        timeline = self.media_pool.CreateTimelineFromClips(timeline_name, clips)
        
        if timeline:
            print(f"✅ Created timeline: {timeline_name}")
            return timeline
        else:
            print(f"❌ Failed to create timeline")
            return None
    
    
    def show_media_pool_structure(self):
        """미디어풀 구조 트리 출력"""
        print(f"\n🌳 Media Pool Structure:")
        print("="*60)
        
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
        print("="*60)


def main():
    """메인 함수 - 대화형 메뉴"""
    try:
        manager = ResolveManager()
        
        while True:
            print("\n" + "="*60)
            print("🎬 DaVinci Resolve Manager")
            print("="*60)
            print("1. Import XML/AAF/EDL to Timeline")
            print("2. Import all XMLs from folder")
            print("3. List all timelines")
            print("4. Organize media pool by extension")
            print("5. Create timeline from bin")
            print("6. Relink clips to folder")
            print("7. Show media pool structure")
            print("8. Exit")
            print("="*60)
            
            choice = input("\nSelect option (1-8): ").strip()
            
            if choice == "1":
                xml_path = input("Enter XML file path: ").strip()
                timeline_name = input("Enter timeline name (or press Enter for default): ").strip()
                if timeline_name == "":
                    timeline_name = None
                manager.import_timeline_from_xml(xml_path, timeline_name)
            
            elif choice == "2":
                folder_path = input("Enter folder path: ").strip()
                manager.import_all_xml_from_folder(folder_path)
            
            elif choice == "3":
                manager.list_timelines()
            
            elif choice == "4":
                bin_name = input("Enter source bin name (default: Master): ").strip()
                if bin_name == "":
                    bin_name = "Master"
                manager.organize_media_pool_by_extension(bin_name)
            
            elif choice == "5":
                bin_name = input("Enter bin name: ").strip()
                timeline_name = input("Enter timeline name (optional): ").strip()
                if timeline_name == "":
                    timeline_name = None
                manager.create_timeline_from_clips(bin_name, timeline_name)
            
            elif choice == "6":
                media_folder = input("Enter media folder path: ").strip()
                manager.relink_clips_to_folder(media_folder)
            
            elif choice == "7":
                manager.show_media_pool_structure()
            
            elif choice == "8":
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
