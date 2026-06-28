import os
import shutil
import csv
from datetime import datetime


# ─────────────────────────────────────────
#  File Category Mapping
# ─────────────────────────────────────────
CATEGORIES = {
    "Images"    : [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "Documents" : [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".csv"],
    "Videos"    : [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
    "Audio"     : [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma", ".m4a"],
    "Archives"  : [".zip", ".rar", ".tar", ".gz", ".7z", ".bz2"],
    "Programs"  : [".exe", ".msi", ".bat", ".sh", ".py", ".apk", ".deb"],
}


# ─────────────────────────────────────────
#  Helper: get category for a file
# ─────────────────────────────────────────
def get_category(filename):
    ext = os.path.splitext(filename)[1].lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"


# ─────────────────────────────────────────
#  Helper: simple progress bar
# ─────────────────────────────────────────
def show_progress(current, total, label="Progress"):
    percent = int((current / total) * 100)
    bar     = "#" * (percent // 5) + "-" * (20 - percent // 5)
    print(f"\r  {label}: [{bar}] {percent}%", end="", flush=True)
    if current == total:
        print()


# ─────────────────────────────────────────
#  Module 1: Directory Selection
# ─────────────────────────────────────────
def select_directory():
    print("\n--- Select Directory ---")
    path = input("Enter Folder Path: ").strip()

    if not path:
        print("⚠  No path entered.")
        return None

    if not os.path.exists(path):
        print("⚠  Error: Folder does not exist. Please check the path.")
        return None

    if not os.path.isdir(path):
        print("⚠  Error: The given path is not a folder.")
        return None

    print(f"✔  Folder found: {path}")
    return path


# ─────────────────────────────────────────
#  Module 2: File Scanning
# ─────────────────────────────────────────
def scan_files(folder_path):
    print("\n--- Scanning Files ---")
    try:
        all_items = os.listdir(folder_path)
        files     = [f for f in all_items if os.path.isfile(os.path.join(folder_path, f))]

        if not files:
            print("  No files found in the selected folder.")
            return []

        print(f"  Found {len(files)} File(s)\n")
        print(f"  {'File Name':<35} {'Extension'}")
        print("  " + "-" * 50)
        for f in files:
            ext = os.path.splitext(f)[1] or "No Extension"
            print(f"  {f:<35} {ext}")

        return files

    except PermissionError:
        print("⚠  Permission Denied: Cannot access this folder.")
        return []
    except Exception as e:
        print(f"⚠  Unexpected error while scanning: {e}")
        return []


# ─────────────────────────────────────────
#  Module 3: Automatic File Organization
# ─────────────────────────────────────────
def organize_files(folder_path, files):
    print("\n--- Organizing Files ---")
    if not files:
        print("  No files to organize.")
        return {}

    moved_summary = {cat: [] for cat in list(CATEGORIES.keys()) + ["Others"]}
    total         = len(files)

    for i, filename in enumerate(files, 1):
        show_progress(i, total, "Organizing")

        category   = get_category(filename)
        target_dir = os.path.join(folder_path, category)

        try:
            os.makedirs(target_dir, exist_ok=True)

            src = os.path.join(folder_path, filename)
            dst = os.path.join(target_dir, filename)

            if os.path.exists(dst):
                base, ext = os.path.splitext(filename)
                dst = os.path.join(target_dir, f"{base}_copy{ext}")

            shutil.move(src, dst)
            moved_summary[category].append(filename)

        except PermissionError:
            print(f"\n  ⚠  Permission denied for: {filename}")
        except FileNotFoundError:
            print(f"\n  ⚠  File not found: {filename}")
        except Exception as e:
            print(f"\n  ⚠  Could not move {filename}: {e}")

    print("\n✔  Files organized successfully!\n")
    print(f"  {'Category':<15} {'Files Moved'}")
    print("  " + "-" * 30)
    for cat, moved in moved_summary.items():
        if moved:
            print(f"  {cat:<15} {len(moved)}")

    return moved_summary


# ─────────────────────────────────────────
#  Module 4: File Statistics
# ─────────────────────────────────────────
def file_statistics(folder_path):
    print("\n--- File Statistics ---")
    try:
        stats      = {cat: 0 for cat in list(CATEGORIES.keys()) + ["Others"]}
        total      = 0
        all_items  = os.listdir(folder_path)

        for item in all_items:
            full_path = os.path.join(folder_path, item)
            if os.path.isfile(full_path):
                cat         = get_category(item)
                stats[cat] += 1
                total      += 1

        print(f"\n  {'Category':<15} {'Count'}")
        print("  " + "-" * 25)
        for cat, count in stats.items():
            print(f"  {cat:<15} {count}")
        print("  " + "-" * 25)
        print(f"  {'Total':<15} {total}")

    except PermissionError:
        print("⚠  Permission Denied.")
    except Exception as e:
        print(f"⚠  Error: {e}")


# ─────────────────────────────────────────
#  Module 5: Search Functionality
# ─────────────────────────────────────────
def search_files(folder_path):
    print("\n--- Search Files ---")
    print("1. Search by File Name")
    print("2. Search by Extension")
    choice = input("Choose option: ").strip()

    try:
        results = []
        for root, _, files in os.walk(folder_path):
            for f in files:
                if choice == "1":
                    keyword = input("Enter file name to search: ").strip().lower()
                    if keyword in f.lower():
                        results.append(os.path.join(root, f))
                    break
                elif choice == "2":
                    ext = input("Enter extension (e.g. .pdf): ").strip().lower()
                    for f2 in files:
                        if f2.lower().endswith(ext):
                            results.append(os.path.join(root, f2))
                    break
                else:
                    print("Invalid option.")
                    return

        if results:
            print(f"\n  Found {len(results)} result(s):")
            for r in results:
                print(f"  → {r}")
        else:
            print("  No matching files found.")

    except Exception as e:
        print(f"⚠  Search error: {e}")


# ─────────────────────────────────────────
#  Module 6: Duplicate File Detection
# ─────────────────────────────────────────
def detect_duplicates(folder_path):
    print("\n--- Duplicate File Detection ---")
    try:
        seen       = {}
        duplicates = []

        for root, _, files in os.walk(folder_path):
            for f in files:
                if f in seen:
                    duplicates.append(f)
                else:
                    seen[f] = True

        if duplicates:
            print(f"  Duplicate Files Found ({len(duplicates)}):")
            for d in duplicates:
                print(f"  → {d}")
        else:
            print("  No Duplicate Files Found.")

    except Exception as e:
        print(f"⚠  Error detecting duplicates: {e}")


# ─────────────────────────────────────────
#  Module 7: Generate Report
# ─────────────────────────────────────────
def generate_report(folder_path):
    print("\n--- Generating Report ---")
    try:
        report_path = os.path.join(folder_path, "file_report.txt")
        now         = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        folder_name = os.path.basename(folder_path)

        stats      = {cat: [] for cat in list(CATEGORIES.keys()) + ["Others"]}
        duplicates = []
        seen       = {}

        for root, dirs, files in os.walk(folder_path):
            # skip the organized category subfolders from stats
            for f in files:
                if f == "file_report.txt":
                    continue
                cat = get_category(f)
                stats[cat].append(f)
                if f in seen:
                    duplicates.append(f)
                else:
                    seen[f] = True

        total = sum(len(v) for v in stats.values())

        with open(report_path, "w", encoding="utf-8") as report:
            report.write("=" * 55 + "\n")
            report.write("          SMART FILE ORGANIZER - REPORT\n")
            report.write("=" * 55 + "\n")
            report.write(f"  Date        : {now}\n")
            report.write(f"  Folder Name : {folder_name}\n")
            report.write(f"  Folder Path : {folder_path}\n")
            report.write(f"  Total Files : {total}\n")
            report.write("\n--- Category-wise Count ---\n")
            for cat, files in stats.items():
                report.write(f"  {cat:<15}: {len(files)}\n")
            report.write("\n--- Duplicate Files ---\n")
            if duplicates:
                for d in duplicates:
                    report.write(f"  {d}\n")
            else:
                report.write("  No Duplicate Files Found.\n")
            report.write("\n--- Organized Folder Structure ---\n")
            for cat, files in stats.items():
                if files:
                    report.write(f"  {cat}/\n")
                    for f in files:
                        report.write(f"    --> {f}\n")
            report.write("=" * 55 + "\n")

        print(f"✔  Report saved to: {report_path}")

    except PermissionError:
        print("⚠  Permission Denied: Cannot write report.")
    except Exception as e:
        print(f"⚠  Error generating report: {e}")


# ─────────────────────────────────────────
#  Bonus: Export Report to CSV
# ─────────────────────────────────────────
def export_to_csv(folder_path):
    print("\n--- Exporting to CSV ---")
    try:
        csv_path = os.path.join(folder_path, "file_report.csv")
        rows     = []

        for root, _, files in os.walk(folder_path):
            for f in files:
                full  = os.path.join(root, f)
                size  = os.path.getsize(full)
                cat   = get_category(f)
                rows.append([f, cat, os.path.splitext(f)[1], size, full])

        with open(csv_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["File Name", "Category", "Extension", "Size (bytes)", "Path"])
            writer.writerows(rows)

        print(f"✔  CSV exported to: {csv_path}")

    except Exception as e:
        print(f"⚠  Error exporting CSV: {e}")


# ─────────────────────────────────────────
#  Bonus: Largest File Finder
# ─────────────────────────────────────────
def largest_file(folder_path):
    print("\n--- Largest File Finder ---")
    try:
        files = []
        for root, _, filenames in os.walk(folder_path):
            for f in filenames:
                full = os.path.join(root, f)
                files.append((f, os.path.getsize(full), full))

        if not files:
            print("  No files found.")
            return

        files.sort(key=lambda x: x[1], reverse=True)
        print(f"\n  Top 5 Largest Files:")
        print(f"  {'File Name':<30} {'Size (bytes)'}")
        print("  " + "-" * 50)
        for name, size, path in files[:5]:
            print(f"  {name:<30} {size}")

    except Exception as e:
        print(f"⚠  Error: {e}")


# ─────────────────────────────────────────
#  Bonus: Recently Modified Files
# ─────────────────────────────────────────
def recently_modified(folder_path):
    print("\n--- Recently Modified Files ---")
    try:
        files = []
        for root, _, filenames in os.walk(folder_path):
            for f in filenames:
                full  = os.path.join(root, f)
                mtime = os.path.getmtime(full)
                files.append((f, mtime))

        if not files:
            print("  No files found.")
            return

        files.sort(key=lambda x: x[1], reverse=True)
        print(f"\n  Top 5 Recently Modified Files:")
        print(f"  {'File Name':<35} {'Last Modified'}")
        print("  " + "-" * 60)
        for name, mtime in files[:5]:
            mod_time = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            print(f"  {name:<35} {mod_time}")

    except Exception as e:
        print(f"⚠  Error: {e}")


# ─────────────────────────────────────────
#  Bonus: Delete Empty Folders
# ─────────────────────────────────────────
def delete_empty_folders(folder_path):
    print("\n--- Delete Empty Folders ---")
    deleted = 0
    try:
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for d in dirs:
                full = os.path.join(root, d)
                if not os.listdir(full):
                    os.rmdir(full)
                    print(f"  Deleted empty folder: {full}")
                    deleted += 1

        if deleted == 0:
            print("  No empty folders found.")
        else:
            print(f"\n✔  {deleted} empty folder(s) deleted.")

    except PermissionError:
        print("⚠  Permission Denied.")
    except Exception as e:
        print(f"⚠  Error: {e}")


# ─────────────────────────────────────────
#  Main Menu
# ─────────────────────────────────────────
def main():
    folder_path = None

    while True:
        print("\n" + "=" * 45)
        print("        SMART FILE ORGANIZER")
        print("=" * 45)
        print("  1. Select Directory")
        print("  2. Scan Files")
        print("  3. Organize Files")
        print("  4. File Statistics")
        print("  5. Search Files")
        print("  6. Detect Duplicate Files")
        print("  7. Generate Report (TXT)")
        print("  8. Export Report to CSV")
        print("  9. Find Largest Files")
        print("  10. Recently Modified Files")
        print("  11. Delete Empty Folders")
        print("  0. Exit")
        print("=" * 45)

        if folder_path:
            print(f"  Active Folder: {folder_path}")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            folder_path = select_directory()

        elif choice in ["2","3","4","5","6","7","8","9","10","11"]:
            if not folder_path:
                print("⚠  Please select a directory first (Option 1).")
                continue

            if   choice == "2":
                scan_files(folder_path)
            elif choice == "3":
                files = scan_files(folder_path)
                organize_files(folder_path, files)
            elif choice == "4":
                file_statistics(folder_path)
            elif choice == "5":
                search_files(folder_path)
            elif choice == "6":
                detect_duplicates(folder_path)
            elif choice == "7":
                generate_report(folder_path)
            elif choice == "8":
                export_to_csv(folder_path)
            elif choice == "9":
                largest_file(folder_path)
            elif choice == "10":
                recently_modified(folder_path)
            elif choice == "11":
                delete_empty_folders(folder_path)

        elif choice == "0":
            print("\n  Exiting Smart File Organizer. Goodbye!")
            break

        else:
            print("  Invalid choice. Please try again.")


if __name__ == "__main__":
    main()