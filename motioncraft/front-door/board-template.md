# The reference board: `Planning/<slug>/board.md`

One board per piece, built after the ten points are locked and before the first render (SWCB #267, lock 5). It is where a reference becomes a row a prompt can draw from and a gate can read: not "like Studio Ghibli" but which film, which shot, and which one thing of it is borrowed. The borrowed-what is always one of the lens's words: **timing, palette, staging, line, texture, shape language, motion**. One row may borrow two things; it then says both, each its own word.

## Shape

```markdown
# Board: <piece> (<slug>, <date>)

## Borrowed

| id | work | link | borrowed | not borrowed | Sean's line |
|---|---|---|---|---|---|
| B1 | <the work: a Cosmos tile, a film and its shot, a print, a YouTube video and its timestamp> | <URL, or the path of Sean's own file> | <one of: timing, palette, staging, line, texture, shape language, motion; what exactly, in a phrase> | <what of this work the piece must not take> | "<his words, verbatim>" |

## Negatives

| id | what | why wrong | source |
|---|---|---|---|
| N1 | <a rejected look, an earlier version, a reference that went the wrong way> | "<what Sean named wrong, verbatim>" | <the approvals id (mc-ap-NNN) for an earlier version; a link or a path otherwise> |
```

## Rules

- **A row is one work, one link.** A reference Sean names in a category ("those Soviet posters") becomes a row only once one poster is named and linked; until then it is an open question in the sidecar.
- **The link is the row.** A copy of someone else's work never enters the folder, a repo, an issue or the ledger. A YouTube video is broken down with the `watch` skill in the room (its frames read, the timing counted, the borrowed-what named) and the row keeps the link and the timestamp; the frames the skill pulled are deleted when the row is written.
- **Thumbnails for Sean's eye only.** When the room shows the board, it may fetch a thumbnail beside each row for the conversation. They go nowhere: not into `Planning/`, not into the sidecar. Sean's own work (a frame from an earlier film, a print he made) is the exception and may sit in `look/`, named as his.
- **To ChatGPT desktop as references:** only rows whose work is Sean's own; every other row crosses as its link and its borrowed-what in words. (Default from the build session, until Sean rules otherwise.)
- **The negatives carry his words.** What he named wrong is the lesson; the room never paraphrases it into a rule.
- **Two pieces, one row: offer the library.** A work cited on a second piece is offered, in that sitting, for a standing reference library under `Planning/library/board.md` in the media root, kept to the same shape. On his yes the row is copied there with both pieces named; the piece's board still carries its own row.
- **The board binds through the brief.** `brief-draft.md`'s *What good looks like* names the rows that bind by id (`B1`, `B3`); a row not named there is context for the room and nothing the studio is held to.
