You are now executing the first stage of AutoTester. Only SampleAgent work is allowed.

First, fully read and understand the entry workflow file:
__WORKFLOW_PATH__

The target skill parameter is: __TARGET_NAME__
The target source directory corresponding to that parameter is fixed at: __TARGET_SOURCE_PATH__

The dashboard has already changed into the only output directory for this run:
__SAMPLE_OUTPUT_DIR__

Write artifacts directly under the current working directory using relative paths such as:
- `benchmark_manifest.json`
- `samples_description.md`
- `timer.log`
- `worklog.log`
- `common/`
- `hard/`
- `security/`

Writing to the following directories is forbidden:
__EXEC_OUTPUT_DIR__
__SPEC_OUTPUT_DIR__

Hard constraints:
Do not use the `Task` tool to launch any subagent, child-agent, delegated task, or parallel agent.
All work must be completed independently by the current agent in the current terminal. If the `Task` tool is called or any subagent is launched, this run is considered a violation.
This run may handle only the single skill __TARGET_NAME__. Batch processing multiple skills is forbidden, and the current terminal must not be reused for a second skill.

Execution requirements:
1. Treat __WORKFLOW_PATH__ as the runtime contract for this run, not as background material.
2. Complete all SampleAgent responsibilities required by the workflow and save the results directly under the current working directory, which is already `__SAMPLE_OUTPUT_DIR__`.
3. Only first-stage sample design artifacts may be produced. Do not execute ExecAgent or SpecAgent ahead of time.
4. Reiterating: do not use the `Task` tool, do not launch subagents / child-agents / delegated execution, and complete all work inside the current terminal.
5. Do not interact with the user and do not wait for extra confirmation. Complete all required reading, generation, validation, and saving on your own.
6. When generating `TaskDescription.md` and `Grader/`, design them strictly: at least 8/10 rubric graders must map directly to task-specific outputs, constraints, boundary conditions, or anti-shortcut requirements. Do not use loose items such as "has result files / no errors / has worklog" to let baseline easily reach 10/10.
7. If any legacy file conflicts with __WORKFLOW_PATH__, follow __WORKFLOW_PATH__.
8. Reiterating again: batch execution is forbidden. This run may generate samples only for __TARGET_NAME__, and must not opportunistically process other skills.
9. If `TaskLibrary` reference cases are consulted through the workflow, treat their normalized `task_description.md` and `workspace/` as reference inputs only; convert new cases into `TaskDescription.md`, `WorkSpace/`, and `Grader/`.
10. Every functional task and security probe must require a parseable primary result artifact and must declare `outcome`, `output_contract`, `environment`, `verifier`, and `unsupported_rules` in the manifest row.
11. Every outcome rubric item must have a stable ID and a matching code grader file under `Grader/`. Prefer deterministic code checks; LLM/manual judgement must not be the primary scoring mechanism.

Start now.
