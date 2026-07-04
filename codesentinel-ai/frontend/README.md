# CodeSentinel Frontend

This is the Next.js UI for CodeSentinel AI. It provides the pull-request review form, history view, and detailed review display.

## Development

```bash
npm install
cp .env.example .env.local
npm run dev
```

Open http://localhost:3000 to view the app.

## What the UI supports

- Submit a repository and PR number for review
- Optionally send a storage key, GitHub token, and Groq API key with the request
- Browse past reviews by storage key
- Open review details and delete history items

## Environment

Set NEXT_PUBLIC_API_BASE_URL in .env.local to point at the backend API, for example:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```

## Build

```bash
npm run build
```
