// frontend/src/routes/+page.server.ts
import type { Actions, ServerLoad } from '@sveltejs/kit';
import { redirect } from '@sveltejs/kit';

export const load: ServerLoad = async ({ locals }) => {
	if (locals.user) {
		throw redirect(302, '/dashboard');
	} else {
		throw redirect(302, '/login');
	}
};
