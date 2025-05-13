## Features

The **“Tapetenputzer”** Discord bot provides a single slash command (`/start`) that, when invoked, will:

1. **Send Direct Messages (DMs) to Every Member**  
   - Delivers the user-provided message to each non-bot member via DM.  
   - Logs successes and failures to the console for each attempt.

2. **Rename All Members**  
   - Changes the nickname of every non-bot member to **“nuked by tapetenputzer”**.  
   - Outputs debug information and errors in the console.

3. **Delete All Channels**  
   - Iterates through every channel (text, voice, announcement, etc.) and deletes them with a 0.5 s throttle.  
   - Logs each deletion or error.

4. **Delete All Categories**  
   - Removes all category objects in the guild, pausing 0.5 s between deletions.

5. **Delete All Roles**  
   - Deletes all roles except the default `@everyone` role, with a 0.5 s delay between each.

6. **Delete Custom Emojis & Stickers**  
   - Removes every custom emoji and sticker on the server, throttled at 0.5 s per deletion.

7. **Revoke All Invite Links**  
   - Fetches all active invites and deletes each one, waiting 0.5 s between operations.

8. **Remove All Webhooks**  
   - Iterates through each text channel, deletes any webhooks found, and logs the outcome with a 0.5 s throttle.

9. **Create Spam Channels & Spam Loop**  
   - Creates **20** new text channels named `Tapetenputzer-1` through `Tapetenputzer-20`, each created with a 0.5 s pause.  
   - Starts a background task that posts the provided message once per second in each newly created channel indefinitely.  
   - Logs every message sent or error encountered.

10. **Extensive Console Debugging**  
    - Uses `print` statements for every step to trace operations, successes, and failures in real time.

---

> **⚠️ WARNING:** This bot performs irreversible, destructive actions on your server.  
> **Use only in isolated test environments.** Deploying it on production or unfamiliar servers can cause permanent data loss!  
