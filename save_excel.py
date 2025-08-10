import os
from openpyxl import Workbook
from openpyxl.styles import Font


def save_to_excel(metadata, track_data, output_path):
    """
    Save playlist metadata and track data to an Excel file.
    :param metadata: Dictionary with playlist metadata.
    :param track_data: List of dictionaries, each representing a track.
    :param output_path: Path to save the Excel file.
    """
    wb = Workbook()
    bold_font = Font(bold=True)

    # Create and populate the Tracks sheet
    ws_tracks = wb.active
    ws_tracks.title = "Tracks"
    if track_data:
        headers = list(track_data[0].keys())
        ws_tracks.append(headers)
        for cell in ws_tracks[1]:
            cell.font = bold_font
        for track in track_data:
            ws_tracks.append([track.get(h, "") for h in headers])

    # Create and populate the Metadata sheet
    ws_meta = wb.create_sheet("Metadata")
    ws_meta.append(["Field", "Value"])
    for cell in ws_meta[1]:
        cell.font = bold_font
    for k, v in metadata.items():
        ws_meta.append([k, v])

    # Ensure output directory exists and save the workbook
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wb.save(output_path)
    print(f"✅ Exported to: {output_path}")