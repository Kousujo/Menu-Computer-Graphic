# dump_code.py
import os

# Các thư mục hoặc file cần bỏ qua để tránh rác
IGNORE_DIRS = {'__pycache__', '.pytest_cache', '.git', 'build', 'dist', 'asset'}
IGNORE_FILES = {'dump_code.py', '.gitignore'}

def main():
    output_file = "all_source_code.txt"
    with open(output_file, "w", encoding="utf-8") as outfile:
        for root, dirs, files in os.walk('.'):
            # Loại bỏ các thư mục ẩn/rác
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for file in files:
                if file in IGNORE_FILES or not file.endswith('.py'):
                    continue
                    
                relative_path = os.path.join(root, file)
                outfile.write(f"\n{'='*50}\n")
                outfile.write(f"FILE PATH: {relative_path}\n")
                outfile.write(f"{'='*50}\n\n")
                
                try:
                    with open(relative_path, "r", encoding="utf-8") as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"Lỗi đọc file: {e}\n")
                    
    print(f"Đã gom toàn bộ code vào file: {output_file}")

if __name__ == "__main__":
    main()