import os
import importlib
from django.apps import apps 

def import_all_view_modules(subfolder="views"):
    print("[AutoRouter] Start importing views...")
    for app_config in apps.get_app_configs():
        app_path = app_config.path
        app_name = app_config.name

        # استيراد views.py مباشرة
        single_file_path = os.path.join(app_path, f"{subfolder}.py")
        if os.path.isfile(single_file_path):
            module_path = f"{app_name}.{subfolder}"
            try:
                importlib.import_module(module_path)
                print(f"[AutoRouter] Imported file: {module_path}")
            except Exception as e:
                print(f"[AutoRouter] Failed to import file {module_path}: {e}")

        # استيراد ملفات مجلد views/
        folder_path = os.path.join(app_path, subfolder)
        if os.path.isdir(folder_path):
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith(".py") and not file.startswith("__"):
                        rel_path = os.path.relpath(os.path.join(root, file), app_path)
                        rel_path = rel_path.replace(os.sep, ".").replace(".py", "")
                        if rel_path.endswith(".__init__"):
                            rel_path = rel_path.replace(".__init__", "")
                        module_path = f"{app_name}.{rel_path}"
                        try:
                            importlib.import_module(module_path)
                            print(f"[AutoRouter] Imported module: {module_path}")
                        except Exception as e:
                            print(f"[AutoRouter] Failed to import module {module_path}: {e}")