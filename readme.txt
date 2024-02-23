> [!WARNING]
> This code is purely made for fun and don't take it seriously.  You might encounter some mysterious 404 Errors


- Error Handling: Encounter a 404? That's just the server telling you it's in another universe.

- Echo Functionality: Echo your innermost thoughts by navigating to `/echo/your_message_here`. Magic, right? (Spoiler: It's just string concatenation.) 

- Secret Files: Visit `/secret` to access a top-secret file.

- User-Agent Retrieval: Ever wondered what your User-Agent is?

    Find out by hitting up `/user-agent`. Spoiler: It's probably something like `"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36."`

> And so much more: Explore the server to discover mysterious 404 pages

# Usage

## Clone this repository.
```bash
git clone http://github.com/Rainax1/cursed-http.git
```

## Run the server with the following command:

```bash
python live-serve.py       # by default ip is 'localhosst' and port is 4222

python live-serve.py -f your_file.html -H 127.0.0.1 -p 4222    # specify host with -H and port with -p if wanted to change

# Visit the server in your web browser by navigating to http://127.0.0.1:4222.
```
TODO:

[ ] Add file serving 

[ ] Serve whole folder or a document file like pdf, html, xhtml, etc
