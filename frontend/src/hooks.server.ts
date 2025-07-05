import type { Handle } from '@sveltejs/kit';
// const apiBase = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000';
import { env } from '$env/dynamic/private';
console.log(env.API_BASE_URL);
export const handle: Handle = async ({ event, resolve }) => {
  // Call backend to fetch session

  const apiBase = env.API_BASE_URL;
  console.log(apiBase);
  if (event.url.pathname.startsWith('/api/')) {
    // Don't fetch /api/me for /api requests → prevent loop
    return resolve(event);
  }

  const res = await event.fetch(`http://127.0.0.1:5000/me`, {
    credentials: 'include',
    headers: {
      cookie: event.request.headers.get('cookie') || ''
    }
  });

  if (res.ok) {
    const user = await res.json();
    event.locals.user = user?.id ? user : null;
  } else {
    event.locals.user = null;
  }

  const response = await resolve(event);
  return response;
};
