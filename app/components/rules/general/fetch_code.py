import git
import tempfile

from app.components.base_rule import BaseRule


class RuleHandler(BaseRule):
    def execute(self, context):
        inspection = context.get("inspection")
        if not inspection:
            raise ValueError("Inspection is missing in context.")

        project = inspection.project
        if not project:
            raise ValueError("No project associated with the inspection.")

        branch = inspection.branch
        url = project.url

        if not url:
            raise ValueError(
                f"Repository URL is missing for project '{project.name}'."
            )

        if not branch:
            raise ValueError(
                f"Branch is not defined for inspection ID {inspection.id}."
            )

        temp_dir = tempfile.mkdtemp()
        try:
            print(
                f"[fetch_code] Cloning {url} (b: {branch}) to {temp_dir}"
            )

            git.Repo.clone_from(url, temp_dir, branch=branch)

            context['data'] = context.get('data', {})
            context['data']['fetch_code'] = {
                'status': True,
                'repository_path': temp_dir
            }

        except Exception as e:
            raise ValueError(f"Failed to fetch code from repository: {str(e)}")

        return context
