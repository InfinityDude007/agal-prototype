from IPython.display import Markdown, display

def display_markdown_file(file_path: str):
    with open(file_path, 'r') as f:
        content = f.read()
    display(Markdown(content))

display_markdown_file('model_response.md')
