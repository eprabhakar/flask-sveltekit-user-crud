import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
  // Call backend to fetch session
  const res = await fetch('http://localhost:5000/me', {
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
