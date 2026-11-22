# Web

Next.js frontend for the ChatGPT clone (TypeScript 7, Tailwind CSS, shadcn/ui with Radix). Structure and rules: see the root [`AGENTS.md`](../../AGENTS.md).

## Setup

```sh
cd apps/web
pnpm install
```

## Commands (run inside `apps/web`)

| Task                          | Command          |
| ----------------------------- | ---------------- |
| Dev server                    | `pnpm dev`       |
| Lint and format check (Biome) | `pnpm lint`      |
| Fix formatting                | `pnpm format`    |
| Type check (TypeScript 7)     | `pnpm typecheck` |
| Production build              | `pnpm build`     |

The dev server runs on http://localhost:3000.

## Notes

- **Biome instead of ESLint:** ESLint's TypeScript parser needs the TypeScript JavaScript API, which TypeScript 7 does not ship until 7.1. Biome does not depend on it.
- **UI components:** add shadcn/ui components with `pnpm dlx shadcn@latest add <name>`. They land in `src/components/ui/`.
