import shutil
from pathlib import Path

from app.components.base_rule import BaseRule


class RuleHandler(BaseRule):
    def execute(self, context):
        temp_dir = context.get('data', {}).get('fetch_code', {}).get('repository_path')

        if temp_dir:
            temp_dir_path = Path(temp_dir)
            if temp_dir_path.exists() and temp_dir_path.is_dir():
                try:
                    shutil.rmtree(temp_dir_path)
                    print(
                        f"[Clean] Deleted tmp dir: {temp_dir}"
                    )
                    context['data']['cleanup_temp_dir'] = {'status': True}
                except Exception as e:
                    print(
                        f"[Clean] Error deleting tmp {temp_dir}: {str(e)}"
                    )
                    context['data']['cleanup_temp_dir'] = {
                        'status': False,
                        'error': str(e)
                    }
            else:
                print(f"[Clean] Directory does not exist: {temp_dir}")
                context['data']['cleanup_temp_dir'] = {
                    'status': False,
                    'error': "Directory not found."
                }
        else:
            print("[Clean] No temporary directory found in context.")
            context['data']['cleanup_temp_dir'] = {
                'status': False,
                'error': "No temp directory found in context."
            }

        return context
