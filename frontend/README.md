# React + TypeScript + Vite + shadcn/ui

This is a template for a new Vite project with React, TypeScript, and shadcn/ui.

## Adding components

To add components to your app, run the following command:

```bash
pnpm dlx shadcn@latest add @boldkit/button
```

The project uses the BOLDkit registry (`@boldkit` in `components.json`), not the default shadcn catalog. Components land in `src/components/ui`.

## Using components

To use the components in your app, import them as follows:

```tsx
import { Button } from "@/components/ui/button"
```
