# Changelog

## v1.4.0 - December 2025

### New Features
- **Suuktest Folder Management**: Added comprehensive tools for managing Suuktest folder structure (`/Users/Shared/suuktest`)
  - `suuktest_scan_structure`: Scan and analyze folder structure with file counts and sizes
  - `suuktest_import_folder`: Import entire project folders with automatic organization
  - `suuktest_import_all_xmls`: Batch import XML/AAF/EDL timelines
  - `suuktest_find_media_files`: Search for media files with filters
  - `suuktest_relink_clips`: Automatically relink offline clips
  - `suuktest_list_projects`: List all projects in Suuktest folder
- **Enhanced XML Timeline Import**: Advanced XML/AAF/EDL timeline import capabilities
  - `import_timeline_from_file`: Import single timeline with metadata
  - `import_all_xml_from_folder`: Batch import timelines from folder
- **Media Pool Management**: New tools for media pool operations
  - `get_clips_in_bin`: Get detailed clip information from bins
  - `get_media_pool_structure`: View complete media pool structure
  - `create_timeline_from_bin_clips`: Create timelines from bin clips
  - `relink_offline_clips`: Advanced offline clip relinking

### Improvements
- Merged github-upload features into main MCP server
- Added support for multiple file formats (video, audio, image, timeline)
- Enhanced error handling and validation
- Improved folder structure navigation

## v1.3.8 - April 2025

### Improvements
- **Cursor Integration**: Added comprehensive documentation for Cursor setup process
- **Entry Point**: Standardized on `main.py` as the proper entry point (replaces direct use of `resolve_mcp_server.py`)
- **Configuration Templates**: Updated example configuration files to use correct paths
- **Documentation**: Added detailed troubleshooting for "client closed" errors in Cursor

### Fixed
- Ensured consistent documentation for environment setup

## v1.3.7 - Installation Improvements, Path Resolution Fixes, Enhanced Configuration

### Improvements
// ... existing content ... 