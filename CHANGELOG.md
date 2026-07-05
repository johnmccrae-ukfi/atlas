0.1.0

Repository Created

Project Structure

PID

### Added

- Microsoft Fabric workspace connected to GitHub development branch
- Bronze Delta loading notebook
- Bronze metadata enhancements
    - source_file_name
    - source_file_path
    - source_file_row_number
    - event_sequence_in_file
    - source_provider
    - bronze_loaded_at_utc

### Changed

- Bronze layer now preserves complete source provenance and event ordering.
- Development workflow updated to use GitHub dev branch for both VS Code and Fabric.