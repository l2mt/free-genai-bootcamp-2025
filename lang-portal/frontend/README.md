# Language Learning Portal Frontend

A modern web application built with React, TypeScript, and Tailwind CSS for the Language Learning Portal.

## Tech Stack

- React 18
- TypeScript
- Vite
- Tailwind CSS
- React Router DOM
- Radix UI Components
- ESLint for code quality

## Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Git

## Getting Started

1. Clone the repository:
```bash
git clone <repository-url>
cd lang-portal/frontend
```

2. Install dependencies:
```bash
npm install
# OR
yarn install
```

3. Start the development server:
```bash
npm run dev
# OR
yarn dev
```

The application will be available at `http://localhost:5173`

## Available Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build the application for production
- `npm run preview` - Preview the production build locally
- `npm run lint` - Run ESLint to check code quality

## Project Structure

```
frontend/
├── src/                    # Source files
│   ├── components/        # Reusable React components
│   ├── contexts/         # React Context providers
│   ├── pages/            # Page components
│   ├── services/         # API services
│   ├── types/            # TypeScript type definitions
│   ├── utils/            # Utility functions
│   ├── App.tsx          # Root component
│   └── main.tsx         # Entry point
├── public/               # Static files
├── index.html           # HTML template
├── tailwind.config.js   # Tailwind CSS configuration
├── vite.config.ts       # Vite configuration
├── tsconfig.json        # TypeScript configuration
├── package.json         # Project dependencies and scripts
└── README.md           # This file
```

## Development Guidelines

1. **Code Style**
   - Follow TypeScript best practices
   - Use functional components with hooks
   - Implement proper type definitions
   - Follow ESLint rules

2. **Component Structure**
   - Keep components small and focused
   - Use composition over inheritance
   - Implement proper prop types
   - Use Tailwind CSS for styling

3. **State Management**
   - Use React Context for global state
   - Keep component state local when possible
   - Implement proper error boundaries

4. **Performance**
   - Implement proper memoization (useMemo, useCallback)
   - Optimize re-renders
   - Use proper lazy loading for routes

## Environment Variables

Create a `.env` file in the root directory:

```env
VITE_API_URL=http://localhost:8000  # Backend API URL
```

## Building for Production

1. Create the production build:
```bash
npm run build
# OR
yarn build
```

2. Preview the production build:
```bash
npm run preview
# OR
yarn preview
```

## Common Issues

1. **Node Modules Issues**
   ```bash
   rm -rf node_modules
   rm package-lock.json
   npm install
   ```

2. **TypeScript Errors**
   - Make sure all dependencies are properly typed
   - Check `tsconfig.json` settings
   - Run `tsc` to verify type checking

3. **Vite Build Issues**
   - Clear the dist folder
   - Verify environment variables
   - Check for circular dependencies

## Browser Support

The application supports all modern browsers:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Create a new branch for your feature
2. Follow the code style guidelines
3. Write clear commit messages
4. Submit a pull request

## License

This project is private and confidential.
