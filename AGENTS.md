# Assignment creation workflow

Keep each assignment independent and follow its README and local instructions. Student templates must leave scored functionality unimplemented and include their rubric, registration in `sync-assign.yml`, and checks for scored functionality.

1. Complete and commit the student template on `feat/add-assignment-<id>` without pushing.
2. Create a separate worktree from that commit at `worktrees/add-assignment-<id>` under the enclosing course workspace, on a branch named `staging/add-assignment-<id>`. Do not place solution worktrees in `/tmp`. Implement the solution only there. For notebooks, add solution cells after the implementation prompts and preserve supplied cells.
3. Use the activity's own virtual environment and dependencies. Run its documented checks and examples, including the complete notebook with the required dataset. Report results and any validation limitations.
4. Never commit or push the solution, or merge it into the student template. Leave solution changes uncommitted in the staging worktree for teacher review.
5. Delete the staging worktree only on the teacher's explicit command. Passing checks or approval of the assignment does not authorize deleting it.

Do not push assignment changes or merge them to main without the teacher's explicit approval.
