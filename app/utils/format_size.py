def format_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    units = ["B", "KB", "MB", "GB", "TB"]
    idx = 0
    while size_bytes >= 1024 and idx < len(units) - 1:
        size_bytes /= 1024
        idx += 1
    return f"{size_bytes:.2f}{units[idx]}"