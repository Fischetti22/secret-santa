# Secret Santa

A basic Streamlit Secret Santa draw for the family. Each person chooses their name once and receives one unique recipient, and can add gift ideas to their wishlist.

Pedro, Sydney, Selena, and Amelia cannot be matched with themselves or one another. The app also prevents every other self-match and duplicate recipient. Gifts should cost $65 or less.

## Run locally

```zsh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app stores the current draw in `assignments.json`. It is excluded from Git so nobody's assigned recipient is published. Delete that file to begin a new draw locally.

## Deploy with Streamlit Community Cloud

1. Push this project to GitHub.
2. In [Streamlit Community Cloud](https://share.streamlit.io/), create an app from the repository.
3. Use `app.py` as the entry point.
4. In the app's settings, add a secret named `ORGANIZER_PASSWORD` so only the organizer can reset the draw.

Streamlit Community Cloud's filesystem is not permanent, so assignments may reset when the app restarts or redeploys. For a real family draw, avoid restarting or redeploying the app until everyone has chosen. Persistent storage (such as a database) is needed to guarantee assignments survive restarts.
