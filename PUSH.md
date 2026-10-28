# Push to GitHub (do this once)

`gh` is not logged in on the agent box, and Cursor cannot mint a new public GitHub repo for you. Create an empty public repo, then push:

```bash
# on your machine (or after: gh auth login)
gh repo create ghost-in-the-machine --public --source=/workspace/ghost-in-the-machine --remote=origin --push
```

Or manually:

1. Create empty repo `ghost-in-the-machine` on GitHub (no README/license — we already have them).
2. Then:

```bash
cd /workspace/ghost-in-the-machine
git remote add origin git@github.com:pr7426/ghost-in-the-machine.git
# or: https://github.com/pr7426/ghost-in-the-machine.git
git push -u origin main
```

3. Replace `pr7426` / `pr7426` in `README.md` and `DEV_SUBMISSION.md` with your username, commit, push again.

4. Publish the DEV.to post from `DEV_SUBMISSION.md` (do not forget tags `#devchallenge` `#hf26challenge`). Deadline ~ Nov 1 14:59 Asia/Shanghai.
