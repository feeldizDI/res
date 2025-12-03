#!/usr/bin/env python3
"""
DaVinci Resolve - 확장자별 미디어풀 자동 정리
사용법: python3 organize_by_extension.py
"""

import sys
import os

# DaVinci Resolve API 경로
resolve_script_api = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
resolve_script_lib = os.path.join(resolve_script_api, "Modules")
sys.path.append(resolve_script_lib)

try:
    import DaVinciResolveScript as dvr_script
    
    # Resolve 연결
    resolve = dvr_script.scriptapp("Resolve")
    
    if not resolve:
        print("❌ ERROR: Could not connect to DaVinci Resolve")
        print("   Make sure DaVinci Resolve is running")
        sys.exit(1)
    
    # 현재 프로젝트 가져오기
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    
    if not project:
        print("❌ ERROR: No project is currently open")
        sys.exit(1)
    
    print(f"📂 Project: {project.GetName()}")
    
    # Media Pool 가져오기
    media_pool = project.GetMediaPool()
    root_folder = media_pool.GetRootFolder()
    
    # ========================================
    # STEP 1: CJU_SE 빈 찾기
    # ========================================
    print("\n🔍 Searching for CJU_SE bin...")
    
    cju_folder = None
    for subfolder in root_folder.GetSubFolderList():
        if subfolder.GetName() == "CJU_SE":
            cju_folder = subfolder
            break
    
    if not cju_folder:
        print("❌ ERROR: CJU_SE bin not found")
        print("   Available bins:")
        for subfolder in root_folder.GetSubFolderList():
            print(f"     - {subfolder.GetName()}")
        sys.exit(1)
    
    print(f"✅ Found CJU_SE bin")
    
    # ========================================
    # STEP 2: 기존 불필요한 폴더 삭제
    # ========================================
    print("\n🗑️  Deleting unnecessary folders...")
    
    folders_to_delete = []
    for subfolder in root_folder.GetSubFolderList():
        folder_name = subfolder.GetName()
        if folder_name in ["VIDEO", "AUDIO", "XML", "EDIT", "MISC"]:
            folders_to_delete.append(subfolder)
            print(f"   Marked for deletion: {folder_name}")
    
    if folders_to_delete:
        result = media_pool.DeleteFolders(folders_to_delete)
        print(f"   Deleted {len(folders_to_delete)} folders")
    else:
        print("   No folders to delete")
    
    # ========================================
    # STEP 3: CJU_SE 빈의 클립 분석
    # ========================================
    print("\n📊 Analyzing clips in CJU_SE...")
    
    clips = cju_folder.GetClipList()
    
    if not clips:
        print("⚠️  No clips found in CJU_SE bin")
        sys.exit(0)
    
    print(f"   Total clips: {len(clips)}")
    
    # 확장자별 그룹화
    extension_groups = {}
    
    for clip in clips:
        clip_name = clip.GetClipProperty("File Name")
        if not clip_name:
            clip_name = clip.GetName()
        
        # 확장자 추출
        _, ext = os.path.splitext(clip_name)
        ext = ext.lower()  # 소문자로 변환
        
        if ext:
            # 확장자에서 점(.) 제거
            ext_clean = ext[1:] if ext.startswith('.') else ext
            
            # 첫 글자만 대문자, 나머지는 소문자 (예: mov -> Mov, xml -> Xml)
            folder_name = ext_clean.capitalize()
            
            if folder_name not in extension_groups:
                extension_groups[folder_name] = []
            
            extension_groups[folder_name].append({
                'clip': clip,
                'name': clip_name
            })
        else:
            print(f"   ⚠️  No extension: {clip_name}")
    
    print(f"\n   Found {len(extension_groups)} unique extensions:")
    for ext, clips_list in sorted(extension_groups.items()):
        print(f"      .{ext.lower()}: {len(clips_list)} files")
    
    # ========================================
    # STEP 4: 확장자별 폴더 생성 및 클립 이동
    # ========================================
    print("\n📁 Creating folders and moving clips...")
    
    moved_total = 0
    
    for folder_name, clips_data in sorted(extension_groups.items()):
        # 폴더가 이미 존재하는지 확인
        existing_folder = None
        for subfolder in root_folder.GetSubFolderList():
            if subfolder.GetName() == folder_name:
                existing_folder = subfolder
                break
        
        # 폴더가 없으면 생성
        if not existing_folder:
            new_folder = media_pool.AddSubFolder(root_folder, folder_name)
            print(f"   ✅ Created folder: {folder_name}/")
            target_folder = new_folder
        else:
            print(f"   📂 Folder exists: {folder_name}/")
            target_folder = existing_folder
        
        # 클립 이동
        if target_folder:
            clips_to_move = [item['clip'] for item in clips_data]
            result = media_pool.MoveClips(clips_to_move, target_folder)
            
            if result:
                print(f"      ➜ Moved {len(clips_to_move)} clips")
                moved_total += len(clips_to_move)
            else:
                print(f"      ⚠️  Failed to move clips")
    
    # ========================================
    # STEP 5: CJU_SE 빈 확인 및 삭제
    # ========================================
    print("\n🧹 Cleaning up...")
    
    remaining_clips = cju_folder.GetClipList()
    remaining_count = len(remaining_clips) if remaining_clips else 0
    
    if remaining_count == 0:
        print(f"   CJU_SE bin is empty")
        delete_result = media_pool.DeleteFolders([cju_folder])
        if delete_result:
            print(f"   ✅ Deleted empty CJU_SE bin")
        else:
            print(f"   ⚠️  Could not delete CJU_SE bin")
    else:
        print(f"   ⚠️  {remaining_count} clips remaining in CJU_SE")
    
    # ========================================
    # STEP 6: 최종 결과 출력
    # ========================================
    print("\n" + "="*50)
    print("📋 FINAL MEDIA POOL STRUCTURE")
    print("="*50)
    
    total_clips_final = 0
    for subfolder in sorted(root_folder.GetSubFolderList(), key=lambda x: x.GetName()):
        folder_name = subfolder.GetName()
        folder_clips = subfolder.GetClipList()
        clip_count = len(folder_clips) if folder_clips else 0
        total_clips_final += clip_count
        
        print(f"  📁 {folder_name}/ ({clip_count} clips)")
    
    print("="*50)
    print(f"✅ Organization complete!")
    print(f"   Total clips organized: {moved_total}")
    print(f"   Total clips in media pool: {total_clips_final}")
    print("="*50)

except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
