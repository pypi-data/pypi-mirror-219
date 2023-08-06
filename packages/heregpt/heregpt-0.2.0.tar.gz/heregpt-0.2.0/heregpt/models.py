from pydantic import BaseModel


class TaskBase(BaseModel):
    tool: str
    task: str
    prompt: str | None = None

    def build_prompt(self):
        self.prompt = f"""Using the tool `{self.tool}` give a single
 suggestion without explanations in a code block format that will
 execute the task sourrounded by three backticks:
```
{self.task}
```
The result should be provided in a YAML with the following format:

tool:
    specify the tool {self.tool}
task:
    specify the task {self.task}
suggested_command:
    place here the result
"""
