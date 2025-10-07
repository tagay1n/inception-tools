from pycaprio import Pycaprio
from pycaprio.core.mappings import InceptionFormat, DocumentState
from io import BytesIO

inception_host = <<SET ME>>
remote_creds = (<<SET ME>>, <<SET ME>>)

main_project = (
    "error-annotation",
    "📝【ХАТАЛАРНЫ ТАМГАЛАУ】",
)

sandbox_project = (
    "error-annotation-sandbox",
    "🏖️ Комлык",
    'tat-constitution.txt'
)

def main():
    client = Pycaprio(inception_host, remote_creds)

    # client.api.export_project("grammar-error-annotation-sandbox")
    current_projects = {p.project_name: p for p in client.api.projects()}
    print("Current projects:", current_projects.keys())
    init_sandbox(client, current_projects)
    init_main(client, current_projects)

    
def init_sandbox(client, projects):
    if not (project := projects.get(sandbox_project[0])):
        print("Creating sandbox project...")
        project = client.api.create_project(
            project_name=sandbox_project[0],
            project_title=sandbox_project[1],
        )
    doc_names = [d.document_name for d in client.api.documents(project)]
    if sandbox_project[0] not in doc_names:
        print("Creating sandbox document...")
        with open(sandbox_project[2], 'rb') as f:
            client.api.create_document(
                project,
                document_name="default", 
                document_format=InceptionFormat.TEXT,
                document_state=DocumentState.NEW, 
                content=BytesIO(f.read())
            )
            
    projects[sandbox_project[0]] = project
        
def init_main(client, projects):
    if not (project := projects.get(main_project[0])):
        print("Creating main project...")
        project = client.api.create_project(
            project_name=main_project[0],
            project_title=main_project[1],
        )
    projects[sandbox_project[0]] = project


if __name__ == "__main__":
    main()