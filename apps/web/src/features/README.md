# Features

One folder per feature, named the same as its backend feature in `apps/api/src/app/features/`.

Each feature folder holds its own:

- `components/`: React components for this feature
- `hooks/`: React hooks for this feature
- `api.ts`: calls to the backend for this feature
- `types.ts`: types for this feature

Routes in `src/app/` stay thin and import from here.

Planned: `chat/` and `conversations/` (Phase 1), `auth/` (Phase 2).
