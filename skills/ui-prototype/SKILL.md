---
name: ui-prototype
description: Creates UI prototypes using NextJS, React, TypeScript, Tailwind CSS, and shadcn/ui. Use when users describe a UI they want to build, attach mockups, or ask to prototype a web interface. Scaffolds a full working project from a template with all shadcn components pre-installed.
---

# UI Prototype

Create fully functional UI prototypes from descriptions or mockups using NextJS, React, TypeScript, Tailwind CSS, and shadcn/ui.

## Overview

This skill scaffolds a new NextJS project from a pre-configured template that includes all shadcn/ui components, Tailwind CSS v4, Biome for linting/formatting, and common utilities. The prototype is intended to showcase a complete UI use case with realistic mock data and multiple routes as needed.

## Template Location

The template is located at `<skill_path>/template/`. It includes:

- NextJS 16 with App Router and React Server Components
- All shadcn/ui components pre-installed in `src/components/ui/`
- Tailwind CSS v4 with CSS variables for theming (light/dark mode)
- Biome for linting and formatting
- Lucide React for icons
- Recharts for data visualization
- Additional libraries: date-fns, embla-carousel-react, cmdk, vaul, sonner, react-day-picker, react-resizable-panels, next-themes

## How to Create a Prototype

### Step 1: Determine the Project Name

- Derive the name from the user's description (e.g., "task manager" becomes `task-manager`)
- If the name is ambiguous, ask the user what to call the project
- Use kebab-case for the project directory name

### Step 2: Scaffold the Project

Copy the template to a new directory. The project should be created next to the template directory or in the user's preferred location.

```bash
# Copy template (exclude .git and node_modules)
rsync -a --exclude='.git' --exclude='node_modules' --exclude='.next' <skill_path>/template/ <target_path>/
```

### Step 3: Install Dependencies

```bash
cd <target_path>

# Enable corepack if pnpm is not available
command -v pnpm >/dev/null 2>&1 || corepack enable

pnpm install
```

### Step 4: Update package.json

Update the `name` field in `package.json` to match the project name.

### Step 5: Build the Prototype UI

Follow these conventions when creating the prototype:

#### File Naming
- Use lowercase kebab-case for all files: `some-component.tsx`, `user-profile.tsx`
- Page routes follow NextJS App Router conventions: `src/app/route-name/page.tsx`

#### Code Style
- Prefer `const` declarations over `function`:
  ```tsx
  const MyComponent = () => (
    <div>Content</div>
  );
  ```
- Use type imports when possible:
  ```tsx
  import type { ReactNode } from "react";
  ```
- Use the `cn()` utility from `@/lib/utils` for conditional class names
- Use shadcn/ui components from `@/components/ui/` for all UI elements
- Use Lucide React for icons

#### Project Structure
- `src/app/` — NextJS pages and layouts (App Router)
- `src/components/` — Custom components for the prototype
- `src/components/ui/` — shadcn/ui components (pre-installed, do not modify)
- `src/data/` — Mock data files
- `src/lib/` — Utility functions
- `src/hooks/` — Custom React hooks

#### Mock Data
- Create mock data files in `src/data/` (e.g., `src/data/users.ts`, `src/data/products.ts`)
- Export typed arrays/objects with realistic sample data
- Use TypeScript interfaces/types for the data shapes

#### Simulating Backend Calls
- Use NextJS Server Components (default in App Router) to return mock data
- For dynamic data, use Server Actions or Route Handlers when it makes sense
- Example pattern for a server-side data fetch:
  ```tsx
  // src/data/products.ts
  export type Product = {
    id: string;
    name: string;
    price: number;
  };

  export const products: Product[] = [
    { id: "1", name: "Widget", price: 9.99 },
    // ...
  ];
  ```
  ```tsx
  // src/app/products/page.tsx
  import { products } from "@/data/products";

  const ProductsPage = () => (
    <div>
      {products.map(product => (
        <div key={product.id}>{product.name}</div>
      ))}
    </div>
  );

  export default ProductsPage;
  ```

#### Multiple Routes
- Create separate routes to showcase different parts of the user interaction
- Use a shared layout with navigation between routes
- Example structure:
  ```
  src/app/
  ├── layout.tsx          # Root layout with navigation
  ├── page.tsx            # Dashboard / home
  ├── items/
  │   ├── page.tsx        # List view
  │   └── [id]/
  │       └── page.tsx    # Detail view
  └── settings/
      └── page.tsx        # Settings page
  ```

### Step 6: Verify the Build

```bash
cd <target_path>
pnpm typecheck
pnpm build
```

Fix any TypeScript or build errors before proceeding.

### Step 7: Update README.md

Replace the template README with a description of the prototype:

```markdown
# Project Name

Brief description of what this prototype demonstrates.

## Getting Started

### Prerequisites
- Node.js (see `.node-version`)
- pnpm (managed via corepack)

### Development
\```bash
corepack enable
pnpm install
pnpm dev
\```

Open [http://localhost:3000](http://localhost:3000).

### Scripts
- `pnpm dev` — Start development server
- `pnpm build` — Build for production
- `pnpm start` — Start production server
- `pnpm typecheck` — Run TypeScript type checking
- `pnpm lint` — Check code with Biome
- `pnpm lint:fix` — Auto-fix lint issues

## Tech Stack
- NextJS 16 (App Router)
- React 19
- TypeScript
- Tailwind CSS v4
- shadcn/ui
```

### Step 8: Create CLAUDE.md

Create a `CLAUDE.md` file in the project root documenting:

- The project purpose and what it prototypes
- Key files and their roles
- The routes/pages available
- Data models used
- Any important patterns or decisions made

Example:
```markdown
# Project Name

## Overview
Brief description of the prototype.

## Structure
- `src/app/` — Pages and layouts
- `src/components/` — Custom prototype components
- `src/data/` — Mock data

## Routes
- `/` — Home/dashboard
- `/items` — List view
- `/items/[id]` — Detail view

## Data Models
- `Item` — { id, name, description, status }

## Conventions
- Uses shadcn/ui components for all UI elements
- Mock data in src/data/ simulates backend responses
- Server Components used by default for data fetching
```

## Available shadcn/ui Components

All of these are pre-installed and ready to import from `@/components/ui/`:

accordion, alert, alert-dialog, aspect-ratio, avatar, badge, breadcrumb, button, button-group, calendar, card, carousel, chart, checkbox, collapsible, combobox, command, context-menu, dialog, direction, drawer, dropdown-menu, empty, field, hover-card, input, input-group, input-otp, item, kbd, label, menubar, native-select, navigation-menu, pagination, popover, progress, radio-group, resizable, scroll-area, select, separator, sheet, sidebar, skeleton, slider, sonner, spinner, switch, table, tabs, textarea, toggle, toggle-group, tooltip

## Important Notes

- The template uses Tailwind CSS v4 with `@theme inline` for CSS variable-based theming
- Components use `@base-ui/react` primitives under the hood
- The `TooltipProvider` is already set up in the root layout
- Biome is configured for linting and formatting — run `pnpm lint:fix` before finalizing
- The project uses `verbatimModuleSyntax` in tsconfig, so type imports are required
